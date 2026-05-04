---
id: PROJ-OLLAM-0001
type: BRANCH
tree: projects
layer: L2
status: ACTIVE
parent: PROJ-ROOT-0000
subordinate_to: PHIL-ROOT-0000
children: []
created: '2026-05-01'
heartbeat: '2026-05-05'
priority: HIGH
owner: claude-code
originSessionId: 3a037550-696c-44a7-9c0e-a74f1d1eead7
resumeSessionId: 38f8c326-0670-4c46-acf2-406e60f168f9
tags:
- ollama
- local-ai
- nvidia
- cuda
- embedding
- code-search
- gguf
- hf-mirror
---
# 本地 AI 模型系统搭建

## 目标
基于 RTX 5070 + Ollama 搭建本地 AI 模型系统，增强 Claude Code 能力。

## 当前状态 (2026-05-02 21:00)

### 模型状态
| 模型 | 大小 | 状态 |
|------|------|------|
| nomic-embed-text | 84 MB | 完成，API验证通过 (768维, norm=1.0) |
| qwen2.5-coder:14b | ~7.7 GB | 需重新下载 (上次文件损坏) |
| qwen2.5:32b | ~12.5 GB | 需重新下载 (上次文件损坏) |
| minicpm-v:8b | ~1.6 GB | 需重新下载 (上次文件损坏) |
| ~~qwen3:8b~~ | 已删除 | 被新模型替代，节省 5.2 GB |

### 2026-05-02 腐败诊断
- hf-mirror 下载的 3 个 GGUF 全部损坏: tensor offset > file size
- SHA256 一致但文件内容截断 — 镜像端可能已有问题
- 症状: ollama 加载时报 "data is not within the file bounds"
- 根因: 低速网络下 urllib 脚本 timeout=120s 太短，反复超时导致文件不完整
- 修复: download_verified.py 新脚本 (wget -c + GGUF 头解析验证 + 预期大小检查)

### 2026-05-02 网络中断
- 19:31:29 系统时钟跳变 → 19:37:26 SSH 重启 → WSL2 NAT 损坏 → DNS 失效
- ipykernel 训练进程 (PID 313712, FreqNet bayes_to_training) 幸存, 78+ CPU 分钟
- WSL2 平台稳定性问题，非 SSH 配置问题

## 硬件环境
- CPU: Intel Core Ultra 7 255HX (20 核, Arrow Lake)
- GPU: NVIDIA RTX 5070 8GB (Blackwell, CC 12.0, CUDA 13.1)
- RAM: 32GB WSL2, 可用扩展到 80GB+
- WSL2 GPU-PV: /usr/lib/wsl/lib/nvidia-smi 可用
- Ollama: v0.12.10 (旧版, CUDA 已工作)
- 磁盘: 884 GB 可用 / 1007 GB

### 网络约束
- GitHub 被墙，ollama.com 极慢 (~20 KB/s)
- hf-mirror.com ~300-800 KB/s 但文件可能损坏
- 网络更新后可尝试 ollama pull (官方 registry 有完整性验证)

## 关键决策

### 模型功能分配 (/root/.claude/scripts/local_ai.py:24-27)
| 模型 | 常量 | 功能 | 命令 |
|------|------|------|------|
| nomic-embed-text | EMBED_MODEL | 语义搜索/嵌入 | lai search / lai embed |
| qwen2.5-coder:14b | CODE_MODEL | 代码审查 | lai review --diff |
| qwen2.5:32b | HEAVY_MODEL | 通用对话 | lai chat |
| minicpm-v:8b | VISION_MODEL | 图像分析 | lai vision |

### 下载策略演进
1. urllib 脚本 (download_and_import.py) → timeout=120s 太短, 已删除
2. wget 手动续传 → 文件完整但内容损坏 (镜像端问题)
3. download_verified.py → wget + GGUF头验证 + 预期大小检查 (当前方案)
4. ollama pull → 网络更新后优先使用 (官方源有完整性保证)

## 交付物

### 模型管理
- `/root/models/download_verified.py` — 带完整性验证的下载+导入脚本 ⭐
- `/root/models/gguf/` — GGUF 模型存储 (当前仅 nomic-embed-text)
- `/root/models/modelfiles/` — Ollama Modelfiles

### CLI 工具
- `/root/.claude/scripts/local_ai.py` — 本地 AI 工具集 (7 条命令)
- Shell 别名: lai / local-ai / lais / lair

### 代码索引
- `/root/.local-ai/index/code_index.pkl` — 2708 文件, 7035 代码块 (51MB)
- 已知: 索引范围过大，含 node_modules/myenv 噪音, 待优化

### 下载指南
- `/root/model_download_guide.txt` — 完整下载+验证+功能分配说明

## 待完成
- [x] nomic-embed-text 下载 + 导入 + 验证
- [x] 清理旧 qwen3:8b
- [x] 诊断 GGUF 腐败根因 + 修复下载脚本
- [ ] 下载 qwen2.5-coder:14b (网络更新后)
- [ ] 下载 qwen2.5:32b (网络更新后)
- [ ] 下载 minicpm-v:8b (网络更新后)
- [ ] 全部验证通过后重建代码索引
- [ ] 优化索引范围 (排除 node_modules, myenv, .nvm)
- [ ] 升级 Ollama (等 GitHub 可访问时)

## 阻塞项
- 网络带宽 ≤ 800 KB/s → 大模型下载需 10+ 小时
- hf-mirror 文件完整性存疑 → 每个文件需 GGUF 验证
- GitHub 被墙 → Ollama 无法升级

## 经验提炼
- [EXP-PAT-0009](experiences-tree/patterns/resumable-sessions.md) — 会话中断恢复
- [EXP-PAT-0012](experiences-tree/patterns/slow-network-large-download.md) — 低速大文件下载
