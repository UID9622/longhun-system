/**
 * 嵌入服务
 * 处理文本嵌入和向量搜索功能
 */

const fs = require('fs-extra');
const path = require('path');
const _ = require('lodash');
const Logger = require('../utils/logger');

// 导入向量数据库实现
const VectorDB = require('../utils/vector-db');

class EmbeddingService {
  constructor() {
    this.vectorDb = null;
    this.logger = new Logger('info', './logs/embedding.log');
    this.chunkSize = parseInt(process.env.CHUNK_SIZE) || 512;
    this.chunkOverlap = parseInt(process.env.CHUNK_OVERLAP) || 50;
    this.vectorDbPath = process.env.VECTOR_DB_PATH || './data/vector_db';
  }

  /**
   * 初始化嵌入服务
   */
  async initialize() {
    try {
      // 确保向量数据库目录存在
      await fs.ensureDir(this.vectorDbPath);
      
      // 初始化向量数据库
      this.vectorDb = new VectorDB(this.vectorDbPath);
      await this.vectorDb.initialize();
      
      this.logger.info('Embedding service initialized');
      return true;
    } catch (error) {
      this.logger.error(`Failed to initialize embedding service: ${error.message}`);
      throw error;
    }
  }

  /**
   * 分割文本为小块
   * @param {string} text - 原始文本
   * @returns {Array} 文本块数组
   */
  chunkText(text) {
    // 简单的基于字符数的分块策略
    const chunks = [];
    let start = 0;
    
    while (start < text.length) {
      const end = Math.min(start + this.chunkSize, text.length);
      let chunk = text.substring(start, end);
      
      // 如果不是最后一块，尝试在句子边界处分割
      if (end < text.length) {
        // 寻找最近的句号、问号、感叹号
        const sentenceEnd = Math.max(
          chunk.lastIndexOf('。'),
          chunk.lastIndexOf('？'),
          chunk.lastIndexOf('！'),
          chunk.lastIndexOf('.'),
          chunk.lastIndexOf('?'),
          chunk.lastIndexOf('!')
        );
        
        if (sentenceEnd > start + this.chunkSize / 2) {
          chunk = text.substring(start, sentenceEnd + 1);
          start = sentenceEnd + 1 - this.chunkOverlap;
        } else {
          start = end - this.chunkOverlap;
        }
      } else {
        start = end;
      }
      
      // 跳过空白块
      if (chunk.trim().length > 0) {
        chunks.push(chunk.trim());
      }
    }
    
    return chunks;
  }

  /**
   * 处理并嵌入文件
   * @param {string} filePath - 文件路径
   * @param {string} content - 文件内容
   * @returns {Promise<Array>} 嵌入向量数组
   */
  async embedFile(filePath, content) {
    try {
      this.logger.info(`Embedding file: ${filePath}`);
      
      // 分割文本
      const chunks = this.chunkText(content);
      
      if (chunks.length === 0) {
        this.logger.warn(`No chunks created from file: ${filePath}`);
        return [];
      }
      
      // 为每个块生成嵌入
      const embeddings = [];
      
      for (let i = 0; i < chunks.length; i++) {
        const chunk = chunks[i];
        
        // 生成嵌入向量（这里应该使用实际的嵌入模型，如 sentence-transformers）
        const embedding = await this.generateEmbedding(chunk);
        
        // 存储到向量数据库
        const id = `${filePath}_${i}`;
        const metadata = {
          filePath,
          chunkIndex: i,
          totalChunks: chunks.length,
          preview: chunk.substring(0, 100) + (chunk.length > 100 ? '...' : '')
        };
        
        await this.vectorDb.add(id, embedding, metadata);
        
        embeddings.push({
          id,
          embedding,
          content: chunk,
          metadata
        });
      }
      
      this.logger.info(`Generated ${embeddings.length} embeddings for file: ${filePath}`);
      return embeddings;
    } catch (error) {
      this.logger.error(`Error embedding file ${filePath}: ${error.message}`);
      throw error;
    }
  }

  /**
   * 生成文本嵌入向量
   * @param {string} text - 要嵌入的文本
   * @returns {Promise<Array>} 嵌入向量
   */
  async generateEmbedding(text) {
    // 这里应该调用实际的嵌入模型
    // 作为示例，我们使用一个简单的随机向量
    // 在实际实现中，您应该：
    // 1. 使用 sentence-transformers 模型
    // 2. 或者调用 OpenAI/其他嵌入 API
    // 3. 或者使用本地嵌入模型
    
    // 示例实现：使用 Ollama 的嵌入功能（如果支持）
    try {
      // 如果 Ollama 支持嵌入，可以使用以下代码：
      // const ollamaService = require('./ollama');
      // const embedding = await ollamaService.embed(text);
      // return embedding;
      
      // 临时随机向量实现（仅用于演示）
      const dimension = 384; // 常见的嵌入维度
      const vector = Array.from({ length: dimension }, () => Math.random());
      
      // 归一化向量
      const magnitude = Math.sqrt(vector.reduce((sum, val) => sum + val * val, 0));
      return vector.map(val => val / magnitude);
    } catch (error) {
      this.logger.error(`Error generating embedding: ${error.message}`);
      throw error;
    }
  }

  /**
   * 搜索相似文档
   * @param {string} query - 查询文本
   * @param {number} limit - 返回结果数量
   * @returns {Promise<Array>} 相似文档列表
   */
  async searchSimilar(query, limit = 5) {
    try {
      this.logger.info(`Searching similar documents for query: ${query.substring(0, 100)}...`);
      
      // 生成查询嵌入
      const queryEmbedding = await this.generateEmbedding(query);
      
      // 在向量数据库中搜索
      const results = await this.vectorDb.search(queryEmbedding, limit);
      
      this.logger.info(`Found ${results.length} similar documents`);
      return results;
    } catch (error) {
      this.logger.error(`Error searching similar documents: ${error.message}`);
      throw error;
    }
  }

  /**
   * 根据文件路径获取文档块
   * @param {string} filePath - 文件路径
   * @returns {Promise<Array>} 文档块列表
   */
  async getDocumentChunks(filePath) {
    try {
      const pattern = `${filePath}_*`;
      const results = await this.vectorDb.getByPattern(pattern);
      
      // 按块索引排序
      const sortedChunks = _.sortBy(results, result => result.metadata.chunkIndex);
      
      return sortedChunks.map(result => ({
        id: result.id,
        content: result.content,
        metadata: result.metadata
      }));
    } catch (error) {
      this.logger.error(`Error getting document chunks for ${filePath}: ${error.message}`);
      throw error;
    }
  }

  /**
   * 删除文件的所有嵌入
   * @param {string} filePath - 文件路径
   * @returns {Promise<boolean>} 是否成功删除
   */
  async deleteFileEmbeddings(filePath) {
    try {
      this.logger.info(`Deleting embeddings for file: ${filePath}`);
      
      // 获取所有相关嵌入
      const pattern = `${filePath}_*`;
      const embeddings = await this.vectorDb.getByPattern(pattern);
      
      // 删除每个嵌入
      for (const embedding of embeddings) {
        await this.vectorDb.delete(embedding.id);
      }
      
      this.logger.info(`Deleted ${embeddings.length} embeddings for file: ${filePath}`);
      return true;
    } catch (error) {
      this.logger.error(`Error deleting embeddings for file ${filePath}: ${error.message}`);
      throw error;
    }
  }

  /**
   * 重建整个向量数据库
   * @param {string} directory - 目录路径
   * @returns {Promise<boolean>} 是否成功重建
   */
  async rebuildIndex(directory) {
    try {
      this.logger.info(`Rebuilding vector index for directory: ${directory}`);
      
      // 清空现有数据库
      await this.vectorDb.clear();
      
      // 递归获取所有文件
      const files = await this.getAllMarkdownFiles(directory);
      
      // 处理每个文件
      for (const file of files) {
        try {
          const content = await fs.readFile(file, 'utf8');
          await this.embedFile(file, content);
        } catch (error) {
          this.logger.error(`Error processing file ${file}: ${error.message}`);
          // 继续处理其他文件
        }
      }
      
      this.logger.info(`Vector index rebuilt successfully with ${files.length} files`);
      return true;
    } catch (error) {
      this.logger.error(`Error rebuilding vector index: ${error.message}`);
      throw error;
    }
  }

  /**
   * 递归获取目录中的所有 Markdown 文件
   * @param {string} directory - 目录路径
   * @returns {Promise<Array>} 文件路径数组
   */
  async getAllMarkdownFiles(directory) {
    const files = [];
    
    async function traverse(dir) {
      const items = await fs.readdir(dir);
      
      for (const item of items) {
        const itemPath = path.join(dir, item);
        const stats = await fs.stat(itemPath);
        
        if (stats.isDirectory()) {
          await traverse(itemPath);
        } else if (stats.isFile() && path.extname(itemPath) === '.md') {
          files.push(itemPath);
        }
      }
    }
    
    await traverse(directory);
    return files;
  }

  /**
   * 获取向量数据库统计信息
   * @returns {Promise<Object>} 统计信息
   */
  async getStats() {
    try {
      const stats = await this.vectorDb.getStats();
      return stats;
    } catch (error) {
      this.logger.error(`Error getting vector database stats: ${error.message}`);
      throw error;
    }
  }
}

module.exports = EmbeddingService;