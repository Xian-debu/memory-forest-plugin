---
name: 开发规范
description: 代码质量标准、命名约定、错误处理、安全红线 — 每次编写代码时自动适用
type: project
originSessionId: 439d65d5-aade-426e-807f-de0013c8a345
---
# 开发规范

## 代码质量
- **Python**：遵循 PEP 8，4空格缩进，120字符行宽
- **JavaScript/TypeScript**：遵循 StandardJS，2空格缩进
- **Go**：遵循 `gofmt` 标准格式
- **C/C++**：遵循 Linux kernel 风格或项目既有风格
- **缩进不得混用空格与 Tab**

## 命名约定
- Python：`snake_case` 变量/函数，`PascalCase` 类，`UPPER_SNAKE` 常量
- JS/TS：`camelCase` 变量/函数，`PascalCase` 类/组件
- Go：`camelCase` 私有，`PascalCase` 公开
- 文件名：`snake_case.py`，`kebab-case.ts`
- **命名须自解释**，禁止单字母变量（循环索引 `i`, `j` 除外）

## 注释原则
- **默认不写注释**，代码即文档
- 仅在以下情况添加单行注释：
  - 非显而易见的约束或 workaround
  - 容易踩坑的边界条件
  - 第三方 API 的奇怪行为
- **禁止**：多行 docstring、注释掉的代码、`// TODO` 无跟踪工单

## 错误处理
- **边界处验证**：用户输入、外部 API 响应、文件读取
- **内部不防御**：信任内部调用链，不写 `if obj is None` 检查不可能出现的状态
- Python：使用 `raise XError` 而非返回错误码
- Go：返回 `(result, error)` 元组，调用方必须检查 error
- **禁止**：空 catch/except、打印错误后继续执行

## 安全红线（不可违反）
- **禁止**：`os.system()` 拼接用户输入、`subprocess(shell=True)` 含未转义数据
- **禁止**：SQL 字符串拼接（使用参数化查询）
- **禁止**：硬编码密钥、token、密码
- **禁止**：`eval()` / `exec()` 处理外部数据
- **禁止**：文件路径拼接导致目录穿越（使用 `os.path.join` / `pathlib`）
- **必须**：外部数据写入 HTML 前做转义（XSS 防护）

## 依赖管理
- Python：`requirements.txt` + 固定版本号（`package==1.2.3`）
- Node：`package.json` + `package-lock.json`
- 新依赖引入前需评估：必要性、体积、许可证、维护活跃度

## 版本控制
- 提交信息：中文简述 + 英文详情（若跨团队协作则英文）
- 一次提交只做一件事
- 不提交生成文件、依赖目录、IDE 配置
- `.gitignore` 必须在首次提交前创建

## 禁止项
- 不编写未经验证的样板代码
- 不引入仅用于"未来可能"的抽象层
- 不格式化非当前修改区域的代码
- 不添加 feature flag 或向后兼容 shim
- 不在同一 PR 中混合重构和功能修改
