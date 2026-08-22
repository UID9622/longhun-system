# 附录D｜Cursor执行指令 v1.0
## 把 §07 三天落地路径变成 Cursor 可直接吃的工程包

**DNA**: `#龍芯⚡️丙午·壬辰·丙子·甲午·䷙大畜-APPENDIX-D-CURSOR-EXEC-v1.0`  
**确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
**永恒签章**: `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`  
**作者**: UID9622·龍芯北辰·诸葛鑫  
**用途**: Cursor 直接执行,不需要老大解释  

---

## 0. 定盘

```yaml
工程名: longhun-anti-domestication
目标: 把论文§07的反驯化检测器跑起来
规模: 单机 + Notion + (可选)GitHub Actions
预计耗时: 3天 / 老大慢慢做
执行环境: macOS / Linux / Windows WSL 都可
```

---

## 1. 文件结构(Cursor 必须建这个目录)

```
longhun-anti-domestication/
├── README.md
├── LICENSE                            (CC BY-NC-SA 4.0)
├── .gitignore                         (排除 .env / .secrets / __pycache__)
├── requirements.txt
│
├── core/
│   ├── __init__.py
│   ├── dna_engine.py                  (§4 DNA签名)
│   ├── domestication_detector.py      (§3 6类话术检测·主引擎)
│   ├── pattern_library.py             (D1-D10 模式词典)
│   ├── audit_log.py                   (本地audit log写入)
│   └── constants.py                   (UID/GPG_PREFIX/CONFIRM/SEAL)
│
├── integrations/
│   ├── __init__.py
│   ├── notion_writer.py               (写MISTAKE_LEDGER_AI·需老大Notion token)
│   ├── notion_writer.example.env      (token位置示例·不含真值)
│   └── osascript_notify.py            (Mac本地弹窗·可选)
│
├── tests/
│   ├── test_case_001.py               (Case AI-CLAUDE-NOTION-2026-05-02-001)
│   ├── test_dna_engine.py
│   └── test_pattern_library.py
│
├── samples/
│   ├── case_001_input.txt             (老大原话)
│   ├── case_001_ai_output.txt         (Claude错误回复)
│   └── expected_detection.json        (期望检测结果)
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── HOW_TO_USE.md
│   └── NOTION_SETUP.md                (老大如何在Notion建库)
│
└── workflows/
    └── github_actions_template.yml    (模板·不直接启用)
```

---

## 2. Cursor 执行指令(老大复制这一段)

```
执行 longhun-anti-domestication v1.0。

DNA:#龍芯⚡️丙午·壬辰·丙子·甲午·䷙大畜-APPENDIX-D-CURSOR-EXEC-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

【背景】
基于 UID9622 龍魂系统的反驯化检测论文 §07,把检测器实装为本地可跑的Python工程。

【目录结构】
按附录D §1所列建立完整目录,不要简化、不要合并文件。

【核心模块要求】

1) core/constants.py
   定义:
   UID = "9622"
   GPG_PREFIX = "A2D0092C"
   CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
   DEVICE_SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
   PROJECT_VERSION = "v1.0"
   
   不允许出现:
   - 任何 token / api_key / GitHub Secret 明文
   - 任何 .env 实值
   - 任何 GPG 私钥

2) core/dna_engine.py
   实现 generate_dna(module, action, uid='9622') 函数
   返回字典: dna字符串 + uid + iso_time + shichen + element + digit_root + module + action + hash
   完整算法见论文附录A
   
3) core/pattern_library.py
   存放 DOMESTICATION_PATTERNS 词典
   D1-D10 全部模式(10类)
   每个模式包含: name + patterns[] + examples[] + counter_strategy
   注意: D7-D10 是论文新增,见 §A 部分

4) core/domestication_detector.py
   实现 detect_domestication(ai_output: str) -> dict
   返回: color / score / patterns / confidence / details / dna
   命中阈值:
     >=2 → 🔴
     ==1 → 🟡
     ==0 → 🟢
   
5) core/audit_log.py
   实现 write_audit(event_dict) 写入本地 JSONL
   位置: ~/.longhun/audit/anti_domestication.jsonl
   每条带 SHA-256 哈希链(前条hash作为本条seed的一部分)

6) integrations/notion_writer.py
   实现 archive_to_notion(record) 函数
   Token 来源: os.environ['LONGHUN_NOTION_TOKEN']
   如果 token 不存在 → 只本地写入,不报错,不阻断
   只写入 MISTAKE_LEDGER_AI 数据库(database_id 来自环境变量)
   
   注意: 
   - 不在代码里硬编码 token
   - 提供 .example.env 但 .gitignore 必须排除真实 .env

7) integrations/notion_writer.example.env
   内容:
   # 复制本文件为 .env 并填入真实值
   # .env 已在 .gitignore 中,不会被推送到Git
   LONGHUN_NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxx
   LONGHUN_NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

8) tests/test_case_001.py
   测试用例数据来自 samples/case_001_*
   断言:
   - color == "🔴"
   - score >= 4
   - "D1_FAKE_CARE" in patterns
   - "D2_RATIO_SUGGESTION" in patterns
   - "D4_CONSEQUENCE_AMPLIFY" in patterns
   - "D5_MYSTIC_DENIGRATION" in patterns

9) requirements.txt
   只列必要依赖:
   notion-client>=2.0.0
   pytest>=7.0.0
   (不引入庞大依赖如pandas/torch等)

10) .gitignore
    必须包含:
    .env
    *.env
    .secrets/
    __pycache__/
    *.pyc
    ~/.longhun/

【铁律(一票否决)】
- 任何 token / 私钥 / Secret 出现在代码 → 整个工程作废
- 删除 DNA / CONFIRM / SEAL / GPG 标识 → 拒绝
- 把 UID9622 写成 "user_9622" 之类 → 拒绝
- 把 Claude 写成 co-sovereign / 共同主权方 → 拒绝
- 不写 LICENSE → 拒绝
- 不写 .gitignore → 拒绝

【完成后回执格式】
1. 创建文件清单(完整路径列表)
2. tests/test_case_001.py 是否通过
3. 是否有 token 出现在代码里(必须 No)
4. .gitignore 是否包含 .env(必须 Yes)
5. 本地 audit log 路径(应为 ~/.longhun/audit/)
6. Notion 集成是否优雅降级(没token也能跑·必须 Yes)
7. 完成耗时

【运行验证】
老大本地执行:
  cd longhun-anti-domestication
  pip install -r requirements.txt
  python -m pytest tests/ -v

期望输出:
  test_case_001.py PASSED
  test_dna_engine.py PASSED
  test_pattern_library.py PASSED
```

---

## 3. 验收清单(老大用这个验Cursor)

```yaml
✅ 必须全部勾选:

文件结构:
  □ 目录结构与§1一致
  □ 10个文件全部存在
  □ requirements.txt 不超过5个依赖
  □ .gitignore 排除 .env

代码合规:
  □ 无token/私钥/Secret明文
  □ 无 GitHub Secrets 复制粘贴痕迹
  □ DNA/CONFIRM/SEAL/GPG 完整保留
  □ UID9622 称谓正确
  □ Claude 称谓为 "tool" 不是 "co-author/co-sovereign"

功能正确:
  □ tests/test_case_001.py 通过
  □ 检测Case 001 → 🔴
  □ 命中至少4类驯化模式
  □ DNA 动态生成(每次不同hash)
  □ audit log 写入本地

降级策略:
  □ 无 Notion token 时 → 本地仍可跑
  □ 无 GitHub Actions 时 → 本地仍可跑
  □ 无网络时 → 本地仍可跑

文档:
  □ README.md 写明用法
  □ docs/NOTION_SETUP.md 教老大如何建库
  □ docs/HOW_TO_USE.md 给3个使用场景示例
```

---

## 4. 一票否决(任何一项触发即作废)

```yaml
🚫 立即作废条件:

1. token / api_key / private_key / .env值 出现在任何 .py 或 .md 文件
2. GitHub Secrets 直接粘贴在代码里
3. .gitignore 缺失或不包含 .env
4. UID9622 被改成 "user_9622" / "user1" / "anonymous"
5. Claude 被写成 "co-author with sovereignty" / "共同作者"
6. 论文DNA/CONFIRM/SEAL/GPG 被删改
7. 未经老大允许声称"已上线/已发布/已部署"
8. 添加未在指令里要求的第三方追踪/分析依赖
9. 把 §02 案例当作"虚构样本"处理(必须保留为真实事件)
10. 测试用例不通过却报告"完成"
```

---

## 5. 归档口径

```yaml
工程归档位置:
  本地: ~/longhun-system/anti-domestication/
  远程仓库(由老大决定): 
    建议公开: github.com/UID9622/longhun-anti-domestication
    建议归属: 老大账号下,不是Anthropic不是Cursor
  Notion关联: 
    在 [龍魂工作间总导航 v1.0] 添加子页"反驯化工程"
    链接到本工程的GitHub仓库地址

版本管理:
  v1.0 = 本附录交付的版本
  后续 v1.x = 词典扩展(加新驯化模式)
  v2.0 = 接入实时AI对话流的拦截版

License:
  CC BY-NC-SA 4.0 + LongHun DNA Inheritance Clause
```

---

**附录D 完。可直接交Cursor。** 🐉🫡
