[简体中文](zh/codebase_analysis.md)

# FastDeploy Codebase — Main Functionality Analysis

## Project Overview

**FastDeploy** is an inference and deployment toolkit for Large Language Models (LLMs) and Visual Language Models (VLMs) built on PaddlePaddle. It delivers production-ready, out-of-the-box deployment solutions and is released under the Apache 2.0 license. It supports Linux and requires Python 3.10–3.12.

---

## Repository Structure

```
FastDeploy/
├── fastdeploy/              # Main Python package (core functional modules)
│   ├── engine/              # Inference engine
│   ├── model_executor/      # Model executor (model architectures & forward passes)
│   ├── input/               # Input processing (tokenization, preprocessing)
│   ├── cache_manager/       # KV cache management
│   ├── scheduler/           # Request scheduler
│   ├── spec_decode/         # Speculative decoding
│   ├── worker/              # Hardware-specific model runner processes
│   ├── router/              # Request routing & load balancing
│   ├── entrypoints/         # Public APIs (OpenAI server, CLI)
│   ├── distributed/         # Distributed inference support
│   ├── plugins/             # Plugin system
│   ├── metrics/             # Performance metrics collection
│   ├── logger/              # Structured logging
│   └── config.py            # Global configuration management
├── custom_ops/              # Hardware-specific custom operators
├── docs/                    # Documentation
├── examples/                # Usage examples
├── tests/                   # Test suite
├── benchmarks/              # Performance benchmarking scripts
└── scripts/                 # Utility scripts
```

---

## Core Functional Module Analysis

### 1. Inference Engine (`fastdeploy/engine/`)

The inference engine is the orchestration core of the entire system. It manages worker processes, coordinates model initialization, and drives the request generation loop.

| File | Main Function |
|---|---|
| `engine.py` | `LLMEngine` main class — manages worker process lifecycles and request generation |
| `common_engine.py` | `EngineService` class — handles distributed engine operations |
| `args_utils.py` | Engine argument parsing and configuration management |
| `request.py` | `Request`/`RequestOutput` data structures for tracking prompts and completions |
| `sampling_params.py` | Sampling parameter management (temperature, top_p, top_k, etc.) |
| `async_llm.py` | Asynchronous LLM inference interface |
| `resource_manager.py` | GPU/memory resource management |
| `sched/` | Request scheduling sub-module |

### 2. Model Executor (`fastdeploy/model_executor/`)

Implements model architecture forward passes with hardware-specific optimized neural network layers.

#### Supported Model Architectures

| Model Family | Key Variants |
|---|---|
| ERNIE-4.5 | 300B-A47B (with MoE & MTP), 21B-A3B, 0.3B |
| ERNIE-VL | 424B-A47B, 28B-A3B (vision-language multimodal) |
| QWEN3 / QWEN3-MoE | 235B, 32B, 14B, 8B, etc. |
| QWEN2.5 / QWEN2 | 72B, 32B, 14B, 7B, 1.5B, etc. |
| QWEN-VL / QWEN3-VL | Vision-language multimodal variants |
| DeepSeek V3 / R1 | Large-scale sparse MoE architecture |
| GLM-4.5 / 4.6 | Air variant and MoE variant |
| PaddleOCR-VL | OCR-focused vision-language model |

#### Optimized Layers (`layers/`)

- **`linear.py`**: Quantized linear layers supporting multiple formats (W4A8, W8A8, FP8, etc.)
- **`attention/`**: FlashAttention and PagedAttention mechanisms
- **`normalization.py`**: RMSNorm and LayerNorm implementations
- **`rotary_embedding.py`**: Rotary Position Embeddings (RoPE)
- **`quantization/`**: Quantization support (W4A8, W8A8, FP8, etc.)
- **`moe/`**: Mixture of Experts (MoE) layers
- **`backends/`**: Hardware-specific backends (GPU, XPU, DCU, GCU, etc.)

### 3. Input Processing (`fastdeploy/input/`)

Handles tokenization and input preprocessing for different models.

- **`text_processor.py`**: Generic text processing with chat template support
- **`ernie4_5_processor.py`**: ERNIE-4.5 text tokenizer
- **`ernie4_5_vl_processor/`**: ERNIE-VL vision-language input processing (image encoding, feature extraction)
- **`qwen_vl_processor/`**, **`qwen3_vl_processor/`**, **`paddleocr_vl_processor/`**: Model-specific VL processors

### 4. KV Cache Management (`fastdeploy/cache_manager/`)

Manages Key-Value (KV) cache storage and transfer for efficient attention computation.

| Component | Function |
|---|---|
| `prefix_cache_manager.py` | Prefix caching to reuse repeated prompt tokens |
| `cache_transfer_manager.py` | Manages cross-device KV cache transfers (NVLink/RDMA) |
| `cache_messager.py` | Message passing for cache operations |
| `multimodal_cache_manager.py` | Cache management for multimodal inputs |
| `transfer_factory/` | Factory for RDMA/NVLink cache transfer protocols |

**Key Capabilities**: Unified KV Cache Transmission Protocol, intelligent hardware selection (RDMA vs NVLink), context caching with dynamic role switching.

### 5. Request Scheduler (`fastdeploy/scheduler/`)

Manages request scheduling, dynamic batching, and resource allocation.

| Scheduler | Function |
|---|---|
| `global_scheduler.py` | Global scheduler coordinating all worker processes |
| `local_scheduler.py` | Per-worker local scheduling |
| `splitwise_scheduler.py` | Load-balancing scheduler for PD-disaggregated deployments |
| `dp_scheduler.py` | Data-parallel scheduling strategy |

**Core Capabilities**: Dynamic batching, token-level scheduling, multi-GPU load balancing, context window management.

### 6. Speculative Decoding (`fastdeploy/spec_decode/`)

Implements advanced decoding strategies to accelerate token generation.

| Algorithm | File | Description |
|---|---|---|
| Multi-Token Prediction (MTP) | `mtp.py` | Predicts multiple tokens in parallel to significantly accelerate generation |
| Suffix Verification | `suffix.py` | Verifies speculative tokens via suffix matching |
| N-gram Prediction | `ngram.py` | Draft model prediction based on N-gram statistics |

### 7. Worker Processes (`fastdeploy/worker/`)

Hardware-specific model runner processes responsible for the actual inference computation.

| Worker | Target Hardware |
|---|---|
| `gpu_model_runner.py` | NVIDIA GPU (CUDA optimized) |
| `xpu_model_runner.py` | Kunlunxin XPU |
| `metax_model_runner.py` | MetaX GPU |
| `hpu_model_runner.py` | Intel Gaudi HPU |
| `gcu_model_runner.py` | Enflame GCU |
| `iluvatar_model_runner.py` | Iluvatar GPU |
| `dcu_model_runner.py` | Hygon DCU |

### 8. Request Router (`fastdeploy/router/`)

Provides request routing and multi-instance load balancing.

- **Python Router**: Python-based routing implementation
- **Go Router** (`golang_router/`): High-performance Go-based router component
- Compatible with vLLM routing API

### 9. Public Entrypoints (`fastdeploy/entrypoints/`)

User-facing API interfaces and command-line tools.

- **`llm.py`**: High-level `LLM` class for offline batch inference
- **`api_server.py`**: OpenAI-compatible API server startup entry point
- **`engine_client.py`**: Client for communicating with the inference engine
- **`openai/`**: OpenAI API compatibility layer (vLLM interface compatible)
- **`cli/`**: Command-line interface tools

**Usage Example**:

```python
from fastdeploy import LLM, SamplingParams

llm = LLM(model="ERNIE-4.5-0.3B", tensor_parallel_size=1)
outputs = llm.chat(messages, SamplingParams(top_p=0.95, max_tokens=512))
```

---

## Inference and Deployment Pipeline

```
User Interface Layer (LLM API / OpenAI Server / CLI)
         │
Inference Engine Layer (LLMEngine)
  ├─ Request management
  ├─ Process orchestration
  └─ Health monitoring
         │
Scheduler
  ├─ Request queuing & prioritization
  ├─ Dynamic batching
  └─ Load balancing
         │
KV Cache Manager
  ├─ KV cache storage
  ├─ Prefix cache reuse
  └─ Cross-device cache transfer (RDMA/NVLink)
         │
Worker Process
  ├─ Model execution (GPU/XPU/DCU, etc.)
  └─ Speculative decoding (MTP/N-gram)
         │
Model Executor
  ├─ Model forward pass
  ├─ Quantized layer execution
  └─ Attention (FlashAttention/PagedAttention)
```

---

## Core Technical Features

### 1. Load-Balanced PD Disaggregation

Separates the Prefill and Decode phases onto different instances. Supports context caching and dynamic instance role switching, optimizing resource utilization while meeting SLO targets and throughput requirements.

### 2. Unified KV Cache Transmission

A lightweight, high-performance transport library that automatically selects the optimal path (NVLink or RDMA), minimizing cross-node cache transfer latency.

### 3. Comprehensive Quantization Support

| Format | Description |
|---|---|
| W8A16 | 8-bit weights, 16-bit activations |
| W8A8 | 8-bit weights and activations |
| W4A16 | 4-bit weights, 16-bit activations |
| W4A8 | 4-bit weights, 8-bit activations |
| W2A16 | 2-bit weights, 16-bit activations |
| FP8 | 8-bit floating-point quantization |
| W4A8C8 | 4-bit weights, 8-bit activations and cache |

### 4. Advanced Acceleration Techniques

- **Speculative Decoding**: Draft model generates candidate tokens that are verified in parallel to accelerate generation.
- **Multi-Token Prediction (MTP)**: Predicts multiple tokens in a single forward pass.
- **Chunked Prefill**: Splits long-context prefill into chunks to reduce Time to First Token (TTFT).
- **CUDA Graph**: Captures and replays CUDA execution graphs to eliminate kernel launch overhead, improving small-batch throughput.

### 5. Multi-Hardware Support

| Hardware | Vendor |
|---|---|
| NVIDIA GPU | NVIDIA |
| Kunlunxin XPU | Kunlunxin Technology |
| Hygon DCU | Hygon |
| Iluvatar GPU | Iluvatar CoreX |
| Enflame GCU | Enflame Technology |
| MetaX GPU | MetaX |
| Intel Gaudi | Intel |

---

## Plugin and Extension System (`fastdeploy/plugins/`)

FastDeploy provides a flexible plugin system with the following extension points:

- **Input Processors**: Custom tokenization and preprocessing logic
- **Model Registry**: Register custom model architectures
- **Token Processors**: Custom output token post-processing
- **Reasoning Parsers**: Structured reasoning chain parsing
- **Tool Parsers**: Function Calling / tool invocation parsing

---

## Observability

- **`metrics/`**: Prometheus-integrated performance metric collection (throughput, latency, cache hit rate, etc.)
- **`logger/`**: Structured logging and distributed tracing
- **`trace/`**: Distributed trace support
- **`collect_env.py`**: System environment information collection for troubleshooting

---

## Build and Test Infrastructure

- **`setup.py`** / **`pyproject.toml`**: Python package installation configuration
- **`build.sh`**: One-click build script
- **`tests/`**: Test suite
- **`benchmarks/`**: Performance benchmarking scripts
- **`dockerfiles/`**: Docker image configurations for different hardware platforms
- **`mkdocs.yml`**: Documentation site build configuration

---

## Summary

FastDeploy is a production-grade LLM/VLM inference and deployment platform. Its core value is:

1. **High Performance**: Multi-level optimizations including PD disaggregation, KV caching, speculative decoding, and quantization maximize throughput and minimize latency.
2. **Ease of Use**: OpenAI API and vLLM-compatible server interface enables single-command deployment.
3. **Broad Model Support**: Covers mainstream LLMs and VLMs including ERNIE, QWEN, DeepSeek, and GLM families.
4. **Multi-Hardware Compatibility**: A unified worker process abstraction hides hardware differences and supports 7+ hardware platforms.
5. **Production-Grade Reliability**: Comprehensive scheduling, caching, routing, and observability systems meet enterprise deployment requirements.
