/**
 * CNSH 核心服务器 - 修复版本
 * 集成 Obsidian 和 Ollama 的知识管理系统
 */

const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs-extra');
const axios = require('axios');
const socketIo = require('socket.io');
const http = require('http');

// 导入环境变量
require('dotenv').config();

// 简单日志工具
const logger = {
  info: (msg) => console.log(`[INFO] ${new Date().toISOString()} ${msg}`),
  error: (msg) => console.error(`[ERROR] ${new Date().toISOString()} ${msg}`),
  debug: (msg) => console.log(`[DEBUG] ${new Date().toISOString()} ${msg}`),
  warn: (msg) => console.warn(`[WARN] ${new Date().toISOString()} ${msg}`)
};

// 初始化应用
const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: process.env.API_CORS_ORIGIN || "*",
    methods: ["GET", "POST"]
  }
});

// 中间件
app.use(cors({
  origin: process.env.API_CORS_ORIGIN || "*",
  credentials: true
}));
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// 静态文件服务
app.use('/static', express.static(path.join(__dirname, '../public')));

// 简单的数据库服务
class SimpleDatabaseService {
  constructor() {
    this.dbPath = process.env.DB_PATH || './data/cnsh.db';
  }

  async initialize() {
    try {
      // 确保数据目录存在
      await fs.ensureDir(path.dirname(this.dbPath));
      logger.info('Simple database initialized');
      return true;
    } catch (error) {
      logger.error(`Failed to initialize database: ${error.message}`);
      throw error;
    }
  }

  async updateFile(filePath, content) {
    // 简化实现，实际应该存储到数据库
    logger.info(`File updated: ${filePath}`);
    return { success: true };
  }

  async saveChat(userId, message, response) {
    // 简化实现，实际应该存储到数据库
    logger.info(`Chat saved for user: ${userId}`);
    return { success: true };
  }
}

// 简单的 Ollama 服务
class SimpleOllamaService {
  constructor() {
    this.baseURL = process.env.OLLAMA_HOST || 'http://localhost:11434';
    this.model = process.env.OLLAMA_MODEL || 'qwen:7b-chat';
  }

  async initialize() {
    try {
      // 检查 Ollama 是否可用
      const response = await axios.get(`${this.baseURL}/api/tags`, { timeout: 5000 });
      logger.info('Ollama service connected');
      return true;
    } catch (error) {
      logger.warn(`Ollama service not available: ${error.message}`);
      // 不要抛出错误，允许系统在没有 Ollama 的情况下运行
      return false;
    }
  }

  async generate(prompt, options = {}) {
    try {
      const requestData = {
        model: this.model,
        prompt,
        stream: false,
        options: {
          temperature: options.temperature || 0.7,
          ...options
        }
      };

      const response = await axios.post(
        `${this.baseURL}/api/generate`,
        requestData,
        { timeout: 30000 }
      );

      return response.data.response;
    } catch (error) {
      logger.error(`Error generating text: ${error.message}`);
      throw error;
    }
  }

  async listModels() {
    try {
      const response = await axios.get(`${this.baseURL}/api/tags`);
      return response.data.models || [];
    } catch (error) {
      logger.error(`Error listing models: ${error.message}`);
      throw error;
    }
  }
}

// 简单的嵌入服务
class SimpleEmbeddingService {
  constructor() {
    this.vectorDbPath = process.env.VECTOR_DB_PATH || './data/vector_db';
  }

  async initialize() {
    try {
      // 确保向量数据库目录存在
      await fs.ensureDir(this.vectorDbPath);
      logger.info('Simple embedding service initialized');
      return true;
    } catch (error) {
      logger.error(`Failed to initialize embedding service: ${error.message}`);
      throw error;
    }
  }

  async embedFile(filePath, content) {
    // 简化实现，实际应该生成向量嵌入
    logger.info(`File embedded: ${filePath}`);
    return { success: true };
  }

  async searchSimilar(query, limit = 5) {
    // 简化实现，实际应该进行向量搜索
    logger.info(`Search query: ${query}`);
    return [];
  }
}

// 初始化服务
let dbService, ollamaService, embeddingService;

// 初始化服务函数
async function initializeServices() {
  try {
    // 初始化数据库服务
    dbService = new SimpleDatabaseService();
    await dbService.initialize();
    
    // 初始化文件服务
    // fileService = new FileService();
    // await fileService.initialize();
    
    // 初始化 Ollama 服务
    ollamaService = new SimpleOllamaService();
    const ollamaAvailable = await ollamaService.initialize();
    
    // 初始化嵌入服务
    embeddingService = new SimpleEmbeddingService();
    await embeddingService.initialize();
    
    logger.info('All services initialized successfully');
    return ollamaAvailable;
  } catch (error) {
    logger.error(`Failed to initialize services: ${error.message}`);
    return false;
  }
}

// API 路由 - Obsidian
app.post('/api/obsidian/upload', async (req, res) => {
  try {
    const { filePath, content } = req.body;
    
    if (!filePath || !content) {
      return res.status(400).json({
        status: 'error',
        message: 'Missing filePath or content'
      });
    }
    
    await dbService.updateFile(filePath, content);
    
    res.json({
      status: 'ok',
      message: 'File uploaded successfully',
      filePath
    });
  } catch (error) {
    logger.error(`Error uploading file: ${error.message}`);
    res.status(500).json({
      status: 'error',
      message: error.message
    });
  }
});

// API 路由 - Ollama
app.get('/api/ollama/status', async (req, res) => {
  try {
    const models = await ollamaService.listModels();
    
    res.json({
      status: 'ok',
      message: 'Ollama service is running',
      models,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    logger.error(`Error getting Ollama status: ${error.message}`);
    res.status(500).json({
      status: 'error',
      message: error.message
    });
  }
});

app.post('/api/ollama/generate', async (req, res) => {
  try {
    const { prompt, options } = req.body;
    
    if (!prompt) {
      return res.status(400).json({
        status: 'error',
        message: 'Missing prompt'
      });
    }
    
    const result = await ollamaService.generate(prompt, options);
    
    res.json({
      status: 'ok',
      result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    logger.error(`Error generating text: ${error.message}`);
    res.status(500).json({
      status: 'error',
      message: error.message
    });
  }
});

// API 路由 - 知识
app.get('/api/knowledge/search', async (req, res) => {
  try {
    const { query, limit = 5 } = req.query;
    
    if (!query) {
      return res.status(400).json({
        status: 'error',
        message: 'Missing query parameter'
      });
    }
    
    const results = await embeddingService.searchSimilar(query, limit);
    
    res.json({
      status: 'ok',
      results,
      total: results.length
    });
  } catch (error) {
    logger.error(`Error searching knowledge: ${error.message}`);
    res.status(500).json({
      status: 'error',
      message: error.message
    });
  }
});

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
      knowledge: '/api/knowledge'
    }
  });
});

// Socket.IO 连接处理
io.on('connection', (socket) => {
  logger.info(`Client connected: ${socket.id}`);
  
  // 处理聊天请求
  socket.on('chat', async (data) => {
    try {
      const { message, userId } = data;
      
      // 调用 Ollama 生成回复
      const response = await ollamaService.generate(message);
      
      // 发送回复
      socket.emit('chat-response', {
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
    logger.info(`File watching configured for ${process.env.OBSIDIAN_VAULT_PATH}`);
  }
});

// 错误处理
process.on('uncaughtException', (error) => {
  logger.error(`Uncaught Exception: ${error.message}`);
  logger.error(error.stack);
});

process.on('unhandledRejection', (reason, promise) => {
  logger.error(`Unhandled Rejection at: ${promise}`);
  logger.error(`Reason: ${reason}`);
});

module.exports = app;