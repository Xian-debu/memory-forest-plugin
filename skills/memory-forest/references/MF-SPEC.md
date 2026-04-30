---
id: MF-SPEC-0001
type: BRANCH
tree: forest
layer: L4
status: ACTIVE
parent: MF-ROOT-0000
created: 2026-04-30
heartbeat: 2026-04-30
priority: ABSOLUTE
originSessionId: 439d65d5-aade-426e-807f-de0013c8a345
---
# 记忆森林规范定义

## 1. 核心概念

### 1.1 记忆森林 (Memory Forest)
所有记忆的顶层容器。包含若干棵**记忆树**，每棵树有独立的根源节点和生命周期。

### 1.2 记忆树 (Memory Tree)
以单一**根源节点**为入口的记忆层级结构。每棵树代表一个独立上下文域（一个项目、一个系统、一个经验池）。

### 1.3 记忆节点 (Memory Node)
记忆的基本存储单元。每个节点是一个 Markdown 文件，通过 frontmatter 声明元数据，正文承载记忆内容。

## 2. 节点类型系统

| 类型 | 标识 | 含义 | 可有子节点 | 可有任务 |
|------|------|------|-----------|---------|
| `ROOT` | 根源节点 | 一棵树的入口，树内唯一 | 是 | 是 |
| `BRANCH` | 分支节点 | 任务组、里程碑、功能模块 | 是 | 是 |
| `LEAF` | 叶节点 | 最小任务/记忆单元 | 否 | 是 |
| `EXPERIENCE` | 经验节点 | 提炼的核心经验 | 否 | 否 |
| `SENTINEL` | 哨兵节点 | 标记树边界，不做存储 | 否 | 否 |

## 3. 嵌套学习分层 (Nested Learning Layers)

### L0 — 瞬时层 (Transient)
- **生命周期**：单次会话内
- **存储位置**：不落盘，在对话上下文中
- **内容**：当前任务的原始交互、中间结果、临时假设
- **更新规则**：会话结束时自动清除
- **容量控制**：超过 10 条旧记录时，压缩为一条摘要

### L1 — 任务层 (Task Memory)
- **生命周期**：跨会话，任务完成后 7 天
- **存储位置**：`projects/<name>/` 下的 LEAF 节点
- **内容**：任务目标、关键决策、当前进度、阻塞项
- **更新规则**：任务状态变化时立即更新 frontmatter，正文追加进展
- **容量控制**：单任务节点正文不超过 100 行，超出则归档旧内容到折叠区

### L2 — 项目层 (Project Memory)
- **生命周期**：项目生命周期 + 30 天归档期
- **存储位置**：`projects/<name>/ROOT.md` 及 BRANCH 节点
- **内容**：项目目标、架构决策、已完成里程碑、活跃分支索引
- **更新规则**：里程碑完成时更新，BRANCH 完成时折叠为摘要
- **容量控制**：活跃 BRANCH 不超过 7 个，超出则合并低优先级分支

### L3 — 跨项目层 (Cross-Project Patterns)
- **生命周期**：长期，季度审查
- **存储位置**：`experiences-tree/patterns/`
- **内容**：可跨项目迁移的模式、方案、教训
- **更新规则**：项目完成时提炼模式到本层
- **容量控制**：模式总数不超过 50 条，超出时合并相似模式

### L4 — 核心经验层 (Core Experiences)
- **生命周期**：永久，年度审查
- **存储位置**：`experiences-tree/core/`
- **内容**：高度凝练的指导性原则（每条 ≤ 3 行）
- **更新规则**：L3 模式被反复验证后升级到 L4
- **容量控制**：核心经验不超过 20 条，超出时投票淘汰

## 4. 节点数据结构

### 4.1 Frontmatter 字段规范
```yaml
---
id: <TREE>-<TYPE>-<NNNN>     # 全局唯一标识
type: ROOT|BRANCH|LEAF|EXPERIENCE|SENTINEL
tree: <tree-name>             # 所属记忆树
layer: L0|L1|L2|L3|L4        # 嵌套学习层
status: ACTIVE|DORMANT|COMPLETED|ARCHIVED|ORPHANED
parent: <parent-id>           # 父节点 id
children: [<child-id>, ...]   # 子节点 id 列表
created: YYYY-MM-DD
completed: YYYY-MM-DD         # 完成日期（若 completed）
heartbeat: YYYY-MM-DD         # 最后心跳时间
priority: ABSOLUTE|HIGH|MEDIUM|LOW|BACKGROUND
owner: <agent-id>             # 所有者（多智能体场景）
shared_with: [<agent-id>]     # 共享目标
tags: [<tag>, ...]            # 检索标签
experience_refs: [<exp-id>]   # 关联经验
---
```

### 4.2 正文结构
```markdown
# [节点标题] — 一句话描述

## 目标
[该节点要达成的目标，可量化]

## 当前状态
[最新状态摘要，每次心跳更新]

## 子节点索引
[若类型为 ROOT/BRANCH，列出活跃子节点及状态]

## 任务清单
- [ ] 未开始的任务
- [x] 已完成的任务

## 关键决策
[记录为什么做了某个选择，而非另一个]

## 阻塞项
[当前阻碍进展的因素]

## 经验提炼
[从本节点完成中提取的 L3/L4 经验]

## 折叠区 (Collapsed Archive)
<details>
[超过容量限制的旧内容折叠在此]
</details>
```

## 5. 心跳机制 (Heartbeat Mechanism)

### 5.1 触发条件
- LEAF 节点的所有任务标记为完成
- 用户切换上下文
- 会话正常结束前
- 显式调用 `/heartbeat`

### 5.2 执行算法
```
function heartbeat(node_id):
    node = load(node_id)

    # 1. 更新本节点心跳时间
    node.heartbeat = today()

    # 2. 检查本节点任务完成情况
    if all_tasks_completed(node):
        node.status = COMPLETED

    # 3. 若是 LEAF 且已完成，向上冒泡
    if node.type == LEAF and node.status == COMPLETED:
        ascend_heartbeat(node.parent)

    # 4. 保存节点
    save(node)

function ascend_heartbeat(node_id):
    node = load(node_id)
    node.heartbeat = today()

    # 检查所有子节点
    all_done = true
    for child in node.children:
        if child.status != COMPLETED and child.status != ARCHIVED:
            all_done = false
            break

    if all_done and node.type == BRANCH:
        # 所有子节点完成 → 折叠为摘要，标记完成
        node.status = COMPLETED
        collapse_children_to_summary(node)
        ascend_heartbeat(node.parent)

    elif all_done and node.type == ROOT:
        # 整棵树完成 → 触发树归档
        node.status = COMPLETED
        archive_tree(node.tree)

    save(node)
```

### 5.3 未完成节点演进
```
当心跳发现某子节点长期 DORMANT（> 7 天无心跳）：
  1. 检查是否为阻塞状态 → 若是，提升 priority
  2. 检查是否可合并到其他子节点 → 若是，合并
  3. 检查是否仍相关 → 若不相关，标记 ORPHANED
  4. 若均不适用 → 降级 priority，推入折叠区
```

## 6. 垃圾回收机制

### 6.1 自动回收规则
| 层级 | 回收条件 | 回收动作 |
|------|---------|---------|
| L0 | 会话结束 | 全部清除 |
| L1 | status=COMPLETED 且 heartbeat > 7天 | 压缩为摘要，移入折叠区 |
| L1 | status=ORPHANED | 直接删除 |
| L2 | status=ARCHIVED 且 heartbeat > 30天 | 全文压缩为 5 行摘要 |
| L3 | heartbeat > 90天 | 审查是否仍相关 |
| L4 | heartbeat > 365天 | 审查是否仍为核心 |

### 6.2 遗忘执行 (Forgetting)
```
遗忘 ≠ 删除。遗忘流程：
1. 检查节点是否被其他活跃节点引用 (experience_refs)
2. 提取 1-3 条核心信息（若尚未提取）
3. 将核心信息写入关联 EXPERIENCE 节点
4. 若有关联经验已记录 → 删除该节点
5. 若无关联经验 → 压缩为摘要，移入折叠区
```

## 7. 上下文窗口保护 (高效回想)

### 7.1 加载策略
- **总是展开**：当前路径 (ROOT → BRANCH → 当前 LEAF)，最多 5 个节点
- **摘要加载**：已完成兄弟节点，仅标题 + 状态
- **按需加载**：非当前树的其他树，仅索引
- **不加载**：ARCHIVED/ORPHANED 节点，除非显式搜索

### 7.2 回想触发词映射
当用户话语中包含以下模式，自动加载对应记忆路径：

| 触发模式 | 加载路径 |
|---------|---------|
| "继续" / "上次" / "之前" | 当前树中最近心跳的未完成节点 |
| "项目X" / "project X" | projects/X 的 ROOT 节点 |
| "系统" / "配置" / "规范" | system-tree 的 ROOT 节点 |
| "经验" / "教训" / "之前遇到过" | experiences-tree/core/ |
| 技术关键词 (MQTT/Docker/Python...) | 全文搜索 tags 字段 |
| "回顾" / "总结" | 当前树全部活跃节点摘要 |

### 7.3 防塞满机制
```
加载节点时遵循:
1. 单次加载节点正文总行数 ≤ 200 行
2. 若当前路径超过 200 行 → 折叠最深层的 LEAF 节点为摘要
3. 若仍超过 → 逐层向上折叠直到满足
4. 优先折叠: COMPLETED > DORMANT > LOW priority
5. 绝不折叠: 当前活跃 LEAF, ABSOLUTE priority 节点
```

## 8. 多智能体支持

### 8.1 所有权模型
- `owner`: 创建节点的 agent，拥有修改权限
- `shared_with`: 可读取但不可修改的 agent 列表
- `owner = "*"`: 全局可读写（公共记忆）

### 8.2 记忆共享协议
```
Agent-A 需要访问 Agent-B 的记忆:
1. Agent-A 声明需求: "需要访问 <tree-name> 的 <node-id>"
2. 检查 node.shared_with 是否包含 Agent-A
3. 若不包含 → 请求 Agent-B 授权 (或由用户授权)
4. 授权后 → Agent-A 可读取，修改需标注 [Agent-A modified]
```

### 8.3 记忆接管
```
当 Agent-B 接手 Agent-A 未完成的工作:
1. 复制 Agent-A 的当前节点为新节点
2. 新节点 owner = Agent-B
3. 原节点标记 status = ARCHIVED, 添加 takeover_by = <agent-b-id>
4. 新节点 parent 不变
```

## 9. 经验提炼机制

### 9.1 提炼时机
- LEAF 节点完成时 → 检查是否有可提炼的教训
- BRANCH 完成时 → 必须提炼至少 1 条经验
- ROOT 完成时 → 必须提炼至少 3 条经验到 L4

### 9.2 提炼格式
```yaml
---
id: EXP-<tree>-<NNNN>
type: EXPERIENCE
tree: experiences
layer: L3|L4
---
# [一句话标题]
## 触发条件
[什么场景下该经验适用]
## 行动
[应该怎么做]
## 结果
[这样做会得到什么结果]
## 反例
[不这样做的后果]
## 来源
[从哪个节点提炼: <node-id>]
```

### 9.3 经验升级
```
L3 → L4 升级条件:
- 同一经验被 3 个以上不同项目引用
- 或用户明确确认为核心原则
- 或同一模式在 L3 中出现 5 次以上
```

## 10. 记忆树创建/删除/回收

### 10.1 创建新树
```
1. 确定树名: projects/<name> 或自定义路径
2. 创建 ROOT.md (type=ROOT)
3. 在 forest-root.md 的 children 中添加新树引用
4. 创建第一个 BRANCH 节点
5. heartbeat(forest-root)
```

### 10.2 删除树
```
1. 确认树内所有节点已完成或可遗弃
2. 提炼核心经验到 experiences-tree
3. 将所有节点标记 status=ARCHIVED
4. 从 forest-root.md 移除引用
5. 30天后物理删除文件
```

### 10.3 回收孤立节点
```
孤立节点: parent 引用不存在 或 status=ORPHANED
1. 心跳时检测孤立节点
2. 尝试找到可接管的父节点
3. 若找不到 → 提炼经验 → 30天后删除
```
