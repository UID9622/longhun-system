# -*- coding: utf-8 -*-
"""
CNSH v2.1 LSP 服务器（基于标准库 JSON-RPC over stdio）
DNA: #龍芯⚡️2026-06-29-CNSH-LSP-v2.1

支持：
- initialize / initialized
- textDocument/didOpen / didChange / didSave
- textDocument/publishDiagnostics（实时类型检查 + 解析错误）
- textDocument/completion
- textDocument/hover
- textDocument/definition
"""
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import lexer as lexer_mod
from . import parser as parser_mod
from . import ast_nodes as ast
from .typechecker import TypeChecker
from .errors import CNSHError
from .tokens import KEYWORDS


# LSP severity levels
SEVERITY_ERROR = 1
SEVERITY_WARNING = 2
SEVERITY_INFORMATION = 3
SEVERITY_HINT = 4


BUILTIN_DOCS = {
    "输出": "内置函数：输出内容到标准输出。",
    "输入": "内置函数：从标准输入读取一行文本。",
    "长度": "内置函数：返回列表、文本或映射的长度。",
    "字符串": "内置函数：把值转换为文本。",
    "整数": "内置函数：把值转换为整数。",
    "小数": "内置函数：把值转换为浮点数。",
    "龍": "龍魂标准库命名空间。",
    "真": "布尔真值。",
    "假": "布尔假值。",
    "变量": "声明一个变量。",
    "常量": "声明一个常量。",
    "函数": "声明一个函数。",
    "模块": "声明一个模块。",
    "结构体": "声明一个结构体。",
    "如果": "条件分支。",
    "否则如果": "条件分支。",
    "否则": "默认分支。",
    "当": "while 循环。",
    "对于": "for 循环。",
    "返回": "从函数返回。",
    "中断": "中断循环。",
    "继续": "继续下一次循环。",
    "使用": "导入模块。",
}


class LspServer:
    def __init__(self, in_stream=None, out_stream=None):
        self.in_stream = in_stream or sys.stdin.buffer
        self.out_stream = out_stream or sys.stdout.buffer
        self.documents: Dict[str, str] = {}
        self.running = False
        self._shutdown = False

    def run(self):
        self.running = True
        while self.running:
            msg = self._read_message()
            if msg is None:
                break
            self._handle(msg)

    # ---------- JSON-RPC I/O ----------
    def _read_message(self) -> Optional[Dict[str, Any]]:
        headers = {}
        while True:
            line = self.in_stream.readline()
            if not line:
                return None
            line = line.decode("utf-8").rstrip("\r\n")
            if line == "":
                break
            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip().lower()] = value.strip()
        length = int(headers.get("content-length", "0"))
        if length <= 0:
            return None
        body = self.in_stream.read(length)
        if len(body) < length:
            return None
        try:
            return json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            return None

    def _send(self, payload: Dict[str, Any]):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        header = f"Content-Length: {len(data)}\r\n\r\n".encode("ascii")
        self.out_stream.write(header + data)
        self.out_stream.flush()

    def _notify(self, method: str, params: Dict[str, Any]):
        self._send({"jsonrpc": "2.0", "method": method, "params": params})

    def _reply(self, id_: Any, result: Any):
        self._send({"jsonrpc": "2.0", "id": id_, "result": result})

    # ---------- Dispatch ----------
    def _handle(self, msg: Dict[str, Any]):
        method = msg.get("method")
        id_ = msg.get("id")
        params = msg.get("params", {})

        if method == "initialize":
            self._reply(id_, self._initialize(params))
        elif method == "initialized":
            pass
        elif method == "shutdown":
            self._shutdown = True
            self._reply(id_, None)
        elif method == "exit":
            self.running = False
        elif method == "textDocument/didOpen":
            self._did_open(params)
        elif method == "textDocument/didChange":
            self._did_change(params)
        elif method == "textDocument/didSave":
            self._did_save(params)
        elif method == "textDocument/completion":
            self._reply(id_, self._completion(params))
        elif method == "textDocument/hover":
            self._reply(id_, self._hover(params))
        elif method == "textDocument/definition":
            self._reply(id_, self._definition(params))
        else:
            self._reply(id_, None)

    def _initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "capabilities": {
                "textDocumentSync": {"openClose": True, "change": 1},
                "completionProvider": {"triggerCharacters": ["."]},
                "hoverProvider": True,
                "definitionProvider": True,
            },
            "serverInfo": {"name": "CNSH-LSP", "version": "2.1.0"},
        }

    # ---------- Document sync ----------
    def _did_open(self, params: Dict[str, Any]):
        doc = params["textDocument"]
        uri = doc["uri"]
        text = doc["text"]
        self.documents[uri] = text
        self._publish_diagnostics(uri, text)

    def _did_change(self, params: Dict[str, Any]):
        doc = params["textDocument"]
        uri = doc["uri"]
        for change in params.get("contentChanges", []):
            self.documents[uri] = change.get("text", "")
        self._publish_diagnostics(uri, self.documents.get(uri, ""))

    def _did_save(self, params: Dict[str, Any]):
        uri = params["textDocument"]["uri"]
        text = self.documents.get(uri, "")
        self._publish_diagnostics(uri, text)

    def _publish_diagnostics(self, uri: str, text: str):
        diagnostics = self._compute_diagnostics(uri, text)
        self._notify("textDocument/publishDiagnostics", {"uri": uri, "diagnostics": diagnostics})

    # ---------- Diagnostics ----------
    def _compute_diagnostics(self, uri: str, text: str) -> List[Dict[str, Any]]:
        diagnostics: List[Dict[str, Any]] = []
        file = self._uri_to_path(uri)
        try:
            tokens = lexer_mod.Lexer(text, file=file).tokenize()
            tree = parser_mod.Parser(tokens).parse()
            ok, errors, warnings = TypeChecker().check(tree)
            for w in warnings:
                diagnostics.append(self._diag_from_pos(w, SEVERITY_WARNING))
            for e in errors:
                diagnostics.append(self._diag_from_pos(e, SEVERITY_ERROR))
        except CNSHError as exc:
            diagnostics.append({
                "range": {
                    "start": {"line": max(0, exc.line - 1), "character": max(0, exc.column - 1)},
                    "end": {"line": max(0, exc.line - 1), "character": max(0, exc.column - 1) + 1},
                },
                "message": str(exc),
                "severity": SEVERITY_ERROR,
            })
        return diagnostics

    def _diag_from_pos(self, message: str, severity: int) -> Dict[str, Any]:
        line, column = self._parse_pos(message)
        return {
            "range": {
                "start": {"line": line, "character": column},
                "end": {"line": line, "character": column + 1},
            },
            "message": message,
            "severity": severity,
        }

    def _parse_pos(self, message: str) -> tuple:
        if message.startswith("[") and "]" in message:
            inner = message[1 : message.index("]")]
            parts = inner.split(":")
            if len(parts) >= 2:
                try:
                    return int(parts[0]) - 1, int(parts[1]) - 1
                except ValueError:
                    pass
        return 0, 0

    def _uri_to_path(self, uri: str) -> str:
        if uri.startswith("file://"):
            return Path(uri[7:]).as_posix()
        return uri

    # ---------- Completion ----------
    def _completion(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        uri = params["textDocument"]["uri"]
        pos = params["position"]
        text = self.documents.get(uri, "")
        items = []
        # 关键字 + 内置
        for kw in KEYWORDS:
            items.append({"label": kw, "kind": 14, "detail": "关键字"})
        for name in BUILTIN_DOCS:
            items.append({"label": name, "kind": 3, "detail": "内置"})
        # 当前文件出现的标识符
        for ident in self._extract_identifiers(text):
            items.append({"label": ident, "kind": 6, "detail": "标识符"})
        return {"items": items}

    def _extract_identifiers(self, text: str) -> List[str]:
        try:
            tokens = lexer_mod.Lexer(text).tokenize()
            return sorted({t.value for t in tokens if t.type == "IDENTIFIER"})
        except Exception:
            return []

    # ---------- Hover ----------
    def _hover(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        uri = params["textDocument"]["uri"]
        pos = params["position"]
        text = self.documents.get(uri, "")
        word = self._word_at(text, pos["line"] + 1, pos["character"] + 1)
        if not word:
            return None
        doc = BUILTIN_DOCS.get(word)
        if not doc:
            return None
        return {"contents": {"kind": "markdown", "value": f"**{word}**\n\n{doc}"}}

    def _word_at(self, text: str, line: int, column: int) -> str:
        lines = text.splitlines()
        if line < 1 or line > len(lines):
            return ""
        ln = lines[line - 1]
        col = max(0, min(column - 1, len(ln)))
        start = col
        while start > 0 and (ln[start - 1].isalnum() or ln[start - 1] == "_" or self._is_cjk(ln[start - 1])):
            start -= 1
        end = col
        while end < len(ln) and (ln[end].isalnum() or ln[end] == "_" or self._is_cjk(ln[end])):
            end += 1
        return ln[start:end]

    def _is_cjk(self, ch: str) -> bool:
        cp = ord(ch)
        return (
            0x4E00 <= cp <= 0x9FFF
            or 0x3400 <= cp <= 0x4DBF
            or 0x3040 <= cp <= 0x309F
            or 0x30A0 <= cp <= 0x30FF
            or 0xAC00 <= cp <= 0xD7AF
        )

    # ---------- Definition ----------
    def _definition(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        uri = params["textDocument"]["uri"]
        pos = params["position"]
        text = self.documents.get(uri, "")
        word = self._word_at(text, pos["line"] + 1, pos["character"] + 1)
        if not word:
            return None
        try:
            tokens = lexer_mod.Lexer(text, file=self._uri_to_path(uri)).tokenize()
            tree = parser_mod.Parser(tokens).parse()
            locator = SymbolLocator(word)
            return locator.find(tree, uri)
        except Exception:
            return None


class SymbolLocator(ast.ASTNode):
    """在 AST 中查找符号定义位置（简化版）"""

    def __init__(self, target: str):
        self.target = target

    def find(self, tree: ast.Program, uri: str) -> Optional[Dict[str, Any]]:
        for stmt in tree.statements:
            loc = self._search(stmt)
            if loc:
                return {"uri": uri, "range": loc}
        return None

    def _search(self, node: ast.ASTNode) -> Optional[Dict[str, Any]]:
        if isinstance(node, ast.FunctionDecl):
            if node.name == self.target:
                return self._range(node)
            for stmt in node.body:
                loc = self._search(stmt)
                if loc:
                    return loc
            for p in node.params:
                if p.name == self.target:
                    return self._range(p)
        elif isinstance(node, ast.VarDecl):
            if node.name == self.target:
                return self._range(node)
        elif isinstance(node, ast.ModuleDecl):
            if node.name == self.target:
                return self._range(node)
            for stmt in node.body:
                loc = self._search(stmt)
                if loc:
                    return loc
        return None

    def _range(self, node: ast.ASTNode) -> Dict[str, Any]:
        return {
            "start": {"line": max(0, node.line - 1), "character": max(0, node.column - 1)},
            "end": {"line": max(0, node.line - 1), "character": max(0, node.column - 1)},
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="CNSH v2.1 LSP 服务器")
    parser.add_argument("--stdio", action="store_true", help="使用标准输入输出通信")
    args = parser.parse_args()

    if args.stdio:
        LspServer().run()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
