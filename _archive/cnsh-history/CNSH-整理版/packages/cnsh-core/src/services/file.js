/**
 * 文件服务
 * 处理文件操作和管理
 */

const fs = require('fs-extra');
const path = require('path');
const Logger = require('../utils/logger');

class FileService {
  constructor() {
    this.vaultPath = process.env.OBSIDIAN_VAULT_PATH || '';
    this.logger = new Logger('info', './logs/file.log');
  }

  /**
   * 初始化文件服务
   */
  async initialize() {
    try {
      // 确保必要的目录存在
      const directories = [
        process.env.UPLOAD_DIR || './uploads',
        process.env.TEMP_DIR || './temp',
        './data'
      ];
      
      for (const dir of directories) {
        await fs.ensureDir(dir);
        this.logger.info(`Directory ensured: ${dir}`);
      }
      
      this.logger.info('File service initialized successfully');
      return true;
    } catch (error) {
      this.logger.error(`Failed to initialize file service: ${error.message}`);
      throw error;
    }
  }

  /**
   * 读取文件内容
   */
  async readFile(filePath) {
    try {
      const content = await fs.readFile(filePath, 'utf8');
      return content;
    } catch (error) {
      this.logger.error(`Error reading file ${filePath}: ${error.message}`);
      throw error;
    }
  }

  /**
   * 写入文件内容
   */
  async writeFile(filePath, content) {
    try {
      // 确保目录存在
      await fs.ensureDir(path.dirname(filePath));
      
      // 写入文件
      await fs.writeFile(filePath, content, 'utf8');
      
      this.logger.info(`File written: ${filePath}`);
      return true;
    } catch (error) {
      this.logger.error(`Error writing file ${filePath}: ${error.message}`);
      throw error;
    }
  }

  /**
   * 检查文件是否存在
   */
  async exists(filePath) {
    try {
      return await fs.pathExists(filePath);
    } catch (error) {
      this.logger.error(`Error checking file existence ${filePath}: ${error.message}`);
      return false;
    }
  }

  /**
   * 获取文件信息
   */
  async getFileInfo(filePath) {
    try {
      const stats = await fs.stat(filePath);
      return {
        path: filePath,
        size: stats.size,
        created: stats.birthtime,
        modified: stats.mtime,
        isDirectory: stats.isDirectory(),
        isFile: stats.isFile()
      };
    } catch (error) {
      this.logger.error(`Error getting file info ${filePath}: ${error.message}`);
      throw error;
    }
  }

  /**
   * 获取目录中的所有文件
   */
  async getFilesInDirectory(dirPath, recursive = false) {
    try {
      const files = [];
      
      const traverse = async (currentPath) => {
        const items = await fs.readdir(currentPath);
        
        for (const item of items) {
          const itemPath = path.join(currentPath, item);
          const stats = await fs.stat(itemPath);
          
          if (stats.isDirectory() && recursive) {
            await traverse(itemPath);
          } else if (stats.isFile()) {
            files.push(itemPath);
          }
        }
      };
      
      await traverse(dirPath);
      return files;
    } catch (error) {
      this.logger.error(`Error getting files in directory ${dirPath}: ${error.message}`);
      throw error;
    }
  }

  /**
   * 获取 Obsidian 库中的所有 Markdown 文件
   */
  async getObsidianMarkdownFiles() {
    if (!this.vaultPath) {
      this.logger.warn('Obsidian vault path not configured');
      return [];
    }
    
    try {
      const files = await this.getFilesInDirectory(this.vaultPath, true);
      return files.filter(file => path.extname(file) === '.md');
    } catch (error) {
      this.logger.error(`Error getting Obsidian markdown files: ${error.message}`);
      return [];
    }
  }

  /**
   * 解析 Markdown 文件的 frontmatter
   */
  parseFrontmatter(content) {
    try {
      // 简单的 frontmatter 解析器
      const frontmatterRegex = /^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)$/;
      const match = content.match(frontmatterRegex);
      
      if (match) {
        const frontmatterText = match[1];
        const body = match[2];
        
        // 简单的 YAML 解析器
        const frontmatter = {};
        frontmatterText.split('\n').forEach(line => {
          const colonIndex = line.indexOf(':');
          if (colonIndex > 0) {
            const key = line.substring(0, colonIndex).trim();
            let value = line.substring(colonIndex + 1).trim();
            
            // 移除引号
            if ((value.startsWith('"') && value.endsWith('"')) || 
                (value.startsWith("'") && value.endsWith("'"))) {
              value = value.slice(1, -1);
            }
            
            frontmatter[key] = value;
          }
        });
        
        return {
          frontmatter,
          body
        };
      }
      
      return {
        frontmatter: {},
        body: content
      };
    } catch (error) {
      this.logger.error(`Error parsing frontmatter: ${error.message}`);
      return {
        frontmatter: {},
        body: content
      };
    }
  }

  /**
   * 生成包含 frontmatter 的 Markdown 内容
   */
  generateMarkdown(frontmatter, body) {
    try {
      if (Object.keys(frontmatter).length === 0) {
        return body;
      }
      
      let frontmatterText = '---\n';
      for (const [key, value] of Object.entries(frontmatter)) {
        if (Array.isArray(value)) {
          frontmatterText += `${key}:\n`;
          value.forEach(item => {
            frontmatterText += `  - ${item}\n`;
          });
        } else if (typeof value === 'object') {
          frontmatterText += `${key}:\n`;
          for (const [subKey, subValue] of Object.entries(value)) {
            frontmatterText += `  ${subKey}: ${subValue}\n`;
          }
        } else {
          frontmatterText += `${key}: ${value}\n`;
        }
      }
      frontmatterText += '---\n\n';
      
      return frontmatterText + body;
    } catch (error) {
      this.logger.error(`Error generating markdown: ${error.message}`);
      return body;
    }
  }

  /**
   * 创建临时文件
   */
  async createTempFile(content, extension = '.tmp') {
    try {
      const tempDir = process.env.TEMP_DIR || './temp';
      await fs.ensureDir(tempDir);
      
      const fileName = `${Date.now()}${extension}`;
      const filePath = path.join(tempDir, fileName);
      
      await fs.writeFile(filePath, content, 'utf8');
      
      return filePath;
    } catch (error) {
      this.logger.error(`Error creating temp file: ${error.message}`);
      throw error;
    }
  }

  /**
   * 删除文件
   */
  async deleteFile(filePath) {
    try {
      const exists = await fs.pathExists(filePath);
      if (exists) {
        await fs.remove(filePath);
        this.logger.info(`File deleted: ${filePath}`);
        return true;
      }
      return false;
    } catch (error) {
      this.logger.error(`Error deleting file ${filePath}: ${error.message}`);
      throw error;
    }
  }

  /**
   * 清理临时文件
   */
  async cleanTempFiles(maxAge = 24 * 60 * 60 * 1000) { // 默认24小时
    try {
      const tempDir = process.env.TEMP_DIR || './temp';
      const exists = await fs.pathExists(tempDir);
      
      if (!exists) {
        return;
      }
      
      const files = await fs.readdir(tempDir);
      const now = Date.now();
      
      for (const file of files) {
        const filePath = path.join(tempDir, file);
        const stats = await fs.stat(filePath);
        
        if (now - stats.mtime.getTime() > maxAge) {
          await fs.remove(filePath);
          this.logger.info(`Temp file cleaned: ${filePath}`);
        }
      }
    } catch (error) {
      this.logger.error(`Error cleaning temp files: ${error.message}`);
    }
  }
}

module.exports = FileService;