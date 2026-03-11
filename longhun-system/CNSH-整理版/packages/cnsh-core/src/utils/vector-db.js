/**
 * 简单的向量数据库实现
 * 用于存储和搜索向量嵌入
 */

const fs = require('fs-extra');
const path = require('path');
const Logger = require('./logger');

class VectorDB {
  constructor(dbPath = './data/vector_db') {
    this.dbPath = dbPath;
    this.logger = new Logger('info', './logs/vector-db.log');
    this.vectors = new Map();
    this.index = null;
  }

  /**
   * 初始化向量数据库
   */
  async initialize() {
    try {
      // 确保数据库目录存在
      await fs.ensureDir(this.dbPath);
      
      // 加载现有数据
      await this.loadData();
      
      this.logger.info('Vector database initialized');
      return true;
    } catch (error) {
      this.logger.error(`Failed to initialize vector database: ${error.message}`);
      throw error;
    }
  }

  /**
   * 加载数据
   */
  async loadData() {
    try {
      const dataPath = path.join(this.dbPath, 'vectors.json');
      const exists = await fs.pathExists(dataPath);
      
      if (exists) {
        const data = await fs.readJson(dataPath);
        this.vectors = new Map(data.vectors || []);
        this.logger.info(`Loaded ${this.vectors.size} vectors from disk`);
      }
    } catch (error) {
      this.logger.error(`Error loading vector data: ${error.message}`);
    }
  }

  /**
   * 保存数据
   */
  async saveData() {
    try {
      const dataPath = path.join(this.dbPath, 'vectors.json');
      const data = {
        vectors: Array.from(this.vectors.entries()),
        updated_at: new Date().toISOString()
      };
      
      await fs.writeJson(dataPath, data);
      this.logger.debug('Vector data saved to disk');
    } catch (error) {
      this.logger.error(`Error saving vector data: ${error.message}`);
    }
  }

  /**
   * 添加向量
   */
  async add(id, vector, metadata = {}) {
    try {
      // 验证向量
      if (!Array.isArray(vector) || vector.length === 0) {
        throw new Error('Vector must be a non-empty array');
      }
      
      // 归一化向量
      const normalizedVector = this.normalizeVector(vector);
      
      // 添加到内存
      this.vectors.set(id, {
        id,
        vector: normalizedVector,
        metadata
      });
      
      // 保存到磁盘
      await this.saveData();
      
      this.logger.debug(`Vector added: ${id}`);
      return true;
    } catch (error) {
      this.logger.error(`Error adding vector ${id}: ${error.message}`);
      throw error;
    }
  }

  /**
   * 获取向量
   */
  get(id) {
    return this.vectors.get(id);
  }

  /**
   * 更新向量
   */
  async update(id, vector, metadata = {}) {
    try {
      // 归一化向量
      const normalizedVector = this.normalizeVector(vector);
      
      // 更新内存
      if (this.vectors.has(id)) {
        this.vectors.set(id, {
          id,
          vector: normalizedVector,
          metadata: { ...this.vectors.get(id).metadata, ...metadata }
        });
        
        // 保存到磁盘
        await this.saveData();
        
        this.logger.debug(`Vector updated: ${id}`);
        return true;
      } else {
        throw new Error(`Vector with id ${id} not found`);
      }
    } catch (error) {
      this.logger.error(`Error updating vector ${id}: ${error.message}`);
      throw error;
    }
  }

  /**
   * 删除向量
   */
  async delete(id) {
    try {
      const deleted = this.vectors.delete(id);
      
      if (deleted) {
        // 保存到磁盘
        await this.saveData();
        this.logger.debug(`Vector deleted: ${id}`);
      }
      
      return deleted;
    } catch (error) {
      this.logger.error(`Error deleting vector ${id}: ${error.message}`);
      throw error;
    }
  }

  /**
   * 搜索相似向量
   */
  async search(queryVector, limit = 5) {
    try {
      // 归一化查询向量
      const normalizedQuery = this.normalizeVector(queryVector);
      
      // 计算相似度
      const similarities = [];
      
      for (const [id, data] of this.vectors.entries()) {
        const similarity = this.cosineSimilarity(normalizedQuery, data.vector);
        similarities.push({
          id,
          similarity,
          metadata: data.metadata
        });
      }
      
      // 按相似度排序
      similarities.sort((a, b) => b.similarity - a.similarity);
      
      // 返回最相似的结果
      return similarities.slice(0, limit);
    } catch (error) {
      this.logger.error(`Error searching vectors: ${error.message}`);
      throw error;
    }
  }

  /**
   * 根据模式获取向量
   */
  async getByPattern(pattern) {
    try {
      const regex = new RegExp(pattern);
      const results = [];
      
      for (const [id, data] of this.vectors.entries()) {
        if (regex.test(id)) {
          results.push({
            id,
            vector: data.vector,
            metadata: data.metadata
          });
        }
      }
      
      return results;
    } catch (error) {
      this.logger.error(`Error getting vectors by pattern: ${error.message}`);
      throw error;
    }
  }

  /**
   * 清空数据库
   */
  async clear() {
    try {
      this.vectors.clear();
      await this.saveData();
      this.logger.info('Vector database cleared');
      return true;
    } catch (error) {
      this.logger.error(`Error clearing vector database: ${error.message}`);
      throw error;
    }
  }

  /**
   * 获取统计信息
   */
  async getStats() {
    return {
      vectorCount: this.vectors.size,
      dbPath: this.dbPath,
      dimensions: this.vectors.size > 0 ? 
        Array.from(this.vectors.values())[0].vector.length : 0
    };
  }

  /**
   * 归一化向量
   */
  normalizeVector(vector) {
    // 计算向量的模长
    const magnitude = Math.sqrt(vector.reduce((sum, val) => sum + val * val, 0));
    
    // 避免除以零
    if (magnitude === 0) {
      return vector;
    }
    
    // 归一化
    return vector.map(val => val / magnitude);
  }

  /**
   * 计算余弦相似度
   */
  cosineSimilarity(vectorA, vectorB) {
    // 确保向量长度相同
    if (vectorA.length !== vectorB.length) {
      throw new Error('Vectors must have the same dimensions');
    }
    
    // 计算点积
    let dotProduct = 0;
    for (let i = 0; i < vectorA.length; i++) {
      dotProduct += vectorA[i] * vectorB[i];
    }
    
    // 由于向量已经归一化，点积就是余弦相似度
    return dotProduct;
  }

  /**
   * 计算欧几里得距离
   */
  euclideanDistance(vectorA, vectorB) {
    if (vectorA.length !== vectorB.length) {
      throw new Error('Vectors must have the same dimensions');
    }
    
    let sumOfSquares = 0;
    for (let i = 0; i < vectorA.length; i++) {
      const diff = vectorA[i] - vectorB[i];
      sumOfSquares += diff * diff;
    }
    
    return Math.sqrt(sumOfSquares);
  }
}

module.exports = VectorDB;