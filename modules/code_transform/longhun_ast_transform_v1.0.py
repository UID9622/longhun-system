#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·AST 代码变换引擎 v1.0
模块二：把英文代码骨子里变成中文

DNA: #龍芯⚡️2026-05-28-LONGHUN-AST-TRANSFORM-v1.0
作者: UID9622 · 龍芯北辰

原理:
    代码 → AST(抽象语法树) → 重命名节点 → 重新生成代码
    逻辑100%不变，变量名/函数名/类名全换成中文

使用:
    python3 longhun_ast_transform.py --input ./raw_project --output ./cn_project
    python3 longhun_ast_transform.py --input app.py              # 单文件
    python3 longhun_ast_transform.py --input ./raw --vocab my_vocab.json
"""

import ast
import os
import re
import json
import copy
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional


# ─── 默认语义词典 ─────────────────────────────────────────
# 格式: "英文标识符": "中文标识符"
# 这是"通心译"的核心资产，会越来越大

DEFAULT_VOCAB: Dict[str, str] = {

    # ── 通用变量名 ──
    "result":        "结果",
    "results":       "结果列表",
    "data":          "数据",
    "value":         "值",
    "values":        "值列表",
    "item":          "条目",
    "items":         "条目列表",
    "key":           "键",
    "keys":          "键列表",
    "index":         "索引",
    "count":         "计数",
    "total":         "总计",
    "size":          "大小",
    "length":        "长度",
    "name":          "名称",
    "names":         "名称列表",
    "path":          "路径",
    "url":           "链接",
    "urls":          "链接列表",
    "text":          "文本",
    "content":       "内容",
    "message":       "消息",
    "msg":           "消息",
    "error":         "错误",
    "err":           "错误",
    "exception":     "异常",
    "output":        "输出",
    "input":         "输入",
    "response":      "响应",
    "request":       "请求",
    "config":        "配置",
    "settings":      "设置",
    "options":       "选项",
    "params":        "参数",
    "args":          "参数列表",
    "kwargs":        "关键字参数",
    "flag":          "标志",
    "status":        "状态",
    "state":         "状态",
    "mode":          "模式",
    "type":          "类型",
    "kind":          "种类",
    "category":      "分类",
    "tag":           "标签",
    "tags":          "标签列表",
    "label":         "标签文字",
    "labels":        "标签列表",
    "source":        "来源",
    "target":        "目标",
    "destination":   "目的地",
    "origin":        "起源",
    "prefix":        "前缀",
    "suffix":        "后缀",
    "pattern":       "模式",
    "match":         "匹配",
    "token":         "令牌",
    "tokens":        "令牌列表",
    "version":       "版本",
    "timestamp":     "时间戳",
    "timeout":       "超时",
    "retry":         "重试",
    "limit":         "上限",
    "offset":        "偏移",
    "page":          "页码",
    "buffer":        "缓冲",
    "chunk":         "块",
    "batch":         "批次",
    "queue":         "队列",
    "stack":         "栈",
    "cache":         "缓存",
    "store":         "存储",
    "db":            "数据库",
    "database":      "数据库",
    "table":         "表",
    "row":           "行",
    "col":           "列",
    "column":        "列",
    "field":         "字段",
    "record":        "记录",

    # ── 用户/身份相关 ──
    "user":          "用户",
    "users":         "用户列表",
    "user_id":       "用户编号",
    "username":      "用户名",
    "password":      "密码",
    "email":         "邮箱",
    "phone":         "手机",
    "address":       "地址",
    "profile":       "个人信息",
    "role":          "角色",
    "permission":    "权限",
    "auth":          "认证",
    "session":       "会话",
    "client":        "客户端",
    "server":        "服务端",
    "host":          "主机",
    "port":          "端口",

    # ── 数值计算 ──
    "num":           "数量",
    "number":        "数字",
    "numbers":       "数字列表",
    "amount":        "金额",
    "price":         "价格",
    "cost":          "成本",
    "score":         "得分",
    "weight":        "权重",
    "weights":       "权重列表",
    "threshold":     "阈值",
    "min_val":       "最小值",
    "max_val":       "最大值",
    "mean":          "均值",
    "avg":           "平均值",

    # ── 通用函数名 ──
    "get":           "获取",
    "set":           "设置",
    "load":          "加载",
    "save":          "保存",
    "read":          "读取",
    "write":         "写入",
    "parse":         "解析",
    "format":        "格式化",
    "convert":       "转换",
    "transform":     "变换",
    "process":       "处理",
    "handle":        "处理",
    "execute":       "执行",
    "run":           "运行",
    "start":         "启动",
    "stop":          "停止",
    "reset":         "重置",
    "clear":         "清空",
    "init":          "初始化",
    "initialize":    "初始化",
    "setup":         "设置",
    "cleanup":       "清理",
    "close":         "关闭",
    "open":          "打开",
    "create":        "创建",
    "build":         "构建",
    "make":          "生成",
    "update":        "更新",
    "delete":        "删除",
    "remove":        "移除",
    "add":           "添加",
    "append":        "追加",
    "insert":        "插入",
    "push":          "推入",
    "pop":           "弹出",
    "merge":         "合并",
    "split":         "分割",
    "join":          "连接",
    "find":          "查找",
    "search":        "搜索",
    "filter":        "过滤",
    "sort":          "排序",
    "check":         "检查",
    "validate":      "验证",
    "verify":        "核验",
    "test":          "测试",
    "log":           "记录日志",
    "print":         "打印",         # 不替换内置，仅用户自定义时
    "send":          "发送",
    "receive":       "接收",
    "fetch":         "获取",
    "upload":        "上传",
    "download":      "下载",
    "encode":        "编码",
    "decode":        "解码",
    "compress":      "压缩",
    "decompress":    "解压",
    "hash":          "哈希",
    "encrypt":       "加密",
    "decrypt":       "解密",
    "sign":          "签名",
    "verify_sign":   "验签",

    # ── 类名 ──
    "Client":        "客户端",
    "Server":        "服务端",
    "Manager":       "管理器",
    "Handler":       "处理器",
    "Parser":        "解析器",
    "Builder":       "构建器",
    "Factory":       "工厂",
    "Router":        "路由器",
    "Scheduler":     "调度器",
    "Worker":        "工作者",
    "Logger":        "日志器",
    "Config":        "配置",
    "Database":      "数据库",
    "Cache":         "缓存",
    "Queue":         "队列",
    "Engine":        "引擎",
    "Processor":     "处理器",
    "Transformer":   "变换器",
    "Validator":     "验证器",
    "Connector":     "连接器",
    "Adapter":       "适配器",
    "Wrapper":       "包装器",
    "Controller":    "控制器",
    "Model":         "模型",
    "View":          "视图",
    "Service":       "服务",
    "Repository":    "仓库",
    "Pipeline":      "流水线",

    # ── 龍魂专有 ──
    "dna":           "龍魂追溯码",
    "tricolor":      "三色审计",
    "fuse":          "熔断",
    "route":         "路由",
    "drawer":        "语义抽屉",
    "sovereignty":   "主权",
    "manifest":      "宣言",
}

# Python 内置函数/关键字，绝对不能改名
PYTHON_BUILTINS = {
    "print", "len", "range", "enumerate", "zip", "map", "filter",
    "isinstance", "issubclass", "hasattr", "getattr", "setattr", "delattr",
    "type", "list", "dict", "set", "tuple", "str", "int", "float", "bool",
    "bytes", "bytearray", "memoryview", "object", "super", "property",
    "staticmethod", "classmethod", "open", "input", "format",
    "abs", "all", "any", "bin", "chr", "dir", "divmod", "eval", "exec",
    "hash", "hex", "id", "iter", "max", "min", "next", "oct", "ord",
    "pow", "repr", "reversed", "round", "sorted", "sum", "vars",
    "Exception", "ValueError", "TypeError", "KeyError", "IndexError",
    "AttributeError", "IOError", "OSError", "RuntimeError", "StopIteration",
    "True", "False", "None", "self", "cls", "__init__", "__str__", "__repr__",
    "__len__", "__iter__", "__next__", "__enter__", "__exit__",
    "__name__", "__file__", "__doc__", "__all__",
}


# ─── AST 变换器 ───────────────────────────────────────────

class 中文变换器(ast.NodeTransformer):
    """
    把 Python AST 里的英文标识符替换为中文
    保留所有逻辑结构，只改名字
    """

    def __init__(self, vocab: Dict[str, str], rename_map: Dict[str, str] = None):
        self.vocab = vocab
        # rename_map: 记录本次实际完成的替换 {原名: 新名}
        self.rename_map: Dict[str, str] = rename_map if rename_map is not None else {}

    def _translate(self, name: str) -> str:
        """翻译一个标识符"""
        if name in PYTHON_BUILTINS:
            return name
        if name.startswith("__") and name.endswith("__"):
            return name  # 魔法方法不改
        if name in self.vocab:
            new_name = self.vocab[name]
            self.rename_map[name] = new_name
            return new_name
        # 处理下划线分词: calculate_total_price → 逐词翻译
        parts = name.split("_")
        translated = []
        for part in parts:
            translated.append(self.vocab.get(part, part))
        result = "_".join(translated)
        if result != name:
            self.rename_map[name] = result
        return result

    # ── 函数名 ──
    def visit_FunctionDef(self, node):
        node.name = self._translate(node.name)
        self.generic_visit(node)
        return node

    def visit_AsyncFunctionDef(self, node):
        node.name = self._translate(node.name)
        self.generic_visit(node)
        return node

    # ── 类名 ──
    def visit_ClassDef(self, node):
        node.name = self._translate(node.name)
        self.generic_visit(node)
        return node

    # ── 变量名 ──
    def visit_Name(self, node):
        node.id = self._translate(node.id)
        return node

    # ── 关键字参数名 ──
    def visit_keyword(self, node):
        if node.arg:
            node.arg = self._translate(node.arg)
        self.generic_visit(node)
        return node

    # ── 函数参数 ──
    def visit_arg(self, node):
        if node.arg not in {"self", "cls"}:
            node.arg = self._translate(node.arg)
        self.generic_visit(node)
        return node

    # ── 属性访问 a.name ──
    def visit_Attribute(self, node):
        node.attr = self._translate(node.attr)
        self.generic_visit(node)
        return node

    # ── 类型注解里的字符串 (前向引用) ──
    def visit_Constant(self, node):
        return node  # 字符串常量不改（防止改掉正常字符串）


# ─── 文件级处理 ───────────────────────────────────────────

def transform_file(
    src_path: Path,
    dest_path: Path,
    vocab: Dict[str, str],
    original_header: str = "",
) -> dict:
    """
    变换单个 Python 文件
    返回变换报告
    """
    report = {
        "file": str(src_path),
        "success": False,
        "renames": {},
        "error": None,
    }

    try:
        source = src_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        report["error"] = f"读取失败: {e}"
        return report

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        report["error"] = f"AST解析失败: {e}"
        return report

    rename_map = {}
    transformer = 中文变换器(vocab, rename_map)
    new_tree = transformer.visit(copy.deepcopy(tree))

    try:
        new_source = ast.unparse(new_tree)
    except Exception as e:
        report["error"] = f"代码生成失败: {e}"
        return report

    # 构建文件头部注释
    dna_hash = hashlib.sha256(source.encode()).hexdigest()[:8].upper()
    header_lines = [
        "# -*- coding: utf-8 -*-",
        f"# 本文件由 龍魂·AST变换引擎 v1.0 自动处理",
        f"# DNA: #龍芯⚡️{datetime.utcnow().strftime('%Y-%m-%d')}-AST-{dna_hash}",
        "#",
    ]
    if original_header:
        header_lines.append("# ─── 原始版权声明（遵守开源协议，保留如下）───")
        for line in original_header.splitlines():
            header_lines.append(f"# {line}")
        header_lines.append("# ─────────────────────────────────────────────")
    header_lines.append(f"# 命名变换对照: {len(rename_map)} 处")
    for orig, new in list(rename_map.items())[:10]:
        header_lines.append(f"#   {orig} → {new}")
    if len(rename_map) > 10:
        header_lines.append(f"#   ... 及其他 {len(rename_map)-10} 处")
    header_lines.append("")

    final_source = "\n".join(header_lines) + "\n" + new_source

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(final_source, encoding="utf-8")

    report["success"] = True
    report["renames"] = rename_map
    return report


def extract_license_header(source: str) -> str:
    """从源文件提取版权注释块（前20行里的注释）"""
    lines = source.splitlines()[:30]
    header = []
    for line in lines:
        stripped = line.strip().lstrip("#").strip()
        if stripped and any(kw in stripped.lower()
                            for kw in ["copyright", "license", "author",
                                       "©", "(c)", "rights"]):
            header.append(stripped)
    return "\n".join(header)


# ─── 项目级处理 ───────────────────────────────────────────

def transform_project(
    src_dir: Path,
    dest_dir: Path,
    vocab: Dict[str, str],
    extensions: tuple = (".py",),
) -> dict:
    """
    变换整个项目目录
    """
    print(f"\n🔄 开始变换: {src_dir} → {dest_dir}")

    summary = {
        "total": 0,
        "success": 0,
        "failed": 0,
        "skipped": 0,
        "rename_total": 0,
        "files": [],
    }

    dest_dir.mkdir(parents=True, exist_ok=True)

    for src_file in src_dir.rglob("*"):
        if src_file.is_dir():
            continue

        # 相对路径，用于生成目标路径
        rel = src_file.relative_to(src_dir)
        dest_file = dest_dir / rel

        # 只处理指定扩展名
        if src_file.suffix not in extensions:
            # 非代码文件直接复制（LICENSE, README 等保留）
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            try:
                import shutil
                shutil.copy2(src_file, dest_file)
                print(f"   📋 复制: {rel}")
                summary["skipped"] += 1
            except Exception as e:
                print(f"   ❌ 复制失败 {rel}: {e}")
            continue

        summary["total"] += 1
        print(f"   🔄 变换: {rel}", end="")

        # 读取原始版权注释
        try:
            raw = src_file.read_text(encoding="utf-8", errors="replace")
            orig_header = extract_license_header(raw)
        except Exception:
            orig_header = ""

        report = transform_file(src_file, dest_file, vocab, orig_header)

        if report["success"]:
            n_renames = len(report["renames"])
            summary["success"] += 1
            summary["rename_total"] += n_renames
            print(f"  ✅ ({n_renames} 处替换)")
        else:
            summary["failed"] += 1
            print(f"  ❌ {report['error']}")

        summary["files"].append(report)

    return summary


# ─── CLI ─────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="龍魂·AST代码变换引擎 · 英文代码骨子里变成中文"
    )
    parser.add_argument("--input",  required=True, help="输入: 文件或目录")
    parser.add_argument("--output", default=None,  help="输出: 文件或目录（默认在原目录旁创建 _cn 版）")
    parser.add_argument("--vocab",  default=None,  help="自定义词典 JSON 文件（英->中）")
    parser.add_argument("--ext",    default=".py", help="处理的扩展名，逗号分隔，默认 .py")
    parser.add_argument("--dump-vocab", action="store_true",
                        help="把内置词典导出为 JSON 文件")
    args = parser.parse_args()

    # 导出词典模式
    if args.dump_vocab:
        vocab_path = Path("longhun_vocab.json")
        vocab_path.write_text(
            json.dumps(DEFAULT_VOCAB, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"✅ 词典已导出: {vocab_path}  ({len(DEFAULT_VOCAB)} 词条)")
        print("📝 你可以编辑这个文件，加入自己的专有词汇，然后用 --vocab 参数传入")
        return

    # 加载词典
    vocab = dict(DEFAULT_VOCAB)
    if args.vocab:
        extra = json.loads(Path(args.vocab).read_text(encoding="utf-8"))
        vocab.update(extra)
        print(f"✅ 已加载自定义词典: {len(extra)} 词条（合计 {len(vocab)} 词）")

    src = Path(args.input)
    if not src.exists():
        print(f"❌ 输入路径不存在: {src}")
        sys.exit(1)

    extensions = tuple(f".{e.lstrip('.')}" for e in args.ext.split(","))

    # ── 单文件模式 ──
    if src.is_file():
        dest = Path(args.output) if args.output else src.with_suffix("_中文.py")
        raw = src.read_text(encoding="utf-8", errors="replace")
        orig_header = extract_license_header(raw)
        report = transform_file(src, dest, vocab, orig_header)
        if report["success"]:
            print(f"✅ 变换完成: {dest}")
            print(f"   共替换 {len(report['renames'])} 处标识符")
            for orig, new in report["renames"].items():
                print(f"   {orig:30s} → {new}")
        else:
            print(f"❌ 变换失败: {report['error']}")
        return

    # ── 目录模式 ──
    dest = Path(args.output) if args.output else src.parent / (src.name + "_中文版")
    summary = transform_project(src, dest, vocab, extensions)

    print(f"\n{'='*60}")
    print(f"📊 变换统计:")
    print(f"   处理文件: {summary['total']}")
    print(f"   ✅ 成功:   {summary['success']}")
    print(f"   ❌ 失败:   {summary['failed']}")
    print(f"   📋 复制:   {summary['skipped']}")
    print(f"   🔤 总替换: {summary['rename_total']} 处")
    print(f"   输出目录: {dest}")
    dna = f"#龍芯⚡️{datetime.utcnow().strftime('%Y-%m-%d')}-AST-TRANSFORM-DONE"
    print(f"   DNA: {dna}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
