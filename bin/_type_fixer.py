# DNA: #龍芯⚡️丙午·乙未·乙丑·小畜-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-_TYPE_FIXER-v1.0-3486bfcb
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""智能批量修复 basedpyright reportMissingTypeArgument — v2（跳过导入行）"""
import re, os

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    
    # === Step 1: 先修复被破坏的导入行 ===
    # 把 from typing import Any, Dict[str, Any], List[Any] 修回 from typing import Any, Dict, List
    content = re.sub(
        r'from typing import (.+)',
        lambda m: 'from typing import ' + re.sub(r'\b(Dict|List|Set|Tuple|Optional|Union)\[[^\]]+\]', r'\1', m.group(1)),
        content
    )
    # 确保有 Any
    if 'from typing import' in content:
        m = re.search(r'from typing import (.+)', content)
        imports = m.group(1)
        if 'Any' not in imports:
            content = content.replace(m.group(1), imports + ', Any')
    
    # === Step 2: 只对非导入行做类型参数化 ===
    lines = content.split('\n')
    new_lines = []
    for i, line in enumerate(lines):
        # 跳过导入行
        if line.strip().startswith('from typing import') or line.strip().startswith('import '):
            new_lines.append(line)
            continue
        
        # 跳过注释行
        stripped = line.strip()
        if stripped.startswith('#') or stripped.startswith('"') or stripped.startswith("'"):
            new_lines.append(line)
            continue
        
        # 在类型注解位置做替换
        # : Dict)  /  : Dict,  /  -> Dict:  /  : Dict\n  (行尾)
        line = re.sub(r':\s*Dict\s*\)', ': Dict[str, Any])', line)
        line = re.sub(r':\s*Dict\s*,', ': Dict[str, Any],', line)
        line = re.sub(r'->\s*Dict\s*:', '-> Dict[str, Any]:', line)
        # 只匹配行尾的 : Dict
        if re.search(r':\s*Dict\s*$', line) and 'Dict[str' not in line:
            line = re.sub(r':\s*Dict\s*$', ': Dict[str, Any]', line)
        # Dict 嵌套: Dict[str, Dict] → Dict[str, Dict[str, Any]]
        line = re.sub(r'Dict\[([^\]]+),\s*Dict\]', r'Dict[\1, Dict[str, Any]]', line)
        
        # List
        line = re.sub(r':\s*List\s*\)', ': List[Any])', line)
        line = re.sub(r':\s*List\s*,', ': List[Any],', line)
        line = re.sub(r'->\s*List\s*:', '-> List[Any]:', line)
        if re.search(r':\s*List\s*$', line) and 'List[' not in line:
            line = re.sub(r':\s*List\s*$', ': List[Any]', line)
        
        # Set
        line = re.sub(r':\s*Set\s*=', ': Set[str] =', line)
        if re.search(r':\s*Set\s*$', line) and 'Set[' not in line:
            line = re.sub(r':\s*Set\s*$', ': Set[str]', line)
        
        # 小写 dict/list
        line = re.sub(r':\s*dict\s*\)', ': dict[str, Any])', line)
        line = re.sub(r':\s*dict\s*,', ': dict[str, Any],', line)
        line = re.sub(r'->\s*dict\s*:', '-> dict[str, Any]:', line)
        if re.search(r':\s*dict\s*$', line) and 'dict[' not in line:
            line = re.sub(r':\s*dict\s*$', ': dict[str, Any]', line)
        
        line = re.sub(r':\s*list\s*\)', ': list[Any])', line)
        line = re.sub(r':\s*list\s*,', ': list[Any],', line)
        line = re.sub(r'->\s*list\s*:', '-> list[Any]:', line)
        if re.search(r':\s*list\s*$', line) and 'list[' not in line:
            line = re.sub(r':\s*list\s*$', ': list[Any]', line)
        
        new_lines.append(line)
    
    content = '\n'.join(new_lines)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

files_to_fix = [
    "bin/lh_biometric_health.py",
    "bin/lh_data_privacy_v2.py",
    "bin/lh_font_manager.py",
    "bin/lh_naming_check.py",
    "bin/lh_naming_unify.py",
    "bin/lh_notion_term_extractor.py",
    "bin/lh_observability_collector.py",
    "bin/lh_persona_signing.py",
    "bin/lh_resource_monitor.py",
    "bin/lh_sovereign_llm.py",
    "bin/lh_threshold_trigger.py",
    "bin/lh_universal_parser.py",
    "bin/lh_water_army_elimination.py",
]

for f in files_to_fix:
    path = f"/Users/zuimeidedeyihan/longhun-system/{f}"
    if os.path.exists(path):
        changed = fix_file(path)
        print(f"{'✅' if changed else '⏭️'} {f}")
    else:
        print(f"❌ {f} not found")
