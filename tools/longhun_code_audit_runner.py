# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 代码可执行性审计工具（多进程版）
DNA: #龍芯⚡️2026-06-26-CODE-AUDIT-RUNNER-MP-v1.0
"""

import sqlite3
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
from collections import Counter
from multiprocessing import Pool, cpu_count

DB_PATH = Path.home() / "_work" / "dragon_knowledge.db"
CST = timezone(timedelta(hours=8))


def now_iso():
    return datetime.now(CST).isoformat()


def run_command(cmd: list[Any], cwd=None, timeout=5) -> tuple[Any, ...]:
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode, result.stdout[:300], result.stderr[:300]
    except subprocess.TimeoutExpired:
        return -1, "", "超时"
    except Exception as e:
        return -2, "", str(e)[:300]


def audit_one(args):
    entry_id, file_path, file_name = args
    ext = Path(file_name).suffix.lower()
    result = {
        "entry_id": entry_id,
        "syntax_ok": "0",
        "help_works": "0",
        "can_import": "0",
        "test_status": "UNKNOWN",
        "test_error": "",
    }
    
    p = Path(file_path)
    if not p.exists():
        result["test_status"] = "FILE_MISSING"
        return result
    
    if ext == '.py':
        # 语法检查
        rc, out, err = run_command(["python3", "-m", "py_compile", str(p)])
        if rc != 0:
            result["test_status"] = "SYNTAX_ERROR"
            result["test_error"] = err
            return result
        result["syntax_ok"] = "1"
        
        try:
            text = p.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            result["test_status"] = "READ_ERROR"
            result["test_error"] = str(e)[:200]
            return result
        
        has_main = 'if __name__' in text
        has_argparse = 'argparse' in text or 'ArgumentParser' in text
        
        if has_main and has_argparse:
            for flag in ['--help', '-h']:
                rc, out, err = run_command(["python3", str(p), flag], cwd=p.parent)
                if rc == 0:
                    result["help_works"] = "1"
                    result["test_status"] = "HELP_OK"
                    return result
            result["test_status"] = "MAIN_NO_HELP"
        elif has_main:
            result["test_status"] = "HAS_MAIN"
        else:
            # 尝试导入
            rc, out, err = run_command([
                "python3", "-c",
                f"import importlib.util; spec=importlib.util.spec_from_file_location('audit_mod', '{p}'); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)"
            ], cwd=p.parent)
            if rc == 0:
                result["can_import"] = "1"
                result["test_status"] = "IMPORT_OK"
            else:
                result["test_status"] = "IMPORT_FAILED"
                result["test_error"] = err
    
    elif ext == '.sh':
        rc, out, err = run_command(["bash", "-n", str(p)])
        if rc != 0:
            result["test_status"] = "SYNTAX_ERROR"
            result["test_error"] = err
            return result
        result["syntax_ok"] = "1"
        result["test_status"] = "SYNTAX_OK"
        
        # 尝试 --help
        rc, out, err = run_command(["bash", str(p), "--help"], cwd=p.parent)
        if rc == 0:
            result["help_works"] = "1"
            result["test_status"] = "HELP_OK"
    
    return result


def main():
    print("🐉 龍魂 · 代码可执行性审计（多进程版）\n")
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    for col in ["syntax_ok", "help_works", "can_import", "test_status", "test_error", "audited_at"]:
        try:
            cur.execute(f"ALTER TABLE device_orphan_files ADD COLUMN {col} TEXT")
        except sqlite3.OperationalError:
            pass
    conn.commit()
    
    # 清除之前的审计结果，重新审计
    cur.execute("UPDATE device_orphan_files SET syntax_ok='', help_works='', can_import='', test_status='', test_error='', audited_at=''")
    conn.commit()
    
    cur.execute("""
        SELECT entry_id, file_path, file_name
        FROM device_orphan_files
        WHERE file_name LIKE '%.py' OR file_name LIKE '%.sh'
        ORDER BY file_path
    """)
    rows = cur.fetchall()
    print(f"待审计脚本: {len(rows)}\n")
    
    workers = max(1, cpu_count() - 1)
    print(f"使用 {workers} 个进程并行审计...\n")
    
    results = []
    with Pool(workers) as pool:
        for i, result in enumerate(pool.imap_unordered(audit_one, rows), 1):
            results.append(result)
            if i % 200 == 0:
                print(f"  已审计 {i}/{len(rows)}")
    
    # 批量写入 DB
    cur.executemany("""
        UPDATE device_orphan_files
        SET syntax_ok=?, help_works=?, can_import=?, test_status=?, test_error=?, audited_at=?
        WHERE entry_id=?
    """, [
        (r["syntax_ok"], r["help_works"], r["can_import"], r["test_status"], r["test_error"], now_iso(), r["entry_id"])
        for r in results
    ])
    conn.commit()
    conn.close()
    
    status_counter = Counter(r["test_status"] for r in results)
    syntax_ok = sum(1 for r in results if r["syntax_ok"] == "1")
    help_ok = sum(1 for r in results if r["help_works"] == "1")
    
    print(f"\n=== 审计完成 ===")
    print(f"总脚本: {len(results)}")
    print(f"语法通过: {syntax_ok}")
    print(f"--help 可用: {help_ok}")
    print(f"\n状态分布:")
    for status, cnt in status_counter.most_common():
        print(f"  {status}: {cnt}")


if __name__ == "__main__":
    main()
