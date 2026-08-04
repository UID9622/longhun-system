#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 老百姓维权助手 Web 版
DNA: #龍芯⚡️2026-06-29-LONGHUN-RIGHTS-WEB-v1.0

本地运行，浏览器打开 http://127.0.0.1:9633/
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rights_assistant import 加载模板, 识别场景, 生成报告

HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>龍魂 · 老百姓维权助手</title>
<style>
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f7f7f7; color: #333; }
h1 { color: #b22222; }
label { display: block; margin-top: 15px; font-weight: bold; }
textarea, input { width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }
button { margin-top: 20px; padding: 12px 24px; background: #b22222; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; }
button:hover { background: #8b0000; }
#result { margin-top: 30px; background: white; padding: 20px; border-radius: 8px; white-space: pre-wrap; display: none; }
.footer { margin-top: 40px; font-size: 12px; color: #666; text-align: center; }
</style>
</head>
<body>
<h1>🐉 龍魂 · 老百姓维权助手</h1>
<p>本地运行，不上传任何平台。输入你的遭遇，自动生成投诉书、法条、话术、证据清单。</p>

<label>描述你的遭遇</label>
<textarea id="text" rows="4" placeholder="例如：物业强制我人脸识别才能进小区门"></textarea>

<label>你的姓名</label>
<input id="name" type="text" placeholder="（你的姓名）">

<label>联系电话</label>
<input id="contact" type="text" placeholder="（联系电话）">

<label>被投诉对象</label>
<input id="target" type="text" placeholder="（物业/公司/商家/房东）">

<label>涉及金额（如有）</label>
<input id="amount" type="text" placeholder="（金额）">

<button onclick="submit()">生成维权报告</button>

<div id="result"></div>
<div class="footer">DNA: #龍芯⚡️2026-06-29-LONGHUN-RIGHTS-WEB-v1.0 · 本地 AI · 人民数据主权</div>

<script>
async function submit() {
    const btn = document.querySelector('button');
    btn.disabled = true; btn.textContent = '生成中...';
    const payload = {
        text: document.getElementById('text').value,
        name: document.getElementById('name').value,
        contact: document.getElementById('contact').value,
        target: document.getElementById('target').value,
        amount: document.getElementById('amount').value,
    };
    const res = await fetch('/api/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
    });
    const data = await res.json();
    const r = document.getElementById('result');
    r.style.display = 'block';
    if (data.error) {
        r.textContent = '⚠️ ' + data.error;
    } else {
        r.textContent = data.report;
    }
    btn.disabled = false; btn.textContent = '生成维权报告';
}
</script>
</body>
</html>
"""


def 启动服务(端口: int = 9633):
    try:
        from flask import Flask, request, jsonify
    except ImportError:
        print("❌ 需要先安装 flask: pip install flask")
        sys.exit(1)

    app = Flask(__name__)
    模板 = 加载模板()

    @app.route("/")
    def index():
        return HTML

    @app.route("/api/generate", methods=["POST"])
    def generate():
        data = request.get_json(force=True)
        文本 = data.get("text", "")
        if not 文本:
            return jsonify({"error": "请输入遭遇描述"}), 400

        场景名 = 识别场景(文本, 模板)
        if not 场景名:
            return jsonify({"error": "暂未识别到具体维权场景，请描述得更具体一些。"}), 400

        参数 = {
            "name": data.get("name") or "（你的姓名）",
            "contact": data.get("contact") or "（联系电话）",
            "target": data.get("target") or "（对方单位/个人）",
            "amount": data.get("amount") or "（金额）",
            "date": "（日期）",
            "id_card": "（身份证号）",
            "org_code": "（统一社会信用代码）",
            "position": "（岗位）",
            "start_date": "（入职/开始日期）",
            "arrears_date": "（开始欠薪日期）",
            "months": "（月数）",
            "product": "（商品/服务名称）",
            "problem": "（问题描述）",
            "purchase_date": "（购买日期）",
            "claim": "（商家宣传内容）",
            "reality": "（实际情况）",
            "compensation": "（索赔金额）",
            "order_no": "（订单号）",
            "address": "（房屋地址）",
            "end_date": "（合同结束日期）",
            "excuse": "（对方理由）",
        }
        数据 = 模板["scenarios"][场景名]
        报告 = 生成报告(场景名, 数据, 参数)

        # 构造文本版报告
        lines = [
            f"【{报告['场景']}】",
            f"生成时间: {报告['生成时间']}",
            f"DNA: {报告['dna']}",
            "",
            "📜 投诉书",
            报告["投诉书"],
            "",
            "⚖️ 法条依据",
        ]
        for 法条 in 报告["法条依据"]:
            lines.append("• " + 法条)
        lines.extend(["", "🗣 怼人话术"])
        for 话术 in 报告["怼人话术"]:
            lines.append("• " + 话术)
        lines.extend(["", "📂 证据清单"])
        for 证据 in 报告["证据清单"]:
            lines.append("• " + 证据)
        lines.extend(["", "📢 投诉渠道"])
        for 渠道 in 报告["投诉渠道"]:
            lines.append("• " + 渠道)
        lines.extend(["", "本报告由本地 AI 生成，不上传任何平台。"])

        return jsonify({"report": "\n".join(lines)})

    print(f"🐉 维权助手网页版已启动: http://127.0.0.1:{端口}/")
    app.run(host="127.0.0.1", port=端口, debug=False)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=9633)
    args = parser.parse_args()
    启动服务(args.port)
