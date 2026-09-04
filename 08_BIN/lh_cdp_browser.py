# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·甲子·癸酉·䷪夬-CODE-补DNA-dc74f2c1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂 CDP 浏览器控制工具 v1.0
用途: 域名备案流程自动化。卡到人工步骤即停。
用法:
  goto <url>   # 打开 URL
  shot [path]  # 截图
  dom [sel]    # 输出页面文本
  click <css> [idx]
  type <css> <text>
  submit <css> <text>
  upload <css> <file>  # 设置文件输入框文件
  eval <js>
  wait <ms>
  title        # 当前 URL + 标题
"""
import json
import sys
import time
import base64
import urllib.request
import websocket

CDP = "http://localhost:9222"
WS = None
MSG_ID = 0


def get_ws_url():
    data = json.loads(urllib.request.urlopen(CDP + "/json").read())
    for t in data:
        if t.get("type") == "page":
            return t["webSocketDebuggerUrl"]
    raise RuntimeError("no page target")


def connect():
    global WS
    if WS is None:
        WS = websocket.create_connection(get_ws_url(), timeout=30)
    return WS


def cmd(method, params=None):
    global MSG_ID
    MSG_ID += 1
    connect().send(json.dumps({"id": MSG_ID, "method": method, "params": params or {}}))
    while True:
        r = json.loads(connect().recv())
        if r.get("id") == MSG_ID:
            if "error" in r:
                raise RuntimeError("CDP: " + str(r["error"]))
            return r.get("result", {})


def eval_js(expr):
    r = cmd("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
    return r.get("result", {}).get("value")


def goto(url):
    cmd("Page.navigate", {"url": url})
    for _ in range(15):
        time.sleep(1)
        try:
            if eval_js("document.readyState") == "complete":
                break
        except Exception:
            pass
    time.sleep(2)
    return eval_js("location.href + ' | ' + document.title")


def shot(path="/tmp/lh_cdp_shot.png"):
    r = cmd("Page.captureScreenshot", {"format": "png"})
    with open(path, "wb") as f:
        f.write(base64.b64decode(r["data"]))
    return path


def dom(selector=None):
    if selector:
        js = "JSON.stringify(Array.from(document.querySelectorAll(%s).slice(0,5)).map(e=>e.outerHTML))" % json.dumps(selector)
    else:
        js = "document.body ? document.body.innerText.slice(0,3000) : ''"
    return eval_js(js) or ""


def click(selector, idx=0):
    js = ("(()=>{const els=document.querySelectorAll(%s);"
          "if(!els.length)return 'NO_MATCH';"
          "const el=els[%d];if(el.scrollIntoView)el.scrollIntoView({block:'center'});"
          "el.click();return 'CLICKED';})()") % (json.dumps(selector), idx)
    return eval_js(js)


def fill(selector, text, submit=False):
    js = ("(()=>{const el=document.querySelector(%s);if(!el)return 'NO_MATCH';"
          "const setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
          "setter.call(el,%s);el.dispatchEvent(new Event('input',{bubbles:true}));"
          "el.dispatchEvent(new Event('change',{bubbles:true}));"
          "if(%s){const f=el.closest('form');if(f){f.submit();return 'SUBMITTED';}}"
          "return 'FILLED';})()") % (json.dumps(selector), json.dumps(text), "true" if submit else "false")
    return eval_js(js)


def wait(ms):
    time.sleep(ms / 1000.0)
    return "OK"


def upload(selector, filepath):
    # 通过 Runtime.evaluate 拿到对象的 objectId，再用 DOM.setFileInputFiles
    js = ("(()=>{const el=document.querySelector(%s);if(!el)return null;"
          "return el;})()") % json.dumps(selector)
    r = cmd("Runtime.evaluate", {"expression": js, "returnByValue": False})
    obj = r.get("result", {})
    if obj.get("type") == "undefined" or not obj.get("objectId"):
        return "NO_MATCH"
    cmd("DOM.setFileInputFiles", {"files": [filepath], "objectId": obj["objectId"]})
    return "UPLOADED"


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)
    op = args[0]
    try:
        if op == "goto":
            print("NAV:", goto(args[1]))
        elif op == "shot":
            print("SHOT:", shot(args[1] if len(args) > 1 else "/tmp/lh_cdp_shot.png"))
        elif op == "dom":
            print(dom(args[1] if len(args) > 1 else None))
        elif op == "click":
            print(click(args[1], int(args[2]) if len(args) > 2 else 0))
        elif op == "type":
            print(fill(args[1], args[2]))
        elif op == "submit":
            print(fill(args[1], args[2], submit=True))
        elif op == "upload":
            print(upload(args[1], args[2]))
        elif op == "eval":
            print(eval_js(args[1]))
        elif op == "wait":
            print(wait(int(args[1])))
        elif op == "title":
            print(eval_js("location.href + ' | ' + document.title"))
        else:
            print("UNKNOWN:", op)
    except Exception as e:
        print("ERR:", repr(e))
        sys.exit(1)
