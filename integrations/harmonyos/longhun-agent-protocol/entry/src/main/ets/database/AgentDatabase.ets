// entry/src/main/ets/database/AgentDatabase.ets
// 龍魂 · 智能体协议数据库 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { relationalStore } from '@kit.ArkData';
import { BusinessError } from '@kit.BasicServicesKit';

const STORE_CONFIG: relationalStore.StoreConfig = {
  name: 'LonghunAgent.db',
  securityLevel: relationalStore.SecurityLevel.S3
};

const SQL_CREATE_AGENTS = `
  CREATE TABLE IF NOT EXISTS agents (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    agent_type TEXT NOT NULL DEFAULT 'user',
    version TEXT DEFAULT '1.0.0',
    device_id TEXT,
    device_type TEXT DEFAULT 'phone',
    endpoint TEXT,
    protocol TEXT DEFAULT '1.0.0',
    status TEXT DEFAULT 'offline',
    permission_level INTEGER DEFAULT 1,
    allowed_scopes TEXT DEFAULT '*',
    dna_signature TEXT,
    registered_at INTEGER,
    updated_at INTEGER
  )
`;

const SQL_CREATE_CAPABILITIES = `
  CREATE TABLE IF NOT EXISTS capabilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    version TEXT DEFAULT '1.0.0',
    enabled INTEGER DEFAULT 1,
    FOREIGN KEY (agent_id) REFERENCES agents(id) ON DELETE CASCADE
  )
`;

const SQL_CREATE_TASKS = `
  CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    intent_id TEXT,
    action TEXT NOT NULL,
    params TEXT,
    priority INTEGER DEFAULT 2,
    status TEXT DEFAULT 'pending',
    progress INTEGER DEFAULT 0,
    executor_id TEXT,
    result TEXT,
    error TEXT,
    dna_signature TEXT,
    created_at INTEGER,
    started_at INTEGER,
    completed_at INTEGER,
    deadline INTEGER
  )
`;

const SQL_CREATE_MESSAGES = `
  CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    msg_type TEXT NOT NULL,
    version TEXT DEFAULT '1.0.0',
    msg_from TEXT,
    msg_to TEXT,
    timestamp INTEGER,
    payload TEXT,
    signature TEXT,
    dna_signature TEXT
  )
`;

const SQL_CREATE_AUDIT = `
  CREATE TABLE IF NOT EXISTS audit_log (
    id TEXT PRIMARY KEY,
    action TEXT NOT NULL,
    actor TEXT NOT NULL,
    target TEXT NOT NULL,
    result TEXT DEFAULT 'success',
    details TEXT,
    dna_signature TEXT,
    timestamp INTEGER
  )
`;

const SQL_CREATE_CIRCUIT_BREAKERS = `
  CREATE TABLE IF NOT EXISTS circuit_breakers (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    target TEXT NOT NULL,
    failure_threshold INTEGER DEFAULT 5,
    success_threshold INTEGER DEFAULT 3,
    timeout_duration INTEGER DEFAULT 30000,
    state TEXT DEFAULT 'closed',
    failure_count INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    total_calls INTEGER DEFAULT 0,
    total_failures INTEGER DEFAULT 0,
    total_successes INTEGER DEFAULT 0
  )
`;

// 索引
const SQL_INDEXES = [
  'CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status)',
  'CREATE INDEX IF NOT EXISTS idx_agents_type ON agents(agent_type)',
  'CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)',
  'CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority)',
  'CREATE INDEX IF NOT EXISTS idx_messages_type ON messages(msg_type)',
  'CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp DESC)',
  'CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_log(action)',
  'CREATE INDEX IF NOT EXISTS idx_audit_actor ON audit_log(actor)',
  'CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_log(timestamp DESC)',
  'CREATE INDEX IF NOT EXISTS idx_cb_state ON circuit_breakers(state)'
];

// 统计视图
const SQL_STATS_VIEW = `
  CREATE VIEW IF NOT EXISTS v_agent_stats AS
  SELECT
    (SELECT COUNT(*) FROM agents) as total_agents,
    (SELECT COUNT(*) FROM agents WHERE status = 'online') as online_agents,
    (SELECT COUNT(*) FROM tasks) as total_tasks,
    (SELECT COUNT(*) FROM tasks WHERE status = 'pending') as pending_tasks,
    (SELECT COUNT(*) FROM tasks WHERE status = 'running') as running_tasks,
    (SELECT COUNT(*) FROM tasks WHERE status = 'completed') as completed_tasks,
    (SELECT COUNT(*) FROM tasks WHERE status = 'failed') as failed_tasks,
    (SELECT COUNT(*) FROM circuit_breakers WHERE state = 'open') as open_circuits
`;

export class AgentDatabase {
  static store: relationalStore.RdbStore | null = null;

  static async init(): Promise<void> {
    try {
      const context = getContext();
      this.store = await relationalStore.getRdbStore(context, STORE_CONFIG);

      await this.store.executeSql(SQL_CREATE_AGENTS);
      await this.store.executeSql(SQL_CREATE_CAPABILITIES);
      await this.store.executeSql(SQL_CREATE_TASKS);
      await this.store.executeSql(SQL_CREATE_MESSAGES);
      await this.store.executeSql(SQL_CREATE_AUDIT);
      await this.store.executeSql(SQL_CREATE_CIRCUIT_BREAKERS);

      for (const idxSql of SQL_INDEXES) {
        await this.store.executeSql(idxSql);
      }

      await this.store.executeSql(SQL_STATS_VIEW);
      console.info('[龍魂] Agent数据库初始化完成');
    } catch (err) {
      const error = err as BusinessError;
      console.error(`[龍魂] 数据库初始化失败: ${error.message}`);
    }
  }

  static async getStats(): Promise<any> {
    if (!this.store) return null;
    try {
      const predicates = new relationalStore.RdbPredicates('v_agent_stats');
      const resultSet = await this.store.query(predicates);
      if (resultSet.goToFirstRow()) {
        return {
          totalAgents: resultSet.getLong(resultSet.getColumnIndex('total_agents')),
          onlineAgents: resultSet.getLong(resultSet.getColumnIndex('online_agents')),
          totalTasks: resultSet.getLong(resultSet.getColumnIndex('total_tasks')),
          pendingTasks: resultSet.getLong(resultSet.getColumnIndex('pending_tasks')),
          runningTasks: resultSet.getLong(resultSet.getColumnIndex('running_tasks')),
          completedTasks: resultSet.getLong(resultSet.getColumnIndex('completed_tasks')),
          failedTasks: resultSet.getLong(resultSet.getColumnIndex('failed_tasks')),
          openCircuits: resultSet.getLong(resultSet.getColumnIndex('open_circuits'))
        };
      }
    } catch (err) {
      console.error('[龍魂] 统计数据查询失败');
    }
    return null;
  }

  static async insertAgent(agent: any): Promise<void> {
    if (!this.store) return;
    const valueBucket: relationalStore.ValuesBucket = {
      id: agent.id,
      name: agent.name,
      agent_type: agent.type,
      version: agent.version,
      device_id: agent.deviceId,
      device_type: agent.deviceType,
      endpoint: agent.endpoint,
      protocol: agent.protocol,
      status: agent.status,
      permission_level: agent.permissionLevel,
      allowed_scopes: agent.allowedScopes.join(','),
      dna_signature: agent.dnaSignature,
      registered_at: Date.now(),
      updated_at: Date.now()
    };
    await this.store.insert('agents', valueBucket);
  }

  static async updateAgentStatus(id: string, status: string): Promise<void> {
    if (!this.store) return;
    const valueBucket: relationalStore.ValuesBucket = {
      status: status,
      updated_at: Date.now()
    };
    const predicates = new relationalStore.RdbPredicates('agents');
    predicates.equalTo('id', id);
    await this.store.update(valueBucket, predicates);
  }

  static async insertTask(task: any): Promise<void> {
    if (!this.store) return;
    const valueBucket: relationalStore.ValuesBucket = {
      id: task.id,
      intent_id: task.intentId,
      action: task.action,
      params: JSON.stringify(task.params),
      priority: task.priority,
      status: task.status,
      progress: task.progress,
      executor_id: task.executorId,
      dna_signature: task.dnaSignature,
      created_at: task.createdAt?.getTime() || Date.now()
    };
    await this.store.insert('tasks', valueBucket);
  }

  static async updateTaskProgress(id: string, progress: number, status: string): Promise<void> {
    if (!this.store) return;
    const valueBucket: relationalStore.ValuesBucket = {
      progress: progress,
      status: status,
      completed_at: status === 'completed' || status === 'failed' ? Date.now() : undefined
    };
    const predicates = new relationalStore.RdbPredicates('tasks');
    predicates.equalTo('id', id);
    await this.store.update(valueBucket, predicates);
  }

  static async insertMessage(msg: any): Promise<void> {
    if (!this.store) return;
    const valueBucket: relationalStore.ValuesBucket = {
      id: msg.id,
      msg_type: msg.type,
      version: msg.version,
      msg_from: msg.from,
      msg_to: msg.to,
      timestamp: msg.timestamp,
      payload: JSON.stringify(msg.payload),
      signature: msg.signature,
      dna_signature: msg.dnaSignature
    };
    await this.store.insert('messages', valueBucket);
  }

  static async insertAudit(record: any): Promise<void> {
    if (!this.store) return;
    const valueBucket: relationalStore.ValuesBucket = {
      id: record.id,
      action: record.action,
      actor: record.actor,
      target: record.target,
      result: record.result,
      details: JSON.stringify(record.details),
      dna_signature: record.dnaSignature,
      timestamp: record.timestamp?.getTime() || Date.now()
    };
    await this.store.insert('audit_log', valueBucket);
  }

  static async cleanup(): Promise<void> {
    if (!this.store) return;
    const threshold = Date.now() - 30 * 24 * 60 * 60 * 1000; // 30天前
    const predicates = new relationalStore.RdbPredicates('messages');
    predicates.lessThan('timestamp', threshold);
    await this.store.delete(predicates);
    console.info('[龍魂] 数据库清理完成 (30天前消息已清除)');
  }

  static destroy(): void {
    if (this.store) {
      this.store.close();
      this.store = null;
    }
  }
}
