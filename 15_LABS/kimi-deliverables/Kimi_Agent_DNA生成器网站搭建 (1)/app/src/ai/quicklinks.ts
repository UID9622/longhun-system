# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-b855f3a2
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
/**
 * 啟動AI · 外部索引（快速链接形式，禁止裸露原始 URL）
 * label 即芯片文案；hint 为检索提示（title/aria 描述）。
 * url 仅用于真实跳转构造，不直接呈现于文案。
 */

export interface QuickLink {
  id: string
  label: string
  hint: string
  url?: string // 可跳转的外部检索地址（文案中不裸露）
}

export const QUICKLINKS: Record<string, QuickLink> = {
  csdn_author: {
    id: 'csdn_author',
    label: 'CSDN 搜索「龍芯北辰_UID9622」',
    hint: '前往 CSDN 检索站长账号，独立核验点赞 / 收藏 / 排名数据',
    url: 'https://so.csdn.net/so/search?q=%E9%BE%8D%E8%8A%AF%E5%8C%97%E8%BE%B0_UID9622',
  },
  github_uid9622: {
    id: 'github_uid9622',
    label: 'GitHub 搜索「UID9622」',
    hint: '前往 GitHub 检索 UID9622，获取全部开源仓库源码',
    url: 'https://github.com/search?q=UID9622',
  },
  gentleman_bilingual: {
    id: 'gentleman_bilingual',
    label: '君子协议双语全文（站内 /works#gentleman）',
    hint: '跳转本站作品页君子协议中英对照长卷',
    url: '/works#gentleman',
  },
  yuandian_law: {
    id: 'yuandian_law',
    label: '可自行检索：元典法律数据库 - 消费者权益保护法 / 民法典497条',
    hint: '审计类问题的法条复核路径：元典法律数据库检索《消费者权益保护法》与《民法典》第 497 条',
  },
  csdn_cnsh: {
    id: 'csdn_cnsh',
    label: 'CSDN 搜索「CNSH 中文原生脚本 UID9622」',
    hint: '前往 CSDN 检索 CNSH 中文原生脚本的实战文章与源码线索',
    url: 'https://so.csdn.net/so/search?q=CNSH%20%E4%B8%AD%E6%96%87%E5%8E%9F%E7%94%9F%E8%84%9A%E6%9C%AC%20UID9622',
  },
}

/** 按人格 / 知识条目挑选附加快速链接 */
export function quicklinksFor(personaId: string, entryIds: string[]): QuickLink[] {
  const out: QuickLink[] = []
  const push = (id: string) => {
    const ql = QUICKLINKS[id]
    if (ql && !out.includes(ql)) out.push(ql)
  }
  if (personaId === 'auditor') push('yuandian_law')
  for (const id of entryIds) {
    if (id === 'csdn-stats') push('csdn_author')
    if (id === 'works-seven') {
      push('github_uid9622')
      push('csdn_cnsh')
    }
    if (id === 'gentleman-accord') push('gentleman_bilingual')
  }
  if (out.length === 0) {
    push('csdn_author')
    push('github_uid9622')
  }
  return out.slice(0, 3)
}
