[English](../codebase_analysis.md)

> **测试专用**

# FastDeploy 代码库主要功能分析

## 项目概述

**FastDeploy** 是基于飞桨（PaddlePaddle）的大语言模型（LLM）与视觉语言模型（VLM）推理部署工具包，提供生产级的开箱即用部署方案。项目遵循 Apache 2.0 开源协议，支持 Linux 平台，Python 版本要求 3.10 至 3.12。

---

## 代码库整体结构

```
FastDeploy/
├── fastdeploy/              # 主 Python 包（核心功能模块）
│   ├── engine/              # 推理引擎
│   ├── model_executor/      # 模型执行器（模型架构与前向计算）
│   ├── input/               # 输入处理（分词、预处理）
│   ├── cache_manager/       # KV 缓存管理
│   ├── scheduler/           # 请求调度器
│   ├── spec_decode/         # 投机解码
│   ├── worker/              # 硬件特定的模型执行进程
│   ├── router/              # 请求路由与负载均衡
│   ├── entrypoints/         # 对外接口（API、CLI）
│   ├── distributed/         # 分布式推理支持
│   ├── plugins/             # 插件系统
│   ├── metrics/             # 性能指标采集
│   ├── logger/              # 结构化日志
│   └── config.py            # 全局配置管理
├── custom_ops/              # 硬件特定自定义算子
├── docs/                    # 文档
├── examples/                # 使用示例
├── tests/                   # 测试套件
├── benchmarks/              # 性能基准测试
└── scripts/                 # 工具脚本
```

---

## 核心功能模块分析

### 1. 推理引擎（`fastdeploy/engine/`）

推理引擎是整个系统的调度核心，负责管理工作进程、协调模型初始化与请求生成。

| 文件 | 主要功能 |
|---|---|
| `engine.py` | `LLMEngine` 主类，管理工作进程生命周期与请求生成 |
| `common_engine.py` | `EngineService` 类，负责分布式引擎操作 |
| `args_utils.py` | 引擎参数解析与配置管理 |
| `request.py` | `Request`/`RequestOutput` 数据结构，追踪提示词与补全结果 |
| `sampling_params.py` | 采样参数管理（temperature、top_p、top_k 等） |
| `async_llm.py` | 异步 LLM 推理接口 |
| `resource_manager.py` | GPU/内存资源管理 |
| `sched/` | 请求调度子模块 |

### 2. 模型执行器（`fastdeploy/model_executor/`）

实现各种模型架构的前向计算，包含硬件特定优化的神经网络层。

#### 支持的模型架构

| 模型系列 | 主要变体 |
|---|---|
| ERNIE-4.5 | 300B-A47B（含 MoE 与 MTP）、21B-A3B、0.3B |
| ERNIE-VL | 424B-A47B、28B-A3B（视觉语言多模态） |
| QWEN3 / QWEN3-MoE | 235B、32B、14B、8B 等 |
| QWEN2.5 / QWEN2 | 72B、32B、14B、7B、1.5B 等 |
| QWEN-VL / QWEN3-VL | 视觉语言多模态版本 |
| DeepSeek V3 / R1 | 大规模稀疏 MoE 架构 |
| GLM-4.5 / 4.6 | Air 版本及 MoE 版本 |
| PaddleOCR-VL | OCR 专向视觉语言模型 |

#### 优化层（`layers/`）

- **`linear.py`**：支持多种量化格式的线性层（W4A8、W8A8、FP8 等）
- **`attention/`**：FlashAttention、PagedAttention 注意力机制
- **`normalization.py`**：RMSNorm、LayerNorm 归一化实现
- **`rotary_embedding.py`**：旋转位置编码（RoPE）
- **`quantization/`**：量化支持（W4A8、W8A8、FP8 等）
- **`moe/`**：专家混合（MoE）层
- **`backends/`**：硬件特定后端（GPU、XPU、DCU、GCU 等）

### 3. 输入处理（`fastdeploy/input/`）

负责不同模型的分词与输入预处理。

- **`text_processor.py`**：通用文本处理，支持聊天模板
- **`ernie4_5_processor.py`**：ERNIE-4.5 文本分词器
- **`ernie4_5_vl_processor/`**：ERNIE-VL 视觉语言输入处理（图像编码、特征提取）
- **`qwen_vl_processor/`**、**`qwen3_vl_processor/`**、**`paddleocr_vl_processor/`**：各模型视觉语言处理器

### 4. KV 缓存管理（`fastdeploy/cache_manager/`）

管理键值缓存（KV Cache）的存储与传输，是高效注意力计算的关键。

| 组件 | 功能 |
|---|---|
| `prefix_cache_manager.py` | 前缀缓存，复用重复的提示词 token |
| `cache_transfer_manager.py` | 管理跨设备 KV 缓存传输（NVLink/RDMA） |
| `cache_messager.py` | 缓存操作的消息传递 |
| `multimodal_cache_manager.py` | 多模态输入的缓存管理 |
| `transfer_factory/` | 支持 RDMA/NVLink 的缓存传输协议工厂 |

**关键特性**：
- 统一 KV 缓存传输协议
- 智能硬件选择（RDMA vs NVLink）
- 上下文缓存与动态角色切换

### 5. 请求调度器（`fastdeploy/scheduler/`）

管理请求调度、动态批处理与资源分配。

| 调度器 | 功能 |
|---|---|
| `global_scheduler.py` | 全局调度器，协调所有工作进程 |
| `local_scheduler.py` | 单工作进程的本地调度 |
| `splitwise_scheduler.py` | PD 分离部署的负载均衡调度器 |
| `dp_scheduler.py` | 数据并行调度策略 |

**核心能力**：动态批处理、Token 级调度、多 GPU 负载均衡、上下文窗口管理。

### 6. 投机解码（`fastdeploy/spec_decode/`）

实现多种加速 Token 生成的解码策略。

| 算法 | 文件 | 说明 |
|---|---|---|
| 多 Token 预测（MTP） | `mtp.py` | 并行预测多个 token，显著加速生成速度 |
| 后缀验证 | `suffix.py` | 基于后缀匹配的投机 token 验证 |
| N-gram 预测 | `ngram.py` | 基于 N-gram 的草稿模型预测 |

### 7. 工作进程（`fastdeploy/worker/`）

各硬件平台专属的模型执行进程，负责实际的推理计算。

| 工作进程 | 目标硬件 |
|---|---|
| `gpu_model_runner.py` | NVIDIA GPU（CUDA 优化） |
| `xpu_model_runner.py` | 昆仑芯 XPU |
| `metax_model_runner.py` | 沐曦 GPU |
| `hpu_model_runner.py` | 英特尔 Gaudi HPU |
| `gcu_model_runner.py` | 燧原 GCU |
| `iluvatar_model_runner.py` | 天数智芯 GPU |
| `dcu_model_runner.py` | 海光 DCU |

### 8. 请求路由（`fastdeploy/router/`）

提供请求路由与多实例负载均衡。

- **Python 路由器**：基于 Python 的路由实现
- **Go 路由器**（`golang_router/`）：高性能 Go 语言路由组件
- 支持 vLLM 兼容路由 API

### 9. 对外接口（`fastdeploy/entrypoints/`）

提供用户友好的 API 接口与命令行工具。

- **`llm.py`**：高层 `LLM` 类，支持离线批量推理
- **`api_server.py`**：OpenAI 兼容 API 服务器启动入口
- **`engine_client.py`**：与推理引擎通信的客户端
- **`openai/`**：OpenAI API 兼容层（与 vLLM 接口兼容）
- **`cli/`**：命令行工具

**使用示例**：

```python
from fastdeploy import LLM, SamplingParams

llm = LLM(model="ERNIE-4.5-0.3B", tensor_parallel_size=1)
outputs = llm.chat(messages, SamplingParams(top_p=0.95, max_tokens=512))
```

---

## 推理与部署流水线

```
用户接口层（LLM API / OpenAI 接口 / CLI）
         │
推理引擎层（LLMEngine）
  ├─ 请求管理
  ├─ 进程编排
  └─ 健康监控
         │
调度器（Scheduler）
  ├─ 请求队列与优先级
  ├─ 动态批处理
  └─ 负载均衡
         │
KV 缓存管理器（Cache Manager）
  ├─ KV Cache 存储
  ├─ 前缀缓存复用
  └─ 跨设备缓存传输（RDMA/NVLink）
         │
工作进程（Worker）
  ├─ 模型执行（GPU/XPU/DCU 等）
  └─ 投机解码（MTP/N-gram）
         │
模型执行器（Model Executor）
  ├─ 模型前向计算
  ├─ 量化层执行
  └─ 注意力机制（FlashAttention/PagedAttention）
```

---

## 核心技术特性

### 1. 负载均衡式 PD 分离（Prefill-Decode Disaggregation）

将预填充（Prefill）和解码（Decode）阶段分离到不同实例上，支持上下文缓存与动态实例角色切换，在保障 SLO 达标率和吞吐量的同时优化资源利用率。

### 2. 统一 KV 缓存传输

轻量级高性能传输库，自动选择最优传输路径（NVLink 或 RDMA），降低跨节点缓存传输延迟。

### 3. 全量化格式支持

| 量化格式 | 说明 |
|---|---|
| W8A16 | 权重 8 位、激活 16 位 |
| W8A8 | 权重与激活均为 8 位 |
| W4A16 | 权重 4 位、激活 16 位 |
| W4A8 | 权重 4 位、激活 8 位 |
| W2A16 | 权重 2 位、激活 16 位 |
| FP8 | 8 位浮点量化 |
| W4A8C8 | 权重 4 位、激活与缓存 8 位 |

### 4. 高级加速技术

- **投机解码（Speculative Decoding）**：通过草稿模型生成候选 token，并行验证，加速生成速度
- **多 Token 预测（MTP）**：单次前向推理同时预测多个 token
- **分块预填充（Chunked Prefill）**：将长上下文预填充分块处理，降低首字延迟（TTFT）
- **CUDA Graph**：通过图捕获消除 CUDA 调用开销，提升小批量推理吞吐

### 5. 多硬件支持

| 硬件平台 | 厂商 |
|---|---|
| NVIDIA GPU | NVIDIA |
| 昆仑芯 XPU | 昆仑芯科技 |
| 海光 DCU | 海光信息 |
| 天数 GPU | 天数智芯 |
| 燧原 GCU | 燧原科技 |
| 沐曦 GPU | 沐曦 |
| 英特尔 Gaudi | Intel |

---

## 插件与扩展系统（`fastdeploy/plugins/`）

FastDeploy 提供灵活的插件系统，支持以下扩展点：

- **输入处理器**：自定义分词与预处理逻辑
- **模型注册表**：注册自定义模型架构
- **Token 处理器**：自定义输出 token 后处理
- **推理解析器**：结构化推理链解析
- **工具解析器**：Function Calling 工具调用解析

---

## 可观测性

- **`metrics/`**：Prometheus 集成的性能指标采集（吞吐、延迟、缓存命中率等）
- **`logger/`**：结构化日志与分布式追踪
- **`trace/`**：分布式链路追踪支持
- **`collect_env.py`**：系统环境信息采集，便于问题排查

---

## 构建与测试

- **`setup.py`** / **`pyproject.toml`**：Python 包安装配置
- **`build.sh`**：一键构建脚本
- **`tests/`**：测试套件
- **`benchmarks/`**：性能基准测试脚本
- **`dockerfiles/`**：各硬件平台 Docker 镜像配置
- **`mkdocs.yml`**：文档站点构建配置

---

## 总结

FastDeploy 是一个面向生产环境的 LLM/VLM 推理部署平台，其核心价值体现在：

1. **高性能**：通过 PD 分离、KV 缓存、投机解码、量化等多层次优化，最大化推理吞吐量并降低延迟。
2. **易用性**：提供兼容 OpenAI API 与 vLLM 接口的服务端，单命令即可完成部署。
3. **广泛的模型支持**：覆盖 ERNIE、QWEN、DeepSeek、GLM 等主流大语言模型及视觉语言模型。
4. **多硬件兼容**：抽象统一的工作进程接口，屏蔽底层硬件差异，支持 7 种以上硬件平台。
5. **生产级可靠性**：完善的调度、缓存、路由与可观测性体系，满足企业级部署需求。
