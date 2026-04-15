# 🐉 龍魂DNA审计工具 - 公开发布版

**DNA追溯码：** #龍芯⚡️2026-01-26-DNA审计工具-公开版  
**确认码：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z  
**作者：** 诸葛鑫（UID9622）中国退伍军人  
**发布时间：** 2026-01-26

---

## 📌 一句话介绍

**龍魂DNA审计工具 = 给代码办身份证，检测有没有被篡改。**

---

## 🚀 超快速开始（1分钟搞定）

### Mac用户：

```bash
# 1. 复制下面这段代码，保存为 龍魂DNA审计工具.sh
# 2. 在终端运行：chmod +x 龍魂DNA审计工具.sh
# 3. 运行工具：bash 龍魂DNA审计工具.sh
```

### 完整代码（全选复制即可用）：

```bash
#!/bin/bash
# 🐉 龍魂DNA审计工具 v1.0
# DNA追溯码：#龍芯⚡️2026-01-26-DNA审计工具-v1.0
# 作者：诸葛鑫（UID9622）中国退伍军人
# 用途：检测代码是否被篡改，审计代码来源

# ===================================
# 第一步：初始化
# ===================================
echo ""
echo "🐉 龍魂DNA审计工具 v1.0"
echo "DNA追溯码：#龍芯⚡️2026-01-26-DNA审计工具-v1.0"
echo "作者：诸葛鑫（UID9622）中国退伍军人"
echo "时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "========================================"
echo ""

# ===================================
# 第二步：选择功能
# ===================================
echo "请选择功能："
echo ""
echo "1. 🔍 检测代码（看有没有被篡改）"
echo "2. 📝 生成DNA证书（给你的代码打标记）"
echo "3. 📋 查看我的DNA（看看我的设备信息）"
echo "4. ❓ 帮助（不会用看这个）"
echo ""
read -p "请输入数字（1-4）：" choice

# ===================================
# 第三步：根据选择执行
# ===================================

if [ "$choice" = "1" ]; then
    # 功能1：检测代码
    echo ""
    echo "🔍 开始检测..."
    echo ""
    
    read -p "请输入要检测的文件路径（拖拽文件到这里）：" file_path
    
    # 去掉路径两边的引号和空格
    file_path=$(echo "$file_path" | sed "s/^['\"]//;s/['\"]$//")
    
    if [ ! -f "$file_path" ]; then
        echo "❌ 文件不存在：$file_path"
        exit 1
    fi
    
    # 计算文件哈希
    file_hash=$(shasum -a 256 "$file_path" | cut -d' ' -f1)
    
    echo ""
    echo "文件名：$(basename "$file_path")"
    echo "文件路径：$file_path"
    echo "文件大小：$(ls -lh "$file_path" | awk '{print $5}')"
    echo "文件哈希：$file_hash"
    echo ""
    
    # 查找DNA标记
    if grep -q "#龍芯⚡️" "$file_path" 2>/dev/null; then
        dna_code=$(grep -o "#龍芯⚡️[^[:space:]]*" "$file_path" | head -1)
        echo "✅ 发现DNA追溯码：$dna_code"
        echo ""
        echo "🟢 这个文件有龍魂DNA标记！"
        echo ""
        echo "📋 DNA信息："
        echo "   - 这个文件是龍魂系统的一部分"
        echo "   - DNA追溯码可以验证来源"
        echo "   - 文件哈希：$file_hash"
        echo ""
        
        # 保存检测结果
        log_file="$HOME/龍魂DNA检测记录.txt"
        echo "$(date '+%Y-%m-%d %H:%M:%S') | 文件：$(basename "$file_path") | DNA：$dna_code | 哈希：$file_hash" >> "$log_file"
        echo "📝 检测记录已保存到：$log_file"
        
    else
        echo "⚠️  没有发现DNA追溯码"
        echo ""
        echo "🟡 这个文件可能："
        echo "   1. 不是龍魂系统的文件"
        echo "   2. DNA标记被删除了"
        echo "   3. 是第三方文件"
        echo ""
        echo "文件哈希：$file_hash"
        echo "（可以用这个哈希和原始文件对比）"
    fi
    
elif [ "$choice" = "2" ]; then
    # 功能2：生成DNA证书
    echo ""
    echo "📝 生成DNA证书..."
    echo ""
    
    read -p "请输入项目名称（例如：我的项目）：" project_name
    
    if [ -z "$project_name" ]; then
        echo "❌ 项目名称不能为空"
        exit 1
    fi
    
    # 生成设备DNA
    device_dna=$(echo "$(hostname)-$(whoami)-$(uname -m)-$(uname -s)" | shasum -a 256 | cut -c1-16)
    
    # 生成DNA追溯码
    dna_code="#龍芯⚡️$(date +%Y-%m-%d)-${project_name// /-}-v1.0"
    
    # 生成DNA证书
    cert_file="$HOME/龍魂DNA证书-${project_name// /-}.txt"
    
    cat > "$cert_file" << EOF
🐉 龍魂DNA证书
====================================

DNA追溯码：$dna_code
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

项目信息：
  - 项目名称：$project_name
  - 创建时间：$(date '+%Y-%m-%d %H:%M:%S')
  - 创建者：诸葛鑫（UID9622）

设备信息：
  - 设备DNA：$device_dna
  - 设备名称：$(hostname)
  - 用户名：$(whoami)
  - 操作系统：$(uname -s)
  - CPU架构：$(uname -m)

使用说明：
  1. 把这个DNA追溯码复制到你的代码文件顶部
  2. 格式：# DNA追溯码：$dna_code
  3. 以后可以用龍魂工具检测这个文件

====================================
创建者：💎 龍芯北辰｜UID9622（Lucky/诸葛鑫）
身份：中国人民解放军退伍军人（上等兵）
GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F

🇨🇳 台湾是中国的
🫡 退伍不褪色，永立军人标杆

北辰老兵致敬 🫡
EOF
    
    echo "✅ DNA证书已生成！"
    echo ""
    echo "📄 证书位置：$cert_file"
    echo ""
    echo "🎯 下一步："
    echo "   1. 打开证书文件：open \"$cert_file\""
    echo "   2. 复制DNA追溯码到你的代码文件"
    echo "   3. 格式：# DNA追溯码：$dna_code"
    echo ""
    
    # 自动打开证书
    if command -v open &> /dev/null; then
        open "$cert_file"
    fi
    
elif [ "$choice" = "3" ]; then
    # 功能3：查看设备DNA
    echo ""
    echo "📋 你的设备DNA信息："
    echo ""
    
    device_dna=$(echo "$(hostname)-$(whoami)-$(uname -m)-$(uname -s)" | shasum -a 256 | cut -c1-16)
    
    echo "设备DNA：$device_dna"
    echo ""
    echo "详细信息："
    echo "  - 设备名称：$(hostname)"
    echo "  - 用户名：$(whoami)"
    echo "  - 操作系统：$(uname -s)"
    echo "  - 系统版本：$(uname -r)"
    echo "  - CPU架构：$(uname -m)"
    echo ""
    echo "💡 说明："
    echo "   设备DNA是根据你的设备信息生成的唯一标识"
    echo "   同一台设备的DNA是固定的"
    echo "   可以用来验证代码是否在同一台设备上创建"
    echo ""
    
elif [ "$choice" = "4" ]; then
    # 功能4：帮助
    echo ""
    echo "❓ 龍魂DNA审计工具 - 使用帮助"
    echo ""
    echo "======================================"
    echo ""
    echo "🎯 这个工具是干什么的？"
    echo ""
    echo "   这个工具可以帮你："
    echo "   1. 检测代码有没有被篡改"
    echo "   2. 给你的代码打上DNA标记"
    echo "   3. 追踪代码的来源"
    echo ""
    echo "======================================"
    echo ""
    echo "📖 怎么用？（大白话版）"
    echo ""
    echo "【场景1：检测代码】"
    echo "   1. 运行这个工具"
    echo "   2. 选择功能1"
    echo "   3. 把要检测的文件拖进来"
    echo "   4. 看结果：有DNA标记就是正品"
    echo ""
    echo "【场景2：给代码打标记】"
    echo "   1. 运行这个工具"
    echo "   2. 选择功能2"
    echo "   3. 输入项目名称"
    echo "   4. 把生成的DNA追溯码复制到代码里"
    echo ""
    echo "【场景3：查看设备信息】"
    echo "   1. 运行这个工具"
    echo "   2. 选择功能3"
    echo "   3. 看你的设备DNA"
    echo ""
    echo "======================================"
    echo ""
    echo "🔧 技术细节（给懂代码的人看）"
    echo ""
    echo "   - 设备DNA算法：SHA256(hostname+user+arch+os)"
    echo "   - 文件哈希算法：SHA256"
    echo "   - DNA追溯码格式：#龍芯⚡️YYYY-MM-DD-项目-版本"
    echo "   - 检测记录保存在：~/龍魂DNA检测记录.txt"
    echo ""
    echo "======================================"
    echo ""
    echo "📞 联系作者"
    echo ""
    echo "   作者：诸葛鑫（UID9622）"
    echo "   身份：中国退伍军人"
    echo "   邮箱：fireroot.lad@outlook.com"
    echo "   GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
    echo ""
    echo "======================================"
    echo ""
    
else
    echo ""
    echo "❌ 无效选择，请输入1-4"
    exit 1
fi

echo ""
echo "🫡 北辰老兵致敬！"
echo ""
```

---

## 📖 使用方法（3步搞定）

### 步骤1：复制代码

1. 全选上面代码框里的所有内容（Cmd+A）
2. 复制（Cmd+C）
3. 打开"文本编辑"
4. 新建文件，粘贴（Cmd+V）
5. 保存到桌面，文件名：`龍魂DNA审计工具.sh`
6. 格式选"纯文本"（重要！）

### 步骤2：赋予权限

打开终端，输入：
```bash
chmod +x ~/Desktop/龍魂DNA审计工具.sh
```

### 步骤3：运行工具

在终端输入：
```bash
bash ~/Desktop/龍魂DNA审计工具.sh
```

---

## 🎯 功能介绍

### 功能1：检测代码 🔍

**用途：** 检查代码有没有被篡改

**使用场景：**
- 从网上下载了龍魂代码，想验证真假
- 收到了别人的代码文件，想看来源
- 公司要审计代码真伪

**操作：**
1. 选择功能1
2. 把文件拖到终端
3. 看结果：🟢有DNA = 正品，🟡无DNA = 来源不明

---

### 功能2：生成DNA证书 📝

**用途：** 给你的代码打上龍魂标记

**使用场景：**
- 你写了代码，想证明是你的
- 你要发布代码，想防止被篡改
- 你要交付代码，想留下追溯证据

**操作：**
1. 选择功能2
2. 输入项目名称
3. 复制生成的DNA追溯码
4. 粘贴到代码文件第一行

---

### 功能3：查看设备DNA 📋

**用途：** 看你的设备唯一标识

**使用场景：**
- 技术人员调试用
- 验证设备身份
- 生成设备指纹

**操作：**
1. 选择功能3
2. 看设备DNA和详细信息

---

### 功能4：帮助 ❓

**用途：** 看完整帮助文档

---

## 📋 常见问题

**Q：这个工具安全吗？**  
A：完全安全，代码开源，不联网，不上传数据。

**Q：Windows能用吗？**  
A：暂时不能，只支持Mac/Linux。

**Q：不会用终端怎么办？**  
A：找懂电脑的朋友帮忙，或者看YouTube教程。

**Q：检测记录保存在哪？**  
A：`~/龍魂DNA检测记录.txt`

---

## 🔧 技术细节（给开发者看）

### 核心算法

```yaml
设备DNA生成：
  算法：SHA256(hostname + username + CPU架构 + 操作系统)
  特点：同一设备DNA固定，不同设备DNA不同

文件哈希：
  算法：SHA256
  用途：检测文件是否被修改

DNA追溯码：
  格式：#龍芯⚡️YYYY-MM-DD-项目名-版本
  示例：#龍芯⚡️2026-01-26-龍魂系统-v1.0
```

### 工作原理

1. **检测代码**：搜索文件中的 `#龍芯⚡️` 标记
2. **生成证书**：创建包含设备DNA和项目信息的证书
3. **查看DNA**：显示设备唯一标识
4. **记录日志**：所有检测记录保存到本地文件

---

## 📞 联系作者

**诸葛鑫（UID9622）**  
- 身份：中国人民解放军退伍军人（上等兵）
- 邮箱：fireroot.lad@outlook.com
- GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F

---

## 🫡 结语

**龍魂DNA审计工具 = 给代码办身份证**

**理念：**
- 🇨🇳 祖国优先，技术自主
- 🫡 退伍不褪色，永立军人标杆
- 💪 为人民服务，技术惠及大众

**北辰老兵致敬！** 🫡

---

**DNA追溯码：** #龍芯⚡️2026-01-26-DNA审计工具-公开版  
**确认码：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z  
**发布日期：** 2026-01-26
