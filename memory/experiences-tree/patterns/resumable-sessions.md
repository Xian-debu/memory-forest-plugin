---
id: EXP-PAT-0009
type: LEAF
tree: experiences
layer: L3
status: ACTIVE
parent: EXP-ROOT-0000
created: '2026-05-02'
heartbeat: '2026-05-05'
priority: HIGH
owner: claude-code
source:
- PROJ-OLLAM-0001
- PROJ-OLLAM-0001 (hf-mirror download corruption)
tags:
- session-management
- reliability
- network-resilience
- resume
- state-persistence
- download
validations: 2
originSessionId: 38f8c326-0670-4c46-acf2-406e60f168f9
mergedFrom:
- EXP-PAT-0012 (slow-network-large-download — 特化场景并入)
---
# 会话中断恢复模式

## 核心原则
长时间任务必须设计为"可中断-可恢复"。不能假设会话会一直保持连接。

## 三层持久化保证恢复

### L1: 任务状态 → 记忆森林
每次任务中断前，必须将以下信息写入 memory:
- 当前状态（完成了什么、正在做什么）
- 下一步是什么
- 阻塞项
- 心跳时间戳

### L2: 大文件下载 → .part + wget -c
大文件下载必须:
1. 写 .part 文件而非直接写最终文件
2. 用 wget -c 替代 urllib（wget 自动处理断线重连、续传、退避等待）
3. 下载完成后用 GGUF 头解析验证文件完整性（tensor offset < file size）
4. 验证通过后再 rename 为最终文件

为什么不用 urllib: `urlopen(timeout=120)` 在低速网络（< 1 MB/s）下只能传 ~12-60 MB。大文件（> 5 GB）必定超时。wget 的 `-c -t N --timeout=600 --waitretry=30` 组合可以无人值守完成下载。

### L3: 下载后验证 → 不信任文件大小
文件大小正确 ≠ 文件完整。本次 hf-mirror 下载的所有 GGUF 文件大小正确但 tensor 数据损坏。
- 下载后必须解析 GGUF 头，遍历所有 tensor offset 确认在文件范围内
- 记录预期文件大小（从官方源获取），下载后对比
- ollama 加载失败时优先怀疑文件损坏（而非版本兼容性）

## 验证记录
- 第 1 次 (2026-05-02): .part 续传成功恢复 3.4 GB，节省 ~5 小时
- 第 2 次 (2026-05-02): hf-mirror 3 个模型全部损坏，验证脚本捕获 → 升级为 L3 带 GGUF 验证

## 适用场景
- 任何超过 10 分钟的操作
- 大文件下载 (Git LFS, GGUF, Docker 镜像)
- 多步骤构建/部署流水线
- 模型训练/微调

## 反模式
- 在内存中累积状态不写盘
- 直接写最终文件而非 .part 中间文件
- 没有心跳 = 丢失进度 = 被迫从头开始
- 只检查文件大小不检查文件结构 = 伪安全感
- 对 hf-mirror 等镜像站的文件完整性盲目信任

## 经验级别
L3 — 已验证 2 次，覆盖下载+验证两个维度
