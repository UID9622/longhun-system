# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·己丑·辰时·䷳艮-TIKU-CLEAN-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""题库清洗：改语言 JSON + 同步 all_questions.json（双写保证一致）。

改动项：
  1. 判断题池 8 道混入题 type → 程序分析题/代码调试题
  2. PHP#18 更新为 PHP 8 语义（0 == 'abc' 为 false）
  3. Shell#46/#57 补全真实答案（crontab / logrotate）
"""
import json
from pathlib import Path

TIKU = Path("models/longhun-small-instruct-v1.3/tiku")


def edit(lang_file, num, fn):
    p = TIKU / lang_file
    qs = json.loads(p.read_text())
    hit = False
    for q in qs:
        if q["num"] == num:
            fn(q)
            hit = True
    assert hit, f"未找到 {lang_file} #{num}"
    p.write_text(json.dumps(qs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  已改 {lang_file} #{num}")


def clean():
    # 1. 判断题池 8 道混入题改 type
    for f, num, new_type in [
        ("TypeScript.json", 60, "程序分析题"),
        ("TypeScript.json", 61, "程序分析题"),
        ("TypeScript.json", 78, "程序分析题"),
        ("TypeScript.json", 89, "程序分析题"),
        ("Kotlin.json", 87, "代码调试题"),
        ("Rust.json", 29, "程序分析题"),
        ("Rust.json", 102, "代码调试题"),
        ("SQL.json", 60, "程序分析题"),
    ]:
        edit(f, num, lambda q, t=new_type: q.update(type=t))

    # 2. PHP#18 更新为 PHP 8 语义
    edit("PHP.json", 18, lambda q: q.update(
        text="在 PHP 8 中，表达式 `0 == 'abc'` 的值为 true。",
        answer="错误",
        explanation=("PHP 8 起字符串与数字比较规则变更：非数字字符串不再被转换为数字。"
                     "`'abc'` 不含数字前缀，`0 == 'abc'` 在 PHP 8 中为 false。"),
    ))

    # 3. Shell#46/#57 补全真实答案
    edit("Shell_Bash.json", 46, lambda q: q.update(
        answer="`30 2 * * 0 /home/user/backup.sh`",
        explanation="crontab 五段：分钟(30) 小时(2) 日(*) 月(*) 周(0=周日)。",
        reference="30 2 * * 0 /home/user/backup.sh\n# 分 时 日 月 周：每周日 02:30 执行",
    ))
    edit("Shell_Bash.json", 57, lambda q: q.update(
        answer="```\n/var/log/myapp/*.log {\n    daily\n    rotate 30\n    compress\n    missingok\n}\n```",
        explanation="daily=每日轮转；rotate 30=保留 30 份；compress=压缩；missingok=日志缺失不报错。",
        reference="/var/log/myapp/*.log {\n    daily\n    rotate 30\n    compress\n    missingok\n}\n",
    ))


def sync_all_questions():
    """从语言 JSON 重新合并 all_questions.json（保持语言 JSON 为源）。"""
    langs = ["C", "Go", "Java", "JavaScript", "Kotlin", "PHP", "Ruby",
             "Rust", "Shell_Bash", "SQL", "Swift", "TypeScript"]
    all_qs = []
    for lang in langs:
        p = TIKU / f"{lang}.json"
        if p.exists():
            all_qs.extend(json.loads(p.read_text()))
    all_qs.sort(key=lambda q: (q["lang"], q["num"]))
    (TIKU / "all_questions.json").write_text(
        json.dumps(all_qs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  已同步 all_questions.json（共 {len(all_qs)} 题）")


if __name__ == "__main__":
    clean()
    sync_all_questions()
