#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·庚辰·申时·䷗复-NOTION-PULL-ALL-v2.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""龍魂 Notion 全量拉取 v2.0（DOM 路线·浏览器登录态）
原理: CDP Chrome → 侧边栏枚举链接 → 逐页导航 → 提取 DOM → Markdown
支持: BFS 子页 / 断点续跑 / 失败重试 / --list / --page / --max / --cdp
输出: _work/notion_pull/pages/<id>.md + result.json
"""
import argparse, json, re, sys, time
from pathlib import Path
import requests, websocket

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_work" / "notion_pull"
PDIR = OUT / "pages"
IDX = OUT / "pages_index.json"
RESULT = OUT / "result.json"

EXTRACT = r"""(() => {
  const out = {title:'', blocks:[], subLinks:[]};
  const te = document.querySelector('.notion-page-block') || document.querySelector('h1');
  if (te) out.title = (te.innerText||'').trim().slice(0,300);
  const seenT = new Set();
  document.querySelectorAll('[data-block-id]').forEach(el => {
    if (el.parentElement && el.parentElement.closest('[data-block-id]')) return;
    const txt = (el.innerText||'').trim();
    if (!txt || seenT.has(txt)) return;
    seenT.add(txt);
    const cls = el.className||'';
    let type='text';
    if (/header/.test(cls)) type='h2';
    else if (/sub_header/.test(cls)) type='h3';
    else if (/sub_sub_header/.test(cls)) type='h4';
    else if (/bulleted/.test(cls)) type='bullet';
    else if (/numbered/.test(cls)) type='num';
    else if (/quote/.test(cls)) type='quote';
    else if (/code/.test(cls)) type='code';
    else if (/to_do/.test(cls)) type='todo';
    else if (/callout/.test(cls)) type='callout';
    else if (/collection/.test(cls)) type='database';
    out.blocks.push({type:type, text:txt.slice(0,2000)});
  });
  const seenL = new Set();
  document.querySelectorAll('a[href^="/p/"]').forEach(a => {
    const h = a.getAttribute('href');
    if (h && !seenL.has(h)) { seenL.add(h); out.subLinks.push(h); }
  });
  return JSON.stringify(out);
})()"""


def find_tab(ch):
    tabs = requests.get(f"{ch}/json/list", timeout=5).json()
    for t in tabs:
        if "notion" in (t.get("url") or "") and t.get("type") == "page":
            return t
    return None


class CDP:
    """CDP 连接管理器·带自动重连（v2.1 修复 socket is already closed）
    连接断开 → 自动重连 + 重新定位 Notion tab → 上层重发命令"""
    def __init__(self, ch):
        self.ch = ch
        self.ws = None
        self.n = 0
        self.connect()

    def connect(self):
        tab = find_tab(self.ch)
        if not tab:
            raise RuntimeError("CDP 无 Notion 页面（浏览器是否已关闭？）")
        self.ws = websocket.create_connection(tab["webSocketDebuggerUrl"], timeout=120)
        self.n = 0

    def reconnect(self, tries=5):
        try:
            self.ws.close()
        except Exception:
            pass
        self.ws = None
        for i in range(tries):
            try:
                time.sleep(1.5)
                self.connect()
                return True
            except Exception:
                time.sleep(1.5)
        return False

    def _call(self, m, p):
        self.n += 1
        self.ws.send(json.dumps({"id": self.n, "method": m, "params": p}))
        while True:
            x = json.loads(self.ws.recv())
            if x.get("id") == self.n:
                return x

    def cmd(self, m, p, retries=2):
        for i in range(retries + 1):
            try:
                return self._call(m, p)
            except Exception:
                if i == retries:
                    raise
                if not self.reconnect():
                    raise RuntimeError("CDP 重连失败")
        raise RuntimeError("CDP 不可用")

    def ev(self, expr, t=30):
        r = self.cmd("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
        res = r.get("result", {}).get("result", {})
        return res["value"] if "value" in res else {"EXC": str(r.get("result", {}).get("exceptionDetails", {}))[:300]}

    def close(self):
        try:
            self.ws.close()
        except Exception:
            pass


def extract_page(cdp, max_wait=15):
    """等渲染并提取。返回 (ok, data)"""
    st = {}
    start = time.time()
    while time.time() - start < max_wait:
        time.sleep(2)
        v = cdp.ev("JSON.stringify({nb: document.querySelectorAll('[data-block-id]').length, err: document.body.innerText.includes('出错')})")
        try:
            st = json.loads(v)
        except Exception:
            st = {}
        if st.get("nb", 0) > 2 and not st.get("err"):
            break
    if st.get("nb", 0) <= 2:
        return False, st
    v = cdp.ev(EXTRACT)
    if isinstance(v, dict) and "EXC" in v:
        return False, v
    try:
        return True, json.loads(v)
    except Exception:
        return False, {"raw": str(v)[:500]}


def to_md(d, url):
    L = [f"# {d.get('title') or '(untitled)'}", "", f"> source: {url}", ""]
    for b in d.get("blocks", []):
        t, bt = b["text"], b["type"]
        if bt == "h2":
            L.append(f"## {t}")
        elif bt == "h3":
            L.append(f"### {t}")
        elif bt == "h4":
            L.append(f"#### {t}")
        elif bt == "bullet":
            L.append(f"- {t}")
        elif bt == "num":
            L.append(f"1. {t}")
        elif bt == "quote":
            L.append(f"> {t}")
        elif bt == "code":
            L.append(f"```\n{t}\n```")
        elif bt == "todo":
            L.append(f"- [ ] {t}")
        elif bt == "callout":
            L.append(f"💬 {t}")
        elif bt == "database":
            L.append(f"🗃 {t}")
        else:
            L.append(t)
        L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--page", type=str)
    ap.add_argument("--cdp", type=int, default=58182)
    ap.add_argument("--max", type=int, default=0)
    a = ap.parse_args()
    ch = f"http://127.0.0.1:{a.cdp}"
    tab = find_tab(ch)
    if not tab:
        print("ERROR: CDP 无 Notion 页面"); sys.exit(1)
    print(f"CDP: {tab['url'][:70]}", flush=True)
    cdp = CDP(ch)
    st = cdp.ev("JSON.stringify({nb: document.querySelectorAll('[data-block-id]').length, u: location.href.slice(0,60)})")
    try:
        stj = json.loads(st)
    except Exception:
        stj = {}
    if stj.get("nb", 0) < 2:
        print("LOGIN: 页面未加载, 导航主工作区", flush=True)
        cdp.cmd("Page.navigate", {"url": "https://app.notion.com"})
        time.sleep(8)
    print("LOGIN: OK", flush=True)

    if a.page:
        pid = a.page
        cdp.cmd("Page.navigate", {"url": f"https://app.notion.com/{pid}"})
        ok, d = extract_page(cdp)
        if not ok:
            print(f"FAIL {pid}: {d}"); sys.exit(2)
        PDIR.mkdir(parents=True, exist_ok=True)
        md = to_md(d, f"https://app.notion.com/{pid}")
        (PDIR / f"{pid}.md").write_text(md, encoding="utf-8")
        print(f"SAVED {pid} ({len(d['blocks'])}b/{len(md)}c)", flush=True)
        cdp.close(); return

    if a.list or not IDX.exists():
        cdp.cmd("Page.navigate", {"url": "https://app.notion.com"})
        time.sleep(8)
        v = cdp.ev("""(async () => {
          const links = [], seen = new Set();
          document.querySelectorAll('a[href^="/p/"]').forEach(a => {
            const h = a.getAttribute('href') || '';
            const t = (a.innerText || '').trim();
            if (t && !seen.has(h)) { seen.add(h);
              const m = h.match(/[0-9a-f]{32}/g);
              links.push({href: h, id: m ? m[m.length-1] : '', title: t.slice(0,120)}); }
          });
          return JSON.stringify(links);
        })()""")
        try:
            links = json.loads(v)
        except Exception:
            print(f"LIST FAIL: {v}"); sys.exit(2)
        OUT.mkdir(parents=True, exist_ok=True)
        IDX.write_text(json.dumps({"links": links, "count": len(links)}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"LIST: {len(links)} pages", flush=True)
        if a.list:
            for l in links:
                print(f"  {l['id']}  {l['title'][:55]}", flush=True)
            cdp.close(); return

    idx = json.loads(IDX.read_text(encoding="utf-8"))
    queue = [l["href"] for l in idx["links"] if l["id"]]
    done = set(p.stem for p in PDIR.glob("*.md")) if PDIR.exists() else set()
    seen_h = set()
    results = []
    failed = []
    PDIR.mkdir(parents=True, exist_ok=True)
    print(f"QUEUE: {len(queue)} · already done: {len(done)}", flush=True)
    cnt = 0
    dead = False
    while queue and not dead:
        href = queue.pop(0)
        if href in seen_h:
            continue
        seen_h.add(href)
        m = re.findall(r"[0-9a-f]{32}", href)
        pid = m[-1] if m else href
        if pid in done:
            continue
        url = "https://app.notion.com" + href if href.startswith("/") else href
        ok = False
        d = {}
        for attempt in range(3):
            try:
                cdp.cmd("Page.navigate", {"url": url})
                ok, d = extract_page(cdp)
            except Exception as e:
                ok, d = False, {"error": str(e)[:200]}
                # socket 断开 → 自动重连后重试
                if not cdp.reconnect():
                    print(f"  CDP 彻底不可用, 中止于 {pid}", flush=True)
                    failed.append({"id": pid, "href": href, "status": "cdp-dead", "err": str(e)[:200]})
                    dead = True
                    break
            if ok:
                break
        if not ok:
            print(f"  FAIL {pid}: {str(d)[:120]}", flush=True)
            results.append({"id": pid, "href": href, "status": "fail"})
            failed.append({"id": pid, "href": href, "status": "fail", "err": str(d)[:200]})
            continue
        md = to_md(d, url)
        (PDIR / f"{pid}.md").write_text(md, encoding="utf-8")
        done.add(pid)
        cnt += 1
        for sub in d.get("subLinks", []):
            if sub not in seen_h:
                queue.append(sub)
        results.append({"id": pid, "href": href, "status": "ok", "title": d.get("title", "")[:100],
                        "blocks": len(d.get("blocks", [])), "chars": len(md)})
        print(f"  OK [{cnt}] {d.get('title','')[:45]} ({len(d.get('blocks',[]))}b/{len(md)}c)", flush=True)
        time.sleep(0.5)
        if a.max and cnt >= a.max:
            break
    RESULT.write_text(json.dumps({"total": len(results), "done": cnt, "failed": len(failed), "results": results}, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "failed.json").write_text(json.dumps(failed, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"DONE: {cnt} pages → {PDIR} · 失败 {len(failed)} (清单: _work/notion_pull/failed.json)", flush=True)
    cdp.close()


if __name__ == "__main__":
    main()
