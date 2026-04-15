# CNSH 构建系统
# DNA追溯码：#龍芯⚡️2026-03-22-CNSH-MAKEFILE-v1.0
# 创建者：诸葛鑫（UID9622）

PYTHON  := python3
CLI     := $(shell pwd)/cli/cnsh
EXAMPLES := examples

.PHONY: help install test build-examples clean run-hello

## 默认目标：显示帮助
help:
	@echo ""
	@echo "🇨🇳 CNSH 构建系统 v1.0"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "  make install        安装 cnsh 命令（加入 PATH）"
	@echo "  make test           运行测试套件"
	@echo "  make build-examples 编译所有示例程序"
	@echo "  make run-hello      运行 hello.cnsh 示例"
	@echo "  make clean          清理编译产物"
	@echo ""

## 安装 cnsh 到 /usr/local/bin
install:
	@echo "安装 cnsh 命令..."
	@chmod +x $(CLI)
	@ln -sf $(CLI) /usr/local/bin/cnsh || \
		(echo "需要 sudo，尝试：sudo ln -sf $(CLI) /usr/local/bin/cnsh" && exit 1)
	@echo "✅ 安装完成！现在可以直接运行：cnsh run <file.cnsh>"

## 运行测试套件
test:
	@echo "运行测试套件..."
	@$(PYTHON) tests/test_compiler.py

## 编译所有示例
build-examples:
	@echo "编译示例程序..."
	@$(PYTHON) $(CLI) build $(EXAMPLES)/

## 运行 hello.cnsh
run-hello:
	@$(PYTHON) $(CLI) run $(EXAMPLES)/hello.cnsh

## 清理编译产物（.c 和可执行文件）
clean:
	@echo "清理编译产物..."
	@find . -name "*.c" ! -path "./.git/*" -delete
	@find $(EXAMPLES) -type f ! -name "*.cnsh" ! -name "*.md" -delete 2>/dev/null || true
	@echo "✅ 清理完成"
