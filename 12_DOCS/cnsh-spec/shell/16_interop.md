# 第16章：与 Python/Shell 互操作

> **DNA**: `#龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-CNSH-CHAPTER-16-v1.0`
> **创建者**: 诸葛鑫（UID9622）
> **协议**: CC BY-NC-SA 4.0（核心思想层）
> **确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
> **三色**: 🟢 已定稿

---

## 16.1 执行外部命令

```cnsh
执行 "ls -la"
执行 "python3 script.py"
执行命令 "health_check.sh"
```

## 16.2 调用 Python

```cnsh
调用Python 函数="json.loads" 参数=["{'a': 1}"]
# 返回: {'a': 1}

执行Python 代码="
def add(a, b):
    return a + b
print(add(1, 2))
"
# 输出: 3
```

## 16.3 调用 Shell 管道

```cnsh
执行Shell "cat data.jsonl | jq '.verdict' | sort | uniq -c"
```

## 16.4 嵌入 Shell 脚本

```cnsh
脚本 开始
  #!/bin/bash
  echo "Hello from shell"
  ./deploy.sh
脚本 结束
```

## 16.5 数据互转

```cnsh
# CNSH 数据结构 → JSON
转换JSON 数据 = {名称: "龍魂", 版本: "1.0"}
# 输出: {"名称": "龍魂", "版本": "1.0"}

# JSON → CNSH
解析JSON 文本 = '{"名称": "龍魂"}'
# 输出: {名称: "龍魂"}
```

| 转换 | 说明 |
|------|------|
| `转换JSON` | CNSH → JSON 字符串 |
| `解析JSON` | JSON → CNSH 结构 |
| `转换列表` | 转列表 |
| `解析CSV` | CSV → 列表 |

## 16.6 与龍魂引擎互操作

```cnsh
# 调用 lh 命令
执行 "lh status"
执行 "lh audit"
执行 "lh te"          # 时间戳引擎
执行 "lh keys"        # 统一密钥出口
执行 "lh gpg sign ."  # GPG 签名
```

## 16.7 边界与安全

| 场景 | 建议 |
|------|------|
| 优先 CNSH 内建 | 能内建不调用外部 |
| 外部命令需白名单 | 禁止任意命令执行 |
| 敏感数据 | 禁止传给未知外部程序 |
| 境外 API | 出口走 P77 审查 |

## 16.8 本章小结

- `执行` / `执行Python` / `执行Shell` 调用外部
- JSON 互转：`转换JSON` / `解析JSON`
- 可直接调用龍魂 `lh` 系列命令
- 外部命令白名单 + 敏感数据保护

## 16.9 练习

1. 用 CNSH 执行 `lh status` 并输出结果
2. 把一个 CNSH 映射转成 JSON
3. 调用 Python 的 `len()` 函数

---

## 章节导航

- 上一章：[第15章：错误处理与回退](./15_error_handling.md)
- 下一篇：[附录A：保留关键字](../appendix/A_reserved_keywords.md)
- 目录：[INDEX.md](../INDEX.md)

---

**GPG**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
