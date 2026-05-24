/**
 * 数据库服务
 * 管理 CNSH 系统的数据存储
 */

const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs-extra');
const Logger = require('../utils/logger');

class DatabaseService {
  constructor() {
    this.db = null;
    this.dbPath = process.env.DB_PATH || './data/cnsh.db';
    this.logger = new Logger('info', './logs/database.log');
  }

  /**
   * 初始化数据库
   */
  async initialize() {
    try {
      // 确保数据目录存在
      const dbDir = path.dirname(this.dbPath);
      await fs.ensureDir(dbDir);
      
      // 连接数据库
      this.db = new sqlite3.Database(this.dbPath, (err) => {
        if (err) {
          this.logger.error(`Error opening database: ${err.message}`);
          throw err;
        } else {
          this.logger.info(`Connected to SQLite database at ${this.dbPath}`);
        }
      });
      
      // 创建表
      await this.createTables();
      
      this.logger.info('Database initialized successfully');
      return true;
    } catch (error) {
      this.logger.error(`Failed to initialize database: ${error.message}`);
      throw error;
    }
  }

  /**
   * 创建数据库表
   */
  async createTables() {
    return new Promise((resolve, reject) => {
      // 文件表
      const createFilesTable = `
        CREATE TABLE IF NOT EXISTS files (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          path TEXT UNIQUE NOT NULL,
          content TEXT,
          hash TEXT,
          updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
      `;
      
      // 聊天记录表
      const createChatsTable = `
        CREATE TABLE IF NOT EXISTS chats (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id TEXT NOT NULL,
          message TEXT NOT NULL,
          response TEXT NOT NULL,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
      `;
      
      // 知识表
      const createKnowledgeTable = `
        CREATE TABLE IF NOT EXISTS knowledge (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT NOT NULL,
          content TEXT NOT NULL,
          tags TEXT,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
      `;
      
      this.db.serialize(() => {
        this.db.run(createFilesTable);
        this.db.run(createChatsTable);
        this.db.run(createKnowledgeTable, (err) => {
          if (err) {
            reject(err);
          } else {
            resolve();
          }
        });
      });
    });
  }

  /**
   * 更新文件
   */
  async updateFile(filePath, content) {
    return new Promise((resolve, reject) => {
      const hash = this.generateHash(content);
      const sql = `
        INSERT OR REPLACE INTO files (path, content, hash, updated_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
      `;
      
      this.db.run(sql, [filePath, content, hash], function(err) {
        if (err) {
          reject(err);
        } else {
          resolve({ id: this.lastID, updated: true });
        }
      });
    });
  }

  /**
   * 获取文件
   */
  async getFile(filePath) {
    return new Promise((resolve, reject) => {
      const sql = 'SELECT * FROM files WHERE path = ?';
      
      this.db.get(sql, [filePath], (err, row) => {
        if (err) {
          reject(err);
        } else {
          resolve(row);
        }
      });
    });
  }

  /**
   * 保存聊天记录
   */
  async saveChat(userId, message, response) {
    return new Promise((resolve, reject) => {
      const sql = `
        INSERT INTO chats (user_id, message, response)
        VALUES (?, ?, ?)
      `;
      
      this.db.run(sql, [userId, message, response], function(err) {
        if (err) {
          reject(err);
        } else {
          resolve({ id: this.lastID });
        }
      });
    });
  }

  /**
   * 获取聊天历史
   */
  async getChatHistory(userId, limit = 20) {
    return new Promise((resolve, reject) => {
      const sql = `
        SELECT * FROM chats 
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT ?
      `;
      
      this.db.all(sql, [userId, limit], (err, rows) => {
        if (err) {
          reject(err);
        } else {
          resolve(rows.reverse()); // 按时间正序返回
        }
      });
    });
  }

  /**
   * 添加知识
   */
  async addKnowledge(title, content, tags) {
    return new Promise((resolve, reject) => {
      const tagsJson = JSON.stringify(tags || []);
      const sql = `
        INSERT INTO knowledge (title, content, tags)
        VALUES (?, ?, ?)
      `;
      
      this.db.run(sql, [title, content, tagsJson], function(err) {
        if (err) {
          reject(err);
        } else {
          resolve({ id: this.lastID });
        }
      });
    });
  }

  /**
   * 获取知识
   */
  async getKnowledge(id) {
    return new Promise((resolve, reject) => {
      const sql = 'SELECT * FROM knowledge WHERE id = ?';
      
      this.db.get(sql, [id], (err, row) => {
        if (err) {
          reject(err);
        } else if (row) {
          // 解析标签
          try {
            row.tags = JSON.parse(row.tags);
          } catch (e) {
            row.tags = [];
          }
          resolve(row);
        } else {
          resolve(null);
        }
      });
    });
  }

  /**
   * 搜索知识
   */
  async searchKnowledge(query, limit = 10) {
    return new Promise((resolve, reject) => {
      const sql = `
        SELECT * FROM knowledge 
        WHERE title LIKE ? OR content LIKE ?
        ORDER BY updated_at DESC
        LIMIT ?
      `;
      
      const searchTerm = `%${query}%`;
      
      this.db.all(sql, [searchTerm, searchTerm, limit], (err, rows) => {
        if (err) {
          reject(err);
        } else {
          // 解析标签
          rows.forEach(row => {
            try {
              row.tags = JSON.parse(row.tags);
            } catch (e) {
              row.tags = [];
            }
          });
          resolve(rows);
        }
      });
    });
  }

  /**
   * 获取所有文件
   */
  async getAllFiles() {
    return new Promise((resolve, reject) => {
      const sql = 'SELECT * FROM files ORDER BY updated_at DESC';
      
      this.db.all(sql, [], (err, rows) => {
        if (err) {
          reject(err);
        } else {
          resolve(rows);
        }
      });
    });
  }

  /**
   * 删除文件
   */
  async deleteFile(filePath) {
    return new Promise((resolve, reject) => {
      const sql = 'DELETE FROM files WHERE path = ?';
      
      this.db.run(sql, [filePath], function(err) {
        if (err) {
          reject(err);
        } else {
          resolve({ deleted: this.changes > 0 });
        }
      });
    });
  }

  /**
   * 生成简单的哈希值
   */
  generateHash(content) {
    // 使用简单的哈希函数，实际应用中应该使用更安全的哈希算法
    let hash = 0;
    if (content.length === 0) return hash.toString();
    
    for (let i = 0; i < content.length; i++) {
      const char = content.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // 转换为32位整数
    }
    
    return hash.toString();
  }

  /**
   * 关闭数据库连接
   */
  close() {
    if (this.db) {
      this.db.close((err) => {
        if (err) {
          this.logger.error(`Error closing database: ${err.message}`);
        } else {
          this.logger.info('Database connection closed');
        }
      });
    }
  }
}

module.exports = DatabaseService;