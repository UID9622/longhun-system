import PageHero from '@/components/PageHero'
import SectionHeading from '@/components/SectionHeading'
import SealTag from '@/components/SealTag'
import { Code2, Terminal, Cpu, Globe, ArrowUpRight, CheckCircle2 } from 'lucide-react'

/**
 * 龍魂·API & 开发者 `/api` — 对外接口 · SDK 集成 · 开发者资源
 */
export default function ApiDocs() {
  return (
    <>
      <PageHero
        eyebrow="DEVELOPERS"
        title="API & 开发者"
        subtitle="开放接口 · SDK 双语言 · 开源 MulanPSL v2 · 商业友好 · 一键集成"
        seal="卷拾 / API"
      />

      {/* 接入方式 */}
      <section className="px-6 py-24 md:px-12">
        <div className="mx-auto max-w-container">
          <SectionHeading
            eyebrow="INTEGRATION"
            title="接入方式"
            subtitle="三种方式，从轻到重，按需选择"
          />
          <div className="mt-16 grid gap-8 md:grid-cols-3">
            {[
              {
                icon: <Terminal className="h-7 w-7 text-gold" />,
                title: 'CLI 命令行',
                desc: '一键安装，自然语言交互，无需编程背景',
                install: 'pip install longhun-system',
                items: ['lh search / lh audit / lh status', 'lh bos / lh --align / lh te', 'python3 bin/lh_*.py 直接调用'],
              },
              {
                icon: <Code2 className="h-7 w-7 text-gold" />,
                title: 'Python SDK',
                desc: 'pip 安装，三行代码集成，18/18 自测全绿',
                install: 'pip install longhun-tricolor',
                items: [
                  'from longhun.tricolor import evaluate',
                  'from longhun_memory import seal, unseal',
                  'from lh_time_engine import get_output_stamp',
                ],
              },
              {
                icon: <Globe className="h-7 w-7 text-gold" />,
                title: 'REST API',
                desc: '标准 HTTP 接口，跨语言调用，零依赖',
                install: 'GET https://uid9622.cn/api/',
                items: [
                  '健康检查: /api/health',
                  '三色审计: /api/tricolor/evaluate',
                  'DNA生成: /api/dna/generate',
                  '搜索: /api/search?q=...',
                ],
              },
            ].map((c, i) => (
              <div
                key={i}
                className="hairline group flex flex-col bg-ink-2 p-8 transition-colors duration-300 hover:bg-ink-3"
              >
                <span className="flex h-12 w-12 items-center justify-center rounded-none border border-line bg-ink">
                  {c.icon}
                </span>
                <h3 className="mt-5 font-serif text-[18px] font-bold text-paper">{c.title}</h3>
                <p className="mt-2 text-[14px] leading-[1.8] text-paper-dim">{c.desc}</p>
                <code className="mt-4 block truncate border-t border-line pt-4 font-mono text-[13px] text-gold">
                  {c.install}
                </code>
                <ul className="mt-4 flex flex-col gap-2">
                  {c.items.map((it, j) => (
                    <li key={j} className="flex items-start gap-2 text-[13px] text-paper-faint">
                      <CheckCircle2 className="mt-0.5 h-3.5 w-3.5 shrink-0 text-gold-dim" />
                      <code className="font-mono text-[12px]">{it}</code>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* SDK 列表 */}
      <section className="hairline-t px-6 py-24 md:px-12">
        <div className="mx-auto max-w-container">
          <SectionHeading
            eyebrow="SDK ECOSYSTEM"
            title="已发布 SDK"
            subtitle="MulanPSL v2 开源许可 · 商业友好 · 可自由集成到付费产品"
          />
          <div className="mt-16 grid gap-6 md:grid-cols-2">
            {[
              {
                name: 'longhun-tricolor',
                ver: 'v1.1',
                lang: 'Python + JavaScript',
                desc: '三色审计引擎 · OpenAPI 3.1 契约 · 双语言实现 · 一致性自测 100%',
                links: { pypi: '#', npm: '#', doc: '#' },
              },
              {
                name: 'longhun-system',
                ver: 'v2.0',
                lang: 'Python',
                desc: '系统核心包 · lh 统一命令入口 · 192 引擎 · 45 技能 · 9 层架构',
                links: { pypi: '#', github: '#', doc: '#' },
              },
              {
                name: 'longhun-memory',
                ver: 'v2.0',
                lang: 'Python + Rust',
                desc: '加密记忆系统 · SM4/SM3 国密 · Rust FFI 50x 加速 · CNSH 文本格式',
                links: { pypi: '#', doc: '#' },
              },
              {
                name: 'longhun-save',
                ver: 'v2.0',
                lang: 'Python',
                desc: 'DNA 代理审计 · 审计日志 append-only · 主权签章 · 反篡改冻结',
                links: { pypi: '#', doc: '#' },
              },
              {
                name: 'lh-time-engine',
                ver: 'v4.0',
                lang: 'Python',
                desc: '干支四柱 · 64 卦梅花易数 · 时间戳输出 · 独立可复用',
                links: { pypi: '#', doc: '#' },
              },
              {
                name: 'lh-baidu-bos',
                ver: 'v1.0',
                lang: 'Python',
                desc: '百度云 BOS 存储网关 · 增量同步 · 备份恢复 · 优雅降级本地模拟',
                links: { pypi: '#', doc: '#' },
              },
            ].map((sdk, i) => (
              <div key={i} className="hairline flex flex-col gap-4 bg-ink-2 p-6 transition-colors hover:bg-ink-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Cpu className="h-5 w-5 text-gold" />
                    <h3 className="font-mono text-[15px] font-bold text-paper">{sdk.name}</h3>
                  </div>
                  <SealTag>{sdk.ver}</SealTag>
                </div>
                <p className="text-[13px] leading-[1.8] text-paper-dim">{sdk.desc}</p>
                <div className="flex items-center gap-3 border-t border-line pt-4 text-[12px]">
                  <span className="text-paper-faint">{sdk.lang}</span>
                  <span className="text-line">|</span>
                  {sdk.links.pypi ? (
                    <a href={sdk.links.pypi} className="text-gold-dim hover:text-gold transition-colors">
                      PyPI <ArrowUpRight className="inline h-3 w-3" />
                    </a>
                  ) : null}
                  {sdk.links.npm ? (
                    <a href={sdk.links.npm} className="text-gold-dim hover:text-gold transition-colors">
                      npm <ArrowUpRight className="inline h-3 w-3" />
                    </a>
                  ) : null}
                  {sdk.links.github ? (
                    <a href={sdk.links.github} className="text-gold-dim hover:text-gold transition-colors">
                      GitHub <ArrowUpRight className="inline h-3 w-3" />
                    </a>
                  ) : null}
                  <a href={sdk.links.doc} className="text-gold-dim hover:text-gold transition-colors">
                    文档 <ArrowUpRight className="inline h-3 w-3" />
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 协议声明 */}
      <section className="hairline-t px-6 py-20 md:px-12">
        <div className="mx-auto max-w-container">
          <div className="hairline flex flex-col items-center gap-6 bg-ink-2 p-10 text-center">
            <SealTag>MulanPSL v2 · 商业友好</SealTag>
            <p className="max-w-[640px] text-[14px] leading-[2] text-paper-faint">
              工程层代码采用 MulanPSL v2 开源许可，允许商业使用、修改、分发。
              思想层内容（协议/白皮书/哲学）受 CC BY-NC-SA 4.0 保护。
            </p>
          </div>
        </div>
      </section>
    </>
  )
}
