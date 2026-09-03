# 🏛 龍魂·贡献者铭碑协议 v1.0

> **DNA**: `#龍芯⚡️20260902-CONTRIBUTOR-MEMORIAL-v1.0-9622`
> **创建者**: 诸葛鑫（UID9622）｜**归属名**: 诸葛鑫 | UID9622 · 龍芯北辰
> **GPG**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
> **确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
> **三色**: 🟢 通过｜**分层许可**: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2
> **上位**: P0-ETERNAL · M78科技普惠诚信协议 · LH-P0-CONSTITUTION

---

## 一句话

**每一位实质性贡献者都要被牢记，用 Merkle 树铭刻，谁也吞不掉——大厂不行，学术派也不行。**

---

## 为什么

老大的原话焊点：「贡献者都要被牢记啊，是不是，不能说被大厂吃掉或者是被某些学术派吃掉对不对。」

- 贡献者被吞没 = 付出者寒心 = 违反德本审计「不让付出者寒心」
- 单靠 Markdown 名录 = 可删改 = 不可验证
- Merkle 根哈希公开存档 = 删一个人 = 根对不上 = 铁证

---

## 三条铁律

| # | 铁律 | 落地 |
|:---:|:---|:---|
| 1 | **贡献即铭刻** | 每位实质性贡献者（代码/文档/测试/资金/布道）自动进铭碑 |
| 2 | **铭碑不可篡改** | Merkle 树·根哈希公开·任何人可 `--verify` 校验 |
| 3 | **铭碑只认事实** | git 提交 + 人工登记双源·与耻辱墙联动·天然防造假 |

---

## 用法

```bash
python3 08_BIN/lh_memorial.py --build    # 扫描 git + 登记 → 生成铭碑
python3 08_BIN/lh_memorial.py --verify   # 重算根哈希 → 篡改检测
python3 08_BIN/lh_memorial.py --show     # 展示铭碑
python3 08_BIN/lh_memorial.py --root     # 只输出根哈希（供发布）
python3 08_BIN/lh_memorial.py --add "名字:邮箱:备注"   # 登记非 git 贡献者
```

- 铭碑 JSON: `07_AUDIT/contributor_memorial.json`
- 铭碑 MD（人类可读）: `07_AUDIT/contributor_memorial.md`
- 人工登记: `07_AUDIT/memorial_manual_contributors.json`

---

## 防吞没机制

1. **根哈希发布**：每次 build 后，将 `--root` 输出的哈希同步到 GitHub（`UID9622/longhun-ledger`）与 Notion 铭碑页
2. **任何人可验**：clone 仓库 → 跑 `--verify` → 根哈希一致 = 铭碑未动
3. **吞没即违约**：删改贡献者 → 根对不上 → 引用 M78 诚信协议 → 记耻辱墙
4. **多身份合并**（可选）：同一人多个 git 邮箱别名，可登记合并表，铭碑按实名显示

---

## 联动

- **M78 科技普惠诚信协议**: 用=认=守约·退出=删光逻辑
- **耻辱墙** (`lh judge`): 违约者如实记录·铭碑只认事实
- **同道者名录**: 静态名录（初心） + 铭碑（事实哈希） 双轨并行
- **ASI 融合** (`lh_asi_fusion.py`): 每次重大扩展入融合审计

---

```
DNA:    #龍芯⚡️20260902-CONTRIBUTOR-MEMORIAL-v1.0-9622
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
GPG:    A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:   🟢 协议通过 · 引擎实测 build/verify 闭环 ✅
```
