
# 激活码权限系统模块

tokens = {
    "TOKEN-001": {"used": False, "device_id": None, "level": "standard"},
    "TOKEN-002": {"used": True, "device_id": "device-x", "level": "admin"}
}

def verify_token(token, device_id):
    if token not in tokens:
        return {"valid": False}
    info = tokens[token]
    if info["used"] and info["device_id"] != device_id:
        return {"valid": False}
    if not info["used"]:
        info["used"] = True
        info["device_id"] = device_id
    return {"valid": True, "level": info["level"]}
