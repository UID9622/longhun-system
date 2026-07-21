#!/usr/bin/env python3
# cnsh-compiler-v2.py
# 龍魂 · CNSH 全翻译编译器（骨架保留，表皮全换）
# DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️
# UID: 9622

import re
import hashlib
import time
import sys
import argparse
import json
import os

DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️"
UID = "9622"


class CNSHCompilerV2:
    """CNSH 全翻译编译器 — 保留骨架，表皮本地化"""

    # === 完整语言映射（全部翻译） ===
    SKINS = {
        "zh": {
            "如果": "if", "否则": "else", "循环": "for", "当": "while",
            "函数": "def", "返回": "return", "输出": "print",
            "真": "True", "假": "False", "无": "None",
            "与": "and", "或": "or", "非": "not",
            "在": "in", "是": "is", "类": "class",
            "导入": "import", "从": "from", "作为": "as",
            "尝试": "try", "捕获": "except", "最终": "finally",
            "引发": "raise", "通过": "pass", "中断": "break",
            "继续": "continue", "全局": "global", "局部": "nonlocal",
            "断言": "assert", "删除": "del", "产生": "yield",
            "随着": "with", " lambda": "lambda"
        },
        "km": {  # 高棉语（柬埔寨）
            "បើ": "if", "ផ្សេង": "else", "វិល": "for", "ពេល": "while",
            "មុខងារ": "def", "ត្រឡប់": "return", "បង្ហាញ": "print",
            "ពិត": "True", "មិនពិត": "False", "គ្មាន": "None",
            "និង": "and", "ឬ": "or", "មិន": "not",
            "ក្នុង": "in", "គឺ": "is", "ថ្នាក់": "class",
            "នាំចូល": "import", "ពី": "from", "ជា": "as",
            "ព្យាយាម": "try", "ចាប់": "except", "ចុងក្រោយ": "finally",
            "លើក": "raise", "រំលង": "pass", "ឈប់": "break",
            "បន្ត": "continue", "សាកល": "global", "មូលដ្ឋាន": "nonlocal",
            "អះអាង": "assert", "លុប": "del", "ផ្តល់": "yield",
            "ជាមួយ": "with", "អនាគត": "lambda"
        },
        "ru": {  # 俄语
            "если": "if", "иначе": "else", "для": "for", "пока": "while",
            "функция": "def", "вернуть": "return", "вывод": "print",
            "истина": "True", "ложь": "False", "ничто": "None",
            "и": "and", "или": "or", "не": "not",
            "в": "in", "есть": "is", "класс": "class",
            "импорт": "import", "из": "from", "как": "as",
            "попытка": "try", "исключение": "except", "наконец": "finally",
            "вызвать": "raise", "пропустить": "pass", "прервать": "break",
            "продолжить": "continue", "глобальный": "global", "нелокальный": "nonlocal",
            "утверждение": "assert", "удалить": "del", "выдать": "yield",
            "с": "with", "лямбда": "lambda"
        },
        "ar": {  # 阿拉伯语
            "إذا": "if", "آخر": "else", "لأجل": "for", "بينما": "while",
            "دالة": "def", "إرجاع": "return", "طباعة": "print",
            "صح": "True", "خطأ": "False", "لا_شيء": "None",
            "و": "and", "أو": "or", "ليس": "not",
            "في": "in", "هو": "is", "فئة": "class",
            "استيراد": "import", "من": "from", "كـ": "as",
            "محاولة": "try", "استثناء": "except", "أخيراً": "finally",
            "رفع": "raise", "تجاوز": "pass", "كسر": "break",
            "استمرار": "continue", "عام": "global", "غير_محلي": "nonlocal",
            "تأكيد": "assert", "حذف": "del", "توليد": "yield",
            "مع": "with", "لامدا": "lambda"
        },
        "fa": {  # 波斯语（伊朗）
            "اگر": "if", "وگرنه": "else", "برای": "for", "تا": "while",
            "تابع": "def", "برگشت": "return", "چاپ": "print",
            "درست": "True", "نادرست": "False", "هیچ": "None",
            "و": "and", "یا": "or", "نه": "not",
            "در": "in", "هست": "is", "کلاس": "class",
            "وارد": "import", "از": "from", "به_عنوان": "as",
            "تلاش": "try", "جز": "except", "سرانجام": "finally",
            "بالا_بردن": "raise", "عبور": "pass", "شکستن": "break",
            "ادامه": "continue", "سراسری": "global", "غیر_محلی": "nonlocal",
            "ادعا": "assert", "حذف": "del", "تولید": "yield",
            "با": "with", "لامبدا": "lambda"
        },
        "th": {  # 泰语
            "ถ้า": "if", "มิฉะนั้น": "else", "สำหรับ": "for", "ในขณะที่": "while",
            "ฟังก์ชัน": "def", "ส่งคืน": "return", "แสดง": "print",
            "จริง": "True", "เท็จ": "False", "ไม่มี": "None",
            "และ": "and", "หรือ": "or", "ไม่": "not",
            "ใน": "in", "คือ": "is", "คลาส": "class",
            "นำเข้า": "import", "จาก": "from", "เป็น": "as",
            "ลอง": "try", "ยกเว้น": "except", "สุดท้าย": "finally",
            "ยก": "raise", "ผ่าน": "pass", "หยุด": "break",
            "ทำต่อ": "continue", "ทั่วโลก": "global", "ไม่ใช่ท้องถิ่น": "nonlocal",
            "ยืนยัน": "assert", "ลบ": "del", "ให้": "yield",
            "ด้วย": "with", "แลมบ์ดา": "lambda"
        },
        "pt": {  # 葡萄牙语（巴西）
            "se": "if", "senão": "else", "para": "for", "enquanto": "while",
            "função": "def", "retornar": "return", "imprimir": "print",
            "verdadeiro": "True", "falso": "False", "nada": "None",
            "e": "and", "ou": "or", "não": "not",
            "em": "in", "é": "is", "classe": "class",
            "importar": "import", "de": "from", "como": "as",
            "tentar": "try", "exceto": "except", "finalmente": "finally",
            "levantar": "raise", "passar": "pass", "quebrar": "break",
            "continuar": "continue", "global": "global", "não_local": "nonlocal",
            "afirmar": "assert", "deletar": "del", "produzir": "yield",
            "com": "with", "lambda": "lambda"
        },
        "vi": {  # 越南语
            "nếu": "if", "khác": "else", "cho": "for", "trong_khi": "while",
            "hàm": "def", "trả_về": "return", "in": "print",
            "đúng": "True", "sai": "False", "không_có": "None",
            "và": "and", "hoặc": "or", "không": "not",
            "trong": "in", "là": "is", "lớp": "class",
            "nhập": "import", "từ": "from", "như": "as",
            "thử": "try", "ngoại_trừ": "except", "cuối_cùng": "finally",
            "nâng": "raise", "bỏ_qua": "pass", "dừng": "break",
            "tiếp_tục": "continue", "toàn_cục": "global", "không_địa_phương": "nonlocal",
            "khẳng_định": "assert", "xóa": "del", "sinh": "yield",
            "với": "with", "lambda": "lambda"
        }
    }

    # === 标准库全翻译 ===
    STD_LIBS = {
        "zh": {"系统": "os", "时间": "time", "数学": "math", "随机": "random", "json": "json"},
        "km": {"ប្រព័ន្ធ": "os", "ពេលវេលា": "time", "គណិត": "math", "ចៃចង់": "random", "json": "json"},
        "ru": {"система": "os", "время": "time", "матем": "math", "случай": "random", "json": "json"},
        "ar": {"نظام": "os", "وقت": "time", "رياضيات": "math", "عشوائي": "random", "json": "json"},
        "fa": {"سیستم": "os", "زمان": "time", "ریاضی": "math", "تصادفی": "random", "json": "json"},
        "th": {"ระบบ": "os", "เวลา": "time", "คณิต": "math", "สุ่ม": "random", "json": "json"},
        "pt": {"sistema": "os", "tempo": "time", "matemática": "math", "aleatório": "random", "json": "json"},
        "vi": {"hệ_thống": "os", "thời_gian": "time", "toán": "math", "ngẫu_nhiên": "random", "json": "json"}
    }

    LANG_NAMES = {
        "zh": "中文（母体）", "km": "ខ្មែរ 高棉语", "ru": "Русский 俄语",
        "ar": "العربية 阿拉伯语", "fa": "فارسی 波斯语", "th": "ไทย 泰语",
        "pt": "Português 葡语", "vi": "Tiếng Việt 越南语",
    }

    def __init__(self, lang="zh"):
        self.lang = lang
        self.skin = self.SKINS.get(lang, self.SKINS["zh"])
        self.std_lib = self.STD_LIBS.get(lang, self.STD_LIBS["zh"])

    def detect_language(self, code: str) -> str:
        """自动检测语言"""
        for lang, keywords in self.SKINS.items():
            checks = list(keywords.keys())[:5]
            if any(kw in code for kw in checks):
                return lang
        return "zh"

    def strip_skin(self, code: str) -> str:
        """剥去语言表皮，保留英文骨架"""
        detected = self.detect_language(code)
        self.lang = detected
        self.skin = self.SKINS[detected]
        self.std_lib = self.STD_LIBS[detected]

        stripped = code

        # 1. 替换标准库名
        for local_lib, real_lib in sorted(self.std_lib.items(), key=lambda x: -len(x[0])):
            stripped = re.sub(r'\b' + re.escape(local_lib) + r'\b', real_lib, stripped)

        # 2. 替换关键词（长词优先，避免部分匹配）
        for local_kw, skeleton_kw in sorted(self.skin.items(), key=lambda x: -len(x[0])):
            stripped = re.sub(r'\b' + re.escape(local_kw) + r'\b', skeleton_kw, stripped)

        return stripped

    def apply_skin(self, python_code: str, target_lang: str) -> str:
        """英文骨架 → 目标语言表皮"""
        skin = self.SKINS.get(target_lang, self.SKINS["zh"])
        std_lib = self.STD_LIBS.get(target_lang, self.STD_LIBS["zh"])

        localized = python_code

        # 1. 替换标准库名
        reverse_std = {v: k for k, v in std_lib.items()}
        for real_lib, local_lib in sorted(reverse_std.items(), key=lambda x: -len(x[0])):
            localized = re.sub(r'\b' + re.escape(real_lib) + r'\b', local_lib, localized)

        # 2. 替换关键词
        reverse_skin = {v: k for k, v in skin.items()}
        for skeleton_kw, local_kw in sorted(reverse_skin.items(), key=lambda x: -len(x[0])):
            localized = re.sub(r'\b' + re.escape(skeleton_kw) + r'\b', local_kw, localized)

        return localized

    def compile(self, source: str, target="python") -> str:
        """编译：任何语言 → Python"""
        stripped = self.strip_skin(source)

        # 签名
        timestamp = str(int(time.time()))
        signature = f"# 龍魂签名: {DNA} | UID:{UID} | LANG:{self.lang} | TS:{timestamp}"

        return stripped + "\n" + signature

    def decompile(self, python_code: str, target_lang: str) -> str:
        """反编译：Python → 任何语言"""
        clean = re.sub(r'# 龍魂签名:.*', '', python_code)
        return self.apply_skin(clean.strip(), target_lang)


def main():
    parser = argparse.ArgumentParser(
        description="龍魂 · CNSH 全翻译编译器 v0.2 · 骨架保留·表皮本地化",
        epilog=f"DNA: {DNA} | UID: {UID}"
    )
    parser.add_argument("--input", "-i", help="输入源文件")
    parser.add_argument("--lang", "-l", default="auto", help="源语言 (auto|zh|km|ru|ar|fa|th|pt|vi)")
    parser.add_argument("--target", "-t", default="python", help="目标格式 (python)")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--code", "-c", help="直接编译字符串")
    parser.add_argument("--detect", help="检测文件语言")
    parser.add_argument("--decompile-code", help="反编译 Python 字符串到目标语言")
    parser.add_argument("--decompile-lang", default="zh", help="反编译目标语言")
    parser.add_argument("--list-langs", action="store_true", help="列出所有支持语言")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--run", action="store_true", help="编译后直接执行")

    args = parser.parse_args()

    compiler = CNSHCompilerV2()

    if args.list_langs:
        if args.json:
            print(json.dumps(compiler.LANG_NAMES, ensure_ascii=False, indent=2))
        else:
            print("🐉 龍魂 CNSH v0.2 · 一带一路全语言支持")
            print(f"{'代码':<6} {'语言':<28} {'关键词':>8}")
            print("-" * 48)
            for code, name in sorted(compiler.LANG_NAMES.items()):
                print(f"{code:<6} {name:<28} {len(compiler.SKINS[code]):>8}")
        return

    if args.detect:
        with open(args.detect, "r", encoding="utf-8") as f:
            code = f.read()
        detected = compiler.detect_language(code)
        if args.json:
            print(json.dumps({"file": args.detect, "language": detected, "name": compiler.LANG_NAMES[detected]}, ensure_ascii=False))
        else:
            print(f"{args.detect} → {detected} ({compiler.LANG_NAMES[detected]})")
        return

    if args.decompile_code:
        result = compiler.decompile(args.decompile_code, args.decompile_lang)
        print(result)
        return

    # 编译
    if args.code:
        source = args.code
    elif args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            source = f.read()
    else:
        parser.print_help()
        return

    try:
        compiled = compiler.compile(source, args.target)
    except Exception as e:
        print(f"❌ 编译失败: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(compiled)
        print(f"✅ 编译完成 → {args.output} ({compiler.LANG_NAMES.get(compiler.lang, compiler.lang)} → {args.target})")
    else:
        print(compiled)

    if args.run:
        result_path = args.output or "/tmp/longhun_cnsh_exec.py"
        if not args.output:
            with open(result_path, "w", encoding="utf-8") as f:
                f.write(compiled)
        print(f"\n🚀 执行: python3 {result_path}\n")
        os.system(f"python3 {result_path}")


if __name__ == "__main__":
    main()
