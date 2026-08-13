# 🔐 Mac文件2：加密工具.command （第1部分）

> Notion URL: https://app.notion.com/p/Mac-2-command-1-e5a7a4da6baa41b181c0a3b9839a3c3d
> Created: 2025-10-16T16:20:00.000Z
> Last edited: 2026-07-01T15:36:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
# 🔐 加密工具.command（第1部分）
> Mac专用 | 图形界面加密工具
---
## 📝 代码第1部分：脚本头部
创建文件：加密工具.command
```bash
#!/bin/bash
# UID9622 加密工具 - 图形界面版

cd "$(dirname "$0")"

python3 << 'PYTHON_CODE_START'
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import zipfile
import hashlib
import datetime
import threading
from pathlib import Path

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import padding
except ImportError:
    import tkinter.messagebox as mb
    mb.showerror("错误", "请先运行「一键安装.command」安装依赖库！")
    exit(1)

class EncryptApp:
    """加密工具主程序"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 UID9622 加密工具")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        
        # 配置
        self.home = Path.home() / ".uid9622"
        self.home.mkdir(exist_ok=True)
        self.password_file = self.home / "password.txt"
        
        # 创建界面
        self.create_widgets()
        
        # 初始化密码
        self.password = self.load_or_create_password()
        self.selected_folder = None
```
---
请继续查看第2部分！
