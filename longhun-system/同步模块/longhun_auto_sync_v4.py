def asset_proof_workflow(file_path: str):
    """数字资产龙骨证据链·四步闭环·乔前辈出品"""
    import subprocess
    import platform
    import time
    from pathlib import Path

    GPG_FINGERPRINT = 'A2D0092CEE2E5BA87035600924C3704A8CC26D5F'
    CONFIRM_CODE = '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z'

    fn = Path(file_path)
    if not fn.exists():
        print(f"🔴 文件不存在: {file_path}")
        return

    # ── 第一步：本地时间戳 ──
    stat = fn.stat()
    ctime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_ctime))
    mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_mtime))

    print(f"\n{'='*60}")
    print(f"🗂️  文件路径: {fn.resolve()}")
    print(f"📅 创建时间: {ctime}")
    print(f"📝 修改时间: {mtime}")
    print(f"⚙️  文件大小: {stat.st_size} 字节")
    print(f"{'='*60}")

    # ── 第二步：授时状态检查 ──
    sys_plat = platform.system()
    print(f"\n🌏 当前平台: {sys_plat}")

    if sys_plat == 'Darwin':
        print("⏰ 检查Mac授时状态...")
        try:
            result = subprocess.run(
                ['sntp', '-v', 'time.apple.com'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                print("🟢 NTP授时正常（Apple时间服务器）")
            else:
                print("🟡 建议：[系统设置→日期与时间→自动设置] 打开")
        except Exception:
            print("🟡 建议：[系统设置→日期与时间→自动设置] 打开，推荐北斗/GPS校准")

    elif sys_plat == 'Linux':
        print("⏰ 检查Linux授时状态...")
        try:
            result = subprocess.run(
                ['timedatectl', 'status'],
                capture_output=True, text=True, timeout=5
            )
            if 'NTP service: active' in result.stdout or 'synchronized: yes' in result.stdout:
                print("🟢 NTP授时已激活")
            else:
                print("🟡 建议运行：sudo timedatectl set-ntp true")
        except Exception:
            print("🟡 建议：[设置→日期和时间→自动设置] 打开")

    else:
        print("🟡 请手动确认系统时间已与网络同步（推荐北斗/GPS授时）")

    # ── 第三步：GPG签名 ──
    asc_file = fn.with_suffix(fn.suffix + '.asc')
    print(f"\n🔑 正在生成GPG签名: {asc_file.name}")
    try:
        result = subprocess.run(
            ['gpg', '--armor', '--detach-sign', str(fn)],
            capture_output=True, text=True
        )
        if result.returncode == 0 and asc_file.exists():
            print(f"✅ GPG签名成功: {asc_file}")
            # 顺手验证一下
            verify = subprocess.run(
                ['gpg', '--verify', str(asc_file), str(fn)],
                capture_output=True, text=True
            )
            if verify.returncode == 0:
                print("🟢 签名验证通过")
            else:
                print("🟡 签名已生成，验证异常，请手动确认")
        else:
            print(f"🔴 GPG签名失败: {result.stderr.strip()}")
            print("💡 提示：先运行 gpg --list-secret-keys 确认密钥存在")
    except FileNotFoundError:
        print("🔴 未找到 gpg 命令 → Mac请运行: brew install gnupg")
    except Exception as e:
        print(f"🔴 签名异常: {e}")

    # ── 第四步：标准明细模板 + 备份提醒 ──
    print(f"\n{'='*60}")
    print("📋 标准数字资产明细模板")
    print(f"{'='*60}")
    print(f"文件名    : {fn.name}")
    print(f"创建时间  : {ctime}")
    print(f"修改时间  : {mtime}")
    print(f"GPG指纹   : {GPG_FINGERPRINT}")
    print(f"签名文件  : {asc_file.name}")
    print(f"确认码    : {CONFIRM_CODE}")
    print(f"备份状态  : ⏳ 待备份")
    print(f"{'='*60}")
    print(f"\n☁️  备份提醒:")
    print(f"   请将以下两个文件一同上传华为云空间/网盘:")
    print(f"   ① {fn.name}")
    print(f"   ② {asc_file.name}")
    print(f"\n🐉 数字龙骨证据链闭环完成！\n")

