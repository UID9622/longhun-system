/**
 * CNSH 核心服务器
 * 集成 Obsidian 和 Ollama 的知识管理系统
 */

const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs-extra');
const axios = require('axios');
const { v4: uuidv4 } = require('uuid');
const socketIo = require('socket.io');
const http = require('http');
const chokidar = require('chokidar');
const _ = require('lodash');
const markdown = require('marked');
const DOMPurify = require('isomorphic-dompurify');

// 导入环境变量
require('dotenv').config();

// 导入路由模块
const obsidianRouter = require('./routes/obsidian');
const ollamaRouter = require('./routes/ollama');
const knowledgeRouter = require('./routes/knowledge');

// 导入服务模块
const DatabaseService = require('./services/database');
const FileService = require('./services/file');
const OllamaService = require('./services/ollama');
const EmbeddingService = require('./services/embedding');
const Logger = require('./utils/logger');
const LegalKnowledgeIntegration = require('../legal-knowledge/integration');

// 创建简单日志工具，以防 Logger 类有问题
const simpleLogger = {
  info: (msg) => console.log(`[INFO] ${msg}`),
  error: (msg) => console.error(`[ERROR] ${msg}`),
  debug: (msg) => console.log(`[DEBUG] ${msg}`),
  warn: (msg) => console.warn(`[WARN] ${msg}`)
};

// 初始化应用
const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: process.env.API_CORS_ORIGIN || "http://localhost:3000",
    methods: ["GET", "POST"]
  }
});

// 初始化日志
let logger;
try {
  logger = new Logger(process.env.LOG_LEVEL || 'info', process.env.LOG_FILE || './logs/cnsh.log');
} catch (error) {
  console.warn('Failed to initialize Logger, using simple logger:', error.message);
  logger = simpleLogger;
}

// 中间件
app.use(cors({
  origin: process.env.API_CORS_ORIGIN || "http://localhost:3000",
  credentials: true
}));
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// 静态文件服务
app.use('/static', express.static(path.join(__dirname, '../public')));

// 初始化服务
let dbService, fileService, ollamaService, embeddingService, legalKnowledgeService;

// 初始化数据库
async function initializeServices() {
  try {
    await dbService.initialize();
    await fileService.initialize();
    await ollamaService.initialize();
    await embeddingService.initialize();
    
    // 初始化法律知识库集成
    legalKnowledgeService = new LegalKnowledgeIntegration();
    
    logger.info('All services initialized successfully');
  } catch (error) {
    logger.error(`Failed to initialize services: ${error.message}`);
    process.exit(1);
  }
}

// API 路由
app.use('/api/obsidian', obsidianRouter);
app.use('/api/ollama', ollamaRouter);
app.use('/api/knowledge', knowledgeRouter);

// 健康检查端点
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    version: require('../package.json').version
  });
});

// 法律合规检查API
app.post('/api/legal/compliance', (req, res) => {
  try {
    const { content, countryCode } = req.body;
    
    if (!content) {
      return res.status(400).json({
        error: 'Content is required',
        code: 'MISSING_CONTENT'
      });
    }
    
    if (!legalKnowledgeService) {
      return res.status(503).json({
        error: 'Legal knowledge service not available',
        code: 'SERVICE_UNAVAILABLE'
      });
    }
    
    const complianceResult = legalKnowledgeService.checkContentCompliance(content, countryCode);
    
    res.json({
      success: true,
      result: complianceResult,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    logger.error(`Legal compliance check error: ${error.message}`);
    res.status(500).json({
      error: 'Internal server error',
      code: 'INTERNAL_ERROR'
    });
  }
});

// 获取当前国家法律边界
app.get('/api/legal/boundary', (req, res) => {
  try {
    const countryCode = req.query.country || legalKnowledgeService.currentCountry;
    const legalBoundary = legalKnowledgeService.getLegalBoundary(countryCode);
    const countryProfile = legalKnowledgeService.getCurrentCountryProfile();
    
    res.json({
      success: true,
      currentCountry: countryCode,
      legalBoundary,
      countryProfile,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    logger.error(`Get legal boundary error: ${error.message}`);
    res.status(500).json({
      error: 'Internal server error',
      code: 'INTERNAL_ERROR'
    });
  }
});

// 根路径
app.get('/', (req, res) => {
  res.json({
    name: 'CNSH Server',
    version: require('../package.json').version,
    description: '集成 Obsidian 和 Ollama 的知识管理系统',
    endpoints: {
      health: '/health',
      obsidian: '/api/obsidian',
      ollama: '/api/ollama',
      knowledge: '/api/knowledge',
      legal: '/api/legal'
    }
  });
});

// Socket.IO 连接处理
io.on('connection', (socket) => {
  logger.info(`Client connected: ${socket.id}`);
  
  // 加入房间（基于用户ID）
  socket.on('join', (userId) => {
    socket.join(userId);
    logger.info(`User ${userId} joined room`);
  });
  
  // 处理文件变更事件
  socket.on('file-change', async (data) => {
    try {
      const { filePath, userId } = data;
      const fileContent = await fs.readFile(filePath, 'utf8');
      
      // 更新数据库
      await dbService.updateFile(filePath, fileContent);
      
      // 生成向量嵌入
      await embeddingService.embedFile(filePath, fileContent);
      
      // 通知用户
      socket.to(userId).emit('file-updated', {
        filePath,
        timestamp: new Date().toISOString()
      });
      
      logger.info(`File processed: ${filePath}`);
    } catch (error) {
      logger.error(`Error processing file ${filePath}: ${error.message}`);
      socket.emit('error', { message: error.message });
    }
  });
  
  // 处理聊天请求
  socket.on('chat', async (data) => {
    try {
      const { message, userId, context } = data;
      
      // 获取上下文相关的文档
      const relevantDocs = await embeddingService.searchSimilar(message, 5);
      
      // 构建提示词
      const contextDocs = relevantDocs.map(doc => doc.content).join('\n\n');
      const prompt = `
Context:
${contextDocs}

User message: ${message}

Please respond based on the provided context:
`;
      
      // 调用 Ollama
      const response = await ollamaService.generate(prompt);
      
      // 发送回复
      socket.to(userId).emit('chat-response', {
        message: response,
        timestamp: new Date().toISOString()
      });
      
      // 记录聊天
      await dbService.saveChat(userId, message, response);
      
    } catch (error) {
      logger.error(`Error in chat: ${error.message}`);
      socket.emit('error', { message: error.message });
    }
  });
  
  socket.on('disconnect', () => {
    logger.info(`Client disconnected: ${socket.id}`);
  });
});

// 启动服务器
const PORT = process.env.CNSH_PORT || 3000;
const HOST = process.env.CNSH_HOST || 'localhost';

server.listen(PORT, HOST, async () => {
  logger.info(`CNSH Server running at http://${HOST}:${PORT}`);
  
  // 初始化服务
  await initializeServices();
  
  // 如果配置了 Obsidian 路径，启动文件监控
  if (process.env.OBSIDIAN_VAULT_PATH) {
    const watcher = chokidar.watch(path.join(process.env.OBSIDIAN_VAULT_PATH, '**/*.md'), {
      ignored: /(^|[\/\\])\../, // 忽略隐藏文件
      persistent: true
    });
    
    watcher.on('change', async (filePath) => {
      try {
        const content = await fs.readFile(filePath, 'utf8');
        await dbService.updateFile(filePath, content);
        await embeddingService.embedFile(filePath, content);
        
        // 通知所有连接的客户端
        io.emit('file-changed', {
          filePath,
          timestamp: new Date().toISOString()
        });
        
        logger.info(`File updated: ${filePath}`);
      } catch (error) {
        logger.error(`Error updating file ${filePath}: ${error.message}`);
      }
    });
    
    logger.info(`File watcher started for ${process.env.OBSIDIAN_VAULT_PATH}`);
  }
});

// 错误处理
process.on('uncaughtException', (error) => {
  logger.error(`Uncaught Exception: ${error.message}`);
  logger.error(error.stack);
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  logger.error(`Unhandled Rejection at: ${promise}`);
  logger.error(`Reason: ${reason}`);
});

module.exports = app;