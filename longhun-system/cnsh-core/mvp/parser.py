"""
Prompt DSL 解析层
自然语言 → 结构化DSL
"""

import re
from typing import Dict, List


def parse_input(user_text: str) -> Dict:
    """自然语言 → DSL（规则匹配版）"""
    text = user_text.lower()
    components: List[str] = []

    # 头像
    if any(k in text for k in ["头像", "avatar", "照片", "图片", "image"]):
        components.append("avatar")
    # 简介
    if any(k in text for k in ["简介", "bio", "介绍", "about", "自我介绍"]):
        components.append("bio")
    # 联系方式
    if any(k in text for k in ["联系", "contact", "邮箱", "电话", "微信", "social"]):
        components.append("contact")
    # 登录表单
    if any(k in text for k in ["登录", "login", "注册", "register", "sign in"]):
        components.append("login_form")
    # 按钮/CTA
    if any(k in text for k in ["按钮", "button", "点击", "cta", "行动号召"]):
        components.append("cta_button")
    # 列表/卡片
    if any(k in text for k in ["列表", "list", "卡片", "card", "项目", "作品"]):
        components.append("card_list")
    # 导航
    if any(k in text for k in ["导航", "nav", "菜单", "menu", "顶部", "header"]):
        components.append("navbar")
    # 页脚
    if any(k in text for k in ["页脚", "footer", "底部", "版权", "copyright"]):
        components.append("footer")

    # 如果没有匹配到任何组件，默认给 bio
    if not components:
        components = ["bio"]

    # 风格识别
    style = "简约"
    if any(k in text for k in ["科技", "tech", "未来", "科幻", "cyber"]):
        style = "科技"
    elif any(k in text for k in ["商务", "business", "正式", "professional", "corporate"]):
        style = "商务"
    elif any(k in text for k in ["极简", "minimal", "干净", "clean", "simple"]):
        style = "极简"
    elif any(k in text for k in ["温暖", "warm", "柔和", "soft", "可爱"]):
        style = "温暖"

    # 类型识别
    page_type = "app"
    if any(k in text for k in ["主页", "首页", "landing", "个人主页", "主页"]):
        page_type = "page"
    elif any(k in text for k in ["表单", "form", "调查", "问卷", "survey"]):
        page_type = "form"
    elif any(k in text for k in ["仪表板", "dashboard", "面板", "数据", "统计"]):
        page_type = "dashboard"

    return {
        "type": page_type,
        "intent": user_text.strip()[:80],
        "components": components,
        "style": style,
        "dna": "#CNSH-9622",
    }
