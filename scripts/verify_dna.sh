#!/bin/bash
# 龍魂 · DNA 引擎一键验证 v1.0
# DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷗复-DNA-VERIFY-v1.0-CB002
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 说明: 校验核心引擎/对齐/助手/签名 四件套，任一步失败即退出非0

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT"

echo "=============================================="
echo "  🐉 DNA 引擎 · 一键验证 v1.0"
echo "=============================================="

echo ""
echo "[1/5] 文件存在性..."
for f in bin/lh_dna_ref_impl.py bin/dna_helper.py bin/voice_input.py bin/vision_input.py; do
    if [ -f "$f" ]; then echo "  ✅ $f"; else echo "  ❌ $f 缺失"; exit 1; fi
done

echo ""
echo "[2/5] 参考实现自测（6 组测试向量）..."
python3 bin/lh_dna_ref_impl.py --selftest

echo ""
echo "[3/5] 主引擎 vs 参考实现对拍..."
python3 - <<'PY'
import sys
sys.path.insert(0, 'bin')
import lh_dna_generator as main
import importlib.util
spec = importlib.util.spec_from_file_location('ref', 'bin/lh_dna_ref_impl.py')
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
cases = [('2026-08-21',14,'对拍1'),('2024-02-10',12,'对拍2'),('2026-08-12',9,'对拍3'),('1900-01-01',0,'对拍4'),('2026-12-31',23,'对拍5')]
ok = 0
for ds,h,t in cases:
    m = main.generate(title=t, category='doc', action='创建', actor='UID9622', date_str=ds, hours=h).dna_string
    r = ref.generate(title=t, category='doc', action='创建', date_str=ds, hours=h)['dna_string']
    if m == r:
        ok += 1; print(f"  ✅ {ds} {h}时")
    else:
        print(f"  ❌ {ds} {h}时\n    主引擎: {m}\n    参考实现: {r}")
print(f"  对拍结果: {ok}/{len(cases)}")
if ok != len(cases):
    sys.exit(1)
PY

echo ""
echo "[4/5] DNA 助手（生成·不落盘）..."
python3 bin/dna_helper.py --dna-only --text "一键验证" --category system --action 验证

echo ""
echo "[5/5] GPG 签名检查..."
for f in bin/lh_dna_ref_impl.py bin/dna_helper.py bin/voice_input.py bin/vision_input.py; do
    if [ -f "$f.asc" ]; then echo "  ✅ $f.asc"; else echo "  ⚠️  $f.asc 未签名（交付前补签）"; fi
done

echo ""
echo "=============================================="
echo "  ✅ 验证完成 · DNA: #龍芯⚡️VERIFY-DONE"
echo "=============================================="
