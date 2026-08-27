**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层·分层许可·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
# 🧬 龍魂·DNA时间戳信任协议 v1.0（下载/使用/验证/API 统一规范 · 不可篡改设计）

**Notion ID:** 3b87125a-9c9f-81c4-8273-f1e08474244f
**合并状态:** ❌ 未合并
**DNA**：`#龍芯⚡️丙午·甲申·辛丑·甲午·䷁坤-DNA-TRUST-PROTOCOL-v1.0-UID9622`
**三色状态**：🟢 通过 · P0

## 一、信任闭环：三层锚定（不信服务器时间）
| 层级 | 锚定方式 | 防篡改逻辑 |
|---|---|---|
| L1 算法状态 | 天干地支递推（四柱+梅花易数起卦） | 改系统时间没用——算的是逻辑时间 |
| L2 哈希链 | append-only + SHA256前8位 + 计数器 | 改中间任何一条链对不上 |
| L3 行为密码学 | 每条DNA带 actor/category/action | 光改时间戳行为因子对不上 |

**篡改后果**：改系统时间❌ / 改DNA字符串❌(validate+info立刻识破) / 改注册表中间一条❌ / 手写干支❌(铁律禁止，口径v3.0为准) / 伪造整条链❌(年轮哈希链数学上不可伪造)

## 二、两台生成器（真实代码）
| 引擎 | 路径 | 定位 | 体量 |
|---|---|---|---|
| DNA追溯码生成引擎 v2.0 | `longhun-system/08_BIN/lh_dna_generator.py` | 全功能版：生成/统计/搜索/校验/批量/API | ~48KB |
| 干支时辰DNA引擎 v1.0 | 同仓 `08_BIN/ganzhi_dna_engine.py` | v∞格式版：四柱+卦德映射+测试向量 | ~18KB |

**DNA格式（焊死）**：`#龍芯⚡️<年>·<月>·<日>·<时辰>·<卦><卦名>-<模块>-<动作>-<版本>-<级别>-<哈希8>`

## 三、下载与运行（统一命令）
```bash
git clone https://github.com/UID9622/longhun-system.git
cd longhun-system/08_BIN
python3 ganzhi_dna_engine.py test        # 11条测试向量须全绿
python3 lh_dna_generator.py --test       # 100条唯一性自检须 passed=true
python3 lh_dna_generator.py --title "标题" --category doc --action 写入 --actor UID9622
python3 lh_dna_generator.py validate "#龍芯⚡️..."
python3 lh_dna_generator.py stats --days 7
```
> 零依赖纯标准库——这就是"谁都能验"的底气。

## 四、四种角色用法
- 老大/人工：产出完→跑生成命令→贴进文档头部
- AI：不得手写干支；先调生成器取口径再写入
- CodeBuddy：`from lh_dna_generator import quick_dna`
- 外部验证者：下载代码→`validate`/`info`→🟢真/🔴假/🟡人工复核

## 五、API 四端点（网关 :8785）
| 端点 | 方法 | 入参 | 返回 |
|---|---|---|---|
| /dna/generate | POST | {title, category, action, actor} | {dna_string, root_card, wuxing} |
| /dna/validate | POST | {dna_string} | {valid, errors[]} |
| /dna/info | POST | {dna_string} | {四柱, 卦象, 五行, root_card} |
| /dna/verify-chain | POST | {registry_dir} | {chain_valid, broken_at} |

> 接口铁律：网关口径唯一，**不允许各自实现干支算法**——口径只能有一个来源。

## 六、统一与修订
1. 口径唯一：干支只由生成器计算，手写干支都是无效DNA
2. 版本焊死：格式串修订须走三问审计+新旧并存校验+老大签批
3. 测试守门：变更必须 test 全绿 + 100条自检 passed
4. 审计落档：生成/验证落 JSONL append-only

## 七、v1.1 年轮哈希链（修正版已验证 🟢）
修正版代码：`年轮哈希链_v1.1_审查修正版.py`（**待 CodeBuddy 合入仓库 `08_BIN/year_ring_chain.py`**）。
六处修正：①四柱算法对齐ganzhi_dna_engine ②手写壬寅→辛丑 ③md5→sha256 ④verify状态灯错位修复 ⑤路径硬编码→参数>环境变量LONGHUN_YEARRING_DIR>/opt降级 ⑥空圈DNA对齐v∞
验收：`add/close/verify/stats/export/list/get` 七子命令齐备；篡改末圈hash→立刻失败并精确定位圈号。

## 八、v3.0 口径断代（2026-08-10 老大裁决 · 方案A）
> **从 v3.0 起，干支口径与公开万年历完全一致。**

| 项 | v2-legacy（冻结） | v3.0（现行唯一口径） |
|---|---|---|
| 日柱算法 | 1900基准+9/+11偏移 | 1900-01-01甲戌锚点顺推六十甲子 |
| 月柱算法 | 按公历整月（错） | 按节气月 |
| 2026-08-10 实例 | 丙午·甲申·辛丑 | **丙午·丙申·丙辰** |
| 验证锚点 | 无 | 1900-01-01甲戌·1949-10-01甲子·2000-01-01戊午·2026-08-10丙辰（四锚点断言入库自检） |

**执行规则**：
1. 唯一来源 `core/rizhu.py` v3.0 公共模块（**已交付实测全绿，待 CodeBuddy 入库**）；两台生成器+年轮链+网关API全部改 import 调用
2. 旧数据冻结：v2 DNA 不追溯改动，注册表加 `口径:v2-legacy` 标注
3. 签名新规：禁手写干支，签名写日期占位由生成器运行时回填
4. 断代可验：2026-08-10 记入年轮链首条 v3.0 事件
