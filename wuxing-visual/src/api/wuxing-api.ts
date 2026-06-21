/**
 * 龍魂五行計算器 · API 集成層
 *
 * 🐉 DNA:#龍芯⚡️2026-06-07-WUXING-API-v3.5
 * 責任: UID9622 · 不免責
 */

export interface WuxingTreeResponse {
  center: {
    id: string;
    label: string;
  };
  rivers: River[];
  nodes: Node[];
  archiveNodes: Node[];
}

export interface River {
  id: string;
  name: string;
  wuxing: 'metal' | 'wood' | 'water' | 'fire' | 'earth';
  color: string;
  description: string;
}

export interface Node {
  id: string;
  label: string;
  riverId: string;
  layer: number;
  children: Node[];
  dnaStatus: 'verified' | 'pending' | 'rejected';
  data?: Record<string, any>;
}

export interface CalculateRequest {
  input: string;
  riverIds?: string[];
}

export interface CalculateResponse {
  result: {
    dnaSignature: string;
    wuxing: string;
    strength: number;
    nodes: Node[];
  };
  processingTime: number;
}

// ============================================================================
// [API 基礎類]
// ============================================================================

export class WuxingAPI {
  private baseUrl: string;
  private timeout: number = 10000;

  constructor(baseUrl: string = 'http://localhost:8000/api') {
    this.baseUrl = baseUrl;
  }

  /**
   * 獲取完整五行樹數據
   */
  async getWuxingTree(): Promise<WuxingTreeResponse> {
    return this.request<WuxingTreeResponse>('GET', '/wuxing/tree');
  }

  /**
   * 獲取單個河道數據
   */
  async getRiver(riverId: string): Promise<River> {
    return this.request<River>('GET', `/wuxing/river/${riverId}`);
  }

  /**
   * 獲取節點詳情
   */
  async getNode(nodeId: string): Promise<Node> {
    return this.request<Node>('GET', `/wuxing/node/${nodeId}`);
  }

  /**
   * 執行五行計算
   */
  async calculate(request: CalculateRequest): Promise<CalculateResponse> {
    return this.request<CalculateResponse>('POST', '/wuxing/calculate', request);
  }

  /**
   * 獲取三色審計狀態
   */
  async getAuditStatus(nodeId: string): Promise<{ status: 'verified' | 'pending' | 'rejected'; details: string }> {
    return this.request('GET', `/wuxing/audit/${nodeId}`);
  }

  /**
   * 批量驗證節點
   */
  async verifyNodes(nodeIds: string[]): Promise<Record<string, boolean>> {
    return this.request('POST', '/wuxing/verify-nodes', { nodeIds });
  }

  // ============================================================================
  // [內部方法]
  // ============================================================================

  private async request<T>(method: string, endpoint: string, body?: any): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    const options: RequestInit = {
      method,
      headers: {
        'Content-Type': 'application/json',
        'X-Client': 'wuxing-visual-v3.5',
      },
    };

    if (body && (method === 'POST' || method === 'PUT')) {
      options.body = JSON.stringify(body);
    }

    try {
      const response = await Promise.race([
        fetch(url, options),
        new Promise<Response>((_, reject) =>
          setTimeout(() => reject(new Error('Request timeout')), this.timeout)
        ),
      ]);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API 請求失敗: ${method} ${endpoint}`, error);
      throw error;
    }
  }
}

// ============================================================================
// [Mock API · 離線開發]
// ============================================================================

export class WuxingAPIMock extends WuxingAPI {
  async getWuxingTree(): Promise<WuxingTreeResponse> {
    // 模擬延遲
    await new Promise((resolve) => setTimeout(resolve, 200));

    return {
      center: {
        id: 'center-uid9622',
        label: 'UID9622',
      },
      rivers: [
        {
          id: 'river-metal',
          name: '金 · 西方',
          wuxing: 'metal',
          color: '#FFD700',
          description: '肅殺·收斂·秋季之氣',
        },
        {
          id: 'river-wood',
          name: '木 · 東方',
          wuxing: 'wood',
          color: '#90EE90',
          description: '生長·展開·春季之氣',
        },
        {
          id: 'river-water',
          name: '水 · 北方',
          wuxing: 'water',
          color: '#87CEEB',
          description: '潤澤·下行·冬季之氣',
        },
        {
          id: 'river-fire',
          name: '火 · 南方',
          wuxing: 'fire',
          color: '#FF6347',
          description: '炎上·向上·夏季之氣',
        },
        {
          id: 'river-earth',
          name: '土 · 中央',
          wuxing: 'earth',
          color: '#CD853F',
          description: '承載·居中·四時交界',
        },
      ],
      nodes: [
        {
          id: 'node-001',
          label: 'DNA 簽章驗證',
          riverId: 'river-metal',
          layer: 2,
          children: [
            { id: 'node-001-1', label: 'SHA-256 哈希', riverId: 'river-metal', layer: 3, children: [], dnaStatus: 'verified' },
            { id: 'node-001-2', label: 'GPG 簽名', riverId: 'river-metal', layer: 3, children: [], dnaStatus: 'verified' },
          ],
          dnaStatus: 'verified',
        },
        {
          id: 'node-002',
          label: '規則引擎',
          riverId: 'river-wood',
          layer: 2,
          children: [
            { id: 'node-002-1', label: '六條核心規則', riverId: 'river-wood', layer: 3, children: [], dnaStatus: 'verified' },
          ],
          dnaStatus: 'verified',
        },
        {
          id: 'node-003',
          label: 'Secret Guard',
          riverId: 'river-water',
          layer: 2,
          children: [],
          dnaStatus: 'pending',
        },
      ],
      archiveNodes: [
        { id: 'archive-001', label: '已驗證節點', riverId: '', layer: 5, children: [], dnaStatus: 'verified' },
      ],
    };
  }

  async calculate(request: CalculateRequest): Promise<CalculateResponse> {
    await new Promise((resolve) => setTimeout(resolve, 300));

    return {
      result: {
        dnaSignature: '#龍芯⚡️2026-06-07-WUXING-CALC-v1.0',
        wuxing: 'water',
        strength: 0.85,
        nodes: [],
      },
      processingTime: 125,
    };
  }

  async getAuditStatus(nodeId: string): Promise<any> {
    await new Promise((resolve) => setTimeout(resolve, 100));

    return {
      status: 'verified' as const,
      details: '通過三色審計·無安全風險',
    };
  }
}

// ============================================================================
// [API 客戶端單例]
// ============================================================================

let apiInstance: WuxingAPI | null = null;

export function getWuxingAPI(useMock: boolean = false): WuxingAPI {
  if (!apiInstance) {
    apiInstance = useMock ? new WuxingAPIMock() : new WuxingAPI();
  }
  return apiInstance;
}

export function setWuxingAPI(api: WuxingAPI): void {
  apiInstance = api;
}

// ============================================================================
// [React Hook · 使用 API]
// ============================================================================

import { useEffect, useState } from 'react';

export function useWuxingTree() {
  const [data, setData] = useState<WuxingTreeResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const api = getWuxingAPI(true); // 先用 Mock
        const result = await api.getWuxingTree();
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err : new Error(String(err)));
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  return { data, loading, error };
}

export function useWuxingCalculate() {
  const [result, setResult] = useState<CalculateResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const calculate = async (input: string) => {
    setLoading(true);
    try {
      const api = getWuxingAPI(true);
      const response = await api.calculate({ input });
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err : new Error(String(err)));
    } finally {
      setLoading(false);
    }
  };

  return { result, loading, error, calculate };
}
