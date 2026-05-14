---
name: preflight-checklist
description: "最短强制前置清单 — 每次诊断/修改前必须执行, 跳过任一步=输出不可靠"
metadata: 
  node_type: memory
  type: system
  layer: L5
  priority: ABSOLUTE
  originSessionId: 20882313-c58a-4336-8abc-c1519c94024d
---

# 前置检查清单 (PREFLIGHT)

以下不是建议。是**每次**诊断/修改/设计前的硬性步骤。
当你准备写代码或声称"有问题"时，逐条核对：

```
☐ 1. 记忆 grep — grep -i "<topic>" /root/.claude/projects/-root/memory/MEMORY.md
     → 命中? Read 相关文件全文，特别关注 "已知限制" "注意" "不要"

☐ 2. 已有测试 — ls *test* *validate* *check* 先跑一遍
     → 全部通过? 你的"有问题"判断大概率是错的

☐ 3. 项目文档 — CLAUDE.md / ROOT.md / README 是否存在?
     → 先读，它可能已经告诉你不要做什么

☐ 4. 网络调研 — 以下任一条件触发:
     - 涉及 2025+ 技术/库/API 行为
     - 记忆无覆盖 + 代码无文档
     - 涉及第三方系统的具体参数/方法
     → ws "query" --text --quick

☐ 5. 形成假设 — 只有 1-4 完成后才能做
     → 假设必须可验证，不是"感觉像"
```

## 反模式 STOP 信号

如果你发现自己在做以下任何事，**立即停止，回到 ☐ 1**:

- 设计自己的测试用例来"诊断问题"
- 因为"这个数字不对"就判断是 bug
- 修改代码超过 3 行而不清楚为什么
- 花超过 3 轮对话在"探索"上而没有查记忆或网络
- ws 用了 `run_in_background`
