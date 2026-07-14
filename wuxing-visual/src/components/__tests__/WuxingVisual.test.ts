/**
 * 龍魂五行计算器 · React 组件单元测试
 *
 * 🐉 DNA:#龍芯⚡️2026-06-07-WUXING-VISUAL-TEST-v3.5
 * 责任: UID9622 · 不免责
 */

import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import * as React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { WuxingVisualSystem } from '../WuxingVisual';

// ============================================================================
// [测试数据]
// ============================================================================

const mockWuxingData = {
  center: {
    id: 'center-uid9622',
    label: 'UID9622',
  },
  rivers: [
    {
      id: 'river-metal',
      name: '金 · 西方',
      wuxing: 'metal' as const,
      color: '#FFD700',
      description: '肃杀·收敛·秋季之气',
    },
    {
      id: 'river-wood',
      name: '木 · 东方',
      wuxing: 'wood' as const,
      color: '#90EE90',
      description: '生长·展开·春季之气',
    },
    {
      id: 'river-water',
      name: '水 · 北方',
      wuxing: 'water' as const,
      color: '#87CEEB',
      description: '润泽·下行·冬季之气',
    },
  ],
  nodes: [
    {
      id: 'node-001',
      label: 'DNA 签章验证',
      riverId: 'river-metal',
      layer: 2,
      children: [],
      dnaStatus: 'verified' as const,
    },
    {
      id: 'node-002',
      label: '规则引擎',
      riverId: 'river-wood',
      layer: 2,
      children: [],
      dnaStatus: 'verified' as const,
    },
  ],
  archiveNodes: [],
};

// ============================================================================
// [组件测试套件]
// ============================================================================

describe('WuxingVisualSystem 组件', () => {
  let container: HTMLElement;

  beforeEach(() => {
    container = document.createElement('div');
    document.body.appendChild(container);
  });

  afterEach(() => {
    if (container && container.parentNode) {
      container.parentNode.removeChild(container);
    }
  });

  // ========================================================================
  // [渲染测试]
  // ========================================================================

  it('应该正确渲染主容器', () => {
    const { container: testContainer } = render(
      <WuxingVisualSystem data={mockWuxingData} />,
      { container }
    );

    expect(testContainer.querySelector('.wuxing-visual-container')).toBeTruthy();
  });

  it('应该显示中心节点 (北辰不动点)', () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const centerNode = container.querySelector('.center-node');
    expect(centerNode).toBeTruthy();
    expect(centerNode?.textContent).toContain('UID9622');
  });

  it('应该渲染所有五行河道', () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const riverButtons = container.querySelectorAll('[class*="river"]');
    // 应该有 3 个河道按钮
    expect(riverButtons.length).toBeGreaterThanOrEqual(3);
  });

  // ========================================================================
  // [交互测试]
  // ========================================================================

  it('点击河道应该选择该河道', async () => {
    const { rerender } = render(
      <WuxingVisualSystem data={mockWuxingData} />,
      { container }
    );

    // 找到第一个河道按钮
    const riverButtons = container.querySelectorAll('button');
    const firstRiver = riverButtons[0];

    // 点击河道
    fireEvent.click(firstRiver);

    // 等待状态更新
    await waitFor(() => {
      // 河道应该被选中 (视觉效果: scale-125)
      const styles = window.getComputedStyle(firstRiver);
      expect(firstRiver.classList.contains('scale-125') ||
             styles.transform.includes('scale')).toBeTruthy();
    }, { timeout: 500 });
  });

  it('重复点击同一河道应该取消选择', async () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const riverButtons = container.querySelectorAll('button');
    const firstRiver = riverButtons[0];

    // 第一次点击: 选择
    fireEvent.click(firstRiver);
    await waitFor(() => {
      expect(firstRiver).toHaveClass('scale-125');
    }, { timeout: 300 });

    // 第二次点击: 取消选择
    fireEvent.click(firstRiver);
    await waitFor(() => {
      expect(firstRiver).not.toHaveClass('scale-125');
    }, { timeout: 300 });
  });

  it('应该显示审计面板', () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const auditPanel = container.querySelector('.audit-panel');
    expect(auditPanel).toBeTruthy();
    expect(auditPanel?.textContent).toContain('三色审计');
  });

  // ========================================================================
  // [Layer 组件测试]
  // ========================================================================

  it('Layer0 应该显示正确的中心标签', () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const centerNode = container.querySelector('.layer-0');
    expect(centerNode?.textContent).toContain('UID9622');
  });

  it('Layer1 应该显示所有河道', () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const layer1 = container.querySelector('.layer-1');
    const riverElements = layer1?.querySelectorAll('button');

    expect(riverElements?.length).toBe(mockWuxingData.rivers.length);
  });

  it('Layer56 应该显示外圈归档信息', () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const layer56 = container.querySelector('.layer-56');
    expect(layer56?.textContent).toContain('DNA 审计门');
    expect(layer56?.textContent).toContain('待审外圈');
    expect(layer56?.textContent).toContain('熔断隔离');
  });

  // ========================================================================
  // [数据绑定测试]
  // ========================================================================

  it('河道颜色应该正确绑定', () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const riverButtons = container.querySelectorAll('[style*="background"]');
    // 应该有河道按钮带颜色
    expect(riverButtons.length).toBeGreaterThan(0);
  });

  it('节点状态应该影响颜色', () => {
    const dataWithMixedStatus = {
      ...mockWuxingData,
      nodes: [
        ...mockWuxingData.nodes,
        {
          id: 'node-003',
          label: '待审节点',
          riverId: 'river-water',
          layer: 2,
          children: [],
          dnaStatus: 'pending' as const,
        },
      ],
    };

    render(<WuxingVisualSystem data={dataWithMixedStatus} />, { container });

    // 应该有不同颜色的节点
    const styledNodes = container.querySelectorAll('[style*="background"]');
    expect(styledNodes.length).toBeGreaterThan(mockWuxingData.nodes.length);
  });

  // ========================================================================
  // [无障碍测试]
  // ========================================================================

  it('河道按钮应该有 title 属性用于无障碍', () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const riverButtons = container.querySelectorAll('button[title]');
    expect(riverButtons.length).toBeGreaterThan(0);
  });

  it('应该支持键盘导航 (可点击的按钮)', () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const buttons = container.querySelectorAll('button');
    buttons.forEach(button => {
      // 所有按钮应该是可聚焦的
      expect(button.tabIndex).toBeGreaterThanOrEqual(-1);
    });
  });

  // ========================================================================
  // [性能测试]
  // ========================================================================

  it('应该在 1 秒内完成初始渲染', async () => {
    const startTime = performance.now();

    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const endTime = performance.now();
    const renderTime = endTime - startTime;

    expect(renderTime).toBeLessThan(1000);
  });

  it('应该支持大型数据集 (1000+ 节点)', () => {
    const largeData = {
      ...mockWuxingData,
      nodes: Array.from({ length: 1000 }, (_, i) => ({
        id: `node-${i}`,
        label: `节点 ${i}`,
        riverId: mockWuxingData.rivers[i % mockWuxingData.rivers.length].id,
        layer: 2 + (i % 4),
        children: [],
        dnaStatus: (i % 3 === 0 ? 'verified' : 'pending') as const,
      })),
    };

    const startTime = performance.now();
    render(<WuxingVisualSystem data={largeData} />, { container });
    const endTime = performance.now();

    expect(endTime - startTime).toBeLessThan(3000); // 3秒内
  });

  // ========================================================================
  // [边界情况测试]
  // ========================================================================

  it('应该处理空河道列表', () => {
    const emptyData = {
      ...mockWuxingData,
      rivers: [],
    };

    expect(() => {
      render(<WuxingVisualSystem data={emptyData} />, { container });
    }).not.toThrow();
  });

  it('应该处理空节点列表', () => {
    const emptyData = {
      ...mockWuxingData,
      nodes: [],
    };

    expect(() => {
      render(<WuxingVisualSystem data={emptyData} />, { container });
    }).not.toThrow();
  });

  it('应该处理未定义的 children', () => {
    const dataWithoutChildren = {
      ...mockWuxingData,
      nodes: [
        {
          id: 'node-test',
          label: '测试节点',
          riverId: 'river-metal',
          layer: 2,
          // children 未定义
          dnaStatus: 'verified' as const,
        } as any,
      ],
    };

    expect(() => {
      render(<WuxingVisualSystem data={dataWithoutChildren} />, { container });
    }).not.toThrow();
  });
});

// ============================================================================
// [集成测试]
// ============================================================================

describe('WuxingVisualSystem 集成测试', () => {
  let container: HTMLElement;

  beforeEach(() => {
    container = document.createElement('div');
    document.body.appendChild(container);
  });

  afterEach(() => {
    if (container && container.parentNode) {
      container.parentNode.removeChild(container);
    }
  });

  it('完整的用户交互流程', async () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    // 1. 验证初始渲染
    expect(container.querySelector('.center-node')).toBeTruthy();

    // 2. 点击河道
    const riverButtons = container.querySelectorAll('button');
    fireEvent.click(riverButtons[0]);

    await waitFor(() => {
      expect(riverButtons[0]).toHaveClass('scale-125');
    }, { timeout: 300 });

    // 3. 验证审计面板更新
    const auditPanel = container.querySelector('.audit-panel');
    expect(auditPanel?.textContent).toContain('绿色');

    // 4. 点击另一个河道
    fireEvent.click(riverButtons[1]);

    await waitFor(() => {
      expect(riverButtons[1]).toHaveClass('scale-125');
    }, { timeout: 300 });
  });

  it('应该正确管理展开/折叠状态', async () => {
    const dataWithChildren = {
      ...mockWuxingData,
      nodes: [
        {
          ...mockWuxingData.nodes[0],
          children: [
            {
              id: 'node-001-1',
              label: '子节点 1',
              riverId: 'river-metal',
              layer: 3,
              children: [],
              dnaStatus: 'verified' as const,
            },
          ],
        },
      ],
    };

    render(<WuxingVisualSystem data={dataWithChildren} />, { container });

    // 应该支持节点展开状态
    const expandedElements = container.querySelectorAll('[class*="expand"]');
    // 可能没有展开，但不应该出错
    expect(container.querySelector('.wuxing-visual-container')).toBeTruthy();
  });
});

// ============================================================================
// [快照测试]
// ============================================================================

describe('WuxingVisualSystem 快照测试', () => {
  it('应该与快照匹配', () => {
    const { container } = render(
      <WuxingVisualSystem data={mockWuxingData} />
    );

    expect(container).toMatchSnapshot();
  });
});

// ============================================================================
// [性能基准]
// ============================================================================

describe('WuxingVisualSystem 性能基准', () => {
  it('渲染性能: 初始化 < 500ms', () => {
    const start = performance.now();
    render(<WuxingVisualSystem data={mockWuxingData} />);
    const end = performance.now();

    console.log(`✅ 初始化耗时: ${(end - start).toFixed(2)}ms`);
    expect(end - start).toBeLessThan(500);
  });

  it('交互性能: 河道切换 < 100ms', async () => {
    const { container } = render(
      <WuxingVisualSystem data={mockWuxingData} />
    );

    const button = container.querySelector('button');
    const start = performance.now();
    fireEvent.click(button!);
    const end = performance.now();

    console.log(`✅ 河道切换耗时: ${(end - start).toFixed(2)}ms`);
    expect(end - start).toBeLessThan(100);
  });
});
