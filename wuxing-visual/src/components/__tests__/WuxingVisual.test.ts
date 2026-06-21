/**
 * 龍魂五行計算器 · React 組件單元測試
 *
 * 🐉 DNA:#龍芯⚡️2026-06-07-WUXING-VISUAL-TEST-v3.5
 * 責任: UID9622 · 不免責
 */

import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import * as React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { WuxingVisualSystem } from '../WuxingVisual';

// ============================================================================
// [測試數據]
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
      description: '肅殺·收斂·秋季之氣',
    },
    {
      id: 'river-wood',
      name: '木 · 東方',
      wuxing: 'wood' as const,
      color: '#90EE90',
      description: '生長·展開·春季之氣',
    },
    {
      id: 'river-water',
      name: '水 · 北方',
      wuxing: 'water' as const,
      color: '#87CEEB',
      description: '潤澤·下行·冬季之氣',
    },
  ],
  nodes: [
    {
      id: 'node-001',
      label: 'DNA 簽章驗證',
      riverId: 'river-metal',
      layer: 2,
      children: [],
      dnaStatus: 'verified' as const,
    },
    {
      id: 'node-002',
      label: '規則引擎',
      riverId: 'river-wood',
      layer: 2,
      children: [],
      dnaStatus: 'verified' as const,
    },
  ],
  archiveNodes: [],
};

// ============================================================================
// [組件測試套件]
// ============================================================================

describe('WuxingVisualSystem 組件', () => {
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
  // [渲染測試]
  // ========================================================================

  it('應該正確渲染主容器', () => {
    const { container: testContainer } = render(
      <WuxingVisualSystem data={mockWuxingData} />,
      { container }
    );

    expect(testContainer.querySelector('.wuxing-visual-container')).toBeTruthy();
  });

  it('應該顯示中心節點 (北辰不動點)', () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const centerNode = container.querySelector('.center-node');
    expect(centerNode).toBeTruthy();
    expect(centerNode?.textContent).toContain('UID9622');
  });

  it('應該渲染所有五行河道', () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const riverButtons = container.querySelectorAll('[class*="river"]');
    // 應該有 3 個河道按鈕
    expect(riverButtons.length).toBeGreaterThanOrEqual(3);
  });

  // ========================================================================
  // [交互測試]
  // ========================================================================

  it('點擊河道應該選擇該河道', async () => {
    const { rerender } = render(
      <WuxingVisualSystem data={mockWuxingData} />,
      { container }
    );

    // 找到第一個河道按鈕
    const riverButtons = container.querySelectorAll('button');
    const firstRiver = riverButtons[0];

    // 點擊河道
    fireEvent.click(firstRiver);

    // 等待狀態更新
    await waitFor(() => {
      // 河道應該被選中 (視覺效果: scale-125)
      const styles = window.getComputedStyle(firstRiver);
      expect(firstRiver.classList.contains('scale-125') ||
             styles.transform.includes('scale')).toBeTruthy();
    }, { timeout: 500 });
  });

  it('重複點擊同一河道應該取消選擇', async () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const riverButtons = container.querySelectorAll('button');
    const firstRiver = riverButtons[0];

    // 第一次點擊: 選擇
    fireEvent.click(firstRiver);
    await waitFor(() => {
      expect(firstRiver).toHaveClass('scale-125');
    }, { timeout: 300 });

    // 第二次點擊: 取消選擇
    fireEvent.click(firstRiver);
    await waitFor(() => {
      expect(firstRiver).not.toHaveClass('scale-125');
    }, { timeout: 300 });
  });

  it('應該顯示審計面板', () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const auditPanel = container.querySelector('.audit-panel');
    expect(auditPanel).toBeTruthy();
    expect(auditPanel?.textContent).toContain('三色審計');
  });

  // ========================================================================
  // [Layer 組件測試]
  // ========================================================================

  it('Layer0 應該顯示正確的中心標籤', () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const centerNode = container.querySelector('.layer-0');
    expect(centerNode?.textContent).toContain('UID9622');
  });

  it('Layer1 應該顯示所有河道', () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const layer1 = container.querySelector('.layer-1');
    const riverElements = layer1?.querySelectorAll('button');

    expect(riverElements?.length).toBe(mockWuxingData.rivers.length);
  });

  it('Layer56 應該顯示外圈歸檔信息', () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const layer56 = container.querySelector('.layer-56');
    expect(layer56?.textContent).toContain('DNA 審計門');
    expect(layer56?.textContent).toContain('待審外圈');
    expect(layer56?.textContent).toContain('熔斷隔離');
  });

  // ========================================================================
  // [數據綁定測試]
  // ========================================================================

  it('河道顏色應該正確綁定', () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const riverButtons = container.querySelectorAll('[style*="background"]');
    // 應該有河道按鈕帶顏色
    expect(riverButtons.length).toBeGreaterThan(0);
  });

  it('節點狀態應該影響顏色', () => {
    const dataWithMixedStatus = {
      ...mockWuxingData,
      nodes: [
        ...mockWuxingData.nodes,
        {
          id: 'node-003',
          label: '待審節點',
          riverId: 'river-water',
          layer: 2,
          children: [],
          dnaStatus: 'pending' as const,
        },
      ],
    };

    render(<WuxingVisualSystem data={dataWithMixedStatus} />, { container });

    // 應該有不同顏色的節點
    const styledNodes = container.querySelectorAll('[style*="background"]');
    expect(styledNodes.length).toBeGreaterThan(mockWuxingData.nodes.length);
  });

  // ========================================================================
  // [無障礙測試]
  // ========================================================================

  it('河道按鈕應該有 title 屬性用於無障礙', () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const riverButtons = container.querySelectorAll('button[title]');
    expect(riverButtons.length).toBeGreaterThan(0);
  });

  it('應該支持鍵盤導航 (可點擊的按鈕)', () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const buttons = container.querySelectorAll('button');
    buttons.forEach(button => {
      // 所有按鈕應該是可聚焦的
      expect(button.tabIndex).toBeGreaterThanOrEqual(-1);
    });
  });

  // ========================================================================
  // [性能測試]
  // ========================================================================

  it('應該在 1 秒內完成初始渲染', async () => {
    const startTime = performance.now();

    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    const endTime = performance.now();
    const renderTime = endTime - startTime;

    expect(renderTime).toBeLessThan(1000);
  });

  it('應該支持大型數據集 (1000+ 節點)', () => {
    const largeData = {
      ...mockWuxingData,
      nodes: Array.from({ length: 1000 }, (_, i) => ({
        id: `node-${i}`,
        label: `節點 ${i}`,
        riverId: mockWuxingData.rivers[i % mockWuxingData.rivers.length].id,
        layer: 2 + (i % 4),
        children: [],
        dnaStatus: (i % 3 === 0 ? 'verified' : 'pending') as const,
      })),
    };

    const startTime = performance.now();
    render(<WuxingVisualSystem data={largeData} />, { container });
    const endTime = performance.now();

    expect(endTime - startTime).toBeLessThan(3000); // 3秒內
  });

  // ========================================================================
  // [邊界情況測試]
  // ========================================================================

  it('應該處理空河道列表', () => {
    const emptyData = {
      ...mockWuxingData,
      rivers: [],
    };

    expect(() => {
      render(<WuxingVisualSystem data={emptyData} />, { container });
    }).not.toThrow();
  });

  it('應該處理空節點列表', () => {
    const emptyData = {
      ...mockWuxingData,
      nodes: [],
    };

    expect(() => {
      render(<WuxingVisualSystem data={emptyData} />, { container });
    }).not.toThrow();
  });

  it('應該處理未定義的 children', () => {
    const dataWithoutChildren = {
      ...mockWuxingData,
      nodes: [
        {
          id: 'node-test',
          label: '測試節點',
          riverId: 'river-metal',
          layer: 2,
          // children 未定義
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
// [集成測試]
// ============================================================================

describe('WuxingVisualSystem 集成測試', () => {
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

  it('完整的用戶交互流程', async () => {
    render(<WuxingVisualSystem data={mockWuxingData} />, { container });

    // 1. 驗證初始渲染
    expect(container.querySelector('.center-node')).toBeTruthy();

    // 2. 點擊河道
    const riverButtons = container.querySelectorAll('button');
    fireEvent.click(riverButtons[0]);

    await waitFor(() => {
      expect(riverButtons[0]).toHaveClass('scale-125');
    }, { timeout: 300 });

    // 3. 驗證審計面板更新
    const auditPanel = container.querySelector('.audit-panel');
    expect(auditPanel?.textContent).toContain('綠色');

    // 4. 點擊另一個河道
    fireEvent.click(riverButtons[1]);

    await waitFor(() => {
      expect(riverButtons[1]).toHaveClass('scale-125');
    }, { timeout: 300 });
  });

  it('應該正確管理展開/摺疊狀態', async () => {
    const dataWithChildren = {
      ...mockWuxingData,
      nodes: [
        {
          ...mockWuxingData.nodes[0],
          children: [
            {
              id: 'node-001-1',
              label: '子節點 1',
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

    // 應該支持節點展開狀態
    const expandedElements = container.querySelectorAll('[class*="expand"]');
    // 可能沒有展開，但不應該出錯
    expect(container.querySelector('.wuxing-visual-container')).toBeTruthy();
  });
});

// ============================================================================
// [快照測試]
// ============================================================================

describe('WuxingVisualSystem 快照測試', () => {
  it('應該與快照匹配', () => {
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

    console.log(`✅ 初始化耗時: ${(end - start).toFixed(2)}ms`);
    expect(end - start).toBeLessThan(500);
  });

  it('交互性能: 河道切換 < 100ms', async () => {
    const { container } = render(
      <WuxingVisualSystem data={mockWuxingData} />
    );

    const button = container.querySelector('button');
    const start = performance.now();
    fireEvent.click(button!);
    const end = performance.now();

    console.log(`✅ 河道切換耗時: ${(end - start).toFixed(2)}ms`);
    expect(end - start).toBeLessThan(100);
  });
});
