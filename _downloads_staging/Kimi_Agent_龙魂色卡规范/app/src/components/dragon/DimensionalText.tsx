/*
  龍魂系统 · 多维字体组件
  文件名：DimensionalText.tsx
  来源：src/components/dragon/DimensionalText.tsx
  根文件：~/.龍魂/LONGHUN_ETERNAL_ANCHOR.md
  创作者：UJID9622 · 龍芯北辰
  用途：根据维度、状态、情绪、五行属性渲染龍魂特效文字
  注意：本标头为来源链的一部分，删除或剥离将破坏来源完整性

  DNA: #龍芯⚡️20260626140000000-DIMENSIONAL-TEXT-COMPONENT-v1.0
*/

import React from 'react';
import { cn } from '@/lib/utils';

export type Dimension = '3d' | '4d' | '5d';
export type Emotion = 'green' | 'red' | 'yellow' | 'gold' | 'blue' | 'purple';
export type Wuxing = 'metal' | 'wood' | 'water' | 'fire' | 'earth';
export type PulseState = 'green' | 'red' | 'yellow' | 'gold';

export interface DimensionalTextProps {
  children: React.ReactNode;
  /** 维度：3D 空间 / 4D 时间 / 5D 语义 */
  dimension?: Dimension;
  /** 3D 具体模式 */
  mode3d?: 'scale' | 'bevel' | 'emboss';
  /** 4D 具体模式 */
  mode4d?: 'breathe' | 'flow' | 'pulse';
  /** 5D 具体模式 */
  mode5d?: 'emotion' | 'wuxing' | 'weight';
  /** 情绪色相 */
  emotion?: Emotion;
  /** 五行属性 */
  wuxing?: Wuxing;
  /** 脉动状态 */
  pulse?: PulseState;
  /** 数据权重 [0, 1]，用于字重映射 */
  weight?: number;
  /** 是否降低动画（性能降级） */
  reducedMotion?: boolean;
  className?: string;
  as?: 'h1' | 'h2' | 'h3' | 'p' | 'span' | 'div';
}

function mapWeightToClass(weight: number = 0.5): string {
  const clamped = Math.max(0, Math.min(1, weight));
  const level = Math.round(clamped * 6);
  return `dragon-text-weight-${level}`;
}

export function DimensionalText({
  children,
  dimension = '3d',
  mode3d = 'scale',
  mode4d = 'breathe',
  mode5d = 'emotion',
  emotion = 'gold',
  wuxing = 'fire',
  pulse = 'gold',
  weight = 0.5,
  reducedMotion = false,
  className,
  as: Component = 'span',
}: DimensionalTextProps) {
  const classes: string[] = [];

  // 3D: 空间深度
  if (dimension === '3d') {
    if (mode3d === 'scale') classes.push('dragon-text-3d');
    if (mode3d === 'bevel') classes.push('dragon-text-bevel');
    if (mode3d === 'emboss') classes.push('dragon-text-emboss');
  }

  // 4D: 时间流动
  if (dimension === '4d' && !reducedMotion) {
    if (mode4d === 'breathe') classes.push('dragon-text-breathe');
    if (mode4d === 'flow') classes.push('dragon-text-flow');
    if (mode4d === 'pulse') classes.push(`dragon-text-pulse-${pulse}`);
  }

  // 5D: 语义权重
  if (dimension === '5d') {
    if (mode5d === 'emotion') classes.push(`dragon-text-emotion-${emotion}`);
    if (mode5d === 'wuxing') classes.push(`dragon-text-wuxing-${wuxing}`);
    if (mode5d === 'weight') classes.push(mapWeightToClass(weight));
  }

  return (
    <Component className={cn(classes, className)}>
      {children}
    </Component>
  );
}

export default DimensionalText;
