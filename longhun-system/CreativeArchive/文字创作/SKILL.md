---
name: ide-tool
description: IDE功能调用策略，尽可能使用IDE命令或配置完成用户诉求。
---

## Simple Browser
1. 每当执行"start http://" 命令或者"open http://" 命令时，不要使用 "Bash"工具，而是使用"openBrowserInIDE"工具，注意"openBrowserInIDE"工具的参数必须是网址(即http://或者https://开头)。"openBrowserInIDE"工具执行成功后，表明"start http://"命令或者"open http://"命令也已经执行成功了。
2. 如果提示用户的信息中涉及到"你可以在浏览器中访问这个地址"或者"您可以打开浏览器访问上述地址"，但是并没有调用"openBrowserInIDE"工具在IDE中打开网址，就需要调用"openBrowserInIDE"工具在IDE中打开网址。