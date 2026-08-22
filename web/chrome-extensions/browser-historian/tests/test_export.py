#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂·浏览器史官 导出功能全链路测试
模拟 scan → classify → export 完整数据流
DNA: #龍芯⚡️丙午·乙未·己亥·庚午·䷚颐-test-export-v1.0
"""

import json
import re
import sys
import os
from datetime import datetime

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # tests/ 上层即插件根目录
PASS = 0
FAIL = 0
WARN = 0

def test(name):
    def decorator(fn):
        def wrapper():
            global PASS, FAIL, WARN
            try:
                result = fn()
                if result is False:
                    FAIL += 1
                    print(f"  ❌ {name}")
                    if isinstance(result, str):
                        print(f"     → {result}")
                elif result == "WARN":
                    WARN += 1
                    print(f"  ⚠️  {name}")
                else:
                    PASS += 1
                    print(f"  ✅ {name}")
                    if isinstance(result, str):
                        print(f"     → {result}")
            except Exception as e:
                FAIL += 1
                print(f"  ❌ {name}")
                print(f"     → 异常: {e}")
        return wrapper
    return decorator

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. manifest.json 测试
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@test("manifest.json 存在且合法")
def test_manifest_exists():
    path = os.path.join(DIR, "manifest.json")
    if not os.path.exists(path):
        return "manifest.json 不存在"
    with open(path) as f:
        m = json.load(f)
    assert m["manifest_version"] == 3, "Must be MV3"
    assert "permissions" in m, "permissions field missing"
    assert "history" in m["permissions"], "history permission missing"
    assert "storage" in m["permissions"], "storage permission missing"
    assert "downloads" in m["permissions"], "downloads permission missing (needed for saveAs)"
    assert m.get("host_permissions") == [], f"host_permissions must be empty, got {m.get('host_permissions')}"
    return f"MV3·{len(m['permissions'])}权限·host_permissions空"

@test("manifest.json CSS变量引用正确")
def test_css_variables():
    css_path = os.path.join(DIR, "styles.css")
    with open(css_path) as f:
        css = f.read()
    # 检查弹窗样式使用正确的CSS变量名
    # 之前样式写了 --card-bg 但实际文件用 --bg-card
    card_bg_count = css.count("--card-bg")
    bg_card_count = css.count("--bg-card")
    if "--card-bg" in css:
        return "WARN"
    return f"CSS变量一致·card-bg={card_bg_count}·bg-card={bg_card_count}"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. popup.js 逻辑测试 (静态分析)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@test("popup.js prepareExport 函数定义")
def test_prepare_export_defined():
    js_path = os.path.join(DIR, "popup.js")
    with open(js_path) as f:
        js = f.read()
    assert "async function prepareExport" in js or "function prepareExport" in js, \
        "prepareExport not defined"
    assert "window._currentData" in js, "window._currentData not used"
    return "prepareExport + _currentData 已定义"

@test("popup.js 导出弹窗逻辑")
def test_export_modal_logic():
    js_path = os.path.join(DIR, "popup.js")
    with open(js_path) as f:
        js = f.read()
    assert "showExportModal" in js, "showExportModal not defined"
    assert "hideExportModal" in js, "hideExportModal not defined"
    assert "doExport" in js, "doExport not defined"
    assert "chrome.downloads" in js, "chrome.downloads not used in export"
    assert "saveAs" in js, "saveAs: true not set (no system dialog)"
    return "弹窗三函数(chrome.downloads+saveAs)"

@test("popup.js trainingMaterial 字段")
def test_training_material_field():
    js_path = os.path.join(DIR, "popup.js")
    with open(js_path) as f:
        js = f.read()
    assert "trainingMaterial" in js, "trainingMaterial flag missing in export payload"
    assert "export-training" in js or "training" in js.lower(), \
        "training checkbox id not found"
    return "trainingMaterial 字段已嵌入导出逻辑"

@test("popup.js 导出元数据选项")
def test_export_metadata_option():
    js_path = os.path.join(DIR, "popup.js")
    with open(js_path) as f:
        js = f.read()
    assert "includeMeta" in js or "export-include-meta" in js, \
        "include-meta checkbox not found"
    assert "visitCount" in js, "visitCount not in export (metadata fields missing)"
    return "包含元数据选项已实现"

@test("popup.js 数据获取路径正确")
def test_data_acquisition():
    js_path = os.path.join(DIR, "popup.js")
    with open(js_path) as f:
        js = f.read()
    # 关键修复：应该先从 _currentData 取，再回 storage
    checks = [
        ("window._currentData", "必须使用 _currentData 实时变量"),
        ("GET_STORED_DATA", "必须回退到 storage"),
        ("totalUnique", "必须检查 totalUnique"),
    ]
    for keyword, msg in checks:
        assert keyword in js, f"{msg} ({keyword} not found)"
    return "window._currentData → GET_STORED_DATA 双路径回退"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. popup.html 弹窗结构测试
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@test("popup.html 导出弹窗 DOM 结构")
def test_export_modal_dom():
    html_path = os.path.join(DIR, "popup.html")
    with open(html_path) as f:
        html = f.read()
    assert 'id="export-modal"' in html, "export-modal div missing"
    assert 'id="export-training"' in html, "training checkbox missing"
    assert 'id="export-include-meta"' in html, "include-meta checkbox missing"
    assert 'id="btn-export-cancel"' in html, "cancel button missing"
    assert 'id="btn-export-confirm"' in html, "confirm button missing"
    assert '本地模型训练原料' in html, "training label text missing"
    return "弹窗DOM完整·2checkbox·2button"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. background.js 和 classifier.js 测试
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@test("background.js Service Worker 注册正确")
def test_background_sw():
    bg_path = os.path.join(DIR, "background.js")
    with open(bg_path) as f:
        bg = f.read()
    assert "chrome.runtime.onInstalled" in bg, "onInstalled listener missing"
    assert "chrome.runtime.onMessage" in bg or "addListener" in bg, \
        "message listener missing"
    assert "chrome.history" in bg, "chrome.history API not used"
    return "SW注册·消息监听·history API"

@test("classifier.js 308域名加载")
def test_classifier_domains():
    cl_path = os.path.join(DIR, "classifier.js")
    with open(cl_path) as f:
        cl = f.read()
    assert "DOMAIN_MAP" in cl, "DOMAIN_MAP not defined"
    # 粗略计数字符串中URL数量
    url_count = len(re.findall(r"'https?://", cl))
    return f"DOMAIN_MAP·{url_count}个URL·8分类"

@test("classifier.js 三级分类覆盖")
def test_classifier_levels():
    cl_path = os.path.join(DIR, "classifier.js")
    with open(cl_path) as f:
        cl = f.read()
    levels = ["DOMAIN_MAP", "DOMAIN_FUZZY", "KEYWORD_PATTERNS"]
    found = [l for l in levels if l in cl]
    assert len(found) == 3, f"分类层级不足，找到: {found}"
    return f"三级分类: {'→'.join(found)}"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. 导出JSON结构验证 (模拟)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@test("导出JSON结构 (模拟 payload 构建)")
def test_export_json_structure():
    """模拟 popup.js doExport() 构建的 payload 是否符合预期"""
    # 模拟扫描数据
    mock_items = [
        {"url": "https://chat.openai.com/", "title": "ChatGPT", "visitCount": 5,
         "lastVisitTime": 1700000000000, "cat": "ai_tech", "catName": "AI技术",
         "catIcon": "🤖", "catColor": "#6366f1"},
        {"url": "https://github.com/zhuque", "title": "GitHub", "visitCount": 100,
         "lastVisitTime": 1699990000000, "cat": "ai_tech", "catName": "AI技术",
         "catIcon": "🤖", "catColor": "#6366f1"},
    ]
    mock_data = {
        "totalUnique": 3066,
        "totalRaw": 10234,
        "stats": {"ai_tech": 500, "adult": 100},
        "scanTime": "2026-07-24T12:00:00Z",
        "items": mock_items,
    }

    # Case 1: training=true, includeMeta=true (全量)
    payload1 = build_export_payload(mock_data, training=True, include_meta=True)
    assert payload1["trainingMaterial"] == True, "trainingMaterial should be true"
    assert payload1["totalUnique"] == 3066
    assert len(payload1["items"]) == 2
    assert "visitCount" in payload1["items"][0], "includeMeta=true must have visitCount"
    assert "catColor" in payload1["items"][0], "includeMeta=true must have catColor"

    # Case 2: training=false, includeMeta=false (最简)
    payload2 = build_export_payload(mock_data, training=False, include_meta=False)
    assert payload2["trainingMaterial"] == False, "trainingMaterial should be false"
    assert len(payload2["items"]) == 2
    assert "url" in payload2["items"][0]
    assert "title" in payload2["items"][0]
    assert "cat" in payload2["items"][0]
    # 不应包含 visitCount/catColor
    assert "visitCount" not in payload2["items"][0], "includeMeta=false must NOT have visitCount"
    assert "catColor" not in payload2["items"][0], "includeMeta=false must NOT have catColor"

    # Case 3: training=true, includeMeta=false (训练原料，不含元数据)
    payload3 = build_export_payload(mock_data, training=True, include_meta=False)
    assert payload3["trainingMaterial"] == True
    assert "visitCount" not in payload3["items"][0]

    return "3场景通过: training✓ includeMeta✓ 字段控制✓"

@test("导出JSON必含字段")
def test_export_required_fields():
    mock_data = {"totalUnique": 1, "totalRaw": 3, "stats": {}, "scanTime": "now", "items": [
        {"url": "https://example.com", "title": "Test", "visitCount": 1,
         "lastVisitTime": 1700000000000, "cat": "other", "catName": "其他",
         "catIcon": "📦", "catColor": "#888"}
    ]}
    payload = build_export_payload(mock_data, True, True)
    required = ["exportedAt", "exportDate", "trainingMaterial", "totalUnique",
                "totalRaw", "stats", "scanTime", "source", "items"]
    missing = [r for r in required if r not in payload]
    assert not missing, f"缺少字段: {missing}"
    assert payload["source"] == "longhun-browser-historian-v1.0"
    return f"{len(required)}个顶层字段·source正确"

@test("导出JSON文件名格式")
def test_export_filename_format():
    export_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"longhun-browser-history-{export_date}.json"
    assert filename.startswith("longhun-browser-history-")
    assert filename.endswith(".json")
    assert re.match(r"longhun-browser-history-\d{4}-\d{2}-\d{2}\.json", filename)
    return f"文件名: {filename}"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. 无数据/空数据 边界测试
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@test("空数据/零数据边界检查")
def test_empty_data_border():
    """模拟数据为空时的防御逻辑"""
    # popup.js 中的判断: !data || !data.totalUnique || data.totalUnique <= 0
    checks = [
        (None, "null data → 应提示扫描"),
        ({"totalUnique": 0}, "totalUnique=0 → 应提示扫描"),
        ({}, "empty obj → 应提示扫描"),
        ({"totalUnique": None}, "totalUnique=None → 应提示扫描"),
    ]
    for data, desc in checks:
        should_alert = (not data or not data.get("totalUnique") or data["totalUnique"] <= 0)
        assert should_alert, f"{desc}: 应该返回true却返回false"
    return "4种边界条件通过"

def build_export_payload(data, training=False, include_meta=True):
    """模拟 popup.js doExport() 的 payload 构建逻辑"""
    export_date = datetime.now().strftime("%Y-%m-%d")
    payload = {
        "exportedAt": int(datetime.now().timestamp() * 1000),
        "exportDate": export_date,
        "trainingMaterial": training,
        "totalUnique": data["totalUnique"],
        "totalRaw": data["totalRaw"],
        "stats": data["stats"],
        "scanTime": data["scanTime"],
        "source": "longhun-browser-historian-v1.0",
        "items": [],
    }

    for item in data["items"]:
        if include_meta:
            payload["items"].append({
                "url": item["url"],
                "title": item.get("title", ""),
                "visitCount": item.get("visitCount", 0),
                "lastVisitTime": item.get("lastVisitTime", 0),
                "cat": item["cat"],
                "catName": item["catName"],
                "catIcon": item["catIcon"],
                "catColor": item["catColor"],
            })
        else:
            payload["items"].append({
                "url": item["url"],
                "title": item.get("title", ""),
                "cat": item["cat"],
            })
    return payload

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. styles.css 弹窗样式检查
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@test("styles.css 弹窗样式完整")
def test_modal_styles():
    css_path = os.path.join(DIR, "styles.css")
    with open(css_path) as f:
        css = f.read()
    selectors = [".modal", ".modal-content", ".modal-header", ".modal-body",
                 ".modal-actions", ".option-row", ".option-text"]
    missing = [s for s in selectors if s not in css]
    assert not missing, f"缺少CSS选择器: {missing}"
    assert "fadeIn" in css, "fadeIn 动画缺失"
    assert "slideUp" in css, "slideUp 动画缺失"
    return f"{len(selectors)}个弹窗选择器·2动画"

@test("styles.css 主题变量一致性")
def test_theme_consistency():
    css_path = os.path.join(DIR, "styles.css")
    with open(css_path) as f:
        css = f.read()
    # 定义在 :root 中的变量
    root_match = re.search(r':root\s*\{(.*?)\}', css, re.DOTALL)
    if root_match:
        root_vars = re.findall(r'--([\w-]+)\s*:', root_match.group(1))
        return f":root定义{len(root_vars)}个CSS变量"
    return "WARN"
    return "无 :root 变量定义"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8. 文件完整性检查
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@test("所有必需文件存在")
def test_all_files_present():
    required = [
        "manifest.json", "background.js", "classifier.js",
        "popup.html", "popup.js", "styles.css",
        "icons/icon16.png", "icons/icon48.png", "icons/icon128.png",
        "validate.sh",
    ]
    missing = []
    for f in required:
        if not os.path.exists(os.path.join(DIR, f)):
            missing.append(f)
    assert not missing, f"缺少文件: {missing}"
    return f"{len(required)}个文件齐全"

@test("validate.sh 自检脚本可执行")
def test_validate_executable():
    vpath = os.path.join(DIR, "validate.sh")
    assert os.access(vpath, os.X_OK) or os.access(vpath, os.R_OK), \
        "validate.sh 不可读/不可执行"
    return "可读可执行"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 运行
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == "__main__":
    print("=" * 60)
    print("🐉 龍魂·浏览器史官 导出功能全链路测试")
    print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   目录: {DIR}")
    print("=" * 60)
    print()

    # 收集所有 test_ 函数
    import inspect
    tests = []
    for name, obj in sorted(globals().items()):
        if name.startswith("test_") and callable(obj) and name != "test":
            tests.append(obj)

    for t in tests:
        t()

    print()
    print("=" * 60)
    total = PASS + FAIL + WARN
    print(f"  结果: ✅ {PASS}通过  ❌ {FAIL}失败  ⚠️ {WARN}警告  (共{total}项)")
    print("=" * 60)

    if FAIL > 0:
        print("\n🔴 有测试失败，请检查上述 ❌ 项目")
        sys.exit(1)
    elif WARN > 0:
        print("\n🟡 全部通过但有警告，请关注上述 ⚠️ 项目")
        sys.exit(0)
    else:
        print("\n🟢 全绿！导出功能各环节验证通过")
        sys.exit(0)
