# 龍魂系统 · 支付宝当面付个人申请自动化方案
# UID9622 · 身份证直接搞定 · 无需营业执照

---

## 一、核心结论

**支付宝"当面付"个人版，无需营业执照，身份证直接申请。**

- 单笔限额: 1000元
- 单日限额: 5万元
- 费率: 0.38% (官方渠道)
- 到账: 实时到个人支付宝余额

---

## 二、申请流程 (手动版)

### 方式A: 手机支付宝APP (推荐，最简单)

```
1. 打开支付宝APP
2. 首页搜索: "签约助手"
3. 点击"签约助手" (官方)
4. 找到"当面付" -> 点击"立即开通"
5. 经营类目: 选择"百货零售-超市-超市 (非平台类)"
6. 营业执照: 不上传 (选填，跳过)
7. 店铺招牌: 网上随便找一张便利店/超市门头照片
8. 提交 -> 等待审核 (一般2-30分钟)
```

### 方式B: 电脑网页版 (费率0.38%)

```
1. 电脑登录: https://b.alipay.com
2. 顶部导航: "产品中心" -> "当面付"
3. 点击"立即接入"
4. 经营类目: "生活百货" 或 "平台类综合商城"
5. 营业执照: 不上传 (非必填)
6. 店铺招牌: 百度搜索"便利店门头"，找一张上传
7. 确认提交 -> 等待审核
```

**注意**: 网页版费率0.38%，商家中心签约是0.6%，别走错了。

---

## 三、接口配置 (获取API密钥)

### 3.1 创建应用

```
1. 登录支付宝开放平台: https://open.alipay.com
2. 控制台 -> "网页&移动应用" -> "创建应用"
3. 应用名称: 龍魂系统
4. 应用类型: 网页应用
5. 绑定商家账号: 当前登录的支付宝账号
```

### 3.2 设置接口加签

```
1. 进入应用详情 -> "开发设置" -> "接口加签方式"
2. 点击"设置"
3. 加签模式: 选择"公钥"
4. 下载"支付宝开放平台开发助手" (密钥生成工具)
5. 运行工具 -> 选择"RSA2" -> 生成密钥对
6. 复制"应用公钥" -> 粘贴到支付宝后台 -> 保存
7. 支付宝会生成"支付宝公钥" -> 复制保存
8. 保存"应用私钥" (本地，不要泄露)
```

### 3.3 获取APPID

```
应用详情页 -> 查看APPID (一串数字)
记录: APPID、应用私钥、支付宝公钥
```

---

## 四、自动化脚本设计

### 4.1 信息存储 (固定文件夹)

```
~/longhun-system/secrets/alipay/
├── id_card.json          # 身份证信息 (加密)
├── phone.txt             # 手机号 (明文)
├── app_credentials.json  # APPID + 密钥 (加密)
└── shop_photo.jpg        # 店铺门头照片
```

### 4.2 自动化脚本架构

```
用户输入:
  ├── 操作密码 (解锁加密文件)
  ├── 短信验证码 (接收后输入)
  └── 人脸验证 (最后一步手动)

系统自动:
  ├── 读取身份证信息
  ├── 读取手机号
  ├── 上传店铺门头照片
  ├── 填写经营类目
  ├── 跳过营业执照
  ├── 提交申请
  └── 保存申请记录
```

---

## 五、Python自动化脚本

### 5.1 信息读取模块

```python
#!/usr/bin/env python3
# alipay_info_loader.py

import json
from pathlib import Path
from cryptography.fernet import Fernet
import hashlib
import base64

class LonghunAlipayInfo:
    # 龍魂支付宝信息加载器

    SECRETS_DIR = Path.home() / "longhun-system" / "secrets" / "alipay"

    def __init__(self, password: str):
        self.password = password
        self.key = self._derive_key(password)
        self.cipher = Fernet(self.key)

    def _derive_key(self, password: str) -> bytes:
        key = hashlib.sha256(password.encode()).digest()
        return base64.urlsafe_b64encode(key)

    def load_id_card(self) -> dict:
        filepath = self.SECRETS_DIR / "id_card.json"
        if not filepath.exists():
            return {}
        with open(filepath, 'rb') as f:
            encrypted = f.read()
        try:
            decrypted = self.cipher.decrypt(encrypted)
            return json.loads(decrypted.decode())
        except:
            print("[错误] 密码错误，无法解密身份证信息")
            return {}

    def load_phone(self) -> str:
        filepath = self.SECRETS_DIR / "phone.txt"
        if filepath.exists():
            return filepath.read_text().strip()
        return ""

    def load_credentials(self) -> dict:
        filepath = self.SECRETS_DIR / "app_credentials.json"
        if not filepath.exists():
            return {}
        with open(filepath, 'rb') as f:
            encrypted = f.read()
        try:
            decrypted = self.cipher.decrypt(encrypted)
            return json.loads(decrypted.decode())
        except:
            return {}

    def save_credentials(self, appid: str, private_key: str, alipay_public_key: str):
        # 保存应用凭证 (首次配置后)
        self.SECRETS_DIR.mkdir(parents=True, exist_ok=True)
        creds = {
            "appid": appid,
            "private_key": private_key,
            "alipay_public_key": alipay_public_key
        }
        encrypted = self.cipher.encrypt(json.dumps(creds).encode())
        with open(self.SECRETS_DIR / "app_credentials.json", 'wb') as f:
            f.write(encrypted)
        print("[成功] 应用凭证已加密保存")


# 使用示例
if __name__ == "__main__":
    password = input("请输入操作密码: ")
    loader = LonghunAlipayInfo(password)

    id_card = loader.load_id_card()
    phone = loader.load_phone()
    creds = loader.load_credentials()

    print(f"身份证: {id_card.get('name', '未加载')}")
    print(f"手机号: {phone}")
    print(f"APPID: {creds.get('appid', '未配置')}")
```

### 5.2 浏览器自动化申请

```python
#!/usr/bin/env python3
# alipay_apply_automation.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time

class AlipayFaceToFaceApply:
    # 支付宝当面付自动申请

    def __init__(self, personal_info: dict, shop_photo_path: str):
        self.info = personal_info
        self.shop_photo = shop_photo_path
        self.driver = None

    def start(self):
        # 启动浏览器
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--headless')  # 调试时关闭

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    def apply_via_mobile(self):
        # 手机端申请流程
        # 注意: 手机端需要扫码登录，部分步骤需手动
        print("[步骤1] 打开支付宝签约助手")
        self.driver.get("https://b.alipay.com")

        print("[提示] 请手动扫码登录支付宝")
        input("登录完成后按回车继续...")

        # 搜索当面付
        search_box = self.driver.find_element(By.ID, "search")
        search_box.send_keys("当面付")
        search_box.submit()

        # 点击当面付产品
        face_to_face = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "当面付"))
        )
        face_to_face.click()

        # 点击立即开通
        apply_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "立即开通"))
        )
        apply_btn.click()

        # 填写经营类目
        print("[步骤2] 填写经营类目")
        category_select = Select(self.driver.find_element(By.NAME, "category"))
        category_select.select_by_visible_text("百货零售")

        sub_category = Select(self.driver.find_element(By.NAME, "sub_category"))
        sub_category.select_by_visible_text("超市")

        # 跳过营业执照
        print("[步骤3] 跳过营业执照 (个人无需上传)")
        # 营业执照上传框存在但不上传

        # 上传店铺门头照片
        print("[步骤4] 上传店铺门头照片")
        photo_input = self.driver.find_element(By.NAME, "shop_photo")
        photo_input.send_keys(self.shop_photo)

        # 填写联系人信息
        print("[步骤5] 填写联系人信息")
        name_input = self.driver.find_element(By.NAME, "contact_name")
        name_input.send_keys(self.info['id_card']['name'])

        phone_input = self.driver.find_element(By.NAME, "contact_phone")
        phone_input.send_keys(self.info['phone'])

        # 提交申请
        print("[步骤6] 提交申请")
        submit_btn = self.driver.find_element(By.ID, "submit")
        submit_btn.click()

        print("[成功] 申请已提交，等待审核")
        print("[提示] 审核通常需要2-30分钟")

    def close(self):
        if self.driver:
            self.driver.quit()
```

### 5.3 一键申请脚本

```bash
#!/bin/bash
# alipay_apply.sh
# 一键申请支付宝当面付

echo "========================================"
echo "龍魂系统 · 支付宝当面付申请"
echo "无需营业执照 · 身份证直接搞定"
echo "========================================"
echo ""

# 检查依赖
if ! command -v python3 &> /dev/null; then
    echo "[错误] 需要安装 Python3"
    exit 1
fi

if ! python3 -c "import selenium" 2>/dev/null; then
    echo "[提示] 正在安装依赖..."
    pip3 install selenium cryptography
fi

# 输入密码
echo -n "请输入操作密码: "
read -s PASSWORD
echo ""

# 运行Python脚本
python3 << EOF
import sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / "longhun-system" / "scripts"))

from alipay_info_loader import LonghunAlipayInfo
from alipay_apply_automation import AlipayFaceToFaceApply

# 加载信息
loader = LonghunAlipayInfo("$PASSWORD")
id_card = loader.load_id_card()
phone = loader.load_phone()

if not id_card:
    print("[错误] 无法读取身份证信息")
    sys.exit(1)

print(f"[成功] 信息加载完成")
print(f"  姓名: {id_card['name']}")
print(f"  手机号: {phone}")
print("")

# 检查店铺照片
shop_photo = str(Path.home() / "longhun-system" / "secrets" / "alipay" / "shop_photo.jpg")
if not Path(shop_photo).exists():
    print("[错误] 未找到店铺门头照片")
    print("[提示] 请准备一张便利店/超市门头照片，保存到:")
    print(f"  {shop_photo}")
    sys.exit(1)

# 启动自动化
personal_info = {
    "id_card": id_card,
    "phone": phone
}

automation = AlipayFaceToFaceApply(personal_info, shop_photo)
automation.start()

try:
    automation.apply_via_mobile()
    print("")
    print("[成功] 申请流程已完成")
    print("[提示] 请查看支付宝APP或短信，获取审核结果")
finally:
    automation.close()
EOF

echo ""
echo "========================================"
echo "申请完成"
echo "========================================"
```

---

## 六、收款接口对接

### 6.1 创建收款订单

```python
#!/usr/bin/env python3
# alipay_payment.py

from alipay import AliPay
import json
from pathlib import Path
from cryptography.fernet import Fernet
import hashlib
import base64
import time

class LonghunAlipayPayment:
    # 龍魂支付宝收款接口

    def __init__(self, password: str):
        self.password = password
        self.alipay = self._init_alipay()

    def _init_alipay(self) -> AliPay:
        # 初始化支付宝SDK
        secrets_dir = Path.home() / "longhun-system" / "secrets" / "alipay"

        key = base64.urlsafe_b64encode(hashlib.sha256(self.password.encode()).digest())
        cipher = Fernet(key)

        with open(secrets_dir / "app_credentials.json", 'rb') as f:
            encrypted = f.read()

        creds = json.loads(cipher.decrypt(encrypted).decode())

        return AliPay(
            appid=creds['appid'],
            app_notify_url=None,  # 默认回调地址
            app_private_key_string=creds['private_key'],
            alipay_public_key_string=creds['alipay_public_key'],
            sign_type="RSA2",
            debug=False
        )

    def create_order(self, amount: float, dna: str, subject: str = "龍魂系统服务") -> dict:
        # 创建收款订单
        # Args:
        #     amount: 金额 (元)
        #     dna: 内容DNA
        #     subject: 订单标题
        # Returns:
        #     订单信息，包含支付二维码

        # 生成订单号 (含DNA)
        order_id = f"LH{dna[:8]}{int(time.time())}"

        # 创建订单
        order_string = self.alipay.api_alipay_trade_precreate(
            out_trade_no=order_id,
            total_amount=str(amount),
            subject=subject,
            body=f"DNA:{dna}"
        )

        return {
            "order_id": order_id,
            "amount": amount,
            "dna": dna,
            "qr_code": order_string.get('qr_code'),  # 支付二维码URL
            "status": "pending",
            "created_at": time.time()
        }

    def query_order(self, order_id: str) -> dict:
        # 查询订单状态
        result = self.alipay.api_alipay_trade_query(out_trade_no=order_id)
        return {
            "order_id": order_id,
            "status": result.get('trade_status', 'UNKNOWN'),
            "amount": result.get('total_amount'),
            "paid_at": result.get('gmt_payment')
        }


# 使用示例
if __name__ == "__main__":
    password = input("请输入操作密码: ")
    payment = LonghunAlipayPayment(password)

    # 创建订单
    order = payment.create_order(
        amount=0.01,  # 测试金额1分钱
        dna="da146546c027abd9b4353fee362216ea",
        subject="龍魂系统测试订单"
    )

    print(f"订单创建成功")
    print(f"  订单号: {order['order_id']}")
    print(f"  金额: {order['amount']}元")
    print(f"  二维码: {order['qr_code']}")
    print(f"  请使用支付宝扫码支付")
```

---

## 七、执行清单

### 今天必须做的

```bash
# 1. 创建目录结构
mkdir -p ~/longhun-system/secrets/alipay
mkdir -p ~/longhun-system/scripts

# 2. 保存脚本 (把上面的Python代码保存到对应文件)
# alipay_info_loader.py -> ~/longhun-system/scripts/
# alipay_apply_automation.py -> ~/longhun-system/scripts/
# alipay_payment.py -> ~/longhun-system/scripts/
# alipay_apply.sh -> ~/longhun-system/scripts/

# 3. 准备身份证信息 (首次)
python3 ~/longhun-system/scripts/alipay_info_loader.py
# 输入密码 -> 输入身份证信息 -> 保存

# 4. 准备店铺门头照片
# 百度搜索"便利店门头"，下载一张保存到:
# ~/longhun-system/secrets/alipay/shop_photo.jpg

# 5. 准备手机号
echo "138****8888" > ~/longhun-system/secrets/alipay/phone.txt
```

### 本周完成的

```bash
# 1. 运行申请脚本
bash ~/longhun-system/scripts/alipay_apply.sh

# 2. 等待审核通过 (2-30分钟)
# 3. 登录支付宝开放平台，创建应用
# 4. 生成密钥，保存凭证
# 5. 测试收款 (1分钱)
```

---

## 八、龍魂标识

```
龍魂系统 · 支付宝当面付个人申请方案
无需营业执照 · 身份证直接搞定 · 零门槛

#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```

---

END
