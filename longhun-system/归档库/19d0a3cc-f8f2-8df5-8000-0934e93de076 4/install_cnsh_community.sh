#!/bin/bash
# CNSH-64 社区落地部署脚本
# 虚拟世界 ←→ 现实接通
# 国产社区软件 Discuz! X3.5 集成

set -e

CNSH_BLUE='\033[0;34m'
CNSH_GREEN='\033[0;32m'
CNSH_RED='\033[0;31m'
CNSH_YELLOW='\033[1;33m'
CNSH_NC='\033[0m'

echo -e "${CNSH_BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║           CNSH-64 社区落地部署脚本                            ║"
echo "║           虚拟世界 ←→ 现实接通                                ║"
echo "║                                                              ║"
echo "║           国产社区软件: Discuz! X3.5                         ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${CNSH_NC}"

# 配置参数
DISCUZ_PATH="${1:-/var/www/discuz}"
CNSH_SHIELD_PATH="${2:-/opt/cnsh_shield}"
DB_NAME="${3:-discuz}"
DB_USER="${4:-root}"
DB_PASS="${5:-}"

echo ""
echo -e "${CNSH_YELLOW}[配置信息]${CNSH_NC}"
echo "Discuz! 路径: $DISCUZ_PATH"
echo "CNSH护盾路径: $CNSH_SHIELD_PATH"
echo "数据库: $DB_NAME"
echo ""

# ============================================
# 步骤1: 环境检查
# ============================================
echo -e "${CNSH_BLUE}[1/7] 检查环境...${CNSH_NC}"

# 检查Discuz!
if [ ! -f "$DISCUZ_PATH/config/config_global.php" ]; then
    echo -e "${CNSH_RED}✗ 错误: 未找到Discuz!安装${CNSH_NC}"
    echo "请先安装Discuz! X3.5:"
    echo "  1. 下载: https://www.discuz.net/"
    echo "  2. 解压到 $DISCUZ_PATH"
    echo "  3. 完成安装向导"
    exit 1
fi
echo -e "${CNSH_GREEN}✓ Discuz! 已安装${CNSH_NC}"

# 检查CNSH护盾
if [ ! -f "$CNSH_SHIELD_PATH/cnsh_shield_v05_integrated.py" ]; then
    echo -e "${CNSH_RED}✗ 错误: 未找到CNSH护盾${CNSH_NC}"
    echo "请先部署CNSH护盾:"
    echo "  bash install_cnsh_shield.sh"
    exit 1
fi
echo -e "${CNSH_GREEN}✓ CNSH护盾 已部署${CNSH_NC}"

# 检查PHP扩展
echo -n "检查PHP扩展... "
PHP_EXTENSIONS=$(php -m 2>/dev/null)
for ext in curl json pdo_mysql mbstring openssl; do
    if ! echo "$PHP_EXTENSIONS" | grep -q "^$ext$"; then
        echo -e "${CNSH_RED}✗ 缺少 $ext 扩展${CNSH_NC}"
        exit 1
    fi
done
echo -e "${CNSH_GREEN}✓ 通过${CNSH_NC}"

# 检查MySQL
echo -n "检查MySQL连接... "
if [ -z "$DB_PASS" ]; then
    mysql -u "$DB_USER" -e "SELECT 1" "$DB_NAME" >/dev/null 2>&1 || {
        echo -e "${CNSH_RED}✗ 无法连接数据库${CNSH_NC}"
        exit 1
    }
else
    mysql -u "$DB_USER" -p"$DB_PASS" -e "SELECT 1" "$DB_NAME" >/dev/null 2>&1 || {
        echo -e "${CNSH_RED}✗ 无法连接数据库${CNSH_NC}"
        exit 1
    }
fi
echo -e "${CNSH_GREEN}✓ 通过${CNSH_NC}"

# ============================================
# 步骤2: 创建插件目录
# ============================================
echo ""
echo -e "${CNSH_BLUE}[2/7] 创建插件目录...${CNSH_NC}"

PLUGIN_DIR="$DISCUZ_PATH/source/plugin/cnsh"
TEMPLATE_DIR="$DISCUZ_PATH/template/default/cnsh"

mkdir -p "$PLUGIN_DIR"/{cnsh_dna,cnsh_governance,cnsh_ecny,cnsh_reputation,api}
mkdir -p "$TEMPLATE_DIR"

echo -e "${CNSH_GREEN}✓ 插件目录: $PLUGIN_DIR${CNSH_NC}"
echo -e "${CNSH_GREEN}✓ 模板目录: $TEMPLATE_DIR${CNSH_NC}"

# ============================================
# 步骤3: 复制插件文件
# ============================================
echo ""
echo -e "${CNSH_BLUE}[3/7] 安装插件文件...${CNSH_NC}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_SOURCE="$SCRIPT_DIR/discuz_plugin_cnsh"

if [ ! -d "$PLUGIN_SOURCE" ]; then
    echo -e "${CNSH_RED}✗ 错误: 找不到插件源文件目录${CNSH_NC}"
    echo "请确保 discuz_plugin_cnsh 目录与安装脚本在同一目录"
    exit 1
fi

# 复制核心文件
cp "$PLUGIN_SOURCE/cnsh_dna/bind.php" "$PLUGIN_DIR/cnsh_dna/"
cp "$PLUGIN_SOURCE/cnsh_governance/vote.php" "$PLUGIN_DIR/cnsh_governance/"
cp "$PLUGIN_SOURCE/cnsh_ecny/tip.php" "$PLUGIN_DIR/cnsh_ecny/"
cp "$PLUGIN_SOURCE/api/dna_query.php" "$PLUGIN_DIR/api/"
cp "$PLUGIN_SOURCE/config.inc.php" "$PLUGIN_DIR/"
cp "$PLUGIN_SOURCE/install.php" "$PLUGIN_DIR/"
cp "$PLUGIN_SOURCE/install.sql" "$PLUGIN_DIR/"

# 创建入口文件
cat > "$PLUGIN_DIR/cnsh.inc.php" << 'EOF'
<?php
/**
 * CNSH-64 插件入口
 */
if(!defined('IN_DISCUZ')) {
    exit('Access Denied');
}

$mod = $_GET['mod'] ?: 'index';
$action = $_GET['action'] ?: 'index';

switch ($mod) {
    case 'bind':
        require_once __DIR__ . '/cnsh_dna/bind.php';
        $controller = new cnsh_bind();
        break;
    case 'governance':
        require_once __DIR__ . '/cnsh_governance/vote.php';
        $controller = new cnsh_governance();
        break;
    case 'ecny':
    case 'wallet':
        require_once __DIR__ . '/cnsh_ecny/tip.php';
        $controller = new cnsh_ecny();
        break;
    case 'api':
        require_once __DIR__ . '/api/dna_query.php';
        $controller = new cnsh_api();
        break;
    default:
        showmessage('未知的模块');
}

if (method_exists($controller, $action)) {
    $controller->$action();
} else {
    showmessage('未知的操作');
}
EOF

# 创建discuz_plugin_cnsh.xml
PLUGIN_VERSION="1.0.0"
cat > "$PLUGIN_DIR/discuz_plugin_cnsh.xml" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<plugin>
    <identifier>cnsh</identifier>
    <name>CNSH-64社区系统</name>
    <description>CNSH-64虚拟身份与现实社区接通系统，包含DNA绑定、70%治理、数字人民币打赏</description>
    <version>$PLUGIN_VERSION</version>
    <copyright>CNSH-64 Project</copyright>
    <installfile>install.php</installfile>
    <modules>
        <module type="plugin">
            <name>CNSH-DNA绑定</name>
            <url>cnsh:bind</url>
        </module>
        <module type="plugin">
            <name>社区治理</name>
            <url>cnsh:governance</url>
        </module>
        <module type="plugin">
            <name>数字钱包</name>
            <url>cnsh:wallet</url>
        </module>
    </modules>
    <hooks>
        <hook name="profile_baseinfo_top">
            <![CDATA[plugin_cnsh_dna::profile_baseinfo_top]]>
        </hook>
        <hook name="viewthread_bottom">
            <![CDATA[plugin_cnsh_ecny::viewthread_bottom]]>
        </hook>
        <hook name="spacecp_baseinfo_top">
            <![CDATA[plugin_cnsh_ecny::spacecp_baseinfo_top]]>
        </hook>
    </hooks>
</plugin>
EOF

echo -e "${CNSH_GREEN}✓ 插件文件安装完成${CNSH_NC}"

# ============================================
# 步骤4: 导入数据库
# ============================================
echo ""
echo -e "${CNSH_BLUE}[4/7] 导入数据库...${CNSH_NC}"

# 获取表前缀
TABLE_PRE=$(grep "\$tablepre" "$DISCUZ_PATH/config/config_global.php" | head -1 | sed "s/.*= *['\"]\([^'\"]*\).*/\1/")
if [ -z "$TABLE_PRE" ]; then
    TABLE_PRE="pre_"
fi

# 处理SQL文件
SQL_FILE="$PLUGIN_DIR/install.sql"
if [ -f "$SQL_FILE" ]; then
    # 替换表前缀
    sed "s/pre_/${TABLE_PRE}/g" "$SQL_FILE" > "$PLUGIN_DIR/install_processed.sql"
    
    # 导入数据库
    if [ -z "$DB_PASS" ]; then
        mysql -u "$DB_USER" "$DB_NAME" < "$PLUGIN_DIR/install_processed.sql" 2>&1 | grep -v "Warning" || true
    else
        mysql -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" < "$PLUGIN_DIR/install_processed.sql" 2>&1 | grep -v "Warning" || true
    fi
    
    rm "$PLUGIN_DIR/install_processed.sql"
    echo -e "${CNSH_GREEN}✓ 数据库导入完成${CNSH_NC}"
else
    echo -e "${CNSH_RED}✗ 找不到SQL文件${CNSH_NC}"
    exit 1
fi

# ============================================
# 步骤5: 生成API密钥
# ============================================
echo ""
echo -e "${CNSH_BLUE}[5/7] 配置API密钥...${CNSH_NC}"

API_KEY=$(openssl rand -hex 32)

# 更新配置文件
sed -i "s/\$_config\['cnsh'\]\['api_key'\] = ''/\$_config['cnsh']['api_key'] = '$API_KEY'/" "$PLUGIN_DIR/config.inc.php"

echo -e "${CNSH_GREEN}✓ API密钥已生成${CNSH_NC}"

# ============================================
# 步骤6: 设置权限
# ============================================
echo ""
echo -e "${CNSH_BLUE}[6/7] 设置文件权限...${CNSH_NC}"

# 检测Web服务器用户
WEB_USER=$(ps aux | grep -E "(nginx|apache|httpd|php-fpm)" | grep -v grep | head -1 | awk '{print $1}')
if [ -z "$WEB_USER" ]; then
    WEB_USER="www-data"
fi

chown -R $WEB_USER:$WEB_USER "$PLUGIN_DIR" 2>/dev/null || true
chmod -R 755 "$PLUGIN_DIR"

echo -e "${CNSH_GREEN}✓ 权限设置完成 (用户: $WEB_USER)${CNSH_NC}"

# ============================================
# 步骤7: 创建模板文件
# ============================================
echo ""
echo -e "${CNSH_BLUE}[7/7] 创建模板文件...${CNSH_NC}"

# DNA绑定页面模板
cat > "$TEMPLATE_DIR/bind.htm" << 'EOF'
<!--{template common/header}-->
<div class="bm cl">
    <div class="bm_h cl">
        <h2>绑定CNSH-DNA身份</h2>
    </div>
    <div class="bm_c">
        <div class="cnsh-bind-intro">
            <h3>什么是DNA绑定?</h3>
            <p>将您的CNSH-DNA身份与社区账号绑定，获得:</p>
            <ul>
                <li>✓ 信誉体系 - 社区行为影响DNA信誉分</li>
                <li>✓ 治理投票权 - 参与社区70%治理决策</li>
                <li>✓ 数字人民币钱包 - 接收打赏和交易</li>
            </ul>
        </div>
        
        <form action="plugin.php?id=cnsh:bind&action=do_bind" method="post">
            <input type="hidden" name="formhash" value="{FORMHASH}">
            
            <div class="cnsh-form-group">
                <label>您的DNA地址:</label>
                <input type="text" name="dna" placeholder="0x..." class="px" style="width:400px">
            </div>
            
            <div class="cnsh-form-group">
                <label>签名证明:</label>
                <textarea name="signature" placeholder="使用DNA私钥签名消息: BIND:{UID}:{TIMESTAMP}" class="pt" style="width:400px;height:80px"></textarea>
            </div>
            
            <div class="cnsh-form-group">
                <label>时间戳:</label>
                <input type="text" name="timestamp" value="{TIMESTAMP}" class="px" readonly>
            </div>
            
            <button type="submit" class="pn pnc">确认绑定</button>
        </form>
        
        <div class="cnsh-bind-help">
            <h4>如何生成签名?</h4>
            <pre>
# 使用CNSH护盾CLI
cnsh-shield sign --dna YOUR_DNA --message "BIND:{UID}:{TIMESTAMP}"
            </pre>
        </div>
    </div>
</div>
<!--{template common/footer}-->
EOF

# 治理页面模板
cat > "$TEMPLATE_DIR/governance.htm" << 'EOF'
<!--{template common/header}-->
<div class="bm cl">
    <div class="bm_h cl">
        <h2>社区治理 (70%规则)</h2>
        <span class="y">
            <a href="plugin.php?id=cnsh:governance&action=create" class="pn pnc">发起提案</a>
        </span>
    </div>
    <div class="bm_c">
        <div class="cnsh-governance-stats">
            <p>我的投票权重: <strong>$my_weight</strong></p>
        </div>
        
        <table class="dt">
            <tr>
                <th>提案</th>
                <th>类型</th>
                <th>状态</th>
                <th>支持率</th>
                <th>截止时间</th>
                <th>操作</th>
            </tr>
            <!--{loop $proposals $proposal}-->
            <tr>
                <td><a href="plugin.php?id=cnsh:governance&action=view&pid=$proposal[id]">$proposal[title]</a></td>
                <td><!--{if $proposal[type]==1}-->社区规则<!--{elseif $proposal[type]==2}-->版主任免<!--{else}-->资金分配<!--{/if}--></td>
                <td><!--{if $proposal[status]==0}-->投票中<!--{elseif $proposal[status]==1}-->已通过<!--{elseif $proposal[status]==2}-->已否决<!--{else}-->已执行<!--{/if}--></td>
                <td>
                    <!--{eval $ratio=$proposal[total_weight]>0?$proposal[support_weight]/$proposal[total_weight]*100:0}-->
                    {echo round($ratio,1)}%
                </td>
                <td>{echo date('Y-m-d H:i', $proposal[end_time])}</td>
                <td><a href="plugin.php?id=cnsh:governance&action=view&pid=$proposal[id]">查看</a></td>
            </tr>
            <!--{/loop}-->
        </table>
        
        $multipage
    </div>
</div>
<!--{template common/footer}-->
EOF

echo -e "${CNSH_GREEN}✓ 模板文件创建完成${CNSH_NC}"

# ============================================
# 完成
# ============================================
echo ""
echo -e "${CNSH_GREEN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║              ✅ 部署完成！                                    ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${CNSH_NC}"

echo ""
echo -e "${CNSH_YELLOW}下一步操作:${CNSH_NC}"
echo ""
echo "1. 登录Discuz!后台 → 应用 → 插件"
echo "   找到 'CNSH-64社区系统' 点击安装"
echo ""
echo "2. 启用插件后，配置以下参数:"
echo "   • CNSH护盾API: http://localhost:16384"
echo "   • 数字人民币API: http://localhost:16385"
echo "   • API密钥: $API_KEY"
echo ""
echo "3. 用户访问以下页面:"
echo "   • DNA绑定: http://your-site/plugin.php?id=cnsh:bind"
echo "   • 社区治理: http://your-site/plugin.php?id=cnsh:governance"
echo "   • 数字钱包: http://your-site/plugin.php?id=cnsh:wallet"
echo ""
echo "4. 确保CNSH护盾正在运行:"
echo "   python3 $CNSH_SHIELD_PATH/cnsh_shield_v05_integrated.py"
echo ""
echo -e "${CNSH_BLUE}══════════════════════════════════════════════════════════════${CNSH_NC}"
echo ""
echo "API密钥已保存至: $PLUGIN_DIR/config.inc.php"
echo "请妥善保管，用于CNSH护盾回调验证"
echo ""
echo -e "${CNSH_GREEN}虚拟世界与现实已接通，系统可以运行了。${CNSH_NC}"
echo ""

# 保存部署信息
cat > "$SCRIPT_DIR/deploy_info.txt" << EOF
CNSH-64 社区部署信息
====================
部署时间: $(date '+%Y-%m-%d %H:%M:%S')
Discuz! 路径: $DISCUZ_PATH
插件路径: $PLUGIN_DIR
数据库: $DB_NAME
API密钥: $API_KEY

访问地址:
- DNA绑定: plugin.php?id=cnsh:bind
- 社区治理: plugin.php?id=cnsh:governance  
- 数字钱包: plugin.php?id=cnsh:wallet
- API接口: plugin.php?id=cnsh:api&action=ping
EOF

echo "部署信息已保存至: $SCRIPT_DIR/deploy_info.txt"
