#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-05-CNSH-CGEN-v0.1-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 依赖: 纯标准库 · 零三方
# 用途: CNSH→C 翻译器 v0.1（鸿蒙 NDK / N-API 后端种子）。
#   语法权威: tests/cnsh_samples/（CNSH 基线 P0 · PR#95 封板）。
#   支持子集: 功能/返回/如果/否则/循环..在..范围/打印(多参)/
#             真/假/和/或/非/整数|字符串|布尔 类型标注/字符串拼接(+)/
#             字符串相等比较(==/!=) / int 运算 + - * / % **
#   输出: --napi 时生成鸿蒙 napi C 注册包装（无 main）；否则纯 C main（可本机 clang 对拍）。
import sys
import re
import math

KEYWORDS = {"功能", "返回", "如果", "否则", "循环", "在", "真", "假", "空",
            "和", "或", "非", "打印"}
BUILTIN_NOGEN = {"输入"}  # 鸿蒙端无 stdin → 明确拒绝而非静默
TYPE_MAP = {"整数": "int", "字符串": "str", "布尔": "bool"}

def cnsh_str(x):
    return '"%s"' % x.replace("\\", "\\\\").replace('"', '\\"')

class TokenizeError(Exception):
    pass

class ParseError(Exception):
    pass

def tokenize(src):
    toks = []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if c.isspace():
            i += 1
            continue
        if c == "#":  # 注释到行尾
            while i < n and src[i] != "\n":
                i += 1
            continue
        m = re.match(r'"[^"]*"', src[i:])
        if m:
            toks.append(("STR", m.group(0)[1:-1]))
            i += len(m.group(0))
            continue
        if c.isdigit():
            m = re.match(r"\d+", src[i:])
            toks.append(("NUM", int(m.group(0))))
            i += len(m.group(0))
            continue
        if c.isalpha() or "\u4e00" <= c <= "\u9fff" or c == "_":
            m = re.match(r"[\w\u4e00-\u9fff]+", src[i:])
            word = m.group(0)
            i += len(word)
            toks.append(("WORD", word))
            continue
        two = src[i:i + 2]
        if two in ("==", "!=", ">=", "<=", "**"):
            toks.append(("OP", two))
            i += 2
            continue
        if c in "+-*/%><=(){}:,":
            toks.append(("OP", c))
            i += 1
            continue
        raise TokenizeError("无法识别的字符: %r (行内位置 %d)" % (c, i))
    toks.append(("EOF", None))
    return toks

class Parser:
    """递归下降 → AST(list of dict)，树与 cnsh_compiler.py 语义对齐（Python 语义）。"""

    def __init__(self, toks):
        self.t = toks
        self.p = 0
        self.functions = {}   # 名称 -> {"params":[(名,类型)], "ret":类型|None}
        self.calls = []       # 在解析体里出现的调用顺序(名称列表) 用不着，靠后扫
        self.current_func = None

    def peek(self):
        return self.t[self.p]

    def next(self):
        x = self.t[self.p]
        self.p += 1
        return x

    def expect(self, kind, val=None):
        x = self.next()
        if x[0] != kind or (val is not None and x[1] != val):
            raise ParseError("期望 %r%r，实得 %r" % (kind, val, x))
        return x

    def word(self):
        return self.next()[1]

    def match_op(self, op):
        if self.peek()[0] == "OP" and self.peek()[1] == op:
            self.p += 1
            return True
        return False

    # ── 顶层 ──
    def parse_program(self):
        stmts = []
        while self.peek()[0] != "EOF":
            if self.peek()[0] == "WORD" and self.peek()[1] == "功能":
                stmts.append(self.parse_func())
            else:
                stmts.extend(self.parse_stmts_until({"EOF"}))
        return {"type": "program", "body": stmts}

    def parse_func(self):
        self.word()  # 功能
        name = self.word()
        self.expect("OP", "(")
        params = []
        while self.peek()[0] != "OP" or self.peek()[1] != ")":
            pname = self.word()
            ptype = "整数"
            if self.match_op(":"):
                ptype = self.word()
            params.append((pname, TYPE_MAP.get(ptype, "int")))
            if not self.match_op(","):
                break
        self.expect("OP", ")")
        ret = None
        # '->' 返回类型标注
        if self.peek()[0] == "OP" and self.peek()[1] == "-":
            self.next()
            if self.peek()[0] == "OP" and self.peek()[1] == ">":
                self.next()
                ret = TYPE_MAP.get(self.word(), "int")
        self.expect("OP", "{")
        body = self.parse_stmts_until({"}"})
        self.expect("OP", "}")
        self.functions[name] = {"params": params, "ret": ret}
        return {"type": "func", "name": name, "params": params, "ret": ret, "body": body}

    def parse_stmts_until(self, stops):
        out = []
        while True:
            x = self.peek()
            if x[0] == "EOF":
                if "EOF" in stops:
                    break
                raise ParseError("缺少收尾 %r" % stops)
            if x[0] == "OP" and x[1] in stops:
                break
            out.append(self.parse_stmt())
        return out

    def parse_stmt(self):
        x = self.peek()
        if x[0] == "WORD":
            k = x[1]
            if k == "返回":
                self.next()
                e = None
                if not (self.peek()[0] == "OP" and self.peek()[1] == "}"):
                    e = self.parse_expr()
                return {"type": "return", "value": e}
            if k == "如果":
                self.next()
                cond = self.parse_expr()  # 真实语法无括号：如果 n <= 1 {
                self.expect("OP", "{")
                then = self.parse_stmts_until({"}"})
                self.expect("OP", "}")
                els = None
                if self.peek()[0] == "WORD" and self.peek()[1] == "否则":
                    self.next()
                    self.expect("OP", "{")
                    els = self.parse_stmts_until({"}"})
                    self.expect("OP", "}")
                return {"type": "if", "cond": cond, "then": then, "else": els}
            if k == "循环":
                self.next()
                var = self.word()
                self.word()  # 在
                if self.peek()[0] == "WORD" and self.peek()[1] == "范围":
                    self.next()
                    self.expect("OP", "(")
                    end = self.parse_expr()
                    self.expect("OP", ")")
                else:
                    end = self.parse_expr()
                self.expect("OP", "{")
                body = self.parse_stmts_until({"}"})
                self.expect("OP", "}")
                return {"type": "for", "var": var, "end": end, "body": body}
            if k == "打印":
                self.next()
                self.expect("OP", "(")
                args = []
                if not (self.peek()[0] == "OP" and self.peek()[1] == ")"):
                    args.append(self.parse_expr())
                    while self.match_op(","):
                        args.append(self.parse_expr())
                self.expect("OP", ")")
                return {"type": "call", "name": "打印", "args": args}
        # 赋值 or 表达式语句
        e = self.parse_expr()
        if e["type"] == "assign":
            return e
        return {"type": "exprstmt", "expr": e}

    # ── 表达式（precedence climbing） ──
    def parse_expr(self):
        return self.parse_or()

    def parse_or(self):
        left = self.parse_and()
        while self.peek()[0] == "WORD" and self.peek()[1] == "或":
            self.next()
            right = self.parse_and()
            left = {"type": "binop", "op": "或", "left": left, "right": right}
        return left

    def parse_and(self):
        left = self.parse_cmp()
        while self.peek()[0] == "WORD" and self.peek()[1] == "和":
            self.next()
            right = self.parse_cmp()
            left = {"type": "binop", "op": "和", "left": left, "right": right}
        return left

    def parse_cmp(self):
        left = self.parse_add()
        if self.peek()[0] == "OP" and self.peek()[1] in ("==", "!=", ">", "<", ">=", "<="):
            op = self.next()[1]
            right = self.parse_add()
            return {"type": "binop", "op": op, "left": left, "right": right}
        return left

    def parse_add(self):
        left = self.parse_mul()
        while self.peek()[0] == "OP" and self.peek()[1] in ("+", "-"):
            op = self.next()[1]
            right = self.parse_mul()
            left = {"type": "binop", "op": op, "left": left, "right": right}
        return left

    def parse_mul(self):
        left = self.parse_pow()
        while self.peek()[0] == "OP" and self.peek()[1] in ("*", "/", "%"):
            op = self.next()[1]
            right = self.parse_pow()
            left = {"type": "binop", "op": op, "left": left, "right": right}
        return left

    def parse_pow(self):
        left = self.parse_unary()
        if self.match_op("**"):
            right = self.parse_unary()
            return {"type": "binop", "op": "**", "left": left, "right": right}
        return left

    def parse_unary(self):
        x = self.peek()
        if x[0] == "WORD" and x[1] == "非":
            self.next()
            return {"type": "unary", "op": "非", "expr": self.parse_unary()}
        if x[0] == "OP" and x[1] == "-":
            self.next()
            return {"type": "unary", "op": "-", "expr": self.parse_unary()}
        return self.parse_primary()

    def parse_primary(self):
        x = self.peek()
        if x[0] == "NUM":
            self.next()
            return {"type": "num", "value": x[1]}
        if x[0] == "STR":
            self.next()
            return {"type": "str", "value": x[1]}
        if x[0] == "WORD":
            k = x[1]
            if k == "真":
                self.next()
                return {"type": "bool", "value": True}
            if k == "假":
                self.next()
                return {"type": "bool", "value": False}
            if k == "空":
                self.next()
                return {"type": "str", "value": ""}
            self.next()
            if self.peek()[0] == "OP" and self.peek()[1] == "(":  # 函数调用
                self.next()
                args = []
                if not (self.peek()[0] == "OP" and self.peek()[1] == ")"):
                    args.append(self.parse_expr())
                    while self.match_op(","):
                        args.append(self.parse_expr())
                self.expect("OP", ")")
                return {"type": "call", "name": k, "args": args}
            if self.peek()[0] == "OP" and self.peek()[1] == "=":  # 赋值
                self.next()
                val = self.parse_expr()
                return {"type": "assign", "name": k, "value": val}
            return {"type": "var", "name": k}
        if x[0] == "OP" and x[1] == "(":
            self.next()
            e = self.parse_expr()
            self.expect("OP", ")")
            return e
        raise ParseError("意外 token %r" % (x,))


# ────────────────────────────── C 生成 ──────────────────────────────
TYPE_C = {"int": "long long", "str": "const char*", "bool": "int"}

class CGen:
    def __init__(self, prog, napi=False, no_main=False, dna="", gpg=""):
        self.prog = prog
        self.napi = napi
        self.no_main = no_main
        self.dna = dna
        self.gpg = gpg
        self.funcs = prog.get("_functions", {})
        # 收集函数签名
        self.sigs = {}
        for st in prog["body"]:
            if st["type"] == "func":
                ret = st.get("ret") or "void"
                if ret == "str":
                    ret = "const char*"
                params = ", ".join(
                    "%s %s" % (TYPE_C[t], n) for (n, t) in st["params"])
                self.sigs[st["name"]] = (ret, params)
        self.var_types = {}
        self.current_ret = None
        self.retbuf_depth = 0
        self.main_body = []
        self.exported = []

    def infer(self, e):
        t = e["type"]
        if t == "num":
            return "int"
        if t == "str":
            return "str"
        if t == "bool":
            return "bool"
        if t == "var":
            return self.var_types.get(e["name"], "int")
        if t == "assign":
            return self.infer(e["value"])
        if t == "call":
            n = e["name"]
            if n == "范围":
                return "int"
            if n in self.funcs:
                r = self.funcs[n].get("ret")
                return r if r else "int"
            return "int"
        if t == "binop":
            op = e["op"]
            if op in ("==", "!=", ">", "<", ">=", "<=", "和", "或"):
                return "bool"
            lt, rt = self.infer(e["left"]), self.infer(e["right"])
            if op == "+" and (lt == "str" or rt == "str"):
                return "str"
            return "int"
        if t == "unary":
            return "int" if e["op"] == "-" else "bool"
        return "int"

    def gen_val(self, e):
        """生成数值(int/bool) C 表达式。"""
        t = e["type"]
        if t == "num":
            return str(e["value"])
        if t == "bool":
            return "1" if e["value"] else "0"
        if t == "var":
            return e["name"]
        if t == "assign":
            raise ParseError("赋值不可作右值")
        if t == "call":
            n = e["name"]
            args = ", ".join(self.gen_rval(a) for a in e["args"])
            return "%s(%s)" % (self.c_name(n), args)
        if t == "binop":
            op = e["op"]
            if op in ("==", "!=", ">", "<", ">=", "<="):
                lt, rt = self.infer(e["left"]), self.infer(e["right"])
                if lt == "str" or rt == "str":
                    c = "strcmp(%s, %s)" % (self.gen_str_expr(e["left"]),
                                            self.gen_str_expr(e["right"]))
                    return "(%s %s 0)" % (c, "!=" if op == "!=" else "==")
                return "(%s %s %s)" % (self.gen_val(e["left"]), op,
                                       self.gen_val(e["right"]))
            if op in ("和", "或"):
                l, r = self.gen_val(e["left"]), self.gen_val(e["right"])
                return "((long long)(%s) %s (long long)(%s))" % (
                    l, "&&" if op == "和" else "||", r)
            if op == "+":
                lt, rt = self.infer(e["left"]), self.infer(e["right"])
                if lt == "str" or rt == "str":
                    raise ParseError("字符串拼接必须走字符串表达式")
                return "(%s + %s)" % (self.gen_val(e["left"]), self.gen_val(e["right"]))
            if op == "**":
                return "(long long)pow(%s, %s)" % (self.gen_val(e["left"]),
                                                   self.gen_val(e["right"]))
            return "(%s %s %s)" % (self.gen_val(e["left"]), op,
                                   self.gen_val(e["right"]))
        if t == "unary":
            if e["op"] == "非":
                return "(!(%s))" % self.gen_val(e["expr"])
            return "(-(%s))" % self.gen_val(e["expr"])
        raise ParseError("非数值表达式 %s" % t)

    def gen_rval(self, e):
        """右值：int/bool → gen_val；str → gen_str_expr(内联缓冲)。"""
        if self.infer(e) == "str":
            return self.gen_str_expr(e)
        return self.gen_val(e)

    def gen_str_expr(self, e):
        """生成字符串表达式的 C 代码(直接可用的 C 字符串表达式)。"""
        t = e["type"]
        if t == "str":
            return cnsh_str(e["value"])
        if t == "var":
            return e["name"]
        if t == "call":
            n = e["name"]
            if n in self.funcs and self.funcs[n].get("ret") == "str":
                args = ", ".join(self.gen_rval(a) for a in e["args"])
                return "%s(%s)" % (self.c_name(n), args)
            raise ParseError("字符串上下文调用 %s 返回类型非字符串" % n)
        if t == "binop" and e["op"] == "+":
            lt, rt = self.infer(e["left"]), self.infer(e["right"])
            if lt == "str" and rt == "str":
                left, right = self.gen_str_expr(e["left"]), self.gen_str_expr(e["right"])
                return self.strcat_c(left, right)
            raise ParseError("字符串拼接两端须同为字符串")
        raise ParseError("表达式 %s 不是字符串" % t)

    def strcat_c(self, l, r):
        # 用栈缓冲拼接(单表达式场景足够)；避免 malloc 便于鸿蒙静态内存
        return "cnsh_cat(%s, %s)" % (l, r)

    def c_name(self, n):
        if n == "打印":
            return "cnsh_print"
        if n == "范围":
            raise ParseError("范围 为循环构造，不作函数调用")
        if n in ("长度", "类型", "输入"):
            raise ParseError("内置 %s 暂不支持鸿蒙 C 后端" % n)
        return "cnsh_%s" % n

    def stmts_c(self, body, indent):
        out = []
        for s in body:
            out.extend(self.stmt_c(s, indent))
        return out

    def stmt_c(self, s, ind):
        pad = "    " * ind
        t = s["type"]
        if t == "func":
            return []
        if t == "assign":
            ty = self.infer(s["value"])
            self.var_types[s["name"]] = ty
            v = s["name"]
            if ty == "str":
                self.var_types[v] = "str"
                return ["%s%s = %s;" % (pad, v, self.gen_rval(s["value"]))]
            return ["%s%s = %s;" % (pad, v, self.gen_val(s["value"]))]
        if t == "call":
            n = s["name"]
            if n == "打印":
                return self.print_c(s["args"], pad)
            return ["%s%s;" % (pad, self.gen_val(s))]
        if t == "exprstmt":
            return ["%s%s;" % (pad, self.gen_val(s["expr"]))]
        if t == "return":
            if s["value"] is None:
                return ["%sreturn;" % pad]
            if self.infer(s["value"]) == "str":
                return ["%sreturn %s;" % (pad, self.gen_str_expr(s["value"]))]
            return ["%sreturn %s;" % (pad, self.gen_val(s["value"]))]
        if t == "if":
            cond = self.gen_val(s["cond"])
            out = ["%sif (%s) {" % (pad, cond)]
            out.extend(self.stmts_c(s["then"], ind + 1))
            if s.get("else"):
                out.append("%s} else {" % pad)
                out.extend(self.stmts_c(s["else"], ind + 1))
            out.append("%s}" % pad)
            return out
        if t == "for":
            v = s["var"]
            self.var_types[v] = "int"
            out = ["%sfor (long long %s = 0; %s < %s; %s++) {" % (
                pad, v, v, self.gen_val(s["end"]), v)]
            out.extend(self.stmts_c(s["body"], ind + 1))
            out.append("%s}" % pad)
            return out
        return []

    def print_c(self, args, pad):
        if not args:
            return ["%sprintf(\"\\n\");" % pad]
        lines = []
        for i, a in enumerate(args):
            pre = " " if i > 0 else ""
            if self.infer(a) == "str":
                lines.append("%sprintf(\"%s%%s\", %s);" % (
                    pad, pre, self.gen_str_expr(a)))
            elif self.infer(a) == "bool":
                lines.append("%sprintf(\"%s%%s\", (%s) ? \"真\" : \"假\");" % (
                    pad, pre, self.gen_val(a)))
            else:
                lines.append("%sprintf(\"%s%%lld\", (long long)(%s));" % (
                    pad, pre, self.gen_val(a)))
        lines.append("%sprintf(\"\\n\");" % pad)
        return lines

    def _collect_vars(self, stmts, out):
        """收集函数体内需显式声明的局部变量（C 无隐式声明）。"""
        for s in stmts:
            t = s["type"]
            if t == "assign":
                out[s["name"]] = self.infer(s["value"])
            elif t == "for":
                out[s["var"]] = "int"
                self._collect_vars(s["body"], out)
            elif t == "if":
                self._collect_vars(s["then"], out)
                if s.get("else"):
                    self._collect_vars(s["else"], out)

    def gen_func_c(self, st):
        name = st["name"]
        cn = self.c_name(name)
        ret, params = self.sigs[name]
        vtypes = {}
        self._collect_vars(st["body"], vtypes)
        param_names = {n for (n, _t) in st["params"]}
        lines = []
        lines.append("static %s %s(%s) {" % (ret, cn, params))
        for n, _t in st["params"]:
            self.var_types[n] = _t
        for n, ty in vtypes.items():
            if n in param_names:
                continue
            self.var_types[n] = ty
            lines.append("    %s %s = %s;" % (TYPE_C[ty], n,
                                              '""' if ty == "str" else "0"))
        lines.extend(self.stmts_c(st["body"], 1))
        if ret != "void":
            if st.get("ret") != "str":
                lines.append("    return 0;")
            else:
                lines.append("    return \"\";")
        lines.append("}")
        return lines

    def render(self):
        out = []
        out.append("/* 由 cnsh_cgen.py v0.1 自动生成 · 请勿手改 */")
        if self.dna:
            out.append('static const char* CNSH_DNA = "%s";' % self.dna)
        if self.gpg:
            out.append('static const char* CNSH_GPG = "%s";' % self.gpg)
        out.append("#include <stdio.h>")
        out.append("#include <string.h>")
        out.append("#include <math.h>")
        out.append("")
        for st in self.prog["body"]:
            if st["type"] == "func":
                ret, params = self.sigs[st["name"]]
                out.append("static %s %s(%s);" % (ret, "cnsh_%s" % st["name"], params))
        out.append("")
        out.append("static const char* cnsh_cat(const char* l, const char* r) {")
        out.append("    static char __cat_buf[1024];")
        out.append("    if (l == __cat_buf) { /* 嵌套拼接：左操作数即自身缓冲，就地追加 */")
        out.append("        strncat(__cat_buf, r, 1023 - strlen(__cat_buf));")
        out.append("        return __cat_buf;")
        out.append("    }")
        out.append("    strncpy(__cat_buf, l, 1023); __cat_buf[1023] = 0;")
        out.append("    strncat(__cat_buf, r, 1023 - strlen(__cat_buf));")
        out.append("    return __cat_buf;")
        out.append("}")
        out.append("")
        # 函数实现
        for st in self.prog["body"]:
            if st["type"] == "func":
                out.extend(self.gen_func_c(st))
                out.append("")
        # main
        if not self.napi and not self.no_main:
            out.append("int main(void) {")
            for st in self.prog["body"]:
                if st["type"] == "func" and st["name"] == "主":
                    out.append("    cnsh_主();")
            out.append("    return 0;")
            out.append("}")
        return "\n".join(out) + "\n"


def parse_program(src):
    p = Parser(tokenize(src))
    prog = p.parse_program()
    prog["_functions"] = p.functions
    return prog


def main(argv):
    import argparse
    ap = argparse.ArgumentParser(description="CNSH→C 翻译器 v0.1（鸿蒙 NDK 后端种子）")
    ap.add_argument("input")
    ap.add_argument("--out", default=None)
    ap.add_argument("--napi", action="store_true", help="生成鸿蒙 napi 注册包装(无 main)")
    ap.add_argument("--no-main", action="store_true", help="仅生成 CNSH 逻辑函数(无 main/napi)，供鸿蒙桥链接或本机冒烟")
    ap.add_argument("--dna", default="#龍芯⚡️2026-09-05-CNSH-CGEN-v0.1-UID9622")
    ap.add_argument("--gpg", default="A2D0092CEE2E5BA87035600924C3704A8CC26D5F")
    a = ap.parse_args(argv)
    with open(a.input, encoding="utf-8") as f:
        src = f.read()
    prog = parse_program(src)
    out_path = a.out or (a.input.rsplit(".", 1)[0] + ".c")
    if a.napi:
        napi_src = napi_render(prog, a.dna, a.gpg)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(napi_src)
        print("napi 输出:", out_path)
    else:
        g = CGen(prog, napi=False, no_main=a.no_main, dna=a.dna, gpg=a.gpg)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(g.render())
        print("C 输出:", out_path)
    return 0


def napi_render(prog, dna, gpg):
    """鸿蒙 N-API(C API) 注册包装：导出 CNSH 顶层功能函数为原生方法。"""
    g = CGen(prog, napi=True, dna=dna, gpg=gpg)
    core = g.render()
    exported = []
    for st in prog["body"]:
        if st["type"] == "func" and st["name"] not in ("主",):
            exported.append(st["name"])
    lines = ["/* cnsh napi bridge - 鸿蒙注册段(自动生成骨架) */",
             "#include \"napi/native_api.h\"",
             "",
             "static napi_value CnshGreet(napi_env env, napi_callback_info info) {",
             "    return NULL; /* 由 鸿蒙桥 cnsh_napi.c 手工实现，见 cpp/cnsh_napi.c */",
             "}",
             "",
             "EXTERN_C_START",
             "static napi_value Init(napi_env env, napi_value exports) {",
             "    /* 导出登记在此(手工桥在 cpp/cnsh_napi.c 完成，含 DNA 常量与三色审计) */",
             "    (void)env; (void)exports;",
             "    return exports;",
             "}",
             "EXTERN_C_END",
             "",
             "static napi_module cnshModule = {",
             "    .nm_version = 1,",
             "    .nm_flags = 0,",
             "    .nm_filename = NULL,",
             "    .nm_register_func = Init,",
             "    .nm_modname = \"cnsh_bridge\",",
             "    .nm_priv = ((void*)0),",
             "    .reserved = { 0 },",
             "};",
             "",
             "__attribute__((constructor)) static void RegisterCnshModule(void) {",
             "    napi_module_register(&cnshModule);",
             "}",
             ""]
    return core + "\n" + "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
