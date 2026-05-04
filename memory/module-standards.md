---
name: 模块规范与自测规范
description: Python/Node/Go 模块结构标准，接口设计要求，以及 if __name__ == '__main__' 自测模式
type: project
originSessionId: 439d65d5-aade-426e-807f-de0013c8a345
---
# 模块规范与自测规范

## 模块定义
- **模块**：可独立导入、独立测试的最小功能单元
- Python：一个 `.py` 文件或一个 `__init__.py` 包
- Node：一个 `.js`/`.ts` 文件或 `index.js` 目录
- Go：一个 package 目录

## 模块结构模板（Python）

```python
"""模块简短描述（单行）"""
# 标准库 import
# 第三方库 import
# 本地 import

# ---- 常量 / 类型定义 ----

# ---- 公开 API ----

def public_function(arg1: type, arg2: type) -> ReturnType:
    ...

# ---- 内部实现 ----

def _private_helper(x: type) -> type:
    ...

# ---- 自测 ----

if __name__ == "__main__":
    # 完整功能测试
    ...
```

## 模块自测规范

### Python `if __name__ == '__main__'` 规则
- **必须包含**：每个模块文件末尾必须有 `if __name__ == '__main__':` 块
- **必须测试**：
  1. 每个公开函数的正常调用路径
  2. 每个公开函数的边界/异常输入
  3. 模块集成行为（若模块有内部协作）
- **必须输出**：清晰的成功/失败结果（打印或返回退出码）
- **模式**：
```python
if __name__ == "__main__":
    tests_passed = 0
    tests_failed = 0

    # Test 1: normal case
    try:
        result = public_function(valid_input)
        assert result == expected, f"Expected {expected}, got {result}"
        tests_passed += 1
        print("PASS: test_normal_case")
    except Exception as e:
        tests_failed += 1
        print(f"FAIL: test_normal_case - {e}")

    # ... more tests ...

    print(f"\n{tests_passed} passed, {tests_failed} failed")
    sys.exit(0 if tests_failed == 0 else 1)
```

### Node 模块自测
```javascript
// 文件末尾
if (require.main === module) {
    // 运行自测
    console.log('Running self-tests...');
    testFunction1();
    testFunction2();
}
```

### Go 模块自测
- 使用标准 `_test.go` 文件
- `go test ./...` 运行
- 若模块是 main package，提供 `-test` 模式或独立测试文件

## 公开 API 设计要求
- **最小接口**：仅暴露必须公开的符号，其余用 `_` 前缀或模块私有
- **类型注解**（Python）：所有公开函数必须有类型注解
- **不变性保护**：公开 API 接收和返回不可变类型或防御性拷贝
- **文档字符串**：仅公开函数需要一行描述其用途和返回值

## 模块间依赖规则
- 依赖方向单向：`上层 → 下层`，`抽象 → 具体`
- 循环依赖绝对禁止
- 模块 A 不直接导入模块 B 的子模块的内部符号（`from b._internal import xxx`）

## 模块命名
- Python：`snake_case.py`
- Node：`kebab-case.js` 或 `camelCase.js`
- Go：小写字母 package 名，与目录名一致
