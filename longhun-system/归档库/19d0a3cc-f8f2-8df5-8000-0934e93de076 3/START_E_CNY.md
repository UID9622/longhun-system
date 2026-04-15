# CNSH-64 数字人民币接入快速指南

## 1. 启动护盾

```bash
cd ~/.cnsh
python3 cnsh_shield_v05_integrated.py
```

## 2. 绑定数字人民币钱包

```
🐉 > /e_cny
  1. 绑定DNA: bind <钱包ID>
  2. 支付: pay <收款方> <金额> [用途]
  3. 海外准入: overseas <地区> <护照号>
  4. 审计查询: audit <交易DNA>

e_cny> bind 0031000900456651
```

## 3. 发起支付

```
e_cny> pay 商家DNA 100.00 购买商品
```

## 4. 海外用户准入

```
e_cny> overseas 香港 E12345678
```

## 铁律确认

| 铁律 | 状态 |
|------|------|
| 数字人民币 = DNA身份证 | ✅ |
| 没有其他支付方式 | ✅ |
| 1毫米都不让 | ✅ |
| 海外用户必须离岸钱包 | ✅ |
| 每笔交易DNA追溯 | ✅ |
| 小额匿名/大额实名分层 | ✅ |

## 文件位置

- 主护盾: `~/.cnsh/cnsh_shield_v05_integrated.py`
- 数字人民币模块: `~/.cnsh/cnsh_e_cny_module.py`
- 钱包数据: `~/.cnsh/e_cny_wallet.json` (600权限)
- 交易记录: `~/.cnsh/e_cny_transactions.json` (600权限)

## DNA追溯

`#龍芯⚡️2026-03-23-E-CNY-v0.9.0`
