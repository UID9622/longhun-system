#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
龍魂生态准入弹窗 · 嵌入器 v1.0
LongHun Sovereign Popup Embedder — injects alive verification into all entry points

功能：
  1. 生成可嵌入的 HTML/JS 弹窗代码
  2. 自动检测所有分发点并注入
  3. 提供 HTTP API 供前端调用 (/api/eco/alive-status)
  4. 弹窗样式：深渊暗色 + 龍魂金 + 三色状态徽章

DNA: #龍芯⚡️丙午·甲申·辛丑·坤卦-SOVEREIGN-POPUP-EMBEDDER-v1.0
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
Creator: 诸葛鑫 (UID9622)
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


# ═════════════════════════════════════════════════
# 弹窗 HTML/JS 模板
# ═════════════════════════════════════════════════

POPUP_TEMPLATE = """<!-- 龍魂生态准入弹窗 · 自动注入 · 勿手动修改 -->
<style>
#lh-eco-popup-overlay {
    display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0, 0, 0, 0.85); z-index: 99999; justify-content: center; align-items: center;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
}
#lh-eco-popup-overlay.active { display: flex; }
.lh-popup-card {
    background: linear-gradient(145deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%);
    border: 1px solid #c9a54b; border-radius: 12px; padding: 32px 40px;
    max-width: 480px; width: 90%; text-align: center; color: #e0d5c1;
    box-shadow: 0 0 60px rgba(201, 165, 75, 0.15), 0 8px 32px rgba(0,0,0,0.6);
}
.lh-popup-title {
    font-size: 28px; font-weight: 700; color: #c9a54b; margin-bottom: 8px;
    letter-spacing: 2px;
}
.lh-popup-subtitle {
    font-size: 14px; color: #8a7a5a; margin-bottom: 24px;
}
.lh-status-badge {
    display: inline-block; padding: 6px 18px; border-radius: 20px;
    font-size: 13px; font-weight: 600; margin: 16px 0; letter-spacing: 1px;
}
.lh-status-alive { background: rgba(46, 204, 113, 0.15); color: #2ecc71; border: 1px solid rgba(46, 204, 113, 0.3); }
.lh-status-expired { background: rgba(241, 196, 15, 0.15); color: #f1c40f; border: 1px solid rgba(241, 196, 15, 0.3); }
.lh-status-builder { background: rgba(201, 165, 75, 0.15); color: #c9a54b; border: 1px solid rgba(201, 165, 75, 0.3); }
.lh-popup-detail { font-size: 13px; color: #8a8a8a; line-height: 1.8; margin: 16px 0; }
.lh-popup-btn {
    display: inline-block; margin: 6px; padding: 10px 24px; border-radius: 6px;
    font-size: 14px; font-weight: 600; cursor: pointer; border: none; letter-spacing: 1px;
    transition: all 0.2s ease;
}
.lh-btn-primary {
    background: linear-gradient(135deg, #c9a54b, #e2c87a); color: #0a0a0f;
}
.lh-btn-primary:hover { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(201,165,75,0.4); }
.lh-btn-secondary { background: transparent; color: #c9a54b; border: 1px solid #c9a54b; }
.lh-btn-secondary:hover { background: rgba(201,165,75,0.1); }
.lh-popup-footer { font-size: 11px; color: #5a5a5a; margin-top: 20px; }
.lh-popup-footer a { color: #c9a54b; text-decoration: none; }
</style>

<div id="lh-eco-popup-overlay">
    <div class="lh-popup-card">
        <div class="lh-popup-title">🌐 龍魂生态</div>
        <div class="lh-popup-subtitle">月度活人验证 · 生态准入关</div>
        <div id="lh-status-badge" class="lh-status-badge">加载中...</div>
        <div class="lh-popup-detail" id="lh-popup-detail"></div>
        <div>
            <button class="lh-popup-btn lh-btn-primary" onclick="lhEcoRenew()">💓 续费心跳 ¥1/月</button>
            <button class="lh-popup-btn lh-btn-secondary" onclick="lhEcoClose()">稍后再说</button>
        </div>
        <div class="lh-popup-footer">
            每月1元证明你是活人 · 数据永远归你 · <a href="https://uid9622.cn/protocol" target="_blank">协议全文</a>
        </div>
    </div>
</div>

<script>
(function() {
    var API_BASE = '/api/eco';
    var popup = document.getElementById('lh-eco-popup-overlay');
    var lastShown = localStorage.getItem('lh_eco_popup_last');
    var now = Date.now();
    
    // 24小时内不重复弹窗
    if (lastShown && (now - parseInt(lastShown)) < 86400000) return;
    
    function showPopup() {
        if (popup) popup.classList.add('active');
        localStorage.setItem('lh_eco_popup_last', now.toString());
    }
    
    function fetchStatus() {
        fetch(API_BASE + '/alive-status')
            .then(function(r) { return r.json(); })
            .then(function(data) {
                var badge = document.getElementById('lh-status-badge');
                var detail = document.getElementById('lh-popup-detail');
                if (!badge || !detail) return;
                
                if (data.status === 'alive') {
                    badge.textContent = '🟢 生态内';
                    badge.className = 'lh-status-badge lh-status-alive';
                    detail.innerHTML = '验证有效 · 到期: ' + (data.expiry || '—') + '<br>剩余: ' + (data.days_left || 0) + '天';
                    // 生态内不弹窗
                } else if (data.status === 'builder') {
                    badge.textContent = '⚪ 共建者';
                    badge.className = 'lh-status-badge lh-status-builder';
                    detail.innerHTML = '连续12月+ · 生态内全功能 + 治理投票';
                } else {
                    badge.textContent = '🟡 生态外';
                    badge.className = 'lh-status-badge lh-status-expired';
                    detail.innerHTML = '月度验证已过期<br>数据保留·可导出·不锁功能<br>续费1元即刻回归生态内';
                    showPopup();
                }
            })
            .catch(function() {
                // API不可达时不弹窗
            });
    }
    
    // 页面加载后2秒检查
    setTimeout(fetchStatus, 2000);
    
    // 暴露全局函数
    window.lhEcoRenew = function() {
        fetch(API_BASE + '/renew', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({uid: 'UID9622'}) })
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (data.qr_code || data.payment_url) {
                    window.open(data.payment_url || data.qr_code, '_blank');
                }
                if (popup) popup.classList.remove('active');
                setTimeout(fetchStatus, 3000);
            });
    };
    window.lhEcoClose = function() {
        if (popup) popup.classList.remove('active');
    };
})();
</script>
<!-- /龍魂生态准入弹窗 -->"""

# ═════════════════════════════════════════════════
# API Handler (Flask/FastAPI 兼容)
# ═════════════════════════════════════════════════

API_HANDLER_CODE = '''
# ── 生态准入 API ──
@app.route('/api/eco/alive-status', methods=['GET'])
def eco_alive_status():
    """查询生态状态 · 前端弹窗调用"""
    uid = request.args.get('uid', 'UID9622')
    try:
        from bin.lh_ecosystem_passport import 月度活人验证
        ok, msg = 月度活人验证(uid)
        now = datetime.datetime.now()
        # 解析到期日
        import re as _re
        expiry_match = _re.search(r'到期: (\\d{4}-\\d{2}-\\d{2})', msg)
        expiry = expiry_match.group(1) if expiry_match else ""
        days_match = _re.search(r'剩余: (\\d+)天', msg)
        days_left = int(days_match.group(1)) if days_match else 0
        
        # 判定状态
        if "共建者" in msg:
            status = "builder"
        elif "生态内" in msg:
            status = "alive"
        else:
            status = "expired"
        
        return jsonify({"status": status, "expiry": expiry, "days_left": days_left, "detail": msg})
    except Exception as e:
        return jsonify({"status": "unknown", "error": str(e)})

@app.route('/api/eco/renew', methods=['POST'])
def eco_renew():
    """续费心跳 · 前端续费按钮调用"""
    data = request.get_json() or {}
    uid = data.get('uid', 'UID9622')
    try:
        from bin.lh_ecosystem_passport import 活人验证心跳
        ok, msg = 活人验证心跳(uid)
        # 尝试获取支付二维码
        payment_url = ""
        try:
            import sys as _s
            _s.path.insert(0, '03_LAYERS/L5_服务层/services/xpay')
            from xpay_gateway import XPayGateway
            gw = XPayGateway()
            order = gw.create_payment_order(uid, 1.0, "月度活人验证续费")
            payment_url = order.get("qr_code", "") or order.get("payment_url", "")
        except Exception:
            pass
        return jsonify({"success": ok, "detail": msg, "payment_url": payment_url})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
'''


# ═════════════════════════════════════════════════
# 扫描 & 注入引擎
# ═════════════════════════════════════════════════

class PopupEmbedder:
    """弹窗注入器 — 自动扫描所有分发点并注入生态准入弹窗"""

    def __init__(self, workspace_root: str = ""):
        self.root = Path(workspace_root) if workspace_root else Path(__file__).parent.parent
        self.inject_marker = "<!-- 龍魂生态准入弹窗 · 自动注入 -->"
        self.stats = {"scanned": 0, "injected": 0, "already_injected": 0, "skipped": 0, "errors": []}

    def scan_entry_points(self) -> List[Path]:
        """扫描所有 HTML 分发点"""
        entries = []
        search_dirs = [
            self.root / "web",
            self.root / "web_apps",
            self.root / "10_PORTAL",
            self.root / "portal",
            self.root / "dashboard",
            self.root / "pages",
            self.root / "public-content",
        ]
        for d in search_dirs:
            if d.exists():
                entries.extend(d.rglob("*.html"))
                entries.extend(d.rglob("*.vue"))
        
        # 也检查根目录的 index.html
        root_html = self.root / "index.html"
        if root_html.exists():
            entries.append(root_html)
        
        return sorted(set(entries))

    def inject_popup(self, filepath: Path, dry_run: bool = False) -> Tuple[bool, str]:
        """向单个 HTML 文件注入弹窗代码"""
        self.stats["scanned"] += 1
        try:
            content = filepath.read_text(encoding='utf-8')
        except Exception as e:
            self.stats["skipped"] += 1
            self.stats["errors"].append(str(filepath))
            return False, f"读取失败: {e}"

        # 检查是否已注入
        if self.inject_marker in content:
            self.stats["already_injected"] += 1
            return True, "已注入·跳过"

        # 注入位置：</body> 之前，或 </html> 之前
        injected = False
        if "</body>" in content:
            content = content.replace("</body>", POPUP_TEMPLATE + "\n</body>")
            injected = True
        elif "</html>" in content:
            content = content.replace("</html>", POPUP_TEMPLATE + "\n</html>")
            injected = True
        
        if not injected:
            self.stats["skipped"] += 1
            return False, "未找到注入点"

        if not dry_run:
            try:
                filepath.write_text(content, encoding='utf-8')
                self.stats["injected"] += 1
            except Exception as e:
                self.stats["errors"].append(str(filepath))
                return False, f"写入失败: {e}"
        else:
            self.stats["injected"] += 1

        return True, "注入成功"

    def inject_all(self, dry_run: bool = False) -> dict:
        """扫描并注入所有分发点"""
        entries = self.scan_entry_points()
        for fp in entries:
            ok, msg = self.inject_popup(fp, dry_run=dry_run)
        
        return {
            "scanned": self.stats["scanned"],
            "injected": self.stats["injected"],
            "already_injected": self.stats["already_injected"],
            "skipped": self.stats["skipped"],
            "errors": self.stats["errors"],
            "entry_points": [str(e.relative_to(self.root)) for e in entries],
        }

    def list_entry_points(self) -> List[dict]:
        """列出所有分发点及注入状态"""
        entries = self.scan_entry_points()
        results = []
        for fp in entries:
            try:
                content = fp.read_text(encoding='utf-8')
                status = "已注入" if self.inject_marker in content else "待注入"
            except Exception:
                status = "读取错误"
            results.append({
                "path": str(fp.relative_to(self.root)),
                "status": status,
                "size": fp.stat().st_size if fp.exists() else 0,
            })
        return results

    def generate_api_handler(self) -> str:
        """生成 API handler 代码（可复制到 Flask/FastAPI app）"""
        return API_HANDLER_CODE

    def generate_standalone_popup_html(self) -> str:
        """生成独立弹窗 HTML（可直接在浏览器打开测试）"""
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>龍魂生态准入</title>
<style>
body {{ margin: 0; padding: 0; background: #0a0a0f; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
</style>
</head>
<body>
{POPUP_TEMPLATE}
<script>
// 测试模式：自动显示弹窗
document.getElementById('lh-eco-popup-overlay').classList.add('active');
document.getElementById('lh-status-badge').textContent = '🟡 生态外';
document.getElementById('lh-status-badge').className = 'lh-status-badge lh-status-expired';
document.getElementById('lh-popup-detail').textContent = '月度验证已过期\\n数据保留·可导出\\n续费1元即刻回归';
</script>
</body>
</html>"""


# ═════════════════════════════════════════════════
# CLI
# ═════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂生态准入弹窗嵌入器 v1.0")
    parser.add_argument("action", nargs="?", default="list",
                       choices=["scan", "list", "inject", "dry-run", "generate-api", "generate-popup"])
    parser.add_argument("--workspace", "-w", default="", help="工作区根目录")
    args = parser.parse_args()

    embedder = PopupEmbedder(args.workspace) if args.workspace else PopupEmbedder()

    if args.action == "list" or args.action == "scan":
        print("🌐 龍魂生态准入 · 分发点扫描")
        print(f"   扫描时间: {datetime.now().isoformat()[:19]}")
        print()
        entries = embedder.list_entry_points()
        for e in entries:
            icon = "✅" if e["status"] == "已注入" else "🟡"
            print(f"   {icon} {e['path']} ({e['status']})")
        print(f"\n   总计: {len(entries)} 个分发点")
        injected = sum(1 for e in entries if e["status"] == "已注入")
        print(f"   已注入: {injected} · 待注入: {len(entries) - injected}")

    elif args.action == "inject":
        print("🌐 注入生态准入弹窗...")
        result = embedder.inject_all(dry_run=False)
        print(f"   已扫描: {result['scanned']}")
        print(f"   已注入: {result['injected']}")
        print(f"   已存在: {result['already_injected']}")
        print(f"   跳过: {result['skipped']}")
        if result['errors']:
            print(f"   错误: {len(result['errors'])}")
            for e in result['errors']:
                print(f"     ❌ {e}")

    elif args.action == "dry-run":
        print("🌐 预览注入（不实际修改文件）...")
        result = embedder.inject_all(dry_run=True)
        print(f"   将注入: {result['injected']} 个文件")
        print(f"   已存在: {result['already_injected']} 个文件")

    elif args.action == "generate-api":
        print(embedder.generate_api_handler())

    elif args.action == "generate-popup":
        popup_path = Path(__file__).parent / ".." / ".." / "10_PORTAL" / "eco-popup-standalone.html"
        popup_path.parent.mkdir(parents=True, exist_ok=True)
        popup_path.write_text(embedder.generate_standalone_popup_html(), encoding='utf-8')
        print(f"✅ 独立弹窗已生成: {popup_path}")


if __name__ == "__main__":
    main()
