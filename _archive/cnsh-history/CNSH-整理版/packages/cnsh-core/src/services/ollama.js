/**
 * Ollama 服务
 * 与本地 Ollama 服务器通信，处理模型推理
 */

const axios = require('axios');
const Logger = require('../utils/logger');

class OllamaService {
  constructor() {
    this.baseURL = process.env.OLLAMA_HOST || 'http://localhost:11434';
    this.model = process.env.OLLAMA_MODEL || 'qwen:7b-chat';
    this.timeout = parseInt(process.env.OLLAMA_TIMEOUT) || 30;
    this.maxTokens = parseInt(process.env.OLLAMA_MAX_TOKENS) || 2048;
    this.temperature = parseFloat(process.env.OLLAMA_TEMPERATURE) || 0.7;
    this.logger = new Logger('info', './logs/ollama.log');
  }

  /**
   * 初始化 Ollama 服务
   */
  async initialize() {
    try {
      // 检查 Ollama 是否可用
      await this.checkConnection();
      
      // 检查模型是否可用
      await this.checkModel();
      
      this.logger.info(`Ollama service initialized with model: ${this.model}`);
      return true;
    } catch (error) {
      this.logger.error(`Failed to initialize Ollama service: ${error.message}`);
      throw error;
    }
  }

  /**
   * 检查与 Ollama 的连接
   */
  async checkConnection() {
    try {
      const response = await axios.get(`${this.baseURL}/api/tags`, { timeout: 5000 });
      this.logger.info('Ollama connection established');
      return response.data;
    } catch (error) {
      throw new Error(`Cannot connect to Ollama at ${this.baseURL}: ${error.message}`);
    }
  }

  /**
   * 检查指定模型是否可用
   */
  async checkModel() {
    try {
      const response = await axios.get(`${this.baseURL}/api/tags`);
      const models = response.data.models || [];
      
      const modelExists = models.some(model => 
        model.name.includes(this.model.split(':')[0])
      );
      
      if (!modelExists) {
        this.logger.warn(`Model ${this.model} not found. Available models: ${models.map(m => m.name).join(', ')}`);
        throw new Error(`Model ${this.model} not found. Please pull it first: ollama pull ${this.model}`);
      }
      
      this.logger.info(`Model ${this.model} is available`);
      return true;
    } catch (error) {
      throw new Error(`Error checking model: ${error.message}`);
    }
  }

  /**
   * 生成文本
   * @param {string} prompt - 提示词
   * @param {Object} options - 生成选项
   * @returns {Promise<string>} 生成的文本
   */
  async generate(prompt, options = {}) {
    try {
      const requestData = {
        model: this.model,
        prompt,
        stream: false,
        options: {
          temperature: options.temperature || this.temperature,
          top_p: options.topP || 0.9,
          max_tokens: options.maxTokens || this.maxTokens,
          ...options
        }
      };

      this.logger.debug(`Generating text with prompt: ${prompt.substring(0, 100)}...`);
      
      const response = await axios.post(
        `${this.baseURL}/api/generate`,
        requestData,
        { timeout: this.timeout * 1000 }
      );
      
      const result = response.data.response;
      this.logger.debug(`Generated response: ${result.substring(0, 100)}...`);
      
      return result;
    } catch (error) {
      this.logger.error(`Error generating text: ${error.message}`);
      throw new Error(`Failed to generate text: ${error.message}`);
    }
  }

  /**
   * 对话生成
   * @param {Array} messages - 对话消息数组
   * @param {Object} options - 生成选项
   * @returns {Promise<string>} 生成的回复
   */
  async chat(messages, options = {}) {
    try {
      const requestData = {
        model: this.model,
        messages,
        stream: false,
        options: {
          temperature: options.temperature || this.temperature,
          top_p: options.topP || 0.9,
          max_tokens: options.maxTokens || this.maxTokens,
          ...options
        }
      };

      this.logger.debug(`Chat with ${messages.length} messages`);
      
      const response = await axios.post(
        `${this.baseURL}/api/chat`,
        requestData,
        { timeout: this.timeout * 1000 }
      );
      
      const result = response.data.message.content;
      this.logger.debug(`Chat response: ${result.substring(0, 100)}...`);
      
      return result;
    } catch (error) {
      this.logger.error(`Error in chat: ${error.message}`);
      
      // 如果 chat 接口不支持，回退到 generate
      if (error.response && error.response.status === 404) {
        this.logger.warn('Chat endpoint not available, falling back to generate');
        
        // 将消息转换为提示词
        const prompt = messages.map(msg => 
          `${msg.role}: ${msg.content}`
        ).join('\n\n') + '\n\nassistant:';
        
        return this.generate(prompt, options);
      }
      
      throw new Error(`Failed to chat: ${error.message}`);
    }
  }

  /**
   * 获取可用模型列表
   * @returns {Promise<Array>} 模型列表
   */
  async listModels() {
    try {
      const response = await axios.get(`${this.baseURL}/api/tags`);
      return response.data.models || [];
    } catch (error) {
      this.logger.error(`Error listing models: ${error.message}`);
      throw new Error(`Failed to list models: ${error.message}`);
    }
  }

  /**
   * 拉取模型
   * @param {string} modelName - 模型名称
   * @param {Function} onProgress - 进度回调函数
   * @returns {Promise<Object>} 拉取结果
   */
  async pullModel(modelName, onProgress) {
    try {
      this.logger.info(`Starting to pull model: ${modelName}`);
      
      const response = await axios.post(
        `${this.baseURL}/api/pull`,
        { name: modelName },
        { 
          responseType: 'stream',
          timeout: 0 // 设置为0表示无超时，因为下载可能需要很长时间
        }
      );
      
      // 处理流式响应
      return new Promise((resolve, reject) => {
        let responseData = '';
        
        response.data.on('data', (chunk) => {
          try {
            responseData += chunk.toString();
            
            // 尝试解析JSON行
            const lines = responseData.split('\n').filter(line => line.trim());
            const lastLine = lines[lines.length - 1];
            
            if (lastLine) {
              const data = JSON.parse(lastLine);
              
              // 调用进度回调
              if (onProgress && typeof onProgress === 'function') {
                const progress = data.status === 'success' ? 100 : 
                                 (data.total && data.completed) ? 
                                   Math.round((data.completed / data.total) * 100) : 0;
                
                onProgress({
                  status: data.status,
                  progress,
                  total: data.total,
                  completed: data.completed
                });
              }
              
              if (data.status === 'success') {
                resolve(data);
              }
            }
          } catch (parseError) {
            // 继续累积数据，可能JSON不完整
          }
        });
        
        response.data.on('end', () => {
          try {
            // 尝试解析最后的响应
            const data = JSON.parse(responseData);
            resolve(data);
          } catch (error) {
            this.logger.error(`Error parsing pull model response: ${error.message}`);
            reject(new Error(`Failed to pull model: Invalid response`));
          }
        });
        
        response.data.on('error', (error) => {
          this.logger.error(`Error pulling model: ${error.message}`);
          reject(new Error(`Failed to pull model: ${error.message}`));
        });
      });
    } catch (error) {
      this.logger.error(`Error pulling model ${modelName}: ${error.message}`);
      throw new Error(`Failed to pull model ${modelName}: ${error.message}`);
    }
  }

  /**
   * 删除模型
   * @param {string} modelName - 模型名称
   * @returns {Promise<Object>} 删除结果
   */
  async deleteModel(modelName) {
    try {
      this.logger.info(`Deleting model: ${modelName}`);
      
      const response = await axios.delete(`${this.baseURL}/api/delete`, {
        data: { name: modelName }
      });
      
      this.logger.info(`Model ${modelName} deleted successfully`);
      return response.data;
    } catch (error) {
      this.logger.error(`Error deleting model ${modelName}: ${error.message}`);
      throw new Error(`Failed to delete model ${modelName}: ${error.message}`);
    }
  }

  /**
   * 获取模型信息
   * @param {string} modelName - 模型名称
   * @returns {Promise<Object>} 模型信息
   */
  async getModelInfo(modelName) {
    try {
      const response = await axios.post(
        `${this.baseURL}/api/show`,
        { name: modelName }
      );
      
      return response.data;
    } catch (error) {
      this.logger.error(`Error getting model info for ${modelName}: ${error.message}`);
      throw new Error(`Failed to get model info: ${error.message}`);
    }
  }

  /**
   * 嵌入文本
   * @param {string} text - 要嵌入的文本
   * @returns {Promise<Array>} 嵌入向量
   */
  async embed(text) {
    try {
      const response = await axios.post(
        `${this.baseURL}/api/embeddings`,
        {
          model: this.model,
          prompt: text
        }
      );
      
      return response.data.embedding;
    } catch (error) {
      this.logger.error(`Error embedding text: ${error.message}`);
      throw new Error(`Failed to embed text: ${error.message}`);
    }
  }
}

module.exports = OllamaService;