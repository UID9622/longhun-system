# -*- coding: utf-8 -*-
"""
龍魂·信任核心测试夹具 v1.0
DNA: #龍芯⚡️丙午·丙申-TRUST-CORE-v1.0-TEST-FIXTURE
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
为什么存在: 落位到 04_ENGINES/trust-core/ 后，pytest 从仓库根目录收集时
  longhun_trust 不在 sys.path。本文件把引擎库根加入 path，保证测试独立可跑。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
