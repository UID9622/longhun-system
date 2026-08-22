#!/usr/bin/env bash
# 龍魂 · G3 阶段四：DNA链 + 零宽检测 + 硬回滚（2026-08-20 由 pre-commit 主钩子 source）
# DNA: #龍芯⚡️丙午·丙申·丙寅·甲午·䷕贲-GIT-HOOK-DNA-CHAIN-v1.0
set +e
echo ""
echo -e "${GREEN}🧬 阶段四 · DNA链/零宽字符/硬回滚审计（G3）${NC}"
PHASE4_FAIL=0

# 1) 零宽/隐藏字符检测（防注入误判·G0 铁律·macOS 兼容用 python3）
# 2026-08-22: U+200D(ZWJ) 是 emoji 标准组合(🧚🏼♀️/🏳️🌈)移除，U+2060 加入——防 SEAL 头误伤
# 2026-08-22: 只查新增行(+)，跳过删除行(-)——旧版本零宽残留在删除行不拦截本次提交
if git -C "$REPO_ROOT" diff --cached | python3 -c "
import sys
BAD = ['\u200b', '\u200c', '\ufeff', '\u2060']
ok = True
for line in sys.stdin.buffer.read().decode('utf-8', errors='ignore').splitlines():
    if line.startswith('+') and not line.startswith('+++'):
        if any(b in line for b in BAD):
            ok = False
            break
sys.exit(0 if not ok else 1)
" 2>/dev/null; then
  echo -e "${RED}  🔴 检出零宽/隐藏字符：会被外部扫描判为提示注入${NC}"
  PHASE4_FAIL=1
else
  echo -e "${GREEN}  [✓] 暂存内容无零宽/隐藏字符${NC}"
fi

# 2) DNA 链一致性校验（🔴 LH-FAIL-06）
if [ -f "$REPO_ROOT/scripts/verify_dna.py" ]; then
  python3 "$REPO_ROOT/scripts/verify_dna.py" --staged >/tmp/lh_verify_dna.log 2>&1
  vd_exit=$?
  tail -5 /tmp/lh_verify_dna.log
  if [ $vd_exit -ne 0 ]; then
    echo -e "${RED}  🔴 LH-FAIL-06 DNA 链断裂/零宽命中${NC}"
    PHASE4_FAIL=1
  else
    echo -e "${GREEN}  [✓] DNA 链校验通过${NC}"
  fi
fi

# 3) 硬回滚哨兵：评分连续下降 2 轮则提示（🟡 LH-FAIL-04）
if [ -f "$REPO_ROOT/.lh_score_history" ]; then
  read -r s1 s2 <<< "$(tail -n 2 "$REPO_ROOT/.lh_score_history" | tr '\n' ' ')"
  if [ -n "${s2:-}" ] && awk "BEGIN{exit !($s2 < $s1)}" 2>/dev/null; then
    echo -e "${YELLOW}  🟡 LH-FAIL-04 评分下降，建议 git revert 前一提交${NC}"
  fi
fi

if [ "$PHASE4_FAIL" -ne 0 ]; then
  TOTAL_EXIT=1
fi
set -e
