# Changelog

## [1.1.0] — 2026-05-01 · 自我进化 v1

### 新增

**自动化引擎 (Evolution A)**
- `scripts/memory_forest.py` — 核心库，提供 frontmatter 解析、心跳冒泡、GC 回收、全文搜索、健康检查
- `scripts/mf.py` — CLI 工具，9 个命令：`status`, `heartbeat`, `gc`, `search`, `health`, `create`, `list`, `show`, `ls`
- `scripts/heartbeat_hook.py` — Stop hook，会话退出时自动心跳所有活跃节点并扫描 GC 候选
- 在 settings.local.json 中配置 `Stop` hook

**MCP Memory Server (Evolution B)**
- `scripts/mcp_memory_forest.py` — 零依赖 MCP 服务 (JSON-RPC 2.0 over stdio)
- 8 个 MCP 工具：`memory_status`, `memory_health`, `memory_search`, `memory_read`, `memory_heartbeat`, `memory_gc_check`, `memory_list`, `memory_create`
- 在 settings.local.json 中注册 `mcpServers.memory-forest`

**启动自检协议 (Evolution C)**
- `scripts/startup_hook.py` — SessionStart hook，每次会话启动自动健康检查 + GC 扫描
- 在 settings.local.json 中配置 `SessionStart` hook
- `SKILL.md` 更新：添加自动化机制说明、会话退出序列

**工作流优化 (Evolution D)**
- `scripts/aliases.sh` — Shell 别名：`mf`/`mfs`/`mfh`/`mfgc` (记忆操作), `dexec`/`dcp` (Docker), `cc`/`ccc`/`ccp` (Claude CLI)
- `.bashrc` 集成：自动 source aliases.sh
- 权限白名单优化：27 条规则，新增 `Bash(claude *)` / `Bash(python3 /root/.claude/scripts/*)`

### 修复
- `doc-usage-guide.md` 和 `doc-relationship.md` 补全记忆森林 frontmatter (id/type/tree/layer/status/heartbeat)
- `heartbeat_node` 修复 status 变更消息 bug（保存旧状态再生成消息）
- `gc_check` 修复缺失 heartbeat 时的日期回退逻辑（使用 `created` 而非 `2000-01-01`）
- 清理未使用的 import (`json`, `hashlib`, `Path`, `_dt`)

### 状态
- 记忆森林：24 节点 / 4 棵活跃树 / HEALTHY / 0 GC 候选
- 系统配置树：17 个规范文档完整
- 经验池：6 条 L4 核心准则 + 2 条 L3 跨项目模式
- 项目树：2 个项目（框架重构 + 自我进化）

---

## [1.0.0] — 2026-04-30

### 初始发布
- 记忆森林框架：forest-root, MF-SPEC, MF-RUNTIME, MEMORY.md
- 系统配置树 (system-tree)：5 个分支 17 个规范文档
- 经验池树 (experiences-tree)：6 条 L4 核心行为准则
- 项目记忆树 (projects-tree)：框架重构项目模板
- memory-forest skill：完整的 SKILL.md + references
