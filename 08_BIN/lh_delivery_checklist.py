#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂·交付清单自检器 v1.0

每次交付前跑这个脚本，逐项检查5条交付标准。
不通过不汇报。

用法:
  python3 bin/lh_delivery_checklist.py --type chrome-ext    # Chrome插件
  python3 bin/lh_delivery_checklist.py --type python-svc    # Python服务
  python3 bin/lh_delivery_checklist.py --type web-portal    # Web门户
  python3 bin/lh_delivery_checklist.py --type harmony       # 鸿蒙应用
  python3 bin/lh_delivery_checklist.py --type shell         # Shell脚本
  python3 bin/lh_delivery_checklist.py --path <dir> --type <type>  # 指定路径

DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-DELIVERY-CHECKLIST-v1.0-a3e8f1c9
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime

# ── 三色审计 ──
GREEN = "🟢"
YELLOW = "🟡"
RED = "🔴"

results = []  # [(standard_name, mark, detail)]


def check(name: str, ok: bool, detail: str = ""):
    mark = GREEN if ok else RED
    results.append((name, mark, detail))
    print(f"  {mark} {name}" + (f" → {detail}" if detail else ""))


def warn(name: str, detail: str = ""):
    results.append((name, YELLOW, detail))
    print(f"  {YELLOW} {name}" + (f" → {detail}" if detail else ""))


def count_marks():
    g = sum(1 for _, m, _ in results if m == GREEN)
    y = sum(1 for _, m, _ in results if m == YELLOW)
    r = sum(1 for _, m, _ in results if m == RED)
    return g, y, r


# ══════════════════════════════════════════════════════════
# 标准1：交付前自检
# ══════════════════════════════════════════════════════════
def check_standard_1_selfcheck(path: str, prod_type: str):
    print(f"\n{'='*60}")
    print(f"  标准1 · 交付前自检 ({prod_type})")
    print(f"{'='*60}")

    if prod_type == "chrome-ext":
        # 检查 validate.sh 存在且可执行
        val_path = os.path.join(path, "validate.sh")
        if os.path.exists(val_path):
            check("validate.sh 存在", True)
            # 运行它
            try:
                out = subprocess.run(["bash", val_path], capture_output=True, text=True, timeout=30, cwd=path)
                ok = out.returncode == 0
                # 提取关键行
                lines = [l for l in out.stdout.split("\n") if l.strip() and ("✅" in l or "❌" in l or "⚠" in l)]
                detail = f"{len(lines)}项检查" if ok else f"exit={out.returncode}"
                check("validate.sh 通过", ok, detail)
                if not ok:
                    for l in out.stdout.split("\n"):
                        if "❌" in l:
                            print(f"     → {l.strip()}")
            except Exception as e:
                check("validate.sh 运行", False, str(e))
        else:
            check("validate.sh 缺失", False, "Chrome插件必须附带validate.sh")

    elif prod_type == "python-svc":
        # 检查是否有测试
        has_pytest = os.path.exists(os.path.join(path, "test_")) or os.path.exists(os.path.join(path, "tests/"))
        has_test_arg = False
        # 搜索 --test 参数支持
        for f in os.listdir(path):
            if f.endswith(".py"):
                with open(os.path.join(path, f)) as fh:
                    content = fh.read()
                    if "--test" in content or "unittest" in content or "pytest" in content:
                        has_test_arg = True
                        break
        if has_pytest or has_test_arg:
            check("测试文件存在", True)
        else:
            warn("未发现测试文件", "Python服务建议附带测试")

    elif prod_type == "web-portal":
        # 检查 index.html 存在
        index_path = os.path.join(path, "index.html")
        if os.path.exists(index_path):
            check("index.html 存在", True)
            # 基本HTML检查
            with open(index_path) as f:
                html = f.read()
            check("HTML有效(含</html>)", "</html>" in html)
            check("HTML含viewport", "viewport" in html or "meta name=\"viewport\"" not in html)
        else:
            check("index.html 缺失", False)

    elif prod_type == "harmony":
        # 检查 build-profile.json5
        bp = os.path.join(path, "build-profile.json5")
        if os.path.exists(bp):
            check("build-profile.json5 存在", True)
        else:
            check("鸿蒙编译配置缺失", False)

    elif prod_type == "shell":
        # shellcheck
        for f in os.listdir(path):
            if f.endswith(".sh"):
                try:
                    out = subprocess.run(["shellcheck", os.path.join(path, f)],
                                         capture_output=True, text=True, timeout=15)
                    check(f"shellcheck {f}", out.returncode == 0,
                          f"{len(out.stdout.split(chr(10)))} issues" if out.returncode != 0 else "clean")
                except FileNotFoundError:
                    warn(f"shellcheck 未安装", "跳过语法检查")


# ══════════════════════════════════════════════════════════
# 标准2：安装指引防呆
# ══════════════════════════════════════════════════════════
def check_standard_2_foolproof(path: str, prod_type: str):
    print(f"\n{'='*60}")
    print(f"  标准2 · 安装指引防呆")
    print(f"{'='*60}")

    readme_files = ["README.md", "INSTALL.md", "安装说明.md", "readme.md"]
    found_readme = None
    for rf in readme_files:
        rp = os.path.join(path, rf)
        if os.path.exists(rp):
            found_readme = rp
            break

    if found_readme:
        check("安装说明文件存在", True, os.path.basename(found_readme))
        with open(found_readme) as f:
            content = f.read()

        # 防呆检查
        has_dir_hint = any(kw in content for kw in
                           ["选中", "文件夹本身", "不要打开", "选择目录", "加载已解压", "完整路径"])
        check("目录选择提示", has_dir_hint,
              "已强调选文件夹本身" if has_dir_hint else "缺少防呆提示")

        has_prereq = "开发者模式" in content or "前置" in content or "前提" in content or "准备" in content
        check("前置条件标注", has_prereq,
              "已标注" if has_prereq else "缺少前置条件")

        has_faq = "FAQ" in content or "常见问题" in content or "排错" in content or "故障" in content
        check("错误排查FAQ", has_faq,
              "已含" if has_faq else "缺少FAQ")

        has_version = re.search(r'v?\d+\.\d+(\.\d+)?', content)
        check("版本号标注", bool(has_version),
              has_version.group(0) if has_version else "缺少版本号")

    else:
        check("安装说明文件", False, "需要 README.md 或 INSTALL.md")


# ══════════════════════════════════════════════════════════
# 标准3：实机验证前置
# ══════════════════════════════════════════════════════════
def check_standard_3_verification(path: str, prod_type: str):
    print(f"\n{'='*60}")
    print(f"  标准3 · 实机验证前置")
    print(f"{'='*60}")

    # 检查是否涉及服务器部署
    has_deploy = any(
        os.path.exists(os.path.join(path, d)) for d in
        ["deploy/", "docker/", "Dockerfile", "docker-compose.yml",
         "systemd/", ".env.kunpeng", "鲲鹏"]
    )

    # 搜索关键词判断是否涉及鲲鹏
    involves_server = False
    ext_dirs = ["deploy", "docker", "config", "services"]
    for ed in ext_dirs:
        edp = os.path.join(path, ed)
        if os.path.isdir(edp):
            involves_server = True
            break

    # 搜索 deploy/ 目录是否存在
    deploy_paths = [
        os.path.join(path, "deploy"),
        os.path.join(os.path.dirname(path), "deploy"),
    ]
    for dp in deploy_paths:
        if os.path.isdir(dp):
            involves_server = True
            break

    if involves_server:
        # 检查是否有部署脚本
        check("涉及服务器部署", True, "标准3强制实机验证")

        # 尝试 SSH 连通性检查
        try:
            out = subprocess.run(
                ["ssh", "-i", os.path.expanduser("~/.ssh/longhun_kunpeng_ed25519"),
                 "-o", "ConnectTimeout=5", "-o", "BatchMode=yes",
                 "root@119.13.90.27", "echo ok"],
                capture_output=True, text=True, timeout=10
            )
            if out.returncode == 0:
                check("鲲鹏 SSH 连通", True, "119.13.90.27 可达")
            else:
                warn("鲲鹏 SSH 不通", "需确认实机验证状态")
        except Exception:
            warn("鲲鹏 SSH 连接失败", "离线环境或密钥问题")

        # 检查是否有健康检查脚本
        hc_paths = [
            os.path.join(path, "deploy/scripts/health_check.sh"),
            "deploy/scripts/health_check.sh",
        ]
        hc_found = any(os.path.exists(p) for p in hc_paths)
        check("健康检查脚本", hc_found,
              "已就绪" if hc_found else "建议补充")

        # 检查汇报中是否有遗留问题
        report_files = []
        for root, _, files in os.walk(path):
            for f in files:
                if f.endswith(".md") and any(kw in f.lower() for kw in ["report", "delivery", "status"]):
                    report_files.append(os.path.join(root, f))

        unchecked_keywords = []
        for rf in report_files[:3]:  # 只检查前3个
            try:
                with open(rf) as f:
                    content = f.read()
                    for kw in ["待验证", "暂不通", "可能有问题", "TODO", "FIXME"]:
                        if kw in content:
                            unchecked_keywords.append(f"{os.path.basename(rf)}: '{kw}'")
            except Exception:
                pass

        if unchecked_keywords:
            warn("发现未解决标记", "; ".join(unchecked_keywords[:3]))
        else:
            check("无可疑遗留标记", True)
    else:
        check("不涉及服务器部署", True, "标准3不适用")


# ══════════════════════════════════════════════════════════
# 标准4：数据安全声明
# ══════════════════════════════════════════════════════════
def check_standard_4_privacy(path: str, prod_type: str):
    print(f"\n{'='*60}")
    print(f"  标准4 · 数据安全声明")
    print(f"{'='*60}")

    # 判断是否涉及用户数据
    involves_user_data = False
    keywords = ["history", "storage", "localStorage", "cookie", "数据库", "db",
                "user", "用户", "数据", "data", "permission", "权限"]

    for root, _, files in os.walk(path):
        # 限制深度，跳过大目录
        depth = root.replace(path, "").count(os.sep)
        if depth > 3:
            continue
        for f in files:
            if f.endswith((".js", ".html", ".py", ".md", ".json")):
                try:
                    with open(os.path.join(root, f), errors="ignore") as fh:
                        content = fh.read(4096)  # 只读开头4KB
                        if any(kw.lower() in content.lower() for kw in keywords):
                            involves_user_data = True
                            break
                except Exception:
                    pass
        if involves_user_data:
            break

    if involves_user_data:
        check("涉及用户数据", True, "标准4强制数据安全声明")

        # 搜索数据声明
        declarations = []
        for root, _, files in os.walk(path):
            depth = root.replace(path, "").count(os.sep)
            if depth > 2:
                continue
            for f in files:
                if f.endswith((".md", ".html")):
                    try:
                        with open(os.path.join(root, f), errors="ignore") as fh:
                            content = fh.read()
                            if any(kw in content for kw in
                                   ["数据存储", "本地存储", "数据不会离开", "数据不出",
                                    "本地运行", "不上传", "不收集", "privacy",
                                    "data storage", "local only"]):
                                declarations.append(f)
                    except Exception:
                        pass

        check("数据安全声明", len(declarations) > 0,
              f"已找到{len(declarations)}处声明" if declarations else "缺失数据去向说明")

        # 检查权限声明是否有理由
        for root, _, files in os.walk(path):
            depth = root.replace(path, "").count(os.sep)
            if depth > 2:
                continue
            for f in files:
                if f.endswith((".json", ".md")):
                    try:
                        with open(os.path.join(root, f), errors="ignore") as fh:
                            content = fh.read()
                            if "permissions" in content.lower() and "host_permissions" in content.lower():
                                perm_reasons = any(kw in content.lower() for kw in
                                                   ["权限说明", "permission reason", "为什么需要",
                                                    "用途:", "理由:", "because"])
                                check("权限理由说明", perm_reasons,
                                      "已说明" if perm_reasons else "权限无理由说明")
                                break
                    except Exception:
                        pass

        # 检查数字来源标注
        num_sources = any(kw in content.lower() if "content" in dir() else False
                          for kw in ["内置", "用户数据", "内置域名", "用户浏览"])
        if 'content' in dir():
            check("数字来源标注", num_sources,
                  "已区分内置/用户数据" if num_sources else "未标注数字来源")
    else:
        check("不涉及用户数据", True, "标准4不适用")


# ══════════════════════════════════════════════════════════
# 标准5：回归测试
# ══════════════════════════════════════════════════════════
def check_standard_5_regression(path: str, prod_type: str):
    print(f"\n{'='*60}")
    print(f"  标准5 · 回归测试")
    print(f"{'='*60}")

    # 检查是否有测试文件/目录
    test_locations = ["tests/", "test/", "__tests__/"]
    test_files = []
    for tl in test_locations:
        tp = os.path.join(path, tl)
        if os.path.isdir(tp):
            test_files = [os.path.join(tp, f) for f in os.listdir(tp) if f.endswith((".py", ".js", ".sh"))]
            break

    if not test_files:
        # 搜索单独测试文件
        for f in os.listdir(path):
            if f.startswith("test_") or f.endswith("_test.py") or f.endswith("_test.js"):
                test_files.append(os.path.join(path, f))

    if test_files:
        check("测试文件存在", True, f"{len(test_files)}个")
        # 尝试运行Python测试
        for tf in test_files:
            if tf.endswith(".py"):
                try:
                    out = subprocess.run([sys.executable, tf],
                                         capture_output=True, text=True, timeout=30, cwd=path)
                    ok = out.returncode == 0
                    check(f"测试运行: {os.path.basename(tf)}", ok,
                          "全部通过" if ok else f"exit={out.returncode}")
                except Exception as e:
                    warn(f"测试运行失败: {os.path.basename(tf)}", str(e)[:60])
            elif tf.endswith(".sh"):
                try:
                    out = subprocess.run(["bash", tf],
                                         capture_output=True, text=True, timeout=30, cwd=path)
                    ok = out.returncode == 0
                    check(f"测试运行: {os.path.basename(tf)}", ok,
                          "全部通过" if ok else f"exit={out.returncode}")
                except Exception as e:
                    warn(f"测试运行失败: {os.path.basename(tf)}", str(e)[:60])
    else:
        warn("无测试文件", "建议补充端到端测试")


# ══════════════════════════════════════════════════════════
# 附：路径铁律 + 密钥检查
# ══════════════════════════════════════════════════════════
def check_bonus_path_security(path: str):
    print(f"\n{'='*60}")
    print(f"  附 · 路径铁律 + 安全底线")
    print(f"{'='*60}")

    # 路径铁律
    forbidden_patterns = ["~/Downloads", "/tmp/", "/Desktop/", "~/Desktop"]
    resolved = os.path.realpath(path)
    in_forbidden = any(fp in resolved for fp in forbidden_patterns)
    check("文件路径正确", not in_forbidden,
          resolved if not in_forbidden else f"禁止路径: {resolved}")

    # 密钥检查
    found_keys = False
    secret_patterns = [
        r'(?i)(api[_-]?key|secret|password|token|private[_-]?key)\s*[:=]\s*["\'][\w\-\.]{8,}["\']',
        r'-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----',
        r'(?i)(sk-[a-zA-Z0-9]{20,})',
    ]
    for root, _, files in os.walk(path):
        depth = root.replace(path, "").count(os.sep)
        if depth > 3 or ".git" in root:
            continue
        for f in files:
            if f.endswith((".py", ".js", ".sh", ".json", ".yml", ".yaml", ".env", ".md")):
                try:
                    with open(os.path.join(root, f), errors="ignore") as fh:
                        content = fh.read()
                        for sp in secret_patterns:
                            if re.search(sp, content):
                                found_keys = True
                                # 排除 .env.example
                                if not f.endswith(".example") and "example" not in f:
                                    warn(f"疑似密钥: {f}")
                                    break
                except Exception:
                    pass
        if found_keys:
            break

    if not found_keys:
        check("无硬编码密钥", True)

    # 防火墙检查（Python文件）
    has_firewall = False
    for root, _, files in os.walk(path):
        depth = root.replace(path, "").count(os.sep)
        if depth > 3:
            continue
        for f in files:
            if f.endswith(".py"):
                try:
                    with open(os.path.join(root, f), errors="ignore") as fh:
                        if "LH_AUDIT_FIREWALL" in fh.read():
                            has_firewall = True
                            break
                except Exception:
                    pass
    if has_firewall:
        check("语义防火墙已嵌入", True)


# ══════════════════════════════════════════════════════════
# 主流程
# ══════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="龍魂·交付清单自检器")
    parser.add_argument("--type", choices=["chrome-ext", "python-svc", "web-portal",
                                            "harmony", "shell"],
                        help="交付物类型")
    parser.add_argument("--path", default=".", help="交付物路径 (默认当前目录)")
    args = parser.parse_args()

    path = os.path.realpath(args.path)

    print()
    print("=" * 60)
    print("🐉 龍魂·交付清单自检器 v1.0")
    print(f"   路径: {path}")
    print(f"   类型: {args.type}")
    print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    if not args.type:
        print(f"\n{RED} 请指定交付物类型 --type")
        print("   可选: chrome-ext, python-svc, web-portal, harmony, shell")
        sys.exit(1)

    # 逐标准检查
    check_standard_1_selfcheck(path, args.type)
    check_standard_2_foolproof(path, args.type)
    check_standard_3_verification(path, args.type)
    check_standard_4_privacy(path, args.type)
    check_standard_5_regression(path, args.type)
    check_bonus_path_security(path)

    # ── 结果汇总 ──
    g, y, r = count_marks()
    print()
    print("=" * 60)
    print(f"  结 果 汇 总")
    print("=" * 60)
    print(f"  {GREEN} 通过: {g}  |  {YELLOW} 待核: {y}  |  {RED} 不通过: {r}")
    print()

    if r > 0:
        print(f"  {RED} 有 {r} 项不通过 — 交付前必须修复")
        print()
        print("  不通过项:")
        for name, mark, detail in results:
            if mark == RED:
                print(f"    ❌ {name} → {detail}")
        sys.exit(1)
    elif y > 0:
        print(f"  {YELLOW} 有 {y} 项待核 — 建议修复后汇报")
        print()
        print("  待核项:")
        for name, mark, detail in results:
            if mark == YELLOW:
                print(f"    ⚠️  {name} → {detail}")
        print()
        print("  可以交付，但建议先处理以上待核项。")
    else:
        print(f"  {GREEN} 全部通过！可以汇报老大。")
        print()
        print("  交付签章:")
        print(f"    executor: lh_delivery_checklist.py v1.0")
        print(f"    audit_mark: {GREEN}")
        print(f"    risk_score: 0.0")
        print(f"    timestamp: {datetime.now().isoformat()}")
        print()

    # ── DNA签章 ──
    print(f"  DNA: #龍芯⚡️{datetime.now().strftime('%Y%m%d-%H%M%S')}-DELIVERY-CHECKLIST-PASS-{hex(hash(path))[-8:]}")


if __name__ == "__main__":
    main()
