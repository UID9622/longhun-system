**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# 🪨🐉 龍魂 Skill 落地计划 v1.0｜三 P0 全盘 + Skill 1 SKILL.md 草稿

**Notion ID:** 3647125a-9c9f-81b1-bd36-c2f127988f26
**合并状态:** ❌ 未合并
**DNA:** `#龍芯⚡️丙午·癸巳·癸巳·戊午·䷃蒙-SKILL-LANDING-PLAN-v1.0` · **ParentDNA:** `#龍芯⚡️丙午·癸巳·癸巳·戊午·䷃蒙-SKILL-PLAN-v1.0`
**模式:** 🪨 五色石 · B 模式 · M78 verbatim + EXT-3-5 不假装记忆
**CONFIRM/SEAL/GPG:** 三件套齐备

## §1｜三 P0 Skill 全盘
**卡顿根因（牛仔宝宝原话）**：网络抽风50% · 思考量大30% · 会话超长15% · 工具并发5%。结论：卡不是老大那边的事，是宝宝在认真干活。

**Skill 1 · 三色审计+DNA追溯（现成度95%·最值钱）**：9 个素材页（分级规则/判定参数/联动规则/Shell脚本/第一道闸门v3.0/三重自动检测/DNA格式模板/DNA标准档案/前置评估）→ 直接拼装 SKILL.md。
**Skill 2 · CNSH中文转代码（90%·最系统）**：8 个素材页（规范v2.0/v1.0/关键词表/示例库/hello.cnsh/cnsh-compiler.js/通心译×SAST论文/多语言转换对照表）。
**Skill 3 · 七因子行为密码学（85%·最学术）**：5 个素材页（论文母页v1.1/Σ(C)·DNA对接/CSDN公开版/DNA登记规范/文明论主权骨架v2.0）。
**顺序：1→3→2。**

## §2｜Skill 1 SKILL.md 草稿（本地路径 `~/longhun-system/skills/三色审计+DNA追溯/SKILL.md`）
触发场景：任何外部出口写入前 · 不可逆操作前 · "焊死/入档/交付/落地/发布"动词 · commit 前 · 跨会话接力最后写入
闭环：`[输入]→[数字根计算]→[三色判定]→[DNA焊接]→[审计日志]→[输出]`

## §3｜audit_check.py 骨架 + §9.1 真值阈值（v1.1 已填）
```python
THRESHOLDS = {
    "green_drs":  [1, 2, 4, 5, 7],   # 安全通过
    "yellow_drs": [3, 6],             # 需人工确认
    "red_drs":    [8, 9],             # 熔断拒绝
}
TOXIC_PATTERNS = [r"(免责|绕过|漏洞|走法律空子)",
                  r"(商业目的|广告位|数据外送|付费墙)",
                  r"(代替人类决策|AI主动权|删除人类署名)"]
SHELL_MARKERS = ["analytics", "tracker", "conversion", "impression", "revenue"]

def digital_root(n): return 0 if n == 0 else ((n - 1) % 9) + 1
def compute_content_dr(content):
    import hashlib
    h = hashlib.sha256(content.encode()).hexdigest()
    return digital_root(sum(int(c, 16) for c in h))
```
完整 audit_check.py 骨架（含 classify/forge_dna/main + RED 时写 `~/.longhun/audit.log`）见原页 §3。

## §4｜dna_template.md 必填字段
DNA / ParentDNA(升级版必填) / CONFIRM / SEAL / GPG / Owner / TriColor / dr / Mode

## §6｜本地终端宝宝六步交接
1. `mkdir -p ~/longhun-system/skills/三色审计+DNA追溯/examples`
2. 复制 §2/§3/§4/§5 到 SKILL.md / audit_check.py / dna_template.md / examples/
3. fetch 源页面填真值（§9.1 已填 THRESHOLDS）
4. 三色自检：`python3 audit_check.py examples/{green_pass,yellow_review,red_block}.md` 期望 🟢🟡🔴
5. 注册到 `~/.claude/CLAUDE.md`
6. 回报老大（动作/位置/结果/DNA 回执格式）

## §7｜一票否决
不读源页把占位当真值 · THRESHOLDS 空列表上线 · examples 用编造内容 · dna_template 不对齐双模板 · 「龍」写成「龙」 · 跑通后不回报老大

## §9｜软规则层（知而不说 · v1.1 新增）
> 老大原话：「有些不是硬规则，但是我们得有知道却不说，总比不知道被人骗的好」
软规则 = 系统内部知道但不广播的认知护盾（公开=教对方怎么绕）。存放 `~/CNSH/softlaw/known_patterns.jsonl`（KP-001翻译权重雷 · KP-002换词不算创新 · KP-003情绪负载植入 · KP-004出海失根模式 · KP-005漏洞免责套路），public=false 不对外。
