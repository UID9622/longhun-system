/*
  龍魂系统 · 多维字体展示页
  文件名：TypographyPage.tsx
  来源：src/pages/typography/TypographyPage.tsx
  根文件：~/.龍魂/LONGHUN_ETERNAL_ANCHOR.md
  创作者：UJID9622 · 龍芯北辰
  注意：本标头为来源链的一部分，删除或剥离将破坏来源完整性

  DNA: #龍芯⚡️20260626140000000-TYPOGRAPHY-PAGE-v1.0
*/

import { DimensionalText } from '@/components/dragon';

export function TypographyPage() {
  return (
    <div className="min-h-screen bg-spectrum-void text-spectrum-bright p-8 space-y-16">
      <section className="space-y-4">
        <h2 className="text-label text-spectrum-dim">3D · 空间深度</h2>
        <div className="space-y-6">
          <DimensionalText dimension="3d" mode3d="scale" as="h1" className="text-hero">
            龍魂
          </DimensionalText>
          <DimensionalText dimension="3d" mode3d="bevel" as="h2" className="text-h1">
            晶面倒角
          </DimensionalText>
          <DimensionalText dimension="3d" mode3d="emboss" as="h3" className="text-h2">
            浮雕主权
          </DimensionalText>
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-label text-spectrum-dim">4D · 时间流动</h2>
        <div className="space-y-6">
          <DimensionalText dimension="4d" mode4d="breathe" as="h2" className="text-h1">
            呼吸权重
          </DimensionalText>
          <DimensionalText dimension="4d" mode4d="flow" as="h2" className="text-h1">
            流光扫描
          </DimensionalText>
          <div className="flex gap-8">
            <DimensionalText dimension="4d" mode4d="pulse" pulse="green" className="text-h2">
              通过
            </DimensionalText>
            <DimensionalText dimension="4d" mode4d="pulse" pulse="red" className="text-h2">
              熔断
            </DimensionalText>
            <DimensionalText dimension="4d" mode4d="pulse" pulse="yellow" className="text-h2">
              警示
            </DimensionalText>
            <DimensionalText dimension="4d" mode4d="pulse" pulse="gold" className="text-h2">
              主控
            </DimensionalText>
          </div>
        </div>
      </section>

      <section className="space-y-4">
        <h2 className="text-label text-spectrum-dim">5D · 语义权重</h2>
        <div className="space-y-6">
          <div className="flex gap-6 flex-wrap">
            <DimensionalText dimension="5d" mode5d="emotion" emotion="green" className="text-h2">
              稳定
            </DimensionalText>
            <DimensionalText dimension="5d" mode5d="emotion" emotion="red" className="text-h2">
              危险
            </DimensionalText>
            <DimensionalText dimension="5d" mode5d="emotion" emotion="gold" className="text-h2">
              主权
            </DimensionalText>
            <DimensionalText dimension="5d" mode5d="emotion" emotion="blue" className="text-h2">
              外联
            </DimensionalText>
            <DimensionalText dimension="5d" mode5d="emotion" emotion="purple" className="text-h2">
              进化
            </DimensionalText>
          </div>
          <div className="flex gap-6 flex-wrap">
            <DimensionalText dimension="5d" mode5d="wuxing" wuxing="metal" className="text-h2">
              金
            </DimensionalText>
            <DimensionalText dimension="5d" mode5d="wuxing" wuxing="wood" className="text-h2">
              木
            </DimensionalText>
            <DimensionalText dimension="5d" mode5d="wuxing" wuxing="water" className="text-h2">
              水
            </DimensionalText>
            <DimensionalText dimension="5d" mode5d="wuxing" wuxing="fire" className="text-h2">
              火
            </DimensionalText>
            <DimensionalText dimension="5d" mode5d="wuxing" wuxing="earth" className="text-h2">
              土
            </DimensionalText>
          </div>
          <div className="space-y-2">
            <DimensionalText dimension="5d" mode5d="weight" weight={0.1} className="text-h3">
              权重 0.1
            </DimensionalText>
            <DimensionalText dimension="5d" mode5d="weight" weight={0.5} className="text-h3">
              权重 0.5
            </DimensionalText>
            <DimensionalText dimension="5d" mode5d="weight" weight={0.9} className="text-h3">
              权重 0.9
            </DimensionalText>
          </div>
        </div>
      </section>
    </div>
  );
}

export default TypographyPage;
