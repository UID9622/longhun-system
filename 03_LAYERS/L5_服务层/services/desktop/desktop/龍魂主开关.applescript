-- 龍魂系统桌面主开关（动态生成）
-- 来源：desktop/menu-registry.json + 各模块 desktop-menu.json
-- DNA:#龍芯⚡️2026-06-18-LONGHUN-MASTER-SWITCH-FILE1-v1.2

property rootPath : "/Users/zuimeidedeyihan/longhun-system"
property menuItems : {"🎛️ 打开龍魂控制中心（推荐）  🟢常驻", "启动龍魂操作台（:9622）  🟢常驻", "打开项目终端  🟢常驻", "🖥️ 启动 CNSH 多语言终端 v5.0  🟢常驻", "🎛️ 启动龍魂操作台  🟢常驻", "🗺️ 龍魂生态实时仪表盘  🟢常驻", "📝 打开龍码中文编辑器  🟢常驻", "停止龍魂操作台  ⚙️配置", "开机自启动 ▸ 安装  ⚙️配置", "开机自启动 ▸ 卸载  ⚙️配置", "🔨 重新编译龍码编辑器 App  ⚙️配置", "执行 CNSH 自检  ▶点一次", "执行每日审计  ▶点一次", "🩺 运行左右互搏自愈审计  ▶点一次", "查看系统状态  ▶点一次", "🔄 重新生成主开关菜单  ▶点一次", "🗣️ 龍魂语音合成（文字转语音）  ▶点一次", "👁️ 图像文字识别（OCR）  ▶点一次", "🌐 通心译：英→中示例  ▶点一次", "✅ 运行 CNSH 四层检查  ▶点一次", "📋 CNSH 终端审计报告  ▶点一次", "📜 龍魂协议（大白话）  ▶点一次", "🔐 运行六层加密堆栈测试  ▶点一次", "👁️ 运行 L6 灵魂层测试  ▶点一次", "⚖️ 运行权重调谐器  ▶点一次", "🐉 运行底座启动台自检  ▶点一次", "📋 运行脚本管理器报告  ▶点一次", "❓ 运行 MVP 启动器帮助  ▶点一次", "🌌 星辰记忆：添加示例  ▶点一次", "✨ 生成星辰记忆页面  ▶点一次", "📊 星辰记忆统计  ▶点一次", "🐉 龍魂编年史：初始化里程碑  ▶点一次", "📜 生成龍魂编年史页面  ▶点一次", "📚 查看 cnsh-core 规范索引  ▶点一次", "🛡️ 运行 KFPP 知识纯净度演示  ▶点一次", "💱 查看主权币种  ▶点一次", "💰 演示支付（CNY → UID1001）  ▶点一次", "📊 XPay 交易统计  ▶点一次", "开启操作台网页  👁只看", "📘 查看 CNSH 整合说明文档  👁只看", "📊 查看三色审计报告  👁只看", "📘 查看星辰记忆说明  👁只看", "📘 查看编年史说明  👁只看", "📘 查看 KFPP 说明  👁只看", "📘 查看 XPay 设计说明  👁只看", "退出"}

repeat
    set choice to choose from list menuItems with title "🐉 龍魂主开关" with prompt "选择要执行的操作，不用记任何命令：🟢常驻=点一次长期运行；▶点一次=跑完就停；👁只看=只开文件/网页；⚙️配置=改设定" default items {item 1 of menuItems} OK button name "执行" cancel button name "退出"
    if choice is false then exit repeat
    set selected to item 1 of choice
    if selected is "退出" then exit repeat

    try
        set resultText to runMenu(selected)
        if length of resultText > 900 then
            set resultText to (text 1 thru 900 of resultText) & "\n...（输出过长，请查看日志）"
        end if
        display dialog resultText buttons {"确定"} default button "确定" with title "🐉 龍魂主开关"
    on error errMsg
        display dialog "执行出错：" & errMsg buttons {"确定"} default button "确定" with icon stop
    end try
end repeat

on runMenu(selected)
    set qRoot to quoted form of rootPath
    if selected is "🎛️ 打开龍魂控制中心（推荐）  🟢常驻" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && python3 desktop/龍魂控制中心.py >/dev/null 2>&1 &"
        -- 上面已经 return，以下只是备注：常驻服务点一次即可，不需要反复点
    else if selected is "启动龍魂操作台（:9622）  🟢常驻" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && export PYTHONPATH=/Users/zuimeidedeyihan/longhun-system && mkdir -p logs && if ! lsof -ti:9622 >/dev/null 2>&1; then cd control-panel && nohup python3 main.py >> ../logs/control-panel.log 2>&1 & fi && echo '龍魂操作台已启动或正在运行'"
        -- 上面已经 return，以下只是备注：常驻服务点一次即可，不需要反复点
    else if selected is "打开项目终端  🟢常驻" then
        do shell script "open -a \"Terminal\" \"/Users/zuimeidedeyihan/longhun-system\""
        return "已打开应用"
        -- 上面已经 return，以下只是备注：常驻服务点一次即可，不需要反复点
    else if selected is "🖥️ 启动 CNSH 多语言终端 v5.0  🟢常驻" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/cnsh-terminal && python3 cnsh_terminal_v5.py gui >/dev/null 2>&1 &"
        -- 上面已经 return，以下只是备注：常驻服务点一次即可，不需要反复点
    else if selected is "🎛️ 启动龍魂操作台  🟢常驻" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/control-panel && (python3 main.py >/tmp/longhun-control-panel.log 2>&1 &) && sleep 2 && open http://127.0.0.1:9622/static/index.html"
        -- 上面已经 return，以下只是备注：常驻服务点一次即可，不需要反复点
    else if selected is "🗺️ 龍魂生态实时仪表盘  🟢常驻" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/control-panel && (python3 main.py >/tmp/longhun-control-panel.log 2>&1 &) && sleep 2 && open http://127.0.0.1:9622/ecosystem-dashboard"
        -- 上面已经 return，以下只是备注：常驻服务点一次即可，不需要反复点
    else if selected is "📝 打开龍码中文编辑器  🟢常驻" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && python3 editor/龍码编辑器.py >/dev/null 2>&1 &"
        -- 上面已经 return，以下只是备注：常驻服务点一次即可，不需要反复点
    else if selected is "停止龍魂操作台  ⚙️配置" then
        set userChoice to display dialog "关闭后台操作台服务" buttons {"取消", "确定"} default button "确定" with icon caution
        if button returned of userChoice is "取消" then
            return "已取消"
        end if
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && (lsof -ti:9622 | xargs kill -9 2>/dev/null) || true && echo '龍魂操作台已停止'"
    else if selected is "开机自启动 ▸ 安装  ⚙️配置" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && bash bin/install-autostart.sh 2>&1"
    else if selected is "开机自启动 ▸ 卸载  ⚙️配置" then
        set userChoice to display dialog "移除开机自动执行" buttons {"取消", "确定"} default button "确定" with icon caution
        if button returned of userChoice is "取消" then
            return "已取消"
        end if
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && launchctl unload ~/Library/LaunchAgents/com.uid9622.longhun.autostart.plist 2>/dev/null || true && echo '开机自启动已卸载'"
    else if selected is "🔨 重新编译龍码编辑器 App  ⚙️配置" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && bash bin/build-chinese-editor.sh"
    else if selected is "执行 CNSH 自检  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && export PYTHONPATH=/Users/zuimeidedeyihan/longhun-system && python3 CNSH/task_executor_v9_integrated.py 2>&1 | tail -n 12"
    else if selected is "执行每日审计  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && bash bin/longhun-daily-audit.sh 2>&1 | tail -n 18"
    else if selected is "🩺 运行左右互搏自愈审计  ▶点一次" then
        set userChoice to display dialog "自己找漏洞、自己修复：目录、权限、菜单、服务、重复模块" buttons {"取消", "确定"} default button "确定" with icon caution
        if button returned of userChoice is "取消" then
            return "已取消"
        end if
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && python3 bin/longhun-self-heal.py --repair"
    else if selected is "查看系统状态  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && bash bin/longhun-status.sh 2>&1"
    else if selected is "🔄 重新生成主开关菜单  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && bash bin/build-desktop-switch.sh 2>&1 && echo '主开关已更新，请关闭本窗口后重新打开龍魂主开关.app'"
    else if selected is "🗣️ 龍魂语音合成（文字转语音）  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/cnsh-terminal && python3 multimodal_cli.py speak \"你好，龍魂系统已就位\" --offline"
    else if selected is "👁️ 图像文字识别（OCR）  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/cnsh-terminal && python3 multimodal_cli.py ocr /Users/zuimeidedeyihan/longhun-system/cnsh-terminal/multimodal_demo.png"
    else if selected is "🌐 通心译：英→中示例  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/cnsh-terminal && python3 cnsh_terminal_v5.py translate \"Prompt Engineering makes the Agent smarter\""
    else if selected is "✅ 运行 CNSH 四层检查  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/cnsh-terminal && python3 cnsh_terminal_v5.py check test.cnsh"
    else if selected is "📋 CNSH 终端审计报告  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/cnsh-terminal && python3 cnsh_terminal_v5.py audit"
    else if selected is "📜 龍魂协议（大白话）  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/cnsh-terminal && python3 cnsh_terminal_v5.py 协议"
    else if selected is "🔐 运行六层加密堆栈测试  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/crypto-stack/src && python3 stack_runner.py"
    else if selected is "👁️ 运行 L6 灵魂层测试  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/crypto-stack/src && python3 l6_soul.py"
    else if selected is "⚖️ 运行权重调谐器  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/crypto-stack/src && python3 weight_tuner.py"
    else if selected is "🐉 运行底座启动台自检  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && python3 executors/kimi-agent-v2/longhun_foundation_launcher_v2.0.py --auto 2>&1 | tail -n 40"
    else if selected is "📋 运行脚本管理器报告  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && python3 executors/kimi-agent-v2/longhun_script_manager_v2.0.py report 2>&1 | tail -n 30"
    else if selected is "❓ 运行 MVP 启动器帮助  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && python3 executors/kimi-agent-v2/longhun_mvp_launcher_v2.0.py --help"
    else if selected is "🌌 星辰记忆：添加示例  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/memory-universe && python3 星辰记忆系统.py seed"
    else if selected is "✨ 生成星辰记忆页面  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/memory-universe && python3 星辰记忆系统.py generate && open /Users/zuimeidedeyihan/longhun-system/memory-universe/index.md"
    else if selected is "📊 星辰记忆统计  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/memory-universe && python3 星辰记忆系统.py stats"
    else if selected is "🐉 龍魂编年史：初始化里程碑  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/project-memory && python3 龍魂编年史.py seed"
    else if selected is "📜 生成龍魂编年史页面  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/project-memory && python3 龍魂编年史.py generate && open /Users/zuimeidedeyihan/longhun-system/project-memory/index.md"
    else if selected is "📚 查看 cnsh-core 规范索引  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/project-memory && python3 龍魂编年史.py specs"
    else if selected is "🛡️ 运行 KFPP 知识纯净度演示  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && python3 systems/kfpp/kfpp_executor_v1.0.py"
    else if selected is "💱 查看主权币种  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && python3 xpay/src/cli.py currencies"
    else if selected is "💰 演示支付（CNY → UID1001）  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && python3 xpay/src/cli.py pay 100.00 CNY UID1001 --memo \"桌面主开关演示\""
    else if selected is "📊 XPay 交易统计  ▶点一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && python3 xpay/src/cli.py stats"
    else if selected is "开启操作台网页  👁只看" then
        do shell script "open \"http://127.0.0.1:9622\""
        return "已打开 http://127.0.0.1:9622"
    else if selected is "📘 查看 CNSH 整合说明文档  👁只看" then
        return do shell script "open /Users/zuimeidedeyihan/longhun-system/cnsh.integrated/info.md"
    else if selected is "📊 查看三色审计报告  👁只看" then
        return do shell script "open /Users/zuimeidedeyihan/longhun-system/crypto-stack/audit_three_color.md"
    else if selected is "📘 查看星辰记忆说明  👁只看" then
        return do shell script "open /Users/zuimeidedeyihan/longhun-system/memory-universe/README.md"
    else if selected is "📘 查看编年史说明  👁只看" then
        return do shell script "open /Users/zuimeidedeyihan/longhun-system/project-memory/README.md"
    else if selected is "📘 查看 KFPP 说明  👁只看" then
        return do shell script "open /Users/zuimeidedeyihan/longhun-system/systems/kfpp/README.md"
    else if selected is "📘 查看 XPay 设计说明  👁只看" then
        return do shell script "open /Users/zuimeidedeyihan/longhun-system/xpay/README.md"
    end if
end runMenu
