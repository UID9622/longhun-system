/**
 * 🐉 鲲鹏服务器同步（119.13.90.27）
 * SSH key 优先 · 密码备用 · 只同步编辑器工作文件
 * DNA: #龍芯⚡️丙午·丙申·辛酉·己丑·䷹兑为泽-CNSH-KUNPENG-UID9622
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 */

(function () {
  const { exec } = require('child_process');
  const KUNPENG = 'root@119.13.90.27';
  const REMOTE_DIR = '/opt/longhun/shared/editor/';
  const SSH_KEY = `${process.env.HOME}/.ssh/longhun_kunpeng_ed25519`;

  class KunpengSync {
    /**
     * 推送文件到鲲鹏
     * @param {string} localPath
     * @param {string} remoteName
     */
    static push(localPath, remoteName) {
      return new Promise((resolve) => {
        const keyArg = require('fs').existsSync(SSH_KEY) ? `-i ${SSH_KEY}` : '';
        exec(`scp ${keyArg} ${JSON.stringify(localPath)} ${KUNPENG}:${REMOTE_DIR}${remoteName} 2>&1`,
          (err, stdout, stderr) => {
            if (err) resolve({ success: false, error: stderr || err.message });
            else resolve({ success: true, message: `已推送 ${remoteName} → 鲲鹏 ${REMOTE_DIR}` });
          });
      });
    }

    /** 拉取文件 */
    static pull(remoteName, localPath) {
      return new Promise((resolve) => {
        const keyArg = require('fs').existsSync(SSH_KEY) ? `-i ${SSH_KEY}` : '';
        exec(`scp ${keyArg} ${KUNPENG}:${REMOTE_DIR}${remoteName} ${JSON.stringify(localPath)} 2>&1`,
          (err, stdout, stderr) => {
            if (err) resolve({ success: false, error: stderr || err.message });
            else resolve({ success: true, message: `已拉取 ${remoteName}` });
          });
      });
    }
  }

  if (typeof window !== 'undefined') window.KunpengSync = KunpengSync;
  if (typeof module !== 'undefined' && module.exports) module.exports = KunpengSync;
})();
