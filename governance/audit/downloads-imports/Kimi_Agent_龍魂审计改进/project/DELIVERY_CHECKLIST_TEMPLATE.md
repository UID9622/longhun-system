# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!--
DNA 标识: DRAGON-SOUL-DELIVERY-CHECKLIST-v1.0.0
作者: 龍魂系统交付团队
创建时间: 2024-01-15
审计修复: M7 - 缺少交付清单
-->

# 最终交付清单模板

## 1. 概述

本文档定义龍魂系统最终交付的标准清单模板。交付清单是发布流程的**阻塞项**（Blocking Item），清单未通过验证时，流程必须暂停，不得继续后续部署步骤。

**阻塞规则**:
- 任何必填字段缺失 ➜ **阻塞流程**
- SHA256 哈希值不匹配 ➜ **阻塞流程**
- 文件权限不符合规范 ➜ **阻塞流程**
- DNA 标识缺失或格式错误 ➜ **阻塞流程**
- Git 提交哈希无法验证 ➜ **阻塞流程**

---

## 2. 交付清单模板

### 2.1 清单表格

```markdown
<!-- 交付清单开始 -->
| 序号 | 文件名 | 文件类型 | 行数 | DNA 标识 | Git 提交哈希 | 文件权限 | 存储路径 | SHA256 哈希值 | 状态 |
|------|--------|----------|------|----------|-------------|----------|----------|--------------|------|
| 1 | | | | | | | | | |
| 2 | | | | | | | | | |
| 3 | | | | | | | | | |
| 4 | | | | | | | | | |
| 5 | | | | | | | | | |
<!-- 交付清单结束 -->
```

### 2.2 字段说明

| 字段          | 必填 | 说明                                          | 示例值                                     |
|---------------|------|-----------------------------------------------|--------------------------------------------|
| 序号          | 是   | 文件在清单中的序号                            | 1                                          |
| 文件名        | 是   | 文件名称（含扩展名）                          | validate_welding_point.py                  |
| 文件类型      | 是   | 文件类型分类                                  | Python / Shell / Markdown / Config / YAML  |
| 行数          | 是   | 文件总行数（wc -l）                           | 156                                        |
| DNA 标识      | 是   | 文件顶部的 DNA 署名                           | DRAGON-SOUL-WELD-v2.1.0                    |
| Git 提交哈希  | 是   | 文件对应的 Git commit hash（前8位）           | a1b2c3d4                                   |
| 文件权限      | 是   | 文件权限位（755/644/600 等）                  | 644                                        |
| 存储路径      | 是   | 文件的绝对存储路径                            | /opt/dragon_soul/bin/                      |
| SHA256 哈希值 | 是   | 文件的 SHA256 完整哈希（用于完整性验证）       | e3b0c44298fc1c149afbf4c8996fb92427ae41e... |
| 状态          | 是   | 验证状态（✅ 通过 / ❌ 未通过 / ⏳ 待验证）   | ✅                                          |

### 2.3 权限规范

| 文件类型     | 推荐权限 | 说明                         |
|--------------|----------|------------------------------|
| 可执行脚本   | 755      | Shell/Python 等可执行文件    |
| 配置文件     | 644      | 静态配置文件                 |
| 敏感配置     | 600      | 含密码/密钥的配置            |
| 日志文件     | 644      | 日志输出文件                 |
| 数据文件     | 644      | 数据存储文件                 |
| 目录         | 755      | 普通目录                     |
| 敏感目录     | 700      | 含敏感文件的目录             |

---

## 3. 自动化生成命令

### 3.1 完整清单自动生成脚本

```bash
#!/bin/bash
# =============================================================================
# 交付清单自动生成脚本
# DNA: DRAGON-SOUL-DELIVERY-GEN-v1.0.0
# =============================================================================
set -euo pipefail

# 配置
DELIVERY_DIR="${1:-/opt/dragon_soul}"
OUTPUT_FILE="${2:-DELIVERY_CHECKLIST.md}"
REPO_ROOT="${3:-$(git rev-parse --show-toplevel 2>/dev/null || echo '.')}"

# DNA 标识正则
DNA_PATTERN="DNA[[:space:]]*[:][[:space:]]*DRAGON-SOUL"

echo "正在生成交付清单..."
echo "扫描目录: ${DELIVERY_DIR}"
echo "输出文件: ${OUTPUT_FILE}"

# 生成清单头部
cat > "${OUTPUT_FILE}" << 'HEADER'
<!-- DNA: DRAGON-SOUL-DELIVERY-CHECKLIST-AUTO -->
| 序号 | 文件名 | 文件类型 | 行数 | DNA 标识 | Git 提交哈希 | 文件权限 | 存储路径 | SHA256 哈希值 | 状态 |
|------|--------|----------|------|----------|-------------|----------|----------|--------------|------|
HEADER

# 计数器
counter=0

# 遍历交付目录中的文件
while IFS= read -r -d '' file; do
    # 跳过目录和二进制文件（可选）
    if [[ -d "$file" ]]; then
        continue
    fi

    ((counter++)) || true

    # 文件名
    filename=$(basename "$file")

    # 文件类型
    extension="${filename##*.}"
    case "$extension" in
        py)   filetype="Python" ;;
        sh)   filetype="Shell" ;;
        md)   filetype="Markdown" ;;
        yml|yaml) filetype="YAML" ;;
        json) filetype="JSON" ;;
        conf|cfg) filetype="Config" ;;
        *)    filetype="Other" ;;
    esac

    # 行数
    line_count=$(wc -l < "$file" 2>/dev/null || echo "N/A")

    # DNA 标识
    dna_id=$(grep -oP 'DNA\s*:\s*DRAGON-SOUL[^[:space:]]*' "$file" 2>/dev/null | head -1 || echo "N/A")
    if [[ -z "$dna_id" ]]; then
        dna_id="MISSING"
    fi

    # Git 提交哈希
    if git -C "${REPO_ROOT}" log --oneline -- "$file" &>/dev/null; then
        git_hash=$(git -C "${REPO_ROOT}" log -1 --format="%h" -- "$file" 2>/dev/null || echo "N/A")
    else
        git_hash="N/A"
    fi

    # 文件权限
    file_perms=$(stat -c '%a' "$file" 2>/dev/null || stat -f '%Lp' "$file" 2>/dev/null || echo "N/A")

    # 存储路径
    storage_path=$(dirname "$file")

    # SHA256 哈希值
    sha256_hash=$(sha256sum "$file" 2>/dev/null | awk '{print $1}' || shasum -a 256 "$file" 2>/dev/null | awk '{print $1}' || echo "N/A")

    # 状态
    if [[ "$dna_id" == "MISSING" || "$dna_id" == "N/A" ]]; then
        status="❌"
    elif [[ "$sha256_hash" == "N/A" ]]; then
        status="❌"
    else
        status="✅"
    fi

    # 输出表格行
    printf "| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s |\n" \
        "$counter" \
        "$filename" \
        "$filetype" \
        "$line_count" \
        "$dna_id" \
        "$git_hash" \
        "$file_perms" \
        "$storage_path" \
        "$sha256_hash" \
        "$status" \
        >> "${OUTPUT_FILE}"

done < <(find "$DELIVERY_DIR" -maxdepth 2 -type f -print0 2>/dev/null)

echo "交付清单生成完成: ${OUTPUT_FILE}"
echo "共处理 ${counter} 个文件"
```

### 3.2 单个文件信息生成命令

```bash
# 获取文件所有必要信息的快捷命令
file_info() {
    local filepath="$1"

    echo "===== 文件信息: ${filepath} ====="
    echo "文件名:        $(basename "$filepath")"
    echo "文件类型:      $(file -b --mime-type "$filepath")"
    echo "行数:          $(wc -l < "$filepath")"
    echo "DNA 标识:      $(grep -oP 'DNA\s*:\s*DRAGON-SOUL[^[:space:]]*' "$filepath" 2>/dev/null | head -1 || echo 'MISSING')"
    echo "Git 提交哈希:  $(git log -1 --format='%h' -- "$filepath" 2>/dev/null || echo 'N/A')"
    echo "文件权限:      $(stat -c '%a' "$filepath" 2>/dev/null)"
    echo "存储路径:      $(dirname "$filepath")"
    echo "SHA256:        $(sha256sum "$filepath" | awk '{print $1}')"
    echo "===================================="
}

# 使用示例:
# file_info /path/to/your/file.py
```

### 3.3 完整性验证脚本

```bash
#!/bin/bash
# =============================================================================
# 交付清单完整性验证脚本
# DNA: DRAGON-SOUL-DELIVERY-VERIFY-v1.0.0
# =============================================================================
set -euo pipefail

verify_delivery() {
    local checklist_file="$1"
    local issues=0

    echo "===== 交付清单完整性验证 ====="

    # 读取清单并验证每个文件
    tail -n +3 "$checklist_file" | while IFS='|' read -r seq filename filetype lines dna git_hash perms path sha256 status; do
        # 去除空格
        filename=$(echo "$filename" | xargs)
        dna=$(echo "$dna" | xargs)
        sha256=$(echo "$sha256" | xargs)
        status=$(echo "$status" | xargs)

        # 跳过空行
        [[ -z "$filename" ]] && continue

        # 验证 DNA 标识
        if [[ "$dna" == "MISSING" || "$dna" == "N/A" ]]; then
            echo "❌ [BLOCKING] DNA 标识缺失: ${filename}"
            ((issues++)) || true
        fi

        # 验证 SHA256
        if [[ "$sha256" == "N/A" ]]; then
            echo "❌ [BLOCKING] SHA256 无法计算: ${filename}"
            ((issues++)) || true
        fi

        # 验证状态
        if [[ "$status" == "❌" ]]; then
            echo "❌ [BLOCKING] 文件未通过验证: ${filename}"
            ((issues++)) || true
        fi
    done

    if [[ $issues -eq 0 ]]; then
        echo "✅ 所有文件通过验证，交付清单完整"
        return 0
    else
        echo "❌ 发现 ${issues} 个阻塞问题，流程暂停"
        return 1
    fi
}
```

---

## 4. 使用示例

### 4.1 完整填写的交付清单示例

| 序号 | 文件名 | 文件类型 | 行数 | DNA 标识 | Git 提交哈希 | 文件权限 | 存储路径 | SHA256 哈希值 | 状态 |
|------|--------|----------|------|----------|-------------|----------|----------|--------------|------|
| 1 | validate_welding_point.py | Python | 287 | DNA: DRAGON-SOUL-WELD-v2.1.0 | a3f7e2d9 | 644 | /opt/dragon_soul/bin/ | 8f7b3c2d1e5a9f6b4c8d2e1a7f3b5c9d4e6a8f2b1c3d5e7f9a0b2c4d6e8f0a1b | ✅ |
| 2 | safe_cleanup.sh | Shell | 156 | DNA: DRAGON-SOUL-SAFE-CLEANUP-v1.2.0 | b8e5c1a4 | 755 | /opt/dragon_soul/bin/ | 3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a1b3c5d7e9f1a3b5c7d9e1f3a5b | ✅ |
| 3 | health_check.sh | Shell | 98 | DNA: DRAGON-SOUL-HEALTH-v1.0.0 | c2d4e6f8 | 755 | /opt/dragon_soul/scripts/ | 1b3c5d7e9f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a1b3c | ✅ |
| 4 | system.conf | Config | 45 | DNA: DRAGON-SOUL-CONF-v1.0.0 | d5f7a9b1 | 644 | /opt/dragon_soul/etc/ | 5c7d9e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a1b3c5d7e9f1a3b5c7d | ✅ |
| 5 | credentials.env | Config | 12 | DNA: DRAGON-SOUL-CRED-v1.0.0 | e8a0b2c4 | 600 | /opt/dragon_soul/secrets/ | 7d9e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a1b3c5d7e9f1a3b5c7d9e | ✅ |

### 4.2 阻塞场景示例

**场景**: DNA 标识缺失

| 序号 | 文件名 | 文件类型 | 行数 | DNA 标识 | Git 提交哈希 | 文件权限 | 存储路径 | SHA256 哈希值 | 状态 |
|------|--------|----------|------|----------|-------------|----------|----------|--------------|------|
| 1 | unmarked_script.sh | Shell | 50 | **MISSING** | a1b2c3d4 | 755 | /opt/dragon_soul/bin/ | 9f8e7d6c5b4a3928172635404938271655049382718493827165049382716253 | ❌ |

**处理结果**: ⛔ **流程阻塞** — 文件缺少 DNA 标识，必须补充后才能继续。

---

## 5. 验证流程

```
┌─────────────────────────────────────────────────────────────┐
│                    交付清单验证流程                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ 生成清单  │───▶│ 自动验证  │───▶│ 人工审核  │              │
│  └──────────┘    └────┬─────┘    └────┬─────┘              │
│                       │                │                     │
│                       ▼                ▼                     │
│                  ┌──────────┐    ┌──────────┐              │
│                  │ 通过 ✅  │    │ 通过 ✅  │              │
│                  └────┬─────┘    └────┬─────┘              │
│                       │                │                     │
│                       └────────┬───────┘                     │
│                                ▼                             │
│                         ┌──────────┐                         │
│                         │ 允许交付  │                         │
│                         └──────────┘                         │
│                                │                             │
│                       ┌────────┴────────┐                    │
│                       ▼                 ▼                    │
│                  ┌──────────┐     ┌──────────┐              │
│                  │ 阻塞 ❌  │     │ 阻塞 ❌  │              │
│                  └────┬─────┘     └────┬─────┘              │
│                       │                │                     │
│                       └────────┬───────┘                     │
│                                ▼                             │
│                         ┌──────────┐                         │
│                         │ 暂停流程  │                         │
│                         │ 修复问题  │                         │
│                         └──────────┘                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.1 自动化验证检查点

```bash
#!/bin/bash
# 交付清单阻塞性验证
check_blocking_items() {
    local checklist="$1"
    local blockers=0

    echo "===== 阻塞项检查 ====="

    # 检查1: 所有必填字段非空
    if grep -q "| *| *| *| *|" "$checklist"; then
        echo "❌ [BLOCKING] 发现空字段"
        ((blockers++)) || true
    fi

    # 检查2: 无 MISSING DNA
    if grep -q "MISSING" "$checklist"; then
        echo "❌ [BLOCKING] 发现 DNA 标识缺失"
        ((blockers++)) || true
    fi

    # 检查3: 无 ❌ 状态
    if grep -q "❌" "$checklist"; then
        echo "❌ [BLOCKING] 发现未通过验证的文件"
        ((blockers++)) || true
    fi

    # 检查4: SHA256 不为 N/A
    if grep -q "N/A.*N/A" "$checklist"; then
        echo "❌ [BLOCKING] 发现无法计算的哈希值"
        ((blockers++)) || true
    fi

    if [[ $blockers -eq 0 ]]; then
        echo "✅ 无阻塞项，流程可以继续"
        return 0
    else
        echo "⛔ 发现 ${blockers} 个阻塞项，流程暂停！"
        return 1
    fi
}
```

---

## 6. 集成到 CI/CD 流水线

```yaml
# .gitlab-ci.yml 或 .github/workflows/delivery.yml
# DNA: DRAGON-SOUL-CICD-DELIVERY-v1.0.0

delivery_check:
  stage: deploy
  script:
    # 1. 生成交付清单
    - bash scripts/generate_checklist.sh "$CI_PROJECT_DIR" "DELIVERY_CHECKLIST.md"

    # 2. 验证清单完整性
    - bash scripts/verify_delivery.sh "DELIVERY_CHECKLIST.md"

    # 3. 检查阻塞项
    - |
      if ! bash scripts/check_blocking_items.sh "DELIVERY_CHECKLIST.md"; then
        echo "⛔ 交付清单验证失败，阻塞部署流程"
        exit 1
      fi

    # 4. 归档交付清单
    - cp DELIVERY_CHECKLIST.md "$CI_PROJECT_DIR/artifacts/"

  artifacts:
    paths:
      - DELIVERY_CHECKLIST.md
    expire_in: 1 year

  # 阻塞规则：验证失败时阻止部署
  allow_failure: false
```

---

## 7. 变更记录

| 版本   | 日期       | 修改人       | 修改内容                 |
|--------|------------|--------------|--------------------------|
| 1.0.0  | 2024-01-15 | 龍魂交付团队 | 初始版本，修复 M7        |
