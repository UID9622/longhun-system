# 龍魂·uid9622.cn 三入口门户 Makefile
# DNA: #龍芯⚡️丙午·甲申·丁未·离为火-Makefile-v1.0

.PHONY: help local start stop sync deploy status

SERVER_IP ?= 119.13.90.27
SSH_KEY ?= $(HOME)/.ssh/longhun_kunpeng_ed25519

help:
	@echo "🐉 龍魂·三入口门户命令"
	@echo ""
	@echo "  make local    本地启动 (localhost:8899)"
	@echo "  make start    同 local"
	@echo "  make stop     停止本地服务"
	@echo "  make sync     同步到服务器"
	@echo "  make deploy   服务器一键部署 (Nginx + SSL)"
	@echo "  make status   查看状态"
	@echo ""

local start:
	@bash scripts/deploy-local.sh

stop:
	@bash -c '[[ -f /tmp/longhun-portal.pid ]] && kill $$(cat /tmp/longhun-portal.pid) 2>/dev/null || true; echo "已停止"'

sync:
	@SERVER_IP=$(SERVER_IP) bash scripts/sync-to-server.sh

deploy:
	@scp -i $(SSH_KEY) -r portal/ scripts/ nginx/ configs/ root@$(SERVER_IP):/root/longhun-portal-deploy/
	@ssh -i $(SSH_KEY) root@$(SERVER_IP) "cd /root/longhun-portal-deploy && bash scripts/deploy-server.sh"

status:
	@echo "🐉 龍魂门户状态"
	@if [[ -f /tmp/longhun-portal.pid ]] && kill -0 $$(cat /tmp/longhun-portal.pid) 2>/dev/null; then \
		echo "  本地: 运行中 (PID: $$(cat /tmp/longhun-portal.pid))"; \
	else \
		echo "  本地: 未运行"; \
	fi
	@echo "  地址: http://localhost:8899"
	@echo "  普通者: http://localhost:8899/index.html"
	@echo "  无障碍: http://localhost:8899/accessible.html"
	@echo "  开发者: http://localhost:8899/developer.html"
