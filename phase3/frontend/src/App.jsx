import React, { useState, useEffect, useRef } from 'react';
import './App.css';

/**
 * 龍魂系统 Phase 3 - React 前端框架 v1.0
 * Longhun System Phase 3 - React Frontend Framework v1.0
 * 
 * DNA:#龍芯⚡️2026-06-06-PHASE3-REACT-FRONTEND-v1.0
 * Author: UID9622 (龍芯北辰)
 * Status: Production Ready
 */

// API 基础 URL
const API_URL = 'http://localhost:8000/api/v1';
const WS_URL = 'ws://localhost:8000/ws/v1/stream';

// ═══════════════════════════════════════════════════════════════════════════
// 第一部·API 客户端
// ═══════════════════════════════════════════════════════════════════════════

class ApiClient {
  static async get(endpoint) {
    const response = await fetch(`${API_URL}${endpoint}`);
    if (!response.ok) throw new Error(`API Error: ${response.statusText}`);
    return response.json();
  }

  static async post(endpoint, data) {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error(`API Error: ${response.statusText}`);
    return response.json();
  }

  static async put(endpoint, data) {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error(`API Error: ${response.statusText}`);
    return response.json();
  }

  static async delete(endpoint) {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'DELETE'
    });
    if (!response.ok) throw new Error(`API Error: ${response.statusText}`);
    return response.json();
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// 第二部·UI 组件
// ═══════════════════════════════════════════════════════════════════════════

// 仪表板卡片组件
const MetricCard = ({ title, value, unit, color }) => (
  <div className={`metric-card ${color}`}>
    <h3>{title}</h3>
    <div className="metric-value">
      {value}
      {unit && <span className="unit">{unit}</span>}
    </div>
  </div>
);

// 告警卡片组件
const AlertCard = ({ alert, onAcknowledge }) => (
  <div className={`alert-card level-${alert.level}`}>
    <div className="alert-header">
      <span className={`badge level-${alert.level}`}>{alert.level}</span>
      <span className="message">{alert.message}</span>
    </div>
    <div className="alert-footer">
      <span className="source">{alert.source}</span>
      <button onClick={() => onAcknowledge(alert.id)} className="btn-small">
        确认
      </button>
    </div>
  </div>
);

// 技能卡片组件
const SkillCard = ({ skill, onExecute }) => (
  <div className="skill-card">
    <div className="skill-header">
      <h4>{skill.name}</h4>
      <span className={`status ${skill.status}`}>{skill.status}</span>
    </div>
    <div className="skill-body">
      <p><strong>平台:</strong> {skill.platform}</p>
      <p><strong>分类:</strong> {skill.category}</p>
      <p><strong>优先级:</strong> {skill.priority}/10</p>
      <p><strong>执行次数:</strong> {skill.execution_count}</p>
      <p><strong>成功率:</strong> {skill.success_rate.toFixed(1)}%</p>
    </div>
    <button onClick={() => onExecute(skill.id)} className="btn-execute">
      执行
    </button>
  </div>
);

// 执行历史表格
const ExecutionTable = ({ executions }) => (
  <table className="execution-table">
    <thead>
      <tr>
        <th>执行 ID</th>
        <th>技能</th>
        <th>状态</th>
        <th>耗时 (ms)</th>
        <th>开始时间</th>
      </tr>
    </thead>
    <tbody>
      {executions.map(exec => (
        <tr key={exec.id} className={`status-${exec.status}`}>
          <td className="monospace">{exec.id.substring(0, 8)}...</td>
          <td>{exec.skill_id}</td>
          <td><span className={`badge ${exec.status}`}>{exec.status}</span></td>
          <td>{exec.duration_ms || '-'}</td>
          <td>{new Date(exec.start_time).toLocaleTimeString()}</td>
        </tr>
      ))}
    </tbody>
  </table>
);

// ═══════════════════════════════════════════════════════════════════════════
// 第三部·页面组件
// ═══════════════════════════════════════════════════════════════════════════

// 仪表板页面
const DashboardPage = () => {
  const [metrics, setMetrics] = useState(null);
  const [recentExecutions, setRecentExecutions] = useState([]);
  const [activeAlerts, setActiveAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const wsRef = useRef(null);

  useEffect(() => {
    // 加载初始数据
    loadDashboard();

    // 建立 WebSocket 连接
    connectWebSocket();

    // 定期刷新（每 5 秒）
    const interval = setInterval(loadDashboard, 5000);

    return () => {
      clearInterval(interval);
      if (wsRef.current) wsRef.current.close();
    };
  }, []);

  const loadDashboard = async () => {
    try {
      const data = await ApiClient.get('/dashboard');
      setMetrics(data.metrics);
      setRecentExecutions(data.recent_executions);
      setActiveAlerts(data.active_alerts);
      setLoading(false);
    } catch (error) {
      console.error('加载仪表板失败:', error);
    }
  };

  const connectWebSocket = () => {
    wsRef.current = new WebSocket(WS_URL);
    wsRef.current.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.type === 'health') {
        setMetrics(message.data);
      }
    };
    wsRef.current.onerror = (error) => {
      console.error('WebSocket 错误:', error);
    };
  };

  const handleAcknowledge = async (alertId) => {
    try {
      await ApiClient.post(`/alerts/${alertId}/acknowledge`, {});
      loadDashboard();
    } catch (error) {
      console.error('确认告警失败:', error);
    }
  };

  if (loading) return <div className="loading">加载中...</div>;

  return (
    <div className="dashboard-page">
      <h2>龍魂系统仪表板</h2>

      {/* 核心指标 */}
      <section className="metrics-section">
        <h3>系统指标</h3>
        <div className="metrics-grid">
          <MetricCard title="CPU 使用率" value={metrics?.cpu} unit="%" color="cpu" />
          <MetricCard title="内存使用率" value={metrics?.memory} unit="%" color="memory" />
          <MetricCard title="磁盘使用率" value={metrics?.disk} unit="%" color="disk" />
          <MetricCard title="执行成功率" value={metrics?.success_rate} unit="%" color="success" />
        </div>
      </section>

      {/* 活跃告警 */}
      {activeAlerts.length > 0 && (
        <section className="alerts-section">
          <h3>活跃告警 ({activeAlerts.length})</h3>
          <div className="alerts-list">
            {activeAlerts.map(alert => (
              <AlertCard
                key={alert.id}
                alert={alert}
                onAcknowledge={handleAcknowledge}
              />
            ))}
          </div>
        </section>
      )}

      {/* 最近执行 */}
      <section className="executions-section">
        <h3>最近执行</h3>
        {recentExecutions.length > 0 ? (
          <ExecutionTable executions={recentExecutions} />
        ) : (
          <p className="empty">暂无执行记录</p>
        )}
      </section>
    </div>
  );
};

// 技能管理页面
const SkillsPage = () => {
  const [skills, setSkills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [platform, setPlatform] = useState(null);
  const [newSkill, setNewSkill] = useState({
    id: '',
    name: '',
    platform: 'longhun',
    category: 'general',
    priority: 5
  });

  useEffect(() => {
    loadSkills();
  }, [platform]);

  const loadSkills = async () => {
    try {
      const query = platform ? `?platform=${platform}` : '';
      const data = await ApiClient.get(`/skills${query}`);
      setSkills(data);
      setLoading(false);
    } catch (error) {
      console.error('加载技能失败:', error);
    }
  };

  const handleCreateSkill = async () => {
    if (!newSkill.id || !newSkill.name) {
      alert('请填写必要信息');
      return;
    }

    try {
      await ApiClient.post('/skills', newSkill);
      setNewSkill({ id: '', name: '', platform: 'longhun', category: 'general', priority: 5 });
      loadSkills();
      alert('技能创建成功');
    } catch (error) {
      console.error('创建技能失败:', error);
      alert('创建技能失败');
    }
  };

  const handleExecuteSkill = async (skillId) => {
    try {
      const result = await ApiClient.post(`/skills/${skillId}/execute`, {});
      alert(`技能已提交执行: ${result.execution_id}`);
      loadSkills();
    } catch (error) {
      console.error('执行技能失败:', error);
      alert('执行技能失败');
    }
  };

  if (loading) return <div className="loading">加载中...</div>;

  return (
    <div className="skills-page">
      <h2>技能管理</h2>

      {/* 创建新技能 */}
      <section className="create-skill-section">
        <h3>注册新技能</h3>
        <div className="form-grid">
          <input
            type="text"
            placeholder="技能 ID (如: /health-check)"
            value={newSkill.id}
            onChange={(e) => setNewSkill({ ...newSkill, id: e.target.value })}
          />
          <input
            type="text"
            placeholder="技能名称"
            value={newSkill.name}
            onChange={(e) => setNewSkill({ ...newSkill, name: e.target.value })}
          />
          <select
            value={newSkill.platform}
            onChange={(e) => setNewSkill({ ...newSkill, platform: e.target.value })}
          >
            <option value="longhun">龍魂</option>
            <option value="kimi">Kimi</option>
            <option value="claude">Claude</option>
            <option value="ollama">Ollama</option>
          </select>
          <input
            type="text"
            placeholder="分类"
            value={newSkill.category}
            onChange={(e) => setNewSkill({ ...newSkill, category: e.target.value })}
          />
          <input
            type="number"
            min="1"
            max="10"
            value={newSkill.priority}
            onChange={(e) => setNewSkill({ ...newSkill, priority: parseInt(e.target.value) })}
          />
          <button onClick={handleCreateSkill} className="btn-primary">
            创建技能
          </button>
        </div>
      </section>

      {/* 技能列表 */}
      <section className="skills-section">
        <h3>技能列表 ({skills.length})</h3>
        <div className="platform-filter">
          <button
            className={!platform ? 'active' : ''}
            onClick={() => setPlatform(null)}
          >
            全部
          </button>
          {['longhun', 'kimi', 'claude', 'ollama'].map(p => (
            <button
              key={p}
              className={platform === p ? 'active' : ''}
              onClick={() => setPlatform(p)}
            >
              {p}
            </button>
          ))}
        </div>
        <div className="skills-grid">
          {skills.map(skill => (
            <SkillCard
              key={skill.id}
              skill={skill}
              onExecute={handleExecuteSkill}
            />
          ))}
        </div>
      </section>
    </div>
  );
};

// 告警管理页面
const AlertsPage = () => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('active');

  useEffect(() => {
    loadAlerts();
    const interval = setInterval(loadAlerts, 3000);
    return () => clearInterval(interval);
  }, [filter]);

  const loadAlerts = async () => {
    try {
      const query = filter ? `?status=${filter}` : '';
      const data = await ApiClient.get(`/alerts${query}`);
      setAlerts(data);
      setLoading(false);
    } catch (error) {
      console.error('加载告警失败:', error);
    }
  };

  const handleAcknowledge = async (alertId) => {
    try {
      await ApiClient.post(`/alerts/${alertId}/acknowledge`, {});
      loadAlerts();
    } catch (error) {
      console.error('确认告警失败:', error);
    }
  };

  if (loading) return <div className="loading">加载中...</div>;

  return (
    <div className="alerts-page">
      <h2>告警管理</h2>

      <div className="filter-tabs">
        <button
          className={filter === 'active' ? 'active' : ''}
          onClick={() => setFilter('active')}
        >
          活跃 ({alerts.length})
        </button>
        <button
          className={filter === 'acknowledged' ? 'active' : ''}
          onClick={() => setFilter('acknowledged')}
        >
          已确认
        </button>
        <button
          className={filter === 'resolved' ? 'active' : ''}
          onClick={() => setFilter('resolved')}
        >
          已解决
        </button>
      </div>

      <div className="alerts-list">
        {alerts.length > 0 ? (
          alerts.map(alert => (
            <AlertCard
              key={alert.id}
              alert={alert}
              onAcknowledge={handleAcknowledge}
            />
          ))
        ) : (
          <p className="empty">没有 {filter} 状态的告警</p>
        )}
      </div>
    </div>
  );
};



// 龍魂 Skills 页面
const LonghunSkillsPage = () => {
  const [htmlSkills, setHtmlSkills] = useState([]);
  const [pythonSkills, setPythonSkills] = useState([]);
  const [selectedSkill, setSelectedSkill] = useState(null);
  const [skillContent, setSkillContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('list');

  useEffect(() => {
    loadLonghunSkills();
  }, []);

  const loadLonghunSkills = async () => {
    try {
      const data = await ApiClient.get('/longhun-skills');
      setHtmlSkills(data.html_skills || []);
      setPythonSkills(data.python_skills || []);
      setLoading(false);
    } catch (error) {
      console.error('加载龍魂 Skills 失败:', error);
    }
  };

  const handleViewSkill = async (skillId) => {
    try {
      const data = await ApiClient.get(`/longhun-skills/${skillId}/content`);
      setSelectedSkill(skillId);
      setSkillContent(data.content);
      setActiveTab('content');
    } catch (error) {
      console.error('获取 Skill 内容失败:', error);
    }
  };

  const handleExecuteSkill = async (skillId) => {
    try {
      const result = await ApiClient.post(`/longhun-skills/${skillId}/execute`, {});
      alert(`Skill 已提交执行: ${result.execution_id}`);
    } catch (error) {
      console.error('执行 Skill 失败:', error);
      alert('执行 Skill 失败');
    }
  };

  if (loading) return <div className="loading">加载龍魂 Skills 中...</div>;

  return (
    <div className="longhun-skills-page">
      <h2>🐉 龍魂 Skills 系统</h2>
      
      <div className="skills-tabs">
        <button
          className={activeTab === 'list' ? 'active' : ''}
          onClick={() => setActiveTab('list')}
        >
          Skills 列表 ({htmlSkills.length + pythonSkills.length})
        </button>
        {selectedSkill && (
          <button
            className={activeTab === 'content' ? 'active' : ''}
            onClick={() => setActiveTab('content')}
          >
            查看内容
          </button>
        )}
      </div>

      {activeTab === 'list' && (
        <>
          {/* HTML Interactive Skills */}
          <section className="skills-section">
            <h3>🎨 HTML Interactive Skills ({htmlSkills.length})</h3>
            <div className="skills-grid">
              {htmlSkills.map(skill => (
                <div key={skill.name} className="skill-card html-skill">
                  <div className="skill-header">
                    <h4>{skill.name}</h4>
                    <span className="skill-type">HTML</span>
                  </div>
                  <div className="skill-body">
                    <p>{skill.filename}</p>
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                    <button 
                      onClick={() => handleViewSkill(skill.name)} 
                      className="btn-small"
                    >
                      查看
                    </button>
                    <button 
                      onClick={() => handleExecuteSkill(skill.name)} 
                      className="btn-small"
                    >
                      渲染
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Python Utility Skills */}
          <section className="skills-section">
            <h3>🐍 Python Utility Skills ({pythonSkills.length})</h3>
            <div className="skills-grid">
              {pythonSkills.map(skill => (
                <div key={skill.name} className="skill-card python-skill">
                  <div className="skill-header">
                    <h4>{skill.name}</h4>
                    <span className="skill-type">Python</span>
                  </div>
                  <div className="skill-body">
                    <p>{skill.filename}</p>
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                    <button 
                      onClick={() => handleViewSkill(skill.name)} 
                      className="btn-small"
                    >
                      查看
                    </button>
                    <button 
                      onClick={() => handleExecuteSkill(skill.name)} 
                      className="btn-small"
                    >
                      执行
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </section>
        </>
      )}

      {activeTab === 'content' && selectedSkill && (
        <section className="skill-content-section">
          <h3>📄 {selectedSkill} - 内容</h3>
          <div style={{ 
            backgroundColor: '#0a0e27', 
            padding: '20px', 
            borderRadius: '8px',
            border: '1px solid #00d4ff',
            maxHeight: '600px',
            overflow: 'auto'
          }}>
            <pre style={{ margin: 0, color: '#00d4ff', fontSize: '12px' }}>
              {skillContent.substring(0, 2000)}...
            </pre>
          </div>
          <button 
            onClick={() => setActiveTab('list')} 
            className="btn-primary"
            style={{ marginTop: '20px' }}
          >
            返回列表
          </button>
        </section>
      )}
    </div>
  );
};


// ═══════════════════════════════════════════════════════════════════════════
// 第四部·主应用组件
// ═══════════════════════════════════════════════════════════════════════════

export default function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <DashboardPage />;
      case 'skills':
        return <SkillsPage />;
      case 'alerts':
        return <AlertsPage />;
            case 'longhun-skills':
        return <LonghunSkillsPage />;
      default:
        return <DashboardPage />;
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="logo">
          <h1>🐉 龍魂系统 Phase 3</h1>
          <p>AI 行为治理框架·三层监督·生产级别</p>
        </div>
      </header>

      <nav className="app-nav">
        <button
          className={currentPage === 'dashboard' ? 'active' : ''}
          onClick={() => setCurrentPage('dashboard')}
        >
          📊 仪表板
        </button>
        <button
          className={currentPage === 'skills' ? 'active' : ''}
          onClick={() => setCurrentPage('skills')}
        >
          ⚙️ 技能管理
        </button>
        <button
          className={currentPage === 'alerts' ? 'active' : ''}
          onClick={() => setCurrentPage('alerts')}
        >
          🚨 告警系统
        </button>
        <button
          className={currentPage === 'longhun-skills' ? 'active' : ''}
          onClick={() => setCurrentPage('longhun-skills')}
        >
          🐉 龍魂 Skills
        </button>

      </nav>

      <main className="app-main">
        {renderPage()}
      </main>

      <footer className="app-footer">
        <p>DNA:#龍芯⚡️2026-06-06-PHASE3-REACT-FRONTEND-v1.0</p>
        <p>责任: UID9622 · 不免责</p>
      </footer>
    </div>
  );
}
