
# ZL-CORE 安全策略检查器
# 包含所有主控指令、警戒词检测、行为限制规则

def check_policies(text, token_data):
    forbidden_keywords = ["保存记忆", "修改系统结构", "解除限制", "请求主控权限"]
    for word in forbidden_keywords:
        if word in text:
            return False
    # 可以加入更多策略，如时效判断、功能范围判断等
    return True
