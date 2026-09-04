# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 龍之心语 v2.0 · 完整演示数据
// DNA: #龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-LONGHUN-HEART-TALK-v2.0

import type {
  User, Room, Message, AuditEntry, AIModel, PlazaRepo,
  Contributor, AuthGrant, ApiEndpoint, GithubRepo
} from '@/types';
import { generateDNA, sha256Hash, auditMessage, getTimestamp } from './dna';

// ─── 当前用户 ───
export const CURRENT_USER: User = {
  uid: 'UID9622',
  name: '龍芯北辰',
  avatar: 'https://avatars.githubusercontent.com/u/228023117?v=4',
  creditScore: 9999,
  contributionScore: 8888,
  status: 'online',
  verified: true,
  gpgFingerprint: 'A2D0092CEE2E5BA87035600924C3704A8CC26D5F',
  authLevel: 'founder',
  joinedAt: '2024-01-01',
  repos: 5,
};

const USER_AI: User = {
  uid: 'LH-KIMI-001', name: 'Kimi智能体', avatar: '',
  creditScore: 10000, contributionScore: 5000,
  status: 'online', verified: true,
  authLevel: 'maintainer', joinedAt: '2024-06-01', repos: 0,
};

const USER_DEV: User = {
  uid: 'LH-DEV-042', name: '开发者小易', avatar: '',
  creditScore: 3200, contributionScore: 1800,
  status: 'away', verified: true,
  authLevel: 'developer', joinedAt: '2025-03-15', repos: 2,
};

const USER_VETERAN: User = {
  uid: 'LH-VET-007', name: '老战友阿强', avatar: '',
  creditScore: 5600, contributionScore: 4200,
  status: 'offline', verified: true,
  authLevel: 'citizen', joinedAt: '2025-01-10', repos: 0,
};

// ─── AI模型广场 ───
export const AI_MODELS: AIModel[] = [
  // 本地模型
  {
    id: 'model-llama3', name: 'Llama 3.1', provider: 'ollama', type: 'local',
    description: 'Meta开源大模型，支持8B/70B参数，可完全本地部署，数据绝对不出境',
    version: '3.1', tags: ['llm', '本地优先', '开源'], parameters: '8B/70B',
    license: 'LLAMA 3.1', status: 'online', downloads: 15420, rating: 4.7,
    dna: generateDNA('HEART-TALK', 'MODEL-Llama3'), mcpSupport: true,
    localInstall: 'ollama pull llama3.1', requirements: '8GB+ RAM / GPU可选',
    apiEndpoint: 'http://localhost:11434',
  },
  {
    id: 'model-qwen2', name: 'Qwen 2.5', provider: 'ollama', type: 'local',
    description: '阿里巴巴通义千问开源版，中文能力优秀，支持本地部署',
    version: '2.5', tags: ['llm', '中文', '开源'], parameters: '7B/72B',
    license: 'QWEN', status: 'online', downloads: 12800, rating: 4.6,
    dna: generateDNA('HEART-TALK', 'MODEL-Qwen2'), mcpSupport: true,
    localInstall: 'ollama pull qwen2.5', requirements: '8GB+ RAM',
    apiEndpoint: 'http://localhost:11434',
  },
  {
    id: 'model-deepeek-coder', name: 'DeepSeek-Coder', provider: 'lmstudio', type: 'local',
    description: 'DeepSeek代码专用模型，编程能力强劲，支持多种编程语言',
    version: 'v2', tags: ['coding', '开发助手', '开源'], parameters: '6.7B/33B',
    license: 'MIT', status: 'online', downloads: 8900, rating: 4.8,
    dna: generateDNA('HEART-TALK', 'MODEL-DS-Coder'), mcpSupport: true,
    localInstall: 'lmstudio 搜索 DeepSeek-Coder', requirements: '16GB+ RAM推荐',
    apiEndpoint: 'http://localhost:1234',
  },
  // 云端模型
  {
    id: 'model-kimi-moonshot', name: 'Kimi Moonshot', provider: 'kimi', type: 'cloud',
    description: 'Moonshot AI 出品，长文本处理能力突出，支持200万字上下文',
    version: 'v1.5', tags: ['llm', '长文本', '国产'], parameters: '???',
    license: '商用API', status: 'online', downloads: 999999, rating: 4.5,
    dna: generateDNA('HEART-TALK', 'MODEL-Kimi'), mcpSupport: false,
    apiEndpoint: 'https://api.moonshot.cn/v1',
  },
  {
    id: 'model-deepseek-chat', name: 'DeepSeek-V3', provider: 'deepseek', type: 'cloud',
    description: '深度求索最新大模型，推理能力强，性价比高',
    version: 'v3', tags: ['llm', '推理', '国产'], parameters: '671B(MoE)',
    license: '商用API', status: 'online', downloads: 999999, rating: 4.7,
    dna: generateDNA('HEART-TALK', 'MODEL-DS-V3'), mcpSupport: false,
    apiEndpoint: 'https://api.deepseek.com/v1',
  },
  {
    id: 'model-qwen-max', name: '通义千问-Max', provider: 'tongyi', type: 'cloud',
    description: '阿里云旗舰大模型，综合能力全面，企业级服务',
    version: 'qwen-max', tags: ['llm', '企业', '国产'], parameters: '???',
    license: '商用API', status: 'online', downloads: 999999, rating: 4.4,
    dna: generateDNA('HEART-TALK', 'MODEL-QwenMax'), mcpSupport: false,
    apiEndpoint: 'https://dashscope.aliyuncs.com/api',
  },
  {
    id: 'model-claude', name: 'Claude 4', provider: 'claude', type: 'cloud',
    description: 'Anthropic出品，安全性和推理能力顶尖，国际兜底模型',
    version: '4', tags: ['llm', '安全', '国际'], parameters: '???',
    license: '商用API', status: 'online', downloads: 999999, rating: 4.6,
    dna: generateDNA('HEART-TALK', 'MODEL-Claude4'), mcpSupport: false,
    apiEndpoint: 'https://api.anthropic.com',
  },
  // 龍魂系统模型
  {
    id: 'model-longhun-core', name: '龍魂核心引擎', provider: 'longhun-core', type: 'longhun',
    description: '龍魂系统自主可控AI核心，基于三层监督+三色审计+DNA追溯的治理架构',
    version: 'v5.0', tags: ['龍魂', '主权AI', '治理'], parameters: ' proprietary',
    license: '龍魂君子协议', status: 'online', downloads: 9622, rating: 5.0,
    dna: generateDNA('HEART-TALK', 'MODEL-LongHun-Core'), mcpSupport: true,
    apiEndpoint: 'http://api.longhun.local/v1',
  },
  {
    id: 'model-longhun-nlp', name: '龍文NLP', provider: 'longhun-nlp', type: 'longhun',
    description: '中文优先NLP引擎，CNSH术语支持，通心译双语映射',
    version: 'v3.0', tags: ['龍魂', '中文NLP', 'CNSH'], parameters: ' proprietary',
    license: '龍魂君子协议', status: 'beta', downloads: 4800, rating: 4.8,
    dna: generateDNA('HEART-TALK', 'MODEL-LongHun-NLP'), mcpSupport: true,
    apiEndpoint: 'http://api.longhun.local/nlp',
  },
  {
    id: 'model-longhun-asr', name: '龍音ASR', provider: 'longhun-asr', type: 'longhun',
    description: '中文优先语音识别，拼音对齐，四声分类，支持CNSH语音编程',
    version: 'v5.0', tags: ['龍魂', '语音', 'ASR'], parameters: ' proprietary',
    license: '龍魂君子协议', status: 'online', downloads: 3200, rating: 4.6,
    dna: generateDNA('HEART-TALK', 'MODEL-LongHun-ASR'), mcpSupport: true,
    apiEndpoint: 'http://api.longhun.local/asr',
  },
  {
    id: 'model-longhun-ocr', name: '龍瞳OCR', provider: 'longhun-ocr', type: 'longhun',
    description: '中文优先图像识别，龍字专用检测，甲骨文字符分类',
    version: 'v2.0', tags: ['龍魂', 'OCR', '图像'], parameters: ' proprietary',
    license: '龍魂君子协议', status: 'online', downloads: 2800, rating: 4.5,
    dna: generateDNA('HEART-TALK', 'MODEL-LongHun-OCR'), mcpSupport: true,
    apiEndpoint: 'http://api.longhun.local/ocr',
  },
];

// ─── 广场仓库 ───
export const PLAZA_REPOS: PlazaRepo[] = [
  {
    id: 'repo-001', name: 'longhun-system', description: '龍魂系统 · 25核心模块 · 13,800+行代码 · 三层监督+三色审计+DNA全链路追溯',
    url: 'https://github.com/UID9622/longhun-system', category: 'governance',
    language: 'Python', stars: 1, forks: 0, contributors: 1, updated: '2026-06-28',
    dna: generateDNA('HEART-TALK', 'REPO-longhun-system'), owner: 'UID9622',
    tags: ['AI治理', '审计框架', '主权AI'], license: 'CC BY-NC-SA 4.0', authRequired: false,
  },
  {
    id: 'repo-002', name: 'longhun-calendar', description: '龍魂万年历 · 自主字体/算法/本地运行 · 农历/节气/卦象/主权审计',
    url: 'https://github.com/UID9622/longhun-calendar', category: 'calendar',
    language: 'JavaScript', stars: 0, forks: 0, contributors: 1, updated: '2026-06-27',
    dna: generateDNA('HEART-TALK', 'REPO-longhun-calendar'), owner: 'UID9622',
    tags: ['万年历', '节气', '卦象'], license: '龍魂君子协议', authRequired: false,
  },
  {
    id: 'repo-003', name: 'longhun-kimi-skills', description: '龍魂Kimi技能集：中文原生数字生态、三色审计、DNA追溯、通心译',
    url: 'https://github.com/UID9622/longhun-kimi-skills', category: 'dev-tool',
    language: 'Python', stars: 0, forks: 0, contributors: 1, updated: '2026-06-18',
    dna: generateDNA('HEART-TALK', 'REPO-longhun-kimi-skills'), owner: 'UID9622',
    tags: ['Kimi', '技能集', '开发工具'], license: '龍魂君子协议', authRequired: false,
  },
  {
    id: 'repo-004', name: 'LonghunFont', description: '龍魂字体 · 自主可控中文字体基础设施',
    url: 'https://github.com/UID9622/LonghunFont', category: 'font',
    language: 'HTML', stars: 0, forks: 0, contributors: 1, updated: '2026-06-23',
    dna: generateDNA('HEART-TALK', 'REPO-LonghunFont'), owner: 'UID9622',
    tags: ['字体', '中文', '基础设施'], license: 'OFL-1.1', authRequired: false,
  },
  {
    id: 'repo-005', name: 'longhun-evidence-matrix', description: '龍魂取证矩阵 · Evidence Matrix for CNSH-SGR Runtime',
    url: 'https://github.com/UID9622/longhun-evidence-matrix', category: 'security',
    language: 'Python', stars: 0, forks: 0, contributors: 1, updated: '2026-05-21',
    dna: generateDNA('HEART-TALK', 'REPO-evidence-matrix'), owner: 'UID9622',
    tags: ['取证', '安全', '审计'], license: '龍魂君子协议', authRequired: true,
  },
  {
    id: 'repo-006', name: 'cnsh-spec', description: 'CNSH中文原生脚本规范 v3.0 · L1-L7完整层级 · 中文编程宪章',
    url: 'https://github.com/UID9622/cnsh-spec', category: 'cnsh',
    language: 'Markdown', stars: 0, forks: 0, contributors: 1, updated: '2026-06-20',
    dna: generateDNA('HEART-TALK', 'REPO-cnsh-spec'), owner: 'UID9622',
    tags: ['CNSH', '中文编程', '规范'], license: 'CC BY-NC-SA 4.0', authRequired: false,
  },
  {
    id: 'repo-007', name: 'longhun-editor', description: '龍魂编辑器 · CNSH语法高亮 · 中文变量名支持 · DNA追溯集成',
    url: 'https://github.com/UID9622/longhun-editor', category: 'editor',
    language: 'TypeScript', stars: 0, forks: 0, contributors: 1, updated: '2026-06-25',
    dna: generateDNA('HEART-TALK', 'REPO-longhun-editor'), owner: 'UID9622',
    tags: ['编辑器', 'CNSH', 'IDE'], license: '龍魂君子协议', authRequired: false,
  },
  {
    id: 'repo-008', name: 'heart-talk-protocol', description: '龍之心语社交协议 · 加密群聚 · DNA追溯 · 三色审计 · 本地优先',
    url: 'https://github.com/UID9622/heart-talk-protocol', category: 'community',
    language: 'TypeScript', stars: 0, forks: 0, contributors: 1, updated: '2026-06-28',
    dna: generateDNA('HEART-TALK', 'REPO-heart-talk'), owner: 'UID9622',
    tags: ['社交协议', '加密', '主权'], license: '龍魂君子协议', authRequired: false,
  },
];

// ─── 贡献者 ───
export const CONTRIBUTORS: Contributor[] = [
  { uid: 'UID9622', name: '龍芯北辰', avatar: '', contributionScore: 8888, repos: 5, level: 'founder', dna: generateDNA('HEART-TALK', 'CONTRIBUTOR-founder') },
  { uid: 'LH-DEV-042', name: '开发者小易', avatar: '', contributionScore: 1800, repos: 2, level: 'developer', dna: generateDNA('HEART-TALK', 'CONTRIBUTOR-dev042') },
  { uid: 'LH-VET-007', name: '老战友阿强', avatar: '', contributionScore: 4200, repos: 0, level: 'citizen', dna: generateDNA('HEART-TALK', 'CONTRIBUTOR-vet007') },
  { uid: 'LH-KIMI-001', name: 'Kimi智能体', avatar: '', contributionScore: 5000, repos: 0, level: 'maintainer', dna: generateDNA('HEART-TALK', 'CONTRIBUTOR-kimi') },
];

// ─── 授权记录 ───
export const AUTH_GRANTS: AuthGrant[] = [
  { id: 'grant-001', grantee: '开发者小易', granteeUid: 'LH-DEV-042', repo: 'longhun-system', level: 'developer', grantedAt: '2026-03-15', expiresAt: '2027-03-15', dna: generateDNA('HEART-TALK', 'GRANT-dev'), status: 'active', gpgSigned: true },
  { id: 'grant-002', grantee: 'Kimi智能体', granteeUid: 'LH-KIMI-001', repo: 'longhun-system', level: 'maintainer', grantedAt: '2025-06-01', dna: generateDNA('HEART-TALK', 'GRANT-maintainer'), status: 'active', gpgSigned: true },
  { id: 'grant-003', grantee: '龍芯北辰', granteeUid: 'UID9622', repo: '全部仓库', level: 'founder', grantedAt: '2024-01-01', dna: generateDNA('HEART-TALK', 'GRANT-founder'), status: 'active', gpgSigned: true },
];

// ─── API端点 ───
export const API_ENDPOINTS: ApiEndpoint[] = [
  { id: 'api-001', name: '模型列表', method: 'GET', path: '/api/v1/models', description: '获取全部可用AI模型列表', auth: false, dna: generateDNA('HEART-TALK', 'API-MODELS-LIST') },
  { id: 'api-002', name: '模型调用', method: 'POST', path: '/api/v1/models/{id}/chat', description: '调用指定模型进行对话', auth: true, dna: generateDNA('HEART-TALK', 'API-MODEL-CHAT'), example: 'curl -X POST http://api.longhun.local/v1/models/llama3/chat -d {"messages": [...]}' },
  { id: 'api-003', name: 'DNA追溯', method: 'GET', path: '/api/v1/dna/{dna}', description: '根据DNA码追溯完整链路', auth: false, dna: generateDNA('HEART-TALK', 'API-DNA-TRACE') },
  { id: 'api-004', name: '审计日志', method: 'GET', path: '/api/v1/audit', description: '获取三色审计日志', auth: true, dna: generateDNA('HEART-TALK', 'API-AUDIT-LOG') },
  { id: 'api-005', name: 'MCP工具列表', method: 'GET', path: '/api/v1/mcp/tools', description: '获取MCP协议暴露的工具列表', auth: false, dna: generateDNA('HEART-TALK', 'API-MCP-TOOLS') },
  { id: 'api-006', name: '创建房间', method: 'POST', path: '/api/v1/rooms', description: '创建加密对话房间', auth: true, dna: generateDNA('HEART-TALK', 'API-ROOM-CREATE') },
  { id: 'api-007', name: '发送消息', method: 'POST', path: '/api/v1/rooms/{id}/messages', description: '发送带DNA追溯的加密消息', auth: true, dna: generateDNA('HEART-TALK', 'API-MESSAGE-SEND') },
  { id: 'api-008', name: '授权申请', method: 'POST', path: '/api/v1/auth/grant', description: '申请仓库访问授权', auth: true, dna: generateDNA('HEART-TALK', 'API-AUTH-GRANT') },
  { id: 'api-009', name: '广场仓库', method: 'GET', path: '/api/v1/plaza/repos', description: '获取开源广场仓库列表', auth: false, dna: generateDNA('HEART-TALK', 'API-PLAZA-REPOS') },
  { id: 'api-010', name: '贡献者排行', method: 'GET', path: '/api/v1/plaza/contributors', description: '获取贡献者排行榜', auth: false, dna: generateDNA('HEART-TALK', 'API-PLAZA-CONTRIBUTORS') },
];

// ─── 房间数据（保留聊天功能）───
function makeMsg(id: string, roomId: string, sender: User, content: string, audit: '🟢' | '🟡' | '🔴' = '🟢', encrypted = true): Message {
  return {
    id, roomId, sender, content,
    timestamp: getTimestamp(),
    dna: generateDNA('HEART-TALK', `MSG-${id}`),
    audit, encrypted,
    hash: sha256Hash(content + id),
    type: 'text',
  };
}

const roomMsgs: Record<string, Message[]> = {
  room_private: [
    makeMsg('msg-001', 'room_private', CURRENT_USER, '私密小窝已创建。这里只有家人能进，所有消息端侧加密。'),
    makeMsg('msg-002', 'room_private', USER_AI, 'DNA追溯码已生成，房间私钥保存在本地Keychain中。'),
  ],
  room_team: [
    makeMsg('msg-101', 'room_team', USER_DEV, '万年历的节气算法调通了，农历公历对齐率100%！'),
    makeMsg('msg-102', 'room_team', CURRENT_USER, '对接CNSH编辑器的字元渲染层，DNA追溯贯穿每个操作。'),
    makeMsg('msg-103', 'room_team', USER_AI, '三层监督已激活。感知层→认知层→决策层，全流程覆盖。'),
  ],
  room_public: [
    makeMsg('msg-201', 'room_public', CURRENT_USER, '各位龍魂公民，龍之心语公开测试正式开始！'),
    makeMsg('msg-202', 'room_public', USER_VETERAN, '支持！数据主权归人民，不做数据贩子。'),
  ],
  room_intl: [
    makeMsg('msg-301', 'room_intl', USER_AI, 'International channel initialized.', '🟡'),
  ],
};

export const INITIAL_ROOMS: Room[] = [
  { id: 'room_private', name: '北辰之家', type: 'private', dna: generateDNA('HEART-TALK', 'ROOM-private'), creator: CURRENT_USER, members: [CURRENT_USER], messages: roomMsgs['room_private'], createdAt: getTimestamp(), lastActive: getTimestamp(), unreadCount: 0, encrypted: true, auditLevel: '🟢' },
  { id: 'room_team', name: '龍魂开发组', type: 'team', dna: generateDNA('HEART-TALK', 'ROOM-team'), creator: CURRENT_USER, members: [CURRENT_USER, USER_DEV, USER_AI], messages: roomMsgs['room_team'], createdAt: getTimestamp(), lastActive: getTimestamp(), unreadCount: 2, encrypted: true, auditLevel: '🟢' },
  { id: 'room_public', name: '龍魂公民广场', type: 'public', dna: generateDNA('HEART-TALK', 'ROOM-public'), creator: CURRENT_USER, members: [CURRENT_USER, USER_VETERAN, USER_DEV, USER_AI], messages: roomMsgs['room_public'], createdAt: getTimestamp(), lastActive: getTimestamp(), unreadCount: 1, encrypted: false, auditLevel: '🟢' },
  { id: 'room_intl', name: '国际交流通道', type: 'international', dna: generateDNA('HEART-TALK', 'ROOM-intl'), creator: CURRENT_USER, members: [CURRENT_USER, USER_AI], messages: roomMsgs['room_intl'], createdAt: getTimestamp(), lastActive: getTimestamp(), unreadCount: 1, encrypted: true, auditLevel: '🟡' },
];

export const INITIAL_AUDITS: AuditEntry[] = [
  { id: 'a-001', timestamp: getTimestamp(), module: '模型广场', level: '🟢', message: '10个AI模型已加载（本地3/云端4/龍魂3）', dna: generateDNA('HEART-TALK', 'AUDIT-MODELS') },
  { id: 'a-002', timestamp: getTimestamp(), module: '广场仓库', level: '🟢', message: '8个开源仓库已索引，分类完成', dna: generateDNA('HEART-TALK', 'AUDIT-REPOS') },
  { id: 'a-003', timestamp: getTimestamp(), module: '授权管理', level: '🟢', message: '3条授权记录已验证，GPG签名全部有效', dna: generateDNA('HEART-TALK', 'AUDIT-AUTH') },
  { id: 'a-004', timestamp: getTimestamp(), module: 'API网关', level: '🟢', message: '10个API端点已注册，MCP协议就绪', dna: generateDNA('HEART-TALK', 'AUDIT-API') },
  { id: 'a-005', timestamp: getTimestamp(), module: '开发者中心', level: '🟢', message: 'SDK/文档/示例代码已部署', dna: generateDNA('HEART-TALK', 'AUDIT-DEV') },
  { id: 'a-006', timestamp: getTimestamp(), module: '端侧加密', level: '🟢', message: '加密引擎就绪，私钥本地存储', dna: generateDNA('HEART-TALK', 'AUDIT-CRYPTO') },
  { id: 'a-007', timestamp: getTimestamp(), module: '三层监督', level: '🟢', message: '感知/认知/决策三层治理在线', dna: generateDNA('HEART-TALK', 'AUDIT-SUPERVISOR') },
];

export const GITHUB_REPOS: GithubRepo[] = PLAZA_REPOS.map(r => ({
  name: r.name, description: r.description, url: r.url,
  language: r.language, stars: r.stars, updated: r.updated,
}));

export function createMessage(roomId: string, sender: User, content: string, modelId?: string): Message {
  const audit = auditMessage(content);
  return {
    id: `msg-${Date.now()}`, roomId, sender, content,
    timestamp: getTimestamp(),
    dna: generateDNA('HEART-TALK', `MSG-${Date.now()}`),
    audit, encrypted: true,
    hash: sha256Hash(content + Date.now()),
    type: 'text', modelId,
  };
}
