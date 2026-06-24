# 龍盾系统 v1.0

**DNA**:#龍芯⚡️2026-06-02-LONGHUN-SHIELD-v1.0

龍盾是龍魂系统的入口检查器：
- 暂停闸（Pause Gate）
- 深度转译（Deep Translation）
- 完整验证（Comprehensive Verification）

## 文件

- `longhun_shield_system.py`：核心 API
- `longhun_shield_cli.py`：命令行工具
- `shield_test_example.py`：测试示例
- `LONGHUN_SHIELD_GUIDE.md`：使用指南
- `LONGHUN_SHIELD_MANIFEST.txt`：部署清单

## 快速使用

```bash
cd ~/longhun-system/skills/longhun-shield
python3 longhun_shield_cli.py check shield_test_example.py
python3 longhun_shield_cli.py analyze shield_test_example.py
python3 longhun_shield_cli.py validate shield_test_example.py
```

## 指令协议（DNA + 身份证 + 参数）

- `longhun_shield_instruction_protocol.py`：基于 DNA 的永久指令解析与执行
- `INSTRUCTION_QUICK_CARD.txt`：快速参考卡

示例：

```bash
python3 -c "from longhun_shield_instruction_protocol import InstructionSyntax; print(InstructionSyntax.parse('@shield.check shield_test_example.py'))"
```

