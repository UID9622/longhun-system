#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·井-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""华为云自动创建AK/SK — 一步到位"""
import asyncio, json, re, sys, time
from pathlib import Path
from playwright.async_api import async_playwright

CRED_FILE = Path.home() / ".longhun/huawei-credentials.json"
IAM_URL = "https://console.huaweicloud.com/iam/#/mine/accessKey"

def log(msg):
    print(msg, flush=True)

async def main():
    log("[1] 启动Chromium浏览器...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        ctx = await browser.new_context(accept_downloads=True)
        page = await ctx.new_page()
        
        await page.goto(IAM_URL, wait_until="domcontentloaded")
        log("[2] 浏览器已打开华为云IAM凭证页")
        log(">>> 请手动登录华为云（需要验证码的话手动输入）")
        log(">>> 登录成功后脚本会全自动创建AK/SK")
        log(">>> 最多等待 5 分钟...")
        
        # 等登录：监测"新增访问密钥"按钮
        for i in range(60):
            await asyncio.sleep(5)
            try:
                btn = page.locator("text=新增访问密钥")
                if await btn.count() > 0 and await btn.first.is_visible():
                    log("[3] 检测到已登录，开始自动创建AK/SK...")
                    break
            except:
                pass
            if i % 6 == 0:
                log(f"   等待登录中... ({i*5}s)")
        else:
            log("❌ 超时，未检测到登录")
            await browser.close()
            return
        
        # 点击"新增访问密钥"
        try:
            await page.locator("text=新增访问密钥").first.click()
            await asyncio.sleep(1.5)
        except Exception as e:
            log(f"点击失败: {e}")
        
        # 可能会有二次确认弹窗
        try:
            # 各种可能的确认按钮
            for sel in ["button:has-text('确定')", "button:has-text('确认')", 
                        ".btn-confirm", "[class*='confirm']"]:
                try:
                    confirm = page.locator(sel).first
                    if await confirm.is_visible(timeout=2000):
                        await confirm.click()
                        log("   已点确认")
                        await asyncio.sleep(2)
                        break
                except:
                    continue
        except:
            pass
        
        # 等待密钥显示
        await asyncio.sleep(2)
        
        # 提取AK/SK
        ak, sk = None, None
        page_text = await page.content()
        
        # 方法1: 页面文本正则
        ak_pat = re.search(r'(?:Access[_\s]*Key[_\s]*(?:Id|ID)?|AK)[:\s]*([A-Za-z0-9]{15,50})', page_text)
        sk_pat = re.search(r'(?:Secret[_\s]*(?:Access[_\s]*)?Key|SK)[:\s]*([A-Za-z0-9/+]{30,60})', page_text)
        
        if ak_pat and sk_pat:
            ak, sk = ak_pat.group(1), sk_pat.group(1)
        else:
            # 方法2: 检查下载
            dl_dir = Path.home() / "Downloads"
            csvs = sorted(dl_dir.glob("credentials*.csv"), key=lambda x: x.stat().st_mtime, reverse=True)
            if csvs:
                log(f"   从下载读取: {csvs[0].name}")
                content = csvs[0].read_text()
                lines = content.strip().split('\n')
                if len(lines) >= 2:
                    headers = lines[0].split(',')
                    values = lines[1].split(',')
                    for h, v in zip(headers, values):
                        h_lower = h.strip().lower()
                        if 'access' in h_lower and 'key' in h_lower:
                            ak = v.strip()
                        if 'secret' in h_lower:
                            sk = v.strip()
        
        if ak and sk:
            log(f"\n{'='*50}")
            log(f"AK: {ak}")
            log(f"SK: {sk}")
            log(f"{'='*50}")
            
            CRED_FILE.parent.mkdir(parents=True, exist_ok=True)
            cred_data = {
                "access_key": {"id": ak, "secret": sk},
                "project": "cn-north-4",
                "region": "cn-north-4"
            }
            CRED_FILE.write_text(json.dumps(cred_data, indent=2, ensure_ascii=False))
            log(f"\n✅ 凭证已保存: {CRED_FILE}")
            
            # 立即开端口
            log("\n[4] 开放安全组 TCP 7000...")
            proc = await asyncio.create_subprocess_exec(
                "python3", str(Path(__file__).parent.parent / "deploy/huawei_open_frp_port.py"),
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            log(stdout.decode())
            if stderr:
                log(stderr.decode())
        else:
            log("\n⚠️ 自动提取失败，尝试截图...")
            await page.screenshot(path=str(Path.home() / ".longhun/huawei_aksk_result.png"))
            log(f"请查看截图或把AK/SK贴给我: {Path.home()}/.longhun/huawei_aksk_result.png")
            log("手动复制后输入 AK 和 SK:")
            ak = input("AK: ").strip()
            sk = input("SK: ").strip()
            if ak and sk:
                cred_data = {
                    "access_key": {"id": ak, "secret": sk},
                    "project": "cn-north-4", "region": "cn-north-4"
                }
                CRED_FILE.write_text(json.dumps(cred_data, indent=2, ensure_ascii=False))
                log(f"✅ 已手动保存")
        
        log("\n[5] 5秒后自动关闭浏览器...")
        await asyncio.sleep(5)
        await browser.close()
        log("完成！")

asyncio.run(main())
