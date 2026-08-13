# idb.js | IndexedDB封装工具

> Notion URL: https://app.notion.com/p/idb-js-IndexedDB-17d252cca3df4983b5ed0349cd58ac9c
> Created: 2025-12-13T05:06:00.000Z
> Last edited: 2026-07-01T13:18:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
DNA确认码：#ZHUGEXIN⚡️2025-LU-SYNC-IDB-JS-V1.0
## 🎯 核心功能
### 数据库设计
- 数据库名：lu_sync_v8_ui
- 版本号：1
- 表结构：
### API接口
- openDB() - 打开/创建数据库
- put(store, obj) - 插入/更新记录
- getAll(store) - 查询所有记录
- get(store, key) - 查询单条记录
## 📋 完整代码
```javascript
// IDB helper for popup — minimal
const IDB = (function(){
  const DB_NAME = 'lu_sync_v8_ui';
  const DB_VERSION = 1;
  let db = null;
  
  async function openDB(){
    if(db) return db;
    return new Promise((resolve,reject)=>{
      const req = indexedDB.open(DB_NAME, DB_VERSION);
      req.onupgradeneeded = (e)=>{
        const d = e.target.result;
        if(!d.objectStoreNames.contains('workers')) 
          d.createObjectStore('workers', { keyPath: 'id' });
        if(!d.objectStoreNames.contains('learningChains')) 
          d.createObjectStore('learningChains', { keyPath: 'id' });
        if(!d.objectStoreNames.contains('errors')) 
          d.createObjectStore('errors', { keyPath: 'id' });
      };
      req.onsuccess = (e)=>{ db = e.target.result; resolve(db); };
      req.onerror = (e)=> reject(e);
    });
  }

  async function put(store, obj){
    const database = await openDB();
    return new Promise((resolve,reject)=>{
      const tx = database.transaction([store], 'readwrite');
      const s = tx.objectStore(store);
      s.put(obj);
      tx.oncomplete = ()=> resolve(obj);
      tx.onerror = (e)=> reject(e);
    });
  }

  async function getAll(store){
    const database = await openDB();
    return new Promise((resolve,reject)=>{
      const tx = database.transaction([store], 'readonly');
      const s = tx.objectStore(store);
      const r = s.getAll();
      r.onsuccess = ()=> resolve(r.result || []);
      r.onerror = (e)=> reject(e);
    });
  }

  async function get(store, key){
    const database = await openDB();
    return new Promise((resolve,reject)=>{
      const tx = database.transaction([store], 'readonly');
      const s = tx.objectStore(store);
      const r = s.get(key);
      r.onsuccess = ()=> resolve(r.result);
      r.onerror = (e)=> reject(e);
    });
  }

  return { openDB, put, getAll, get };
})();
```
## 🔧 使用示例
### 初始化数据库
```javascript
await IDB.openDB();
```
### 插入数据
```javascript
await IDB.put('workers', {
  id: 'w-1',
  name: '任务执行',
  function: '执行天层指令',
  status: '活跃',
  learning_chain: '火',
  color: '#D84315'
});
```
### 查询所有
```javascript
const workers = await IDB.getAll('workers');
console.log(workers);
```
### 查询单条
```javascript
const worker = await IDB.get('workers', 'w-1');
console.log(worker);
```
## 📊 数据结构
### workers表
```javascript
{
  id: string,           // 唯一ID
  name: string,         // Worker名称
  function: string,     // 功能描述
  status: string,       // 状态：活跃/待优化/待处理/空闲
  learning_chain: string, // 五行属性：木/火/土/金/水
  color: string         // 显示颜色（十六进制）
}
```
### learningChains表
```javascript
{
  id: string,           // 唯一ID
  element: string,      // 五行元素
  module: string,       // 模块名称
  chain_desc: string,   // 学习链描述
  status: string,       // 状态emoji
  color: string         // 显示颜色
}
```
### errors表
```javascript
{
  id: string,           // 唯一ID
  timestamp: number,    // 时间戳
  detail: string,       // 错误详情
  refined: boolean      // 是否已炼化
}
```
## ⚡ 技术要点
### 单例模式
- db 变量缓存数据库连接
- 首次调用 openDB() 创建，后续复用
### Promise封装
- 所有IndexedDB异步操作包装为Promise
- 支持async/await语法
### 事务管理
- 写操作：readwrite 事务
- 读操作：readonly 事务
- 自动提交/回滚
### 错误处理
- 所有操作捕获 onerror 事件
- 通过Promise的reject向上抛出
---
创建人：💖 文心（技术归档）
数据架构审核：📊 数据大师 ✅ 通过
