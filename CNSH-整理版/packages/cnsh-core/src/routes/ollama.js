/**
 * Ollama 路由
 * 处理 Ollama 相关的 API 请求
 */

const express = require('express');
const router = express.Router();
const Logger = require('../utils/logger');
const OllamaService = require('../services/ollama');

const logger = new Logger('info', './logs/ollama.log');

/**
 * 获取 Ollama 服务状态
 */
router.get('/status', async (req, res) => {
  try {
    const ollamaService = new OllamaService();
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

/**
 * 生成文本
 */
router.post('/generate', async (req, res) => {
  try {
    const { prompt, options } = req.body;
    
    if (!prompt) {
      return res.status(400).json({
        status: 'error',
        message: 'Missing prompt'
      });
    }
    
    const ollamaService = new OllamaService();
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

/**
 * 对话
 */
router.post('/chat', async (req, res) => {
  try {
    const { messages, options } = req.body;
    
    if (!messages || !Array.isArray(messages)) {
      return res.status(400).json({
        status: 'error',
        message: 'Missing or invalid messages'
      });
    }
    
    const ollamaService = new OllamaService();
    const result = await ollamaService.chat(messages, options);
    
    res.json({
      status: 'ok',
      result,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    logger.error(`Error in chat: ${error.message}`);
    res.status(500).json({
      status: 'error',
      message: error.message
    });
  }
});

/**
 * 获取模型列表
 */
router.get('/models', async (req, res) => {
  try {
    const ollamaService = new OllamaService();
    const models = await ollamaService.listModels();
    
    res.json({
      status: 'ok',
      models
    });
  } catch (error) {
    logger.error(`Error getting models: ${error.message}`);
    res.status(500).json({
      status: 'error',
      message: error.message
    });
  }
});

/**
 * 拉取模型
 */
router.post('/pull', async (req, res) => {
  try {
    const { modelName } = req.body;
    
    if (!modelName) {
      return res.status(400).json({
        status: 'error',
        message: 'Missing modelName'
      });
    }
    
    const ollamaService = new OllamaService();
    
    // 拉取模型可能需要很长时间，我们使用流式响应
    res.writeHead(200, {
      'Content-Type': 'application/json',
      'Transfer-Encoding': 'chunked'
    });
    
    const onProgress = (progress) => {
      res.write(JSON.stringify(progress) + '\n');
    };
    
    const result = await ollamaService.pullModel(modelName, onProgress);
    res.end(JSON.stringify({
      status: 'ok',
      result
    }));
  } catch (error) {
    logger.error(`Error pulling model: ${error.message}`);
    res.status(500).json({
      status: 'error',
      message: error.message
    });
  }
});

module.exports = router;