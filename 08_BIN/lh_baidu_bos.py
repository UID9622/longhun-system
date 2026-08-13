#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
龍魂·百度云BOS存储网关 v1.0
=============================
百度智能云对象存储(BOS)统一接入层。
功能: 上传/下载/列表/删除/同步/备份/恢复。
未配置AK/SK时优雅降级为本地模拟模式。

DNA: #龍芯⚡️丙午·甲申·己亥·䷁坤-BAIDU-BOS-GATEWAY-v1.0
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

import os
import sys
import json
import hashlib
import argparse
import logging
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, List, Tuple

# ─── 本地兼容常量 ───
LONGHUN_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = LONGHUN_ROOT / "config"
BOS_CONFIG = CONFIG_DIR / "baidu_bos.json"
BOS_CACHE = CONFIG_DIR / "bos_cache.json"
SYNC_LOG = LONGHUN_ROOT / "logs" / "bos_sync.log"
DEFAULT_BUCKET = "longhun-system-backup"
DEFAULT_REGION = "bj"  # 北京节点（境内·合规）

LOG = logging.getLogger("lh_bos")
LOG.setLevel(logging.INFO)
_h = logging.StreamHandler()
_h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
LOG.addHandler(_h)


# ═══════════════════════════════════════════════
# 配置管理
# ═══════════════════════════════════════════════

def _load_config() -> dict:
    """加载百度云BOS配置"""
    default = {
        "ak": "",
        "sk": "",
        "endpoint": f"https://{DEFAULT_REGION}.bcebos.com",
        "bucket": DEFAULT_BUCKET,
        "region": DEFAULT_REGION,
        "prefix": "longhun/",
        "backup_excludes": [
            "__pycache__/", "*.pyc", "node_modules/", ".git/",
            "_private/", ".DS_Store", "*.asc", "models/*.bin", "models/*.safetensors"
        ],
        "auto_backup_hours": 6,
        "retention_days": 90,
        "enabled": False,
    }
    if BOS_CONFIG.exists():
        try:
            with open(BOS_CONFIG) as f:
                cfg = json.load(f)
            for k, v in default.items():
                if k not in cfg:
                    cfg[k] = v
            return cfg
        except Exception:
            return default
    return default


def _save_config(cfg: dict):
    """保存配置"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(BOS_CONFIG, "w") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def _load_cache() -> dict:
    """加载本地文件→云端映射缓存"""
    if BOS_CACHE.exists():
        try:
            with open(BOS_CACHE) as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _save_cache(cache: dict):
    """保存缓存"""
    with open(BOS_CACHE, "w") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)


# ═══════════════════════════════════════════════
# BOS 客户端（真实SDK或降级模拟）
# ═══════════════════════════════════════════════

class BOSClient:
    """百度云BOS客户端统一封装"""

    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.bucket = cfg["bucket"]
        self.prefix = cfg.get("prefix", "")
        self._client = None
        self._live = False

    def _ensure_client(self) -> bool:
        """延迟初始化BOS SDK客户端"""
        if self._client is not None:
            return self._live

        ak = self.cfg.get("ak", "")
        sk = self.cfg.get("sk", "")

        if not ak or not sk or ak.startswith("your_"):
            LOG.warning("⚠️ 百度云BOS未配置AK/SK，使用本地模拟模式（文件不入云）")
            self._live = False
            return False

        try:
            from baidubce.services.bos.bos_client import BosClient
            from baidubce.bce_client_configuration import BceClientConfiguration
            from baidubce.auth.bce_credentials import BceCredentials

            config = BceClientConfiguration(
                credentials=BceCredentials(ak, sk),
                endpoint=self.cfg["endpoint"]
            )
            self._client = BosClient(config)
            self._live = True
            LOG.info("✅ 百度云BOS客户端初始化成功")
            return True
        except ImportError:
            LOG.warning("⚠️ baidubce SDK未安装(pip install bce-python-sdk)，降级为本地模拟")
            self._live = False
            return False
        except Exception as e:
            LOG.error(f"❌ BOS客户端初始化失败: {e}")
            self._live = False
            return False

    def _key(self, local_path: str) -> str:
        """本地路径→BOS对象key"""
        return f"{self.prefix}{local_path.lstrip('/')}"

    # ── 核心操作 ──

    def upload(self, local_path: str, remote_key: str = None) -> Tuple[bool, str]:
        """上传文件到BOS"""
        local = Path(local_path)
        if not local.exists():
            return False, f"文件不存在: {local_path}"

        key = remote_key or self._key(local_path)
        if not self._ensure_client():
            # 模拟模式：记录到缓存
            cache = _load_cache()
            cache[key] = {
                "local": str(local),
                "size": local.stat().st_size,
                "sha256": _file_hash(local_path),
                "uploaded": datetime.now(timezone.utc).isoformat(),
                "mode": "simulated",
            }
            _save_cache(cache)
            LOG.info(f"📦 [模拟] 上传: {local_path} → {key}")
            return True, key

        try:
            with open(local_path, "rb") as f:
                self._client.put_object(self.bucket, key, f, len(f.read()))
                f.seek(0)
                self._client.put_object(self.bucket, key, f)
            LOG.info(f"☁️ 上传成功: {local_path} → bos://{self.bucket}/{key}")
            return True, key
        except Exception as e:
            return False, f"上传失败: {e}"

    def download(self, remote_key: str, local_path: str) -> Tuple[bool, str]:
        """从BOS下载文件"""
        if not self._ensure_client():
            cache = _load_cache()
            if remote_key in cache:
                LOG.info(f"📦 [模拟] 下载: {remote_key} → {local_path} (已在本地)")
                return True, "已在本地(模拟模式)"
            return False, f"远程文件不存在: {remote_key}"

        try:
            response = self._client.get_object(self.bucket, remote_key)
            Path(local_path).parent.mkdir(parents=True, exist_ok=True)
            with open(local_path, "wb") as f:
                f.write(response.data.read())
            LOG.info(f"📥 下载成功: {remote_key} → {local_path}")
            return True, local_path
        except Exception as e:
            return False, f"下载失败: {e}"

    def list_objects(self, prefix: str = None, max_keys: int = 1000) -> List[Dict]:
        """列出BOS中的对象"""
        search_prefix = prefix or self.prefix
        if not self._ensure_client():
            cache = _load_cache()
            return [
                {"key": k, "size": v.get("size", 0), "last_modified": v.get("uploaded", ""), "mode": "simulated"}
                for k, v in cache.items()
                if k.startswith(search_prefix)
            ][:max_keys]

        try:
            resp = self._client.list_objects(self.bucket, prefix=search_prefix, max_keys=max_keys)
            return [
                {
                    "key": obj.key,
                    "size": obj.size,
                    "last_modified": obj.last_modified,
                    "etag": obj.etag,
                }
                for obj in resp.contents
            ]
        except Exception as e:
            LOG.error(f"列表失败: {e}")
            return []

    def delete(self, remote_key: str) -> Tuple[bool, str]:
        """删除BOS中的对象"""
        if not self._ensure_client():
            cache = _load_cache()
            cache.pop(remote_key, None)
            _save_cache(cache)
            return True, f"[模拟] 已删除: {remote_key}"

        try:
            self._client.delete_object(self.bucket, remote_key)
            LOG.info(f"🗑️ 已删除: {remote_key}")
            return True, remote_key
        except Exception as e:
            return False, f"删除失败: {e}"

    def exists(self, remote_key: str) -> bool:
        """检查对象是否存在"""
        if not self._ensure_client():
            return remote_key in _load_cache()
        try:
            self._client.get_object_meta_data(self.bucket, remote_key)
            return True
        except Exception:
            return False


# ═══════════════════════════════════════════════
# 辅助工具
# ═══════════════════════════════════════════════

def _file_hash(path: str, algo: str = "sha256") -> str:
    """文件哈希"""
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _should_exclude(file_path: str, excludes: List[str]) -> bool:
    """检查文件是否应被排除"""
    import fnmatch
    path_str = str(file_path)
    for pattern in excludes:
        if fnmatch.fnmatch(path_str, f"*{pattern}") or pattern.rstrip("/") in path_str:
            return True
    return False


# ═══════════════════════════════════════════════
# 核心命令
# ═══════════════════════════════════════════════

def cmd_setup(args):
    """配置百度云BOS"""
    cfg = _load_config()
    if args.ak:
        cfg["ak"] = args.ak
    if args.sk:
        cfg["sk"] = args.sk
    if args.bucket:
        cfg["bucket"] = args.bucket
    if args.region:
        cfg["region"] = args.region
        cfg["endpoint"] = f"https://{args.region}.bcebos.com"
    if args.enable:
        cfg["enabled"] = True
    if args.disable:
        cfg["enabled"] = False
    _save_config(cfg)

    # 测试连接
    client = BOSClient(cfg)
    if client._ensure_client():
        print(f"""
╔═══════════════════════════════════════════╗
║  🐉 百度云BOS配置完成                      ║
║  Bucket: {cfg['bucket']:<30s} ║
║  Region: {cfg['region']:<30s} ║
║  Prefix: {cfg['prefix']:<30s} ║
║  Status: {'🟢 已启用' if cfg['enabled'] else '🟡 未启用'}                      ║
╚═══════════════════════════════════════════╝
""")
    else:
        print(f"⚠️ BOS未连接（{cfg.get('ak','') and 'AK/SK无效' or '未配置AK/SK'}），本地模拟模式已就绪")


def cmd_upload(args):
    """上传文件/目录"""
    cfg = _load_config()
    client = BOSClient(cfg)
    source = Path(args.path)
    ok, fail = 0, 0

    if source.is_file():
        success, msg = client.upload(str(source))
        print(f"{'✅' if success else '❌'} {msg}")
        return

    if source.is_dir():
        for f in source.rglob("*"):
            if not f.is_file():
                continue
            if _should_exclude(str(f), cfg.get("backup_excludes", [])):
                continue
            rel = f.relative_to(source) if args.relative else f
            key = client._key(str(rel))
            success, msg = client.upload(str(f), key)
            if success:
                ok += 1
            else:
                fail += 1
                LOG.warning(f"  ❌ {msg}")
        print(f"\n上传完成: ✅ {ok} / ❌ {fail}")


def cmd_download(args):
    """下载文件"""
    cfg = _load_config()
    client = BOSClient(cfg)
    success, msg = client.download(args.remote, args.local)
    print(f"{'✅' if success else '❌'} {msg}")


def cmd_list(args):
    """列出云端文件"""
    cfg = _load_config()
    client = BOSClient(cfg)
    prefix = args.prefix or cfg["prefix"]
    objects = client.list_objects(prefix=prefix, max_keys=args.max)
    if not objects:
        print("(空)")
        return
    total_size = 0
    for obj in objects:
        size_kb = obj["size"] / 1024
        total_size += obj["size"]
        print(f"  {obj['last_modified'][:19] if obj.get('last_modified') else 'N/A'}  {size_kb:>8.1f}KB  {obj['key']}")
    print(f"\n共 {len(objects)} 个对象, 总大小 {total_size/1024/1024:.1f}MB")


def cmd_sync(args):
    """同步本地目录到BOS（增量·仅传变更文件）"""
    cfg = _load_config()
    client = BOSClient(cfg)
    source_dir = Path(args.dir)
    if not source_dir.exists():
        print(f"❌ 目录不存在: {args.dir}")
        sys.exit(1)

    cache = _load_cache()
    new_cache = {}
    uploaded, skipped, failed = 0, 0, 0

    excludes = cfg.get("backup_excludes", [])
    files = [f for f in source_dir.rglob("*") if f.is_file() and not _should_exclude(str(f), excludes)]

    print(f"🔄 同步: {source_dir} → bos://{cfg['bucket']}/{cfg['prefix']}")
    print(f"   文件总数: {len(files)}")

    for fpath in files:
        rel = str(fpath.relative_to(source_dir))
        key = client._key(rel)
        fhash = _file_hash(str(fpath))

        # 增量判断：hash未变 → 跳过
        if key in cache and cache[key].get("sha256") == fhash:
            skipped += 1
            new_cache[key] = cache[key]
            continue

        success, msg = client.upload(str(fpath), key)
        if success:
            uploaded += 1
            new_cache[key] = {
                "local": str(fpath),
                "size": fpath.stat().st_size,
                "sha256": fhash,
                "uploaded": datetime.now(timezone.utc).isoformat(),
            }
        else:
            failed += 1
            LOG.warning(f"  ❌ {msg}")

    _save_cache(new_cache)

    # 写同步日志
    SYNC_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(SYNC_LOG, "a") as lf:
        lf.write(f"[{datetime.now(timezone.utc).isoformat()}] sync {source_dir.name}: "
                 f"uploaded={uploaded} skipped={skipped} failed={failed}\n")

    print(f"\n同步完成: ☁️ 上传 {uploaded} | ⏭️ 跳过 {skipped} | ❌ 失败 {failed}")


def cmd_backup(args):
    """全量备份指定目录到BOS"""
    cfg = _load_config()
    if not cfg["enabled"]:
        print("⚠️ 百度云BOS未启用，使用本地备份")
        return

    client = BOSClient(cfg)
    for dir_path in args.dirs:
        p = Path(dir_path)
        if not p.exists():
            print(f"⚠️ 跳过不存在的目录: {dir_path}")
            continue
        # 用_sync逻辑
        print(f"📦 备份: {dir_path}")
        # 复用sync逻辑
        from types import SimpleNamespace
        fake_args = SimpleNamespace(dir=dir_path)
        cmd_sync(fake_args)


def cmd_pull(args):
    """从BOS拉取恢复全部数据到本地"""
    cfg = _load_config()
    client = BOSClient(cfg)
    local_root = Path(args.output)
    local_root.mkdir(parents=True, exist_ok=True)

    objects = client.list_objects(prefix=cfg["prefix"])
    ok, fail = 0, 0
    prefix_len = len(cfg["prefix"])

    for obj in objects:
        key = obj["key"]
        rel = key[prefix_len:] if key.startswith(cfg["prefix"]) else key
        local_path = local_root / rel
        success, msg = client.download(key, str(local_path))
        if success:
            ok += 1
        else:
            fail += 1
            LOG.warning(f"  ❌ {msg}")

    print(f"\n拉取完成: ✅ {ok} / ❌ {fail}")


def cmd_status(args):
    """检查BOS连接和存储状态"""
    cfg = _load_config()
    client = BOSClient(cfg)
    live = client._ensure_client()
    objects = client.list_objects(max_keys=10000)
    total_size = sum(o["size"] for o in objects)

    synced_count = len(_load_cache())

    print(f"""
╔═══════════════════════════════════════════╗
║  🐉 龍魂·百度云BOS存储状态                ║
╠═══════════════════════════════════════════╣
║  BOS连接: {'🟢 在线' if live else '🟡 模拟(本地)'}                    ║
║  Bucket:  {cfg['bucket']:<30s} ║
║  对象数:  {len(objects):>5d}                         ║
║  总大小:  {total_size/1024/1024:>8.1f} MB                    ║
║  索引数:  {synced_count:>5d}                         ║
║  备份间隔:{cfg.get('auto_backup_hours',6):>5d}h                        ║
║  保留天数:{cfg.get('retention_days',90):>5d}d                        ║
╚═══════════════════════════════════════════╝
""")


def cmd_clean(args):
    """清理云端过期备份"""
    cfg = _load_config()
    client = BOSClient(cfg)
    retention = cfg.get("retention_days", 90)
    cutoff = time.time() - retention * 86400

    objects = client.list_objects(prefix=cfg["prefix"])
    deleted = 0
    for obj in objects:
        # 跳过模拟模式的对象（无真实时间戳）
        if not obj.get("last_modified"):
            continue
        try:
            ts = datetime.fromisoformat(obj["last_modified"].replace("Z", "+00:00"))
            if ts.timestamp() < cutoff:
                ok, _ = client.delete(obj["key"])
                if ok:
                    deleted += 1
        except Exception:
            pass

    print(f"清理完成: 删除 {deleted} 个过期对象（>{retention}天）")


# ═══════════════════════════════════════════════
# CLI入口
# ═══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·百度云BOS存储网关",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh bos setup --ak YOUR_AK --sk YOUR_SK --bucket longhun-backup
  lh bos upload ./data/
  lh bos sync ./web_apps/
  lh bos list
  lh bos pull --output ./restore/
  lh bos status
  lh bos backup --dirs ./data/ ./config/
"""
    )
    sub = parser.add_subparsers(dest="cmd", help="子命令")

    # setup
    p = sub.add_parser("setup", help="配置百度云BOS")
    p.add_argument("--ak", help="Access Key")
    p.add_argument("--sk", help="Secret Key")
    p.add_argument("--bucket", help="Bucket名称")
    p.add_argument("--region", default="bj", help="地域（默认bj北京）")
    p.add_argument("--enable", action="store_true", help="启用BOS")
    p.add_argument("--disable", action="store_true", help="禁用BOS")

    # upload
    p = sub.add_parser("upload", help="上传文件/目录")
    p.add_argument("path", help="本地路径")
    p.add_argument("--relative", action="store_true", help="保持相对路径")

    # download
    p = sub.add_parser("download", help="下载文件")
    p.add_argument("remote", help="远程key")
    p.add_argument("local", help="本地路径")

    # list
    p = sub.add_parser("list", help="列出云端文件")
    p.add_argument("--prefix", help="过滤前缀")
    p.add_argument("--max", type=int, default=100, help="最大数量")

    # sync
    p = sub.add_parser("sync", help="增量同步目录")
    p.add_argument("dir", help="本地目录")

    # backup
    p = sub.add_parser("backup", help="备份指定目录")
    p.add_argument("--dirs", nargs="+", required=True, help="要备份的目录列表")

    # pull
    p = sub.add_parser("pull", help="从BOS拉取恢复")
    p.add_argument("--output", default="./bos_restore/", help="恢复目标目录")

    # status
    sub.add_parser("status", help="查看存储状态")

    # clean
    sub.add_parser("clean", help="清理过期备份")

    args = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    cmd_map = {
        "setup": cmd_setup,
        "upload": cmd_upload,
        "download": cmd_download,
        "list": cmd_list,
        "sync": cmd_sync,
        "backup": cmd_backup,
        "pull": cmd_pull,
        "status": cmd_status,
        "clean": cmd_clean,
    }
    cmd_map[args.cmd](args)


if __name__ == "__main__":
    main()
