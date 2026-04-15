# 🇨🇳 中国文化元宇宙·Notion数据库完整Schema

**DNA追溯码：** #ZHUGEXIN⚡️2026-01-25-中国文化Schema-v1.0

---

## 📊 Database 1: Scene（场景库·中华时空）

### 核心字段
| 字段名 | 类型 | 选项/说明 | 示例 |
|--------|------|-----------|------|
| Name | Title | 场景名称 | 长安城·大明宫 |
| Dynasty | Select | 远古/夏商周/春秋战国/秦汉/三国/魏晋南北朝/隋唐/五代十国/宋/元/明/清/近现代 | 唐朝 |
| HistoricalPeriod | Text | 具体年代 | 公元618-907年 |
| Type | Select | 宫殿/城市/山水/园林/寺庙/村落/战场/洞天福地 | 宫殿 |
| BBox | Text | 范围[长,宽,高] | [500,500,100] |
| CulturalDNA | Multi-select | 儒/道/佛/法/墨/兵/其他 | 儒家,盛唐气象 |
| PhilosophyTheme | Select | 天人合一/中庸之道/道法自然/因果轮回/其他 | 天人合一 |
| Architecture | Multi-select | 宫殿/亭台/楼阁/廊桥/牌坊/四合院 | 宫殿,楼阁 |
| NaturalElement | Multi-select | 山/水/云/风/日/月/星/雨/雪/雾 | 云,风 |
| CulturalSymbol | Multi-select | 龍/凤/麒麟/玄武/朱雀/白虎/青龍 | 龍,凤 |
| Skybox URL | URL | 天空盒贴图 | https://... |
| Ground Material | URL | 地面材质 | https://... |
| Lighting | Number | 光照0-1 | 0.8 |
| Gravity | Number | 重力 | 9.8 |
| Objects | Relation | 关联物件 | → Object DB |
| Rules | Relation | 关联规则 | → Rules DB |
| Events | Relation | 关联事件 | → Events DB |
| MusicTheme | Text | 背景音乐主题 | 古筝,琵琶 |
| SeasonalEffect | Select | 春/夏/秋/冬/不变 | 春 |
| TimeOfDay | Select | 晨/午/暮/夜/不变 | 暮 |
| CulturalFestival | Multi-select | 春节/清明/端午/中秋/重阳 | 春节 |
| PoetryInspiration | Text | 相关诗词 | "长安一片月，万户捣衣声" |
| HistoricalEvents | Relation | 历史事件 | → Events DB |
| FamousFigures | Relation | 著名人物 | → Actor DB |
| DiplomaticStatus | Select | 和平/战争/商贸/封闭 | 和平 |
| Prosperity | Number | 繁荣度0-10 | 9 |
| CulturalInfluence | Number | 文化影响力0-10 | 10 |
| Created | Created time | 创建时间 | 自动 |
| Last Edited | Last edited time | 最后编辑 | 自动 |

---

## 📊 Database 2: Object（物件库·中华器物）

### 核心字段
| 字段名 | 类型 | 选项/说明 | 示例 |
|--------|------|-----------|------|
| Name | Title | 物件名称 | 青铜九鼎 |
| Category | Select | 礼器/乐器/兵器/文房/日用/建筑构件/装饰/服饰 | 礼器 |
| Dynasty | Select | 同Scene | 商周 |
| Type | Select | Prop/Interactive/NPC/Item | Prop |
| Model URL | URL | 3D模型地址 | https://... |
| Transform | Text | [位置,旋转,缩放] | [0,0,0],[0,0,0],[1,1,1] |
| Scene | Relation | 所属场景 | → Scene DB |
| Material | Multi-select | 青铜/玉石/陶瓷/木/竹/绸/纸/金/银/铁 | 青铜 |
| CraftsmanshipLevel | Select | 官窑/民窑/皇家/贡品/民间/工匠 | 皇家 |
| CulturalMeaning | Text | 文化寓意 | 国之重器，象征统治权威 |
| SymbolicPattern | Multi-select | 龍纹/凤纹/云纹/回纹/饕餮/夔纹 | 龍纹,饕餮 |
| PhilosophyConnection | Multi-select | 儒/道/佛/法/墨/兵 | 儒家 |
| HistoricalStory | Text | 相关典故 | 问鼎中原 |
| RitualUse | Select | 祭祀/礼仪/日用/装饰/兵器/其他 | 祭祀 |
| Rarity | Select | 常见/罕见/稀有/绝世 | 绝世 |
| Durability | Number | 耐久度 | 100 |
| CulturalValue | Number | 文化价值0-10 | 10 |
| ArtisticValue | Number | 艺术价值0-10 | 9 |
| Interactions | Relation | 可交互方式 | → Interaction DB |
| Events | Relation | 触发事件 | → Events DB |
| OwnerHistory | Text | 历任拥有者 | 夏启→商汤→周武王 |
| State | Select | Visible/Hidden/Locked/Broken | Visible |
| Pickable | Checkbox | 可拾取 | ✓ |
| Blessing | Text | 祝福效果 | 增加威望+5 |
| Curse | Text | 诅咒效果 | 无 |
| RelatedPoetry | Text | 相关诗文 | "钟鼎山林各天性" |
| DNA Tags | Multi-select | 自定义标签 | 权力,庄重,青铜时代 |
| Created | Created time | 创建时间 | 自动 |
| Last Edited | Last edited time | 最后编辑 | 自动 |

---

## 📊 Database 3: Rules（规则库·天道法则）

### 核心字段
| 字段名 | 类型 | 选项/说明 | 示例 |
|--------|------|-----------|------|
| Name | Title | 规则名称 | 天道酬勤 |
| Category | Select | 道德/物理/经济/战斗/社交/天气/时间 | 道德 |
| PhilosophySchool | Multi-select | 儒/道/佛/法/墨/兵 | 儒家 |
| MoralLevel | Select | 天道/人道/地道 | 天道 |
| VirtueType | Multi-select | 仁/义/礼/智/信/忠/孝/廉/耻 | 勤,智 |
| Trigger | Text | 触发条件 | 持续努力工作 |
| Condition Expression | Text | 条件表达式 | effort > 80 && time > 30days |
| Action | Text | 执行动作 | 增加技能熟练度 * 1.5 |
| KarmaEffect | Select | 善报/恶报/中性/因果循环 | 善报 |
| SocialHarmony | Number | 社会和谐影响-10到+10 | +5 |
| WisdomLevel | Select | 初学/领悟/精通/大师/圣人 | 精通 |
| Scope | Select | Scene/Object/Actor/Global | Actor |
| Priority | Select | Low/Medium/High/Critical | High |
| Cooldown | Number | 冷却时间(秒) | 0 |
| Bound Objects | Relation | 绑定物件 | → Object DB |
| Bound Scenes | Relation | 绑定场景 | → Scene DB |
| Bound Actors | Relation | 绑定角色 | → Actor DB |
| HistoricalExample | Text | 历史案例 | 苏秦刺股,终成大器 |
| ClassicQuote | Text | 经典语录 | "天行健，君子以自强不息" |
| ModernApplication | Text | 现代应用 | 学习工作中的坚持 |
| ConflictsWith | Relation | 冲突规则 | → Rules DB |
| Enabled | Checkbox | 是否启用 | ✓ |
| DNA Tags | Multi-select | 自定义标签 | 儒家,励志,奋斗 |
| Created | Created time | 创建时间 | 自动 |
| Last Edited | Last edited time | 最后编辑 | 自动 |

---

## 📊 Database 4: Events（事件库·华夏史诗）

### 核心字段
| 字段名 | 类型 | 选项/说明 | 示例 |
|--------|------|-----------|------|
| Name | Title | 事件名称 | 三顾茅庐 |
| EventType | Select | 历史/神话/传说/典故/节日/灾难/战争/外交 | 典故 |
| Dynasty | Select | 同Scene | 三国 |
| HistoricalFigure | Multi-select | 关联人物 | 刘备,诸葛亮 |
| MoralLesson | Text | 道德教益 | 礼贤下士,求贤若渴 |
| CulturalImpact | Number | 文化影响0-10 | 9 |
| StoryArc | Select | 起/承/转/合 | 转 |
| PhilosophyTheme | Multi-select | 同Rules | 儒家 |
| Trigger Type | Select | onEnterScene/onClick/onTime/onCondition/onDivinationSign | onCondition |
| Trigger Params | Text | 触发参数 | player.reputation > 50 |
| Actions | Relation | 执行规则 | → Rules DB |
| Next Event | Relation | 下一事件 | → Events DB (隆中对) |
| Alternative Event | Relation | 分支事件 | → Events DB |
| Delay | Number | 延迟(秒) | 0 |
| Condition | Text | 前置条件 | 已拜访两次 |
| Repeatable | Select | Once/Daily/Weekly/Unlimited | Once |
| LocationBound | Relation | 绑定地点 | → Scene DB (隆中) |
| TimeRequirement | Text | 时间要求 | 冬季 |
| WeatherRequirement | Select | 晴/雨/雪/雾/任意 | 雪 |
| NarrativeText | Text | 叙事文本 | "将军既帝室之胄..." |
| DialogueOptions | Text | 对话选项 | [恳请出山/离去] |
| SuccessOutcome | Text | 成功结果 | 诸葛亮同意出山 |
| FailureOutcome | Text | 失败结果 | 需再次拜访 |
| RelatedPoetry | Text | 相关诗词 | "三顾频烦天下计" |
| HistoricalAccuracy | Select | 史实/演义/虚构 | 史实 |
| EmotionalTone | Select | 悲壮/豪迈/哀愁/欢喜/庄严 | 真诚 |
| MusicCue | Text | 音乐提示 | 古琴曲《卧龍吟》 |
| CinematicSequence | URL | 过场动画 | https://... |
| Achievement | Relation | 解锁成就 | → Achievement DB |
| DNA Tags | Multi-select | 自定义标签 | 求贤,三国,典故 |
| Created | Created time | 创建时间 | 自动 |
| Last Edited | Last edited time | 最后编辑 | 自动 |

---

## 📊 Database 5: Interaction（交互库·华夏礼仪）

### 核心字段
| 字段名 | 类型 | 选项/说明 | 示例 |
|--------|------|-----------|------|
| Name | Title | 交互名称 | 作揖行礼 |
| Type | Select | 礼仪/对话/拾取/使用/学习/战斗/交易/祭祀 | 礼仪 |
| EtiquetteLevel | Select | 日常/正式/重大仪式 | 正式 |
| SocialContext | Multi-select | 家庭/官场/江湖/文坛/市井/军营 | 官场 |
| VirtueExpression | Multi-select | 仁/义/礼/智/信 | 礼 |
| RelationshipImpact | Number | 亲密度变化-10到+10 | +3 |
| CulturalDepth | Select | 表层/深层/精髓 | 深层 |
| ProprietyLevel | Select | 符合/勉强/违背礼制 | 符合 |
| Associated Object | Relation | 关联物件 | → Object DB |
| Associated Event | Relation | 关联事件 | → Events DB |
| UI Type | Select | 按钮/文本提示/自动/手势 | 手势 |
| Condition | Text | 前置条件 | 同朝为官 |
| Result | Text | 交互结果 | 增加威望+2 |
| Cooldown | Number | 冷却时间 | 5 |
| RequiredEtiquette | Number | 礼仪要求0-10 | 6 |
| SuccessDialogue | Text | 成功对话 | "久仰大名" |
| FailureDialogue | Text | 失败对话 | "失礼了" |
| BodyLanguage | Text | 肢体语言 | 双手抱拳,躬身 |
| VoiceTone | Select | 恭敬/平和/威严/亲切 | 恭敬 |
| HistoricalReference | Text | 历史参考 | 古代官员朝见礼仪 |
| ModernEquivalent | Text | 现代对应 | 握手问候 |
| SeasonalVariation | Text | 季节变化 | 春节加拜年祝福 |
| Analytics Tag | Multi-select | 统计标签 | 社交,礼仪,官场 |
| DNA Tags | Multi-select | 自定义标签 | 儒家,礼制,尊重 |
| Created | Created time | 创建时间 | 自动 |
| Last Edited | Last edited time | 最后编辑 | 自动 |

---

## 📊 Database 6: Actor（角色库·华夏众生）

### 核心字段
| 字段名 | 类型 | 选项/说明 | 示例 |
|--------|------|-----------|------|
| Name | Title | 角色名称 | 诸葛亮·孔明 |
| CharacterArchetype | Select | 忠臣/义士/才子/佳人/神仙/妖魔/百姓/商贾/工匠 | 忠臣 |
| Dynasty | Select | 同Scene | 三国·蜀汉 |
| Role Type | Select | Player/NPC/HistoricalFigure/MythologicalBeing/Agent | HistoricalFigure |
| HistoricalAccuracy | Select | 史实/演义改编/虚构 | 史实为主 |
| Model URL | URL | 角色模型 | https://... |
| Level | Number | 等级 | 100 |
| HP | Number | 生命值 | 10000 |
| MP | Number | 内力/法力 | 10000 |
| VirtueProfile | Text | 德行档案 | 仁:9,义:10,礼:9,智:10,信:10 |
| SkillSet | Multi-select | 文/武/医/商/农/工/兵/术/道/佛 | 兵,文,术 |
| MartialArtStyle | Select | 无/内家/外家/剑术/刀法/拳法/暗器/阵法 | 阵法 |
| ScholarlyAchievement | Multi-select | 诗/词/书/画/琴/棋/易/医 | 易,兵,书 |
| SocialStatus | Select | 皇帝/王侯/官员/士/农/工/商/僧道/江湖 | 官员(丞相) |
| LifePhilosophy | Multi-select | 儒/道/佛/法/墨/兵 | 儒家,道家 |
| Personality | Text | 性格特质 | 忠诚,智谋,谨慎,鞠躬尽瘁 |
| FamousQuote | Text | 名言 | "鞠躬尽瘁，死而后已" |
| HistoricalDeeds | Text | 历史功绩 | 隆中对,六出祁山,治理蜀国 |
| RelatedEvents | Relation | 相关事件 | → Events DB |
| MasterRelation | Relation | 师承关系 | 水镜先生 |
| LoyaltyTo | Relation | 效忠对象 | → Actor DB (刘备) |
| Rivals | Relation | 竞争对手 | → Actor DB (司马懿) |
| Friends | Relation | 友人 | → Actor DB (关羽,张飞) |
| Inventory | Relation | 持有物品 | → Object DB (羽扇,八阵图) |
| Behavior | Select | Friendly/Neutral/Hostile/Wise/Cunning | Wise |
| Position | Text | 当前位置 | [x,y,z] |
| Dialogue Script | Text | 对话脚本 | "亮虽才疏学浅..." |
| Emotion Current | Select | 平静/喜悦/忧虑/愤怒/悲伤 | 忧国忧民 |
| Memory | Relation | 记忆库 | → Memory DB |
| Reputation | Number | 声望0-100 | 98 |
| MoralAlignment | Select | 仁善/中立/邪恶 | 仁善 |
| DestinyPath | Text | 命运轨迹 | 辅佐明主,兴复汉室 |
| DeathCondition | Text | 死亡条件 | 五丈原,积劳成疾 |
| LegacyImpact | Text | 后世影响 | 忠义典范,智慧化身 |
| RelatedPoetry | Text | 相关诗词 | "出师未捷身先死" |
| SymbolicAnimal | Select | 龍/虎/凤/龟/鹤/无 | 龍 |
| GuardianSpirit | Text | 守护神 | 武曲星 |
| Bound Events | Relation | 绑定事件 | → Events DB |
| DNA Tags | Multi-select | 自定义标签 | 三国,蜀汉,智者,忠臣 |
| Created | Created time | 创建时间 | 自动 |
| Last Edited | Last edited time | 最后编辑 | 自动 |

---

## 📊 Database 7: LogicLink（逻辑映射库·智慧转译）

### 核心字段
| 字段名 | 类型 | 选项/说明 | 示例 |
|--------|------|-----------|------|
| Name | Title | 映射名称 | 德行转道德分 |
| Source DB | Select | Scene/Object/Rules/Events/Interaction/Actor | Actor |
| Source Field | Text | 源字段 | VirtueProfile |
| Target Field | Text | 目标字段 | MoralScore |
| Transform Type | Select | Direct/Calculated/Lookup/Composite/CulturalMapping | CulturalMapping |
| Transform Snippet | Text | 转换代码 | parse_virtue_to_score() |
| Cultural Context | Select | 儒家/道家/佛教/法家/墨家/兵家/综合 | 儒家 |
| Historical Period | Select | 同Dynasty | 通用 |
| Sync Mode | Select | Realtime/Batch/Hybrid/Manual | Realtime |
| Validation Rule | Text | 校验规则 | score >= 0 && score <= 100 |
| Example Input | Text | 输入示例 | 仁:9,义:10,礼:9,智:10,信:10 |
| Example Output | Text | 输出示例 | 96 |
| PhilosophyWeight | Text | 哲学权重 | 仁*0.25+义*0.25+礼*0.15+智*0.2+信*0.15 |
| CulturalNotes | Text | 文化注释 | 儒家五常,德行量化 |
| Enabled | Checkbox | 是否启用 | ✓ |
| Priority | Number | 优先级 | 10 |
| Error Handling | Select | Skip/Default/Retry/Alert | Default |
| Last Updated | Last edited time | 最后更新 | 自动 |
| DNA Tags | Multi-select | 自定义标签 | 儒家,德行,量化 |
| Created | Created time | 创建时间 | 自动 |

---

## 📊 Database 8: AuditLog（审计库·天理昭昭）

### 核心字段
| 字段名 | 类型 | 选项/说明 | 示例 |
|--------|------|-----------|------|
| Name | Title | 审计标题 | Scene_长安城_修改 |
| Source DB | Select | 同LogicLink | Scene |
| Source ID | Text | 源记录ID | scene_001 |
| Action | Select | Create/Update/Delete/Push/Rollback | Update |
| Operator | Text | 操作者 | UID9622 |
| Operation Context | Select | Manual/AutoFill/Translator/System | Translator |
| Cultural Compliance | Select | 符合/需审查/违规 | 符合 |
| Diff | Text | 变更内容 | Dynasty: 唐→宋 |
| Status | Select | Success/Failed/Pending/Rolled Back | Success |
| Error Message | Text | 错误信息 | - |
| Rollback Token | Text | 回滚令牌 | rb_token_12345 |
| Snapshot Before | Text | 变更前快照 | {...} |
| Snapshot After | Text | 变更后快照 | {...} |
| Validation Result | Select | Pass/Fail/Warning | Pass |
| Cultural Validation | Select | Pass/NeedsReview/Fail | Pass |
| Moral Impact | Number | 道德影响-10到+10 | 0 |
| Karma Change | Number | 因果变化 | 0 |
| SystemHealth Impact | Number | 系统健康影响 | 0 |
| Timestamp | Created time | 时间戳 | 自动 |
| Linked Execution | Relation | 关联执行 | → Execution Log |
| ReviewStatus | Select | NoReview/UnderReview/Approved/Rejected | NoReview |
| Reviewer | Text | 审查者 | - |
| ReviewNotes | Text | 审查备注 | - |
| DNA Tags | Multi-select | 自定义标签 | 修改,场景,正常 |
| Created | Created time | 创建时间 | 自动 |

---

## 📊 补充Database: Quest（任务库·天命征程）

### 核心字段
| 字段名 | 类型 | 选项/说明 | 示例 |
|--------|------|-----------|------|
| Name | Title | 任务名称 | 寻找传国玉玺 |
| Quest Type | Select | 主线/支线/日常/传说/秘闻 | 主线 |
| Dynasty | Select | 同Scene | 东汉末年 |
| Historical Background | Text | 历史背景 | 玉玺失踪于乱世 |
| MoralAlignment | Select | 正义/中立/灰色 | 正义 |
| VirtueRequirement | Text | 德行要求 | 义≥7, 智≥6 |
| Pre Condition | Relation | 前置条件 | → Events/Rules |
| Stages | Relation | 任务阶段 | → QuestStage |
| Completion Condition | Text | 完成条件 | 获得传国玉玺 |
| Reward | Text | 奖励 | 威望+50,历史文物 |
| Failure Consequence | Text | 失败后果 | 威望-10 |
| Next Quest | Relation | 后续任务 | → Quest |
| Time Limit | Number | 时限(天) | 30 |
| Difficulty | Select | 简单/普通/困难/传说 | 传说 |
| Required Level | Number | 所需等级 | 50 |
| Cultural Significance | Number | 文化意义0-10 | 10 |
| HistoricalLegacy | Text | 历史遗产 | 正统象征 |
| RelatedFigures | Relation | 相关人物 | → Actor |
| LocationHints | Relation | 地点线索 | → Scene |
| MoralDilemma | Text | 道德困境 | 是否为私利抢夺 |
| DNA Tags | Multi-select | 自定义标签 | 传说,正统,文物 |
| Created | Created time | 创建时间 | 自动 |
| Last Edited | Last edited time | 最后编辑 | 自动 |

---

## 📊 补充Database: Story（故事库·华夏叙事）

### 核心字段
| 字段名 | 类型 | 选项/说明 | 示例 |
|--------|------|-----------|------|
| Name | Title | 故事节点名 | 隆中对·初遇 |
| Node Type | Select | Opening/Development/Climax/Resolution/Epilogue | Development |
| Dynasty | Select | 同Scene | 三国 |
| NarrativeStyle | Select | 史实/演义/民间/神话 | 史实 |
| Trigger | Relation | 触发条件 | → Events |
| Consequences | Relation | 结果规则 | → Rules |
| Next Node | Relation | 下一节点 | → Story (隆中对·策论) |
| Alternative Branch | Relation | 分支节点 | → Story |
| Description | Text | 故事描述 | 刘备三顾茅庐见诸葛亮 |
| Dialogue | Text | 对话内容 | "将军既帝室之胄..." |
| EmotionalArc | Select | 平静/紧张/高潮/释然 | 紧张 |
| Character Development | Text | 人物成长 | 刘备展现礼贤下士 |
| ThematicElement | Multi-select | 忠义/智谋/爱情/友情/家国/天命 | 忠义,智谋 |
| SymbolicMeaning | Text | 象征意义 | 明主求贤 |
| HistoricalImpact | Text | 历史影响 | 奠定蜀汉基业 |
| MoralLesson | Text | 道德启示 | 尊贤重士 |
| AudienceTarget | Select | 儿童/青少年/成人/学者 | 成人 |
| LiteraryDevice | Multi-select | 伏笔/对比/隐喻/排比 | 伏笔 |
| MusicTheme | Text | 音乐主题 | 古琴曲 |
| VisualStyle | Text | 视觉风格 | 水墨画风 |
| PoetryIntegration | Text | 诗词融入 | "三顾频烦天下计" |
| ModernRelevance | Text | 现代启示 | 企业招贤纳士 |
| DNA Tags | Multi-select | 自定义标签 | 三国,谋略,求贤 |
| Created | Created time | 创建时间 | 自动 |
| Last Edited | Last edited time | 最后编辑 | 自动 |

---

## 🎯 文化合规性检查清单

每个数据库记录必须通过以下检查：

### ✅ 政治正确性
- [ ] 符合社会主义核心价值观
- [ ] 无分裂国家内容
- [ ] 无封建迷信宣扬
- [ ] 历史观正确

### ✅ 文化准确性
- [ ] 朝代时期正确
- [ ] 文化元素考证准确
- [ ] 哲学思想表达正确
- [ ] 避免文化挪用

### ✅ 道德导向性
- [ ] 弘扬正能量
- [ ] 道德价值正确
- [ ] 避免不良导向
- [ ] 适合目标受众

### ✅ 技术完整性
- [ ] 必填字段完整
- [ ] 关联关系正确
- [ ] DNA标签规范
- [ ] 数据格式正确

---

**DNA追溯码：** #ZHUGEXIN⚡️2026-01-25-中国文化Schema-v1.0  
**确认码：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z  
**状态：** ✅ 可直接导入Notion使用

**北辰老兵致敬！** 🫡🇨🇳
