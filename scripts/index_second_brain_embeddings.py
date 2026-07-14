#!/Users/zuimeidedeyihan/longhun-system/.venv_longhun_math/bin/python
# -*- coding: utf-8 -*-
"""#龍芯⚡️2026-06-29-INDEX-SECOND-BRAIN-EMBEDDINGS-CLI-v1.0
为第二大脑补全向量索引
"""
import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from second_brain.embed_backfill import backfill


def main():
    result = backfill()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
