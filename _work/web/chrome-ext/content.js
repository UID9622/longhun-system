// 龍魂9625·content · 悬浮侧边栏展示结果
chrome.runtime.onMessage.addListener((msg) => {
	if (msg.type !== "LONGHUN_RESULT") return;
	let box = document.getElementById("longhun-9625-box");
	if (!box) {
		box = document.createElement("div");
		box.id = "longhun-9625-box";
		box.style.cssText = `
			position:fixed;top:20px;right:20px;width:380px;max-height:70vh;
			overflow:auto;background:#fff;border:2px solid #D4AF37;border-radius:12px;
			padding:16px;z-index:999999;font-family:system-ui,-apple-system,sans-serif;
			box-shadow:0 8px 24px rgba(0,0,0,.2);font-size:14px;line-height:1.6;color:#222;
		`;
		document.body.appendChild(box);
	}
	const d = msg.data || {};
	const safe = (s) => String(s || "").replace(/[<>&]/g, c => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;" }[c]));
	box.innerHTML = `
		<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
			<strong>🐉 龍魂9625 · ${safe(d.color || "🟢")}</strong>
			<span style="cursor:pointer;color:#999;font-size:18px" id="longhun-close">✕</span>
		</div>
		<div style="font-weight:600;margin-bottom:4px">${safe(d.title || "结果")}</div>
		<pre style="white-space:pre-wrap;background:#f7f7f7;padding:8px;border-radius:6px;font-size:12px;max-height:300px;overflow:auto">${safe(d.summary || "")}</pre>
		<div style="color:#888;font-size:11px;margin-top:6px">DNA: ${safe(d.dna || "")}</div>
		${d.notion_url ? `<div style="margin-top:6px"><a href="${safe(d.notion_url)}" target="_blank" style="color:#D4AF37">📓 已入Notion →</a></div>` : ""}
	`;
	document.getElementById("longhun-close").onclick = () => box.remove();
});
