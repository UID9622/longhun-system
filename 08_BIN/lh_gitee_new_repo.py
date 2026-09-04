#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷓观-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·䷒临-LH_GITEE_NEW_REPO-v1.0-f116684a
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""Gitee repo creator via Kimi WebBridge"""
import subprocess, json, time, sys

BASE = 'http://127.0.0.1:10086/command'
S = 'gitee-create'

def call(data):
    r = subprocess.run(['curl','-s','-X','POST',BASE,'-H','Content-Type: application/json',
        '-d',json.dumps(data)], capture_output=True, text=True, timeout=20)
    return json.loads(r.stdout)

name = sys.argv[1] if len(sys.argv) > 1 else 'test-repo'

# Navigate
call({'action':'navigate','args':{'url':'https://gitee.com/projects/new'},'session':S})
time.sleep(3)

# Fill via JS
js = f"""
(() => {{
    const sel = '[name="repo[name]"]';
    const i = document.querySelector(sel);
    if (!i) return 'NO_INPUT';
    i.value = '{name}';
    i.dispatchEvent(new Event('input', {{bubbles:true}}));
    const ps = document.querySelector('[name="repo[path]"]');
    if (ps) {{ ps.value = '{name}'; ps.dispatchEvent(new Event('input', {{bubbles:true}})); }}
    return i.value;
}})()
"""
r = call({'action':'evaluate','args':{'code':js},'session':S})
print(f'Fill: {r.get("data",{}).get("value","ERR")}')

# Click create
r2 = call({'action':'evaluate','args':{
    'code': """(() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const b = btns.find(x => x.textContent.includes('创建'));
        if (b) { b.click(); return 'CLICKED'; }
        return 'NO_BTN';
    })()"""
},'session':S})
print(f'Click: {r2.get("data",{}).get("value","ERR")}')

time.sleep(2)
r3 = call({'action':'evaluate','args':{'code':'JSON.stringify({url:location.href,title:document.title,body:document.body.innerText.substring(0,200)})'},'session':S})
print(f'Result: {r3.get("data",{}).get("value","ERR")}')
