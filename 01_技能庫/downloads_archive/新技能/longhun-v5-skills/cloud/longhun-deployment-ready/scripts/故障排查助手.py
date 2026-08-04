#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂故障排查助手 (Longhun Troubleshooting Assistant)
=====================================
DNA: #龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2

常见问题诊断与解决方案，支持交互式和命令行两种模式。

用法:
    python3 故障排查助手.py [问题关键词]
    python3 故障排查助手.py --interactive
    python3 故障排查助手.py --list
"""

import sys
import json
import argparse
from datetime import datetime
from typing import Dict, List, Optional

SKILL_DNA = "#龍芯⚡️2026-06-19-LONGHUN-DEPLOY-READY-v5.2"


class Colors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    BOLD = '\033[1m'


# ============================================================
# 故障知识库
# ============================================================

TROUBLESHOOTING_KB = {
    "port_occupied": {
        "id": "E001",
        "category": "端口占用",
        "symptoms": ["Address already in use", "端口被占用", "bind() failed", "EADDRINUSE"],
        "diagnosis": [
            "运行: lsof -i :<port> 或 netstat -tlnp | grep <port>",
            "运行: ss -tlnp | grep <port>",
        ],
        "solutions": [
            "方案1: 终止占用进程 - kill -9 $(lsof -t -i :PORT)",
            "方案2: 更换应用端口 - 修改配置文件中的port参数",
            "方案3: 等待进程释放 - 占用进程可能正在关闭",
            "方案4: 使用SO_REUSEADDR选项 - 允许重用TIME_WAIT状态的端口",
        ],
        "prevention": "部署前运行 部署就绪检查器.py 检查端口占用",
        "severity": "高",
    },
    "database_connection": {
        "id": "E002",
        "category": "数据库连接",
        "symptoms": ["Connection refused", "数据库连不上", "OperationalError", "timeout", "cant connect"],
        "diagnosis": [
            "检查1: 数据库服务是否运行 - systemctl status postgresql/mysql",
            "检查2: 连接字符串是否正确 - echo $DATABASE_URL",
            "检查3: 网络连通性 - telnet DB_HOST DB_PORT",
            "检查4: 防火墙设置 - sudo iptables -L | grep DB_PORT",
        ],
        "solutions": [
            "方案1: 启动数据库服务 - sudo systemctl start postgresql",
            "方案2: 创建数据库和用户 - sudo -u postgres createdb app_db",
            "方案3: 修正连接字符串 - 检查用户名、密码、主机、端口",
            "方案4: 开放防火墙端口 - sudo ufw allow 5432/tcp",
            "方案5: 增加连接超时 - 在连接参数中添加 connect_timeout=10",
        ],
        "prevention": "部署前验证数据库连接配置，确保数据库服务已启动",
        "severity": "高",
    },
    "dependency_missing": {
        "id": "E003",
        "category": "依赖缺失",
        "symptoms": ["ModuleNotFoundError", "No module named", "ImportError", "package not found"],
        "diagnosis": [
            "检查1: pip list | grep 包名",
            "检查2: python3 -c 'import 包名'",
            "检查3: 确认requirements.txt中包含该依赖",
            "检查4: 检查虚拟环境是否激活 - which python3",
        ],
        "solutions": [
            "方案1: 安装缺失包 - pip install 包名",
            "方案2: 全部重装 - pip install -r requirements.txt --force-reinstall",
            "方案3: 使用虚拟环境 - python3 -m venv venv && source venv/bin/activate",
            "方案4: 指定版本 - pip install 包名==版本号",
            "方案5: 使用国内镜像 - pip install -i https://pypi.tuna.tsinghua.edu.cn/simple 包名",
        ],
        "prevention": "部署前运行 环境验证器.py 检查依赖完整性",
        "severity": "中",
    },
    "permission_denied": {
        "id": "E004",
        "category": "权限不足",
        "symptoms": ["Permission denied", "EACCES", "不允许的操作", "access denied"],
        "diagnosis": [
            "检查1: 当前用户 - whoami",
            "检查2: 文件权限 - ls -la 文件路径",
            "检查3: 目录权限 - ls -ld 目录路径",
            "检查4: SELinux状态 - getenforce (CentOS/RHEL)",
        ],
        "solutions": [
            "方案1: 修改文件权限 - chmod 644 文件 / chmod 755 目录",
            "方案2: 修改所有者 - sudo chown -R $USER:$USER 目录",
            "方案3: 使用sudo执行 - sudo 原命令",
            "方案4: 临时关闭SELinux - sudo setenforce 0 (仅调试)",
            "方案5: 添加用户到组 - sudo usermod -aG docker $USER",
        ],
        "prevention": "使用配置验证器检查文件权限，遵循最小权限原则",
        "severity": "中",
    },
    "config_error": {
        "id": "E005",
        "category": "配置错误",
        "symptoms": ["KeyError", "配置项缺失", "Config not found", "Invalid configuration"],
        "diagnosis": [
            "检查1: 配置文件存在 - ls config.yaml .env",
            "检查2: 环境变量设置 - env | grep APP_",
            "检查3: 配置格式 - python3 -c 'import yaml; yaml.safe_load(open(\"config.yaml\"))'",
            "检查4: 必要参数 - 对比 config/ 下的示例配置",
        ],
        "solutions": [
            "方案1: 复制示例配置 - cp config.example.yaml config.yaml",
            "方案2: 设置环境变量 - export APP_ENV=production",
            "方案3: 修正YAML格式 - 使用在线YAML校验工具",
            "方案4: 恢复默认配置 - git checkout config.yaml",
        ],
        "prevention": "使用配置验证器检查配置完整性",
        "severity": "高",
    },
    "health_check_fail": {
        "id": "E006",
        "category": "健康检查失败",
        "symptoms": ["/health 500", "健康检查不通过", "服务未响应", "Connection refused"],
        "diagnosis": [
            "检查1: 服务状态 - systemctl status 服务名 / ps aux | grep 进程",
            "检查2: 端口监听 - netstat -tlnp | grep PORT",
            "检查3: 应用日志 - tail -n 50 logs/app.log",
            "检查4: 资源使用 - free -h / df -h",
        ],
        "solutions": [
            "方案1: 重启服务 - systemctl restart 服务名",
            "方案2: 查看错误日志 - journalctl -u 服务名 -n 100",
            "方案3: 增加资源 - 扩容内存/CPU",
            "方案4: 检查依赖服务 - 确保DB/Redis正常",
            "方案5: 回滚版本 - git checkout 上一个稳定版本",
        ],
        "prevention": "部署前运行健康检查脚本，确保所有依赖就绪",
        "severity": "高",
    },
    "migration_fail": {
        "id": "E007",
        "category": "数据库迁移失败",
        "symptoms": ["migration failed", "alembic error", "schema mismatch", "column not found"],
        "diagnosis": [
            "检查1: 当前版本 - alembic current",
            "检查2: 迁移历史 - alembic history",
            "检查3: 数据库连接 - 确认DATABASE_URL正确",
            "检查4: 迁移脚本 - alembic check",
        ],
        "solutions": [
            "方案1: 降级后重试 - alembic downgrade -1 && alembic upgrade head",
            "方案2: 跳过问题迁移 - alembic stamp 目标版本号",
            "方案3: 手动修复 - 直接执行SQL修复schema",
            "方案4: 重建数据库 - 备份后dropdb && createdb (仅开发环境)",
        ],
        "prevention": "迁移前备份数据库，先在 staging 环境测试迁移",
        "severity": "高",
    },
    "ssl_certificate": {
        "id": "E008",
        "category": "SSL证书",
        "symptoms": ["certificate verify failed", "SSL error", "expired", "cert invalid"],
        "diagnosis": [
            "检查1: 证书有效期 - openssl x509 -in cert.pem -noout -dates",
            "检查2: 证书链完整 - openssl s_client -connect host:port",
            "检查3: 系统CA证书 - update-ca-certificates",
        ],
        "solutions": [
            "方案1: 更新证书 - certbot renew",
            "方案2: 使用Let's Encrypt - certbot --nginx",
            "方案3: 临时忽略(不推荐) - 设置verify=False",
            "方案4: 使用自签名证书(内网) - openssl req -x509 -nodes",
        ],
        "prevention": "设置证书过期监控告警，自动续期",
        "severity": "中",
    },
    "memory_leak": {
        "id": "E009",
        "category": "内存泄漏",
        "symptoms": ["OOM", "内存持续增长", "Killed process", "MemoryError"],
        "diagnosis": [
            "检查1: 内存趋势 - free -h (多次执行观察)",
            "检查2: 进程内存 - ps aux --sort=-%mem | head",
            "检查3: Python对象 - 使用tracemalloc/guppy分析",
            "检查4: 系统日志 - dmesg | grep -i 'out of memory'",
        ],
        "solutions": [
            "方案1: 重启服务 - systemctl restart 服务",
            "方案2: 增加swap - sudo fallocate -l 2G /swapfile",
            "方案3: 限制内存 - systemd MemoryLimit=1G",
            "方案4: 代码优化 - 检查未关闭的连接、大对象引用",
            "方案5: 水平扩容 - 增加服务实例分担负载",
        ],
        "prevention": "配置内存监控告警，定期review代码",
        "severity": "中",
    },
    "disk_full": {
        "id": "E010",
        "category": "磁盘满",
        "symptoms": ["No space left", "磁盘满了", "Write error", "无法写入"],
        "diagnosis": [
            "检查1: 磁盘使用 - df -h",
            "检查2: 大文件定位 - du -sh /* | sort -rh | head -20",
            "检查3: 日志大小 - du -sh logs/ /var/log/",
            "检查4: Docker占用 - docker system df",
        ],
        "solutions": [
            "方案1: 清理日志 - find logs/ -name '*.log' -mtime +7 -delete",
            "方案2: 清理Docker - docker system prune -a",
            "方案3: 清理包缓存 - pip cache purge / apt clean",
            "方案4: 扩容磁盘 - 云服务器扩容数据盘",
            "方案5: 日志轮转 - 配置logrotate",
        ],
        "prevention": "配置磁盘使用监控告警，启用日志轮转",
        "severity": "高",
    },
    "service_not_start": {
        "id": "E011",
        "category": "服务启动失败",
        "symptoms": ["Failed to start", "exit code", "服务起不来", "crashed"],
        "diagnosis": [
            "检查1: 启动脚本权限 - ls -la start.sh",
            "检查2: 依赖是否完整 - pip list",
            "检查3: 配置文件正确性 - python3 -c 'import config'",
            "检查4: 端口冲突 - netstat -tlnp",
            "检查5: 查看详细错误 - 直接运行启动命令(非后台)",
        ],
        "solutions": [
            "方案1: 给执行权限 - chmod +x start.sh",
            "方案2: 安装依赖 - pip install -r requirements.txt",
            "方案3: 检查Python路径 - which python3 && python3 --version",
            "方案4: 使用虚拟环境 - source venv/bin/activate",
            "方案5: 查看系统日志 - journalctl -xe | grep 服务名",
        ],
        "prevention": "使用部署执行器按步骤执行，确保前置步骤成功",
        "severity": "高",
    },
    "git_clone_fail": {
        "id": "E012",
        "category": "代码拉取失败",
        "symptoms": ["git clone failed", "repository not found", "Permission denied", "SSL certificate"],
        "diagnosis": [
            "检查1: 仓库URL - git remote -v",
            "检查2: 网络连通 - curl -I 仓库URL",
            "检查3: SSH密钥 - ls -la ~/.ssh/ && cat ~/.ssh/id_rsa.pub",
            "检查4: 权限配置 - git config --list",
        ],
        "solutions": [
            "方案1: 使用HTTPS代替SSH - git clone https://...",
            "方案2: 配置SSH密钥 - ssh-keygen -t ed25519",
            "方案3: 添加免密配置 - git config credential.helper store",
            "方案4: 检查仓库权限 - 确认账号有仓库访问权限",
            "方案5: 跳过SSL验证(不推荐) - git config http.sslVerify false",
        ],
        "prevention": "提前配置好SSH密钥，验证仓库访问权限",
        "severity": "中",
    },
}


class TroubleshootingAssistant:
    """故障排查助手"""

    def __init__(self):
        self.kb = TROUBLESHOOTING_KB

    def search(self, keyword: str) -> List[Dict]:
        """根据关键词搜索故障"""
        results = []
        keyword_lower = keyword.lower()
        for key, issue in self.kb.items():
            # 匹配ID
            if keyword_lower == issue["id"].lower():
                results.append({"key": key, **issue})
                continue
            # 匹配类别
            if keyword_lower in issue["category"].lower():
                results.append({"key": key, **issue})
                continue
            # 匹配症状
            for symptom in issue["symptoms"]:
                if keyword_lower in symptom.lower():
                    results.append({"key": key, **issue})
                    break
        return results

    def show_issue(self, issue: Dict):
        """展示单个故障详情"""
        severity_color = {
            "高": Colors.FAIL,
            "中": Colors.WARNING,
            "低": Colors.OKGREEN,
        }.get(issue.get("severity", "中"), Colors.OKBLUE)

        print(f"\n{Colors.BOLD}{'='*60}{Colors.ENDC}")
        print(f"  {Colors.BOLD}[{issue['id']}] {issue['category']}{Colors.ENDC}")
        print(f"  严重度: {severity_color}{issue.get('severity', '中')}{Colors.ENDC}")
        print(f"{'='*60}")

        print(f"\n{Colors.OKCYAN}【症状】{Colors.ENDC}")
        for s in issue["symptoms"]:
            print(f"  - {s}")

        print(f"\n{Colors.OKBLUE}【诊断步骤】{Colors.ENDC}")
        for i, d in enumerate(issue["diagnosis"], 1):
            print(f"  {i}. {d}")

        print(f"\n{Colors.OKGREEN}【解决方案】{Colors.ENDC}")
        for s in issue["solutions"]:
            print(f"  {s}")

        print(f"\n{Colors.WARNING}【预防措施】{Colors.ENDC}")
        print(f"  {issue.get('prevention', '无')}")

    def list_all_issues(self):
        """列出所有故障"""
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║        龍魂故障排查知识库                                      ║
╠══════════════════════════════════════════════════════════════╣
║  {SKILL_DNA}    ║
╚══════════════════════════════════════════════════════════════╝
""")
        print(f"共 {len(self.kb)} 类常见故障:\n")
        for key, issue in self.kb.items():
            sev_color = {"高": Colors.FAIL, "中": Colors.WARNING, "低": Colors.OKGREEN}.get(issue["severity"], "")
            print(f"  {Colors.BOLD}[{issue['id']}]{Colors.ENDC} {issue['category']:<15} "
                  f"{sev_color}[{issue['severity']}]{Colors.ENDC} {issue['symptoms'][0][:30]}")

    def interactive_mode(self):
        """交互模式"""
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║        龍魂故障排查助手 - 交互模式                             ║
╠══════════════════════════════════════════════════════════════╣
║  输入问题关键词、错误信息或故障ID进行查询                      ║
║  输入 'list' 查看所有故障, 'quit' 退出                        ║
╚══════════════════════════════════════════════════════════════╝
""")
        while True:
            try:
                query = input(f"\n{Colors.OKBLUE}[排查]{Colors.ENDC} 请输入问题描述 > ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n退出")
                break

            if not query:
                continue
            if query.lower() in ('quit', 'exit', 'q'):
                print("退出故障排查助手")
                break
            if query.lower() == 'list':
                self.list_all_issues()
                continue

            results = self.search(query)
            if not results:
                print(f"{Colors.WARNING}未找到匹配 '{query}' 的故障记录{Colors.ENDC}")
                print("建议: 尝试使用更通用的关键词，或运行 'list' 查看所有故障")
                continue

            if len(results) == 1:
                self.show_issue(results[0])
            else:
                print(f"\n找到 {len(results)} 个相关故障:")
                for i, r in enumerate(results, 1):
                    print(f"  {i}. [{r['id']}] {r['category']} - {r['symptoms'][0]}")
                try:
                    choice = input(f"\n查看第几个 (1-{len(results)})? ").strip()
                    idx = int(choice) - 1
                    if 0 <= idx < len(results):
                        self.show_issue(results[idx])
                except (ValueError, IndexError):
                    pass

    def diagnose(self, error_message: str) -> Optional[Dict]:
        """根据错误信息诊断故障"""
        results = self.search(error_message)
        return results[0] if results else None


def main():
    parser = argparse.ArgumentParser(description="龍魂故障排查助手")
    parser.add_argument("keyword", nargs="?", help="问题关键词或错误信息")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有故障")
    parser.add_argument("--id", help="按故障ID查询")
    args = parser.parse_args()

    assistant = TroubleshootingAssistant()

    if args.list:
        assistant.list_all_issues()
    elif args.id:
        results = assistant.search(args.id)
        if results:
            assistant.show_issue(results[0])
        else:
            print(f"未找到ID: {args.id}")
    elif args.interactive or not args.keyword:
        assistant.interactive_mode()
    else:
        results = assistant.search(args.keyword)
        if not results:
            print(f"未找到匹配 '{args.keyword}' 的故障")
            print("尝试使用 --list 查看所有故障")
            sys.exit(1)
        for r in results:
            assistant.show_issue(r)


if __name__ == "__main__":
    main()
