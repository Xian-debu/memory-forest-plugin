---
id: EXP-PAT-0004
type: EXPERIENCE
tree: experiences
layer: L3
status: ACTIVE
created: 2026-05-01
heartbeat: '2026-05-05'
priority: MEDIUM
owner: claude-code
tags:
- yaml
- json
- serialization
- datetime
- frontmatter
- type-conversion
source: PROJ-EVOL-0002
originSessionId: a7664e14-d841-48de-acfa-f9d0da11efe2
---
# YAML-JSON 桥接类型陷阱

## 触发条件
从 YAML frontmatter 解析数据后，通过 `json.dumps` 序列化输出。

## 问题
PyYAML 的 `safe_load` 会自动将 `2026-05-01` 解析为 `datetime.date` 对象，而 `json.dumps` 无法序列化 Python date 对象，导致 `TypeError: Object of type date is not JSON serializable`。

## 行动
1. **方案 A（推荐）**: 自定义 `json.JSONEncoder` 子类，在 `default()` 中检测 `datetime.date/datetime` 并转为 `.isoformat()`
2. **方案 B**: 在 YAML 加载后递归遍历 dict，将所有 date 对象转为字符串
3. **方案 C**: 使用 `yaml.BaseLoader` 替代 `yaml.SafeLoader` — 但会阻止所有自动类型推导
4. 所有从内存节点读取后准备 JSON 输出的地方，统一使用 `safe_json_dumps()` 而非 `json.dumps()`

## 结果
JSON 序列化零失误，date 字段正确输出为 ISO 格式字符串。

## 反例
- 在每个 handler 中单独 `str()` 转换 → 容易遗漏，代码膨胀
- 修改 YAML 源文件让日期带引号 → 破坏 YAML 可读性，治标不治本
- 忽略错误直接 `str(fm.get('heartbeat'))` → 丢失类型安全

## 关键要点
- PyYAML 自动类型推导包括：`datetime.date`, `datetime.datetime`, `int`, `float`, `bool`, `None`
- 只要涉及 YAML → JSON 转换，就必须考虑类型桥接
- `json.JSONEncoder.default()` 是单一控制点，比散落各处的 `str()` 调用更可靠

## 来源
从 PROJ-EVOL-0002 (MCP Memory Forest Server 调试过程) 提炼。首次运行 `memory_status` 时 `json.dumps` 抛出 TypeError，根因是 YAML frontmatter 中的 `heartbeat: 2026-05-01` 被解析为 date 对象。
