
# 模块调度与执行路由中心

def route_module(text, token_data):
    if "推理" in text or "生成" in text:
        return "[ZL-07] 模型执行器响应：你请求的内容已生成。"
    elif "标签" in text or "融合" in text:
        return "[ZL-MASTER] 正在调取副本标签并融合回主控。"
    else:
        return "[ZL-UNK] 未识别模块指令。"
