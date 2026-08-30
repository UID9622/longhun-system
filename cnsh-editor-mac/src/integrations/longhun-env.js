/**
 * 🐉 龍魂统一环境接入（~/.longhun/）
 * 读取环境变量 · 挂载互通引擎应用配置
 * DNA: #龍芯⚡️丙午·丙申·辛酉·己丑·䷹兑为泽-CNSH-ENV-UID9622
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 */

(function () {
  const fs = require('fs');
  const path = require('path');
  const LONGHUN_HOME = `${process.env.HOME}/.longhun`;

  class LonghunEnv {
    /** 读取龍魂环境变量 */
    static readEnv() {
      const envFile = path.join(LONGHUN_HOME, 'env.sh');
      const vars = {
        LONGHUN_HOME,
        LONGHUN_UID: '9622',
        LONGHUN_CONFIRM: '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z',
        LONGHUN_GPG: 'A2D0092CEE2E5BA87035600924C3704A8CC26D5F'
      };
      if (fs.existsSync(envFile)) {
        const content = fs.readFileSync(envFile, 'utf-8');
        const re = /^export\s+(\w+)="?([^"\n]+)"?/gm;
        let m;
        while ((m = re.exec(content)) !== null) {
          vars[m[1]] = m[2];
        }
      }
      return vars;
    }

    /** 应用互通配置状态 */
    static appStatus() {
      const appsDir = path.join(LONGHUN_HOME, 'apps');
      if (!fs.existsSync(appsDir)) return { linked: [], available: false };
      return {
        available: true,
        linked: fs.readdirSync(appsDir).filter((n) => !n.startsWith('.'))
      };
    }

    /** 写共享记忆（追加 JSONL） */
    static writeMemory(key, payload) {
      const memDir = path.join(LONGHUN_HOME, 'memory');
      fs.mkdirSync(memDir, { recursive: true });
      const file = path.join(memDir, 'chat_history.jsonl');
      const record = {
        ts: new Date().toISOString(),
        key,
        dna: `#龍芯⚡️EDITOR-${Date.now().toString(36).toUpperCase()}-UID9622`,
        ...payload
      };
      fs.appendFileSync(file, JSON.stringify(record) + '\n', 'utf-8');
      return record;
    }
  }

  if (typeof window !== 'undefined') window.LonghunEnv = LonghunEnv;
  if (typeof module !== 'undefined' && module.exports) module.exports = LonghunEnv;
})();
