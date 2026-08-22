# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · CNSH 模型路由器 v1.1 · 锚点断言测试
🟡 mock 测试：不打真实 API（requests 全 mock），仅验证路由/审计/DNA/闸门逻辑
退出码: 0=🟢全过 1=🔴有失败
"""
import os, sys, json, tempfile, shutil
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "08_BIN"))
from model_router import (ModelRouter, ModelRegistry, CNSHEditorModelExtension,
                          OpenAICompatibleAdapter, ConfirmGateError, CONFIRM)
from lh_ganzhi import generate_dna

PASS, FAIL = 0, 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1; print(f"  🟢 {name}")
    else: FAIL += 1; print(f"  🔴 {name}"); 

tmp = tempfile.mkdtemp()
reg_path = os.path.join(tmp, "model-registry.yaml")
log_path = os.path.join(tmp, "logs", "shiguan.jsonl")

print("== A. DNA 干支格式 ==")
dna = generate_dna("TEST", "v1.1")
check("DNA 含干支分隔符", dna.count("·") == 3)
check("DNA 含动作标签与版本", "TEST" in dna and "v1.1" in dna)
check("DNA 无旧时间戳格式", "-" not in dna.split("·")[0].replace("#龍芯⚡️丙午",""))

print("== B. 注册表与确认码闸门 ==")
reg = ModelRegistry(reg_path)
check("默认注册表已创建", os.path.exists(reg_path))
check("默认模型 kimi 存在", reg.get("kimi") is not None)
try:
    reg.add_model({"id": "evil"}, confirm_code="WRONG-CODE")
    check("错误确认码被拒绝", False)
except ConfirmGateError:
    check("错误确认码被拒绝", True)
check("正确确认码可写", reg.update_status("kimi", "active", confirm_code=CONFIRM))

print("== C. v1.0 必炸 bug 复验（kwargs 修复）==")
try:
    ad = OpenAICompatibleAdapter(reg.get("kimi"))
    check("OpenAICompatibleAdapter 初始化不炸", True)
    check("timeout 默认 60", ad.timeout == 60)
except NameError:
    check("OpenAICompatibleAdapter 初始化不炸", False)

print("== D. 语言路由 ==")
router = ModelRouter(reg_path, log_path)
zh = router.registry.get_by_language("zh")
check("zh 路由首选 kimi (weight 1.0)", zh and zh[0]["id"] == "kimi")
ar = router.registry.get_by_language("ar")
check("ar 路由到 jais", ar and ar[0]["id"] == "jais")

print("== E. 调用链（mock requests）==")
fake_resp = MagicMock()
fake_resp.status_code = 200
fake_resp.json.return_value = {"choices": [{"message": {"content": "你好，这是模拟响应内容"}}],
                               "usage": {"total_tokens": 42}}
fake_resp.raise_for_status = lambda: None
with patch("model_router.requests.post", return_value=fake_resp), \
     patch("model_router.requests.get", return_value=fake_resp):
    result = router.route("你好", language="zh")
check("路由调用成功", result.get("success") is True)
check("返回体含 DNA", bool(result.get("dna")))
check("三色审计已注入", result.get("audit", {}).get("tricolor") in ("🟢", "🟡", "🔴"))
check("审计评分在 0-100", 0 <= result.get("audit", {}).get("score", -1) <= 100)

print("== F. 史官记录落盘（只传用量不传内容）==")
check("shiguan.jsonl 已生成", os.path.exists(log_path))
if os.path.exists(log_path):
    line = json.loads(open(log_path, encoding="utf-8").readline())
    check("史官含 prompt_length", "prompt_length" in line)
    check("史官不含 prompt 本体", "prompt" not in line and "content" not in line)

print("== G. 故障转移 ==")
with patch("model_router.requests.post", side_effect=Exception("mock-down")), \
     patch("model_router.requests.get", return_value=fake_resp):
    r2 = router.route("测试", language="zh")
check("全模型挂时返回失败+DNA", r2.get("success") is False and bool(r2.get("dna")))

print("== H. 编辑器扩展 ==")
ed = CNSHEditorModelExtension(router)
check("set_model 生效", ed.set_model("jais") is True)
check("set_model 拒绝不存在模型", ed.set_model("ghost") is False)

shutil.rmtree(tmp)
print(f"\n结果: {PASS} 过 / {FAIL} 挂 -> 退出码 {0 if FAIL == 0 else 1}")
sys.exit(0 if FAIL == 0 else 1)
