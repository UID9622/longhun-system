// 龍魂9625·popup · DNA: #龍芯⚡️2026-04-19-EXT-POPUP-v1.0
const ENGINE = "http://127.0.0.1:9625";

// 引擎健康检查
fetch(ENGINE + "/api/health")
	.then(r => r.json())
	.then(d => {
		document.getElementById("status").innerHTML =
			`🟢 引擎在线 · ${d.version || "v1.0"}`;
		document.getElementById("status").className = "ok";
	})
	.catch(() => {
		document.getElementById("status").innerHTML =
			`🔴 引擎离线<br><code>python3 ~/longhun-system/engine/main.py</code>`;
		document.getElementById("status").className = "err";
	});

// 按钮快捷操作
document.querySelectorAll("button[data-ep]").forEach(b => {
	b.onclick = async () => {
		const text = document.getElementById("input").value;
		if (!text.trim()) {
			document.getElementById("out").textContent = "(先粘贴要处理的文本)";
			return;
		}
		try {
			const r = await fetch(ENGINE + b.dataset.ep, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ text })
			});
			const d = await r.json();
			document.getElementById("out").textContent = JSON.stringify(d, null, 2);
		} catch (e) {
			document.getElementById("out").textContent = "🔴 引擎未启动: " + e;
		}
	};
});

// 对话窗
const chatWin = document.getElementById("chat-window");
const chatInput = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");

function appendChat(role, content, dna) {
	const div = document.createElement("div");
	div.className = "chat-msg " + role;
	const safe = (s) => String(s || "").replace(/[<>&]/g, c => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;" }[c]));
	div.innerHTML = role === "user"
		? `<b>您:</b> ${safe(content)}`
		: `<b>🐉龍魂:</b> ${safe(content)}<br><small>${safe(dna || "")}</small>`;
	chatWin.appendChild(div);
	chatWin.scrollTop = chatWin.scrollHeight;
}

async function sendMessage() {
	const msg = chatInput.value.trim();
	if (!msg) return;
	const mode = document.getElementById("mode").value;
	appendChat("user", msg);
	chatInput.value = "";
	chatInput.disabled = true;
	sendBtn.disabled = true;
	try {
		const r = await fetch(ENGINE + "/api/chat", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ message: msg, mode })
		});
		const d = await r.json();
		appendChat("bot", d.reply || "(无回复)", d.dna);
	} catch (e) {
		appendChat("bot", "🔴 引擎未启动或超时: " + e);
	} finally {
		chatInput.disabled = false;
		sendBtn.disabled = false;
		chatInput.focus();
	}
}

sendBtn.onclick = sendMessage;
chatInput.onkeydown = (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); } };
