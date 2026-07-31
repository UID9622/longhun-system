# DNA: #龍芯⚡️丙午·乙未·乙丑·同人-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ============================================================
# 龍魂四绝 · 真实数据 ETL（高德 Web服务 → SQLite）
# 文件：L5_服务层/services/siju_etl.py
# DNA：#龍芯⚡️丙午·辛未·四绝-ETL-v1.0
#
# 真实数据源：高德地图 Web服务 API（地理编码 / 周边搜索 POI）
# 诚信原则：高德返回错误（如 10007 key类型不符）时，降级为 INFERENCE 并标注原因，
#           绝不把错误响应伪装成真实数据（5条硬要求核心）
# 数据主权：本地 SQLite，不上传云端
# ============================================================

import os
import sys
import json
import sqlite3
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from siju_decision import DataSourceType, Provenance

DB_PATH = ROOT / "data" / "siju.db"
AMAP_REST = "https://restapi.amap.com"


# ---- 高德 key 加载（沿用系统 api_keys.env） ----
def load_amap_key() -> str:
    # 优先环境变量，其次扫描 config/api_keys.env
    key = os.getenv("AMAP_KEY")
    if key:
        return key
    cand = ROOT.parent.parent / "config" / "api_keys.env"
    if cand.exists():
        for line in cand.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("AMAP_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


class AmapClient:
    """高德 Web服务客户端（服务端 REST）。"""

    def __init__(self, dna: str, key: str = ""):
        self.dna = dna
        self.key = key or load_amap_key()
        self.last_error = ""

    def _get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        if not self.key:
            self.last_error = "AMAP_KEY 未配置"
            return {"status": "0", "info": self.last_error, "infocode": "NO_KEY"}
        params = dict(params)
        params["key"] = self.key
        url = AMAP_REST + path + "?" + urllib.parse.urlencode(params)
        try:
            with urllib.request.urlopen(url, timeout=15) as r:
                data = json.loads(r.read().decode("utf-8"))
        except Exception as e:
            self.last_error = f"网络异常: {e}"
            return {"status": "0", "info": self.last_error, "infocode": "NET_ERR"}
        if data.get("status") != "1":
            self.last_error = f"{data.get('info')}({data.get('infocode')})"
        return data

    # 1. 地理编码：地址 → 坐标
    def geocode(self, address: str, city: str = "") -> dict[str, Any]:
        return self._get("/v3/geocode/geo",
                         {"address": address, "city": city, "output": "json"})

    # 2. 周边搜索 POI：坐标 + 半径 + 关键词
    def around(self, location: str, keywords: str, radius: int = 3000) -> dict[str, Any]:
        return self._get("/v3/place/around",
                         {"location": location, "keywords": keywords,
                          "radius": radius, "offset": 25, "page": 1, "output": "json"})


# ---- SQLite 存储 ----
def init_db():
    os.makedirs(DB_PATH.parent, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT UNIQUE, lng REAL, lat REAL, district TEXT,
        fetch_time TEXT, dna TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS pois (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        loc_id INTEGER, name TEXT, category TEXT, address TEXT,
        lng REAL, lat REAL, distance INTEGER, brand TEXT,
        source TEXT, fetch_time TEXT, dna TEXT)''')
    c.execute('CREATE INDEX IF NOT EXISTS idx_pois_loc ON pois(loc_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_pois_cat ON pois(category)')
    conn.commit()
    conn.close()


def save_pois(loc_id: int, pois: list[Any], provenance: str, dna: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for p in pois:
        c.execute('''INSERT OR IGNORE INTO pois
            (loc_id,name,category,address,lng,lat,distance,brand,source,fetch_time,dna)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
            (loc_id, p.get("name"), p.get("category"), p.get("address"),
             p.get("lng"), p.get("lat"), p.get("distance"),
             p.get("brand"), provenance, datetime.now().isoformat(), dna))
    conn.commit()
    conn.close()


# 品类 → 高德 POI 分类关键词映射
CATEGORY_MAP = {
    "奶茶店": "奶茶", "咖啡店": "咖啡", "快餐店": "快餐",
    "火锅店": "火锅", "烘焙店": "烘焙", "便利店": "便利店",
    "餐饮": "餐饮", "零售": "购物",
}


def run_etl(address: str, category: str, dna: str, city: str = "",
            radius: int = 3000) -> dict[str, Any]:
    """
    真实 ETL 主流程：
      1. 地理编码 2. 周边搜索 3. 入库
    返回 {ok, mode, location, competitors, provenance, note}
    """
    init_db()
    client = AmapClient(dna)
    geo = client.geocode(address, city)
    if geo.get("status") != "1" or not geo.get("geocodes"):
        # 诚信降级：不冒充真实数据
        return {
            "ok": False, "mode": "INFERENCE",
            "location": None, "competitors": [],
            "provenance": None,
            "note": f"高德地理编码失败：{client.last_error}（已降级为推演模式，非真实数据）",
        }

    gc = geo["geocodes"][0]
    lng, lat = map(float, gc["location"].split(","))
    district = gc.get("district", "")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO locations (address,lng,lat,district,fetch_time,dna) VALUES (?,?,?,?,?,?)',
              (address, lng, lat, district, datetime.now().isoformat(), dna))
    loc_id = c.execute('SELECT id FROM locations WHERE address=?', (address,)).fetchone()[0]
    conn.commit()
    conn.close()

    kw = CATEGORY_MAP.get(category, category)
    resp = client.around(f"{lng},{lat}", kw, radius)
    competitors = []
    if resp.get("status") == "1":
        for po in resp.get("pois", []):
            plng, plat = map(float, po["location"].split(","))
            competitors.append({
                "name": po.get("name"),
                "category": po.get("type", "").split(";")[0],
                "address": po.get("address", ""),
                "lng": plng, "lat": plat,
                "distance": int(po.get("distance", 0)),
                "brand": po.get("name", "").split(("("))[0],
            })
        prov = Provenance(
            source_type=DataSourceType.PUBLIC_MAP,
            source_url="https://restapi.amap.com/v3/place/around",
            fetch_time=datetime.now(), reliability="high",
            update_frequency="实时", dna_trace=dna,
            notes=f"高德周边搜索POI·半径{radius}m·关键词『{kw}』·真实数据",
            ref_policy="高德地图开放平台服务条款",
        )
        save_pois(loc_id, competitors, "amap", dna)
        return {"ok": True, "mode": "REAL", "location": {"lng": lng, "lat": lat, "district": district},
                "competitors": competitors, "provenance": prov.to_dict(),
                "note": f"真实拉取周边『{kw}』{len(competitors)}家"}
    else:
        return {"ok": False, "mode": "INFERENCE", "location": {"lng": lng, "lat": lat, "district": district},
                "competitors": [], "provenance": None,
                "note": f"高德周边搜索失败：{client.last_error}（坐标已得，竞品降级推演）"}


if __name__ == "__main__":
    dna = "#龍魂⚡️20260716-ETL-TEST"
    print("=== 用系统里的高德 key 实跑 ETL（温州瑞安 奶茶店）===")
    res = run_etl("温州瑞安", "奶茶店", dna, city="温州")
    print("模式:", res["mode"])
    print("说明:", res["note"])
    if res["location"]:
        print("坐标:", res["location"])
    print("竞品数:", len(res["competitors"]))
