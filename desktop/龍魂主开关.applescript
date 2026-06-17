-- 龍魂系統桌面主开关
-- 點擊後彈出選單，無需記任何命令
-- DNA: #龍芯⚡️2026-06-17-LONGHUN-MASTER-SWITCH-v1.0

property rootPath : "/Users/zuimeidedeyihan/longhun-system"
property logDir : rootPath & "/logs"

set menuItems to {"啟動龍魂操作台（:9622）", "停止龍魂操作台", "開啟操作台網頁", "執行 CNSH 自檢", "執行每日審計", "開機自啟動 ▸ 安裝", "開機自啟動 ▸ 卸載", "查看系統狀態", "打開項目終端", "退出"}

repeat
	set choice to choose from list menuItems with title "🐉 龍魂主开关" with prompt "選擇要執行的操作，不用記任何命令：" default items {"啟動龍魂操作台（:9622）"} OK button name "執行" cancel button name "退出"
	if choice is false then exit repeat
	set selected to item 1 of choice
	if selected is "退出" then exit repeat

	try
		set msg to runMenu(selected)
		display dialog msg buttons {"確定"} default button "確定" with title "🐉 龍魂主开关"
	on error errMsg
		display dialog "執行出錯：" & errMsg buttons {"確定"} default button "確定" with icon stop
	end try
end repeat

on runMenu(selected)
	set qRoot to quoted form of rootPath
	if selected is "啟動龍魂操作台（:9622）" then
		return doShell("cd " & qRoot & " && export PYTHONPATH=" & qRoot & " && mkdir -p logs && if ! lsof -ti:9622 >/dev/null 2>&1; then cd control-panel && nohup python3 main.py >> ../logs/control-panel.log 2>&1 & fi && echo '龍魂操作台已啟動或正在運行'")

	else if selected is "停止龍魂操作台" then
		return doShell("cd " & qRoot & " && (lsof -ti:9622 | xargs kill -9 2>/dev/null) || true && echo '龍魂操作台已停止'")

	else if selected is "開啟操作台網頁" then
		do shell script "open http://127.0.0.1:9622"
		return "已在瀏覽器打開 http://127.0.0.1:9622"

	else if selected is "執行 CNSH 自檢" then
		return doShell("cd " & qRoot & " && export PYTHONPATH=" & qRoot & " && python3 CNSH/task_executor_v9_integrated.py 2>&1 | tail -n 12")

	else if selected is "執行每日審計" then
		return doShell("cd " & qRoot & " && bash bin/longhun-daily-audit.sh 2>&1 | tail -n 18")

	else if selected is "開機自啟動 ▸ 安裝" then
		return doShell("cd " & qRoot & " && bash bin/install-autostart.sh 2>&1")

	else if selected is "開機自啟動 ▸ 卸載" then
		return doShell("cd " & qRoot & " && launchctl unload ~/Library/LaunchAgents/com.uid9622.longhun.autostart.plist 2>/dev/null || true && echo '開機自啟動已卸載'")

	else if selected is "查看系統狀態" then
		return doShell("cd " & qRoot & " && bash bin/longhun-status.sh 2>&1")

	else if selected is "打開項目終端" then
		do shell script "open -a Terminal " & qRoot
		return "已打開終端並進入項目目錄"

	else
		return "未知選項"
	end if
end runMenu

on doShell(cmd)
	return do shell script cmd
end doShell
