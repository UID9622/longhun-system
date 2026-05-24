/**
 * Obsidian 路由
 * 处理 Obsidian 插件相关的 API 请求
 */

const express = require('express');
const router = express.Router();
const Logger = require('../utils/logger');

const logger = new Logger('info', './logs/obsidian.log');

/**
 * 获取 Obsidian 插件状态
 */
router.get('/status', (req, res) => {
  try {
    res.json({
      status: 'ok',
      message: 'Obsidian API is running',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    logger.error(`Error getting Obsidian status: ${error.message}`);
    res.status(500).json({
      status: 'error',
      message: error.message
    });
  }
});

/**
 * 上传文件到 CNSH 系统
 */
router.post('/upload', async (req, res) => {
  try {
    const { filePath, content } = req.body;
    
    if (!filePath || !content) {
      return res.status(400).json({
        status: 'error',
        message: 'Missing filePath or content'
      });
    }
    
    // 这里应该调用文件服务和嵌入服务
    logger.info(`File uploaded: ${filePath}`);
    
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

/**
 * 获取文件内容
 */
router.get('/file/:path(*)', async (req, res) => {
  try {
    const filePath = req.params.path;
    
    // 这里应该从数据库或文件系统获取文件内容
    logger.info(`File requested: ${filePath}`);
    
    res.json({
      status: 'ok',
      filePath,
      content: 'File content placeholder'
    });
  } catch (error) {
    logger.error(`Error getting file ${filePath}: ${error.message}`);
    res.status(500).json({
      status: 'error',
      message: error.message
    });
  }
});

/**
 * 搜索文件
 */
router.get('/search', async (req, res) => {
  try {
    const { query, limit = 10 } = req.query;
    
    if (!query) {
      return res.status(400).json({
        status: 'error',
        message: 'Missing query parameter'
      });
    }
    
    // 这里应该调用搜索服务
    logger.info(`Search query: ${query}`);
    
    res.json({
      status: 'ok',
      results: [],
      total: 0
    });
  } catch (error) {
    logger.error(`Error searching files: ${error.message}`);
    res.status(500).json({
      status: 'error',
      message: error.message
    });
  }
});

module.exports = router;