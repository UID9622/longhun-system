# 🛡️ 龍魂自检值班表 v1.0｜监听·审计·回执·复盘 — 谁干·多久·失职怎么办

> Notion URL: https://app.notion.com/p/v1-0-4efcfc980eb644d4bede1c9edb0f105f
> Created: 2026-06-04T18:57:00.000Z
> Last edited: 2026-07-15T23:42:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
## 一、👁️ 人格值班表(谁干·多久·交不出回执怎么办)
按你《五大后台自运行人格配置中心 v3.1》真实职责派工,不另造名字。
## 二、🔍 自检能力差距表(现在的花架子 vs 真自检)
## 三、🛠️ 要补的自检函数(longhun_self_check_v1.0.py 骨架)
真测量,不是打印漂亮横幅。建议 P04 鲁班落地:
```python
#!/usr/bin/env python3
# DNA: #龍芯⚡️2026-06-05-SELF-CHECK-v1.0  责任:UID9622·不免责
import subprocess, sqlite3, json, sys
from pathlib import Path

class SelfCheck:
    """真·自检:每条结论必须有证据,否则降级。禁止硬编码分数。"""
    def __init__(self): self.results = []   # (name, color, evidence)

    def _rec(self, name, ok, evidence, warn=False):
        color = "🟢" if ok else ("🟡" if warn else "🔴")
        self.results.append((name, color, str(evidence)[:300]))

    # 1) 文件真存在(不是 print ✅)
    def check_files(self, files):
        for f in files:
            p = Path(f)
            self._rec(f"file:{f}", p.exists(), f"size={p.stat().st_size if p.exists() else 0}")

    # 2) DB 真能连 + 真有行(戳破"空表实时监控")  —— P05
    def check_db_heartbeat(self, db, table):
        try:
            c = sqlite3.connect(db); n = c.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]; c.close()
            self._rec(f"db:{table}", n > 0, f"rows={n}", warn=(n == 0))  # 0行=🟡,不准说"运行中"
        except Exception as e:
            self._rec(f"db:{table}", False, e)

    # 3) 依赖安全自扫(能逮住那 72 个洞)  —— P04
    def check_security(self):
        r = subprocess.run(["pip-audit", "-f", "json"], capture_output=True, text=True)
        try: vulns = len(json.loads(r.stdout or "[]"))
        except Exception: vulns = -1
        self._rec("security:pip-audit", vulns == 0, f"vulns={vulns}", warn=(vulns > 0))

    # 4) DNA 哈希链完整性(口号变校验)  —— P06
    def check_dna_chain(self, db):
        try:
            c = sqlite3.connect(db)
            rows = c.execute("SELECT prev_hash,hash FROM dna_chain ORDER BY id").fetchall(); c.close()
            prev = None; ok = True
            for ph, h in rows:
                if prev is not None and ph != prev: ok = False; break
                prev = h
            self._rec("dna_chain", ok, f"len={len(rows)} linked={ok}")
        except Exception as e:
            self._rec("dna_chain", False, e)

    # 5) 测试真跑(不是写"100%")  —— P04
    def check_tests(self):
        r = subprocess.run(["pytest", "-q"], capture_output=True, text=True)
        last = r.stdout.strip().splitlines()[-1] if r.stdout else r.stderr[:200]
        self._rec("tests:pytest", r.returncode == 0, last)

    # 6) 诚实度自审:扫自己输出里的禁词  —— P05
    def check_honesty(self, text):
        banned = ["100/100", "99.9%", "永久", "永不", "实时监控已启动"]
        hits = [w for w in banned if w in text]
        self._rec("honesty", not hits, f"无证据禁词={hits}", warn=bool(hits))

    def report(self):
        red = [r for r in self.results if r[1] == "🔴"]
        yellow = [r for r in self.results if r[1] == "🟡"]
        print("─── 自检复盘 ───")
        for n, c, e in self.results: print(f"{c} {n} :: {e}")
        verdict = "🔴 熔断" if red else ("🟡 待审" if yellow else "🟢 通行")
        print(f"裁决:{verdict}  🟢{len(self.results)-len(red)-len(yellow)}/🟡{len(yellow)}/🔴{len(red)}")
        sys.exit(1 if red else 0)   # 红就让 CI / pre-push 失败

if __name__ == "__main__":
    sc = SelfCheck()
    sc.check_files(["longhun_mvp_executor_v1.0.py", "longhun_mvp_launcher_v1.0.py"])
    sc.check_db_heartbeat(str(Path.home()/".龍魂/kfpp/kfpp_execution.db"), "contamination_events")
    sc.check_security()
    sc.check_dna_chain(str(Path.home()/".龍魂/kfpp/kfpp_execution.db"))
    # sc.check_tests()
    sc.report()
```
## 四、🔌 落地接线清单(把上面那张表接成真的)
这一节做完,值班表才从「设计图」变「运行中」。
### 4.1 🟢 P04 安全闸 — git pre-push 钩子
```bash
# ~/longhun-system/.git/hooks/pre-push  (记得 chmod +x)
#!/bin/bash
echo "🔍 P04 鲁班·push前安全自检..."
python3 longhun_self_check_v1.0.py || { echo "🔴 自检未过,push 已拦截"; exit 1; }
```
### 4.2 🟢 P05 监听 + P03 日复盘 — launchd 常驻(macOS)
```xml
<!-- ~/Library/LaunchAgents/com.uid9622.longhun.selfcheck.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0"><dict>
  <key>Label</key><string>com.uid9622.longhun.selfcheck</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>/Users/zuimeidedeyihan/longhun-system/longhun_self_check_v1.0.py</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>23</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardOutPath</key><string>/Users/zuimeidedeyihan/longhun-system/logs/selfcheck.log</string>
</dict></plist>
```
```bash
launchctl load ~/Library/LaunchAgents/com.uid9622.longhun.selfcheck.plist
```
### 4.3 接线进度
## 五、🕳️ M265 下水道 · Cloudflare Tunnel 命令清单(真接外部 MCP)
```bash
# ===== 第0步:先验证本地真有 MCP 在某端口(别对空气打隧道)=====
lsof -iTCP -sTCP:LISTEN -n -P | grep -E '7000|5000|8787'
curl -s http://localhost:7000/sse || echo "❌ 7000 没 MCP 在听,先起服务"
# 没有独立服务?用网关把 stdio MCP 包成 HTTP:
# npx -y supergateway --stdio "你的mcp启动命令" --port 8787

# ===== 第1步:装 cloudflared =====
brew install cloudflared

# ===== 第2步:登录(浏览器授权 longhun888.com)=====
cloudflared tunnel login

# ===== 第3步:建隧道 =====
cloudflared tunnel create longhun-mcp        # 记下 <TUNNEL_ID>

# ===== 第4步:DNS 指向隧道 =====
cloudflared tunnel route dns longhun-mcp mcp.longhun888.com

# ===== 第5步:写配置 ~/.cloudflared/config.yml =====
# tunnel: <TUNNEL_ID>
# credentials-file: /Users/zuimeidedeyihan/.cloudflared/<TUNNEL_ID>.json
# ingress:
#   - hostname: mcp.longhun888.com
#     service: http://localhost:7000   # 改成第0步确认在听的端口
#   - service: http_status:404

# ===== 第6步:跑起来 =====
cloudflared tunnel run longhun-mcp

# ===== 第7步:公网验证(用手机流量/隔壁机器)=====
curl -i https://mcp.longhun888.com/sse
```
---
```javascript
─── 尾·审计 ───
时间  : 2026-06-05 02:5x CST(周五)
DNA   : #龍芯⚡️2026-06-05-SELFCHECK-DUTY-v1.0
三色  : 🟢设计自洽 / 🟡待本地接线 / 🔴72漏洞待清
守恒  : 派工=8岗·全挂落地机制+失职后果
责任  : UID9622 × 云端宝宝P02 · 不免责
```
