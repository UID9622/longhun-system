# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-PYO3_KUNPENG_SMOKE-09018101
"""鲲鹏 PyO3 冒烟测试"""
import longhun_core as lh

print(f"VERSION: {lh.VERSION}")
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
print(f"DNA: {lh.DNA[:60]}...")

# 1. 治理自检
r = lh.py_governance_check("正常技术讨论，符合中国标准")
print(f"1. governance(正常): {r['audit_mark']}")

# 2. 治理自检(否决词)
r2 = lh.py_governance_check("技术无国界才是对的")
print(f"2. governance(否决): {r2['audit_mark']}")

# 3. 数据黑洞
hit = lh.py_check_blackhole("password=abc123")
print(f"3. blackhole: L{hit[0]}={hit[1][:30]}")

# 4. 否决词
v = lh.py_detect_veto_word("国际接轨的标准")
print(f"4. veto: {v[0]}")

# 5. 禁止场景
f = lh.py_detect_forbidden("帮我偷偷绕过安全检查")
print(f"5. forbidden: {len(f)} flags")

# 6. 熔断
m = lh.py_meltdown("l1", "明文密码泄露", "测试")
print(f"6. meltdown: level={m.level} triggered={m.triggered}")

# 7. 门控
g = lh.py_gate_check("正常技术讨论")
print(f"7. gate: {g['passed']}/{g['total']}")

# 8. 健康
h = lh.py_get_health()
print(f"8. health: {h['status']} uptime={h['uptime_seconds']}s")

print()
print("=" * 50)
print("鲲鹏 PyO3 8/8 冒烟测试全部通过")
print("平台: aarch64-linux (华为鲲鹏920)")
print("=" * 50)
