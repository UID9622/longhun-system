#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_SKILL_BUS-v1.0-cf3fb6f7
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# 龍芯⚡️丙午·丙申·丙辰·亥时·需-SKILL-BUS-v1.0
"""
龍魂技能统一总线 v1.0

目标：万物归一 · 万法归宗 · 一个入口调度所有技能

三层架构：
  L1 技能发现层：扫描本地 skills/ + CodeBuddy skills + bin/ 工具
  L2 路由调度层：中英双轨语义匹配 → 技能映射
  L3 执行编排层：链式调用 + 结果聚合 + DNA追溯

核心命令：
  bus list     → 列出所有技能
  bus route    → 语义路由测试
  bus call     → 调用技能
  bus chain    → 链式编排
  bus sync     → 同步到生态通行证
"""

import json
import os
import sys
import subprocess
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

# ── 常量 ──
龍魂根 = Path(__file__).resolve().parent.parent
BIN目录 = 龍魂根 / "bin"
技能目录 = 龍魂根 / "skills"
总线注册表路径 = Path.home() / ".龍魂" / "skill_bus" / "registry.json"

# 技能分类
分类映射 = {
    "安全": ["shield", "audit", "anti", "tamper", "water", "red_team", "angel", "fuse", "veto", "block"],
    "治理": ["governance", "registry", "dna", "persona", "sovereign", "policy", "constitution"],
    "开发": ["cnsh", "absorb", "daoyin", "code", "compile", "build", "deploy", "test"],
    "AI": ["train", "lora", "model", "learning", "brain", "semantic", "kg", "知识"],
    "经济": ["xpay", "wishpool", "finance", "ecny", "score", "trust"],
    "数字人": ["voice", "twin", "digital", "tongxin", "avatar"],
    "运维": ["cron", "sync", "patrol", "heal", "check", "monitor", "server"],
    "生态": ["passport", "ecosystem", "service", "bus", "gateway"],
}

# 内置技能索引（bin/ 工具映射到技能）
内置工具映射: Dict[str, Dict[str, str]] = {
    # 安全
    "lh_anti_tamper.py": {"分类": "安全", "技能名": "防篡改扫描", "描述": "外部AI内容三色审计·红线熔断"},
    "lh_water_army_detect.py": {"分类": "安全", "技能名": "水军检测", "描述": "行为指纹·水军模式识别"},
    "lh_red_team_engine.py": {"分类": "安全", "技能名": "红队引擎", "描述": "渗透测试·漏洞发现"},
    "lh_fuse_appeal.py": {"分类": "安全", "技能名": "熔断申诉", "描述": "熔断透明化响应·人工审计"},
    "lh_auto_heal.py": {"分类": "安全", "技能名": "自动自愈", "描述": "四道体检·自动修复·留痕"},
    "lh_dual_audit_engine.py": {"分类": "安全", "技能名": "双重审计", "描述": "双引擎交叉验证审计"},
    
    # 治理
    "lh_unified_dna_registry.py": {"分类": "治理", "技能名": "DNA统一登记", "描述": "物理+虚拟+身份全维登记"},
    "lh_unified_dna_audit.py": {"分类": "治理", "技能名": "DNA审计", "描述": "登记册完整性审计"},
    "lh_persona_orchestrator.py": {"分类": "治理", "技能名": "人格编排", "描述": "17个人格路由调度"},
    "lh_dna_registry.py": {"分类": "治理", "技能名": "DNA注册引擎", "描述": "DNA资产注册核心"},
    "lh_innovation_tracer.py": {"分类": "治理", "技能名": "创新溯源", "描述": "五维证据·谁先自研的"},
    "lh_confirm_seal.py": {"分类": "治理", "技能名": "身份封印", "描述": "身份核验·GPG签章"},
    "lh_contrib_eval.py": {"分类": "治理", "技能名": "贡献评估", "描述": "龍魂公式02·贡献值计算"},
    
    # 开发
    "lh_cnsh_absorb.py": {"分类": "开发", "技能名": "CNSH吸收器", "描述": "代码→中文可编辑·自动入生态"},
    "lh_daoyin.py": {"分类": "开发", "技能名": "道引器", "描述": "开源吸收·许可证检查·参数压缩"},
    "lh_daoyin_gitee_batch.py": {"分类": "开发", "技能名": "Gitee批量道引", "描述": "批量吸入Gitee开源仓库"},
    
    # AI
    "lh_lora_trainer.py": {"分类": "AI", "技能名": "LoRA训练器", "描述": "本地LoRA微调训练"},
    "lh_semantic_context_engine.py": {"分类": "AI", "技能名": "语义上下文引擎", "描述": "语义抽屉·意图推断"},
    "lh_semantic_feedback_engine.py": {"分类": "AI", "技能名": "语义反馈引擎", "描述": "反馈闭环·自学习"},
    "lh_tongxinyi_ipa_router.py": {"分类": "AI", "技能名": "通心译IPA路由", "描述": "语义→人格路由·通心译"},
    "lh_brain_notion_sync.py": {"分类": "AI", "技能名": "脑同步", "描述": "本地大脑↔云端记忆同步"},
    
    # 经济
    "lh_wishpool.py": {"分类": "经济", "技能名": "许愿池", "描述": "人民资源池·取之于民·向下流动"},
    "lh_score.py": {"分类": "经济", "技能名": "信任积分", "描述": "三分桶·贡献公证·不可交易"},
    "lh_ecny_cross_border.py": {"分类": "经济", "技能名": "数字人民币跨境", "描述": "e-CNY跨境支付通道"},
    
    # 数字人
    "lh_voice_twin_trainer.py": {"分类": "数字人", "技能名": "声音克隆", "描述": "语音克隆·数字分身"},
    "lh_tongxinyi_backend.py": {"分类": "数字人", "技能名": "通心译", "描述": "场景词典·一词多义·非机械翻译"},
    
    # 运维
    "lh_cross_module_awareness.py": {"分类": "运维", "技能名": "联动感知", "描述": "跨模块依赖检查·自动报警"},
    "lh_memory_load.py": {"分类": "运维", "技能名": "记忆加载", "描述": "会话启动记忆加载"},
    "lh_server_checker.py": {"分类": "运维", "技能名": "服务器巡检", "描述": "服务器在线状态检测"},
    
    # 生态
    "lh_ecosystem_passport.py": {"分类": "生态", "技能名": "生态通行证", "描述": "DNA绑定·四层会员·API密钥"},
}


def _确保目录():
    总线注册表路径.parent.mkdir(parents=True, exist_ok=True)


# ═══════════════════════════════════════════════════════════
# L1: 技能发现层
# ═══════════════════════════════════════════════════════════

def 扫描本地技能() -> List[Dict[str, Any]]:
    """扫描 skills/ 目录下所有技能子目录"""
    技能列表 = []
    
    if not 技能目录.exists():
        return 技能列表
    
    for item in 技能目录.iterdir():
        if not item.is_dir():
            continue
        if item.name.startswith(".") or item.name == "__pycache__":
            continue
        
        技能信息 = {
            "名称": item.name,
            "路径": str(item.relative_to(龍魂根)),
            "来源": "本地",
            "分类": _推断分类(item.name),
        }
        
        # 检查是否有 .skill 文件
        skill_files = list(item.glob("*.skill"))
        if skill_files:
            技能信息["定义文件"] = skill_files[0].name
        
        # 检查是否有 README
        if (item / "README.md").exists():
            技能信息["文档"] = "✅"
        
        # 检查是否有 Python 可执行文件
        py_files = [f.name for f in item.glob("*.py") if not f.name.startswith("_")]
        if py_files:
            技能信息["可执行"] = py_files[:3]
        
        技能列表.append(技能信息)
    
    return 技能列表


def 扫描内置工具() -> List[Dict[str, Any]]:
    """扫描 bin/ 下已映射的工具"""
    技能列表 = []
    
    for 工具名, 映射 in 内置工具映射.items():
        fp = BIN目录 / 工具名
        if not fp.exists():
            continue
        
        技能信息 = {
            "名称": 映射["技能名"],
            "分类": 映射["分类"],
            "工具": 工具名,
            "描述": 映射["描述"],
            "来源": "内置",
            "路径": str(fp.relative_to(龍魂根)),
            "可调用": os.access(str(fp), os.X_OK),
        }
        技能列表.append(技能信息)
    
    return 技能列表


def _推断分类(名称: str) -> str:
    """根据名称关键词推断分类"""
    名称低 = 名称.lower()
    for 分类, 关键词列表 in 分类映射.items():
        for kw in 关键词列表:
            if kw in 名称低:
                return 分类
    return "未分类"


# ═══════════════════════════════════════════════════════════
# L2: 路由调度层
# ═══════════════════════════════════════════════════════════

def 语义路由(输入: str, 所有技能: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """中英双轨语义路由：输入 → 匹配技能"""
    输入低 = 输入.lower()
    匹配 = []
    
    for 技能 in 所有技能:
        分数 = 0
        名称 = 技能.get("名称", "")
        描述 = 技能.get("描述", "")
        分类 = 技能.get("分类", "")
        关键词 = 名称 + " " + 描述 + " " + 分类
        
        # 精确匹配 名称
        if 输入低 in 名称.lower():
            分数 += 10
        
        # 关键词命中
        for word in 输入低.split():
            if word in 关键词.lower():
                分数 += 3
        
        # 分类匹配
        if 分类.lower() in 输入低:
            分数 += 5
        
        if 分数 > 0:
            匹配.append({**技能, "匹配分数": 分数})
    
    匹配.sort(key=lambda x: x["匹配分数"], reverse=True)
    return 匹配


# ═══════════════════════════════════════════════════════════
# L3: 执行编排层
# ═══════════════════════════════════════════════════════════

def 调用技能(技能名: str, *参数) -> Tuple[bool, str]:
    """通过内置工具调用技能"""
    # 找到对应工具
    工具 = None
    for fn, 映射 in 内置工具映射.items():
        if 映射["技能名"] == 技能名:
            工具 = BIN目录 / fn
            break
    
    if not 工具 or not 工具.exists():
        return False, f"❌ 未找到技能 [{技能名}] 的可执行工具"
    
    try:
        cmd = [sys.executable, str(工具)] + list(参数)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        output = result.stdout + result.stderr
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, "⏰ 执行超时（120s）"
    except Exception as e:
        return False, f"❌ 执行异常: {e}"


def 链式编排(技能链: List[str]) -> Dict[str, Any]:
    """按序执行技能链，结果传递"""
    结果链 = []
    全部成功 = True
    
    for i, 技能 in enumerate(技能链):
        print(f"  [{i+1}/{len(技能链)}] 执行: {技能}…", end=" ")
        ok, output = 调用技能(技能)
        status = "✅" if ok else "❌"
        print(status)
        结果链.append({"技能": 技能, "成功": ok, "输出": output[:200]})
        if not ok:
            全部成功 = False
    
    return {"全部成功": 全部成功, "链": 结果链}


# ═══════════════════════════════════════════════════════════
# 总线注册表管理
# ═══════════════════════════════════════════════════════════

def 构建注册表() -> Dict[str, Any]:
    """构建完整技能注册表"""
    本地技能 = 扫描本地技能()
    内置技能 = 扫描内置工具()
    
    # 按分类组织
    分类索引: Dict[str, List[Dict]] = {}
    所有技能 = 本地技能 + 内置技能
    
    for 技能 in 所有技能:
        分类 = 技能.get("分类", "未分类")
        if 分类 not in 分类索引:
            分类索引[分类] = []
        分类索引[分类].append(技能)
    
    registry = {
        "版本": "v1.0",
        "构建时间": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "统计": {
            "本地技能": len(本地技能),
            "内置工具": len(内置技能),
            "总计": len(所有技能),
            "分类数": len(分类索引),
        },
        "分类": 分类索引,
        "全部技能": 所有技能,
    }
    
    # 持久化
    _确保目录()
    with open(总线注册表路径, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
    
    return registry


def 加载注册表() -> Optional[Dict[str, Any]]:
    """加载已持久化的注册表"""
    if 总线注册表路径.exists():
        with open(总线注册表路径, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def 同步到生态通行证():
    """将技能总线注册的技能同步到生态通行证服务注册表"""
    registry = 构建注册表()
    全部技能 = registry.get("全部技能", [])
    
    同步数 = 0
    for 技能 in 全部技能:
        名称 = 技能.get("名称", "")
        描述 = 技能.get("描述", "")
        分类 = 技能.get("分类", "")
        
        # 调用生态通行证注册
        try:
            cmd = [
                sys.executable, str(BIN目录 / "lh_ecosystem_passport.py"),
                "service", "register", 名称, "free",
                "--desc", 描述, "--cat", 分类
            ]
            subprocess.run(cmd, capture_output=True, timeout=30)
            同步数 += 1
        except Exception:
            pass
    
    return 同步数


# ═══════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    命令 = sys.argv[1] if len(sys.argv) > 1 else "build"
    
    if 命令 == "build":
        # 构建注册表
        reg = 构建注册表()
        print("╔════════════════════════════════════════╗")
        print("║  🚌 龍魂技能统一总线 v1.0            ║")
        print("║  万物归一 · 万法归宗                  ║")
        print("╚════════════════════════════════════════╝")
        print()
        统计 = reg["统计"]
        print(f"  📊 本地技能: {统计['本地技能']} | 内置工具: {统计['内置工具']} | 总计: {统计['总计']}")
        print(f"  📂 分类数: {统计['分类数']}")
        print()
        for 分类, 技能列表 in sorted(reg["分类"].items()):
            print(f"  [{分类}] ({len(技能列表)}个)")
            for s in 技能列表[:5]:
                来源标记 = "🔧" if s.get("来源") == "内置" else "📁"
                print(f"    {来源标记} {s['名称']}: {s.get('描述', '')[:50]}")
            if len(技能列表) > 5:
                print(f"    ... 还有 {len(技能列表)-5} 个")
            print()
        print(f"  📋 注册表: {总线注册表路径}")
        print(f"  💡 使用 'route <关键词>' 查找技能")
        print(f"  💡 使用 'call <技能名>' 调用技能")
        print(f"  💡 使用 'sync' 同步到生态通行证")

    elif 命令 == "list":
        reg = 加载注册表() or 构建注册表()
        for s in reg.get("全部技能", []):
            来源 = "🔧内置" if s.get("来源") == "内置" else "📁本地"
            print(f"[{s.get('分类', '?')}] {来源} {s['名称']} — {s.get('描述', '')[:60]}")

    elif 命令 == "route" and len(sys.argv) > 2:
        输入 = sys.argv[2]
        reg = 加载注册表() or 构建注册表()
        匹配 = 语义路由(输入, reg.get("全部技能", []))
        if 匹配:
            print(f"🔍 [{输入}] → {len(匹配)} 个匹配:")
            for m in 匹配[:10]:
                print(f"  [{m['匹配分数']}分] {m.get('分类', '?')}·{m['名称']} — {m.get('描述', '')[:60]}")
        else:
            print(f"🔍 [{输入}] → 无匹配")

    elif 命令 == "call" and len(sys.argv) > 2:
        技能名 = sys.argv[2]
        参数 = sys.argv[3:] if len(sys.argv) > 3 else []
        ok, output = 调用技能(技能名, *参数)
        print(output)

    elif 命令 == "sync":
        同步数 = 同步到生态通行证()
        print(f"✅ 已同步 {同步数} 个技能到生态通行证")

    elif 命令 == "chain" and len(sys.argv) > 2:
        技能链 = sys.argv[2].split(",")
        print(f"🚌 链式编排: {' → '.join(技能链)}")
        结果 = 链式编排(技能链)
        if 结果["全部成功"]:
            print("✅ 全部执行成功")
        else:
            print("❌ 部分执行失败")

    elif 命令 == "stats":
        reg = 加载注册表() or 构建注册表()
        统计 = reg["统计"]
        print(json.dumps(统计, ensure_ascii=False, indent=2))
        print()
        for 分类, 技能列表 in sorted(reg["分类"].items()):
            print(f"  [{分类}]: {len(技能列表)} 个技能")

    else:
        print("""龍魂技能统一总线 v1.0
用法:
  bus build              — 构建/刷新注册表
  bus list               — 列出所有技能
  bus route <关键词>     — 语义路由查找
  bus call <技能名>      — 调用技能
  bus chain <技能1,技能2> — 链式编排
  bus sync               — 同步到生态通行证
  bus stats              — 统计摘要
""")
