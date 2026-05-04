---
id: EXP-PAT-0010
name: data-normalize-at-source
description: 数据 pipeline 中在源头统一 shape/格式，下游代码因而可删除脆弱的重解析逻辑
type: LEAF
tree: experiences
layer: L3
status: ACTIVE
parent: EXP-ROOT-0000
heartbeat: '2026-05-05'
originSessionId: dc7b6208-9d01-4be5-a94f-1e85b570f468
---
# 数据源头归一化，下游不需要修复

**规则**: 数据 pipeline 的每一个阶段应该产出格式一致的输出。如果下游需要做变形/重解析来矫正不一致，问题在源头而非下游。

**Why**: 本次框架重构中，`splits.py:_process_and_window` 多通道产出 `[C, L]` 单通道产出 `[L, 1]`，迫使 `dataset.py:__getitem__` 每次调用都做 squeeze/transpose 修复。这浪费每次取样本的 CPU 时间，且逻辑脆弱（依赖 `use_multichannel` 标志做启发式判断）。

**How to apply**: 发现下游代码在做格式修复 → 追溯到上游源头 → 在源头统一格式 → 简化/删除下游修复逻辑。不是"哪个 shape 对"，而是"所有路径产出同一个 shape"。
