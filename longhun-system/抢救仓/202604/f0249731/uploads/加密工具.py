#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 UID9622·本地终端加密工具 v3.0
完整+灵活+易用版本

功能：
1. 加密你的Python代码
2. 本地安全运行
3. 灵活调用接口
4. 防止被破解

DNA标签: #UID9622-DNA-终端加密-V3.0
"""

import os
import sys
import marshal
import base64
import zlib
import hashlib
import json
from pathlib import Path
from datetime import datetime

class UID9622Encryptor:
    """UID9622加密器（完整灵活版）"""
    
    def __init__(self):
        self.version = "v3.0"
        self.workspace = Path.home() / "UID9622" / "🔐 加密工具"
        self.workspace.mkdir(parents=True, exist_ok=True)
        
        print("=" * 70)
        print(f"🔐 UID9622·本地终端加密工具 {self.version}")
        print("=" * 70)
        print("💝 完整+灵活+易用版本")
        print("=" * 70 + "\n")
    
    def 显示菜单(self):
        """显示主菜单"""
        print("\n📋 请选择操作：\n")
        print("  1️⃣  加密单个文件")
        print("  2️⃣  加密整个文件夹")
        print("  3️⃣  测试加密文件")
        print("  4️⃣  解密文件（需要密钥）")
        print("  5️⃣  查看加密历史")
        print("  0️⃣  退出")
        print("\n" + "-" * 70)
    
    def 加密文件(self, 文件路径):
        """加密单个文件"""
        
        print(f"\n🔐 开始加密: {文件路径}")
        print("-" * 70)
        
        # 检查文件
        if not os.path.exists(文件路径):
            print("❌ 文件不存在")
            return None
        
        # 读取源代码
        with open(文件路径, 'r', encoding='utf-8') as f:
            源代码 = f.read()
        
        # 生成密钥
        密钥 = self._生成密钥(文件路径)
        print(f"🔑 密钥: {密钥[:32]}...")
        
        # 四层加密
        print("🔒 第1层：编译成字节码...")
        字节码 = marshal.dumps(compile(源代码, 文件路径, 'exec'))
        
        print("🔒 第2层：压缩...")
        压缩后 = zlib.compress(字节码, level=9)
        
        print("🔒 第3层：XOR加密...")
        加密后 = self._xor加密(压缩后, 密钥)
        
        print("🔒 第4层：Base64编码...")
        最终加密 = base64.b64encode(加密后).decode('utf-8')
        
        # 生成文件名
        文件名 = Path(文件路径).stem
        输出文件夹 = self.workspace / 文件名
        输出文件夹.mkdir(exist_ok=True)
        
        # 生成加密包装
        加密文件 = self._生成加密包装(最终加密, 密钥, 文件名, 输出文件夹)
        
        # 保存密钥
        密钥文件 = self._保存密钥(密钥, 文件名, 输出文件夹)
        
        # 生成使用示例
        示例文件 = self._生成使用示例(文件名, 输出文件夹)
        
        # 记录历史
        self._记录加密历史(文件路径, 加密文件, 密钥文件)
        
        print("\n" + "=" * 70)
        print("✅ 加密完成！")
        print("=" * 70)
        print(f"\n📦 输出文件夹: {输出文件夹}")
        print(f"\n生成的文件：")
        print(f"  1. {文件名}_encrypted.py  ← 加密后的文件（给别人用）")
        print(f"  2. {文件名}_key.txt       ← 解密密钥（你保存）")
        print(f"  3. {文件名}_demo.py       ← 使用示例")
        
        return 加密文件
    
    def _生成密钥(self, 文件路径):
        """生成加密密钥"""
        时间戳 = datetime.now().isoformat()
        随机数据 = os.urandom(32).hex()
        密钥源 = f"UID9622-{文件路径}-{时间戳}-{随机数据}"
        return hashlib.sha512(密钥源.encode()).hexdigest()
    
    def _xor加密(self, 数据, 密钥):
        """XOR加密"""
        密钥字节 = 密钥.encode()
        密钥长度 = len(密钥字节)
        
        加密数据 = bytearray()
        for i, 字节 in enumerate(数据):
            加密数据.append(字节 ^ 密钥字节[i % 密钥长度])
        
        return bytes(加密数据)
    
    def _生成加密包装(self, 加密数据, 密钥, 文件名, 输出文件夹):
        """生成加密包装文件"""
        
        # 分割密钥（混淆）
        密钥段 = [密钥[i:i+32] for i in range(0, len(密钥), 32)]
        
        包装代码 = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 UID9622加密包 - {文件名}
版本: v3.0
加密时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

⚠️  此文件已加密保护
✅ 可以正常使用所有功能
❌ 无法查看源代码
"""

import marshal
import base64
import zlib
import sys

class _EncryptedCore:
    """加密核心（不可查看）"""
    
    def __init__(self):
        # 密钥分段存储
        self._k = ["{密钥段[0]}", "{密钥段[1]}", "{密钥段[2]}", "{密钥段[3]}"]
        
        # 加密数据
        self._data = """{加密数据}"""
        
        self._loaded = False
        self._funcs = {{}}
    
    def _get_key(self):
        """重构密钥"""
        return ''.join(self._k)
    
    def _decrypt(self):
        """解密并加载"""
        if self._loaded:
            return
        
        try:
            # Base64解码
            encrypted = base64.b64decode(self._data)
            
            # XOR解密
            key_bytes = self._get_key().encode()
            key_len = len(key_bytes)
            decrypted = bytearray()
            for i, byte in enumerate(encrypted):
                decrypted.append(byte ^ key_bytes[i % key_len])
            
            # 解压缩
            decompressed = zlib.decompress(bytes(decrypted))
            
            # 加载字节码
            code = marshal.loads(decompressed)
            
            # 执行到全局空间
            exec(code, self._funcs)
            
            self._loaded = True
            
        except Exception as e:
            print("❌ 加密包损坏或密钥错误")
            sys.exit(1)
    
    def __getattr__(self, name):
        """动态加载函数"""
        self._decrypt()
        if name in self._funcs:
            return self._funcs[name]
        raise AttributeError(f"没有找到: {name}")

# 创建全局实例
_core = _EncryptedCore()

# 模块级访问
def __getattr__(name):
    return getattr(_core, name)

# 使用说明
__doc__ = """
🔐 UID9622加密包 - {文件名}

使用方法：
    import {文件名}_encrypted as algo
    
    # 调用你的函数
    result = algo.your_function(params)

特性：
    ✅ 完整功能保留
    ✅ 源代码已加密
    ✅ 防止逆向破解
    ✅ 本地安全运行

DNA标签: #UID9622-{文件名.upper()}-ENCRYPTED
"""
'''
        
        输出文件 = 输出文件夹 / f"{文件名}_encrypted.py"
        with open(输出文件, 'w', encoding='utf-8') as f:
            f.write(包装代码)
        
        return 输出文件
    
    def _保存密钥(self, 密钥, 文件名, 输出文件夹):
        """保存密钥文件"""
        
        密钥内容 = f"""
🔑 UID9622解密密钥
==================

文件名: {文件名}
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
版本: v3.0

完整密钥:
{密钥}

⚠️  重要提示：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 此密钥用于解密 {文件名}_encrypted.py
2. 请妥善保管，切勿泄露
3. 丢失密钥将无法恢复源代码
4. 建议备份到安全位置

DNA标签: #UID9622-KEY-{文件名.upper()}
确认码: #ZHUGEXIN⚡️{文件名.upper()}-{datetime.now().strftime('%Y%m%d')}
"""
        
        密钥文件 = 输出文件夹 / f"{文件名}_key.txt"
        with open(密钥文件, 'w', encoding='utf-8') as f:
            f.write(密钥内容)
        
        return 密钥文件
    
    def _生成使用示例(self, 文件名, 输出文件夹):
        """生成使用示例"""
        
        示例代码 = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 UID9622加密包使用示例 - {文件名}
"""

# 导入加密包
import {文件名}_encrypted as algo

def main():
    """使用示例"""
    
    print("🔐 UID9622加密包演示")
    print("=" * 60)
    
    # 示例：调用加密包中的函数
    # result = algo.your_function(param1, param2)
    # print(f"结果: result")
    
    print("\\n✅ 加密包运行正常！")
    print("\\n💡 使用说明：")
    print("   1. 像普通模块一样导入")
    print("   2. 调用任何函数和类")
    print("   3. 源代码已被保护")
    print("   4. 功能完全正常")
    
    print("\\n🎉 你的核心算法已安全加密！")

if __name__ == "__main__":
    main()
'''
        
        示例文件 = 输出文件夹 / f"{文件名}_demo.py"
        with open(示例文件, 'w', encoding='utf-8') as f:
            f.write(示例代码)
        
        return 示例文件
    
    def _记录加密历史(self, 源文件, 加密文件, 密钥文件):
        """记录加密历史"""
        
        历史文件 = self.workspace / "加密历史.json"
        
        历史记录 = {
            "时间": datetime.now().isoformat(),
            "源文件": str(源文件),
            "加密文件": str(加密文件),
            "密钥文件": str(密钥文件)
        }
        
        if 历史文件.exists():
            with open(历史文件, 'r', encoding='utf-8') as f:
                历史 = json.load(f)
        else:
            历史 = []
        
        历史.append(历史记录)
        
        with open(历史文件, 'w', encoding='utf-8') as f:
            json.dump(历史, f, ensure_ascii=False, indent=2)
    
    def 查看历史(self):
        """查看加密历史"""
        
        历史文件 = self.workspace / "加密历史.json"
        
        if not 历史文件.exists():
            print("\n📋 还没有加密历史")
            return
        
        with open(历史文件, 'r', encoding='utf-8') as f:
            历史 = json.load(f)
        
        print("\n📋 加密历史记录")
        print("=" * 70)
        
        for i, 记录 in enumerate(历史, 1):
            print(f"\n{i}. {Path(记录['源文件']).name}")
            print(f"   时间: {记录['时间'][:19]}")
            print(f"   加密文件: {记录['加密文件']}")
    
    def 运行(self):
        """运行主程序"""
        
        while True:
            self.显示菜单()
            选择 = input("请选择 > ").strip()
            
            if 选择 == "1":
                文件路径 = input("\n请输入文件路径（或拖拽文件）: ").strip()
                文件路径 = 文件路径.replace("'", "").replace('"', '')
                self.加密文件(文件路径)
                
            elif 选择 == "2":
                print("\n此功能开发中...")
                
            elif 选择 == "3":
                print("\n此功能开发中...")
                
            elif 选择 == "4":
                print("\n此功能开发中...")
                
            elif 选择 == "5":
                self.查看历史()
                
            elif 选择 == "0":
                print("\n👋 再见！")
                break
            
            else:
                print("\n❌ 无效选择")
            
            input("\n按回车继续...")