// DNA: #龍芯⚡️丙午·丙申·庚申·亥时-HARMONYOS-CHAT-DEMO-v1.2-UID9622
// CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
// 龍魂 · 鸿蒙端跨设备对话示例 v1.2
// 功能：从 Mac 拉取记忆摘要 → 调用 Mac 桥接对话 → 保存新记忆

import http from '@ohos.net.http';
import fs from '@ohos.file.fs';
import promptAction from '@ohos.promptAction';

const TAG = 'LonghunChatDemo';

// ===== 配置区（按实际环境修改）=====
const MAC_IP = '192.168.31.100';          // Mac 局域网 IP
const SYNC_PORT = 19622;                  // 同步服务端口
const CHAT_PORT = 18799;                  // 对话桥接端口
const MEMORY_FILE = 'longhun_memory.json'; // 鸿蒙本地记忆文件名

// ===== 工具函数 =====

/**
 * 读取鸿蒙本地记忆摘要
 */
async function loadLocalMemory(): Promise<string> {
  try {
    const ctx = getContext();
    const dir = ctx.filesDir;
    const path = dir + '/' + MEMORY_FILE;
    if (!fs.access(path)) {
      return '';
    }
    const file = fs.openSync(path, fs.OpenMode.READ_ONLY);
    const buf = new ArrayBuffer(1024 * 64);
    const len = fs.readSync(file.fd, buf);
    fs.closeSync(file);
    return String.fromCharCode.apply(null, new Uint8Array(buf, 0, len));
  } catch (err) {
    console.warn(TAG, '读取本地记忆失败: ' + JSON.stringify(err));
    return '';
  }
}

/**
 * 保存记忆摘要到鸿蒙本地
 */
async function saveLocalMemory(content: string): Promise<void> {
  try {
    const ctx = getContext();
    const dir = ctx.filesDir;
    const path = dir + '/' + MEMORY_FILE;
    const file = fs.openSync(path, fs.OpenMode.CREATE | fs.OpenMode.TRUNC | fs.OpenMode.WRITE_ONLY);
    const encoder = new util.TextEncoder();
    fs.writeSync(file.fd, encoder.encodeInto(content));
    fs.closeSync(file);
  } catch (err) {
    console.error(TAG, '保存本地记忆失败: ' + JSON.stringify(err));
  }
}

/**
 * 调用 Mac 桥接进行对话
 * @param prompt 用户问题
 * @param context 记忆上下文（可选）
 */
export async function chatWithMac(prompt: string, context: string = ''): Promise<string> {
  return new Promise((resolve, reject) => {
    const httpRequest = http.createHttp();
    const systemPrompt = context
      ? `你是龍魂助手。以下是从 Mac 同步来的记忆摘要，请据此保持对话连续性：\n${context}\n\n现在请回答用户问题。`
      : '你是龍魂助手。';

    const payload = JSON.stringify({
      prompt: prompt,
      system: systemPrompt,
      stream: false,
    });

    httpRequest.request(
      `http://${MAC_IP}:${CHAT_PORT}/api/v1/chat`,
      {
        method: http.RequestMethod.POST,
        header: { 'Content-Type': 'application/json' },
        extraData: payload,
        connectTimeout: 15000,
        readTimeout: 120000,
      },
      (err, data) => {
        if (err) {
          console.error(TAG, '对话请求失败: ' + JSON.stringify(err));
          reject(err);
          return;
        }
        try {
          const resp = JSON.parse(data.result.toString());
          if (resp.success) {
            resolve(resp.response);
          } else {
            reject(new Error(resp.error || '未知错误'));
          }
        } catch (e) {
          reject(e);
        } finally {
          httpRequest.destroy();
        }
      }
    );
  });
}

/**
 * 从 Mac 同步记忆摘要
 * 注意：本示例为简化版，实际应使用 longhun-cross-platform 的 SM4+ECDH 加密通道。
 *       在集成 xsync 之前，可先用 HTTP 兜底：在 Mac 上由 xsync serve 暴露健康检查，
 *       真正的记忆文件建议通过 xsync sync-memory 命令拉取。
 */
export async function syncMemoryFromMac(): Promise<string> {
  // 推荐做法：通过 Shell 调用 Python xsync_workflow.py sync-memory
  // 这里给出 HTTP 兜底示例，用于快速验证对话连续性。
  return new Promise((resolve, reject) => {
    const httpRequest = http.createHttp();
    httpRequest.request(
      `http://${MAC_IP}:${SYNC_PORT + 1}/health`,  // xsync serve 的健康检查端口
      {
        method: http.RequestMethod.GET,
        connectTimeout: 10000,
        readTimeout: 10000,
      },
      async (err, data) => {
        if (err) {
          console.error(TAG, '健康检查失败: ' + JSON.stringify(err));
          reject(err);
          return;
        }
        try {
          const health = JSON.parse(data.result.toString());
          console.info(TAG, 'Mac 同步服务健康: ' + JSON.stringify(health));
          // 实际记忆拉取应通过 Shell 调用 xsync sync-memory
          // 本 demo 仅保存一个标记，表示已连接成功
          await saveLocalMemory(JSON.stringify({
            last_sync: new Date().toISOString(),
            mac_ip: MAC_IP,
            status: 'connected',
          }));
          resolve('已连接 Mac 同步服务');
        } catch (e) {
          reject(e);
        } finally {
          httpRequest.destroy();
        }
      }
    );
  });
}

/**
 * 完整对话流程：先同步记忆，再对话
 */
export async function chatWithContext(prompt: string): Promise<string> {
  try {
    await syncMemoryFromMac();
  } catch (e) {
    console.warn(TAG, '记忆同步失败，使用本地记忆: ' + JSON.stringify(e));
  }
  const memory = await loadLocalMemory();
  const answer = await chatWithMac(prompt, memory);
  // 把新对话追加到本地记忆
  const newMemory = {
    last_dialog: { q: prompt, a: answer, t: new Date().toISOString() },
  };
  await saveLocalMemory(JSON.stringify(newMemory));
  return answer;
}

// ===== 示例 UI 调用（ArkTS UIAbility 中）=====
// @Entry
// @Component
// struct ChatPage {
//   @State message: string = '';
//   @State reply: string = '';
//
//   build() {
//     Column() {
//       TextInput({ placeholder: '问龍魂...' })
//         .onChange((v) => this.message = v)
//       Button('发送')
//         .onClick(async () => {
//           this.reply = await chatWithContext(this.message);
//         })
//       Text(this.reply)
//     }
//   }
// }
