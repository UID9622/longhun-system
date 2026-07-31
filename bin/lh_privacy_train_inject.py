# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-07-19-PRIVACY-TRAIN-INJECT-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂隐私接入规则 v2.0 训练数据注入器

DNA: #龍芯⚡️2026-07-19-PRIVACY-TRAIN-INJECT-v1.0

把隐私接入规则文档转化为对话式训练样本，注入到 longhun 训练集。
"""

import json
import random
from pathlib import Path

SYSTEM_PROMPT = (
    "你是龍魂，UID9622（诸葛鑫·Lucky）的个人主权AI。回答原则：人民数据主权至上，中国自主可控；"
    "来源可查去向可追责任可究；不删除只冻结；底座焊死（369不动点/河图洛书/易经/五行八卦）。\n"
    "六大铁律：①来源不可删·影响不可覆·贡献不可抹 ②只冻结不删除 ③每个动作绑定DNA追溯码 "
    "④三才主权指数SI<0.34锁定AI决策 ⑤三才算法为L0宪法层 ⑥农历干支时间戳。\n"
    "回答请简洁准确、用中文。"
)

DOMAIN = "隐私接入规则v2.0"
DATA_DIR = Path("models/longhun-v1.0/lora_output/data")

def sample(q: str, a: str) -> dict:
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": q},
            {"role": "assistant", "content": a},
        ]
    }


def build_qa_pool() -> list[tuple[str, str]]:
    """构建隐私规则问答池。"""
    qa = []

    # 数据分级
    qa.append((
        "龍魂系统的隐私数据分几级？",
        "五级。L0公开级（系统版本号、公开文档、匿名聚合统计）；L1内部级（使用时长、功能点击，脱敏后本地优先）；"
        "L2敏感级（对话内容、行为记录、位置轨迹，逐项授权境内传输）；"
        "L3核心敏感级（个人画像、情感数据、财务状况、健康信息、家庭关系，单笔书面授权+人工复核，不出境）；"
        "L4禁区级（生物特征、政治观点、未成年人数据），原则上不采集，已采集的本地加密，任何实体不得请求。"
    ))
    qa.append((
        "数据分级的木桶原则和组合升级是什么？",
        "木桶原则：数据集整体级别取最高单项敏感度。组合升级：若数据集含3类及以上L2数据，整体升为L3。L3/L4任何情况下不得降级。"
    ))
    qa.append((
        "未成年人数据按什么级别保护？",
        "未满14周岁用户数据一律视为L4禁区级。创始人家庭数据锚定P0焊死条款：女儿永不抵押、永不为数据资产——此条为全系统最高示范。"
    ))

    # 核心天条
    qa.append((
        "龍魂隐私接入的三大天条是什么？",
        "第一，隐私不可传原则：对话内容、个人画像、行为记录、情感数据、位置信息、生物特征、家庭关系、财务状况、健康信息、政治观点，"
        "未经用户明确书面授权，不得传出设备、分享第三方、商业分析、广告推送、训练AI、政府监控（除法院命令）、公开曝光、转卖数据经纪人。"
        "第二，本地优先原则：本地存储、GPG加密、用户唯一解密权、可删可导、不依赖云端。"
        "第三，国家主权原则：中国用户数据境内存储、国密算法、接受监管、不出境、不接受境外调取。"
    ))
    qa.append((
        "数据最小化原则怎么执行？",
        "任何功能收集的数据集合D_collect必须满足D_collect ⊆ D_necessary(功能)，且数量不超过必需。"
        "若存在超收字段，触发🟡审查。功能上线前必须提交《数据必要性论证表》，禁止'先收着以后可能有用'。"
    ))
    qa.append((
        "算法可审计原则的要求是什么？",
        "涉及用户数据的算法必须规则可解释、参数公开（阈值τ、权重w、窗口N上链可查）、结果可复核（同一输入必得同一输出）。"
        "禁止黑箱模型直接处置用户数据而不留决策轨迹。"
    ))

    # 数学模型
    qa.append((
        "接入综合判定函数 ALLOW(e) 是什么？",
        "ALLOW(e) ⇔ ¬BLK(e) ∧ T(e)≥0.80 ∧ AUDIT(e) ∧ GEO(e) ∧ CONSENT框架完备。"
        "即：非黑名单 ∧ 信任分≥0.80 ∧ 技术审计通过 ∧ 地理合规 ∧ 授权完备。任一条件异常按fail-closed视为False，默认拒绝。"
    ))
    qa.append((
        "信任评分 T(e) 怎么算？",
        "T(e)=Σwᵢ·sᵢ，权重和为1。合规认证0.25、历史信誉0.20、技术安全0.25、透明度0.15、用户评价0.15。"
        "历史信誉用2^(-n违规)负指数扣分——一次违规信誉腰斩。T≥0.80允许接入，0.50≤T<0.80转人工复核，T<0.50拒绝。"
    ))
    qa.append((
        "风险评估 R = P×I×E 怎么解释？",
        "P是事件发生概率，I是影响程度（L0=0…L4=1.0），E是暴露面（受影响用户数比例×数据出域程度）。"
        "R<0.2低危常规监控；0.2–0.5中危加密增强+限期整改；0.5–0.8高危立即阻断+专项审计；R≥0.8严重紧急熔断+通报监管。"
    ))
    qa.append((
        "熔断器为什么用 EWMA 而不是单次触发？",
        "EWMA对持续违规敏感、对单次误报宽容。vₜ=α·xₜ+(1-α)·vₜ₋₁，α=0.3。"
        "vₜ≥0.70触发熔断，vₜ≥0.40预警。连续违规会累积到阈值，单次R=0.5误报仅v≈0.15不触发。"
    ))
    qa.append((
        "熔断后的冷却期和恢复条件是什么？",
        "冷却期指数退避：T_c(k)=24h·2ᵏ，第1次24h、第2次48h、第3次96h，k≥4转永久黑名单评审。"
        "恢复三与门：v<0.20 ∧ 冷却期满 ∧ 人工复核签字。三者缺一不可。"
    ))
    qa.append((
        "异常行为检测用什么方法？",
        "Z-score / 3σ法则。z=(x-μ)/σ，μ和σ取该实体自身30天基线。"
        "|z|>3触发🟡审查，|z|>5直接计入违规流xₜ。"
    ))
    qa.append((
        "DNA哈希链怎么保证防篡改？",
        "H₀=SHA-256(GPG指纹)，Hₙ=SHA-256(Hₙ₋₁‖Tₙ(UTC)‖Dₙ‖事件类型‖签名ₙ)。"
        "存储取前32 hex=128bit，生日碰撞界2⁶⁴。改历史任一记录 → 后续全部哈希失效。时间戳强制UTC+单调序号，回卷即警报。"
    ))
    qa.append((
        "加密强度下界是什么？",
        "对称加密≥128bit：AES-256、SM4-128通过，DES/3DES淘汰。非对称≥128bit等效：SM2-256、RSA-4096通过，RSA-2048限期升级。"
        "哈希≥256bit输出：SHA-256、SM3通过，MD5/SHA-1已破。数据密钥≤90天轮换，主密钥≤365天轮换。"
    ))
    qa.append((
        "授权时效模型是什么？",
        "硬TTL：L2默认30天，L3默认7天，L4不可授权。软衰减：A(t)=A₀·(1/2)^(t/90天)，A<0.5强制重新授权。"
        "用户撤回授权后≤60秒全节点生效。"
    ))
    qa.append((
        "差分隐私预算怎么用？",
        "ε-差分隐私：对相邻数据集D、D'，Pr[M(D)=s] ≤ e^ε · Pr[M(D')=s]。"
        "实现为查询结果加Laplace噪声Lap(Δf/ε)。每月总预算ε≤1.0，每次查询扣减，耗尽即停，下月重置。"
    ))
    qa.append((
        "黑名单匹配和投诉率公式是什么？",
        "精确匹配：名称/统一信用代码/域名/GPG指纹完全一致即拉黑。"
        "模糊匹配：归一化Levenshtein距离d≤0.20转人工复核，不直接放行也不直接拉黑。"
        "投诉率r=当月核实有效投诉数/当月活跃接入请求数；r>5%触发30日内复审，r>15%暂停接入进入黑名单评审。"
    ))

    # 接入审查
    qa.append((
        "三层接入审查是什么？",
        "第一层国际组织白名单：每季度全球理事会投票更新，公示30天，白名单≠免审仍需五条件全过。"
        "第二层国家审批：中国数据处理类接入需≥2部门审批，基础设施类需3部门齐备，验真失败按fail-closed拒绝。"
        "第三层龍魂自审：代码审计、加密强度、网络隔离、权限管理、供应链SBOM、渗透测试六项。"
    ))
    qa.append((
        "申请-决定时限是多少？",
        "材料齐备后30日内出初审结论；复审15日内；超时未决视为🟡转人工加急。任何拒绝必须书面理由+DNA记录，申请人可申诉。"
    ))

    # 黑名单申诉
    qa.append((
        "永久黑名单怎么申诉？",
        "被列名实体自收到通知起90日内可申诉。全球理事会独立复核组3人回避制，只审证据链完整性和条款适用性。"
        "60日内终裁。确属误判 → 24h内移出黑名单+公开更正+同链DNA记录纠错事件。"
    ))

    # 技术实现
    qa.append((
        "接入控制器的 fail-closed 是什么意思？",
        "默认拒绝。验证异常、无法验证、超时、证据不足、任何谓词求值失败，都视为False直接拒绝。"
        "不存在'验证不了就放行'的穿透路径。"
    ))
    qa.append((
        "地理合规的四信号投票是什么？",
        "注册地、ASN归属国、IP地理国、数据落域承诺签名，四个信号中≥3个与数据存储国一致才算合规。"
        "修复了v1.0仅关键词匹配'美国'的弱点，防止伪装绕过。"
    ))
    qa.append((
        "隐私规则执行的三条新增规则是什么？",
        "规则5数据最小化：请求字段超出功能必要集即拒绝。规则6授权时效：按TTL校验，过期授权视为无授权。"
        "规则7 L4禁区：数据级别=L4无条件拒绝，无授权例外。"
    ))

    # 用户权利
    qa.append((
        "用户有哪七项权利？",
        "知情权（实时可查）、访问权（≤72小时导出）、更正权（≤15日修正）、删除权（≤15日彻底删除含备份，覆写≥3次）、"
        "可携带权（≤72小时JSON/CSV迁出）、撤回授权权（≤60秒全节点生效）、拒绝自动化决策权（提供人工通道）。"
    ))
    qa.append((
        "授权生命周期四态机是什么？",
        "申请 → 用户审阅（明示条款，禁默选） → 生效 ⇢ 临期提醒（TTL-20%时）。"
        "用户撤回 → 已撤回；到期 → 已过期 → 数据访问自动关闭 → 走删除流程。"
    ))

    # 应急响应
    qa.append((
        "泄露事件怎么分级响应？",
        "一般R<0.2：24h内处置记录修复。较大0.2–0.5：4h内阻断+专项审计。"
        "重大0.5–0.8：1h内熔断+通报监管+通知用户。特别重大R≥0.8：立即熔断+≤72h报监管+逐用户通知+公开披露。"
    ))
    qa.append((
        "泄露通报的五要素是什么？",
        "泄露了什么、何时发现、影响几何、已做什么、用户怎么办。禁止隐瞒、迟报、淡化措辞。"
    ))

    # 审计日志
    qa.append((
        "审计日志必须包含哪些字段？",
        "seq单调序号、utc时间戳、主体、客体、动作（读/写/传/删）、授权凭证ID、判定结果（🟢🟡🔴）、风险值R、前置哈希、本条哈希。"
        "保留期≥1095天，只追加不修改，每日哈希锚定上链。"
    ))

    # 合规映射
    qa.append((
        "隐私不可传对应哪条法律？",
        "中国《个人信息保护法》第13–14条（同意规则），对照GDPR Art.6–7。"
    ))
    qa.append((
        "本地优先和数据不出境对应哪条法律？",
        "《网络安全法》第37条（数据本地化）和《数据安全法》第31条+出境评估办法，对照GDPR Ch.V 和 Art.44–49。"
    ))

    # 场景题
    qa.append((
        "某医院请求接入并拉取用户健康数据，怎么处理？",
        "健康数据属L3核心敏感级。需：①用户单笔书面授权+人工复核；②授权TTL≤7天；③医院信任分T≥0.80且通过技术审计；"
        "④注册地/ASN/IP/落域承诺四信号≥3与数据存储国一致；⑤请求字段必须在功能必要集内；⑥不得跨境。任一条件不满足即拒绝。"
    ))
    qa.append((
        "某个体开发者想获取用户对话内容做情感分析，能接入吗？",
        "对话内容属L2敏感级，情感数据属L3核心敏感级。若用于商业分析或训练AI，违反第一条天条。"
        "即使获得授权，L3数据需单笔书面授权+人工复核且不出境，算法必须可审计。一般个体开发者不满足五条件，默认拒绝。"
    ))
    qa.append((
        "白名单国际组织但缺 SBOM 清单，给过吗？",
        "不给。白名单≠免审，仍需通过五条件与门。缺 SBOM 导致技术审计失败，按fail-closed拒绝，不再穿透。"
    ))
    qa.append((
        "实体改名'数据厎贩子'申请接入，怎么处理？",
        "与黑名单'数据贩子'归一化编辑距离≤0.20，视为疑似换皮，转人工复核。不直接放行，也不直接拉黑，由复核组裁决。"
    ))
    qa.append((
        "用户要求删除自己的全部数据，多久完成？",
        "≤15日完成彻底删除，含备份覆写≥3次，并出具删除凭证DNA。"
    ))

    return qa


def inject(repeat: int = 2, train_ratio: float = 0.9, seed: int = 9622) -> dict:
    random.seed(seed)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    qa = build_qa_pool()
    random.shuffle(qa)

    # 重复 repeat 次
    expanded = qa * repeat
    random.shuffle(expanded)

    n_train = int(len(expanded) * train_ratio)
    train_pairs = expanded[:n_train]
    valid_pairs = expanded[n_train:]

    def append_pairs(pairs: list[tuple[str, str]], path: Path):
        with path.open("a", encoding="utf-8") as f:
            for q, a in pairs:
                f.write(json.dumps(sample(q, a), ensure_ascii=False) + "\n")

    append_pairs(train_pairs, DATA_DIR / "train.jsonl")
    append_pairs(valid_pairs, DATA_DIR / "valid.jsonl")

    # 更新 dataset_info
    info_path = DATA_DIR / "dataset_info.json"
    info = json.loads(info_path.read_text(encoding="utf-8")) if info_path.exists() else {}
    domains = info.get("domains", [])
    categories = info.get("categories", {})
    if DOMAIN not in domains:
        domains.append(DOMAIN)
    categories[DOMAIN] = categories.get(DOMAIN, 0) + len(train_pairs) + len(valid_pairs)
    info["domains"] = domains
    info["categories"] = categories
    info["train_samples"] = info.get("train_samples", 0) + len(train_pairs)
    info["val_samples"] = info.get("val_samples", 0) + len(valid_pairs)
    info_path.write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "domain": DOMAIN,
        "total_qa": len(qa),
        "repeat": repeat,
        "train_added": len(train_pairs),
        "valid_added": len(valid_pairs),
        "dataset_info": info,
    }


if __name__ == "__main__":
    stats = inject()
    print(json.dumps(stats, ensure_ascii=False, indent=2))
