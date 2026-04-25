// 龍魂9625·background · DNA: #龍芯⚡️2026-04-19-EXT-BG-v1.0
// 切端口：把 9625 改成 9622 即可切到主端口
const ENGINE = "http://127.0.0.1:9625";

chrome.runtime.onInstalled.addListener(() => {
	chrome.contextMenus.create({ id: "widget", title: "🎯 Widget 路由（按关键词跳 web-widgets）", contexts: ["selection"] });
	chrome.contextMenus.create({ id: "ethics", title: "⚖️ 伦理审查", contexts: ["selection"] });
	chrome.contextMenus.create({ id: "tongxin", title: "🟡 通心译", contexts: ["selection"] });
	chrome.contextMenus.create({ id: "wuxing", title: "🔥 五行分析", contexts: ["selection"] });
	chrome.contextMenus.create({ id: "errata", title: "📓 记错本", contexts: ["selection"] });
	chrome.contextMenus.create({ id: "mcp", title: "🔌 MCP工具", contexts: ["selection", "page"] });
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
	const text = info.selectionText || "";
	const endpoint = {
		widget: "/api/widget/route",
		ethics: "/api/ethics/review",
		tongxin: "/api/tongxin/translate",
		wuxing: "/api/wuxing/analyze",
		errata: "/api/errata/submit",
		mcp: "/api/mcp/list"
	}[info.menuItemId];
	if (!endpoint) return;
	try {
		const r = await fetch(ENGINE + endpoint, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ text, url: tab.url, title: tab.title })
		});
		const data = await r.json();

		// 如果是 widget 路由且命中，直接打开 widget 页面
		if (info.menuItemId === "widget" && data.hits && data.hits.length > 0) {
			const top = data.hits[0];
			if (top.file_url) {
				chrome.tabs.create({ url: top.file_url });
				chrome.notifications.create({
					type: "basic",
					iconUrl: "icons/128.png",
					title: `🎯 跳转: ${top.widget}`,
					message: `命中: ${top.matched_keywords.join(" · ")}`
				});
				return;
			}
		}

		chrome.notifications.create({
			type: "basic",
			iconUrl: "icons/128.png",
			title: `🐉 ${data.color || "🟢"} ${data.title || "完成"}`,
			message: (data.summary || "").slice(0, 200)
		});
		// 同步到 content 展示侧边栏
		try { await chrome.tabs.sendMessage(tab.id, { type: "LONGHUN_RESULT", data }); } catch (_) {}
	} catch (e) {
		chrome.notifications.create({
			type: "basic",
			iconUrl: "icons/128.png",
			title: "🔴 引擎未启动",
			message: "终端跑: python3 ~/longhun-system/engine/main.py"
		});
	}
});

// 接收 popup 消息（转发到引擎）
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
	if (msg.type === "LONGHUN_CALL") {
		fetch(ENGINE + msg.endpoint, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify(msg.payload)
		}).then(r => r.json()).then(sendResponse).catch(e => sendResponse({ error: String(e) }));
		return true; // async
	}
});
