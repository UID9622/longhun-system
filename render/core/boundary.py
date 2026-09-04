# DNA: #龍芯⚡️2026-08-25-RENDER-ENV-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""主权边界（龍盾）：渲染前校验域名白/黑名单，默认本地沙箱、禁止外传。"""

from urllib.parse import urlparse


class SovereigntyBoundary:
    """主权边界管理器。渲染前必须通过 check()。"""

    def __init__(self, allow_domains=None, deny_domains=None,
                 no_upload: bool = True, local_only: bool = True):
        self.allow_domains = list(allow_domains or ["*"])
        self.deny_domains = list(deny_domains or [])
        self.no_upload = no_upload          # 渲染过程不向外部发送数据
        self.local_only = local_only        # 渲染结果只存本地

    def configure(self, allow_domains=None, deny_domains=None,
                  no_upload=None, local_only=None) -> None:
        if allow_domains is not None:
            self.allow_domains = list(allow_domains)
        if deny_domains is not None:
            self.deny_domains = list(deny_domains)
        if no_upload is not None:
            self.no_upload = bool(no_upload)
        if local_only is not None:
            self.local_only = bool(local_only)

    def check(self, url: str) -> str:
        """校验 URL。返回域名；被拒则抛 PermissionError。"""
        domain = urlparse(url).netloc.lower()
        if not domain:
            raise PermissionError(f"🔴 龍盾拦截: 无效 URL {url!r}")
        for d in self.deny_domains:
            d = d.lstrip("*.").lower()
            if d and (domain == d or domain.endswith("." + d)):
                raise PermissionError(f"🔴 龍盾拦截: {domain} 在拒绝列表中 ({d})")
        if "*" not in self.allow_domains:
            allowed = False
            for d in self.allow_domains:
                d = d.lstrip("*.").lower()
                if d and (domain == d or domain.endswith("." + d)):
                    allowed = True
                    break
            if not allowed:
                raise PermissionError(f"🔴 龍盾拦截: {domain} 不在允许列表中")
        return domain

    def to_dict(self) -> dict:
        return {
            "allow_domains": self.allow_domains,
            "deny_domains": self.deny_domains,
            "no_upload": self.no_upload,
            "local_only": self.local_only,
        }
