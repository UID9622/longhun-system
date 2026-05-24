// ===== 龍魂存储管理器 =====
// 使用 IndexedDB 实现本地永久存储

window.storageManager = (function() {
  let db = null;
  const DB_NAME = 'DragonSoulDB';
  const DB_VERSION = 2;
  const MEMORY_STORE = 'memories';
  const DNA_STORE = 'dna_records';

  async function init() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, DB_VERSION);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        db = request.result;
        console.log('✅ IndexedDB 初始化成功');
        resolve(db);
      };

      request.onupgradeneeded = (event) => {
        const database = event.target.result;

        if (!database.objectStoreNames.contains(MEMORY_STORE)) {
          const memoryStore = database.createObjectStore(MEMORY_STORE, { keyPath: 'DNA' });
          memoryStore.createIndex('创建时间', '创建时间', { unique: false });
        }

        if (!database.objectStoreNames.contains(DNA_STORE)) {
          const dnaStore = database.createObjectStore(DNA_STORE, { keyPath: 'dna_code' });
          dnaStore.createIndex('timestamp', 'timestamp', { unique: false });
          dnaStore.createIndex('creator', 'creator', { unique: false });
        }
      };
    });
  }

  async function saveMemory(memory) {
    return new Promise((resolve, reject) => {
      const tx = db.transaction(MEMORY_STORE, 'readwrite');
      const store = tx.objectStore(MEMORY_STORE);
      const request = store.put(memory);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async function getMemory(dna) {
    return new Promise((resolve, reject) => {
      const tx = db.transaction(MEMORY_STORE, 'readonly');
      const store = tx.objectStore(MEMORY_STORE);
      const request = store.get(dna);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async function getAllMemories() {
    return new Promise((resolve, reject) => {
      const tx = db.transaction(MEMORY_STORE, 'readonly');
      const store = tx.objectStore(MEMORY_STORE);
      const request = store.getAll();
      request.onsuccess = () => resolve(request.result || []);
      request.onerror = () => reject(request.error);
    });
  }

  async function deleteMemory(dna) {
    return new Promise((resolve, reject) => {
      const tx = db.transaction(MEMORY_STORE, 'readwrite');
      const store = tx.objectStore(MEMORY_STORE);
      const request = store.delete(dna);
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  async function clearAllMemories() {
    return new Promise((resolve, reject) => {
      const tx = db.transaction(MEMORY_STORE, 'readwrite');
      const store = tx.objectStore(MEMORY_STORE);
      const request = store.clear();
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  // DNA 存证相关
  async function saveDNA(record) {
    return new Promise((resolve, reject) => {
      const tx = db.transaction(DNA_STORE, 'readwrite');
      const store = tx.objectStore(DNA_STORE);
      const request = store.put(record);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async function getDNA(dnaCode) {
    return new Promise((resolve, reject) => {
      const tx = db.transaction(DNA_STORE, 'readonly');
      const store = tx.objectStore(DNA_STORE);
      const request = store.get(dnaCode);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async function getAllDNA() {
    return new Promise((resolve, reject) => {
      const tx = db.transaction(DNA_STORE, 'readonly');
      const store = tx.objectStore(DNA_STORE);
      const request = store.getAll();
      request.onsuccess = () => resolve(request.result || []);
      request.onerror = () => reject(request.error);
    });
  }

  async function deleteDNA(dnaCode) {
    return new Promise((resolve, reject) => {
      const tx = db.transaction(DNA_STORE, 'readwrite');
      const store = tx.objectStore(DNA_STORE);
      const request = store.delete(dnaCode);
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  async function clearAllDNA() {
    return new Promise((resolve, reject) => {
      const tx = db.transaction(DNA_STORE, 'readwrite');
      const store = tx.objectStore(DNA_STORE);
      const request = store.clear();
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  return {
    init,
    saveMemory, getMemory, getAllMemories, deleteMemory, clearAllMemories,
    saveDNA, getDNA, getAllDNA, deleteDNA, clearAllDNA
  };
})();
