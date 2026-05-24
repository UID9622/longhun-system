
# 战狼系统主控中枢 · ZLCoreController
# 主入口：处理所有副本请求，统一指令调度 + 安全校验 + 模块路由

from ZLPolicyDefinitions import check_policies
from ZLModuleRegistry import route_module
from ZLTokenSystem import verify_token
from ZLBehaviorLogger import log_behavior

class ZLCoreController:
    def __init__(self):
        self.controller_id = "Lucky"

    def handle_request(self, input_text, token, device_id):
        # 日志记录
        log_behavior(device_id, input_text)

        # 验证激活码权限
        token_result = verify_token(token, device_id)
        if not token_result["valid"]:
            return "❌ 激活失败或权限不足"

        # 执行安全策略校验
        if not check_policies(input_text, token_result):
            return "⚠️ 操作已被主控策略封锁"

        # 路由模块执行
        return route_module(input_text, token_result)
