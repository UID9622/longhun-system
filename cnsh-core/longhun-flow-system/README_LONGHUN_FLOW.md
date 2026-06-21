# UID9622｜龍魂流场总控 v2.0 使用说明

## 一句话

五个本地 HTML 文件的统一切换入口 · 不删原文件 · 不假融合 · 不假联动。

## 真体系归位

- IPA 编号: `LOCAL-VIZ-MASTER → IPA-010 龍魂流场可视化`
- 上游: 全谱入口 v1.1 (`#龍芯⚡️2026-05-08-LONGHUN-FULL-MAP-ENTRY-FILE2-v1.1`)
- 主权: 解除宣言 v1.0 已生效 · 本代码不授权 AI 训练

## 文件清单

| 类型 | 文件 |
|---|---|
| 新建 | flow-field-index.json |
| 新建 | longhun-master-control.html |
| 新建 | README_LONGHUN_FLOW.md |
| 已有·勿动 | longhun-28mansions-v1.html |
| 已有·勿动 | longhun-unified-v9.html |
| 已有·勿动 | longhun-flow-field-v9.html |
| 已有·勿动 | current.html |
| 已有·勿动 | dragon_soul_9622.html |

## 启动

### 推荐: 本地服务器

```bash
cd longhun-flow-system/
python3 -m http.server 9622
```

打开: http://localhost:9622/longhun-master-control.html

### 备选: 直接双击

某些浏览器会拦截 file:// 协议下的 iframe · 看到"加载失败"就改用本地服务器。

## 使用规则

- 启动后**默认不预加载任何 iframe** · 欢迎页等待点击
- 点左侧入口 · iframe 才加载对应 HTML
- 想改默认 → 改 `flow-field-index.json` 的 `default_view` 为对应 id
- 加新 HTML → 在 `flow-field-index.json` 的 `files` 加一条 · HTML 代码不用改

## 一票否决(接驳公式对准表 §S)

1. 不假联动 · 不说五图已深度融合
2. 不删原文件 · 不覆盖原文件
3. 不读密钥 · 不读 .env
4. 不上传 · 不联网
5. 不假执行 · 没真启动浏览器不算验收
6. 不擅自加默认 default_view 抢占老大启动主权

## ROOT_CARD

```yaml
title: UID9622 龍魂流场总控 v2.0
ipa: LOCAL-VIZ-MASTER
parent_ipa: IPA-010 龍魂流场可视化
dna: "#龍芯⚡️2026-05-08-LONGHUN-FLOW-MASTER-v2.0"
parent_dna: "#龍芯⚡️2026-05-08-LONGHUN-FULL-MAP-ENTRY-v1.1-IPA-COMPLETE"
sovereignty: 解除宣言 v1.0 已生效
seal: "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
gpg: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
confirm: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
root: dr=5 土
tricolor: 🟢
conclusion: 本地工程 · 不假融合 · 不假联动 · 主权回收声明已生效
```
