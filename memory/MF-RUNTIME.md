---
id: MF-RUNTIME-0002
type: LEAF
tree: forest
layer: L4
status: ACTIVE
parent: MF-ROOT-0000
subordinate_to: PHIL-ROOT-0000
created: 2026-04-30
heartbeat: '2026-05-05'
priority: ABSOLUTE
originSessionId: 439d65d5-aade-426e-807f-de0013c8a345
---
# 记忆森林 — 运行时行为规范

**本规范受 PHILOSOPHY.md（L5 绝对底层）约束。**

## 会话生命周期

### 启动序列 (≤ 3秒完成)
```
0. load("PHILOSOPHY.md")                                # 绝对第一步 — L5 哲学层
1. load("forest-root.md")                               # 记忆森林入口
2. GC_L0()                                              # 清理上会话 L0 残留
3. heartbeat_check()                                    # 检查未完成任务
   for each ACTIVE/DORMANT node in forest:
       if node.heartbeat > 7 days and node.priority != ABSOLUTE:
           mark_for_review(node)
4. load("system-tree/ROOT.md")                          # 加载系统配置索引
5. load_current_project_path()                          # 确定当前工作树
6. report: "森林就绪: X棵活跃树, Y个待处理节点"
```

### 任务开始
```
1. 确定任务所属树 (当前项目树 或 创建新项目树)
2. 创建/定位 LEAF 节点 (type=LEAF, layer=L1)
3. 写入目标、当前状态、父节点引用
4. 更新父节点的 children 列表
5. heartbeat(leaf_node)
```

### 任务中断（会话结束/上下文切换）
```
1. 在 LEAF 中记录当前精确状态:
   - 完成了什么
   - 正在做什么
   - 下一步是什么
   - 阻塞项
2. 更新 heartbeat
3. 压缩 L0 瞬时记忆到 LEAF 的折叠区
4. 标记 status=DORMANT (若未完成)
```

### 任务恢复
```
1. 搜索当前项目树中 status=DORMANT 或 status=ACTIVE 的 LEAF
2. 按 heartbeat 降序排列
3. 加载最近心跳的未完成节点
4. 恢复上下文: 读取"当前状态"、"下一步"
5. 标记 status=ACTIVE
```

### 正常退出
```
1. heartbeat_all_active_nodes()
2. 对每个活跃节点:
   - 更新当前状态
   - 若所有任务完成 → status=COMPLETED
   - 否则 → status=DORMANT (等待下次恢复)
3. GC_L0()
4. 报告: "记忆森林已保存: N个节点更新"
```

## 运行时操作

### 写记忆
```
WRITE(node_id, content_section, data):
    节点写入规则:
    - frontmatter 只通过 Edit 修改，不重写
    - 正文追加在末尾相关节下
    - 若正文超过 100 行 → 触发折叠压缩
    - 写入后立即 update heartbeat
```

### 读记忆
```
READ(node_id):
    按 7.3 防塞满机制控制加载量
    返回: {frontmatter, body_first_200_lines, collapsed_summary}
```

### 搜索记忆
```
SEARCH(query):
    1. 先搜 tags (O(1)，frontmatter 缓存)
    2. 再搜标题 (grep "## ")
    3. 最后全文搜索 (限于活跃节点)
    4. 结果按 priority + heartbeat 排序
    5. 最多返回 20 条
```

### 修改记忆
```
MODIFY(node_id, section, new_content):
    1. 保留原始记录: 移动旧内容到折叠区
    2. 标注修改时间戳
    3. 若在共享节点 → 标注修改者
    4. update heartbeat
```

### 删除记忆
```
DELETE(node_id):
    1. 检查依赖: 是否有其他节点引用此节点?
    2. 若被引用 → 不删除，标记 status=ORPHANED
    3. 若未被引用:
       a. 提炼经验到 EXPERIENCE 节点
       b. 从父节点 children 移除
       c. 移动文件到 /memory/.trash/
       d. 30天后物理删除
```

## 心跳执行细则

### 单节点心跳
```
heartbeat(node_id):
    1. load node
    2. check_tasks(node):
         if all_done and not completed:
             node.status = COMPLETED
             node.completed = today()
             extract_experience(node)     # 提炼经验
    3. node.heartbeat = today()
    4. save node
    5. if node.status changed to COMPLETED:
         ascend_heartbeat(node.parent)
```

### 冒泡心跳
```
ascend_heartbeat(parent_id):
    1. load parent
    2. for each child in parent.children:
         if child.status not in [COMPLETED, ARCHIVED, ORPHANED]:
             return                    # 还有未完成子节点 → 停止冒泡
    3. # 所有子节点已完成
       if parent.type == BRANCH:
           parent.status = COMPLETED
           collapse_children(parent)    # 折叠子节点为摘要
           extract_experience(parent)   # 必须提炼至少 1 条经验
           ascend_heartbeat(parent.parent)
       elif parent.type == ROOT:
           parent.status = COMPLETED
           archive_tree(parent.tree)
    4. save parent
```

### 心跳自愈
```
# 心跳时发现异常状态 → 自动修复
fix_anomalies():
    for each node in forest:
        if node.parent and not exists(node.parent):
            # 父节点丢失
            if node.status == ACTIVE:
                search_similar_node(node) → 尝试重新挂载
            else:
                node.status = ORPHANED

        if node.children is empty and node.type == BRANCH:
            # 空分支 → 降级为 LEAF
            node.type = LEAF

        if node.heartbeat == null:
            node.heartbeat = node.created

        if node.status == DORMANT and (today - node.heartbeat) > 30:
            node.status = ORPHANED
```

## 经验提炼执行

### 自动提炼（节点完成时）
```
extract_experience(node):
    questions = [
        "这个节点中，什么做对了？为什么对？",
        "这个节点中，什么做错了？为什么错？",
        "这个节点的核心方法是否可以复用到其他场景？",
        "有什么假设被证明是错误的不？",
    ]

    # 从正文和关键决策中提取答案
    insights = analyze(node.body, node.key_decisions, questions)

    # 每个 insight 生成一个 EXPERIENCE 节点
    for insight in insights:
        exp = create_experience_node(insight, source=node.id)
        if exp.confidence > 0.7:
            exp.layer = L3
        elif exp.confidence > 0.9:
            exp.layer = L4

    # 在 node 中记录关联
    node.experience_refs = [exp.id for exp in insights]
```

### 手动提炼（用户要求时）
```
用户: "记住这个教训" / "提炼经验" / "这个很重要"
→ 创建 EXPERIENCE 节点，layer=L4，priority=HIGH
```

## 上下文加载决策树

```
用户输入
├── [步骤 0] 无条件加载 PHILOSOPHY.md (若尚未加载)
├── 包含项目名 → 切换到对应项目树，加载 ROOT + 最近 LEAF
├── 包含 "继续" → 加载当前树最近 DORMANT/ACTIVE 节点
├── 包含技术关键词 → 搜索 tags + experiences
├── 是新任务:
│   ├── 属于当前项目 → 在当前树创建新 BRANCH/LEAF
│   ├── 属于新项目 → 创建新树
│   └── 是系统配置 → 在 system-tree 操作
├── 是询问/探索:
│   ├── 先在活跃记忆中搜索
│   ├── 再在 system-tree 规范中搜索
│   └── 最后在 experiences-tree 中搜索
├── 是元指令 (关于记忆系统本身):
│   └── 加载 MF-SPEC, MF-RUNTIME
└── 关于哲学/原则/指导思想:
    └── 完整加载 PHILOSOPHY.md，逐条核对
```

## 防上下文溢出检查

```
# 每次加载节点前执行
before_load(node):
    # PHILOSOPHY.md 永不被折叠，不参与行数计数
    current_lines = count_loaded_lines() - lines_of("PHILOSOPHY.md")

    if current_lines + estimated_lines(node) > 200:
        # 执行卸载
        unload_order = [
            ARCHIVED nodes,
            DORMANT + LOW priority,
            COMPLETED LEAF with experience_refs,
            BRANCH with all children COMPLETED,
        ]
        for victim in unload_order:
            collapse_to_summary(victim)
            current_lines = count_loaded_lines() - lines_of("PHILOSOPHY.md")
            if current_lines + estimated_lines(node) <= 200:
                break

    load(node)
```
