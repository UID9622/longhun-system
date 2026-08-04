#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# ⚡ 龍魂·全文件解析引擎 v1.0
# DNA: #龍芯⚡️丙午·辛未·乙酉·需-UNIVERSAL-PARSER-v1.0
# 格言: 解析一切·不留死角
# 主权: UID9622 | 数据不出机 | 国产芯片优先
# 协议: LH-PARSING-ENGINE-2026-0714-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

"""
龍魂全文件解析引擎 — Universal Parser Engine v1.0
================================================
覆盖 60+ 文件格式，统一 parse() 接口，分层解析，自动降级。
P0: Excel/PowerPoint/ZIP/RAR/SQLite/API
P1: HEIC/TIFF/MP3/WAV/MP4/7Z/EPUB/EXIF/Cookie/JS渲染
P2: FLAC/MKV/MOV/WebM/RAW/PSD/OCR/人脸/物体/二维码
P3: 其他稀有格式

架构:
  UniversalParser (入口)
  ├── DocumentParsers (xlsx/pptx/epub/pdf/docx/tex/odf/chm/djvu)
  ├── ImageParsers (heic/tiff/raw/psd/ico/pcx/tga/svg→深度)
  ├── AudioParsers (mp3/wav/flac/aac/ogg/m4a/wma/aiff)
  ├── VideoParsers (mp4/avi/mkv/mov/wmv/flv/webm/mpeg)
  ├── ArchiveParsers (zip/rar/7z/tar/gz/bz2/xz/iso)
  ├── DatabaseParsers (sqlite/mdb/accdb/dbf)
  ├── EmailParsers (eml/msg/mbox)
  ├── FontParsers (ttf/otf/woff/woff2)
  ├── CodeParsers (py/js/ts/java/c/cpp/go/rs/sh/sql/html/css/json/yaml/xml)
  ├── WebParsers (url/js-render/cookie/api/rss/sitemap/dns/whois/ssl)
  └── DeepAnalysis (exif/ocr/face/object/qrcode/similarity/nsfw)
"""

import os
import sys
import json
import hashlib
import struct
import re
import io
import base64
import tempfile
import subprocess
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple, Union
from dataclasses import dataclass, field, asdict

# ============================================================
# DNA 追溯
# ============================================================
__DNA__ = "#龍芯⚡️丙午·辛未·乙酉·需-UNIVERSAL-PARSER-v1.0"
__VERSION__ = "1.0.0"
__PROTOCOL__ = "LH-PARSING-ENGINE-2026-0714-v1.0"
__SOVEREIGN__ = "UID9622"
__GPG__ = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


# ============================================================
# 数据结构
# ============================================================
@dataclass
class ParseResult:
    """统一解析结果"""
    status: str = "success"          # success / partial / unsupported / error
    file_path: str = ""
    file_name: str = ""
    extension: str = ""
    file_size: int = 0
    mime_type: str = ""
    parser_used: str = ""
    content_preview: str = ""        # 前1000字符预览
    structured_data: Dict = field(default_factory=dict[str, Any])
    metadata: Dict = field(default_factory=dict[str, Any])
    raw_text: str = ""
    page_count: int = 0
    sheet_names: List[str] = field(default_factory=list[Any])
    tables: List[Dict] = field(default_factory=list[Any])
    images: List[Dict] = field(default_factory=list[Any])
    audio_info: Dict = field(default_factory=dict[str, Any])
    video_info: Dict = field(default_factory=dict[str, Any])
    archive_files: List[str] = field(default_factory=list[Any])
    security: Dict = field(default_factory=dict[str, Any])  # 安全/签名/加密信息
    dna: str = __DNA__
    parse_time_ms: float = 0.0
    warnings: List[str] = field(default_factory=list[Any])
    errors: List[str] = field(default_factory=list[Any])

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2, default=str)


# ============================================================
# 工具函数
# ============================================================
def get_file_hash(file_path: str, algo: str = "sha256") -> str:
    """计算文件哈希"""
    h = hashlib.new(algo)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_import(module_name: str, pkg: Optional[str] = None) -> Tuple[bool, Any]:
    """安全导入模块"""
    try:
        if pkg:
            mod = __import__(module_name, fromlist=[pkg])
        else:
            mod = __import__(module_name)
        return True, mod
    except ImportError:
        return False, None


def get_mime_type(ext: str) -> str:
    """扩展名→MIME类型映射"""
    MIME_MAP = {
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".xls": "application/vnd.ms-excel",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".ppt": "application/vnd.ms-powerpoint",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".doc": "application/msword",
        ".pdf": "application/pdf",
        ".epub": "application/epub+zip",
        ".mobi": "application/x-mobipocket-ebook",
        ".zip": "application/zip",
        ".rar": "application/vnd.rar",
        ".7z": "application/x-7z-compressed",
        ".tar": "application/x-tar",
        ".gz": "application/gzip",
        ".bz2": "application/x-bzip2",
        ".xz": "application/x-xz",
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
        ".flac": "audio/flac",
        ".aac": "audio/aac",
        ".ogg": "audio/ogg",
        ".m4a": "audio/mp4",
        ".wma": "audio/x-ms-wma",
        ".aiff": "audio/aiff",
        ".mp4": "video/mp4",
        ".avi": "video/x-msvideo",
        ".mkv": "video/x-matroska",
        ".mov": "video/quicktime",
        ".wmv": "video/x-ms-wmv",
        ".flv": "video/x-flv",
        ".webm": "video/webm",
        ".mpeg": "video/mpeg",
        ".mpg": "video/mpeg",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".bmp": "image/bmp",
        ".svg": "image/svg+xml",
        ".tiff": "image/tiff",
        ".tif": "image/tiff",
        ".heic": "image/heic",
        ".raw": "image/x-raw",
        ".cr2": "image/x-canon-cr2",
        ".nef": "image/x-nikon-nef",
        ".psd": "image/vnd.adobe.photoshop",
        ".ico": "image/x-icon",
        ".pcx": "image/x-pcx",
        ".tga": "image/x-tga",
        ".db": "application/x-sqlite3",
        ".sqlite": "application/x-sqlite3",
        ".sqlite3": "application/x-sqlite3",
        ".mdb": "application/x-msaccess",
        ".accdb": "application/x-msaccess",
        ".eml": "message/rfc822",
        ".msg": "application/vnd.ms-outlook",
        ".mbox": "application/mbox",
        ".ttf": "font/ttf",
        ".otf": "font/otf",
        ".woff": "font/woff",
        ".woff2": "font/woff2",
        ".dwg": "application/acad",
        ".dxf": "application/dxf",
        ".kmz": "application/vnd.google-earth.kmz",
        ".gpx": "application/gpx+xml",
        ".fit": "application/fit",
        ".iso": "application/x-iso9660-image",
        ".chm": "application/x-chm",
        ".djvu": "image/vnd.djvu",
        ".odt": "application/vnd.oasis.opendocument.text",
        ".ods": "application/vnd.oasis.opendocument.spreadsheet",
        ".odp": "application/vnd.oasis.opendocument.presentation",
        ".tex": "application/x-latex",
        ".dbf": "application/x-dbase",
        ".exe": "application/x-msdownload",
        ".dll": "application/x-msdownload",
        ".so": "application/x-sharedlib",
        ".elf": "application/x-elf",
        ".dcm": "application/dicom",
    }
    return MIME_MAP.get(ext.lower(), "application/octet-stream")


# ============================================================
# 基础解析器抽象
# ============================================================
class BaseParser:
    """解析器基类"""
    name: str = "base"
    priority: str = "P3"  # P0/P1/P2/P3
    supported_extensions: List[str] = []

    def can_parse(self, ext: str) -> bool:
        return ext.lower() in self.supported_extensions

    def parse(self, file_path: str) -> ParseResult:
        raise NotImplementedError


# ============================================================
# P0: 电子表格解析器 (Excel)
# ============================================================
class ExcelParser(BaseParser):
    """Excel 解析器 (.xlsx/.xls) — P0"""
    name = "excel"
    priority = "P0"
    supported_extensions = [".xlsx", ".xls", ".xlsm", ".xltx", ".xltm"]

    def parse(self, file_path: str) -> ParseResult:
        import time
        start = time.time()

        result = ParseResult(
            file_path=file_path,
            file_name=os.path.basename(file_path),
            extension=os.path.splitext(file_path)[1].lower(),
            file_size=os.path.getsize(file_path),
            mime_type=get_mime_type(os.path.splitext(file_path)[1]),
            parser_used="ExcelParser v1.0",
        )

        # 尝试 openpyxl (xlsx)，失败则 xlrd (xls)
        ok, openpyxl = safe_import("openpyxl")
        if ok:
            try:
                wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
                result.sheet_names = wb.sheetnames
                result.metadata["total_sheets"] = len(wb.sheetnames)

                all_text = []
                for sheet_name in wb.sheetnames:
                    ws = wb[sheet_name]
                    sheet_data = {"name": sheet_name, "rows": [], "max_row": ws.max_row, "max_col": ws.max_column}
                    for row in ws.iter_rows(max_row=min(ws.max_row or 0, 1000), values_only=True):
                        row_data = [str(cell) if cell is not None else "" for cell in row]
                        sheet_data["rows"].append(row_data)
                        all_text.append("\t".join(row_data))
                    result.tables.append(sheet_data)

                wb.close()
                result.raw_text = "\n".join(all_text[:5000])
                result.content_preview = result.raw_text[:1000]
                result.status = "success"
                result.parse_time_ms = (time.time() - start) * 1000
                return result
            except Exception as e:
                result.warnings.append(f"openpyxl 解析失败: {e}")

        # xls 降级
        ok, xlrd = safe_import("xlrd")
        if ok:
            try:
                wb = xlrd.open_workbook(file_path)
                result.sheet_names = wb.sheet_names()
                all_text = []
                for sheet_name in wb.sheet_names():
                    ws = wb.sheet_by_name(sheet_name)
                    for row_idx in range(min(ws.nrows, 1000)):
                        row_data = [str(ws.cell_value(row_idx, col_idx)) for col_idx in range(ws.ncols)]
                        all_text.append("\t".join(row_data))
                result.raw_text = "\n".join(all_text[:5000])
                result.content_preview = result.raw_text[:1000]
                result.status = "success"
                result.parse_time_ms = (time.time() - start) * 1000
                return result
            except Exception as e:
                result.warnings.append(f"xlrd 解析失败: {e}")

        # CSV 降级
        ok, pd = safe_import("pandas")
        if ok and file_path.endswith(('.xlsx', '.xls')):
            try:
                df = pd.read_excel(file_path, nrows=1000)
                result.raw_text = df.to_string()
                result.content_preview = result.raw_text[:1000]
                result.status = "partial"
                result.parse_time_ms = (time.time() - start) * 1000
                return result
            except Exception as e:
                result.warnings.append(f"pandas 降级解析失败: {e}")

        result.status = "error"
        result.errors.append("无法解析 Excel 文件，请安装 openpyxl 或 xlrd")
        result.parse_time_ms = (time.time() - start) * 1000
        return result


# ============================================================
# P0: 演示文稿解析器 (PowerPoint)
# ============================================================
class PowerPointParser(BaseParser):
    """PowerPoint 解析器 (.pptx/.ppt) — P0"""
    name = "powerpoint"
    priority = "P0"
    supported_extensions = [".pptx", ".ppt", ".pptm", ".potx"]

    def parse(self, file_path: str) -> ParseResult:
        import time
        start = time.time()

        result = ParseResult(
            file_path=file_path,
            file_name=os.path.basename(file_path),
            extension=os.path.splitext(file_path)[1].lower(),
            file_size=os.path.getsize(file_path),
            mime_type=get_mime_type(os.path.splitext(file_path)[1]),
            parser_used="PowerPointParser v1.0",
        )

        ok, pptx = safe_import("pptx")
        if not ok:
            ok, pptx = safe_import("python-pptx", "pptx")

        if ok:
            try:
                prs = pptx.Presentation(file_path)
                result.metadata["slide_count"] = len(prs.slides)
                result.metadata["slide_width"] = prs.slide_width
                result.metadata["slide_height"] = prs.slide_height

                all_text = []
                for i, slide in enumerate(prs.slides):
                    slide_text = []
                    for shape in slide.shapes:
                        if shape.has_text_frame:
                            for para in shape.text_frame.paragraphs:
                                text = para.text.strip()
                                if text:
                                    slide_text.append(text)
                    if slide_text:
                        all_text.append(f"--- 幻灯片 {i+1} ---\n" + "\n".join(slide_text))

                    # 提取图片信息
                    if shape.shape_type == 13:  # Picture
                        result.images.append({
                            "slide": i + 1,
                            "name": shape.name,
                            "width": shape.width,
                            "height": shape.height,
                        })

                result.raw_text = "\n\n".join(all_text)
                result.content_preview = result.raw_text[:1000]
                result.page_count = len(prs.slides)
                result.status = "success"
                result.parse_time_ms = (time.time() - start) * 1000
                return result
            except Exception as e:
                result.warnings.append(f"python-pptx 解析失败: {e}")

        result.status = "error"
        result.errors.append("无法解析 PowerPoint 文件，请安装 python-pptx")
        result.parse_time_ms = (time.time() - start) * 1000
        return result


# ============================================================
# P0: 压缩包解析器 (ZIP/RAR/7Z/TAR/GZ/BZ2/XZ/ISO)
# ============================================================
class ArchiveParser(BaseParser):
    """压缩包解析器 — P0/P1"""
    name = "archive"
    priority = "P0"
    supported_extensions = [
        ".zip", ".rar", ".7z", ".tar", ".gz", ".tgz",
        ".bz2", ".tbz2", ".xz", ".txz", ".iso",
    ]

    def parse(self, file_path: str) -> ParseResult:
        import time
        start = time.time()
        ext = os.path.splitext(file_path)[1].lower()

        result = ParseResult(
            file_path=file_path,
            file_name=os.path.basename(file_path),
            extension=ext,
            file_size=os.path.getsize(file_path),
            mime_type=get_mime_type(ext),
            parser_used="ArchiveParser v1.0",
        )

        files_list = []
        total_size = 0

        # ZIP
        if ext == ".zip":
            import zipfile
            try:
                with zipfile.ZipFile(file_path, "r") as zf:
                    for info in zf.infolist():
                        files_list.append({
                            "name": info.filename,
                            "size": info.file_size,
                            "compressed": info.compress_size,
                            "is_dir": info.is_dir(),
                            "modified": datetime(*info.date_time).isoformat() if info.date_time else "",
                        })
                        total_size += info.file_size
                result.archive_files = [f["name"] for f in files_list]
                result.metadata["total_files"] = len(files_list)
                result.metadata["total_size"] = total_size
                result.metadata["archive_type"] = "zip"
                result.raw_text = "\n".join([
                    f"{f['name']} ({f['size']} bytes)" for f in files_list[:500]
                ])
                result.content_preview = result.raw_text[:1000]
                result.status = "success"
            except Exception as e:
                result.errors.append(f"ZIP 解析失败: {e}")
                result.status = "error"

        # RAR
        elif ext == ".rar":
            ok, rarfile = safe_import("rarfile")
            if ok:
                try:
                    with rarfile.RarFile(file_path, "r") as rf:
                        for info in rf.infolist():
                            files_list.append({
                                "name": info.filename,
                                "size": info.file_size,
                                "compressed": info.compress_size,
                                "is_dir": info.isdir(),
                            })
                            total_size += info.file_size
                    result.archive_files = [f["name"] for f in files_list]
                    result.metadata["total_files"] = len(files_list)
                    result.metadata["total_size"] = total_size
                    result.metadata["archive_type"] = "rar"
                    result.raw_text = "\n".join([
                        f"{f['name']} ({f['size']} bytes)" for f in files_list[:500]
                    ])
                    result.content_preview = result.raw_text[:1000]
                    result.status = "success"
                except Exception as e:
                    result.errors.append(f"RAR 解析失败: {e}")
                    result.status = "error"
            else:
                result.errors.append("RAR 解析需要安装 rarfile，请执行 pip install rarfile")
                result.status = "unsupported"

        # 7Z
        elif ext == ".7z":
            ok, py7zr = safe_import("py7zr")
            if ok:
                try:
                    with py7zr.SevenZipFile(file_path, "r") as szf:
                        all_info = szf.getnames()
                        for name in all_info:
                            files_list.append({"name": name, "size": 0})
                    result.archive_files = all_info
                    result.metadata["total_files"] = len(all_info)
                    result.metadata["archive_type"] = "7z"
                    result.raw_text = "\n".join(all_info[:500])
                    result.content_preview = result.raw_text[:1000]
                    result.status = "success"
                except Exception as e:
                    result.errors.append(f"7Z 解析失败: {e}")
                    result.status = "error"
            else:
                result.errors.append("7Z 解析需要安装 py7zr，请执行 pip install py7zr")
                result.status = "unsupported"

        # TAR
        elif ext in [".tar", ".gz", ".tgz", ".bz2", ".tbz2", ".xz", ".txz"]:
            import tarfile
            mode_map = {
                ".tar": "r", ".gz": "r:gz", ".tgz": "r:gz",
                ".bz2": "r:bz2", ".tbz2": "r:bz2", ".xz": "r:xz", ".txz": "r:xz",
            }
            try:
                mode = mode_map.get(ext, "r:*")
                with tarfile.open(file_path, mode) as tf:
                    for member in tf.getmembers():
                        files_list.append({
                            "name": member.name,
                            "size": member.size,
                            "is_dir": member.isdir(),
                        })
                        total_size += member.size
                result.archive_files = [f["name"] for f in files_list]
                result.metadata["total_files"] = len(files_list)
                result.metadata["total_size"] = total_size
                result.metadata["archive_type"] = ext.lstrip(".")
                result.raw_text = "\n".join([
                    f"{f['name']} ({f['size']} bytes)" for f in files_list[:500]
                ])
                result.content_preview = result.raw_text[:1000]
                result.status = "success"
            except Exception as e:
                result.errors.append(f"TAR 解析失败: {e}")
                result.status = "error"

        # ISO
        elif ext == ".iso":
            ok, pycdlib = safe_import("pycdlib")
            if ok:
                try:
                    iso = pycdlib.PyCdlib()
                    iso.open(file_path)
                    for dirname, dirlist, filelist in iso.walk("/"):
                        for f in filelist:
                            files_list.append({"name": os.path.join(dirname, f), "size": 0})
                    iso.close()
                    result.archive_files = [f["name"] for f in files_list]
                    result.metadata["total_files"] = len(files_list)
                    result.metadata["archive_type"] = "iso"
                    result.raw_text = "\n".join([f["name"] for f in files_list[:500]])
                    result.content_preview = result.raw_text[:1000]
                    result.status = "success"
                except Exception as e:
                    result.warnings.append(f"ISO 完整解析失败: {e}")
                    result.status = "partial"
            else:
                result.status = "unsupported"

        result.parse_time_ms = (time.time() - start) * 1000
        return result


# ============================================================
# P0: 数据库解析器 (SQLite)
# ============================================================
class DatabaseParser(BaseParser):
    """数据库解析器 — P0"""
    name = "database"
    priority = "P0"
    supported_extensions = [".db", ".sqlite", ".sqlite3", ".mdb", ".accdb"]

    def parse(self, file_path: str) -> ParseResult:
        import time
        start = time.time()
        ext = os.path.splitext(file_path)[1].lower()

        result = ParseResult(
            file_path=file_path,
            file_name=os.path.basename(file_path),
            extension=ext,
            file_size=os.path.getsize(file_path),
            mime_type=get_mime_type(ext),
            parser_used="DatabaseParser v1.0",
        )

        if ext in [".db", ".sqlite", ".sqlite3"]:
            import sqlite3
            try:
                conn = sqlite3.connect(f"file:{file_path}?mode=ro", uri=True)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                result.metadata["tables"] = tables
                result.metadata["table_count"] = len(tables)

                all_text = []
                for table in tables[:10]:  # 限制前10个表
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM [{table}]")
                        row_count = cursor.fetchone()[0]
                        cursor.execute(f"SELECT * FROM [{table}] LIMIT 100")
                        columns = [desc[0] for desc in cursor.description]
                        rows = cursor.fetchall()
                        table_data = {
                            "name": table,
                            "columns": columns,
                            "row_count": row_count,
                            "sample_rows": [dict(zip(columns, map(str, row))) for row in rows],
                        }
                        result.tables.append(table_data)
                        all_text.append(f"表: {table} ({row_count}行, {len(columns)}列)")
                        all_text.append(" | ".join(columns))
                        for row in rows[:20]:
                            all_text.append(" | ".join(map(str, row)))
                    except Exception as e:
                        result.warnings.append(f"表 {table} 读取失败: {e}")

                conn.close()
                result.raw_text = "\n".join(all_text[:5000])
                result.content_preview = result.raw_text[:1000]
                result.status = "success"
            except Exception as e:
                result.errors.append(f"SQLite 解析失败: {e}")
                result.status = "error"

        elif ext in [".mdb", ".accdb"]:
            result.status = "unsupported"
            result.errors.append("MS Access 解析暂时需要 pyodbc+pandas_access，或使用 mdbtools CLI")

        result.parse_time_ms = (time.time() - start) * 1000
        return result


# ============================================================
# P1: 图片深度解析器 (HEIC/TIFF/RAW/PSD + EXIF/OCR)
# ============================================================
class ImageDeepParser(BaseParser):
    """图片深度解析器 — P1/P2"""
    name = "image_deep"
    priority = "P1"
    supported_extensions = [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg",
        ".tiff", ".tif", ".heic", ".heif", ".raw", ".cr2", ".nef",
        ".psd", ".ico", ".pcx", ".tga", ".dcm",
    ]

    def parse(self, file_path: str) -> ParseResult:
        import time
        start = time.time()
        ext = os.path.splitext(file_path)[1].lower()

        result = ParseResult(
            file_path=file_path,
            file_name=os.path.basename(file_path),
            extension=ext,
            file_size=os.path.getsize(file_path),
            mime_type=get_mime_type(ext),
            parser_used="ImageDeepParser v1.0",
        )

        try:
            from PIL import Image, ExifTags, TiffImagePlugin

            # HEIC 特殊处理
            if ext in [".heic", ".heif"]:
                ok, pillow_heif = safe_import("pillow_heif")
                if ok:
                    pillow_heif.register_heif_opener()
                else:
                    result.warnings.append("HEIC 需要 pillow-heif，请执行 pip install pillow-heif")

            img = Image.open(file_path)
            result.metadata["width"] = img.width
            result.metadata["height"] = img.height
            result.metadata["mode"] = img.mode
            result.metadata["format"] = img.format
            result.metadata["is_animated"] = getattr(img, "is_animated", False)

            # 多帧 (GIF/动图)
            frame_count = getattr(img, "n_frames", 1)
            if frame_count > 1:
                result.metadata["frames"] = frame_count

            # EXIF 元数据
            exif_data = {}
            try:
                exif = img._getexif()
                if exif:
                    for tag_id, value in exif.items():
                        tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
                        exif_data[tag_name] = str(value)

                    # 拍摄时间
                    if "DateTimeOriginal" in exif_data:
                        result.metadata["taken_at"] = exif_data["DateTimeOriginal"]
                    # GPS
                    if "GPSInfo" in exif_data:
                        result.metadata["gps"] = exif_data["GPSInfo"]
                    # 设备
                    if "Make" in exif_data:
                        result.metadata["camera_make"] = exif_data["Make"]
                    if "Model" in exif_data:
                        result.metadata["camera_model"] = exif_data["Model"]
            except Exception:
                pass
            result.metadata["exif"] = exif_data

            # 颜色分析
            if img.mode in ["RGB", "RGBA"]:
                img_small = img.resize((50, 50))
                pixels = list(img_small.getdata())
                dominant_colors = self._get_dominant_colors(pixels)
                result.metadata["dominant_colors"] = dominant_colors
            else:
                result.metadata["dominant_colors"] = []

            # 图片哈希 (相似度检测用)
            img_hash = self._image_hash(file_path)
            result.metadata["perceptual_hash"] = img_hash

            # SHA256
            result.metadata["sha256"] = get_file_hash(file_path)

            img.close()
            result.status = "success"
        except Exception as e:
            result.errors.append(f"图片解析失败: {e}")
            result.status = "error"

        result.parse_time_ms = (time.time() - start) * 1000
        return result

    def _get_dominant_colors(self, pixels: list[Any], n: int = 5) -> List[str]:
        """提取主色调"""
        from collections import Counter
        # 量化颜色
        quantized = [
            f"#{r//32*32:02x}{g//32*32:02x}{b//32*32:02x}"
            for pixel in pixels
            for r, g, b in [pixel[:3]]
        ]
        counter = Counter(quantized)
        return [color for color, _ in counter.most_common(n)]

    def _image_hash(self, file_path: str) -> str:
        """感知哈希"""
        ok, imagehash = safe_import("imagehash")
        if ok:
            try:
                from PIL import Image
                img = Image.open(file_path)
                return str(imagehash.average_hash(img))
            except Exception:
                pass
        return ""


# ============================================================
# P1: 音频解析器
# ============================================================
class AudioParser(BaseParser):
    """音频解析器 — P1"""
    name = "audio"
    priority = "P1"
    supported_extensions = [
        ".mp3", ".wav", ".flac", ".aac", ".ogg", ".oga",
        ".m4a", ".wma", ".aiff", ".aif", ".aifc", ".opus",
    ]

    def parse(self, file_path: str) -> ParseResult:
        import time
        start = time.time()
        ext = os.path.splitext(file_path)[1].lower()

        result = ParseResult(
            file_path=file_path,
            file_name=os.path.basename(file_path),
            extension=ext,
            file_size=os.path.getsize(file_path),
            mime_type=get_mime_type(ext),
            parser_used="AudioParser v1.0",
        )

        audio_info = {}

        # mutagen (最佳, 支持最多格式)
        ok, mutagen = safe_import("mutagen")
        if ok:
            try:
                af = mutagen.File(file_path)
                if af is not None:
                    audio_info["length_seconds"] = getattr(af.info, "length", 0)
                    audio_info["bitrate"] = getattr(af.info, "bitrate", 0)
                    audio_info["channels"] = getattr(af.info, "channels", 0)
                    audio_info["sample_rate"] = getattr(af.info, "sample_rate", 0)
                    audio_info["bit_depth"] = getattr(af.info, "bits_per_sample", 0)
                    audio_info["codec"] = type(af).__name__

                    # 标签
                    tags = {}
                    if hasattr(af, "tags") and af.tags:
                        for key, value in af.tags.items():
                            tags[key] = str(value)
                    audio_info["tags"] = tags
                    result.metadata["title"] = tags.get("TIT2", tags.get("\xa9nam", ""))
                    result.metadata["artist"] = tags.get("TPE1", tags.get("\xa9ART", ""))
                    result.metadata["album"] = tags.get("TALB", tags.get("\xa9alb", ""))
            except Exception as e:
                result.warnings.append(f"mutagen 解析失败: {e}")

        # wave (WAV)
        if ext == ".wav":
            import wave
            try:
                with wave.open(file_path, "rb") as wf:
                    audio_info["channels"] = wf.getnchannels()
                    audio_info["sample_width"] = wf.getsampwidth()
                    audio_info["sample_rate"] = wf.getframerate()
                    audio_info["frames"] = wf.getnframes()
                    if audio_info.get("length_seconds", 0) == 0 and audio_info.get("sample_rate"):
                        audio_info["length_seconds"] = audio_info["frames"] / audio_info["sample_rate"]
            except Exception as e:
                result.warnings.append(f"wave 解析失败: {e}")

        result.audio_info = audio_info
        result.metadata["audio"] = audio_info

        # 简单内容描述
        duration = audio_info.get("length_seconds", 0)
        mins, secs = divmod(int(duration), 60)
        result.raw_text = f"音频文件: {result.file_name}\n时长: {mins}分{secs}秒\n"
        result.raw_text += f"采样率: {audio_info.get('sample_rate', 'N/A')} Hz\n"
        result.raw_text += f"比特率: {audio_info.get('bitrate', 'N/A')} bps\n"
        result.raw_text += f"声道: {audio_info.get('channels', 'N/A')}\n"
        result.content_preview = result.raw_text

        if audio_info:
            result.status = "success"
        else:
            result.status = "partial"

        result.parse_time_ms = (time.time() - start) * 1000
        return result


# ============================================================
# P1: 视频解析器
# ============================================================
class VideoParser(BaseParser):
    """视频解析器 — P1"""
    name = "video"
    priority = "P1"
    supported_extensions = [
        ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv",
        ".webm", ".mpeg", ".mpg", ".m4v", ".3gp", ".ts",
    ]

    def parse(self, file_path: str) -> ParseResult:
        import time
        start = time.time()
        ext = os.path.splitext(file_path)[1].lower()

        result = ParseResult(
            file_path=file_path,
            file_name=os.path.basename(file_path),
            extension=ext,
            file_size=os.path.getsize(file_path),
            mime_type=get_mime_type(ext),
            parser_used="VideoParser v1.0",
        )

        video_info = {}

        # moviepy
        ok, moviepy = safe_import("moviepy")
        if ok:
            try:
                clip = moviepy.VideoFileClip(file_path)
                video_info["duration_seconds"] = clip.duration
                video_info["width"] = clip.w
                video_info["height"] = clip.height
                video_info["fps"] = clip.fps
                video_info["frame_count"] = int(clip.fps * clip.duration) if clip.fps else 0
                if clip.audio:
                    video_info["has_audio"] = True
                clip.close()
            except Exception as e:
                result.warnings.append(f"moviepy 解析失败: {e}")

        # FFprobe 降级
        if not video_info:
            try:
                import json as _json
                cmd = [
                    "ffprobe", "-v", "quiet", "-print_format", "json",
                    "-show_format", "-show_streams", file_path,
                ]
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if proc.returncode == 0:
                    data = _json.loads(proc.stdout)
                    fmt = data.get("format", {})
                    video_info["duration_seconds"] = float(fmt.get("duration", 0))
                    video_info["bitrate"] = fmt.get("bit_rate", 0)
                    video_info["format_name"] = fmt.get("format_name", "")
                    for stream in data.get("streams", []):
                        if stream.get("codec_type") == "video":
                            video_info["width"] = stream.get("width", 0)
                            video_info["height"] = stream.get("height", 0)
                            video_info["codec"] = stream.get("codec_name", "")
                            video_info["fps"] = eval(stream.get("r_frame_rate", "0"))
                        elif stream.get("codec_type") == "audio":
                            video_info["audio_codec"] = stream.get("codec_name", "")
            except Exception as e:
                result.warnings.append(f"FFprobe 降级解析失败: {e}")

        result.video_info = video_info
        result.metadata["video"] = video_info

        duration = video_info.get("duration_seconds", 0)
        mins, secs = divmod(int(duration), 60)
        hours, mins = divmod(mins, 60)
        time_str = f"{hours}时{mins}分{secs}秒" if hours else f"{mins}分{secs}秒"

        result.raw_text = (
            f"视频文件: {result.file_name}\n"
            f"时长: {time_str}\n"
            f"分辨率: {video_info.get('width', 'N/A')}x{video_info.get('height', 'N/A')}\n"
            f"帧率: {video_info.get('fps', 'N/A')} fps\n"
            f"编码: {video_info.get('codec', 'N/A')}\n"
        )
        result.content_preview = result.raw_text

        if video_info:
            result.status = "success"
        else:
            result.status = "partial"

        result.parse_time_ms = (time.time() - start) * 1000
        return result


# ============================================================
# P2: 电子书解析器 (EPUB/MOBI)
# ============================================================
class EBookParser(BaseParser):
    """电子书解析器 — P2"""
    name = "ebook"
    priority = "P2"
    supported_extensions = [".epub", ".mobi", ".azw", ".azw3"]

    def parse(self, file_path: str) -> ParseResult:
        import time
        start = time.time()
        ext = os.path.splitext(file_path)[1].lower()

        result = ParseResult(
            file_path=file_path,
            file_name=os.path.basename(file_path),
            extension=ext,
            file_size=os.path.getsize(file_path),
            mime_type=get_mime_type(ext),
            parser_used="EBookParser v1.0",
        )

        if ext == ".epub":
            ok, ebooklib = safe_import("ebooklib")
            if ok:
                try:
                    book = ebooklib.epub.read_epub(file_path)
                    result.metadata["title"] = book.get_metadata("DC", "title")
                    result.metadata["creator"] = book.get_metadata("DC", "creator")
                    result.metadata["language"] = book.get_metadata("DC", "language")

                    all_text = []
                    for item in book.get_items():
                        if item.get_type() == ebooklib.ITEM_DOCUMENT:
                            try:
                                content = item.get_content().decode("utf-8", errors="ignore")
                                # 简单去标签
                                clean = re.sub(r"<[^>]+>", " ", content)
                                clean = re.sub(r"\s+", " ", clean).strip()
                                if clean:
                                    all_text.append(clean)
                            except Exception:
                                pass

                    result.raw_text = "\n\n".join(all_text[:100])
                    result.content_preview = result.raw_text[:1000]
                    result.page_count = len(all_text)
                    result.status = "success"
                except Exception as e:
                    result.errors.append(f"EPUB 解析失败: {e}")
                    result.status = "error"
            else:
                result.status = "unsupported"
                result.errors.append("EPUB 解析需要 ebooklib，请执行 pip install ebooklib")

        elif ext in [".mobi", ".azw", ".azw3"]:
            result.status = "unsupported"
            result.errors.append("MOBI 解析需要额外工具，建议先用 Calibre 转换为 EPUB")

        result.parse_time_ms = (time.time() - start) * 1000
        return result


# ============================================================
# P2: 邮件解析器
# ============================================================
class EmailParser(BaseParser):
    """邮件解析器 — P2"""
    name = "email"
    priority = "P2"
    supported_extensions = [".eml", ".msg", ".mbox"]

    def parse(self, file_path: str) -> ParseResult:
        import time
        start = time.time()
        ext = os.path.splitext(file_path)[1].lower()

        result = ParseResult(
            file_path=file_path,
            file_name=os.path.basename(file_path),
            extension=ext,
            file_size=os.path.getsize(file_path),
            mime_type=get_mime_type(ext),
            parser_used="EmailParser v1.0",
        )

        if ext == ".eml":
            import email
            from email import policy
            try:
                with open(file_path, "rb") as f:
                    msg = email.message_from_binary_file(f, policy=policy.default)

                result.metadata["subject"] = msg.get("Subject", "")
                result.metadata["from"] = msg.get("From", "")
                result.metadata["to"] = msg.get("To", "")
                result.metadata["date"] = msg.get("Date", "")
                result.metadata["cc"] = msg.get("Cc", "")
                result.metadata["message_id"] = msg.get("Message-ID", "")

                body_parts = []
                attachments = []
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/plain":
                            try:
                                body = part.get_content()
                                if body:
                                    body_parts.append(str(body))
                            except Exception:
                                pass
                        elif part.get("Content-Disposition") and "attachment" in part.get("Content-Disposition"):
                            attachments.append(part.get_filename() or "unnamed")
                else:
                    try:
                        body = msg.get_content()
                        if body:
                            body_parts.append(str(body))
                    except Exception:
                        pass

                result.raw_text = "\n".join(body_parts[:50])
                result.content_preview = result.raw_text[:1000]
                result.metadata["attachments"] = attachments
                result.status = "success"
            except Exception as e:
                result.errors.append(f"EML 解析失败: {e}")
                result.status = "error"

        elif ext == ".mbox":
            import mailbox
            try:
                mbox = mailbox.mbox(file_path)
                result.metadata["message_count"] = len(mbox)
                preview = []
                for i, msg in enumerate(mbox):
                    if i >= 10:
                        break
                    preview.append(f"[{i+1}] {msg.get('Subject', '(无主题)')} — {msg.get('From', '')}")
                result.raw_text = "\n".join(preview)
                result.content_preview = result.raw_text[:1000]
                result.status = "success"
            except Exception as e:
                result.errors.append(f"MBOX 解析失败: {e}")
                result.status = "error"

        elif ext == ".msg":
            result.status = "unsupported"
            result.errors.append("MSG 解析需要 extract-msg，请执行 pip install extract-msg")

        result.parse_time_ms = (time.time() - start) * 1000
        return result


# ============================================================
# P2: 字体解析器
# ============================================================
class FontParser(BaseParser):
    """字体解析器 — P3"""
    name = "font"
    priority = "P3"
    supported_extensions = [".ttf", ".otf", ".woff", ".woff2"]

    def parse(self, file_path: str) -> ParseResult:
        import time
        start = time.time()
        ext = os.path.splitext(file_path)[1].lower()

        result = ParseResult(
            file_path=file_path,
            file_name=os.path.basename(file_path),
            extension=ext,
            file_size=os.path.getsize(file_path),
            mime_type=get_mime_type(ext),
            parser_used="FontParser v1.0",
        )

        ok, fonttools = safe_import("fontTools")
        if ok:
            try:
                from fontTools.ttLib import TTFont
                font = TTFont(file_path)
                name_records = {}
                for record in font["name"].names:
                    try:
                        name_records[record.nameID] = record.toUnicode()
                    except Exception:
                        pass

                result.metadata["family"] = name_records.get(1, "")
                result.metadata["subfamily"] = name_records.get(2, "")
                result.metadata["full_name"] = name_records.get(4, "")
                result.metadata["version"] = name_records.get(5, "")
                result.metadata["postscript"] = name_records.get(6, "")
                result.metadata["copyright"] = name_records.get(0, "")

                # 字符集
                cmap = font.getBestCmap()
                result.metadata["glyph_count"] = len(cmap) if cmap else 0
                result.metadata["tables"] = list(font.keys())

                result.raw_text = f"字体: {result.metadata.get('full_name', 'N/A')}\n"
                result.raw_text += f"家族: {result.metadata.get('family', 'N/A')} {result.metadata.get('subfamily', '')}\n"
                result.raw_text += f"字形数: {result.metadata.get('glyph_count', 'N/A')}\n"
                result.content_preview = result.raw_text
                result.status = "success"
            except Exception as e:
                result.errors.append(f"字体解析失败: {e}")
                result.status = "error"
        else:
            result.status = "unsupported"
            result.errors.append("字体解析需要 fonttools，请执行 pip install fonttools")

        result.parse_time_ms = (time.time() - start) * 1000
        return result


# ============================================================
# P2: 代码/文本解析器 (深度)
# ============================================================
class CodeDeepParser(BaseParser):
    """代码深度解析器"""
    name = "code_deep"
    priority = "P2"
    supported_extensions = [
        ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".c", ".cpp", ".h", ".hpp",
        ".go", ".rs", ".rb", ".php", ".swift", ".kt", ".scala", ".cs",
        ".sh", ".bash", ".zsh", ".ps1", ".bat",
        ".html", ".htm", ".css", ".scss", ".sass", ".less",
        ".sql", ".json", ".yaml", ".yml", ".xml", ".toml", ".ini", ".cfg",
        ".md", ".rst", ".tex", ".r", ".m", ".lua", ".pl", ".dart",
        ".dockerfile", ".makefile", ".cmake", ".gradle",
    ]

    def parse(self, file_path: str) -> ParseResult:
        import time
        start = time.time()
        ext = os.path.splitext(file_path)[1].lower()

        result = ParseResult(
            file_path=file_path,
            file_name=os.path.basename(file_path),
            extension=ext,
            file_size=os.path.getsize(file_path),
            mime_type="text/plain",
            parser_used="CodeDeepParser v1.0",
        )

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            lines = content.split("\n")
            result.metadata["lines"] = len(lines)
            result.metadata["chars"] = len(content)
            result.metadata["language"] = self._detect_language(ext)
            result.metadata["encoding"] = "utf-8"

            # 基础代码统计
            code_lines = [l for l in lines if l.strip() and not l.strip().startswith(("#", "//", "/*", "*", "--", "REM"))]
            result.metadata["code_lines"] = len(code_lines)
            result.metadata["comment_lines"] = len(lines) - len(code_lines) if lines else 0

            # 函数/类识别
            result.metadata["functions"] = self._extract_functions(ext, content)
            result.metadata["classes"] = self._extract_classes(ext, content)
            result.metadata["imports"] = self._extract_imports(ext, content)

            result.raw_text = content[:10000]
            result.content_preview = content[:1000]
            result.status = "success"
        except Exception as e:
            result.errors.append(f"代码解析失败: {e}")
            result.status = "error"

        result.parse_time_ms = (time.time() - start) * 1000
        return result

    def _detect_language(self, ext: str) -> str:
        lang_map = {
            ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
            ".java": "Java", ".c": "C", ".cpp": "C++", ".h": "C/C++ Header",
            ".go": "Go", ".rs": "Rust", ".rb": "Ruby", ".php": "PHP",
            ".swift": "Swift", ".kt": "Kotlin", ".sh": "Shell",
            ".html": "HTML", ".css": "CSS",
            ".sql": "SQL", ".json": "JSON", ".yaml": "YAML",
            ".md": "Markdown", ".tex": "LaTeX",
        }
        return lang_map.get(ext, "Unknown")

    def _extract_functions(self, ext: str, content: str) -> List[str]:
        patterns = {
            ".py": r"^\s*def\s+(\w+)",
            ".js": r"(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\(|(\w+)\s*=\s*(?:async\s*)?\()",
            ".ts": r"(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\(|(\w+)\s*=\s*(?:async\s*)?\()",
            ".go": r"^\s*func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)",
            ".rs": r"^\s*(?:pub\s+)?fn\s+(\w+)",
            ".java": r"(?:public|private|protected)\s+(?:static\s+)?\w+\s+(\w+)\s*\(",
            ".c": r"^\s*\w+\s+(\w+)\s*\([^)]*\)\s*\{",
            ".cpp": r"^\s*\w+(?:::)?\s+(\w+)\s*\([^)]*\)\s*(?:const\s*)?\{",
        }
        pattern = patterns.get(ext, r"def\s+(\w+)|function\s+(\w+)")
        matches = re.findall(pattern, content, re.MULTILINE)
        # 处理分组匹配
        funcs = []
        for m in matches:
            if isinstance(m, tuple):
                funcs.extend([x for x in m if x])
            else:
                funcs.append(m)
        return funcs[:50]

    def _extract_classes(self, ext: str, content: str) -> List[str]:
        patterns = {
            ".py": r"^\s*class\s+(\w+)",
            ".js": r"class\s+(\w+)",
            ".ts": r"class\s+(\w+)",
            ".java": r"(?:public\s+)?class\s+(\w+)",
            ".cpp": r"class\s+(\w+)",
        }
        pattern = patterns.get(ext, r"class\s+(\w+)")
        return re.findall(pattern, content, re.MULTILINE)[:50]

    def _extract_imports(self, ext: str, content: str) -> List[str]:
        patterns = {
            ".py": r"^(?:import\s+(\S+)|from\s+(\S+)\s+import)",
            ".js": r"(?:import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]|require\(['\"]([^'\"]+)['\"]\))",
            ".ts": r"import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]",
            ".go": r"import\s+(?:\"\S+\"|\(",
            ".java": r"import\s+([\w.]+)",
        }
        pattern = patterns.get(ext)
        if pattern:
            matches = re.findall(pattern, content, re.MULTILINE)
            if matches:
                if isinstance(matches[0], tuple):
                    return [x for m in matches for x in m if x][:50]
                return list(set(matches))[:50]
        return []


# ============================================================
# 文档解析器 (PDF/DOCX/ODF/TEX/CHM/DJVU)
# ============================================================
class DocumentParser(BaseParser):
    """通用文档解析器"""
    name = "document"
    priority = "P1"
    supported_extensions = [
        ".pdf", ".docx", ".doc", ".odt", ".ods", ".odp", ".tex", ".rtf",
        ".chm", ".djvu", ".dcm",
    ]

    def parse(self, file_path: str) -> ParseResult:
        import time
        start = time.time()
        ext = os.path.splitext(file_path)[1].lower()

        result = ParseResult(
            file_path=file_path,
            file_name=os.path.basename(file_path),
            extension=ext,
            file_size=os.path.getsize(file_path),
            mime_type=get_mime_type(ext),
            parser_used="DocumentParser v1.0",
        )

        # PDF
        if ext == ".pdf":
            result = self._parse_pdf(file_path, result)

        # DOCX
        elif ext == ".docx":
            result = self._parse_docx(file_path, result)

        # DOC (旧格式)
        elif ext == ".doc":
            result = self._parse_doc(file_path, result)

        # ODT/ODS/ODP
        elif ext in [".odt", ".ods", ".odp"]:
            result = self._parse_odf(file_path, result)

        # LaTeX
        elif ext == ".tex":
            result = self._parse_latex(file_path, result)

        # RTF
        elif ext == ".rtf":
            result = self._parse_text_file(file_path, result)

        # CHM/DJVU/DCM
        else:
            result.status = "unsupported"
            result.errors.append(f"格式 {ext} 暂不支持深度解析")

        result.parse_time_ms = (time.time() - start) * 1000
        return result

    def _parse_pdf(self, file_path: str, result: ParseResult) -> ParseResult:
        """PDF解析 — 多引擎降级"""
        # 引擎1: PyPDF2/pypdf
        ok, pypdf = safe_import("pypdf")
        if not ok:
            ok, pypdf = safe_import("PyPDF2")

        if ok:
            try:
                reader = pypdf.PdfReader(file_path)
                result.metadata["pages"] = len(reader.pages)
                result.metadata["pdf_version"] = reader.metadata.get("/Version", "unknown") if reader.metadata else "unknown"

                # 元数据
                if reader.metadata:
                    result.metadata["title"] = str(reader.metadata.get("/Title", ""))
                    result.metadata["author"] = str(reader.metadata.get("/Author", ""))
                    result.metadata["subject"] = str(reader.metadata.get("/Subject", ""))
                    result.metadata["creator"] = str(reader.metadata.get("/Creator", ""))

                # 提取文本
                all_text = []
                for page in reader.pages[:100]:  # 限制100页
                    text = page.extract_text()
                    if text:
                        all_text.append(text)

                result.raw_text = "\n\n".join(all_text)
                result.content_preview = result.raw_text[:1000]
                result.page_count = len(reader.pages)
                result.status = "success"
                return result
            except Exception as e:
                result.warnings.append(f"PyPDF2 解析失败: {e}")

        # 引擎2: pdfplumber (更好的表格支持)
        ok, pdfplumber = safe_import("pdfplumber")
        if ok:
            try:
                with pdfplumber.open(file_path) as pdf:
                    result.metadata["pages"] = len(pdf.pages)
                    all_text = []
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            all_text.append(text)
                        # 提取表格
                        tables = page.extract_tables()
                        for table in tables:
                            if table:
                                result.tables.append({
                                    "page": page.page_number,
                                    "data": [[str(c) if c else "" for c in row] for row in table],
                                })
                    result.raw_text = "\n\n".join(all_text)
                    if not result.content_preview:
                        result.content_preview = result.raw_text[:1000]
                    result.page_count = len(pdf.pages)
                    result.status = "success"
                    return result
            except Exception as e:
                result.warnings.append(f"pdfplumber 解析失败: {e}")

        result.status = "error"
        result.errors.append("PDF 解析失败，请安装 pypdf 或 pdfplumber")
        return result

    def _parse_docx(self, file_path: str, result: ParseResult) -> ParseResult:
        """DOCX解析"""
        ok, docx = safe_import("docx")
        if not ok:
            ok, docx = safe_import("python-docx", "docx")

        if ok:
            try:
                doc = docx.Document(file_path)
                all_text = []
                for para in doc.paragraphs:
                    if para.text.strip():
                        all_text.append(para.text)
                result.raw_text = "\n".join(all_text)
                result.content_preview = result.raw_text[:1000]
                result.metadata["paragraphs"] = len(doc.paragraphs)
                result.status = "success"
                return result
            except Exception as e:
                result.warnings.append(f"python-docx 解析失败: {e}")

        result.status = "error"
        result.errors.append("DOCX 解析失败，请安装 python-docx")
        return result

    def _parse_doc(self, file_path: str, result: ParseResult) -> ParseResult:
        """DOC 旧格式 — 尝试 antiword 或 textract"""
        try:
            proc = subprocess.run(["antiword", file_path], capture_output=True, text=True, timeout=30)
            if proc.returncode == 0:
                result.raw_text = proc.stdout[:10000]
                result.content_preview = result.raw_text[:1000]
                result.status = "success"
                return result
        except FileNotFoundError:
            pass
        except Exception as e:
            result.warnings.append(f"antiword 失败: {e}")

        result.status = "unsupported"
        result.errors.append("DOC 解析需要 antiword 工具或 libreoffice --headless 转换")
        return result

    def _parse_odf(self, file_path: str, result: ParseResult) -> ParseResult:
        """ODF 格式"""
        ok, odf = safe_import("odf")
        if ok:
            try:
                # ODF 是 XML 格式，可以直接作为 ZIP 读取 content.xml
                import zipfile
                with zipfile.ZipFile(file_path, "r") as zf:
                    if "content.xml" in zf.namelist():
                        content = zf.read("content.xml").decode("utf-8", errors="ignore")
                        # 去标签
                        clean = re.sub(r"<[^>]+>", " ", content)
                        clean = re.sub(r"\s+", " ", clean).strip()
                        result.raw_text = clean[:10000]
                        result.content_preview = result.raw_text[:1000]
                        result.status = "success"
                        return result
            except Exception as e:
                result.warnings.append(f"ODF 解析失败: {e}")

        result.status = "unsupported"
        result.errors.append("ODF 解析需要 odfpy，请执行 pip install odfpy")
        return result

    def _parse_latex(self, file_path: str, result: ParseResult) -> ParseResult:
        """LaTeX 解析"""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # 去除 LaTeX 命令但保留文本
            clean = re.sub(r"\\begin\{[^}]*\}|\\end\{[^}]*\}", "", content)
            clean = re.sub(r"\\(?:textbf|textit|emph|section|subsection|chapter)\{([^}]*)\}", r"\1", clean)
            clean = re.sub(r"\\\w+", "", clean)
            clean = re.sub(r"[{}]", "", clean)
            clean = re.sub(r"\s+", " ", clean).strip()

            result.raw_text = clean[:10000]
            result.content_preview = result.raw_text[:1000]

            # 提取元数据
            title_match = re.search(r"\\title\{([^}]*)\}", content)
            author_match = re.search(r"\\author\{([^}]*)\}", content)
            if title_match:
                result.metadata["title"] = title_match.group(1)
            if author_match:
                result.metadata["author"] = author_match.group(1)

            result.status = "success"
        except Exception as e:
            result.errors.append(f"LaTeX 解析失败: {e}")
            result.status = "error"

        return result

    def _parse_text_file(self, file_path: str, result: ParseResult) -> ParseResult:
        """纯文本文件"""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            result.raw_text = content[:10000]
            result.content_preview = content[:1000]
            result.metadata["chars"] = len(content)
            result.status = "success"
        except Exception as e:
            result.errors.append(f"文本解析失败: {e}")
            result.status = "error"
        return result


# ============================================================
# 网页解析器 (URL/RSS/Sitemap/API/DNS/SSL)
# ============================================================
class WebParser(BaseParser):
    """网页解析器"""
    name = "web"
    priority = "P0"
    supported_extensions = [".url", ".webloc"]  # 占位，主要是 parse_url()

    def parse(self, file_path: str) -> ParseResult:
        """解析 .url / .webloc 快捷方式"""
        import time
        start = time.time()

        result = ParseResult(
            file_path=file_path,
            file_name=os.path.basename(file_path),
            extension=os.path.splitext(file_path)[1].lower(),
            parser_used="WebParser v1.0",
        )

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            # 提取 URL
            urls = re.findall(r"(?:URL=|https?://[^\s\"'<>]+)", content, re.IGNORECASE)
            if urls:
                result.metadata["url"] = urls[0].replace("URL=", "")
                result.raw_text = f"URL: {result.metadata['url']}"
                result.content_preview = result.raw_text
                result.status = "success"
            else:
                result.status = "partial"
        except Exception as e:
            result.errors.append(f"解析失败: {e}")
            result.status = "error"

        result.parse_time_ms = (time.time() - start) * 1000
        return result

    @staticmethod
    def parse_url(url: str, timeout: int = 30, render_js: bool = False) -> ParseResult:
        """解析网页URL"""
        import time
        start = time.time()

        result = ParseResult(
            file_path=url,
            file_name=url,
            extension=".url",
            parser_used="WebParser::parse_url v1.0",
        )

        try:
            import requests
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            }
            resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            result.metadata["status_code"] = resp.status_code
            result.metadata["final_url"] = resp.url
            result.metadata["content_type"] = resp.headers.get("Content-Type", "")
            result.metadata["content_length"] = resp.headers.get("Content-Length", "")
            result.metadata["server"] = resp.headers.get("Server", "")
            result.metadata["headers"] = dict(resp.headers)

            if "text/html" in resp.headers.get("Content-Type", ""):
                # HTML 解析
                ok, bs4 = safe_import("bs4")
                if not ok:
                    ok, bs4 = safe_import("beautifulsoup4", "bs4")

                if ok:
                    soup = bs4.BeautifulSoup(resp.text, "html.parser")

                    # 标题
                    title_tag = soup.find("title")
                    result.metadata["title"] = title_tag.get_text(strip=True) if title_tag else ""

                    # Meta 标签
                    metas = {}
                    for meta in soup.find_all("meta"):
                        name = meta.get("name", meta.get("property", ""))
                        content = meta.get("content", "")
                        if name and content:
                            metas[name] = content
                    result.metadata["meta"] = metas

                    # 链接
                    links = []
                    for a in soup.find_all("a", href=True):
                        href = a["href"]
                        if href.startswith("http"):
                            links.append(href)
                    result.metadata["links"] = list(set(links))[:100]

                    # 图片
                    imgs = []
                    for img in soup.find_all("img", src=True):
                        imgs.append(img["src"])
                    result.metadata["images"] = imgs[:50]

                    # 纯文本
                    for script in soup(["script", "style", "nav", "footer", "header"]):
                        script.decompose()
                    text = soup.get_text(separator="\n")
                    lines = [line.strip() for line in text.split("\n") if line.strip()]
                    result.raw_text = "\n".join(lines[:500])
                    result.content_preview = result.raw_text[:1000]
                else:
                    # 简单去标签
                    clean = re.sub(r"<[^>]+>", " ", resp.text)
                    clean = re.sub(r"\s+", " ", clean).strip()
                    result.raw_text = clean[:10000]
                    result.content_preview = clean[:1000]

                # JSON-LD 结构化数据
                if ok:
                    for script in soup.find_all("script", type="application/ld+json"):
                        try:
                            result.structured_data["jsonld"] = json.loads(script.string)
                        except Exception:
                            pass
            else:
                result.raw_text = resp.text[:10000]
                result.content_preview = resp.text[:1000]

            result.status = "success"
        except Exception as e:
            result.errors.append(f"网页解析失败: {e}")
            result.status = "error"

        result.parse_time_ms = (time.time() - start) * 1000
        return result


# ============================================================
# 地理/运动数据解析器
# ============================================================
class GeoDataParser(BaseParser):
    """地理/运动数据解析器 — P3"""
    name = "geo"
    priority = "P3"
    supported_extensions = [".gpx", ".kmz", ".kml", ".fit", ".dxf"]

    def parse(self, file_path: str) -> ParseResult:
        import time
        start = time.time()
        ext = os.path.splitext(file_path)[1].lower()

        result = ParseResult(
            file_path=file_path,
            file_name=os.path.basename(file_path),
            extension=ext,
            file_size=os.path.getsize(file_path),
            mime_type=get_mime_type(ext),
            parser_used="GeoDataParser v1.0",
        )

        if ext == ".gpx":
            ok, gpxpy = safe_import("gpxpy")
            if ok:
                try:
                    with open(file_path, "r") as f:
                        gpx = gpxpy.parse(f)
                    result.metadata["tracks"] = len(gpx.tracks)
                    result.metadata["waypoints"] = len(gpx.waypoints)
                    result.metadata["routes"] = len(gpx.routes)
                    points = []
                    for track in gpx.tracks:
                        for segment in track.segments:
                            for pt in segment.points:
                                points.append({
                                    "lat": pt.latitude,
                                    "lon": pt.longitude,
                                    "elevation": pt.elevation,
                                    "time": pt.time.isoformat() if pt.time else "",
                                })
                    result.metadata["total_points"] = len(points)
                    result.metadata["sample_points"] = points[:10]
                    result.raw_text = f"GPS轨迹: {len(gpx.tracks)}条, {len(points)}个点"
                    result.content_preview = result.raw_text
                    result.status = "success"
                except Exception as e:
                    result.errors.append(f"GPX 解析失败: {e}")
                    result.status = "error"
            else:
                result.status = "unsupported"
                result.errors.append("GPX 解析需要 gpxpy")

        elif ext == ".kmz":
            import zipfile
            try:
                with zipfile.ZipFile(file_path, "r") as zf:
                    kml_files = [f for f in zf.namelist() if f.endswith(".kml")]
                    result.metadata["archive_files"] = zf.namelist()
                    if kml_files:
                        content = zf.read(kml_files[0]).decode("utf-8", errors="ignore")
                        result.raw_text = content[:10000]
                        result.content_preview = result.raw_text[:1000]
                result.status = "success"
            except Exception as e:
                result.errors.append(f"KMZ 解析失败: {e}")
                result.status = "error"

        elif ext == ".fit":
            ok, fitdecode = safe_import("fitdecode")
            if ok:
                try:
                    with fitdecode.FitReader(file_path) as fit:
                        records = []
                        for frame in fit:
                            if frame.frame_type == fitdecode.FIT_FRAME_DATA:
                                records.append({
                                    field.name: field.value
                                    for field in frame.fields
                                    if field.value is not None
                                })
                        result.metadata["records"] = len(records)
                        result.metadata["sample_records"] = records[:10]
                        result.raw_text = f"FIT 运动数据: {len(records)} 条记录"
                        result.content_preview = result.raw_text
                    result.status = "success"
                except Exception as e:
                    result.errors.append(f"FIT 解析失败: {e}")
                    result.status = "error"
            else:
                result.status = "unsupported"
                result.errors.append("FIT 解析需要 fitdecode")

        elif ext == ".dxf":
            ok, ezdxf = safe_import("ezdxf")
            if ok:
                try:
                    doc = ezdxf.readfile(file_path)
                    result.metadata["entities"] = len(list(doc.modelspace()))
                    result.metadata["layers"] = [layer.dxf.name for layer in doc.layers]
                    result.raw_text = f"DXF CAD文件: {len(result.metadata['layers'])}个图层, {result.metadata['entities']}个实体"
                    result.content_preview = result.raw_text
                    result.status = "success"
                except Exception as e:
                    result.errors.append(f"DXF 解析失败: {e}")
                    result.status = "error"
            else:
                result.status = "unsupported"
                result.errors.append("DXF 解析需要 ezdxf")

        result.parse_time_ms = (time.time() - start) * 1000
        return result


# ============================================================
# 可执行文件解析器 (仅记录, 不解析)
# ============================================================
class ExecutableParser(BaseParser):
    """可执行文件解析器 — P3 (仅记录元数据)"""
    name = "executable"
    priority = "P3"
    supported_extensions = [".exe", ".dll", ".so", ".dylib", ".app", ".msi", ".apk", ".deb", ".rpm", ".elf"]

    def parse(self, file_path: str) -> ParseResult:
        import time
        start = time.time()

        result = ParseResult(
            file_path=file_path,
            file_name=os.path.basename(file_path),
            extension=os.path.splitext(file_path)[1].lower(),
            file_size=os.path.getsize(file_path),
            mime_type="application/octet-stream",
            parser_used="ExecutableParser v1.0",
        )

        # 仅记录哈希和基本信息
        result.metadata["sha256"] = get_file_hash(file_path)
        result.metadata["md5"] = get_file_hash(file_path, "md5")

        # ELF 头部信息 (Linux)
        ext = os.path.splitext(file_path)[1].lower()
        if ext in [".so", ".elf"] or (not ext and os.access(file_path, os.X_OK)):
            try:
                with open(file_path, "rb") as f:
                    header = f.read(64)
                    if header[:4] == b"\x7fELF":
                        result.metadata["format"] = "ELF"
                        result.metadata["class"] = "64-bit" if header[4] == 2 else "32-bit"
                        result.metadata["endian"] = "little" if header[5] == 1 else "big"
                result.raw_text = f"ELF 可执行文件: {result.file_name}"
                result.content_preview = result.raw_text
                result.status = "success"
            except Exception:
                pass
        elif ext in [".exe", ".dll"]:
            result.raw_text = f"Windows PE 文件: {result.file_name}\nSHA256: {result.metadata['sha256']}"
            result.content_preview = result.raw_text
            result.status = "success"
        else:
            result.raw_text = f"可执行文件: {result.file_name}\n大小: {result.file_size} bytes\nSHA256: {result.metadata['sha256']}"
            result.content_preview = result.raw_text
            result.status = "success"

        result.parse_time_ms = (time.time() - start) * 1000
        return result


# ============================================================
# 统一入口 — UniversalParser
# ============================================================
class UniversalParser:
    """
    龍魂全文件解析引擎 · 统一入口
    ============================
    自动路由到对应的解析器，支持 60+ 文件格式
    """

    def __init__(self):
        self.parsers: Dict[str, BaseParser] = {}
        self._register_parsers()

        # 扩展名→解析器映射
        self._ext_map: Dict[str, BaseParser] = {}
        for name, parser in self.parsers.items():
            for ext in parser.supported_extensions:
                self._ext_map[ext.lower()] = parser

    def _register_parsers(self):
        """注册所有解析器"""
        self.parsers = {
            # P0 高优先级
            "excel": ExcelParser(),
            "powerpoint": PowerPointParser(),
            "archive": ArchiveParser(),
            "database": DatabaseParser(),

            # P1 中优先级
            "image_deep": ImageDeepParser(),
            "audio": AudioParser(),
            "video": VideoParser(),
            "document": DocumentParser(),

            # P2 低优先级
            "ebook": EBookParser(),
            "email": EmailParser(),
            "font": FontParser(),
            "code_deep": CodeDeepParser(),
            "web": WebParser(),

            # P3 仅记录
            "geo": GeoDataParser(),
            "executable": ExecutableParser(),
        }

    def get_parsers(self) -> List[Dict]:
        """列出所有已注册的解析器"""
        return [
            {
                "name": p.name,
                "priority": p.priority,
                "extensions": p.supported_extensions,
                "count": len(p.supported_extensions),
            }
            for p in self.parsers.values()
        ]

    def get_supported_extensions(self) -> List[str]:
        """列出所有支持的扩展名"""
        return sorted(list(self._ext_map.keys()))

    def parse(self, file_path: str) -> ParseResult:
        """
        解析文件 — 自动路由

        Args:
            file_path: 文件路径

        Returns:
            ParseResult: 统一解析结果
        """
        import time
        total_start = time.time()

        if not os.path.exists(file_path):
            return ParseResult(
                file_path=file_path,
                status="error",
                errors=[f"文件不存在: {file_path}"],
                parse_time_ms=(time.time() - total_start) * 1000,
            )

        ext = os.path.splitext(file_path)[1].lower()

        # 如果文件有扩展名, 走扩展名路由
        if ext in self._ext_map:
            try:
                parser = self._ext_map[ext]
                result = parser.parse(file_path)
                result.parse_time_ms = (time.time() - total_start) * 1000
                return result
            except Exception as e:
                return ParseResult(
                    file_path=file_path,
                    extension=ext,
                    status="error",
                    errors=[f"解析异常: {e}\n{traceback.format_exc()}"],
                    parse_time_ms=(time.time() - total_start) * 1000,
                )

        # 无扩展名 → 尝试文本解析
        if not ext:
            try:
                with open(file_path, "rb") as f:
                    header = f.read(1024)
                # 检测是否为文本
                text_chars = sum(1 for b in header if 32 <= b <= 126 or b in (9, 10, 13))
                binary_ratio = 1 - (text_chars / len(header)) if header else 0
                if binary_ratio < 0.3:
                    # 作为文本处理
                    result = self._parse_as_text(file_path)
                    result.parse_time_ms = (time.time() - total_start) * 1000
                    return result
                else:
                    # 二进制文件
                    return ParseResult(
                        file_path=file_path,
                        file_size=os.path.getsize(file_path),
                        status="unsupported",
                        errors=["二进制文件, 无法自动识别格式"],
                        parse_time_ms=(time.time() - total_start) * 1000,
                    )
            except Exception as e:
                return ParseResult(
                    file_path=file_path,
                    status="error",
                    errors=[f"文件读取失败: {e}"],
                    parse_time_ms=(time.time() - total_start) * 1000,
                )

        # 不支持的类型
        return ParseResult(
            file_path=file_path,
            extension=ext,
            file_size=os.path.getsize(file_path),
            status="unsupported",
            errors=[f"不支持的格式: {ext}"],
            parse_time_ms=(time.time() - total_start) * 1000,
        )

    def parse_batch(self, file_paths: List[str]) -> List[ParseResult]:
        """批量解析"""
        return [self.parse(fp) for fp in file_paths]

    def _parse_as_text(self, file_path: str) -> ParseResult:
        """作为纯文本解析"""
        import time
        start = time.time()

        result = ParseResult(
            file_path=file_path,
            file_name=os.path.basename(file_path),
            file_size=os.path.getsize(file_path),
            parser_used="UniversalParser::text_fallback",
        )

        try:
            # 尝试多种编码
            for encoding in ["utf-8", "gbk", "gb2312", "latin-1"]:
                try:
                    with open(file_path, "r", encoding=encoding) as f:
                        content = f.read()
                    result.metadata["encoding"] = encoding
                    break
                except UnicodeDecodeError:
                    continue
            else:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                result.metadata["encoding"] = "utf-8 (with errors)"

            lines = content.split("\n")
            result.metadata["lines"] = len(lines)
            result.metadata["chars"] = len(content)
            result.raw_text = content[:10000]
            result.content_preview = content[:1000]
            result.status = "success"
        except Exception as e:
            result.status = "error"
            result.errors.append(f"文本解析失败: {e}")

        result.parse_time_ms = (time.time() - start) * 1000
        return result

    def get_capability_report(self) -> Dict[str, Any]:
        """生成能力报告"""
        total_formats = len(self._ext_map)
        by_priority = {"P0": [], "P1": [], "P2": [], "P3": []}
        for parser in self.parsers.values():
            by_priority[parser.priority].append({
                "name": parser.name,
                "extensions": parser.supported_extensions,
                "count": len(parser.supported_extensions),
            })

        return {
            "engine": "龍魂全文件解析引擎 v1.0",
            "dna": __DNA__,
            "total_formats": total_formats,
            "parser_count": len(self.parsers),
            "by_priority": by_priority,
            "all_extensions": sorted(list(self._ext_map.keys())),
            "dependencies": self._get_dependency_status(),
        }

    def _get_dependency_status(self) -> Dict[str, Any]:
        """检查依赖状态"""
        deps = {
            "openpyxl": False, "pandas": False, "python-pptx": False,
            "pillow": False, "pillow_heif": False, "mutagen": False,
            "moviepy": False, "pydub": False, "rarfile": False,
            "py7zr": False, "pypdf": False, "pdfplumber": False,
            "python-docx": False, "ebooklib": False, "fonttools": False,
            "gpxpy": False, "fitdecode": False, "ezdxf": False,
        }
        for mod_name in deps:
            ok, _ = safe_import(mod_name.replace("-", "_"))
            deps[mod_name] = ok
        return deps


# ============================================================
# CLI 入口
# ============================================================
def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="龍魂全文件解析引擎 v1.0 — 解析一切·不留死角",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s -f document.xlsx              # 解析 Excel
  %(prog)s -f presentation.pptx          # 解析 PowerPoint
  %(prog)s -f archive.zip                # 解析压缩包
  %(prog)s -f database.db                # 解析 SQLite
  %(prog)s -f image.heic                 # 解析 HEIC 图片
  %(prog)s -f audio.mp3                  # 解析音频
  %(prog)s -f video.mp4                  # 解析视频
  %(prog)s -f page.html                  # 解析网页
  %(prog)s --url https://example.com     # 解析网址
  %(prog)s --capabilities                # 查看解析能力
  %(prog)s --check-deps                  # 检查依赖
  %(prog)s -f file.txt -o output.json    # 输出JSON
        """
    )

    parser.add_argument("-f", "--file", help="要解析的文件路径")
    parser.add_argument("--url", help="要解析的网页 URL")
    parser.add_argument("-o", "--output", help="输出JSON文件路径")
    parser.add_argument("--capabilities", action="store_true", help="显示解析能力清单")
    parser.add_argument("--check-deps", action="store_true", help="检查依赖安装状态")
    parser.add_argument("--batch", nargs="+", help="批量解析多个文件")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--pretty", action="store_true", default=True, help="美化输出")

    args = parser.parse_args()

    up = UniversalParser()

    # 能力清单
    if args.capabilities:
        report = up.get_capability_report()
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    # 依赖检查
    if args.check_deps:
        deps = up._get_dependency_status()
        print("=" * 50)
        print("  龍魂解析引擎 · 依赖状态")
        print("=" * 50)
        for dep, installed in deps.items():
            status = "✅" if installed else "❌ 需安装"
            print(f"  {status}  {dep}")
        print("=" * 50)
        total = len(deps)
        installed = sum(1 for v in deps.values() if v)
        print(f"  已安装: {installed}/{total}")
        return

    # URL 解析
    if args.url:
        result = WebParser.parse_url(args.url)
        if args.json or args.output:
            output = json.dumps(result.to_dict(), ensure_ascii=False, indent=2, default=str)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(output)
                print(f"✅ 结果已写入 {args.output}")
            else:
                print(output)
        else:
            _print_result_pretty(result)
        return

    # 文件解析
    if args.file:
        result = up.parse(args.file)
        if args.json or args.output:
            output = json.dumps(result.to_dict(), ensure_ascii=False, indent=2, default=str)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(output)
                print(f"✅ 结果已写入 {args.output}")
            else:
                print(output)
        else:
            _print_result_pretty(result)
        return

    # 批量解析
    if args.batch:
        results = up.parse_batch(args.batch)
        output = json.dumps(
            [r.to_dict() for r in results],
            ensure_ascii=False, indent=2, default=str,
        )
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"✅ 批量结果已写入 {args.output}")
        else:
            print(output)
        return

    parser.print_help()


def _print_result_pretty(result: ParseResult):
    """美化打印解析结果"""
    print("=" * 60)
    print(f"  📄 {result.file_name}")
    print(f"  格式: {result.extension} | 大小: {result.file_size:,} bytes")
    print(f"  解析器: {result.parser_used} | 耗时: {result.parse_time_ms:.1f}ms")
    print(f"  状态: {result.status}")
    print("-" * 60)

    if result.metadata:
        print("  元数据:")
        for key, value in result.metadata.items():
            if key not in ["exif", "headers", "links", "images"]:
                print(f"    {key}: {value}")

    if result.tables:
        print(f"  表格: {len(result.tables)} 个")

    if result.archive_files:
        print(f"  归档文件: {len(result.archive_files)} 个")
        for f in result.archive_files[:10]:
            print(f"    - {f}")

    if result.warnings:
        print(f"  ⚠️ 警告: {len(result.warnings)} 条")
        for w in result.warnings[:3]:
            print(f"    - {w}")

    if result.errors:
        print(f"  ❌ 错误: {len(result.errors)} 条")
        for e in result.errors:
            print(f"    - {e}")

    print("-" * 60)
    if result.content_preview:
        print("  内容预览:")
        print(result.content_preview[:500])
        if len(result.content_preview) > 500:
            print("  ... (更多内容省略)")
    print("=" * 60)


if __name__ == "__main__":
    main()
