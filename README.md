# 记忆森林 (Memory Forest)

一套完整的 AI 行为配置与记忆管理系统，为 Claude Code 提供**分层记忆、行为准则和会话生命周期管理**。

## 这是什么

记忆森林不是工具，而是一套运行在 Claude 上的操作系统——定义了 Claude 如何记忆、如何行为、如何自我迭代。

核心机制：
- **5 层记忆分层** (L0 瞬时 → L4 核心原则)，自动升降级和垃圾回收
- **6 条核心行为准则**，每次会话强制执行
- **心跳机制**追踪任务进度，支持中断/恢复
- **树状结构**组织项目、经验和系统配置

## 安装

```bash
claude plugin marketplace add https://github.com/Xian-debu/memory-forest-plugin
claude plugin install memory-forest
```

## 触发方式

在 Claude Code 中输入以下任意内容即可触发：

| 触发词 | 效果 |
|--------|------|
| "初始化记忆森林" / "initialize memory forest" | 首次设置，创建记忆目录结构 |
| "记住这个教训" / "保存经验" | 提炼并存储经验 |
| "继续上次的 X" / "恢复进度" | 恢复中断的任务 |
| "加载系统配置" / "应用行为准则" | 重新加载行为规范 |

也支持英文触发：`setup memory forest`, `load behavior rules`, `resume task` 等。

## 6 条核心行为准则

| # | 准则 | 说明 |
|---|------|------|
| 1 | 反驳-确认模式 | 收到实质性需求时先验证前提假设，错误时反驳并等用户确认 |
| 2 | 三次重复即自省 | 同一问题被问 3 次，停止当前方法，检讨理解偏差 |
| 3 | 五次失败即停止 | 同一问题 5 次尝试未解决，整理报告等用户指示 |
| 4 | 经验迭代合并 | 新经验与已有经验合并去重，定期垃圾回收 |
| 5 | 自我迭代与自我提示 | Claude 自行改进基础设施，但必须告知用户 |
| 6 | 搜索优先 | 开始工作前先搜索现成方案，不重复造车轮 |

## 记忆分层

| 层 | 生命周期 | 内容 |
|----|---------|------|
| L0 瞬时 | 单次会话 | 当前交互、中间结果 |
| L1 任务 | 跨会话，完成后 7 天 | 任务目标、决策、进度 |
| L2 项目 | 项目周期 + 30 天 | 项目目标、架构决策 |
| L3 跨项目 | 季度审查 | 可跨项目迁移的模式 |
| L4 核心 | 年度审查 | 高度凝练的指导原则（≤20 条） |

## v1.1.0 新增：自动化引擎 + MCP Server + CLI 工具

### CLI 工具 (mf)

```bash
mf status       # 森林状态总览
mf health       # 健康检查
mf heartbeat    # 心跳所有活跃节点
mf gc           # 垃圾回收候选
mf search <kw>  # 全文搜索
mf list [tree]  # 列出节点
mf show <id>    # 查看节点
mf create ...   # 创建节点
```

### MCP Server

8 个 MCP 工具暴露给所有兼容 agent，配置在 `settings.local.json`：
`memory_status`, `memory_health`, `memory_search`, `memory_read`, `memory_heartbeat`, `memory_gc_check`, `memory_list`, `memory_create`

### 自动化 Hooks

- **Stop Hook** — 会话退出自动心跳所有活跃节点 + GC 扫描
- **SessionStart Hook** — 会话启动自动健康检查 + GC 提醒

### Shell 别名

`mf`/`mfs`/`mfh` (记忆操作) · `dexec`/`dcp` (Docker) · `cc`/`ccc`/`ccp` (Claude CLI)

## 更新

```bash
claude plugin update memory-forest
```

## 许可

MIT
