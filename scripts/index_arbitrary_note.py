# DNA: #龍芯⚡️丙午·乙未·乙丑·井-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/Users/zuimeidedeyihan/longhun-system/.venv_longhun_math/bin/python
# -*- coding: utf-8 -*-
"""#龍芯⚡️2026-06-29-INDEX-ARBITRARY-NOTE-v1.0
把任意 Markdown 文件单篇接入第二大脑索引
"""
import sys
import argparse
import hashlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from second_brain.indexer import SecondBrainIndex
from second_brain.models import Note
from second_brain import config
import frontmatter
import re


def parse_file(path: Path) -> Note:
    rel = str(path.relative_to(PROJECT_ROOT))
    text = path.read_text(encoding="utf-8", errors="ignore")
    try:
        post = frontmatter.loads(text)
    except Exception:
        post = frontmatter.Post(text)

    title = post.get("title", "")
    if not title:
        # 先剔除代码块，避免把代码注释当标题
        text_no_code = re.sub(r"```[\s\S]*?```", "", text)
        text_no_code = re.sub(r"`[^`]+`", "", text_no_code)
        m = re.search(r"^#\s+(.+)$", text_no_code, re.MULTILINE)
        title = m.group(1).strip() if m else path.stem

    tags = post.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]
    tags = sorted(set(tags))

    note_id = "note-" + hashlib.sha256(rel.encode("utf-8")).hexdigest()[:12]
    return Note(
        note_id=note_id,
        path=rel,
        title=title,
        content=post.content,
        content_hash=hashlib.sha256(post.content.encode("utf-8")).hexdigest(),
        created=str(path.stat().st_ctime),
        modified=str(path.stat().st_mtime),
        tags=tags,
        links=[],
        aliases=[],
        metadata=dict(post.metadata),
        dna=f"{config.DNA_PREFIX}{config.now_iso().replace('-','').replace(':','').replace('T','')}-SECOND-BRAIN-ARBITRARY-{note_id}",
        audit="🟢",
    )


def main():
    parser = argparse.ArgumentParser(description="单篇 Markdown 接入第二大脑")
    parser.add_argument("path", help="Markdown 文件路径")
    args = parser.parse_args()

    path = Path(args.path).resolve()
    note = parse_file(path)
    index = SecondBrainIndex()
    changed = index.index_note(note)

    # 重新训练/补全 TF-IDF 以包含新文档
    status = index.fit_tfidf()

    print(f"note_id: {note.note_id}")
    print(f"title:   {note.title}")
    print(f"changed: {changed}")
    print(f"embed:   {status}")


if __name__ == "__main__":
    main()
