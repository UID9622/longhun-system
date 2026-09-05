# CONTRIBUTING · cnsh-bridge

> DNA: `#龍芯⚡️2026-09-05-CNSH-BRIDGE-CONTRIBUTING-v1.0-UID9622`
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰

## 本仓库的贡献=无偿署名（Community Credit）

按 UID9622 社区规则（alignment v2.6 第十九层 · 焊死）：**所有贡献一律无偿署名**，
不承诺/不支付任何现金/代币/实物报酬；请勿在 Issue/PR 中索要付款。
龍魂体系整体收益的贡献者权益（含世袭/基金会出口）见 `01_protocols/LH-CONTRIBUTOR-PERPETUITY-CHARTER-v1.0.md`。

## 开发准则

1. **语法权威优先**：CNSH 改动以 `tests/cnsh_samples/`（P0 基线）为准，新增语法须同批提交样本
2. **生成物勿手改**：`cpp/cnsh_logic.c` 由 `08_BIN/cnsh_cgen.py --no-main` 生成，改源头不改成品
3. **判据④实机验证**：代码改动须给可复现命令（本机 clang 冒烟为最小门槛；鸿蒙侧标 🟡 待 DevEco）
4. **无编造**：性能数字/仓库链接/语法特性必须真实可溯，拿不准标 🟡
5. **四行文件头**：DNA/创建者/归属名/许可证分层（思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2）

## 提交流程

1. 本地跑通：`python3 08_BIN/cnsh_cgen.py cnsh/hello.cnsh --out /tmp/x.c && clang /tmp/x.c -o /tmp/x && /tmp/x`
2. GPG 签名：`python3 bin/lh_gpg_sign.py sign <改动文件>`
3. 过闸口：命名/归属名/三色自查后提交（CLI 脚本类自动走 `08_BIN/lh_cnsh_gate.py --record` 留档）
4. PR 至 `UID9622/longhun-system`（monorepo 内本模块路径 `harmonyos/cnsh-bridge/`）

## 签名

```
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
