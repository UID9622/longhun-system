# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 龍之心语 v2.0 · 完整类型系统
// DNA: #龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-LONGHUN-HEART-TALK-v2.0

export type AuditColor = '🟢' | '🟡' | '🔴';
export type RoomType = 'private' | 'team' | 'public' | 'international';
export type ModelType = 'local' | 'cloud' | 'longhun';
export type ModelProvider = 'ollama' | 'lmstudio' | 'kimi' | 'deepseek' | 'tongyi' | 'claude' | 'gpt' | 'longhun-core' | 'longhun-nlp' | 'longhun-asr' | 'longhun-ocr';
export type PageRoute = 'home' | 'plaza' | 'chat' | 'developer' | 'auth' | 'docs' | 'commander' | 'dashboard';
export type PlazaCategory = 'all' | 'ai-model' | 'dev-tool' | 'cnsh' | 'governance' | 'font' | 'calendar' | 'editor' | 'security' | 'community';
export type AuthLevel = 'visitor' | 'citizen' | 'developer' | 'maintainer' | 'guardian' | 'founder';

export interface AuthFactor {
  id: string;
  label: string;
  desc: string;
  icon: string;
}

export interface User {
  uid: string;
  name: string;
  avatar: string;
  creditScore: number;
  contributionScore: number;
  status: 'online' | 'offline' | 'away';
  verified: boolean;
  gpgFingerprint?: string;
  authLevel: AuthLevel;
  joinedAt: string;
  repos: number;
}

export interface AIModel {
  id: string;
  name: string;
  provider: ModelProvider;
  type: ModelType;
  description: string;
  version: string;
  tags: string[];
  parameters: string;
  license: string;
  status: 'online' | 'offline' | 'beta';
  downloads: number;
  rating: number;
  dna: string;
  apiEndpoint?: string;
  mcpSupport: boolean;
  localInstall?: string;
  requirements?: string;
}

export interface Room {
  id: string;
  name: string;
  type: RoomType;
  dna: string;
  creator: User;
  members: User[];
  messages: Message[];
  createdAt: string;
  lastActive: string;
  unreadCount: number;
  encrypted: boolean;
  auditLevel: AuditColor;
  activeModel?: string;
}

export interface Message {
  id: string;
  roomId: string;
  sender: User;
  content: string;
  timestamp: string;
  dna: string;
  audit: AuditColor;
  encrypted: boolean;
  hash: string;
  type: 'text' | 'image' | 'file' | 'voice';
  modelId?: string;
}

export interface AuditEntry {
  id: string;
  timestamp: string;
  module: string;
  level: AuditColor;
  message: string;
  dna: string;
}

export interface PlazaRepo {
  id: string;
  name: string;
  description: string;
  url: string;
  category: PlazaCategory;
  language: string;
  stars: number;
  forks: number;
  contributors: number;
  updated: string;
  dna: string;
  owner: string;
  tags: string[];
  license: string;
  authRequired: boolean;
}

export interface Contributor {
  uid: string;
  name: string;
  avatar: string;
  contributionScore: number;
  repos: number;
  level: AuthLevel;
  dna: string;
}

export interface AuthGrant {
  id: string;
  grantee: string;
  granteeUid: string;
  repo: string;
  level: AuthLevel;
  grantedAt: string;
  expiresAt?: string;
  dna: string;
  status: 'active' | 'expired' | 'revoked';
  gpgSigned: boolean;
}

export interface ApiEndpoint {
  id: string;
  name: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  path: string;
  description: string;
  auth: boolean;
  dna: string;
  example?: string;
}

export interface GithubRepo {
  name: string;
  description: string;
  url: string;
  language: string;
  stars: number;
  updated: string;
}

export const ROOM_TYPE_CONFIG: Record<RoomType, { label: string; icon: string; color: string }> = {
  private:   { label: '私密小窝', icon: '🏠', color: 'text-emerald-400 border-emerald-400/30 bg-emerald-400/5' },
  team:      { label: '工作室',   icon: '⚒️', color: 'text-amber-400 border-amber-400/30 bg-amber-400/5' },
  public:    { label: '公开会议', icon: '🌐', color: 'text-sky-400 border-sky-400/30 bg-sky-400/5' },
  international: { label: '国际通道', icon: '🌍', color: 'text-rose-400 border-rose-400/30 bg-rose-400/5' },
};

export const AUDIT_CONFIG: Record<AuditColor, { label: string; className: string }> = {
  '🟢': { label: '正常通过', className: 'text-green-400 border-green-400/40 bg-green-400/10' },
  '🟡': { label: '警告标记', className: 'text-amber-400 border-amber-400/40 bg-amber-400/10' },
  '🔴': { label: '阻断拦截', className: 'text-red-400 border-red-400/40 bg-red-400/10' },
};

export const MODEL_TYPE_CONFIG: Record<ModelType, { label: string; icon: string; color: string; desc: string }> = {
  local:   { label: '本地模型', icon: '💻', color: 'text-emerald-400 border-emerald-400/30 bg-emerald-400/5', desc: '运行在您的设备上，数据不出境' },
  cloud:   { label: '云端模型', icon: '☁️', color: 'text-sky-400 border-sky-400/30 bg-sky-400/5', desc: '高性能云端API，随时调用' },
  longhun: { label: '龍魂系统', icon: '🐉', color: 'text-amber-400 border-amber-400/30 bg-amber-400/5', desc: '龍魂自主研发，主权可控' },
};

export const PLAZA_CATEGORY_CONFIG: Record<PlazaCategory, { label: string; icon: string }> = {
  all:        { label: '全部', icon: '🔥' },
  'ai-model': { label: 'AI模型', icon: '🤖' },
  'dev-tool': { label: '开发工具', icon: '🔧' },
  cnsh:       { label: 'CNSH语言', icon: '🇨🇳' },
  governance: { label: '治理体系', icon: '⚖️' },
  font:       { label: '字体引擎', icon: '🔤' },
  calendar:   { label: '万年历', icon: '📅' },
  editor:     { label: '编辑器', icon: '✏️' },
  security:   { label: '安全审计', icon: '🛡️' },
  community:  { label: '社区', icon: '👥' },
};

export const AUTH_LEVEL_CONFIG: Record<AuthLevel, { label: string; color: string; desc: string }> = {
  visitor:    { label: '空壳账号', color: 'text-zinc-400', desc: '仅浏览公开内容，无法交互' },
  citizen:    { label: '公民',    color: 'text-sky-400', desc: '可参与对话、广场、评论' },
  developer:  { label: '开发者',  color: 'text-emerald-400', desc: '可接入API/MCP、提交PR、下载SDK' },
  maintainer: { label: '维护者',  color: 'text-amber-400', desc: '可审核代码、管理仓库、查看审计日志' },
  guardian:   { label: '受托者',  color: 'text-purple-400', desc: '七因子全启 · 可参与治理与授权仲裁' },
  founder:    { label: '创始人',  color: 'text-red-400', desc: 'UID9622 · 一票否决 · 最高主权' },
};

export const AUTH_FACTOR_CONFIG: AuthFactor[] = [
  { id: 'password', label: '密码盾', desc: '账号基础密码', icon: 'Lock' },
  { id: 'email',    label: '邮箱锚', desc: '邮箱验证 + 找回', icon: 'Mail' },
  { id: 'phone',    label: '手机链', desc: '手机号 + 短信验证', icon: 'Smartphone' },
  { id: 'gpg',      label: 'GPG印', desc: 'GPG 公钥签名', icon: 'FileSignature' },
  { id: 'hardware', label: '硬件钥', desc: 'YubiKey / 安全芯片', icon: 'KeyRound' },
  { id: 'biometric',label: '生物锁', desc: '指纹 / 面容 / 声纹', icon: 'Fingerprint' },
  { id: 'recovery', label: '见证人', desc: '可信见证人 / 社交恢复', icon: 'Users' },
];

export const AUTH_FEATURE_MAP: Record<AuthLevel, string[]> = {
  visitor:    ['浏览公开文档', '查看模型广场'],
  citizen:    ['加入公开聊天室', '广场评论/点赞', '提交问题反馈'],
  developer:  ['调用 API / MCP', '下载 SDK', '提交 Pull Request', '使用开发者沙盒'],
  maintainer: ['审核代码', '管理仓库权限', '查看审计日志', '发起补丁投票'],
  guardian:   ['参与治理提案', '授权仲裁', '运行监督节点', '发起公投'],
  founder:    ['一票否决', '宪法修改', '核心边界锁定', '最终主权决策'],
};

export const PROVIDER_NAMES: Record<ModelProvider, string> = {
  ollama: 'Ollama',
  lmstudio: 'LM Studio',
  kimi: 'Kimi',
  deepseek: 'DeepSeek',
  tongyi: '通义千问',
  claude: 'Claude',
  gpt: 'GPT',
  'longhun-core': '龍魂核心',
  'longhun-nlp': '龍文NLP',
  'longhun-asr': '龍音ASR',
  'longhun-ocr': '龍瞳OCR',
};
