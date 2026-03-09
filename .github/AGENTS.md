---
# CI 自动化机器人：自动响应仓库事件，执行智能化CI流程
name: ci-automation-bot
purpose: "自动处理PR和Issue，执行CI检查、标签管理、质量门禁"
triggers:
  - github.event: pull_request.opened      # PR创建时
  - github.event: pull_request.synchronize # PR更新（新提交）时
  - github.event: issues.opened            # Issue创建时
  - github.event: issue_comment.created    # 评论创建时（可监听 /commands）
  - schedule: '0 * * * *'                  # 每小时执行一次（清理陈旧PR）
permissions:
  contents: read                           # 读取代码
  pull_requests: write                      # 添加标签、评论
  issues: write                             # 处理Issue
  checks: read                              # 读取CI检查状态
  actions: read                              # 读取Actions状态
context:
  include:
    - README.md                             # 项目概述
    - .github/workflows/**                   # CI工作流定义
    - .github/label-rules.md                 # 标签规则（如有）
    - "package.json"                          # 依赖信息
guardrails:
  - "Never merge PRs automatically"          # 安全红线
  - "Never push to main branch"              # 绝不直接推送到主分支
  - "Escalate to @maintainers on test failures" # 测试失败时通知维护者
  - "Respect CODEOWNERS for approval"        # 遵守代码所有者规则
---
