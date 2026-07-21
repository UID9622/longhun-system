// entry/src/main/ets/engines/HeTuLuoShuEngine.ets
// 龍魂 · 河图洛书引擎
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

export class HeTuLuoShuEngine {
  private heTuMatrix: number[][] = [
    [7, 2, 6],
    [8, 5, 4],
    [3, 10, 9]
  ];

  private luoShuMatrix: number[][] = [
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6]
  ];

  private heTuMnemonic: string[] = [
    '天一生水，地六成之',
    '地二生火，天七成之',
    '天三生木，地八成之',
    '地四生金，天九成之',
    '天五生土，地十成之'
  ];

  private luoShuMnemonic: string[] = [
    '戴九履一',
    '左三右七',
    '二四为肩',
    '六八为足',
    '五居中央'
  ];

  getHeTu(): { matrix: number[][], mnemonic: string[], description: string } {
    return {
      matrix: this.heTuMatrix,
      mnemonic: this.heTuMnemonic,
      description: '河图，相传伏羲氏时，有龙马从黄河出现，背负"河图"。河图以十数合五方、五行、阴阳、天地之象。图式以白圈为阳，为天，为奇数；黑点为阴，为地，为偶数。'
    };
  }

  getLuoShu(): { matrix: number[][], mnemonic: string[], description: string, magicSum: number } {
    return {
      matrix: this.luoShuMatrix,
      mnemonic: this.luoShuMnemonic,
      description: '洛书，相传大禹时，有神龟从洛水出现，背负"洛书"。洛书以九数合九宫、八卦、五行之象。其特点是纵、横、斜三条线上的三个数字之和皆等于15。',
      magicSum: 15
    };
  }

  validateLuoShu(): boolean {
    const m = this.luoShuMatrix;
    const sum = 15;
    for (let i = 0; i < 3; i++) {
      if (m[i][0] + m[i][1] + m[i][2] !== sum) return false;
    }
    for (let j = 0; j < 3; j++) {
      if (m[0][j] + m[1][j] + m[2][j] !== sum) return false;
    }
    if (m[0][0] + m[1][1] + m[2][2] !== sum) return false;
    if (m[0][2] + m[1][1] + m[2][0] !== sum) return false;
    return true;
  }

  getWuXingByNumber(num: number): string {
    const map: Map<number, string> = new Map([
      [1, '水'], [6, '水'],
      [2, '火'], [7, '火'],
      [3, '木'], [8, '木'],
      [4, '金'], [9, '金'],
      [5, '土'], [10, '土']
    ]);
    return map.get(num) || '未知';
  }

  getDirectionByNumber(num: number): string {
    const map: Map<number, string> = new Map([
      [1, '北'], [6, '北'],
      [2, '南'], [7, '南'],
      [3, '东'], [8, '东'],
      [4, '西'], [9, '西'],
      [5, '中'], [10, '中']
    ]);
    return map.get(num) || '未知';
  }
}

export const heTuLuoShuEngine = new HeTuLuoShuEngine();
