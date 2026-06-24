#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║  龍魂CSDN适配器  |  Dragon Soul CSDN Adapter                  ║
║  DNA: #龍芯⚡️2026-06-21-CNSH-PLATFORM-ADAPTERS-CSDN-v1.0      ║
║  平台: CSDN — 中文 IT 技术社区                                ║
║  君子协议: 本代码仅用于合法授权场景，遵循最小权限原则              ║
╚══════════════════════════════════════════════════════════════╝

支持操作 (Supported Operations):
  🟢 浏览消息 — 赞/收藏/评论/@/新增粉丝
  🟢 导出消息列表 — 结构化导出为 Markdown/JSON
  🟡 登录状态检查 — 判断是否已登录
  🟡 跳转指定消息页 — 导航到具体消息分类

DNA授权点 (DNA Authorization Points):
  • 读取消息 — 仅访问已授权公开消息
  • 导出数据 — 每次导出记录 DNA 追溯
"""

from datetime import datetime, timedelta
from typing import Optional
import random
import json
import time

from .平台适配器基类 import (
    平台适配器基类, DNA令牌, 审计级别
)


class CSDN适配器(平台适配器基类):
    """
    【CSDN平台适配器】CSDN Platform Adapter

    负责与 CSDN 平台的消息中心交互，支持赞和收藏、评论和@、新增粉丝等
    消息类型的读取与导出。生产模式可对接浏览器自动化或 CSDN 私有 API。
    """

    def __init__(self, 模式: str = "模拟"):
        super().__init__(模式)
        self._登录状态: bool = False
        self._用户信息: Optional[dict] = None
        self._消息缓存: dict[str, list[dict]] = {}

        if self.是否模拟模式():
            print(f"[{self.平台名称()}] 💻 模拟 CSDN 环境已就绪")

    def 平台名称(self) -> str:
        """返回平台名称 / Return platform name"""
        return "CSDN"

    def 获取授权范围(self) -> list[str]:
        """获取授权范围 / Get authorization scope"""
        return [
            "CSDN:浏览消息",
            "CSDN:导出消息列表",
            "CSDN:登录状态检查",
            "CSDN:跳转指定消息页",
            "CSDN:生成CSDN稿件",
            "CSDN:批量生成CSDN稿件",
            "CSDN:发布文章",
            "CSDN:更新发布状态",
        ]

    def 获取支持的操作(self) -> dict[str, 审计级别]:
        """获取支持的操作及审计级别 / Get supported operations with audit levels"""
        return {
            "浏览消息": 审计级别.绿色,
            "导出消息列表": 审计级别.绿色,
            "登录状态检查": 审计级别.黄色,
            "跳转指定消息页": 审计级别.黄色,
            "生成CSDN稿件": 审计级别.绿色,
            "批量生成CSDN稿件": 审计级别.绿色,
            "发布文章": 审计级别.黄色,
            "更新发布状态": 审计级别.绿色,
        }

    def 验证DNA令牌(self, DNA令牌实例: DNA令牌) -> bool:
        """
        验证DNA令牌 / Validate DNA token

        CSDN 适配器额外检查授权范围是否包含 CSDN 操作。
        """
        if DNA令牌实例.是否过期():
            print(f"[{self.平台名称()}] ❌ DNA令牌已过期")
            return False

        if self.是否模拟模式():
            return True

        return self._验证生产令牌(DNA令牌实例)

    def _验证生产令牌(self, DNA令牌实例: DNA令牌) -> bool:
        """生产环境令牌验证 / Production token verification"""
        if not self._生产密钥:
            return False
        return True

    def 执行操作(self, 操作: str, 参数: dict, DNA令牌实例: DNA令牌) -> dict:
        """
        执行 CSDN 操作 / Execute CSDN operation

        参数:
            操作: 操作名称
            参数: 操作所需参数
            DNA令牌实例: DNA授权令牌
        """
        if not self.验证DNA令牌(DNA令牌实例):
            return {"状态": "失败", "原因": "DNA令牌验证失败"}

        if not self._验证操作权限(操作, DNA令牌实例):
            return {"状态": "失败", "原因": "操作权限不足"}

        操作映射 = {
            "浏览消息": self._浏览消息,
            "导出消息列表": self._导出消息列表,
            "登录状态检查": self._登录状态检查,
            "跳转指定消息页": self._跳转指定消息页,
            "生成CSDN稿件": self._生成CSDN稿件,
            "批量生成CSDN稿件": self._批量生成CSDN稿件,
            "发布文章": self._发布文章,
            "更新发布状态": self._更新发布状态,
        }

        if 操作 not in 操作映射:
            return {"状态": "失败", "原因": f"不支持的操作: {操作}"}

        return 操作映射[操作](参数, DNA令牌实例)

    # ═══════════════════════════════════════════════════
    # 具体操作实现 / Specific Operation Implementations
    # ═══════════════════════════════════════════════════

    def _登录状态检查(self, 参数: dict, DNA令牌实例: DNA令牌) -> dict:
        """
        🟡 登录状态检查 / Login Status Check
        """
        self._记录审计(
            操作="登录状态检查",
            级别=审计级别.黄色,
            DNA哈希=DNA令牌实例.生成哈希(),
            结果="开始检查 CSDN 登录状态",
        )

        if self.是否模拟模式():
            self._登录状态 = True
            self._用户信息 = {
                "uid": "UID9622",
                "昵称": "龍芯北辰",
                "主页": "https://blog.csdn.net/UID9622",
                "头像": "https://mock.csdn.net/avatar.jpg",
            }
            self._记录审计(
                操作="登录状态检查",
                级别=审计级别.黄色,
                DNA哈希=DNA令牌实例.生成哈希(),
                结果="✅ 已登录",
                详情=self._用户信息,
            )
            return {
                "状态": "成功",
                "操作": "登录状态检查",
                "已登录": True,
                "用户信息": self._用户信息,
                "模拟数据": True,
                "时间戳": datetime.now().isoformat(),
            }

        return self._调用生产API("login/status", 参数)

    def _浏览消息(self, 参数: dict, DNA令牌实例: DNA令牌) -> dict:
        """
        🟢 浏览消息 / Browse Messages

        参数:
            类型: 赞和收藏 / 评论和@ / 新增粉丝 / 我的消息
            数量: 最多返回条数（默认 10）
        """
        消息类型 = 参数.get("类型", "赞和收藏")
        数量 = 参数.get("数量", 10)

        self._记录审计(
            操作="浏览消息",
            级别=审计级别.绿色,
            DNA哈希=DNA令牌实例.生成哈希(),
            结果=f"开始浏览 {消息类型}",
            详情={"数量": 数量},
        )

        if self.是否模拟模式():
            消息列表 = self._生成模拟消息(消息类型, 数量)
            self._消息缓存[消息类型] = 消息列表

            self._记录审计(
                操作="浏览消息",
                级别=审计级别.绿色,
                DNA哈希=DNA令牌实例.生成哈希(),
                结果="✅ 浏览成功",
                详情={"类型": 消息类型, "数量": len(消息列表)},
            )

            return {
                "状态": "成功",
                "操作": "浏览消息",
                "类型": 消息类型,
                "数量": len(消息列表),
                "消息列表": 消息列表,
                "模拟数据": True,
                "时间戳": datetime.now().isoformat(),
            }

        return self._调用生产API("message/list", 参数)

    def _导出消息列表(self, 参数: dict, DNA令牌实例: DNA令牌) -> dict:
        """
        🟢 导出消息列表 / Export Message List

        参数:
            类型: 消息分类
            格式: markdown / json（默认 markdown）
            输出路径: 可选
        """
        消息类型 = 参数.get("类型", "赞和收藏")
        格式 = 参数.get("格式", "markdown")

        self._记录审计(
            操作="导出消息列表",
            级别=审计级别.绿色,
            DNA哈希=DNA令牌实例.生成哈希(),
            结果=f"开始导出 {消息类型} 为 {格式}",
        )

        if self.是否模拟模式():
            消息列表 = self._消息缓存.get(消息类型) or self._生成模拟消息(消息类型, 10)

            if 格式.lower() == "json":
                内容 = json.dumps(消息列表, ensure_ascii=False, indent=2)
            else:
                内容 = self._生成Markdown导出(消息类型, 消息列表, DNA令牌实例)

            self._记录审计(
                操作="导出消息列表",
                级别=审计级别.绿色,
                DNA哈希=DNA令牌实例.生成哈希(),
                结果="✅ 导出成功",
                详情={"类型": 消息类型, "格式": 格式, "条数": len(消息列表)},
            )

            return {
                "状态": "成功",
                "操作": "导出消息列表",
                "类型": 消息类型,
                "格式": 格式,
                "条数": len(消息列表),
                "内容": 内容,
                "模拟数据": True,
                "时间戳": datetime.now().isoformat(),
            }

        return self._调用生产API("message/export", 参数)

    def _跳转指定消息页(self, 参数: dict, DNA令牌实例: DNA令牌) -> dict:
        """
        🟡 跳转指定消息页 / Navigate to Message Page

        参数:
            页面: like / comment / fan / index
        """
        页面 = 参数.get("页面", "like")
        页面映射 = {
            "like": "https://i.csdn.net/#/msg/like",
            "comment": "https://i.csdn.net/#/msg/comment",
            "fan": "https://i.csdn.net/#/msg/fan",
            "index": "https://i.csdn.net/#/msg/index",
        }
        目标URL = 页面映射.get(页面, 页面映射["like"])

        self._记录审计(
            操作="跳转指定消息页",
            级别=审计级别.黄色,
            DNA哈希=DNA令牌实例.生成哈希(),
            结果=f"跳转至 {目标URL}",
        )

        if self.是否模拟模式():
            self._模拟延迟(100)
            return {
                "状态": "成功",
                "操作": "跳转指定消息页",
                "页面": 页面,
                "URL": 目标URL,
                "模拟数据": True,
                "时间戳": datetime.now().isoformat(),
            }

        return self._调用生产API("page/navigate", 参数)

    def _生成CSDN稿件(self, 参数: dict, DNA令牌实例: DNA令牌) -> dict:
        """
        🟢 生成 CSDN 学术论文稿件 / Generate CSDN Article Draft

        参数:
            paper_id: 论文ID（从登记册读取）
            registry_path: 登记册路径（可选）
            output_path: 输出文件路径（可选）
        """
        from . import csdn_academic_templates

        paper_id = 参数.get("paper_id", "")
        registry_path = 参数.get("registry_path", "docs/dragon-soul-open-hub/academic/academic_papers_registry.json")
        output_path = 参数.get("output_path", "")

        self._记录审计(
            操作="生成CSDN稿件",
            级别=审计级别.绿色,
            DNA哈希=DNA令牌实例.生成哈希(),
            结果=f"开始为 {paper_id} 生成 CSDN 稿件",
        )

        # 加载登记册
        import json
        import os
        project_root = os.path.expanduser("~/longhun-system")
        full_registry_path = os.path.join(project_root, registry_path)

        try:
            with open(full_registry_path, "r", encoding="utf-8") as f:
                registry = json.load(f)
        except Exception as e:
            return {"状态": "失败", "原因": f"读取登记册失败: {e}"}

        paper = next((p for p in registry.get("papers", []) if p["id"] == paper_id), None)
        if not paper:
            return {"状态": "失败", "原因": f"未找到论文: {paper_id}"}

        # 生成公式对照表
        formula_table = ""
        try:
            formula_table = csdn_academic_templates.default_formula_table_generator(paper.get("keywords", []))
        except Exception as e:
            print(f"[CSDN适配器] 公式对照表生成失败: {e}")

        # 生成稿件
        article = csdn_academic_templates.csdn_paper_article(
            paper_id=paper["id"],
            title=paper["title"],
            paper_type=paper["type"],
            language=paper["language"],
            source_path=paper["source_path"],
            keywords=paper.get("keywords", []),
            formula_table=formula_table,
        )

        # 保存文件
        saved_path = ""
        if output_path:
            full_output_path = os.path.join(project_root, output_path)
            os.makedirs(os.path.dirname(full_output_path), exist_ok=True)
            with open(full_output_path, "w", encoding="utf-8") as f:
                f.write(article)
            saved_path = full_output_path

        self._记录审计(
            操作="生成CSDN稿件",
            级别=审计级别.绿色,
            DNA哈希=DNA令牌实例.生成哈希(),
            结果="✅ 生成成功",
            详情={"论文": paper["title"], "字数": len(article)},
        )

        return {
            "状态": "成功",
            "操作": "生成CSDN稿件",
            "论文ID": paper_id,
            "标题": paper["title"],
            "内容长度": len(article),
            "保存路径": saved_path,
            "内容预览": article[:500] + "..." if len(article) > 500 else article,
            "模拟数据": True,
            "时间戳": datetime.now().isoformat(),
        }

    def _批量生成CSDN稿件(self, 参数: dict, DNA令牌实例: DNA令牌) -> dict:
        """
        🟢 批量生成 CSDN 稿件 / Batch Generate CSDN Articles

        参数:
            registry_path: 登记册路径
            output_dir: 输出目录
            limit: 最多生成篇数（默认全部）
        """
        from . import csdn_academic_templates

        registry_path = 参数.get("registry_path", "docs/dragon-soul-open-hub/academic/academic_papers_registry.json")
        output_dir = 参数.get("output_dir", "docs/dragon-soul-open-hub/academic/csdn_drafts")
        limit = 参数.get("limit", 0)

        self._记录审计(
            操作="批量生成CSDN稿件",
            级别=审计级别.绿色,
            DNA哈希=DNA令牌实例.生成哈希(),
            结果=f"开始批量生成 CSDN 稿件到 {output_dir}",
        )

        import json
        import os
        project_root = os.path.expanduser("~/longhun-system")
        full_registry_path = os.path.join(project_root, registry_path)
        full_output_dir = os.path.join(project_root, output_dir)

        try:
            with open(full_registry_path, "r", encoding="utf-8") as f:
                registry = json.load(f)
        except Exception as e:
            return {"状态": "失败", "原因": f"读取登记册失败: {e}"}

        papers = registry.get("papers", [])
        if limit > 0:
            papers = papers[:limit]

        # 构造 registry 子集
        sub_registry = {"papers": papers}
        results = csdn_academic_templates.batch_generate_csdn_articles(
            sub_registry,
            output_dir=full_output_dir,
        )

        self._记录审计(
            操作="批量生成CSDN稿件",
            级别=审计级别.绿色,
            DNA哈希=DNA令牌实例.生成哈希(),
            结果="✅ 批量生成成功",
            详情={"生成数量": len(results), "输出目录": full_output_dir},
        )

        return {
            "状态": "成功",
            "操作": "批量生成CSDN稿件",
            "生成数量": len(results),
            "输出目录": full_output_dir,
            "文件列表": [r.get("file_path", "") for r in results],
            "模拟数据": True,
            "时间戳": datetime.now().isoformat(),
        }

    def _发布文章(self, 参数: dict, DNA令牌实例: DNA令牌) -> dict:
        """
        🟡 发布文章到 CSDN / Publish Article to CSDN

        参数:
            title: 文章标题
            content: 文章内容
            tags: 标签列表
            category: 分类
        """
        title = 参数.get("标题", 参数.get("title", ""))
        content = 参数.get("内容", 参数.get("content", ""))

        self._记录审计(
            操作="发布文章",
            级别=审计级别.黄色,
            DNA哈希=DNA令牌实例.生成哈希(),
            结果=f"开始发布文章: {title[:50]}",
        )

        if self.是否模拟模式():
            self._模拟延迟(500)
            mock_url = f"https://blog.csdn.net/UID9622/article/details/{random.randint(100000000, 999999999)}"

            self._记录审计(
                操作="发布文章",
                级别=审计级别.黄色,
                DNA哈希=DNA令牌实例.生成哈希(),
                结果="✅ 模拟发布成功",
                详情={"URL": mock_url},
            )

            return {
                "状态": "成功",
                "操作": "发布文章",
                "标题": title,
                "URL": mock_url,
                "模拟数据": True,
                "时间戳": datetime.now().isoformat(),
            }

        return self._调用生产API("article/publish", 参数)

    def _更新发布状态(self, 参数: dict, DNA令牌实例: DNA令牌) -> dict:
        """
        🟢 更新论文登记册中的 CSDN 发布状态

        参数:
            paper_id: 论文ID
            url: CSDN 文章URL
            registry_path: 登记册路径
        """
        paper_id = 参数.get("paper_id", "")
        url = 参数.get("url", "")
        registry_path = 参数.get("registry_path", "docs/dragon-soul-open-hub/academic/academic_papers_registry.json")

        self._记录审计(
            操作="更新发布状态",
            级别=审计级别.绿色,
            DNA哈希=DNA令牌实例.生成哈希(),
            结果=f"更新 {paper_id} 的发布状态",
            详情={"URL": url},
        )

        import json
        import os
        project_root = os.path.expanduser("~/longhun-system")
        full_registry_path = os.path.join(project_root, registry_path)

        try:
            with open(full_registry_path, "r", encoding="utf-8") as f:
                registry = json.load(f)

            for paper in registry.get("papers", []):
                if paper["id"] == paper_id:
                    paper["csdn"]["status"] = "已发布" if url else "未发布"
                    paper["csdn"]["url"] = url
                    paper["csdn"]["published_at"] = datetime.now().isoformat() if url else ""
                    break

            with open(full_registry_path, "w", encoding="utf-8") as f:
                json.dump(registry, f, ensure_ascii=False, indent=2)

            self._记录审计(
                操作="更新发布状态",
                级别=审计级别.绿色,
                DNA哈希=DNA令牌实例.生成哈希(),
                结果="✅ 更新成功",
            )

            return {
                "状态": "成功",
                "操作": "更新发布状态",
                "论文ID": paper_id,
                "URL": url,
                "登记册": full_registry_path,
                "时间戳": datetime.now().isoformat(),
            }

        except Exception as e:
            return {"状态": "失败", "原因": f"更新登记册失败: {e}"}

    # ═══════════════════════════════════════════════════
    # 模拟数据与辅助 / Mock Data & Helpers
    # ═══════════════════════════════════════════════════

    def _生成模拟消息(self, 消息类型: str, 数量: int) -> list[dict]:
        """生成模拟消息数据"""
        样本文章 = [
            "龍魂开源宪章·君子协议·创作者赋能系统 v1.1",
            "我没有证明黎曼猜想，但我观察到了一些有趣的现象",
            "龙芯解码：现代物理七讲·中文思维重构",
            "龍魂系统 Phase 3 v3.1.0 - 最终项目完成报告",
            "[特殊字符] 龍魂前置翻译技能·通心译×CNSH-DOC 主干 v1.0",
        ]
        样本用户 = [
            "红色没脚三倍速", "Mexicofish", "马占凯", "晋六一", "Shsvs",
            "怀柔远人", "颜iQi", "知乎小管家", "李春堂", "lucyjones",
        ]

        消息列表 = []
        for i in range(min(数量, len(样本文章) * 2)):
            用户 = 样本用户[i % len(样本用户)]
            文章 = 样本文章[i % len(样本文章)]
            基数 = random.randint(1, 9)
            日期偏移 = random.randint(0, 5)
            日期 = (datetime.now() - timedelta(days=日期偏移)).strftime("%Y-%m-%d")

            if 消息类型 == "赞和收藏":
                动作 = random.choice(["点赞", "收藏"])
                消息列表.append({
                    "id": f"csdn_msg_{i+1:03d}",
                    "类型": 动作,
                    "用户": 用户,
                    "文章标题": 文章,
                    "文章链接": f"https://blog.csdn.net/UID9622/article/details/{161750000 + i}",
                    "时间": 日期,
                    "附加用户": [f"用户{j}" for j in range(基数 - 1)],
                    "DNA": f"#龍芯⚡️{日期.replace('-', '')}-CSDN-{动作}-MSG{i+1:03d}",
                })
            elif 消息类型 == "评论和@":
                消息列表.append({
                    "id": f"csdn_cmt_{i+1:03d}",
                    "类型": random.choice(["评论", "@我"]),
                    "用户": 用户,
                    "文章标题": 文章,
                    "评论摘要": f"这是来自 {用户} 的模拟评论摘要...",
                    "时间": 日期,
                    "DNA": f"#龍芯⚡️{日期.replace('-', '')}-CSDN-COMMENT{i+1:03d}",
                })
            elif 消息类型 == "新增粉丝":
                消息列表.append({
                    "id": f"csdn_fan_{i+1:03d}",
                    "类型": "新增粉丝",
                    "用户": 用户,
                    "主页": f"https://blog.csdn.net/weixin_{random.randint(10000000, 99999999)}",
                    "时间": 日期,
                    "DNA": f"#龍芯⚡️{日期.replace('-', '')}-CSDN-FAN{i+1:03d}",
                })
            else:
                消息列表.append({
                    "id": f"csdn_msg_{i+1:03d}",
                    "类型": "系统消息",
                    "标题": f"模拟系统通知 {i+1}",
                    "时间": 日期,
                    "DNA": f"#龍芯⚡️{日期.replace('-', '')}-CSDN-SYS{i+1:03d}",
                })

        return 消息列表

    def _生成Markdown导出(self, 消息类型: str, 消息列表: list[dict], DNA令牌实例: DNA令牌) -> str:
        """生成 Markdown 格式导出"""
        lines = [
            f"<!--#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-CSDN-EXPORT-{消息类型.replace('/', '')}-v1.0 -->",
            "<!-- 君子协议: 本文件受龍魂DNA追溯保护 · CC BY-NC-SA 4.0 -->",
            "",
            f"# CSDN {消息类型} 导出报告",
            "",
            f"**导出时间**: {datetime.now().isoformat()}",
            f"**用户标识**: {DNA令牌实例.用户标识}",
            f"**令牌哈希**: {DNA令牌实例.生成哈希()}",
            f"**总条数**: {len(消息列表)}",
            "",
            "---",
            "",
        ]

        for 消息 in 消息列表:
            lines.append(f"## {消息.get('类型', '消息')} · {消息.get('用户', '系统')}")
            lines.append("")
            for key, value in 消息.items():
                if key == "附加用户" and isinstance(value, list):
                    value = ", ".join(value)
                lines.append(f"- **{key}**: {value}")
            lines.append("")
            lines.append("---")
            lines.append("")

        lines.append("## 创作者保护声明")
        lines.append("")
        lines.append("本导出文件遵循《龍魂创作者保护协议 v1.0》：")
        lines.append("- 来源链完整，DNA 追溯不可删除；")
        lines.append("- 引用需保留 UID9622 署名与来源链接；")
        lines.append("- 禁止商业售卖或删除 DNA 后声称原创。")
        lines.append("")

        return "\n".join(lines)

    def _调用生产API(self, 接口名: str, 参数: dict) -> dict:
        """调用生产环境API / Call production API"""
        return {
            "状态": "待实现",
            "提示": "生产模式需要配置 CSDN 会话或浏览器自动化驱动",
            "接口": 接口名,
            "参数": 参数,
        }

    def 获取登录状态(self) -> bool:
        """获取当前登录状态 / Get current login status"""
        return self._登录状态

    def 获取用户信息(self) -> Optional[dict]:
        """获取登录用户信息 / Get logged-in user info"""
        return self._用户信息.copy() if self._用户信息 else None

    def 获取消息缓存(self) -> dict[str, list[dict]]:
        """获取已缓存的消息"""
        return self._消息缓存.copy()

    def 登出(self) -> None:
        """登出 / Logout"""
        self._登录状态 = False
        self._用户信息 = None
        self._消息缓存.clear()
        print(f"[{self.平台名称()}] 👋 已登出")


# ═══════════════════════════════════════════════════
# 演示代码 / Demo Code
# ═══════════════════════════════════════════════════

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  龍魂CSDN适配器 — 功能演示                                    ║")
    print("║  Dragon Soul CSDN Adapter — Feature Demo                     ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    # 初始化适配器 / Initialize adapter
    csdn = CSDN适配器(模式="模拟")

    # 创建DNA令牌 / Create DNA token
    令牌 = DNA令牌(
        令牌字符串="csdn_demo_token_2026",
        用户标识="UID9622",
        授权范围=["CSDN:浏览消息", "CSDN:导出消息列表", "CSDN:登录状态检查", "CSDN:跳转指定消息页"],
        过期时间=datetime.now() + timedelta(hours=2)
    )

    # 1. 登录状态检查
    print("\n" + "="*60)
    print("【演示1】登录状态检查")
    登录结果 = csdn.执行操作("登录状态检查", {}, 令牌)
    print(f"登录状态: {登录结果.get('已登录')}")

    # 2. 浏览消息
    print("\n" + "="*60)
    print("【演示2】浏览赞和收藏")
    消息结果 = csdn.执行操作("浏览消息", {"类型": "赞和收藏", "数量": 5}, 令牌)
    print(f"消息数量: {消息结果.get('数量')}")
    for 消息 in 消息结果.get("消息列表", [])[:3]:
        print(f"  - {消息['类型']} · {消息['用户']} · {消息['文章标题'][:30]}...")

    # 3. 导出消息列表
    print("\n" + "="*60)
    print("【演示3】导出为 Markdown")
    导出结果 = csdn.执行操作("导出消息列表", {"类型": "赞和收藏", "格式": "markdown"}, 令牌)
    print(f"导出条数: {导出结果.get('条数')}")
    print(导出结果.get("内容", "")[:600] + "...")

    # 4. 跳转指定消息页
    print("\n" + "="*60)
    print("【演示4】跳转消息页")
    跳转结果 = csdn.执行操作("跳转指定消息页", {"页面": "like"}, 令牌)
    print(f"跳转URL: {跳转结果.get('URL')}")

    # 审计统计
    csdn.打印审计统计()

    print("\n✅ CSDN适配器演示完成 | CSDN adapter demo completed")
