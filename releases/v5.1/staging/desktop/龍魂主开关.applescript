-- 龍魂系統桌面主开关（動態生成）
-- 來源：desktop/menu-registry.json + 各模塊 desktop-menu.json
-- DNA: #龍芯⚡️2026-06-18-LONGHUN-MASTER-SWITCH-v1.2

property rootPath : "/Users/zuimeidedeyihan/longhun-system"
property menuItems : {"🎛️ 打开龍魂控制中心（推薦）  🟢常駐", "啟動龍魂操作台（:9622）  🟢常駐", "打開項目終端  🟢常駐", "🖥️ 启动 CNSH 多语言终端 v5.0  🟢常駐", "🎛️ 启动龍魂操作台  🟢常駐", "🗺️ 龍魂生态实时仪表盘  🟢常駐", "📝 打开龍碼中文編輯器  🟢常駐", "停止龍魂操作台  ⚙️配置", "開機自啟動 ▸ 安裝  ⚙️配置", "開機自啟動 ▸ 卸載  ⚙️配置", "🔨 重新編譯龍碼編輯器 App  ⚙️配置", "執行 CNSH 自檢  ▶點一次", "執行每日審計  ▶點一次", "🩺 运行左右互搏自愈审计  ▶點一次", "查看系統狀態  ▶點一次", "🔄 重新生成主开关菜單  ▶點一次", "🗣️ 龍魂语音合成（文字转语音）  ▶點一次", "👁️ 图像文字识别（OCR）  ▶點一次", "🌐 通心译：英→中示例  ▶點一次", "✅ 运行 CNSH 四层检查  ▶點一次", "📋 CNSH 終端審計報告  ▶點一次", "📜 龍魂协议（大白话）  ▶點一次", "🔐 运行六层加密堆栈测试  ▶點一次", "👁️ 运行 L6 灵魂层测试  ▶點一次", "⚖️ 运行权重调谐器  ▶點一次", "🐉 運行底座啟動台自檢  ▶點一次", "📋 運行腳本管理器報告  ▶點一次", "❓ 運行 MVP 啟動器幫助  ▶點一次", "🌌 星辰记忆：添加示例  ▶點一次", "✨ 生成星辰记忆页面  ▶點一次", "📊 星辰记忆统计  ▶點一次", "🐉 龍魂編年史：初始化里程碑  ▶點一次", "📜 生成龍魂編年史頁面  ▶點一次", "📚 查看 cnsh-core 規範索引  ▶點一次", "🛡️ 运行 KFPP 知识纯净度演示  ▶點一次", "💱 查看主權幣種  ▶點一次", "💰 演示支付（CNY → UID1001）  ▶點一次", "📊 XPay 交易統計  ▶點一次", "開啟操作台網頁  👁只看", "📘 查看 CNSH 整合說明文檔  👁只看", "📊 查看三色审计报告  👁只看", "📘 查看星辰记忆说明  👁只看", "📘 查看編年史說明  👁只看", "📘 查看 KFPP 说明  👁只看", "📘 查看 XPay 設計說明  👁只看", "退出"}

repeat
    set choice to choose from list menuItems with title "🐉 龍魂主开关" with prompt "選擇要執行的操作，不用記任何命令：🟢常駐=點一次長期運行；▶點一次=跑完就停；👁只看=只開文件/網頁；⚙️配置=改設定" default items {item 1 of menuItems} OK button name "執行" cancel button name "退出"
    if choice is false then exit repeat
    set selected to item 1 of choice
    if selected is "退出" then exit repeat

    try
        set resultText to runMenu(selected)
        if length of resultText > 900 then
            set resultText to (text 1 thru 900 of resultText) & "\n...（輸出過長，請查看日誌）"
        end if
        display dialog resultText buttons {"確定"} default button "確定" with title "🐉 龍魂主开关"
    on error errMsg
        display dialog "執行出錯：" & errMsg buttons {"確定"} default button "確定" with icon stop
    end try
end repeat

on runMenu(selected)
    set qRoot to quoted form of rootPath
    if selected is "🎛️ 打开龍魂控制中心（推薦）  🟢常駐" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && python3 desktop/龍魂控制中心.py >/dev/null 2>&1 &"
        -- 上面已經 return，以下只是備註：常駐服務點一次即可，不需要反覆點
    else if selected is "啟動龍魂操作台（:9622）  🟢常駐" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && export PYTHONPATH=/Users/zuimeidedeyihan/longhun-system && mkdir -p logs && if ! lsof -ti:9622 >/dev/null 2>&1; then cd control-panel && nohup python3 main.py >> ../logs/control-panel.log 2>&1 & fi && echo '龍魂操作台已啟動或正在運行'"
        -- 上面已經 return，以下只是備註：常駐服務點一次即可，不需要反覆點
    else if selected is "打開項目終端  🟢常駐" then
        do shell script "open -a \"Terminal\" \"/Users/zuimeidedeyihan/longhun-system\""
        return "已打開應用"
        -- 上面已經 return，以下只是備註：常駐服務點一次即可，不需要反覆點
    else if selected is "🖥️ 启动 CNSH 多语言终端 v5.0  🟢常駐" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/cnsh-terminal && python3 cnsh_terminal_v5.py gui >/dev/null 2>&1 &"
        -- 上面已經 return，以下只是備註：常駐服務點一次即可，不需要反覆點
    else if selected is "🎛️ 启动龍魂操作台  🟢常駐" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/control-panel && (python3 main.py >/tmp/longhun-control-panel.log 2>&1 &) && sleep 2 && open http://127.0.0.1:9622/static/index.html"
        -- 上面已經 return，以下只是備註：常駐服務點一次即可，不需要反覆點
    else if selected is "🗺️ 龍魂生态实时仪表盘  🟢常駐" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/control-panel && (python3 main.py >/tmp/longhun-control-panel.log 2>&1 &) && sleep 2 && open http://127.0.0.1:9622/ecosystem-dashboard"
        -- 上面已經 return，以下只是備註：常駐服務點一次即可，不需要反覆點
    else if selected is "📝 打开龍碼中文編輯器  🟢常駐" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && python3 editor/龍碼編輯器.py >/dev/null 2>&1 &"
        -- 上面已經 return，以下只是備註：常駐服務點一次即可，不需要反覆點
    else if selected is "停止龍魂操作台  ⚙️配置" then
        set userChoice to display dialog "關閉後台操作台服務" buttons {"取消", "確定"} default button "確定" with icon caution
        if button returned of userChoice is "取消" then
            return "已取消"
        end if
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && (lsof -ti:9622 | xargs kill -9 2>/dev/null) || true && echo '龍魂操作台已停止'"
    else if selected is "開機自啟動 ▸ 安裝  ⚙️配置" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && bash bin/install-autostart.sh 2>&1"
    else if selected is "開機自啟動 ▸ 卸載  ⚙️配置" then
        set userChoice to display dialog "移除開機自動執行" buttons {"取消", "確定"} default button "確定" with icon caution
        if button returned of userChoice is "取消" then
            return "已取消"
        end if
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && launchctl unload ~/Library/LaunchAgents/com.uid9622.longhun.autostart.plist 2>/dev/null || true && echo '開機自啟動已卸載'"
    else if selected is "🔨 重新編譯龍碼編輯器 App  ⚙️配置" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && bash bin/build-chinese-editor.sh"
    else if selected is "執行 CNSH 自檢  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && export PYTHONPATH=/Users/zuimeidedeyihan/longhun-system && python3 CNSH/task_executor_v9_integrated.py 2>&1 | tail -n 12"
    else if selected is "執行每日審計  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && bash bin/longhun-daily-audit.sh 2>&1 | tail -n 18"
    else if selected is "🩺 运行左右互搏自愈审计  ▶點一次" then
        set userChoice to display dialog "自己找漏洞、自己修復：目錄、權限、菜單、服務、重複模塊" buttons {"取消", "確定"} default button "確定" with icon caution
        if button returned of userChoice is "取消" then
            return "已取消"
        end if
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && python3 bin/longhun-self-heal.py --repair"
    else if selected is "查看系統狀態  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && bash bin/longhun-status.sh 2>&1"
    else if selected is "🔄 重新生成主开关菜單  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && bash bin/build-desktop-switch.sh 2>&1 && echo '主开关已更新，請關閉本窗口後重新打開龍魂主开关.app'"
    else if selected is "🗣️ 龍魂语音合成（文字转语音）  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/cnsh-terminal && python3 multimodal_cli.py speak \"你好，龍魂系統已就位\" --offline"
    else if selected is "👁️ 图像文字识别（OCR）  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/cnsh-terminal && python3 multimodal_cli.py ocr /Users/zuimeidedeyihan/longhun-system/cnsh-terminal/multimodal_demo.png"
    else if selected is "🌐 通心译：英→中示例  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/cnsh-terminal && python3 cnsh_terminal_v5.py translate \"Prompt Engineering makes the Agent smarter\""
    else if selected is "✅ 运行 CNSH 四层检查  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/cnsh-terminal && python3 cnsh_terminal_v5.py check test.cnsh"
    else if selected is "📋 CNSH 終端審計報告  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/cnsh-terminal && python3 cnsh_terminal_v5.py audit"
    else if selected is "📜 龍魂协议（大白话）  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/cnsh-terminal && python3 cnsh_terminal_v5.py 协议"
    else if selected is "🔐 运行六层加密堆栈测试  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/crypto-stack/src && python3 stack_runner.py"
    else if selected is "👁️ 运行 L6 灵魂层测试  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/crypto-stack/src && python3 l6_soul.py"
    else if selected is "⚖️ 运行权重调谐器  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/crypto-stack/src && python3 weight_tuner.py"
    else if selected is "🐉 運行底座啟動台自檢  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && python3 executors/kimi-agent-v2/longhun_foundation_launcher_v2.0.py --auto 2>&1 | tail -n 40"
    else if selected is "📋 運行腳本管理器報告  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && python3 executors/kimi-agent-v2/longhun_script_manager_v2.0.py report 2>&1 | tail -n 30"
    else if selected is "❓ 運行 MVP 啟動器幫助  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && python3 executors/kimi-agent-v2/longhun_mvp_launcher_v2.0.py --help"
    else if selected is "🌌 星辰记忆：添加示例  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/memory-universe && python3 星辰记忆系统.py seed"
    else if selected is "✨ 生成星辰记忆页面  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/memory-universe && python3 星辰记忆系统.py generate && open /Users/zuimeidedeyihan/longhun-system/memory-universe/index.md"
    else if selected is "📊 星辰记忆统计  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/memory-universe && python3 星辰记忆系统.py stats"
    else if selected is "🐉 龍魂編年史：初始化里程碑  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/project-memory && python3 龍魂編年史.py seed"
    else if selected is "📜 生成龍魂編年史頁面  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/project-memory && python3 龍魂編年史.py generate && open /Users/zuimeidedeyihan/longhun-system/project-memory/index.md"
    else if selected is "📚 查看 cnsh-core 規範索引  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system/project-memory && python3 龍魂編年史.py specs"
    else if selected is "🛡️ 运行 KFPP 知识纯净度演示  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && python3 systems/kfpp/kfpp_executor_v1.0.py"
    else if selected is "💱 查看主權幣種  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && python3 xpay/src/cli.py currencies"
    else if selected is "💰 演示支付（CNY → UID1001）  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && python3 xpay/src/cli.py pay 100.00 CNY UID1001 --memo \"桌面主开关演示\""
    else if selected is "📊 XPay 交易統計  ▶點一次" then
        return do shell script "cd /Users/zuimeidedeyihan/longhun-system && python3 xpay/src/cli.py stats"
    else if selected is "開啟操作台網頁  👁只看" then
        do shell script "open \"http://127.0.0.1:9622\""
        return "已打開 http://127.0.0.1:9622"
    else if selected is "📘 查看 CNSH 整合說明文檔  👁只看" then
        return do shell script "open /Users/zuimeidedeyihan/longhun-system/cnsh.integrated/info.md"
    else if selected is "📊 查看三色审计报告  👁只看" then
        return do shell script "open /Users/zuimeidedeyihan/longhun-system/crypto-stack/audit_three_color.md"
    else if selected is "📘 查看星辰记忆说明  👁只看" then
        return do shell script "open /Users/zuimeidedeyihan/longhun-system/memory-universe/README.md"
    else if selected is "📘 查看編年史說明  👁只看" then
        return do shell script "open /Users/zuimeidedeyihan/longhun-system/project-memory/README.md"
    else if selected is "📘 查看 KFPP 说明  👁只看" then
        return do shell script "open /Users/zuimeidedeyihan/longhun-system/systems/kfpp/README.md"
    else if selected is "📘 查看 XPay 設計說明  👁只看" then
        return do shell script "open /Users/zuimeidedeyihan/longhun-system/xpay/README.md"
    end if
end runMenu
