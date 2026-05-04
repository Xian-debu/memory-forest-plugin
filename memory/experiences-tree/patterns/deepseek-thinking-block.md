---
id: EXP-PAT-0007
type: EXPERIENCE
tree: experiences
layer: L3
status: ACTIVE
created: 2026-05-01
heartbeat: '2026-05-05'
priority: HIGH
owner: claude-code
tags:
- deepseek
- tokens
- thinking-block
- max-tokens
- api
source: PROJECTS-BRANCH-0001
originSessionId: a7664e14-d841-48de-acfa-f9d0da11efe2
---
# DeepSeek V4 Thinking Block 的 Token 消耗

## 触发条件
使用 DeepSeek API（Anthropic-compatible endpoint），设置 `max_tokens=200` 进行代码审查，返回结果只有 thinking 没有 text。

## 问题
DeepSeek V4 系列模型在生成回复时，会先产生一个 `type: "thinking"` 的 content block（内部推理过程），再产生 `type: "text"` 的实际回复。两个 block 共享 `max_tokens` 预算。如果 `max_tokens` 设置过低，thinking block 会耗尽所有预算，导致 text block 为空。

API 响应结构：
```json
{
  "content": [
    {"type": "thinking", "thinking": "推理过程...", "signature": "..."},
    {"type": "text", "text": "实际回复..."}
  ]
}
```

## 行动
1. **提高 `max_tokens` 默认值**: 从常见的 256/512 提升到 2048，确保 thinking + text 都有空间
2. **提取 text block 时按 type 过滤**: 遍历 `content` 数组，只取 `type == "text"` 的 block，不要硬编码索引 `[0]`
3. **在 CLI 工具中设置合理的默认值**: 交互式场景用 2048，简单任务（翻译/摘要）可用 1024
4. **当只有 thinking 无 text 时，提示用户增大 max_tokens 而非静默返回空**

## 结果
使用 `max_tokens=2048` 后，所有场景（chat/review/summarize/translate）稳定返回完整的 thinking + text。

## 反例
- `result["content"][0]["text"]` → content[0] 是 thinking 块，没有 text 字段，KeyError
- 设置 `max_tokens=200` 做代码审查 → thinking 消耗全部 tokens，text 为空
- 忽略 thinking 块的存在直接取 text → 看似有时能工作（当 thinking 很短时），实际不可靠

## 关键要点
- DeepSeek V4 的 thinking block 是推理过程，长度不定，与 text 共享 `max_tokens`
- 永远按 `type == "text"` 过滤 content 数组，不要假设索引位置
- 默认 `max_tokens` 至少 2048 用于复杂任务，1024 用于简单任务
- 此行为可能在其他支持 "thinking/reasoning" 的模型中也存在

## 来源
从 PROJECTS-BRANCH-0001 (n8n工作流系统搭建) 中调试 AI CLI 时发现
