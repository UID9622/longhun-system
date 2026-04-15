#!/usr/bin/env python3
"""
CNSH-64 社区桥接模块
连接CNSH护盾与Discuz!社区系统

功能：
1. 信誉分双向同步
2. DNA封禁同步
3. 治理结果同步
4. 交易状态同步

虚拟世界 ←→ 现实接通
"""

import asyncio
import aiohttp
import hashlib
import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('CNSH-Community-Bridge')


@dataclass
class CommunityConfig:
    """社区配置"""
    base_url: str          # Discuz! 站点URL
    api_key: str           # API密钥
    sync_interval: int = 300  # 同步间隔(秒)
    timeout: int = 30      # 请求超时


@dataclass
class ReputationUpdate:
    """信誉更新记录"""
    dna: str
    old_score: float
    new_score: float
    reason: str
    tx_hash: str
    timestamp: float


class CommunityBridge:
    """
    CNSH-64 社区桥接器
    
    实现CNSH护盾与Discuz!社区的双向数据同步
    """
    
    def __init__(self, config: CommunityConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self._sync_task: Optional[asyncio.Task] = None
        self._pending_updates: List[ReputationUpdate] = []
        
    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.config.timeout),
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CNSH-API-Key': self.config.api_key
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self._sync_task:
            self._sync_task.cancel()
            try:
                await self._sync_task
            except asyncio.CancelledError:
                pass
        if self.session:
            await self.session.close()
            
    def _sign_request(self, params: Dict) -> str:
        """生成请求签名"""
        # 按key排序后拼接
        sorted_params = sorted(params.items())
        param_str = '&'.join([f'{k}={v}' for k, v in sorted_params])
        # 添加API密钥签名
        sign_str = f"{param_str}&key={self.config.api_key}"
        return hashlib.sha256(sign_str.encode()).hexdigest()
    
    async def _api_call(self, action: str, params: Dict = None, method: str = 'GET') -> Dict:
        """
        调用社区API
        
        Args:
            action: API动作
            params: 请求参数
            method: HTTP方法
            
        Returns:
            API响应
        """
        if not self.session:
            raise RuntimeError("Bridge not initialized")
            
        url = f"{self.config.base_url}/plugin.php?id=cnsh:api&action={action}"
        
        # 添加API密钥
        params = params or {}
        params['api_key'] = self.config.api_key
        
        try:
            if method.upper() == 'GET':
                async with self.session.get(url, params=params) as resp:
                    result = await resp.json()
            else:
                async with self.session.post(url, data=params) as resp:
                    result = await resp.json()
                    
            if result.get('error'):
                logger.error(f"API错误: {result['error']}")
                return {'success': False, 'error': result['error']}
                
            return result
            
        except Exception as e:
            logger.error(f"API调用失败: {e}")
            return {'success': False, 'error': str(e)}
    
    # ==================== DNA查询 ====================
    
    async def query_dna_bindings(self, dna: str) -> Dict:
        """
        查询DNA绑定的社区身份
        
        Args:
            dna: DNA地址
            
        Returns:
            绑定信息列表
        """
        result = await self._api_call('dna_query', {'dna': dna})
        
        if result.get('success'):
            logger.info(f"查询DNA {dna[:16]}... 成功，找到 {result.get('count', 0)} 个绑定")
        
        return result
    
    # ==================== 信誉同步 ====================
    
    async def sync_reputation(self, dna: str, new_score: float, 
                               reason: str = '', tx_hash: str = '') -> bool:
        """
        同步信誉分到社区
        
        Args:
            dna: DNA地址
            new_score: 新信誉分
            reason: 变动原因
            tx_hash: 链上交易哈希
            
        Returns:
            是否成功
        """
        params = {
            'dna': dna,
            'reputation': new_score,
            'reason': reason,
            'tx_hash': tx_hash
        }
        
        result = await self._api_call('reputation_sync', params, 'POST')
        
        if result.get('success'):
            logger.info(f"信誉同步成功: {dna[:16]}... -> {new_score}")
            return True
        else:
            logger.error(f"信誉同步失败: {result.get('error')}")
            return False
    
    async def batch_sync_reputation(self, updates: List[ReputationUpdate]) -> Dict:
        """
        批量同步信誉分
        
        Args:
            updates: 更新记录列表
            
        Returns:
            同步结果
        """
        updates_data = [
            {
                'dna': u.dna,
                'reputation': u.new_score,
                'reason': u.reason,
                'tx_hash': u.tx_hash
            }
            for u in updates
        ]
        
        params = {
            'updates': json.dumps(updates_data)
        }
        
        result = await self._api_call('batch_reputation_sync', params, 'POST')
        
        if result.get('success'):
            logger.info(f"批量信誉同步完成: {result.get('updated', 0)} 个成功")
        
        return result
    
    def queue_reputation_update(self, update: ReputationUpdate):
        """
        将信誉更新加入队列
        
        Args:
            update: 更新记录
        """
        self._pending_updates.append(update)
        logger.debug(f"信誉更新加入队列: {update.dna[:16]}...")
    
    # ==================== DNA封禁 ====================
    
    async def ban_dna(self, dna: str, reason: str, tx_hash: str = '') -> bool:
        """
        封禁DNA及其所有社区身份
        
        Args:
            dna: DNA地址
            reason: 封禁原因
            tx_hash: 链上交易哈希
            
        Returns:
            是否成功
        """
        params = {
            'dna': dna,
            'reason': reason,
            'tx_hash': tx_hash
        }
        
        result = await self._api_call('ban_dna', params, 'POST')
        
        if result.get('success'):
            affected = result.get('affected_users', 0)
            logger.warning(f"DNA封禁成功: {dna[:16]}... 影响 {affected} 个用户")
            return True
        else:
            logger.error(f"DNA封禁失败: {result.get('error')}")
            return False
    
    # ==================== 统计查询 ====================
    
    async def get_governance_stats(self) -> Dict:
        """获取治理统计"""
        return await self._api_call('governance_stats')
    
    async def get_ecny_stats(self) -> Dict:
        """获取数字人民币统计"""
        return await self._api_call('ecny_stats')
    
    async def health_check(self) -> bool:
        """健康检查"""
        result = await self._api_call('ping')
        if result.get('success'):
            logger.info(f"社区API健康: {result.get('version', 'unknown')}")
            return True
        return False
    
    # ==================== 自动同步 ====================
    
    async def start_auto_sync(self):
        """启动自动同步任务"""
        logger.info(f"启动自动同步，间隔: {self.config.sync_interval}秒")
        self._sync_task = asyncio.create_task(self._sync_loop())
    
    async def _sync_loop(self):
        """同步循环"""
        while True:
            try:
                await self._process_pending_updates()
                await asyncio.sleep(self.config.sync_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"同步循环错误: {e}")
                await asyncio.sleep(60)  # 出错后1分钟重试
    
    async def _process_pending_updates(self):
        """处理待同步的更新"""
        if not self._pending_updates:
            return
            
        # 取出一批更新
        batch_size = 50
        batch = self._pending_updates[:batch_size]
        self._pending_updates = self._pending_updates[batch_size:]
        
        # 批量同步
        result = await self.batch_sync_reputation(batch)
        
        # 如果失败，重新加入队列
        if not result.get('success'):
            logger.warning("批量同步失败，重新加入队列")
            self._pending_updates = batch + self._pending_updates


class CNSHShieldIntegration:
    """
    CNSH护盾集成接口
    
    供CNSH护盾调用，实现与社区的深度集成
    """
    
    def __init__(self, bridge: CommunityBridge):
        self.bridge = bridge
        
    async def on_reputation_changed(self, dna: str, old_score: float, 
                                      new_score: float, reason: str,
                                      tx_hash: str = ''):
        """
        信誉变动回调
        
        当CNSH护盾检测到信誉变动时调用
        """
        update = ReputationUpdate(
            dna=dna,
            old_score=old_score,
            new_score=new_score,
            reason=reason,
            tx_hash=tx_hash,
            timestamp=time.time()
        )
        
        # 加入同步队列
        self.bridge.queue_reputation_update(update)
        
        # 如果是重大变动（降级超过20分），立即同步
        if old_score - new_score >= 20:
            await self.bridge.sync_reputation(dna, new_score, reason, tx_hash)
    
    async def on_dna_banned(self, dna: str, reason: str, tx_hash: str = ''):
        """
        DNA封禁回调
        
        当CNSH护盾封禁DNA时调用
        """
        await self.bridge.ban_dna(dna, reason, tx_hash)
    
    async def on_proposal_executed(self, proposal_id: str, result: Dict):
        """
        提案执行回调
        
        当治理提案被执行时调用
        """
        # 同步治理结果到社区
        logger.info(f"提案执行: {proposal_id}")
    
    async def on_tip_confirmed(self, from_dna: str, to_dna: str, 
                                amount: float, tx_hash: str):
        """
        打赏确认回调
        
        当数字人民币打赏被链上确认时调用
        """
        # 增加双方信誉
        await self.bridge.sync_reputation(
            from_dna, 
            await self._get_reputation(from_dna) + 0.5,
            '打赏他人',
            tx_hash
        )
        await self.bridge.sync_reputation(
            to_dna,
            await self._get_reputation(to_dna) + 1,
            '收到打赏',
            tx_hash
        )
    
    async def _get_reputation(self, dna: str) -> float:
        """获取DNA当前信誉分"""
        # 从CNSH护盾查询
        # 这里需要调用护盾的接口
        return 50.0  # 默认值


# ==================== 使用示例 ====================

async def main():
    """主函数 - 演示用法"""
    
    # 配置
    config = CommunityConfig(
        base_url='http://localhost/discuz',
        api_key='your-api-key-here',
        sync_interval=300
    )
    
    # 创建桥接器
    async with CommunityBridge(config) as bridge:
        # 健康检查
        if await bridge.health_check():
            print("✓ 社区API连接正常")
        else:
            print("✗ 社区API连接失败")
            return
        
        # 查询DNA绑定
        result = await bridge.query_dna_bindings(
            '0x7a3f8c2d9e1b4f5a6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0'
        )
        print(f"DNA绑定查询结果: {result}")
        
        # 同步信誉
        success = await bridge.sync_reputation(
            dna='0x7a3f8c2d9e1b4f5a6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0',
            new_score=75.5,
            reason='社区贡献奖励',
            tx_hash='0xabc123...'
        )
        print(f"信誉同步: {'成功' if success else '失败'}")
        
        # 启动自动同步
        await bridge.start_auto_sync()
        
        # 运行一段时间
        print("自动同步已启动，按Ctrl+C停止...")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n停止同步")


if __name__ == '__main__':
    asyncio.run(main())
