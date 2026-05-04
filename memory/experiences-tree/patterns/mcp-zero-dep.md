---
id: EXP-PAT-0003
type: EXPERIENCE
tree: experiences
layer: L3
status: ACTIVE
created: 2026-05-01
heartbeat: '2026-05-05'
priority: HIGH
owner: claude-code
tags:
- mcp
- json-rpc
- stdio
- zero-dependency
- protocol
source: PROJ-EVOL-0002
originSessionId: a7664e14-d841-48de-acfa-f9d0da11efe2
---
# MCP Server 零依赖实现

## 触发条件
需要创建 MCP Server 但无法安装 SDK（PEP 668 阻止、网络限制、或希望零依赖）。

## 行动
1. 不要纠结于安装 SDK — MCP 协议核心是 JSON-RPC 2.0 over stdio，约 50 行代码即可实现
2. 实现三个关键方法：
   - `initialize` → 返回 `protocolVersion` + `capabilities`
   - `tools/list` → 返回工具数组（name + description + inputSchema）
   - `tools/call` → 根据 `params.name` 派发 handler，返回 `{content: [{type: "text", text: result}]}`
3. stdout 是 MCP 传输通道，stderr 用于日志。**不能把任何调试输出混入 stdout**
4. 每行一个 JSON-RPC 消息（`\n` 分隔），读 stdin 写 stdout
5. 所有 handler 返回值必须是 JSON 字符串（`content[].text` 字段）
6. DateEncoder 处理 YAML 解析产生的 `datetime.date` 对象

## 结果
零外部依赖、可被任何 MCP 兼容客户端调用的标准化工具服务。约 400 行代码暴露 8 个工具。

## 反例
- 花大量时间尝试绕过 PEP 668 安装 mcp SDK → 实际上协议简单到不需要 SDK
- 使用 HTTP transport 而非 stdio → stdio 对本地工具更简单，无需端口管理
- 把 print 日志写入 stdout → 破坏 JSON-RPC 消息流，客户端解析失败

## 关键要点
- MCP 协议精华：`initialize` + `tools/list` + `tools/call` 三个方法即可工作
- stdin/stdout 是 transport，stderr 是日志通道
- inputSchema 使用 JSON Schema 标准格式
- 工具返回值必须包裹在 `{content: [{type: "text", text: "..."}]}` 中

## 来源
从 PROJ-EVOL-0002 (MCP Memory Forest Server) 提炼
