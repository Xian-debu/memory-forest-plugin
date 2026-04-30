---
id: EXP-ROOT-0000
type: ROOT
tree: experiences
layer: L4
status: ACTIVE
created: 2026-04-30
heartbeat: 2026-04-30
priority: HIGH
owner: claude-code
children:
  - EXP-CORE-0001
  - EXP-CORE-0002
  - EXP-CORE-0003
  - EXP-CORE-0004
  - EXP-CORE-0005
  - EXP-CORE-0006
originSessionId: 439d65d5-aade-426e-807f-de0013c8a345
---
# 经验池树 — 根源节点

## 目标
存储从所有项目中提炼的核心经验，分为 L3（跨项目模式）和 L4（核心原则）。

## 当前状态
- 已初始化
- 6 条核心行为准则已写入 (EXP-CORE-0001 ~ 0006)
- L3 patterns 目录: 空
- L4 core 目录: 6 条

## 经验索引
- [EXP-CORE-0001](core/behavior-rule-1.md) — 反驳-确认模式
- [EXP-CORE-0002](core/behavior-rule-2.md) — 三次重复即自省
- [EXP-CORE-0003](core/behavior-rule-3.md) — 五次失败即停止
- [EXP-CORE-0004](core/behavior-rule-4.md) — 经验迭代合并与垃圾识别
- [EXP-CORE-0005](core/behavior-rule-5.md) — 自我迭代与自我提示
- [EXP-CORE-0006](core/behavior-rule-6.md) — 搜索优先，不重复造车轮

## 经验升级规则
- L2 → L3: 项目完成时提炼
- L3 → L4: 3 个以上项目验证 或 用户确认为核心

## 容量上限
- L3 patterns: ≤ 50 条
- L4 core: ≤ 20 条
- 超限时按 (引用次数 × 最新心跳) 排序淘汰
