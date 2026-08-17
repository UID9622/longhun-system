# 🐉 龍魂 · DeepSeek Harness 鲲鹏部署 Makefile
# DNA: #龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-DSH-KUNPENG-MAKEFILE-UID9622

.PHONY: help deploy status tunnel stop logs setup-mac validate

KUNPENG_IP ?= $(shell cat ~/.longhun/configs/kunpeng-ip.txt 2>/dev/null || echo "")
DEPLOY_DIR ?= /opt/deepseek-harness-kunpeng
# 鲲鹏专用密钥（P0: SSH 密钥-only，禁止密码登录）
KEY ?= $(HOME)/.ssh/longhun_kunpeng_ed25519
SSH_OPTS = -i $(KEY) -o StrictHostKeyChecking=accept-new

help:
	@echo "🐉 龍魂 · DeepSeek Harness 鲲鹏部署"
	@echo ""
	@echo "  make deploy KUNPENG_IP=xxx    上传到鲲鹏并一键部署"
	@echo "  make status                   查看鲲鹏上容器状态"
	@echo "  make tunnel                   建立本地 SSH 隧道"
	@echo "  make stop                     停止鲲鹏容器"
	@echo "  make logs                     查看 dsh 日志"
	@echo "  make setup-mac IP=xxx         初始化 Mac 本地 lh-dsh 命令"
	@echo "  make validate                 本地校验 Docker Compose 语法"

validate:
	docker compose -f docker-compose.kunpeng.yml config > /dev/null && echo "✅ compose 语法通过"

deploy:
	@if [ -z "$(KUNPENG_IP)" ]; then echo "❌ 请设置 KUNPENG_IP"; exit 1; fi
	@if [ ! -f "$(KEY)" ]; then echo "❌ SSH 密钥不存在: $(KEY)"; exit 1; fi
	ssh $(SSH_OPTS) root@$(KUNPENG_IP) "mkdir -p $(DEPLOY_DIR)"
	scp -i $(KEY) -r . root@$(KUNPENG_IP):$(DEPLOY_DIR)
	ssh $(SSH_OPTS) root@$(KUNPENG_IP) "cd $(DEPLOY_DIR) && chmod +x scripts/*.sh && ./scripts/deploy-kunpeng.sh"

status:
	@if [ -z "$(KUNPENG_IP)" ]; then echo "❌ 请设置 KUNPENG_IP"; exit 1; fi
	ssh $(SSH_OPTS) root@$(KUNPENG_IP) "cd $(DEPLOY_DIR) && docker compose ps"

stop:
	@if [ -z "$(KUNPENG_IP)" ]; then echo "❌ 请设置 KUNPENG_IP"; exit 1; fi
	ssh $(SSH_OPTS) root@$(KUNPENG_IP) "cd $(DEPLOY_DIR) && docker compose down"

logs:
	@if [ -z "$(KUNPENG_IP)" ]; then echo "❌ 请设置 KUNPENG_IP"; exit 1; fi
	ssh $(SSH_OPTS) root@$(KUNPENG_IP) "cd $(DEPLOY_DIR) && docker compose logs -f dsh"

tunnel:
	@if [ -z "$(KUNPENG_IP)" ]; then echo "❌ 请设置 KUNPENG_IP"; exit 1; fi
	ssh $(SSH_OPTS) -N -L 127.0.0.1:2283:127.0.0.1:2283 -L 127.0.0.1:2284:127.0.0.1:2284 -L 127.0.0.1:11434:127.0.0.1:11434 root@$(KUNPENG_IP)

setup-mac:
	@if [ -z "$(IP)" ]; then echo "❌ 请设置 IP=xxx"; exit 1; fi
	./scripts/local-mac-setup.sh $(IP)
