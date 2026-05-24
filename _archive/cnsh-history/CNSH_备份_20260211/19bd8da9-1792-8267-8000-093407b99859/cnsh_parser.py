"""
📝 CNSH解析器 - 解析Markdown文档结构
修复了：
1. 支持多种Markdown标题格式
2. 处理隐形字符
3. 统一换行符
4. 支持YAML Frontmatter
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Any


# 匹配各种标题格式
H1_RE = re.compile(r"^\s*#\s+(.+?)\s*$", re.MULTILINE)
H2_RE = re.compile(r"^\s*##\s+(.+?)\s*$", re.MULTILINE)
H3_RE = re.compile(r"^\s*###\s+(.+?)\s*$", re.MULTILINE)

# YAML Frontmatter匹配
YAML_FRONT_RE = re.compile(r"^---\s*$", re.MULTILINE)


def read_text(path: Path) -> str:
    """读取文本，处理编码问题"""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # 尝试其他编码
        import chardet
        with open(path, 'rb') as f:
            raw = f.read()
            result = chardet.detect(raw)
            encoding = result['encoding'] or 'utf-8'
        return raw.decode(encoding)


def normalize_line_endings(text: str) -> str:
    """统一换行符为LF"""
    return text.replace('\r\n', '\n').replace('\r', '\n')


def remove_bom(text: str) -> str:
    """移除BOM标记"""
    if text.startswith('\ufeff'):
        return text[1:]
    return text


def find_h1_sections(text: str) -> Dict[str, int]:
    """查找所有一级标题"""
    sections: Dict[str, int] = {}
    for i, line in enumerate(text.split('\n')):
        m = H1_RE.match(line)
        if m:
            name = m.group(1).strip()
            sections[name] = i
    return sections


def find_h2_sections(text: str) -> Dict[str, int]:
    """查找所有二级标题"""
    sections: Dict[str, int] = {}
    for i, line in enumerate(text.split('\n')):
        m = H2_RE.match(line)
        if m:
            name = m.group(1).strip()
            sections[name] = i
    return sections


def find_h3_sections(text: str) -> Dict[str, int]:
    """查找所有三级标题"""
    sections: Dict[str, int] = {}
    for i, line in enumerate(text.split('\n')):
        m = H3_RE.match(line)
        if m:
            name = m.group(1).strip()
            sections[name] = i
    return sections


def split_frontmatter(text: str) -> Tuple[str, str]:
    """拆分YAML Frontmatter和正文"""
    lines = text.split('\n')
    
    # 检查是否以---开头
    if len(lines) >= 3 and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                front = '\n'.join(lines[:i + 1])
                body = '\n'.join(lines[i + 1:])
                return front, body
    
    return "", text


def extract_yaml_value(text: str, key: str) -> str:
    """从YAML Frontmatter中提取值"""
    lines = text.split('\n')
    in_yaml = False
    
    for line in lines:
        if line.strip() == "---":
            in_yaml = not in_yaml
            if not in_yaml:
                break
            continue
        
        if in_yaml and line.strip().startswith(f"{key}:"):
            parts = line.split(":", 1)
            if len(parts) > 1:
                return parts[1].strip()
    
    return ""


def find_tables(text: str) -> List[Dict[str, Any]]:
    """查找所有表格"""
    tables = []
    lines = text.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 表格开始
        if '|' in line and i + 1 < len(lines) and '|' in lines[i + 1]:
            table_lines = []
            j = i
            while j < len(lines) and ('|' in lines[j] or lines[j].strip() == ''):
                table_lines.append(lines[j])
                j += 1
            
            tables.append({
                'start_line': i + 1,
                'end_line': j,
                'content': '\n'.join(table_lines)
            })
            
            i = j
        else:
            i += 1
    
    return tables


def find_code_blocks(text: str) -> List[Dict[str, Any]]:
    """查找所有代码块"""
    blocks = []
    lines = text.split('\n')
    
    in_block = False
    block_start = 0
    language = None
    
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            if not in_block:
                # 代码块开始
                in_block = True
                block_start = i
                language = line.strip()[3:].strip()
            else:
                # 代码块结束
                in_block = False
                blocks.append({
                    'start_line': block_start + 1,
                    'end_line': i + 1,
                    'language': language or 'text',
                    'content': '\n'.join(lines[block_start:i+1])
                })
    
    return blocks


def find_lists(text: str) -> List[Dict[str, Any]]:
    """查找所有列表"""
    lists = []
    lines = text.split('\n')
    
    in_list = False
    list_start = 0
    items = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # 列表项
        if stripped.startswith('- ') or stripped.startswith('* ') or re.match(r'^\d+\.\s', stripped):
            if not in_list:
                in_list = True
                list_start = i
            items.append({
                'line': i + 1,
                'content': stripped,
                'level': len(line) - len(line.lstrip())
            })
        elif in_list and stripped != '':
            # 列表结束
            in_list = False
            lists.append({
                'start_line': list_start + 1,
                'end_line': i,
                'items': items
            })
            items = []
    
    # 处理末尾的列表
    if in_list:
        lists.append({
            'start_line': list_start + 1,
            'end_line': len(lines),
            'items': items
        })
    
    return lists


def parse_document(file_path: str) -> Dict[str, Any]:
    """解析完整文档"""
    path = Path(file_path)
    
    # 读取并预处理
    text = read_text(path)
    text = remove_bom(text)
    text = normalize_line_endings(text)
    
    # 拆分Frontmatter
    frontmatter, body = split_frontmatter(text)
    
    # 提取关键信息
    uid = extract_yaml_value(frontmatter, 'UID') or '未知'
    dna_prefix = extract_yaml_value(frontmatter, 'DNA_Prefix') or '未知'
    title = extract_yaml_value(frontmatter, 'Language') or '未知'
    
    # 解析结构
    h1_sections = find_h1_sections(body)
    h2_sections = find_h2_sections(body)
    h3_sections = find_h3_sections(body)
    tables = find_tables(body)
    code_blocks = find_code_blocks(body)
    lists = find_lists(body)
    
    return {
        'file_path': str(path),
        'uid': uid,
        'dna_prefix': dna_prefix,
        'title': title,
        'frontmatter': frontmatter,
        'body': body,
        'structure': {
            'h1_sections': h1_sections,
            'h2_sections': h2_sections,
            'h3_sections': h3_sections,
            'tables': tables,
            'code_blocks': code_blocks,
            'lists': lists
        }
    }


def validate_document(doc: Dict[str, Any]) -> List[str]:
    """验证文档结构"""
    issues = []
    
    # 检查必需区块
    required_sections = [
        '版本号', 'DNA追溯码', '创建者/协作者', '标准头部',
        '演进记录', '熔断条件', '三色审计结论'
    ]
    
    for section in required_sections:
        if section not in doc['structure']['h2_sections']:
            issues.append(f"缺失必填区块: {section}")
    
    # 检查代码块是否闭合
    in_block = False
    for i, line in enumerate(doc['body'].split('\n')):
        if line.strip().startswith('```'):
            in_block = not in_block
    
    if in_block:
        issues.append("代码块未闭合")
    
    # 检查表格列数
    for table in doc['structure']['tables']:
        lines = table['content'].split('\n')
        if len(lines) >= 2:
            first_cols = lines[0].count('|')
            for line in lines[1:]:
                if '|' in line:
                    cols = line.count('|')
                    if cols != first_cols:
                        issues.append(f"表格列数不一致（第{table['start_line']}-{table['end_line']}行）")
                        break
    
    return issues


def main():
    """测试解析器"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python cnsh_parser.py <文件路径>")
        return
    
    file_path = sys.argv[1]
    
    try:
        print(f"🔍 正在解析: {file_path}")
        doc = parse_document(file_path)
        
        print(f"\n📊 文档信息:")
        print(f"   UID: {doc['uid']}")
        print(f"   DNA前缀: {doc['dna_prefix']}")
        print(f"   标题: {doc['title']}")
        
        print(f"\n📋 结构分析:")
        print(f"   一级标题: {len(doc['structure']['h1_sections'])}个")
        print(f"   二级标题: {len(doc['structure']['h2_sections'])}个")
        print(f"   三级标题: {len(doc['structure']['h3_sections'])}个")
        print(f"   表格: {len(doc['structure']['tables'])}个")
        print(f"   代码块: {len(doc['structure']['code_blocks'])}个")
        print(f"   列表: {len(doc['structure']['lists'])}个")
        
        print(f"\n✅ 验证结果:")
        issues = validate_document(doc)
        if issues:
            print(f"   发现 {len(issues)} 个问题:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print("   🟢 文档结构完整！")
    
    except Exception as e:
        print(f"❌ 解析失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
