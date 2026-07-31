# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
from __future__ import annotations
"""
CNSH v2.1 LSP 服务器测试
DNA: #龍芯⚡️2026-06-29-CNSH-LSP-TESTS-v2.1
"""
import io
import json
import unittest

from cnsh_v21.lsp_server import LspServer


class TestLspServer(unittest.TestCase):
    def _send(self, server: LspServer, msg: dict[str, Any]):
        body = json.dumps(msg, ensure_ascii=False).encode("utf-8")
        data = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body
        server.in_stream = io.BytesIO(data)

    def _read_response(self, server: LspServer) -> dict[str, Any]:
        server.out_stream.seek(0)
        header = b""
        while b"\r\n\r\n" not in header:
            chunk = server.out_stream.read(1)
            if not chunk:
                break
            header += chunk
        if not header:
            return {}
        length = 0
        for line in header.decode("ascii").split("\r\n"):
            if line.startswith("Content-Length:"):
                length = int(line.split(":", 1)[1].strip())
                break
        body = server.out_stream.read(length)
        return json.loads(body.decode("utf-8"))

    def test_initialize(self):
        out = io.BytesIO()
        server = LspServer(in_stream=io.BytesIO(), out_stream=out)
        self._send(server, {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
        server._handle(server._read_message())
        resp = self._read_response(server)
        self.assertEqual(resp["id"], 1)
        self.assertIn("capabilities", resp["result"])
        self.assertTrue(resp["result"]["capabilities"]["hoverProvider"])

    def test_diagnostics_on_open(self):
        out = io.BytesIO()
        server = LspServer(in_stream=io.BytesIO(), out_stream=out)
        server._did_open({"textDocument": {"uri": "file:///test.cnsh", "text": "变量 x: 整数 = \"错误\""}})
        # 读取 publishDiagnostics 通知
        resp = self._read_response(server)
        self.assertEqual(resp["method"], "textDocument/publishDiagnostics")
        self.assertEqual(resp["params"]["uri"], "file:///test.cnsh")
        self.assertTrue(len(resp["params"]["diagnostics"]) > 0)

    def test_completion(self):
        out = io.BytesIO()
        server = LspServer(in_stream=io.BytesIO(), out_stream=out)
        server.documents["file:///test.cnsh"] = "变量 计数 = 1"
        self._send(
            server,
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "textDocument/completion",
                "params": {"textDocument": {"uri": "file:///test.cnsh"}, "position": {"line": 0, "character": 0}},
            },
        )
        server._handle(server._read_message())
        resp = self._read_response(server)
        labels = [item["label"] for item in resp["result"]["items"]]
        self.assertIn("变量", labels)
        self.assertIn("输出", labels)
        self.assertIn("计数", labels)


if __name__ == "__main__":
    unittest.main()
