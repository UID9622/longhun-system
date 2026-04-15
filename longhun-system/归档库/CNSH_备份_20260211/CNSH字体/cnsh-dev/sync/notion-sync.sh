#!/bin/bash
# CNSH-Notion 同步脚本 v0.1.1

DB_PATH="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Desktop/cnsh-dev/db/cnsh_kb.db"
VAULT_PATH="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Desktop/cnsh-dev/vault"

echo "🔄 CNSH-Notion 同步开始..."

# 扫描 vault 目录，更新数据库
find "$VAULT_PATH" -name "*.md" | while read -r filepath; do
    relpath="${filepath#$VAULT_PATH/}"
    title=$(grep -m 1 "^# " "$filepath" 2>/dev/null | sed 's/^# //' || basename "$filepath" .md)
    
    # 提取 DNA 码
    dna=$(grep -E "^id: " "$filepath" 2>/dev/null | head -1 | sed 's/id: //' || echo "")
    
    if [ -z "$dna" ]; then
        # 生成新 DNA
        count=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM notes;" 2>/dev/null || echo "0")
        dna="#ZHUGEXIN⚡️-CNSH-NOTE-$(printf "%04d" $((count + 1)))"
        
        # 添加 frontmatter
        temp_file=$(mktemp)
        echo "---" > "$temp_file"
        echo "id: $dna" >> "$temp_file"
        echo "title: $title" >> "$temp_file"
        echo "modified: $(date '+%Y-%m-%d %H:%M:%S')" >> "$temp_file"
        echo "---" >> "$temp_file"
        echo "" >> "$temp_file"
        cat "$filepath" >> "$temp_file"
        mv "$temp_file" "$filepath"
    fi
    
    # 更新数据库
    sqlite3 "$DB_PATH" "INSERT OR REPLACE INTO notes (id, path, title, modified_at) VALUES ('$dna', '$relpath', '$title', datetime('now'));" 2>/dev/null
done

echo "✅ 同步完成"
