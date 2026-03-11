#!/bin/bash
# ============================================================
# 龍魂归集工具包 v2.1 - 快速开始指南
# ============================================================

# ══════════════════════════════════════════════════════════════
# 第一步：进入脚本目录
# ══════════════════════════════════════════════════════════════

cd /Users/zuimeidedeyihan/longhun-system

# ══════════════════════════════════════════════════════════════
# 第二步：查看脚本文件
# ══════════════════════════════════════════════════════════════

ls -la digital_archive_toolkit_v2.1.sh

# ══════════════════════════════════════════════════════════════
# 第三步：给脚本添加执行权限
# ══════════════════════════════════════════════════════════════

chmod +x digital_archive_toolkit_v2.1.sh

# ══════════════════════════════════════════════════════════════
# 第四步：运行脚本（交互式菜单）
# ══════════════════════════════════════════════════════════════

./digital_archive_toolkit_v2.1.sh

# ══════════════════════════════════════════════════════════════
# 第五步：或者直接运行特定功能（非交互式）
# ══════════════════════════════════════════════════════════════

# 选项A：初始化归档目录
./digital_archive_toolkit_v2.1.sh init

# 选项B：解压压缩包
./digital_archive_toolkit_v2.1.sh unpack ~/Downloads

# 选项C：按类型归类文件
./digital_archive_toolkit_v2.1.sh classify ~/Downloads

# 选项D：查找重复文件
./digital_archive_toolkit_v2.1.sh sha256

# 选项E：移除重复文件
./digital_archive_toolkit_v2.1.sh dedup

# 选项F：检查iCloud状态
./digital_archive_toolkit_v2.1.sh icloud

# 选项G：Git初始化
./digital_archive_toolkit_v2.1.sh git-init

# 选项H：Git提交快照
./digital_archive_toolkit_v2.1.sh git-push

# 选项I：磁盘分析
./digital_archive_toolkit_v2.1.sh disk

# 选项J：GPG签名
./digital_archive_toolkit_v2.1.sh gpg-sign

# 选项K：GPG验证
./digital_archive_toolkit_v2.1.sh gpg-verify

# ══════════════════════════════════════════════════════════════
# 第六步：批量模式（一键全流程）
# ══════════════════════════════════════════════════════════════

# 设置批量模式
export LONGHUN_BATCH_MODE=1
export LONGHUN_TASKS="1,4,10"

# 运行批量任务
./digital_archive_toolkit_v2.1.sh

# ══════════════════════════════════════════════════════════════
# 第七步：查看报告
# ══════════════════════════════════════════════════════════════

# 查看归档目录
ls -la ~/CreativeArchive

# 查看报告目录
ls -la ~/CreativeArchive/_reports

# 查看最新报告
cat ~/CreativeArchive/_reports/duplicates_*.txt | tail -50

# ══════════════════════════════════════════════════════════════
# 第八步：配置文件（可选）
# ══════════════════════════════════════════════════════════════

# 创建配置目录
mkdir -p ~/.longhun

# 创建配置文件
cat > ~/.longhun/config.yml << 'EOF'
dna_prefix: #龍芯⚡️
uid_code: 9622
archive_root: ~/CreativeArchive
github_user: uid9622
github_repo: cnsh
EOF

# 创建类型映射配置
cat > ~/CreativeArchive/.type_mappings.conf << 'EOF'
文字创作=txt md doc docx pdf rtf pages odt
图像设计=jpg jpeg png gif bmp tiff psd ai svg webp heic raw cr2 nef
音频视频=mp3 wav flac aac ogg mp4 mov avi mkv m4v m4a
代码脚本=sh py js ts html css json xml yaml yml rb go rs c cpp java
3D模型=blend obj fbx stl dae
科研数据=csv xlsx mat nc dat
电子书=epub mobi azw3 lit
压缩包=zip rar 7z tar bz2 gz
字体文件=ttf otf woff woff2 eot
数据库=sql db sqlite mdb accdb
虚拟机=vmdk vbox ova ovf qcow2
EOF

# ══════════════════════════════════════════════════════════════
# 第九步：环境变量配置（可选）
# ══════════════════════════════════════════════════════════════

# 自定义DNA前缀
export LONGHUN_DNA_PREFIX="#我的龍芯"

# 自定义归档目录
export ARCHIVE_ROOT=~/MyCreativeArchive

# 启用JSON日志
export LONGHUN_LOG_JSON=1

# 设置并行任务数
export LONGHUN_JOBS=8

# 启用并行处理
export LONGHUN_PARALLEL=1

# 禁用颜色输出（云端环境）
export LONGHUN_NO_COLOR=1

# 设置云端环境
export CLOUD_PROVIDER=aliyun

# ══════════════════════════════════════════════════════════════
# 第十步：定时任务（可选）
# ══════════════════════════════════════════════════════════════

# 编辑crontab
crontab -e

# 添加以下定时任务（每天凌晨2点执行）
# 0 2 * * * cd /Users/zuimeidedeyihan/longhun-system && LONGHUN_BATCH_MODE=1 LONGHUN_TASKS="1,4,10" ./digital_archive_toolkit_v2.1.sh

# 每周日凌晨3点执行完整归档
# 0 3 * * 0 cd /Users/zuimeidedeyihan/longhun-system && LONGHUN_BATCH_MODE=1 LONGHUN_TASKS="1,2,3,4,5,10" ./digital_archive_toolkit_v2.1.sh

# ══════════════════════════════════════════════════════════════
# 常用命令速查
# ══════════════════════════════════════════════════════════════

# 查看归档目录结构
tree ~/CreativeArchive -L 3

# 查看磁盘使用情况
du -sh ~/CreativeArchive/*

# 查看文件数量
find ~/CreativeArchive -type f | wc -l

# 查看重复文件
cat ~/CreativeArchive/_reports/dup_list_*.csv | wc -l

# 查看iCloud状态
cat ~/CreativeArchive/_reports/icloud_status_*.txt

# 查看磁盘报告
cat ~/CreativeArchive/_reports/disk_report_*.txt

# 查看GPG签名报告
cat ~/CreativeArchive/_reports/gpg_sign_*.txt

# ══════════════════════════════════════════════════════════════
# 故障排查
# ══════════════════════════════════════════════════════════════

# 如果脚本没有执行权限
chmod +x digital_archive_toolkit_v2.1.sh

# 如果找不到配置文件
ls -la ~/.longhun/config.yml

# 如果归档目录不存在
mkdir -p ~/CreativeArchive

# 如果报告目录不存在
mkdir -p ~/CreativeArchive/_reports

# 查看日志文件
cat ~/.longhun/.longhun.log

# 如果并行处理失败
export LONGHUN_PARALLEL=0

# 如果iCloud路径错误
export ICLOUD_DIR=/custom/icloud/path

# ══════════════════════════════════════════════════════════════
# 完成状态检查
# ══════════════════════════════════════════════════════════════

# 检查脚本是否存在
test -f digital_archive_toolkit_v2.1.sh && echo "脚本文件存在" || echo "脚本文件不存在"

# 检查执行权限
test -x digital_archive_toolkit_v2.1.sh && echo "执行权限已设置" || echo "需要设置执行权限"

# 检查配置文件
test -f ~/.longhun/config.yml && echo "配置文件存在" || echo "配置文件不存在"

# 检查归档目录
test -d ~/CreativeArchive && echo "归档目录存在" || echo "归档目录不存在"

# 检查报告目录
test -d ~/CreativeArchive/_reports && echo "报告目录存在" || echo "报告目录不存在"

# 检查Git仓库
test -d ~/CreativeArchive/.git && echo "Git仓库已初始化" || echo "Git仓库未初始化"

echo ""
echo "=========================================="
echo "龍魂归集工具包v2.1已准备就绪"
echo "脚本位置: /Users/zuimeidedeyihan/longhun-system/digital_archive_toolkit_v2.1.sh"
echo "归档目录: ~/CreativeArchive"
echo "报告目录: ~/CreativeArchive/_reports"
echo "=========================================="
echo ""
echo "快速开始："
echo "  ./digital_archive_toolkit_v2.1.sh"
echo ""
echo "查看菜单选项："
echo "  0 一键全流程"
echo "  1 初始化归档"
echo "  2 解压压缩包"
echo "  3 归类文件"
echo "  4 查找重复"
echo "  5 移除重复"
echo "  6 iCloud检查"
echo "  7 Git初始化"
echo "  8 Git提交"
echo "  9 磁盘分析"
echo "  10 GPG签名"
echo "  11 GPG验证"
echo ""
echo "=========================================="
echo "完成！现在可以运行脚本了！"
echo "=========================================="
