# Changelog

## [2.0.0] — 2026-05-05 · 哲学层大更新

### 新增 — L5 绝对底层哲学层

基于全森林审计（18 个 L3 模式 + 7 条 L4 行为准则 + 5 个系统分支 + 4 个项目历史），建立 8 条哲学原则：

- **一、矛盾论** — 抓主要矛盾，具体问题具体分析
- **二、军事/执行谋略** — 集中兵力、掌握主动权、战略藐视战术重视
- **三、实事求是参谋路线** — 从"群众路线"扩展至完整的参谋循环：深度理解→事实核查→质疑纠正→主动建议→确认执行→反馈转化
- **四、实践真理观** — 实践是检验真理的唯一标准
- **五、持久战与根据地** — 新增"可逆迁移"子原则（每次转换保留回退路径）
- **六、自我批判与整风** — 新增"对称认知"（理解失败=理解成功）和"知识策展"（积累+修剪）
- **七、环境的战争** — 全新。涵盖维护战场、显式资源管理、设计容错。覆盖 6 个 L3 资源管理模式 + 安全分支全部规则
- **八、认知纪律** — 全新。信任权威数据源不信任代理指标、状态隐藏于无状态表面、理解全栈。覆盖 9 个 L3 模式的核心教训

### 扩展

- `PHILOSOPHY.md` — 从 6 条扩展到 8 条原则 25 子原则（原 6 条 17 子原则）
- `experiences-tree/ROOT.md` — 更新核心行为准则→哲学原则映射表，新增 L3 模式→哲学原则对照表
- `MF-SPEC.md` — L5 层定义更新（八条原则），哲学层永不折叠
- `MF-RUNTIME.md` — 启动序列步骤 0 = 加载 PHILOSOPHY.md，决策树哲学分支
- `forest-root.md` — 新增 `subordinate_to: PHIL-ROOT-0000`
- 全系统 12 个节点添加 `subordinate_to: PHIL-ROOT-0000` 约束

### 修正

- `experiences-tree/ROOT.md` 映射表更新：EXP-CORE-0001 反驳-确认 → 三.3（原二.3），EXP-CORE-0003 五次停止 → 七.3（原二.2），EXP-CORE-0004 合并 → 六.4（原五.2）
- `branch-safety.md` 交叉引用新增第七条"环境的战争"
- `branch-meta.md` 交叉引用六.2"反对八股文"

### 状态

- 记忆森林：49 节点 / 5 棵活跃树 / HEALTHY
- 活跃项目：框架重构（Phase 1-12 完成）、自我进化、n8n 工作流、本地 AI 模型

---

## [1.1.0] — 2026-05-01 · 自我进化 v1

### 新增

**自动化引擎 (Evolution A)**
- `scripts/memory_forest.py` — 核心库，提供 frontmatter 解析、心跳冒泡、GC 回收、全文搜索、健康检查
- `scripts/mf.py` — CLI 工具，9 个命令
- `scripts/heartbeat_hook.py` — Stop hook，会话退出时自动心跳
- 在 settings.local.json 中配置 `Stop` hook

**MCP Memory Server (Evolution B)**
- `scripts/mcp_memory_forest.py` — 零依赖 MCP 服务 (JSON-RPC 2.0 over stdio)
- 8 个 MCP 工具

**启动自检协议 (Evolution C)**
- `scripts/startup_hook.py` — SessionStart hook

**工作流优化 (Evolution D)**
- `scripts/aliases.sh` — Shell 别名
- 权限白名单优化

---

## [1.0.0] — 2026-04-30

### 初始发布
- 记忆森林框架：forest-root, MF-SPEC, MF-RUNTIME, MEMORY.md
- 系统配置树：5 个分支 17 个规范文档
- 经验池树：6 条 L4 核心行为准则
- 项目记忆树：框架重构项目模板
- memory-forest skill：完整的 SKILL.md + references
