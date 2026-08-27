# DNA: #龍芯⚡️2026-08-25-RENDER-ENV-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""CNSH 渲染指令解析器：把「渲染.方法(参数)」解析为编排器调用。"""

import ast
import re
import shlex

# 方法名映射：中文 → 英文（编排器方法名）
METHOD_MAP = {
    "打开": "navigate", "等待": "wait", "后退": "go_back", "前进": "go_forward",
    "刷新": "reload", "截图": "screenshot", "提取DOM": "extract_dom",
    "提取文本": "extract_text", "提取元素": "extract_elements",
    "视觉匹配": "visual_match", "点击": "click", "填写": "fill",
    "清空": "clear", "滚动": "scroll", "选择": "select_option",
    "勾选": "check", "取消勾选": "uncheck", "悬停": "hover", "按键": "keypress",
    "导出": "export", "保存": "save", "设置DNA": "set_dna", "审计": "audit",
    "设置边界": "set_boundary", "批量": "batch",
    "注册哈希": "register_hash", "验证哈希": "verify_hash",
}

# 参数别名：中文/英文 → 编排器方法参数名
ARG_ALIASES = {
    "url": "url", "选择器": "selector", "selector": "selector",
    "值": "value", "value": "value", "掩码": "mask", "mask": "mask",
    "模板": "template", "template": "template", "阈值": "threshold",
    "threshold": "threshold", "区域": "region", "region": "region",
    "深度": "depth", "depth": "depth", "模式": "mode", "mode": "mode",
    "类型": "type", "type": "type", "文本": "text", "text": "text",
    "文本包含": "contains_text", "contains_text": "contains_text",
    "坐标": "coords", "coords": "coords", "方向": "direction",
    "direction": "direction", "距离": "distance", "distance": "distance",
    "到底": "to_end", "to_end": "to_end", "元素": "element", "element": "element",
    "到中心": "to_center", "to_center": "to_center", "条件": "condition",
    "condition": "condition", "秒": "seconds", "seconds": "seconds",
    "并发": "concurrency", "concurrency": "concurrency",
    "间隔": "interval", "interval": "interval", "urls": "urls",
    "变量": "variable", "variable": "variable", "路径": "path", "path": "path",
    "格式": "fmt", "fmt": "fmt", "允许域名": "allow_domains",
    "allow_domains": "allow_domains", "拒绝域名": "deny_domains",
    "deny_domains": "deny_domains", "拒绝上传": "no_upload",
    "no_upload": "no_upload", "本地沙箱": "local_only", "local_only": "local_only",
    "组件类型": "element_type", "视觉匹配结果": "match_result",
    "哈希": "sha256", "sha256": "sha256",
}

_METHOD_RE = re.compile(
    r"^\s*(?:渲染|render)\.\s*([\u4e00-\u9fa5A-Za-z0-9]+)\s*\((.*)\)\s*$",
    re.DOTALL,
)


def _eval_arg(token: str):
    """安全解析单个实参 token（字面量/简单表达式）。"""
    token = token.strip()
    if not token:
        return None
    try:
        return ast.literal_eval(token)
    except Exception:
        pass
    # 变量引用 {render.xxx} / {secrets.xxx}
    m = re.fullmatch(r"\{(\w+)\.(\w+)\}", token)
    if m:
        return {"__ref__": f"{m.group(1)}.{m.group(2)}"}
    try:
        return float(token) if re.fullmatch(r"-?\d+(\.\d+)?", token) else token
    except Exception:
        return token


def _split_top_level(s: str):
    """按逗号切分，忽略括号/引号内的逗号。"""
    parts, depth, quote, cur = [], 0, None, []
    for ch in s:
        if quote:
            cur.append(ch)
            if ch == quote:
                quote = None
        elif ch in ("'", '"'):
            quote = ch
            cur.append(ch)
        elif ch in "([{":
            depth += 1
            cur.append(ch)
        elif ch in ")]}":
            depth -= 1
            cur.append(ch)
        elif ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return [p.strip() for p in parts if p.strip()]


def parse_command(cnsh_command: str) -> dict:
    """解析一条 CNSH 渲染指令。

    返回 {method, args, kwargs, raw}；无法解析抛 ValueError。
    示例: 渲染.打开("https://example.com")
          渲染.点击(文本="登录")
          渲染.填写(选择器="#user", 值="UID9622", 掩码=True)
    """
    m = _METHOD_RE.match(cnsh_command)
    if not m:
        raise ValueError(f"无法解析 CNSH 渲染指令: {cnsh_command!r}")
    cn_name = m.group(1)
    method = METHOD_MAP.get(cn_name, cn_name)
    inner = m.group(2).strip()
    args, kwargs = [], {}
    if inner:
        for part in _split_top_level(inner):
            if "=" in part:
                k, v = part.split("=", 1)
                key = ARG_ALIASES.get(k.strip(), k.strip())
                kwargs[key] = _eval_arg(v)
            else:
                args.append(_eval_arg(part))
    return {"method": method, "args": args, "kwargs": kwargs, "raw": cnsh_command}


class CNSHRenderParser:
    """CNSH 渲染指令解析执行器。绑定编排器。"""

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def parse_and_run(self, cnsh_command: str) -> dict:
        cmd = parse_command(cnsh_command)
        method = cmd["method"]
        fn = getattr(self.orchestrator, method, None)
        if not callable(fn):
            raise AttributeError(f"编排器无此指令: {method}")
        # 解析 {render.*}/{secrets.*} 引用
        kwargs = dict(cmd["kwargs"])
        for k, v in kwargs.items():
            if isinstance(v, dict) and v.get("__ref__"):
                kwargs[k] = self._resolve_ref(v["__ref__"])
        result = fn(*cmd["args"], **kwargs)
        if result is None:
            result = {}
        if not isinstance(result, dict):
            result = {"value": result}
        result["_method"] = method
        result["_raw"] = cnsh_command[:200]
        return result

    def _resolve_ref(self, ref: str):
        ns, key = ref.split(".", 1)
        ctx = self.orchestrator.ctx
        if ns == "render" and ctx is not None:
            return getattr(ctx, key, None)
        if ns == "secrets":
            # secrets.* 由 secret-env / 内存注入处理，未注册返回 None
            return self.orchestrator.secrets.get(key)
        return None
