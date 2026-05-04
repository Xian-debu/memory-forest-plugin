---
id: MF-ROOT-0000
type: ROOT
tree: forest
layer: L4
status: ACTIVE
created: 2026-04-30
heartbeat: '2026-05-05'
priority: ABSOLUTE
subordinate_to: PHIL-ROOT-0000
children:
- MF-SPEC-0001
- MF-RUNTIME-0002
- SYS-ROOT-0000
- EXP-ROOT-0000
- PROJ-ROOT-0000
core_behaviors:
- EXP-CORE-0001
- EXP-CORE-0002
- EXP-CORE-0003
- EXP-CORE-0004
- EXP-CORE-0005
- EXP-CORE-0006
initialized: true
originSessionId: 439d65d5-aade-426e-807f-de0013c8a345
---
# 记忆森林 — 根源节点

## 这是什么
记忆森林是本环境所有记忆的唯一管理框架。它位于广义指导思想（PHILOSOPHY.md）之上，是一切信息存储与检索的第一系统入口。

**本节点受 PHILOSOPHY.md（L5 绝对底层）约束。**

## 森林结构

```
PHILOSOPHY.md (L5 绝对底层 — 哲学根)
└── forest-root (本节点, L4)
    ├── MF-SPEC-0001          # 记忆森林规范定义
    ├── MF-RUNTIME-0002       # 记忆森林运行时行为
    ├── system-tree/          # 系统配置树
    │   └── ROOT.md
    ├── experiences-tree/     # 核心经验树（跨项目提炼）
    │   └── ROOT.md
    └── projects-tree/        # 项目记忆树
        └── ROOT.md
```

## 优先级法则
1. **PHILOSOPHY.md 是本节点的上层约束，一切冲突以哲学层为准**
2. 会话启动时，PHILOSOPHY.md 首先加载，forest-root 紧随其后
3. forest-root 决定加载哪些树、哪些节点
4. 文档系统是 system-tree 的叶子节点
5. 若 forest-root 与任何其他系统规范冲突，forest-root 胜出（但服从 PHILOSOPHY）

## 当前森林状态
- 森林创建于: 2026-04-30
- 活跃树数量: 4 (forest, system, experiences, projects)
- system-tree: 5 个分支全部建立，17 个 LEAF 已注册，所有任务完成
- experiences-tree: 6 条核心行为准则 (EXP-CORE-0001~0006)
- projects-tree: 1 活跃项目 (framework-refactor Phase 1-4 完成)
- 初始化状态: **已完成** (2026-04-30)
- 待处理心跳: 0
- 垃圾回收周期: 下次会话启动时执行 L0 清理

## 会话启动协议
```
0. 加载 PHILOSOPHY.md (L5 绝对底层) ← 不可跳过，先于一切
1. 读取本节点 (forest-root.md)
2. 加载核心行为准则 (EXP-CORE-0001~0006) ← 不可跳过
3. 执行垃圾回收 (L0 清理)
4. 检查心跳: 遍历活跃树，查找未完成任务
5. 加载 system-tree 配置 (L4 核心规范)
6. 加载当前项目的 memory-path
7. 根据用户任务类型，加载相关节点
```

## 核心行为准则（每次会话强制执行，共6条）
1. **反驳-确认模式**: 调查→驳倒→修正→**等待确认**→执行
2. **三次重复自省**: 同问题 >3次 → 检讨自身 → 报告用户
3. **五次失败停止**: 同障碍 >5次 → 停止 → 报告现象 → 请求介入
4. **经验迭代合并**: 经验持续合并去重 → 识别并清除垃圾经验 → 经验池保持精简
5. **自我迭代提示**: 自主改进基础设施 → **必须告知用户**改了什么/为什么/有何影响
6. **搜索优先偷懒**: 工作前搜索现成方案 → 可复用/借鉴/合并 → **告知用户**→ 确认后执行
