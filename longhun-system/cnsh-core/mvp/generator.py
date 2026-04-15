"""
UI 生成引擎（AutoUI v1.0）
根据 DSL 生成完整 HTML 页面
"""

from typing import Dict


STYLE_PALETTE = {
    "简约": {
        "bg": "#ffffff",
        "fg": "#1a1a1a",
        "accent": "#333333",
        "font": "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    },
    "科技": {
        "bg": "#0a0a0f",
        "fg": "#e0e0ff",
        "accent": "#00d4ff",
        "font": "'SF Mono', 'Fira Code', monospace",
    },
    "商务": {
        "bg": "#f8f9fa",
        "fg": "#212529",
        "accent": "#0056b3",
        "font": "'Helvetica Neue', Arial, sans-serif",
    },
    "极简": {
        "bg": "#fafafa",
        "fg": "#111111",
        "accent": "#000000",
        "font": "system-ui, sans-serif",
    },
    "温暖": {
        "bg": "#fff8f0",
        "fg": "#4a3b2a",
        "accent": "#e07a5f",
        "font": "'Georgia', 'Times New Roman', serif",
    },
}


def _render_component(comp: str, intent: str) -> str:
    """渲染单个组件为 HTML"""
    if comp == "avatar":
        return '''
    <div class="avatar">
        <img src="https://api.dicebear.com/7.x/notionists/svg?seed=CNSH9622" alt="头像"/>
    </div>'''
    if comp == "bio":
        return f'''
    <div class="bio">
        <p>{intent}</p>
    </div>'''
    if comp == "contact":
        return '''
    <div class="contact">
        <p>📧 hello@cnsh-9622.local</p>
        <p>🌐 <a href="#">链接</a></p>
    </div>'''
    if comp == "login_form":
        return '''
    <form class="login-form" onsubmit="event.preventDefault(); alert('CNSH · 守护验证通过');">
        <input type="text" placeholder="用户名" required/>
        <input type="password" placeholder="密码" required/>
        <button type="submit">登录</button>
    </form>'''
    if comp == "cta_button":
        return '''
    <div class="cta">
        <button onclick="alert('CNSH · 行动已记录')">立即开始</button>
    </div>'''
    if comp == "card_list":
        return '''
    <div class="card-list">
        <div class="card"><h3>项目一</h3><p>描述内容</p></div>
        <div class="card"><h3>项目二</h3><p>描述内容</p></div>
        <div class="card"><h3>项目三</h3><p>描述内容</p></div>
    </div>'''
    if comp == "navbar":
        return '''
    <nav class="navbar">
        <div class="nav-brand">CNSH</div>
        <div class="nav-links">
            <a href="#">首页</a>
            <a href="#">关于</a>
            <a href="#">联系</a>
        </div>
    </nav>'''
    if comp == "footer":
        return '''
    <footer class="footer">
        <p>© 2026 CNSH-9622 · 龍魂系统</p>
        <p class="dna">#龍芯⚡️守护</p>
    </footer>'''
    return ""


def _build_css(style: str) -> str:
    """根据风格生成 CSS"""
    p = STYLE_PALETTE.get(style, STYLE_PALETTE["简约"])
    return f"""<style>
        :root {{
            --bg: {p['bg']};
            --fg: {p['fg']};
            --accent: {p['accent']};
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: {p['font']};
            background: var(--bg);
            color: var(--fg);
            min-height: 100vh;
            line-height: 1.6;
        }}
        .container {{
            max-width: 720px;
            margin: 0 auto;
            padding: 2rem 1.5rem;
        }}
        .navbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
            margin-bottom: 2rem;
            border-bottom: 1px solid rgba(128,128,128,0.2);
        }}
        .nav-brand {{ font-weight: 700; font-size: 1.25rem; }}
        .nav-links a {{ margin-left: 1.5rem; text-decoration: none; color: var(--fg); opacity: 0.8; }}
        .nav-links a:hover {{ opacity: 1; color: var(--accent); }}
        .avatar {{ text-align: center; margin: 2rem 0; }}
        .avatar img {{ width: 120px; height: 120px; border-radius: 50%; border: 3px solid var(--accent); }}
        .bio {{ font-size: 1.1rem; margin: 1.5rem 0; opacity: 0.9; }}
        .contact {{ margin: 1.5rem 0; }}
        .contact a {{ color: var(--accent); }}
        .login-form {{ display: flex; flex-direction: column; gap: 0.75rem; margin: 1.5rem 0; }}
        .login-form input, .login-form button {{
            padding: 0.75rem 1rem;
            border-radius: 8px;
            border: 1px solid rgba(128,128,128,0.3);
            font-size: 1rem;
        }}
        .login-form button {{
            background: var(--accent);
            color: var(--bg);
            border: none;
            cursor: pointer;
            font-weight: 600;
        }}
        .cta {{ margin: 2rem 0; text-align: center; }}
        .cta button {{
            padding: 0.875rem 2rem;
            border-radius: 8px;
            border: none;
            background: var(--accent);
            color: var(--bg);
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
        }}
        .card-list {{ display: grid; gap: 1rem; margin: 1.5rem 0; }}
        .card {{
            padding: 1.25rem;
            border-radius: 12px;
            border: 1px solid rgba(128,128,128,0.15);
            background: rgba(128,128,128,0.03);
        }}
        .card h3 {{ margin-bottom: 0.5rem; color: var(--accent); }}
        .footer {{
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid rgba(128,128,128,0.15);
            text-align: center;
            font-size: 0.875rem;
            opacity: 0.7;
        }}
        .footer .dna {{ margin-top: 0.5rem; font-size: 0.75rem; opacity: 0.5; }}
        h1 {{ font-size: 1.75rem; margin-bottom: 1rem; }}
    </style>"""


def generate_ui(schema: Dict) -> str:
    """根据 DSL 生成完整 HTML 页面"""
    components = schema.get("components", [])
    intent = schema.get("intent", "CNSH 生成页面")
    style = schema.get("style", "简约")
    dna = schema.get("dna", "#CNSH-9622")

    # 如果有 navbar，把它放到 body 开头
    body_parts = []
    nav_html = ""
    footer_html = ""
    main_comps = []

    for comp in components:
        if comp == "navbar":
            nav_html = _render_component(comp, intent)
        elif comp == "footer":
            footer_html = _render_component(comp, intent)
        else:
            main_comps.append(comp)

    if nav_html:
        body_parts.append(nav_html)

    body_parts.append('<div class="container">')
    body_parts.append(f"<h1>{intent}</h1>")
    for comp in main_comps:
        body_parts.append(_render_component(comp, intent))
    if footer_html:
        body_parts.append(footer_html)
    body_parts.append("</div>")

    components_html = "\n".join(body_parts)
    css = _build_css(style)

    html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{intent}</title>
    <meta name="dna" content="{dna}">
    {css}
</head>
<body>
{components_html}
    <!-- {dna} -->
</body>
</html>"""
    return html
