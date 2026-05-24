const sqlite3 = require('sqlite3').verbose();
const fs = require('fs-extra');
const path = require('path');
const { promisify } = require('util');

class EnhancedDatabaseService {
    constructor(config = {}) {
        this.config = {
            dbPath: config.dbPath || './data/databases/sqlite/cnsh.db',
            backupDir: config.backupDir || './data/backups',
            autoBackup: config.autoBackup || true,
            backupInterval: config.backupInterval || 24 * 60 * 60 * 1000, // 24小时
            enableWAL: config.enableWAL !== false,
            enableFTS: config.enableFTS !== false,
            ...config
        };
        
        this.db = null;
        this.backupTimer = null;
        this.isInitialized = false;
    }

    async initialize() {
        try {
            console.log('🗄️ 初始化增强数据库服务...');
            
            // 确保目录存在
            await fs.ensureDir(path.dirname(this.config.dbPath));
            await fs.ensureDir(this.config.backupDir);
            
            // 打开数据库连接
            this.db = new sqlite3.Database(this.config.dbPath);
            
            // 启用WAL模式 (Write-Ahead Logging)
            if (this.config.enableWAL) {
                await this.run('PRAGMA journal_mode = WAL');
                await this.run('PRAGMA synchronous = NORMAL');
                console.log('✅ WAL模式已启用');
            }
            
            // 优化性能设置
            await this.run('PRAGMA cache_size = 10000');
            await this.run('PRAGMA temp_store = MEMORY');
            await this.run('PRAGMA mmap_size = 268435456'); // 256MB
            
            // 启用全文搜索
            if (this.config.enableFTS) {
                await this.enableFullTextSearch();
            }
            
            // 启动自动备份
            if (this.config.autoBackup) {
                this.startAutoBackup();
            }
            
            this.isInitialized = true;
            console.log('✅ 增强数据库服务初始化完成');
            
        } catch (error) {
            console.error('❌ 数据库初始化失败:', error);
            throw error;
        }
    }

    async enableFullTextSearch() {
        try {
            // 为知识库创建全文搜索表
            await this.run(`
                CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts 
                USING fts5(title, content, tags, content=knowledge, content_rowid=id)
            `);
            
            // 创建触发器自动更新全文搜索索引
            await this.run(`
                CREATE TRIGGER IF NOT EXISTS knowledge_fts_insert 
                AFTER INSERT ON knowledge BEGIN
                    INSERT INTO knowledge_fts(rowid, title, content, tags)
                    VALUES (new.id, new.title, new.content, new.tags);
                END
            `);
            
            await this.run(`
                CREATE TRIGGER IF NOT EXISTS knowledge_fts_update 
                AFTER UPDATE ON knowledge BEGIN
                    UPDATE knowledge_fts SET 
                        title = new.title, 
                        content = new.content, 
                        tags = new.tags
                    WHERE rowid = new.id;
                END
            `);
            
            console.log('✅ 全文搜索已启用');
        } catch (error) {
            console.error('⚠️ 全文搜索启用失败:', error);
        }
    }

    async run(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.db.run(sql, params, function(err) {
                if (err) {
                    reject(err);
                } else {
                    resolve({ id: this.lastID, changes: this.changes });
                }
            });
        });
    }

    async get(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.db.get(sql, params, (err, row) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(row);
                }
            });
        });
    }

    async all(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.db.all(sql, params, (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows);
                }
            });
        });
    }

    // 全文搜索
    async searchFTS(query, limit = 20, offset = 0) {
        const sql = `
            SELECT k.*, 
                   rank,
                   snippet(knowledge_fts, 0, '<mark>', '</mark>', '...', 32) as title_snippet,
                   snippet(knowledge_fts, 1, '<mark>', '</mark>', '...', 64) as content_snippet
            FROM knowledge_fts 
            JOIN knowledge k ON knowledge_fts.rowid = k.id
            WHERE knowledge_fts MATCH ?
            ORDER BY rank
            LIMIT ? OFFSET ?
        `;
        return this.all(sql, [query, limit, offset]);
    }

    // 人格相似度搜索
    async searchPersonasByKeywords(keywords, limit = 5) {
        const keywordList = keywords.split(',').map(k => k.trim()).filter(k => k);
        const conditions = keywordList.map(() => 'keywords LIKE ?').join(' OR ');
        const params = keywordList.map(k => `%${k}%`);
        
        const sql = `
            SELECT *, 
                   (CASE 
                        WHEN keywords LIKE ? THEN 10
                        WHEN keywords LIKE ? THEN 5
                        ELSE 1
                   END) as match_score
            FROM personas 
            WHERE ${conditions}
            ORDER BY match_score DESC, level DESC
            LIMIT ?
        `;
        
        return this.all(sql, [...params, limit]);
    }

    // 任务统计
    async getTaskStats() {
        const sql = `
            SELECT 
                status,
                COUNT(*) as count,
                AVG(priority) as avg_priority
            FROM tasks 
            GROUP BY status
        `;
        return this.all(sql);
    }

    // 人格活跃度分析
    async getPersonaActivity(days = 7) {
        const sql = `
            SELECT 
                p.name,
                p.role,
                COUNT(t.id) as task_count,
                AVG(t.priority) as avg_priority,
                MAX(t.created_at) as last_activity
            FROM personas p
            LEFT JOIN tasks t ON (
                t.trigger_persona = p.name OR 
                t.recognized_persona = p.name OR 
                t.executing_persona = p.name
            )
            WHERE t.created_at >= datetime('now', '-${days} days') OR t.created_at IS NULL
            GROUP BY p.id
            ORDER BY task_count DESC, p.level DESC
        `;
        return this.all(sql);
    }

    // 风险分析
    async getRiskAnalysis() {
        const sql = `
            SELECT 
                risk_tags,
                COUNT(*) as audit_count,
                AVG(CASE 
                    WHEN conclusion LIKE '%高风险%' THEN 4
                    WHEN conclusion LIKE '%中风险%' THEN 3
                    WHEN conclusion LIKE '%低风险%' THEN 2
                    ELSE 1
                END) as avg_risk_level
            FROM audits
            WHERE created_at >= datetime('now', '-30 days')
            GROUP BY risk_tags
            ORDER BY avg_risk_level DESC
        `;
        return this.all(sql);
    }

    // 数据库性能分析
    async getPerformanceStats() {
        try {
            const dbSize = await fs.stat(this.config.dbPath);
            const pageCount = await this.get('PRAGMA page_count');
            const pageSize = await this.get('PRAGMA page_size');
            const cacheSize = await this.get('PRAGMA cache_size');
            
            return {
                databaseSize: dbSize.size,
                pageCount: pageCount.page_count,
                pageSize: pageSize.page_size,
                cacheSize: cacheSize.cache_size,
                isWALMode: (await this.get('PRAGMA journal_mode')).journal_mode === 'wal'
            };
        } catch (error) {
            console.error('⚠️ 性能统计获取失败:', error);
            return null;
        }
    }

    // 启动自动备份
    startAutoBackup() {
        if (this.backupTimer) {
            clearInterval(this.backupTimer);
        }
        
        this.backupTimer = setInterval(async () => {
            await this.backup();
        }, this.config.backupInterval);
        
        console.log('✅ 自动备份已启动');
    }

    // 停止自动备份
    stopAutoBackup() {
        if (this.backupTimer) {
            clearInterval(this.backupTimer);
            this.backupTimer = null;
            console.log('⏹️ 自动备份已停止');
        }
    }

    // 备份数据库
    async backup() {
        try {
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const backupPath = path.join(this.config.backupDir, `cnsh_backup_${timestamp}.db`);
            
            await new Promise((resolve, reject) => {
                this.db.backup(backupPath, (err) => {
                    if (err) {
                        reject(err);
                    } else {
                        resolve();
                    }
                });
            });
            
            console.log(`💾 数据库已备份到: ${backupPath}`);
            
            // 清理旧备份
            await this.cleanupOldBackups();
            
            return backupPath;
        } catch (error) {
            console.error('❌ 数据库备份失败:', error);
            throw error;
        }
    }

    // 清理旧备份
    async cleanupOldBackups() {
        try {
            const files = await fs.readdir(this.config.backupDir);
            const backupFiles = files
                .filter(f => f.startsWith('cnsh_backup_') && f.endsWith('.db'))
                .map(f => ({
                    name: f,
                    path: path.join(this.config.backupDir, f),
                    time: fs.statSync(path.join(this.config.backupDir, f)).mtime
                }))
                .sort((a, b) => b.time - a.time);
            
            // 保留最近30个备份
            const backupsToDelete = backupFiles.slice(30);
            
            for (const backup of backupsToDelete) {
                await fs.remove(backup.path);
                console.log(`🗑️ 已删除旧备份: ${backup.name}`);
            }
        } catch (error) {
            console.error('⚠️ 清理旧备份失败:', error);
        }
    }

    // 数据库维护
    async maintenance() {
        try {
            console.log('🔧 开始数据库维护...');
            
            // 分析表统计信息
            await this.run('ANALYZE');
            
            // 重建索引
            await this.run('REINDEX');
            
            // 清理碎片
            await this.run('VACUUM');
            
            console.log('✅ 数据库维护完成');
        } catch (error) {
            console.error('❌ 数据库维护失败:', error);
            throw error;
        }
    }

    // 关闭数据库连接
    async close() {
        try {
            this.stopAutoBackup();
            
            if (this.db) {
                await new Promise((resolve, reject) => {
                    this.db.close((err) => {
                        if (err) {
                            reject(err);
                        } else {
                            resolve();
                        }
                    });
                });
            }
            
            console.log('📁 数据库连接已关闭');
        } catch (error) {
            console.error('❌ 数据库关闭失败:', error);
            throw error;
        }
    }

    // 事务支持
    async transaction(callback) {
        try {
            await this.run('BEGIN TRANSACTION');
            const result = await callback(this);
            await this.run('COMMIT');
            return result;
        } catch (error) {
            await this.run('ROLLBACK');
            throw error;
        }
    }

    // 批量插入
    async batchInsert(table, records) {
        if (!records.length) return [];
        
        const fields = Object.keys(records[0]);
        const placeholders = fields.map(() => '?').join(',');
        const sql = `INSERT INTO ${table} (${fields.join(',')}) VALUES (${placeholders})`;
        
        const result = [];
        for (const record of records) {
            const values = fields.map(field => record[field]);
            const insertResult = await this.run(sql, values);
            result.push(insertResult);
        }
        
        return result;
    }
}

module.exports = EnhancedDatabaseService;