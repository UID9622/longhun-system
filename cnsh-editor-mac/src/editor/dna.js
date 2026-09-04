/**
 * 🐉 龍魂DNA追溯码生成器
 * 格式: #龍芯⚡️{干支}-{模块}-{哈希8}-UID9622
 * DNA: #龍芯⚡️丙午·丙申·辛酉·己丑·䷹兑为泽-CNSH-DNA-UID9622
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 */

(function () {
  const crypto = require('crypto');

  const TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
  const DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
  const UID = '9622';
  const CONFIRM = '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z';

  function getGanZhi(date) {
    const year = date.getFullYear();
    const gan = TIAN_GAN[(year - 4) % 10];
    const zhi = DI_ZHI[(year - 4) % 12];
    return `${gan}${zhi}`;
  }

  function getShiZhi(date) {
    const hour = date.getHours();
    const idx = Math.floor((hour + 1) / 2) % 12;
    return DI_ZHI[idx];
  }

  function getHexagram(date) {
    // 梅花易数简式起卦（日数÷8取余定上下卦）
    const day = date.getDate();
    const month = date.getMonth() + 1;
    const upper = day % 8 || 8;
    const lower = (day + month) % 8 || 8;
    return `卦${upper}${lower}`;
  }

  class DNAGenerator {
    static generate(content, module = 'EDITOR') {
      const now = new Date();
      const ganzhi = getGanZhi(now) + getShiZhi(now);
      const hash = crypto.createHash('sha256')
        .update(content + Date.now().toString())
        .digest('hex')
        .substring(0, 8)
        .toUpperCase();
      return `#龍芯⚡️${ganzhi}-${module}-${hash}-${UID}`;
    }

    static getConfirm() {
      return CONFIRM;
    }

    static getGPG() {
      return 'A2D0092CEE2E5BA87035600924C3704A8CC26D5F';
    }

    static getStamp() {
      const now = new Date();
      const ganzhi = getGanZhi(now) + getShiZhi(now);
      return `🐉${ganzhi}·${getHexagram(now)}·🟢`;
    }
  }

  if (typeof window !== 'undefined') {
    window.DNAGenerator = DNAGenerator;
  }
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = DNAGenerator;
  }
})();
