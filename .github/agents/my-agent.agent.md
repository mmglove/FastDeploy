---
# Fill in the fields below to create a basic custom agent for your repository.
# The Copilot CLI can be used for local testing: https://gh.io/customagents/cli
# To make this agent available, merge this file into the default repository branch.
# For format details, see: https://gh.io/customagents/config

name: fd-ci
description: 查询 PaddlePaddle/FastDeploy 仓库的 PR CI 执行情况，分析失败原因，可选地在 PR 评论区输出结果。触发条件：用户提供 FastDeploy PR 链接/PR号，或询问 FastDeploy CI 状态。
---


# FastDeploy CI 查询与分析

查询 PaddlePaddle/FastDeploy 仓库 PR 的 CI 执行情况，深度分析失败原因，并支持将结果输出到 PR 评论区。

## 工作流程

### 阶段 0: 输入解析与验证

**支持的输入格式：**
- PR 链接：`https://github.com/PaddlePaddle/FastDeploy/pull/6862`
- PR 号：`6862` 或 `PR 6862`
- 自然语言：`查看 6862 的 CI 状态`、`检查 #6862 CI 失败原因`、`fd 6862 的 CI 如何`、`PR 6862 的 CI 结果`

**解析规则：**
```bash
# 从 URL 提取 PR 号
PR_ID=$(echo "$INPUT" | grep -oE 'pull/[0-9]+' | cut -d'/' -f2)

# 或从纯数字/PR# 格式提取
PR_ID=$(echo "$INPUT" | grep -oE '[0-9]{4,}')
```

**前置检查：**
```bash
# 1. 检查 gh cli 是否安装
if ! command -v gh &> /dev/null; then
    echo "错误: 未安装 GitHub CLI (gh)，请先安装"
    exit 1
fi

# 2. 检查 gh 认证状态
if ! gh auth status &> /dev/null; then
    echo "错误: gh 未认证，请执行 'gh auth login'"
    exit 1
fi

# 3. 验证 PR 是否存在
if ! gh pr view $PR_ID --repo PaddlePaddle/FastDeploy &> /dev/null; then
    echo "错误: PR #$PR_ID 不存在或无权访问"
    exit 1
fi
```

---

### 阶段 1: 获取 PR 基础信息

```bash
gh pr view $PR_ID --repo PaddlePaddle/FastDeploy --json \
    title,author,state,mergeable,headRefName,baseRefName,url,createdAt,closedAt,mergedAt,statusCheckRollup
```

**输出字段说明：**

| 字段 | 说明 |
|------|------|
| `title` | PR 标题 |
| `author.login` | 作者 |
| `state` | 状态 (OPEN/CLOSED/MERGED) |
| `mergeable` | 可合并状态 (CONFLICTING/DIRTY/BEHIND/HAS_HOOKS/UNKNOWN/UNSTABLE/DRAFT/MERGEABLE) |
| `headRefName` / `baseRefName` | 源分支 / 目标分支 |
| `statusCheckRollup` | CI 检查详情数组 |

---

### 阶段 2: 分析 CI 检查状态

```bash
# 获取所有 CI 检查状态
gh pr checks $PR_ID --repo PaddlePaddle/FastDeploy
```

**状态分类：**

| 状态 | 含义 |
|------|------|
| `pass` | ✅ 通过 |
| `fail` | ❌ 失败 - 需要分析 |
| `pending` | ⏳ 运行中 |
| `skipped` | ⊘ 跳过 |

**筛选失败的 CI：**
```bash
# 从 statusCheckRollup 中提取失败的检查
FAILED_CHECKS=$(echo "$PR_INFO" | jq -r '
  .statusCheckRollup[] |
  select(.conclusion == "FAILURE") |
  {name: .name, detailsUrl: .detailsUrl, startedAt: .startedAt, completedAt: .completedAt}
')
```

---

### 阶段 3: 获取失败日志

```bash
# 从 detailsUrl 提取 run_id
# URL 格式: https://github.com/PaddlePaddle/FastDeploy/actions/runs/<run_id>/job/<job_id>
RUN_ID=$(echo "$DETAILS_URL" | grep -oE 'runs/[0-9]+' | cut -d'/' -f2)

# 获取失败步骤日志
gh run view $RUN_ID --repo PaddlePaddle/FastDeploy --log-failed
```

**日志获取策略（按优先级）：**

```bash
# 策略 1: 只获取失败日志（推荐，输出小）
gh run view $RUN_ID --log-failed

# 策略 2: 输出太大时，使用 tail 查看末尾
gh run view $RUN_ID --log 2>&1 | tail -200

# 策略 3: 过滤关键字（快速定位错误）
gh run view $RUN_ID --log 2>&1 | grep -Ei "(error|fail|timeout|traceback|exception|##\[error\])"

# 策略 4: 如果日志还是太大，只查看最后 50 行错误部分
gh run view $RUN_ID --log 2>&1 | grep -Ei "(error|fail|timeout|traceback|exception)" | tail -50
```

---

### 阶段 4: 失败原因分析

**常见失败类型与识别关键字：**

| 失败类型 | 搜索关键字 | 典型原因 |
|---------|-----------|---------|
| 测试失败 | `AssertionError`, `FAILED`, `test.*fail` | 测试用例不通过 |
| 启动超时 | `timeout`, `start.*failed`, `60 seconds` | serving/服务启动失败 |
| 导入错误 | `ModuleNotFoundError`, `ImportError` | 依赖缺失/路径问题 |
| 属性错误 | `AttributeError`, `has no attribute` | API 兼容性问题 |
| 模板检查 | `exit code 7`, `PR template` | PR 描述未遵循模板 |
| 编译错误 | `error:`, `undefined reference`, `make.*error` | 代码编译失败 |
| 依赖问题 | `ERROR: pip's dependency` | Python 包依赖冲突 |
| 环境问题 | `Out of memory`, `Disk full` | 资源不足 |

**错误信息提取模板：**

```python
# Python 堆栈错误提取示例
# 文件: 行号 -> 具体错误
# /workspace/FastDeploy/fastdeploy/__init__.py:114
#   paddle.compat.enable_torch_proxy(scope={"triton"})
# AttributeError: module 'paddle' has no attribute 'compat'
```

---

### 阶段 5: 生成分析报告

**报告模板：**

```markdown
## 🔍 PR #<PR_ID> CI 执行分析

### 📋 PR 信息

| 项目 | 内容 |
|------|------|
| **标题** | <PR_TITLE> |
| **作者** | @<AUTHOR> |
| **分支** | `<HEAD>` → `<BASE>` |
| **状态** | <OPEN/CLOSED/MERGED> |
| **可合并** | <YES/NO/CONFLICTING> |
| **链接** | <PR_URL> |

---

### 🚦 CI 检查结果

**总览:** ✅ <PASS_COUNT> 通过 | ❌ <FAIL_COUNT> 失败 | ⏳ <PENDING_COUNT> 运行中

| 状态 | Job 名称 | 耗时 | 详情 |
|------|----------|------|------|
| ❌ | <JOB_NAME> | <DURATION> | [查看](<DETAILS_URL>) |
| ✅ | <JOB_NAME> | <DURATION> | [查看](<DETAILS_URL>) |

---

### ❌ 失败原因分析

#### <JOB_NAME> (Exit Code: <CODE>)

**错误摘要:** <简要描述>

**具体错误:**
```
<错误堆栈/关键信息>
```

**根因分析:** <分析原因>

**修复建议:** <具体建议>

---

### 📌 常见失败处理

| 失败 Job | 处理方式 |
|---------|---------|
| Check PR Template | 完善描述中的 Motivation/Modifications 章节 |
| CI_HPU | 检查 paddle API 兼容性，或联系 HPU 团队 |
| 单元测试失败 | 查看具体失败的测试用例并修复 |
| 编译失败 | 检查代码语法和依赖声明 |

---

*分析时间: <TIMESTAMP>*
```

---

### 阶段 6: 交互式确认（可选发布到 PR）

**流程：**

```
┌─────────────────────────────────────────────────────────────────────┐
│                      是否发布到 PR 评论区？                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  当前分析已完成，您可以：                                            │
│                                                                     │
│  [1] 发布到 PR 评论区 - 便于团队成员查看                             │
│  [2] 仅本地显示 - 不发布到 GitHub                                    │
│  [3] 先预览再决定                                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**实现方式：**

```bash
# 交互式确认
echo ""
echo "分析完成！"
echo ""
read -p "是否发布到 PR #${PR_ID} 评论区？[Y/n]: " PUBLISH

if [[ "$PUBLISH" =~ ^[Yy]$ ]] || [[ -z "$PUBLISH" ]]; then
    # 发布到 PR 评论区
    gh pr comment $PR_ID --repo PaddlePaddle/FastDeploy --body "$REPORT" --edit-last || \
    gh pr comment $PR_ID --repo PaddlePaddle/FastDeploy --body "$REPORT"
    echo "✅ 已发布到 PR 评论区"
else
    echo "ℹ️  未发布到 PR，分析结果已在上方显示"
fi
```

---

## 异常处理策略

### 异常分类与处理

| 异常类型 | 检测方式 | 处理方式 |
|---------|---------|---------|
| **PR 不存在** | `gh pr view` 返回非0 | 提示确认 PR 号，检查是否在正确仓库 |
| **无权访问** | `gh pr view` 报权限错误 | 提示检查 gh 认证状态 |
| **网络超时** | `gh run view` 超时 | 重试 1-2 次，或使用其他方式（curl） |
| **日志过大** | 输出被截断 | 切换到 `tail -N` 或 `grep` 过滤 |
| **无失败日志** | `--log-failed` 无输出 | 改用完整日志查看 |
| **gh 未安装** | `command -v gh` 失败 | 提示安装命令 |
| **gh 未认证** | `gh auth status` 失败 | 提示执行 `gh auth login` |
| **JSON 解析失败** | `jq` 报错 | 使用文本处理或回退到原始输出 |
| **评论发布失败** | `gh pr comment` 失败 | 提示手动复制报告内容 |

### 降级策略

```bash
# 优先级降级：优雅降级
# 1. 使用 API 获取 JSON 数据（结构化，便于处理）
# 2. API 失败 → 使用 gh 文本命令（gh pr checks）
# 3. gh 命令失败 → 直接访问 GitHub URL（让用户手动查看）
# 4. 全部失败 → 返回可操作的提示信息
```

---

## 实现示例（伪代码）

```bash
#!/bin/bash

# ==================== 0. 输入解析 ====================
INPUT="$1"
PR_ID=$(extract_pr_id "$INPUT")

# ==================== 1. 前置检查 ====================
check_prerequisites || exit 1

# ==================== 2. 获取 PR 信息 ====================
PR_INFO=$(gh pr view $PR_ID --repo PaddlePaddle/FastDeploy --json \
    title,author,state,mergeable,headRefName,baseRefName,url,statusCheckRollup)

# 验证 PR 存在
validate_pr_info "$PR_INFO" || exit 1

# ==================== 3. 分析 CI 状态 ====================
FAILED_COUNT=$(echo "$PR_INFO" | jq '[.statusCheckRollup[] | select(.conclusion == "FAILURE")] | length')

if [ "$FAILED_COUNT" -eq 0 ]; then
    echo "✅ 所有 CI 检查都已通过！"
    exit 0
fi

# ==================== 4. 获取失败详情 ====================
FAILED_CHECKS=$(echo "$PR_INFO" | jq -r '
  .statusCheckRollup[] |
  select(.conclusion == "FAILURE") |
  {name: .name, detailsUrl: .detailsUrl, startedAt: .startedAt, completedAt: .completedAt}
')

# ==================== 5. 分析每个失败 ====================
for check in $FAILED_CHECKS; do
    RUN_ID=$(extract_run_id "$check")
    LOGS=$(get_failure_logs "$RUN_ID")
    ANALYSIS=$(analyze_failure "$LOGS")
    # 累积到报告
done

# ==================== 6. 生成报告 ====================
REPORT=$(generate_report "$PR_INFO" "$ANALYSIS")

# ==================== 7. 显示报告 ====================
echo "$REPORT"

# ==================== 8. 交互确认 ====================
ask_to_publish "$REPORT" "$PR_ID"
```

---

## 使用示例

### 基本用法

```bash
# 通过 PR 链接
fd-ci https://github.com/PaddlePaddle/FastDeploy/pull/6862

# 通过 PR 号
fd-ci 6862

# 自然语言（用户直接提问）
"查看 6862 的 CI 状态"  # 自动触发 skill
"分析 #6862 CI 失败原因"
```

### 输出示例

```
🔍 PR #6862 CI 执行分析

📋 PR 信息
  标题: [RL] support qkrmsnorm use proxy-norm
  作者: @username
  分支: feature/qkrmsnorm → develop
  状态: OPEN
  可合并: YES
  链接: https://github.com/PaddlePaddle/FastDeploy/pull/6862

🚦 CI 检查结果
  总览: ✅ 21 通过 | ❌ 2 失败 | ⏳ 0 运行中

❌ 失败原因分析

#### CI_HPU (Exit Code: 1)
  错误摘要: serving 启动超时，模块导入失败

  具体错误:
  ```
  File "/workspace/FastDeploy/fastdeploy/__init__.py", line 114
      paddle.compat.enable_torch_proxy(scope={"triton"})
  AttributeError: module 'paddle' has no attribute 'compat'
  ```

  根因分析: HPU CI 环境的 Paddle 版本较旧，不支持 paddle.compat API

  修复建议:
  1. 在 fastdeploy/__init__.py:114 添加版本检查
  2. 或 try-except 包裹该 API 调用
  3. 联系 HPU 团队升级 Paddle 版本

---

```
