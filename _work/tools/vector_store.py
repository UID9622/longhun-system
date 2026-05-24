#!/usr/bin/env python3
import chromadb, hashlib, glob, os
from datetime import datetime

DB_PATH = os.path.expanduser("~/longhun-system/vector_db")
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name="longhun_dna")

def embed(text, tag):
    doc_id = hashlib.sha256(text.encode()).hexdigest()[:12]
    collection.add(documents=[text], ids=[doc_id], metadatas=[{"tag":tag,"time":datetime.now().isoformat()}])
    return f"#龘芯⚡️{datetime.now().strftime('%Y-%m-%d')}-EMBED-{doc_id}"

count = 0
for f in glob.glob("/Users/zuimeidedeyihan/longhun-system/**/*.md", recursive=True):
    try:
        with open(f, encoding="utf-8", errors="ignore") as fh:
            content = fh.read()[:3000]
            embed(content, f)
            count += 1
    except Exception as e:
        print(f"跳过 {f}: {e}")
print(f"已灌入 {count} 个文档到向量库 ({DB_PATH})")
