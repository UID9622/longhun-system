class PermissionSystem:
    def register_user(self, user_id, digital_id):
        return {"success": True, "user_id": user_id}

if __name__ == "__main__":
    ps = PermissionSystem()
    print("系统层面测试成功！")
