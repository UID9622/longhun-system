// 龍魂宝宝助手组件 v3.0
// DNA:#龍芯⚡️2026-07-07-BAOBAO-COMPONENT-v3.0
// 扩展：计算机引擎卡片（三才·易经·BraKet·CNSH-64·Lu·四柱·公式·五维诊断）

import React, { useMemo } from 'react'
import { useBaobaoStore } from '../store/baobao'
import '../styles/animations.css'

export const Baobao: React.FC = () => {
  const { expression, action, message, isVisible, skillData, bubbleColor } = useBaobaoStore()

  const containerStyle = useMemo(
    () => ({
      position: 'fixed' as const,
      bottom: '30px',
      right: '30px',
      zIndex: 999998,
      opacity: isVisible ? 1 : 0,
      transition: 'opacity 0.3s',
      pointerEvents: 'none' as const,
    }),
    [isVisible]
  )

  // 根据数字根改变宝宝光晕颜色
  const glowColor = useMemo(() => {
    if (!skillData?.五行颜色 && !skillData?.数字报告?.颜色) return 'rgba(255, 20, 147, 0.2)'
    const hex = skillData.五行颜色 || skillData.数字报告?.颜色 || '#FF1493'
    return `${hex}44`
  }, [skillData])

  const baobaoStyle = useMemo(
    () => ({
      width: '80px',
      height: '80px',
      borderRadius: '50%',
      background: 'radial-gradient(circle at 30% 30%, #FFE4E1, #FFB6C1)',
      boxShadow: `0 4px 20px rgba(255, 182, 193, 0.4), 0 0 40px ${glowColor}`,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      animation:
        action === 'talking'
          ? 'baobao-talk 0.4s infinite'
          : action === 'waving'
            ? 'baobao-wave 0.6s ease-in-out'
            : action === 'pulsing'
              ? 'baobao-pulse 1s ease-in-out infinite'
              : 'baobao-breathing 3s ease-in-out infinite',
      cursor: 'pointer',
      position: 'relative' as const,
    }),
    [action, glowColor]
  )

  const eyeStyle = {
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    background: '#333',
    position: 'absolute' as const,
  }

  // 计算中的眼睛变样式
  const leftEyeStyle = useMemo(() => ({
    ...eyeStyle,
    left: '20px',
    top: '25px',
    ...(expression === 'calculating' ? { background: '#DAA520', width: '10px', height: '2px', borderRadius: '2px', top: '27px' } : {}),
  }), [expression])

  const rightEyeStyle = useMemo(() => ({
    ...eyeStyle,
    right: '20px',
    top: '25px',
    ...(expression === 'calculating' ? { background: '#DAA520', width: '10px', height: '2px', borderRadius: '2px', top: '27px' } : {}),
  }), [expression])

  // 判断是否显示技能卡片
  const showSkillCard = Boolean(skillData && (
    skillData.数字根 !== undefined ||
    skillData.五行 ||
    skillData.DNA码 ||
    skillData.综合得分 !== undefined ||
    skillData.卦象名称 ||
    skillData.主力人格 ||
    skillData.Lu指令 ||
    skillData.均衡指数 !== undefined ||
    skillData.状态空间 ||
    skillData.五维诊断
  ))

  const bubbleStyle = useMemo(
    () => ({
      position: 'absolute' as const,
      bottom: showSkillCard ? '-200px' : '-80px',
      left: '50%',
      transform: 'translateX(-50%)',
      background: bubbleColor,
      color: '#fff',
      padding: showSkillCard ? '12px 16px' : '8px 12px',
      borderRadius: '12px',
      fontSize: '12px',
      whiteSpace: showSkillCard ? ('normal' as const) : ('nowrap' as const),
      border: `2px solid ${bubbleColor}`,
      boxShadow: '0 2px 10px rgba(0, 0, 0, 0.15)',
      animation: 'bubble-pop 0.3s ease-out',
      maxWidth: showSkillCard ? '220px' : '150px',
      overflow: 'hidden',
    }),
    [bubbleColor, showSkillCard]
  )

  const tailStyle = {
    position: 'absolute' as const,
    width: '30px',
    height: '30px',
    background: '#FFB6C1',
    borderRadius: '50%',
    bottom: '-20px',
    left: '60%',
    animation: 'baobao-tail 1.5s ease-in-out infinite',
  }

  // 渲染技能卡片内容
  const renderSkillCard = () => {
    if (!skillData) return null

    const sd = skillData as any

    // v3.0 计算机五维诊断卡片
    if (sd.五维诊断) {
      const dims = sd.五维诊断
      return (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '14px', fontWeight: 'bold', marginBottom: '6px' }}>
            🖥️ 五维诊断
          </div>
          <div style={{ fontSize: '9px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '3px', textAlign: 'left' }}>
            <span>🧮 {dims.数字根?.值 || '?'}</span>
            <span>{dims.数字根?.五行 || '?'}</span>
            <span>☯️ {dims.易经卦象?.卦名 || '?'}</span>
            <span>{dims.易经卦象?.判定 || '?'}</span>
            <span>⟨∣ {dims.BraKet人格?.主力 || '?'}</span>
            <span>{dims.BraKet人格?.匹配场景 || '?'}</span>
            <span>lu {dims.Lu指令?.层级?.split('=')?.[0] || '?'}</span>
            <span>{dims.三才决策?.三色 || '?'} {dims.三才决策?.得分 || '?'}</span>
          </div>
        </div>
      )
    }

    // v3.0 三才决策卡片
    if (sd.综合得分 !== undefined && sd.三色) {
      return (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '16px', fontWeight: 'bold', marginBottom: '4px' }}>
            {sd.三色} 三才 {sd.综合得分}
          </div>
          <div style={{ fontSize: '10px', opacity: 0.85 }}>
            天{sd.输入?.['天(时势)'] || '?'}·地{sd.输入?.['地(条件)'] || '?'}·人{sd.输入?.['人(意志)'] || '?'}
          </div>
          <div style={{ fontSize: '9px', marginTop: '3px', fontStyle: 'italic' }}>
            {sd.建议}
          </div>
        </div>
      )
    }

    // v3.0 易经64卦卡片
    if (sd.卦象名称 && sd.最终判定) {
      return (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '16px', fontWeight: 'bold', marginBottom: '4px' }}>
            ☯️ {sd.卦象名称} · {sd.最终判定}
          </div>
          <div style={{ fontSize: '10px', opacity: 0.85 }}>
            风险 {sd.风险等级 || sd.风险级别}
          </div>
          {sd.推理过程 && (
            <div style={{ fontSize: '9px', marginTop: '3px', opacity: 0.75 }}>
              {sd.推理过程}
            </div>
          )}
        </div>
      )
    }

    // v3.0 BraKet人格卡片
    if (sd.主力人格) {
      return (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '14px', fontWeight: 'bold', marginBottom: '4px' }}>
            ⟨⚛️∣ BraKet坍缩
          </div>
          <div style={{ fontSize: '12px' }}>
            {sd.主力人格.名称} ({sd.主力人格.权重})
          </div>
          <div style={{ fontSize: '10px', opacity: 0.8 }}>{sd.匹配场景}</div>
          {sd.权重分布 && (
            <div style={{ fontSize: '8px', marginTop: '4px' }}>
              {Object.keys(sd.权重分布 || {}).slice(0, 4).join('·')}
            </div>
          )}
        </div>
      )
    }

    // v3.0 Lu指令卡片
    if (sd.Lu指令 && sd.层级) {
      return (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '14px', fontWeight: 'bold', marginBottom: '4px' }}>
            💻 Lu指令
          </div>
          <div style={{ fontSize: '11px', fontFamily: 'monospace' }}>
            {sd.Lu指令}
          </div>
          <div style={{ fontSize: '10px', opacity: 0.8 }}>{sd.层级}</div>
          <div style={{ fontSize: '9px', marginTop: '2px' }}>
            {sd.数字根预检}
          </div>
        </div>
      )
    }

    // v3.0 四柱五行卡片
    if (sd.均衡指数 !== undefined && sd.最强 && sd.最弱) {
      return (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '14px', fontWeight: 'bold', marginBottom: '4px' }}>
            🎋 四柱五行
          </div>
          <div style={{ fontSize: '11px' }}>
            强:{sd.最强} 弱:{sd.最弱}
          </div>
          <div style={{ fontSize: '10px' }}>
            均衡 {sd.均衡指数}·{sd.健康状态}
          </div>
        </div>
      )
    }

    // v3.0 CNSH-64 状态卡片
    if (sd.状态空间) {
      return (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '15px', fontWeight: 'bold', marginBottom: '4px' }}>
            📐 CNSH-64
          </div>
          <div style={{ fontSize: '11px' }}>{sd.维度}</div>
          <div style={{ fontSize: '9px', opacity: 0.8 }}>
            |状态空间|=64 &lt; ∞·可控进化
          </div>
        </div>
      )
    }

    // v2.0 数字根+五行卡片
    if (sd.数字根 !== undefined || sd.数字报告?.数字根 !== undefined) {
      const dr = sd.数字根 ?? sd.数字报告?.数字根
      const wx = sd.五行 ?? sd.数字报告?.五行
      const risk = sd.风险 ?? sd.风险级别
      const is369 = dr === 3 || dr === 6 || dr === 9
      return (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '4px' }}>
            {is369 ? '⚡' : '🔢'} 数字根 {dr} · {wx}
          </div>
          <div style={{ fontSize: '10px', opacity: 0.85 }}>
            河图{dr}{sd.数字报告?.方位 || ''}属{wx}
          </div>
          {risk && (
            <div style={{ fontSize: '10px', marginTop: '4px', fontWeight: 'bold' }}>
              {risk}
            </div>
          )}
          {is369 && (
            <div style={{ fontSize: '9px', marginTop: '2px', opacity: 0.75 }}>
              三才算法内核·369不动点
            </div>
          )}
        </div>
      )
    }

    // v2.0 DNA卡片
    if (sd.DNA码) {
      return (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '14px', fontWeight: 'bold', marginBottom: '2px' }}>🧬 DNA已生成</div>
          <div style={{ fontSize: '9px', fontFamily: 'monospace', wordBreak: 'break-all' }}>
            {sd.DNA码}
          </div>
        </div>
      )
    }

    // v2.0 河图洛书卡片
    if (sd.河图 || sd.洛书) {
      return (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '16px', marginBottom: '2px' }}>🏔️ 河图洛书</div>
          <div style={{ fontSize: '11px' }}>中五不动点 = 5</div>
          <div style={{ fontSize: '9px', opacity: 0.8 }}>369三才内核</div>
        </div>
      )
    }

    return null
  }

  return (
    <div style={containerStyle} className="baobao-container">
      <div style={baobaoStyle} className={`baobao baobao-${expression}`}>
        {/* 眼睛 */}
        <div style={leftEyeStyle} />
        <div style={rightEyeStyle} />

        {/* 嘴巴 */}
        <div
          style={{
            position: 'absolute',
            bottom: '20px',
            width: '20px',
            height: '10px',
            borderBottom: '2px solid #333',
            borderRadius: '0 0 20px 20px',
          }}
        />

        {/* 尾巴 */}
        <div style={tailStyle} />
      </div>

      {/* 语音/技能气泡 */}
      {message && (
        <div style={bubbleStyle}>
          {showSkillCard && renderSkillCard()}
          {!showSkillCard && message}
          {showSkillCard && (
            <div style={{ fontSize: '10px', marginTop: '6px', opacity: 0.9, borderTop: '1px solid rgba(255,255,255,0.2)', paddingTop: '4px' }}>
              {message}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
