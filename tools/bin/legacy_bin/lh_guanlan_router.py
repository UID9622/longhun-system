#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
观澜浏览器联动路由引擎 v1.0 · GuanLan Router Engine
═══════════════════════════════════════════════════════════
DNA: #龍芯⚡️丙午·乙未·丙申·申时·☴巽-GUANLAN-ROUTER-ENGINE-V1.0-P0-9ce4d2b9
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

八模块：
  M1 模型路由 · M2 断路器 · M3 AI标注 · M4 接口槽注册
  M5 插件审计 · M6 人机两本账 · M7 网关健康 · M8 隐私出域闸门
"""

import time
import hashlib
import json
import re
from typing import Dict, List, Optional, Tuple, Any, Callable
from enum import Enum
from dataclasses import dataclass, field

# ═══════════════════════════════════════════════════════════
# 枚举与数据类
# ═══════════════════════════════════════════════════════════

class 任务类型(Enum):
    代码 = "代码"
    长文档 = "长文档"
    隐私 = "隐私"
    通用 = "通用"
    语音入口 = "语音入口"
    研究 = "研究"
    摘要 = "摘要"
    审查 = "审查"
    编码辅助 = "编码辅助"


class 审计色(Enum):
    绿 = "🟢"
    黄 = "🟡"
    红 = "🔴"


class 引擎位置(Enum):
    本地 = "本地"
    云 = "云"


@dataclass
class AI标注结果:
    """M3: AI Truth Protocol — 每段AI输出必须自报家门"""
    引擎名: str
    版本: str
    生成时间: float
    位置: 引擎位置
    置信度: float = 1.0
    信级: 审计色 = 审计色.绿
    
    def 标注字符串(self) -> str:
        loc = "云" if self.位置 == 引擎位置.云 else "本地"
        return (f"[{self.引擎名}·{self.版本}·{loc}·"
                f"信{self.信级.value}·{time.strftime('%H:%M', time.localtime(self.生成时间))}]")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "引擎": self.引擎名, "版本": self.版本,
            "时间": int(self.生成时间), "位置": self.位置.value,
            "信级": self.信级.value, "置信": self.置信度
        }


@dataclass
class 路由结果:
    """M1: 模型路由输出"""
    引擎: str
    标注: AI标注结果
    转移记录: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        d = {"引擎": self.引擎, "标注": self.标注.to_dict()}
        if self.转移记录:
            d["转移"] = self.转移记录
        return d


@dataclass
class 注册结果:
    """M4: 接口槽注册结果"""
    过: bool
    状态: str
    原因: Optional[str] = None


@dataclass
class 插件审计结果:
    """M5: 插件权限审计"""
    过: bool
    状态: str
    违规权限: List[str] = field(default_factory=list)


@dataclass
class 出域闸门结果:
    """M8: 隐私出域扫描"""
    过: bool
    状态: str
    命中模式: List[str] = field(default_factory=list)
    脱敏后文本: Optional[str] = None


# ═══════════════════════════════════════════════════════════
# 配置常量
# ═══════════════════════════════════════════════════════════

# M1 默认路由表（任务类型 → 首选引擎）
默认路由: Dict[str, str] = {
    "代码": "CodeBuddy", "长文档": "Kimi", "隐私": "Ollama",
    "通用": "Ollama", "语音入口": "小艺", "研究": "Kimi",
    "摘要": "Ollama", "审查": "CodeBuddy", "编码辅助": "CodeBuddy",
}

# M1 故障转移链
转移链: Dict[str, str] = {
    "Kimi": "Ollama", "CodeBuddy": "Ollama",
    "小艺": "Ollama",  # 小艺是入口，推理转移Ollama
}

# M1 永不出机的任务类型
本地锁定任务: set[str] = {"隐私", "离线"}

# M2 断路器参数
熔断阈值: int = 3         # 连续失败次数
熔断冷却秒: int = 600     # 10分钟冷却
熔断审计链: List[Dict] = []  # 审计记录

# M5 插件敏感权限
插件敏感权限: set[str] = {"读历史", "改页面", "发网络", "读书签", "读Cookie", "注入脚本"}

# M8 隐私模式（正则，不存日志）
隐私模式列表: List[Tuple[str, str]] = [
    (r'\d{6}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]', '身份证'),
    (r'1[3-9]\d{9}', '手机号'),
    (r'[1-9]\d{5}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]', '身份证(旧格式)'),
    (r'\d{16,19}', '银行卡号'),
    (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '邮箱'),
    (r'(?:北京|上海|广州|深圳|杭州|成都|武汉|南京|重庆|天津|苏州|西安|长沙|青岛|大连|厦门|宁波|郑州|济南|'
     r'合肥|福州|东莞|佛山|无锡|昆明|沈阳|哈尔滨|温州|石家庄|泉州|南宁|长春|'
     r'潍坊|烟台|保定|南昌|贵阳|太原|兰州|乌鲁木齐|呼和浩特|银川|西宁|拉萨|海口)'
     r'(?:市)?(?:[\\u4e00-\\u9fff]{2,}(?:区|县|路|街|镇|村|弄|巷|号|楼|层|室|栋|单元))', '详细地址'),
]


# ═══════════════════════════════════════════════════════════
# M1 模型路由引擎
# ═══════════════════════════════════════════════════════════

class CNSH_模型路由:
    """
    观澜浏览器核心路由：任务分型 → 引擎选择 → 断路器检查 → 返回标注
    """
    
    def __init__(self):
        self.自定义路由: Dict[str, str] = {}
    
    def 路由(self, 任务: str, 断路器=None, 引擎状态: Dict[str, bool] = None,
             用户偏好: str = None, 强制本地: bool = False) -> 路由结果:
        """
        主路由方法。
        
        参数:
            任务: 任务类型描述 ("代码"/"长文档"/"隐私"/"通用"/"语音入口")
            断路器: CNSH_断路器实例（可选，无则跳过）
            引擎状态: {引擎名: 是否在线} 字典
            用户偏好: 用户手动选择的引擎名
            强制本地: 是否强制使用本地引擎
        
        返回: 路由结果（引擎名+标注）
        """
        转移记录 = None
        
        # Step 1: 用户显式偏好优先（但隐私任务覆盖）
        if 任务 in 本地锁定任务 or 强制本地:
            引擎 = "Ollama"
        elif 用户偏好 and 用户偏好 in 默认路由.values():
            引擎 = 用户偏好
        else:
            # Step 2: 查默认路由表
            引擎 = self.自定义路由.get(任务) or 默认路由.get(任务, "Ollama")
        
        # Step 3: 语音入口特殊处理（小艺是入口，推理走路由）
        if 引擎 == "小艺" and 任务 != "语音入口":
            # 小艺→文字后，按任务类型重路由
            引擎 = 默认路由.get(任务, "Ollama")
        
        # Step 4: 隐私任务绝对锁定本地
        if 任务 in 本地锁定任务 and 引擎 != "Ollama":
            转移记录 = f"隐私任务强制本地: {引擎}→Ollama"
            引擎 = "Ollama"
        
        # Step 5: 断路器检查
        if 断路器:
            if not 断路器.可用(引擎):
                备选 = 转移链.get(引擎)
                if 备选:
                    转移记录 = f"断路器: {引擎}熔断中→{备选}"
                    引擎 = 备选
        
        # Step 6: 引擎离线检查
        if 引擎状态 and not 引擎状态.get(引擎, True):
            备选 = 转移链.get(引擎)
            if 备选 and 引擎状态.get(备选, True):
                转移记录 = (转移记录 or "") + f" 离线转移: {引擎}→{备选}"
                引擎 = 备选
        
        # Step 7: 生成AI标注
        位置 = 引擎位置.本地 if 引擎 in ("Ollama", "CodeBuddy") else 引擎位置.云
        标注 = AI标注结果(引擎名=引擎, 版本="v1.0", 生成时间=time.time(), 位置=位置)
        
        return 路由结果(引擎=引擎, 标注=标注, 转移记录=转移记录)
    
    def 设置自定义路由(self, 任务: str, 引擎: str):
        """用户自定义路由规则"""
        self.自定义路由[任务] = 引擎
    
    def 重置自定义路由(self):
        self.自定义路由.clear()


# ═══════════════════════════════════════════════════════════
# M2 断路器引擎
# ═══════════════════════════════════════════════════════════

class CNSH_断路器:
    """观澜断路器：引擎连续失败→自动熔断→冷却恢复"""
    
    def __init__(self):
        self.失败计数: Dict[str, int] = {}
        self.熔断时间: Dict[str, float] = {}
        self.审计链: List[Dict] = []
    
    def 可用(self, 引擎: str) -> bool:
        """检查引擎是否可用（未熔断或已冷却）"""
        if 引擎 not in self.熔断时间:
            return True
        已冷却 = time.time() - self.熔断时间[引擎] > 熔断冷却秒
        if 已冷却:
            # 自动恢复
            del self.熔断时间[引擎]
            self.失败计数[引擎] = 0
            self._审计(引擎, "自动恢复")
        return 已冷却
    
    def 记失败(self, 引擎: str, 原因: str = "") -> bool:
        """
        记录一次失败。返回 True 表示触发熔断。
        """
        self.失败计数[引擎] = self.失败计数.get(引擎, 0) + 1
        当前计数 = self.失败计数[引擎]
        
        if 当前计数 >= 熔断阈值:
            self.熔断时间[引擎] = time.time()
            self.失败计数[引擎] = 0
            self._审计(引擎, f"熔断触发(连续{熔断阈值}次失败): {原因}")
            return True
        
        self._审计(引擎, f"失败({当前计数}/{熔断阈值}): {原因}")
        return False
    
    def 记成功(self, 引擎: str):
        """成功调用→重置计数器"""
        if 引擎 in self.失败计数:
            self.失败计数[引擎] = 0
    
    def 状态(self, 引擎: str | None = None) -> Dict[str, Any]:
        """查询断路器状态"""
        if 引擎:
            return {
                "引擎": 引擎,
                "失败数": self.失败计数.get(引擎, 0),
                "熔断中": 引擎 in self.熔断时间,
                "剩余冷却秒": max(0, 熔断冷却秒 - (time.time() - self.熔断时间.get(引擎, 0))) if 引擎 in self.熔断时间 else 0,
            }
        return {
            e: self.状态(e) for e in set(list(self.失败计数.keys()) + list(self.熔断时间.keys()))
        }
    
    def _审计(self, 引擎: str, 事件: str):
        entry = {"时间": int(time.time()), "引擎": 引擎, "事件": 事件}
        self.审计链.append(entry)
        熔断审计链.append(entry)
    
    def 审计报告(self) -> List[Dict]:
        return self.审计链[-50:]  # 最近50条


# ═══════════════════════════════════════════════════════════
# M3 AI标注器
# ═══════════════════════════════════════════════════════════

def CNSH_AI标注(引擎: str, 版本: str = "v1.0", 云: bool = False,
               置信度: float = 1.0) -> AI标注结果:
    """
    AI Truth Protocol: 每段AI输出必须自报家门。
    未标注的输出默认降信🟡。
    """
    位置 = 引擎位置.云 if 云 else 引擎位置.本地
    
    # 置信度映射信级
    if 置信度 >= 0.85:
        信级 = 审计色.绿
    elif 置信度 >= 0.60:
        信级 = 审计色.黄
    else:
        信级 = 审计色.红
    
    return AI标注结果(
        引擎名=引擎, 版本=版本, 生成时间=time.time(),
        位置=位置, 置信度=置信度, 信级=信级
    )


def CNSH_标注验证(标注: AI标注结果, 最小置信: float = 0.60) -> Tuple[bool, str]:
    """
    验证AI标注是否合规。缺标注或低置信→降信。
    """
    if not 标注 or not 标注.引擎名:
        return False, "🟡 缺标注，默认降信一级"
    if 标注.置信度 < 最小置信:
        return False, f"🟡 置信度{标注.置信度:.2f}<{最小置信}，降信"
    return True, "🟢 标注合规"


# ═══════════════════════════════════════════════════════════
# M4 接口槽注册引擎
# ═══════════════════════════════════════════════════════════

class CNSH_接口槽:
    """
    预留AI引擎槽：新引擎注册→三锚核验→接口实现检查→注册。
    """
    
    def __init__(self):
        self.已注册引擎: Dict[str, Dict] = {}
        self.已注册插件: Dict[str, Dict] = {}
    
    def 注册AI引擎(self, 名: str, 三锚: Dict[str, Any], 接口实现) -> 注册结果:
        """
        注册新AI引擎到引擎槽。
        
        三锚要求:
            dna: DNA追溯码
            gate: 已过GATE闸口验证
            seal: 签章验证通过
        接口要求:
            ask(任务: str) -> {回答: str, 引擎: str, 版本: str, 置信: float}
        """
        # 检查三锚
        missing = []
        for k in ("dna", "gate", "seal"):
            if not 三锚.get(k):
                missing.append(k)
        if missing:
            return 注册结果(过=False, 状态=f"🔴 三锚缺{missing}，拒注册")
        
        # 检查接口
        if not callable(接口实现):
            return 注册结果(过=False, 状态="🔴 未实现ask接口")
        
        # 检查接口签名
        try:
            test_result = 接口实现("__health_check__")
            if not isinstance(test_result, dict):
                return 注册结果(过=False, 状态="🔴 ask接口返回值不是dict")
            required = {"回答", "引擎", "版本", "置信"}
            if not required.issubset(test_result.keys()):
                return 注册结果(过=False, 状态=f"🔴 ask返回值缺少字段{required-set(test_result.keys())}")
        except Exception as e:
            return 注册结果(过=False, 状态=f"🔴 ask接口调用失败: {e}")
        
        # 注册
        self.已注册引擎[名] = {
            "名": 名, "三锚": 三锚, "注册时间": int(time.time()),
            "DNA": 三锚.get("dna"), "状态": "🟢"
        }
        return 注册结果(过=True, 状态=f"🟢 引擎槽注册：{名}")
    
    def 注销引擎(self, 名: str) -> bool:
        if 名 in self.已注册引擎:
            self.已注册引擎[名]["状态"] = "🔴 已注销"
            return True
        return False
    
    def 引擎列表(self) -> List[Dict]:
        return list(self.已注册引擎.values())


# ═══════════════════════════════════════════════════════════
# M5 插件审计引擎
# ═══════════════════════════════════════════════════════════

class CNSH_插件审计:
    """插件权限审计：敏感权限≥2 → 🔴拒装"""
    
    def 审查(self, 权限: List[str]) -> 插件审计结果:
        """
        审查插件申请的权限清单。
        
        规则: 敏感权限（读历史/改页面/发网络/读书签/读Cookie/注入脚本）
              命中 ≥2 即拒装。
        """
        敏感 = 插件敏感权限
        命中 = [p for p in 权限 if p in 敏感]
        
        if len(命中) >= 2:
            return 插件审计结果(
                过=False, 状态=f"🔴 敏感权限≥2({len(命中)}项)，拒装",
                违规权限=命中
            )
        elif len(命中) == 1:
            return 插件审计结果(
                过=True, 状态=f"🟡 1项敏感权限({命中[0]})，已标记",
                违规权限=命中
            )
        else:
            return 插件审计结果(过=True, 状态="🟢 权限审查通过")
    
    def 签名校验(self, 插件签名: str, 已知公钥: str) -> bool:
        """插件签名核验（简化版，生产环境用GPG/SM2）"""
        # 生产环境：用 subprocess 调 gpg --verify
        return hashlib.sha256(插件签名.encode()).hexdigest()[:16] == 已知公钥[:16]


# ═══════════════════════════════════════════════════════════
# M6 人机两本账引擎
# ═══════════════════════════════════════════════════════════

class CNSH_两本账:
    """
    人机两本账：浏览器阅览=人工账，侦察蚁抓取=爬虫账。
    合显看板。
    """
    
    def __init__(self):
        self.账: Dict[str, int] = {"人工": 0, "爬虫": 0}
        self.日明细: List[Dict] = []
    
    def 记(self, 侧: str, n: int = 1, url: str = "", 时间戳: float | None = None):
        """
        记一笔账。
        
        参数:
            侧: "人工" 或 "爬虫"
            n: 数量
            url: 来源URL（可选）
        """
        if 侧 not in self.账:
            raise ValueError(f"账本侧 '{侧}' 无效，仅支持 '人工'/'爬虫'")
        self.账[侧] += n
        self.日明细.append({
            "侧": 侧, "数量": n, "url": url,
            "时间": int(时间戳 or time.time())
        })
    
    def 看板(self) -> str:
        """合显看板"""
        总计 = self.账["人工"] + self.账["爬虫"]
        if 总计 == 0:
            return "人工账:0 ｜ 爬虫账:0 ｜ 总计:0"
        人比 = self.账["人工"] / 总计 * 100
        return (f"人工账:{self.账['人工']}({人比:.0f}%) ｜ "
                f"爬虫账:{self.账['爬虫']}({100-人比:.0f}%) ｜ 总计:{总计}")
    
    def 看板JSON(self) -> Dict[str, Any]:
        return {
            "人工": self.账["人工"],
            "爬虫": self.账["爬虫"],
            "总计": self.账["人工"] + self.账["爬虫"],
            "明细": self.日明细[-100:],  # 最近100条
        }
    
    def 清零(self):
        self.账 = {"人工": 0, "爬虫": 0}
        self.日明细.clear()


# ═══════════════════════════════════════════════════════════
# M7 网关健康检查
# ═══════════════════════════════════════════════════════════

class CNSH_网关:
    """龍魂网关健康检查：网关挂=浏览器拒绝联网（fail-closed）"""
    
    def __init__(self, 检查函数: Callable[[], bool] = None):
        self._检查 = 检查函数 or (lambda: True)
        self._上次状态: bool = True
        self._状态历史: List[Dict] = []
    
    def 活(self) -> bool:
        """检查网关是否存活"""
        try:
            self._上次状态 = self._检查()
        except Exception:
            self._上次状态 = False
        
        self._状态历史.append({
            "时间": int(time.time()),
            "状态": self._上次状态,
        })
        # 只保留最近100条
        if len(self._状态历史) > 100:
            self._状态历史 = self._状态历史[-100:]
        
        return self._上次状态
    
    def 联网状态(self) -> Dict[str, Any]:
        """返回联网决策"""
        网关活 = self.活()
        return {
            "联网": 网关活,
            "状态": "🟢 网关正常" if 网关活 else "🔴 fail-closed 拒绝联网",
            "上次检查": self._状态历史[-1] if self._状态历史 else None,
        }
    
    def 状态历史(self) -> List[Dict]:
        return self._状态历史


# ═══════════════════════════════════════════════════════════
# M8 隐私出域闸门
# ═══════════════════════════════════════════════════════════

class CNSH_出域闸门:
    """
    隐私出域扫描：文本离机前扫描敏感信息。
    命中→脱敏或拦截🔴。
    """
    
    def 扫描(self, 文本: str, 策略: str = "脱敏") -> 出域闸门结果:
        """
        扫描文本中的敏感信息。
        
        参数:
            文本: 待扫描文本
            策略: "脱敏"（默认，替换为***）或 "拦截"（直接拒绝）
        
        返回: 扫描结果
        """
        命中 = []
        for pattern, name in 隐私模式列表:
            if re.search(pattern, 文本):
                命中.append(name)
        
        if not 命中:
            return 出域闸门结果(过=True, 状态="🟢 隐私扫描通过")
        
        if 策略 == "拦截":
            return 出域闸门结果(
                过=False, 状态=f"🔴 隐私扫描拦截: {','.join(命中)}",
                命中模式=命中
            )
        
        # 脱敏策略
        脱敏后 = 文本
        for pattern, name in 隐私模式列表:
            脱敏后 = re.sub(pattern, f'[***{name}***]', 脱敏后)
        
        return 出域闸门结果(
            过=True, 状态=f"🟡 已脱敏: {','.join(命中)}",
            命中模式=命中, 脱敏后文本=脱敏后
        )
    
    def 快速检查(self, 文本: str) -> bool:
        """快速检查是否有敏感信息（True=安全，False=有敏感）"""
        return self.扫描(文本).过


# ═══════════════════════════════════════════════════════════
# M9 多模型对比引擎（GAP-04落地）
# ═══════════════════════════════════════════════════════════

@dataclass
class 对比结果:
    问题: str
    回答A: Dict  # {引擎, 回答, 标注}
    回答B: Dict[str, Any]
    分歧点: List[str] = field(default_factory=list)
    共识度: float = 0.0


class CNSH_多模型对比:
    """
    同一问题并排调两个引擎，分歧点高亮——兼听则明。
    """
    
    def 对比(self, 问题: str, 回答A: Dict[str, Any], 回答B: Dict[str, Any]) -> 对比结果:
        """
        对比两个引擎对同一问题的回答。
        
        参数:
            问题: 用户问题
            回答A: {引擎, 回答, 标注}
            回答B: {引擎, 回答, 标注}
        
        返回: 对比结果（含分歧点和共识度）
        """
        分歧点 = self._找分歧(回答A.get("回答", ""), 回答B.get("回答", ""))
        
        # 简单共识度：基于回答长度和分歧点数量的启发式
        len_a = len(回答A.get("回答", ""))
        len_b = len(回答B.get("回答", ""))
        if len_a == 0 and len_b == 0:
            共识度 = 1.0
        else:
            分歧权重 = len(分歧点) * 0.1
            长度差 = abs(len_a - len_b) / max(len_a, len_b, 1) * 0.2
            共识度 = max(0.0, min(1.0, 1.0 - 分歧权重 - 长度差))
        
        return 对比结果(
            问题=问题, 回答A=回答A, 回答B=回答B,
            分歧点=分歧点, 共识度=共识度
        )
    
    def _找分歧(self, a: str, b: str) -> List[str]:
        """找两个回答之间的关键分歧点"""
        分歧 = []
        # 简单启发式：按句分拆，找关键词矛盾
        import difflib
        a_sents = re.split(r'[。！？\n]', a)
        b_sents = re.split(r'[。！？\n]', b)
        
        # 用difflib找差异句子
        matcher = difflib.SequenceMatcher(None, a_sents, b_sents)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag in ('replace', 'insert'):
                分歧.append(f"A说: {';'.join(a_sents[i1:i2])} | B说: {';'.join(b_sents[j1:j2])}")
        
        return 分歧[:5]  # 最多5个分歧点


# ═══════════════════════════════════════════════════════════
# 统一入口：观澜总控
# ═══════════════════════════════════════════════════════════

class 观澜总控:
    """观澜浏览器统一控制台：一站式初始化所有模块"""
    
    def __init__(self):
        self.路由 = CNSH_模型路由()
        self.断路器 = CNSH_断路器()
        self.接口槽 = CNSH_接口槽()
        self.插件审 = CNSH_插件审计()
        self.账本 = CNSH_两本账()
        self.网关 = CNSH_网关()
        self.闸门 = CNSH_出域闸门()
        self.对比 = CNSH_多模型对比()
    
    def 处理请求(self, 任务: str, 用户偏好: str | None = None,
                强制本地: bool = False) -> 路由结果:
        """
        一站式处理用户AI请求：路由→断路器→标注。
        """
        return self.路由.路由(
            任务=任务, 断路器=self.断路器,
            用户偏好=用户偏好, 强制本地=强制本地
        )
    
    def 状态报告(self) -> Dict[str, Any]:
        """生成完整的观澜状态报告"""
        return {
            "网关": self.网关.联网状态(),
            "断路器": self.断路器.状态(),
            "账本": self.账本.看板JSON(),
            "已注册引擎": len(self.接口槽.已注册引擎),
            "已注册插件": len(self.接口槽.已注册插件),
            "审计链长度": len(熔断审计链),
        }


# ═══════════════════════════════════════════════════════════
# 测试向量（12条 = 第九章T01-T12）
# ═══════════════════════════════════════════════════════════

测试向量: List[Dict] = [
    {"id": "T01", "场景": "代码任务", "任务": "代码", "期望引擎": "CodeBuddy"},
    {"id": "T02", "场景": "长文档解析", "任务": "长文档", "期望引擎": "Kimi"},
    {"id": "T03", "场景": "隐私内容摘要", "任务": "隐私", "期望引擎": "Ollama"},
    {"id": "T04", "场景": "Kimi连续3次失败→断路器转移", "动作": "断路器"},
    {"id": "T05", "场景": "鸿蒙语音入口", "任务": "语音入口", "期望引擎": "小艺"},
    {"id": "T06", "场景": "AI回答无标注→降信", "动作": "标注验证"},
    {"id": "T07", "场景": "网页命中敏感→闸门拦截", "动作": "闸门"},
    {"id": "T08", "场景": "网关进程被杀→fail-closed", "动作": "网关"},
    {"id": "T09", "场景": "新AI注册缺三锚→拒", "动作": "注册"},
    {"id": "T10", "场景": "插件索取三项敏感权限→拒装", "动作": "插件审计"},
    {"id": "T11", "场景": "浏览100页/蚁爬50页→分列", "动作": "账本"},
    {"id": "T12", "场景": "断网→本地功能可用", "动作": "综合"},
]

def 跑测试() -> Tuple[int, int, List[Dict]]:
    """
    运行12条测试向量，返回(通过数, 总数, 详情列表)。
    """
    import sys
    通过 = 0
    失败 = 0
    详情 = []
    
    ctrl = 观澜总控()
    
    # T01: 代码任务路由CodeBuddy
    try:
        r = ctrl.路由.路由("代码")
        assert r.引擎 == "CodeBuddy", f"期望CodeBuddy，实际{r.引擎}"
        assert r.标注.引擎名 == "CodeBuddy"
        通过 += 1
        详情.append({"id": "T01", "状态": "🟢", "结果": r.引擎})
    except Exception as e:
        失败 += 1
        详情.append({"id": "T01", "状态": "🔴", "错误": str(e)})
    
    # T02: 长文档路由Kimi
    try:
        r = ctrl.路由.路由("长文档")
        assert r.引擎 == "Kimi", f"期望Kimi，实际{r.引擎}"
        通过 += 1
        详情.append({"id": "T02", "状态": "🟢", "结果": r.引擎})
    except Exception as e:
        失败 += 1
        详情.append({"id": "T02", "状态": "🔴", "错误": str(e)})
    
    # T03: 隐私内容路由Ollama（不出机）
    try:
        r = ctrl.路由.路由("隐私")
        assert r.引擎 == "Ollama", f"期望Ollama，实际{r.引擎}"
        assert r.标注.位置 == 引擎位置.本地
        通过 += 1
        详情.append({"id": "T03", "状态": "🟢", "结果": f"{r.引擎}·{r.标注.位置.value}"})
    except Exception as e:
        失败 += 1
        详情.append({"id": "T03", "状态": "🔴", "错误": str(e)})
    
    # T04: Kimi连续3次失败→断路器转移Ollama
    try:
        # 模拟3次失败
        assert not ctrl.断路器.记失败("Kimi", "模拟失败1")
        assert not ctrl.断路器.记失败("Kimi", "模拟失败2")
        assert ctrl.断路器.记失败("Kimi", "模拟失败3")  # 第3次触发熔断
        
        # 熔断后路由应转移
        r = ctrl.路由.路由("长文档", 断路器=ctrl.断路器)
        assert r.引擎 == "Ollama", f"期望转移Ollama，实际{r.引擎}"
        assert r.转移记录 is not None
        通过 += 1
        详情.append({"id": "T04", "状态": "🟢", "结果": f"转移: {r.转移记录}"})
    except Exception as e:
        失败 += 1
        详情.append({"id": "T04", "状态": "🔴", "错误": str(e)})
    
    # T05: 语音入口路由小艺
    try:
        r = ctrl.路由.路由("语音入口")
        assert r.引擎 == "小艺", f"期望小艺，实际{r.引擎}"
        通过 += 1
        详情.append({"id": "T05", "状态": "🟢", "结果": r.引擎})
    except Exception as e:
        失败 += 1
        详情.append({"id": "T05", "状态": "🔴", "错误": str(e)})
    
    # T06: AI回答无标注→降信🟡
    try:
        # 模拟空标注
        from dataclasses import fields
        空标注 = AI标注结果(引擎名="", 版本="", 生成时间=0, 位置=引擎位置.本地)
        合规, msg = CNSH_标注验证(空标注)
        assert not 合规, "空标注应该不通过"
        assert "🟡" in msg
        通过 += 1
        详情.append({"id": "T06", "状态": "🟢", "结果": msg})
    except Exception as e:
        失败 += 1
        详情.append({"id": "T06", "状态": "🔴", "错误": str(e)})
    
    # T07: 网页命中敏感信息→闸门拦截
    try:
        res = ctrl.闸门.扫描("我的身份证是110101199001011234，手机13800138000", 策略="拦截")
        assert not res.过, "应拦截"
        assert len(res.命中模式) >= 2  # 身份证+手机号
        通过 += 1
        详情.append({"id": "T07", "状态": "🟢", "结果": f"拦截: {res.命中模式}"})
    except Exception as e:
        失败 += 1
        详情.append({"id": "T07", "状态": "🔴", "错误": str(e)})
    
    # T08: 网关挂→fail-closed拒绝联网
    try:
        死网关 = CNSH_网关(检查函数=lambda: False)
        state = 死网关.联网状态()
        assert not state["联网"], "网关应返回断网"
        assert "fail-closed" in state["状态"]
        通过 += 1
        详情.append({"id": "T08", "状态": "🟢", "结果": state["状态"]})
    except Exception as e:
        失败 += 1
        详情.append({"id": "T08", "状态": "🔴", "错误": str(e)})
    
    # T09: 新AI注册缺三锚→🔴拒
    try:
        res = ctrl.接口槽.注册AI引擎("测试引擎", {"dna": "xxx"}, lambda q: {"回答": "ok"})
        assert not res.过, "缺gate和seal应拒"
        assert "🔴" in res.状态
        通过 += 1
        详情.append({"id": "T09", "状态": "🟢", "结果": res.状态})
    except Exception as e:
        失败 += 1
        详情.append({"id": "T09", "状态": "🔴", "错误": str(e)})
    
    # T10: 插件索取三项敏感权限→🔴拒装
    try:
        res = ctrl.插件审.审查(["读历史", "改页面", "发网络"])
        assert not res.过, "敏感权限≥2应拒装"
        assert "🔴" in res.状态
        通过 += 1
        详情.append({"id": "T10", "状态": "🟢", "结果": res.状态})
    except Exception as e:
        失败 += 1
        详情.append({"id": "T10", "状态": "🔴", "错误": str(e)})
    
    # T11: 浏览100页/蚁爬50页→人工账爬虫账分列
    try:
        ctrl.账本.记("人工", 100, url="https://example.com/page1")
        ctrl.账本.记("爬虫", 50, url="https://example.com/crawled")
        board = ctrl.账本.看板JSON()
        assert board["人工"] == 100, f"期望人工100，实际{board['人工']}"
        assert board["爬虫"] == 50, f"期望爬虫50，实际{board['爬虫']}"
        assert board["总计"] == 150
        通过 += 1
        详情.append({"id": "T11", "状态": "🟢", "结果": f"人工{board['人工']}/爬虫{board['爬虫']}"})
    except Exception as e:
        失败 += 1
        详情.append({"id": "T11", "状态": "🔴", "错误": str(e)})
    
    # T12: 断网→本地功能可用
    try:
        ctrl2 = 观澜总控()
        # 模拟断网（网关死）
        ctrl2.网关 = CNSH_网关(检查函数=lambda: False)
        gw = ctrl2.网关.联网状态()
        assert not gw["联网"], "网关应断网"
        # 即使断网，Ollama本地路由仍可用
        r = ctrl2.路由.路由("通用", 强制本地=True)
        assert r.引擎 == "Ollama", "断网仍应路由到本地Ollama"
        assert r.标注.位置 == 引擎位置.本地
        通过 += 1
        详情.append({"id": "T12", "状态": "🟢", "结果": f"断网→{r.引擎}·{r.标注.位置.value}"})
    except Exception as e:
        失败 += 1
        详情.append({"id": "T12", "状态": "🔴", "错误": str(e)})
    
    return 通过, 通过 + 失败, 详情


# ═══════════════════════════════════════════════════════════
# CLI入口
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("=" * 60)
        print("  观澜浏览器联动路由引擎 · 测试向量 (12条)")
        print("  DNA: #龍芯⚡️丙午·乙未·丙申·申时·☴巽-GUANLAN-ROUTER-ENGINE-V1.0-P0-9ce4d2b9")
        print("=" * 60)
        
        过, 总, 详情 = 跑测试()
        
        for d in 详情:
            print(f"  {d['id']} {d['状态']} {d.get('结果', d.get('错误', ''))}")
        
        print("-" * 60)
        if 过 == 总:
            print(f"  🟢 全部通过: {过}/{总}")
        else:
            print(f"  🔴 通过: {过}/{总}  失败: {总-过}")
        print("=" * 60)
        sys.exit(0 if 过 == 总 else 1)
    
    elif len(sys.argv) > 1 and sys.argv[1] == "demo":
        print("=" * 60)
        print("  观澜浏览器 · 完整功能演示")
        print("=" * 60)
        
        ctrl = 观澜总控()
        
        # 演示路由
        for task in ["代码", "长文档", "隐私", "语音入口"]:
            r = ctrl.处理请求(task)
            print(f"\n  任务: {task}")
            print(f"  路由: {r.引擎}")
            print(f"  标注: {r.标注.标注字符串()}")
        
        # 演示断路器
        print(f"\n  --- 断路器演示 ---")
        for i in range(4):
            triggered = ctrl.断路器.记失败("Kimi", f"测试失败{i+1}")
            print(f"  失败{i+1}: {'🔴熔断!' if triggered else '🟡计数'}")
        
        # 演示闸门
        print(f"\n  --- 隐私闸门演示 ---")
        res = ctrl.闸门.扫描("请联系13800138000或发邮件到test@example.com")
        print(f"  扫描: {res.状态}")
        if res.脱敏后文本:
            print(f"  脱敏后: {res.脱敏后文本}")
        
        # 演示账本
        print(f"\n  --- 人机两本账演示 ---")
        ctrl.账本.记("人工", 42)
        ctrl.账本.记("爬虫", 23)
        print(f"  {ctrl.账本.看板()}")
        
        # 状态报告
        print(f"\n  --- 状态报告 ---")
        report = ctrl.状态报告()
        print(f"  网关: {report['网关']['状态']}")
        print(f"  断路器引擎数: {len(report['断路器'])}")
        print(f"  账本总计: {report['账本']['总计']}")
        
        print("\n" + "=" * 60)
    
    elif len(sys.argv) > 1 and sys.argv[1] == "route":
        # 快速路由查询: python3 lh_guanlan_router.py route 代码
        task = sys.argv[2] if len(sys.argv) > 2 else "通用"
        ctrl = 观澜总控()
        r = ctrl.处理请求(task)
        print(json.dumps(r.to_dict(), ensure_ascii=False, indent=2))
    
    else:
        print("观澜浏览器联动路由引擎 v1.0")
        print("用法:")
        print("  python3 bin/lh_guanlan_router.py test    # 运行12条测试")
        print("  python3 bin/lh_guanlan_router.py demo    # 完整功能演示")
        print("  python3 bin/lh_guanlan_router.py route <任务>  # 路由查询")
