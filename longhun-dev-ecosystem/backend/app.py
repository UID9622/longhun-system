# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂生态 · FastAPI 主应用
DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-DEV-APP-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
用法: cd longhun-dev-ecosystem && python3 -m uvicorn backend.app:app --host 0.0.0.0 --port 8800
"""

import hashlib
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .models import Developer, CodeDNA, Contribution, PaymentOrder, SessionLocal, init_db
from .schemas import (
    DeveloperRegisterRequest,
    PaymentConfirmRequest,
    BillRequest,
    PayNotifyRequest,
    CodeInjectRequest,
    SmsSendRequest,
    PhoneLoginRequest,
)
from .dna_generator import generate_developer_dna, generate_code_dna, generate_dna
from .payment import create_payment_order, confirm_payment
from .sms import send_code, verify_code
from .models import placeholder_email
from .monthly_fee import (
    create_monthly_bill,
    confirm_monthly_payment,
    handle_payment_notify,
    check_developer_fee_status,
    freeze_expired_developers,
    get_fee_history,
    get_public_fee_stats,
    export_fee_records,
    export_contributions,
    export_code_dna,
    export_developers,
    get_current_month,
)
from .gateway import available_channels
from .config import BASE_DIR, CONFIRM, GPG, ECOSYSTEM_NAME, ECOSYSTEM_DNA, MONTHLY_FEE_ANCHOR

# 数据库初始化（模块顶层执行：兼容 uvicorn 字符串导入，避免 __main__ 陷阱）
init_db()

app = FastAPI(
    title="龍魂生态 · 月度主权开发者系统",
    version="2.0.0",
    description="月度主权确认金 · 每月1元起步·上不封顶 · 开发者注册 / DNA绑定 / 代码注入 / 贡献者生态",
)

# 身份锚（挂载到 app.state，随服务可查）
app.state.dna = ECOSYSTEM_DNA
app.state.confirm = CONFIRM
app.state.gpg = GPG

# CORS（同源部署无需跨域凭证；避免 allow_origins=* 与 allow_credentials=True 冲突）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态资源（frontend/assets）
frontend_dir = BASE_DIR / "frontend"
assets_dir = frontend_dir / "assets"
if assets_dir.exists():
    app.mount("/static", StaticFiles(directory=str(assets_dir)), name="static")


# ============================================================
# 页面路由
# ============================================================

@app.get("/register")
async def register_page():
    """开发者注册页面"""
    f = frontend_dir / "register.html"
    if not f.exists():
        raise HTTPException(status_code=404, detail="register.html 不存在")
    return FileResponse(str(f))


@app.get("/dashboard")
async def dashboard_page():
    """开发者面板"""
    f = frontend_dir / "dashboard.html"
    if not f.exists():
        raise HTTPException(status_code=404, detail="dashboard.html 不存在")
    return FileResponse(str(f))


@app.get("/")
async def root():
    """服务根信息"""
    return {
        "service": f"{ECOSYSTEM_NAME} · 月度主权开发者系统",
        "version": "2.0.0",
        "dna": ECOSYSTEM_DNA,
        "confirm": CONFIRM,
        "gpg": GPG,
        "fee_convention": MONTHLY_FEE_ANCHOR,
        "channels": available_channels(),
        "pages": {
            "register": "/register",
            "dashboard": "/dashboard",
            "fee_api": "/api/developer/bill",
            "fee_status": "/api/developer/fee-status",
            "fee_history": "/api/developer/fee-history",
            "fee_stats": "/api/ecosystem/fee-stats",
        },
        "status": "🟢 运行中",
    }


# ============================================================
# API 端点
# ============================================================

@app.post("/api/developer/register")
async def register_developer(req: DeveloperRegisterRequest):
    """开发者注册 → 生成DNA → 创建订单"""
    db = SessionLocal()
    try:
        # 检查邮箱是否已注册
        existing = db.query(Developer).filter(Developer.email == req.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="邮箱已被注册")

        # 生成开发者DNA
        dna = generate_developer_dna(req.name, req.email)

        # 创建开发者（待支付·首月免缴）
        dev = Developer(
            dna=dna,
            name=req.name,
            email=req.email,
            nickname=req.nickname,
            gpg_public_key=req.gpg_public_key,
            registered_at=datetime.now(),
            status="pending",
            is_enterprise=req.is_enterprise or False,
            fee_start_month=get_current_month(),
        )
        db.add(dev)
        db.commit()

        # 生成支付订单（首月费·正规网关链路）
        order = create_payment_order(dna, amount=req.amount or 1.0, channel=req.channel or "sandbox")

        return {
            "success": True,
            "dna": dna,
            "message": "注册成功，请完成首月费支付激活",
            "order": order,
            "developer": dev.to_dict(),
            "confirm": CONFIRM,
            "fee_convention": MONTHLY_FEE_ANCHOR,
        }
    finally:
        db.close()


@app.post("/api/sms/send-code")
async def send_sms_code_api(req: SmsSendRequest):
    """发送手机验证码（沙箱模式直接返回验证码·正式通道只换提供商标识）"""
    result = send_code(req.phone)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.post("/api/developer/phone-login")
async def phone_login_api(req: PhoneLoginRequest):
    """手机号+验证码 登录/注册（Kimi式：有账号直接进·没账号自动注册）
    首次（新手机号）返回 need_profile=true → 前端补昵称后二次提交即完成注册+首月费订单
    """
    v = verify_code(req.phone, req.code)
    if not v["success"]:
        raise HTTPException(status_code=400, detail=v["error"])

    db = SessionLocal()
    try:
        dev = db.query(Developer).filter(Developer.phone == req.phone).first()

        # 已有账号 → 直接登录（未激活则补发首月费订单）
        if dev:
            order = None
            if dev.status != "active":
                order = create_payment_order(dev.dna, amount=1.0, channel="sandbox")
            return {
                "success": True,
                "login": True,
                "existing": True,
                "developer": dev.to_dict(),
                "order": order,
                "message": "欢迎回来，手机号已绑定开发者身份",
                "confirm": CONFIRM,
            }

        # 新手机号：首次需补昵称（Kimi式一步注册）
        nickname = (req.nickname or "").strip()
        if not nickname:
            return {
                "success": True,
                "need_profile": True,
                "message": "首次使用，请完善昵称后确认加入",
            }

        name = nickname
        email = placeholder_email(req.phone)  # 占位邮箱（数据主权·不对外展示）
        dna = generate_developer_dna(name, email)
        dev = Developer(
            dna=dna,
            name=name,
            email=email,
            phone=req.phone,
            nickname=nickname,
            gpg_public_key=req.gpg_public_key,
            registered_at=datetime.now(),
            status="pending",
            is_enterprise=req.is_enterprise or False,
            fee_start_month=get_current_month(),
        )
        db.add(dev)
        db.commit()

        order = create_payment_order(dna, amount=1.0, channel="sandbox")
        return {
            "success": True,
            "login": True,
            "existing": False,
            "dna": dna,
            "message": "注册成功，请完成首月费支付激活",
            "order": order,
            "developer": dev.to_dict(),
            "confirm": CONFIRM,
            "fee_convention": MONTHLY_FEE_ANCHOR,
        }
    finally:
        db.close()


@app.post("/api/developer/pay")
async def confirm_payment_api(req: PaymentConfirmRequest):
    """确认支付激活（注册首月费·沙箱闭环/网关回调）"""
    result = confirm_payment(req.developer_dna, req.order_id or "", channel=req.channel or "sandbox")
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


# ============================================================
# 月度主权确认金 API（公约 v1.0）
# ============================================================

@app.post("/api/developer/bill")
async def monthly_bill_api(req: BillRequest):
    """生成当月账单（幂等）: 1元起步·上不封顶·自愿上浮"""
    db = SessionLocal()
    try:
        result = create_monthly_bill(req.developer_dna, db, amount=req.amount, channel=req.channel or "")
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        result["min_fee"] = 1.0
        result["slogan"] = "1元/月不是钱，是立场。上不封顶，是觉悟。杜绝一毛不拔。"
        return result
    finally:
        db.close()


@app.post("/api/developer/pay-monthly")
async def pay_monthly_api(req: PaymentConfirmRequest):
    """确认月费支付（沙箱模式本地闭环）"""
    db = SessionLocal()
    try:
        result = confirm_monthly_payment(req.developer_dna, req.order_id or "", db, channel=req.channel or "sandbox")
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    finally:
        db.close()


@app.post("/api/pay/notify")
async def pay_notify_api(req: PayNotifyRequest):
    """支付网关回调（正规链路·验签→幂等入账）"""
    db = SessionLocal()
    try:
        result = handle_payment_notify(req.params, req.signature, db, channel=req.channel or "")
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    finally:
        db.close()


@app.get("/api/developer/fee-status")
async def fee_status_api(dna: str):
    """查询月费状态（active/grace/frozen）"""
    db = SessionLocal()
    try:
        return check_developer_fee_status(dna, db)
    finally:
        db.close()


@app.get("/api/developer/fee-history")
async def fee_history_api(dna: str, limit: int = 12):
    """查询缴费历史账单"""
    db = SessionLocal()
    try:
        return get_fee_history(dna, db, limit)
    finally:
        db.close()


@app.get("/api/ecosystem/fee-stats")
async def fee_stats_api():
    """生态公开统计（公共贡献池·聚合）"""
    db = SessionLocal()
    try:
        return get_public_fee_stats(db)
    finally:
        db.close()


# ============================================================
# 导出 API（管理员 Token 鉴权 · 历史账单/贡献/代码DNA/名册）
# ============================================================

@app.get("/api/export/fee-records")
async def export_fee_api(token: str, format: str = "csv"):
    db = SessionLocal()
    try:
        return export_fee_records(db, token, format)
    finally:
        db.close()


@app.get("/api/export/contributions")
async def export_contrib_api(token: str, format: str = "csv"):
    db = SessionLocal()
    try:
        return export_contributions(db, token, format)
    finally:
        db.close()


@app.get("/api/export/code-dna")
async def export_codedna_api(token: str, format: str = "csv"):
    db = SessionLocal()
    try:
        return export_code_dna(db, token, format)
    finally:
        db.close()


@app.get("/api/export/developers")
async def export_devs_api(token: str, format: str = "csv"):
    db = SessionLocal()
    try:
        return export_developers(db, token, format)
    finally:
        db.close()


@app.get("/api/developer/{dna}")
async def get_developer(dna: str):
    """获取开发者信息"""
    db = SessionLocal()
    try:
        dev = db.query(Developer).filter(Developer.dna == dna).first()
        if not dev:
            raise HTTPException(status_code=404, detail="开发者不存在")
        return {"success": True, "developer": dev.to_dict()}
    finally:
        db.close()


@app.post("/api/code/inject")
async def inject_code_dna(req: CodeInjectRequest):
    """注入代码DNA：校验开发者 → 生成代码DNA → 登记 + 加贡献分"""
    db = SessionLocal()
    try:
        dev = db.query(Developer).filter(Developer.dna == req.developer_dna).first()
        if not dev:
            raise HTTPException(status_code=404, detail="开发者不存在")
        if dev.status != "active":
            raise HTTPException(status_code=403, detail="开发者未激活，请先完成首月费支付")

        # 月费状态闸（公约第四条）：宽限/冻结不可新注入DNA
        fee_status = check_developer_fee_status(req.developer_dna, db)
        if fee_status["status"] in ("grace", "frozen"):
            raise HTTPException(
                status_code=403,
                detail=f"月费状态 {fee_status['status']}: {fee_status['message']}。宽限/冻结期间代码可读，不可新注入DNA，请先补缴月费。",
            )

        # 生成代码DNA（路径+内容双因子，内容变则DNA变）
        code_dna = generate_code_dna(req.file_path, req.content)
        file_hash = hashlib.sha256(req.content.encode()).hexdigest()

        # 同路径重复注入：先冻结旧记录（不删除只冻结原则·仅限本开发者）
        old = db.query(CodeDNA).filter(
            CodeDNA.file_path == req.file_path,
            CodeDNA.developer_dna == req.developer_dna,
        ).all()
        for o in old:
            if o.file_hash != file_hash:
                o.file_path = f"{o.file_path}@{o.id}.v{datetime.now().strftime('%Y%m%d%H%M%S')}"
        # 同内容已登记（仅限同一开发者）→ 幂等跳过
        dup = db.query(CodeDNA).filter(
            CodeDNA.file_path == req.file_path,
            CodeDNA.file_hash == file_hash,
            CodeDNA.developer_dna == req.developer_dna,
        ).first()
        if dup:
            return {
                "success": True,
                "dna": dup.dna,
                "message": f"⏭️ 内容未变化，复用既有DNA: {dup.dna}",
                "file_path": req.file_path,
                "developer_dna": req.developer_dna,
                "duplicated": True,
            }

        code_record = CodeDNA(
            dna=code_dna,
            developer_dna=req.developer_dna,
            file_path=req.file_path,
            file_hash=file_hash,
            line_count=len(req.content.split("\n")),
            language=req.language or "unknown",
            created_at=datetime.now(),
        )
        db.add(code_record)

        # 增加贡献分与DNA计数
        dev.contribution_score += 1
        dev.dna_count += 1
        db.commit()

        # 记录贡献
        contrib_dna = generate_dna("CONTRIB")
        contrib = Contribution(
            developer_dna=req.developer_dna,
            contribution_type="code",
            content=f"注入代码 {req.file_path}",
            score=1,
            dna=contrib_dna,
        )
        db.add(contrib)
        db.commit()

        return {
            "success": True,
            "dna": code_dna,
            "message": f"✅ 代码DNA已注入: {code_dna}",
            "file_path": req.file_path,
            "developer_dna": req.developer_dna,
        }
    finally:
        db.close()


@app.get("/api/developer/{dna}/contributions")
async def get_contributions(dna: str):
    """获取开发者贡献记录"""
    db = SessionLocal()
    try:
        contribs = (
            db.query(Contribution)
            .filter(Contribution.developer_dna == dna)
            .order_by(Contribution.created_at.desc())
            .all()
        )
        return {
            "success": True,
            "count": len(contribs),
            "contributions": [c.to_dict() for c in contribs],
        }
    finally:
        db.close()


@app.get("/api/code/search")
async def search_code(developer_dna: str):
    """查询某开发者的所有代码DNA"""
    db = SessionLocal()
    try:
        codes = (
            db.query(CodeDNA)
            .filter(CodeDNA.developer_dna == developer_dna)
            .order_by(CodeDNA.created_at.desc())
            .all()
        )
        return {
            "success": True,
            "count": len(codes),
            "codes": [c.to_dict() for c in codes],
        }
    finally:
        db.close()


@app.get("/api/leaderboard")
async def leaderboard():
    """贡献榜（Top 50 开发者）"""
    db = SessionLocal()
    try:
        devs = (
            db.query(Developer)
            .filter(Developer.status == "active")
            .order_by(Developer.contribution_score.desc(), Developer.dna_count.desc())
            .limit(50)
            .all()
        )
        return {
            "success": True,
            "count": len(devs),
            "developers": [
                {
                    "nickname": d.nickname,
                    "dna": d.dna,
                    "contribution_score": d.contribution_score,
                    "dna_count": d.dna_count,
                }
                for d in devs
            ],
        }
    finally:
        db.close()


@app.get("/health")
async def health():
    return {"status": "ok", "service": "longhun-dev-ecosystem", "dna": ECOSYSTEM_DNA}


# ============================================================
# 启动
# ============================================================

if __name__ == "__main__":
    import uvicorn

    print(f"🐉 {ECOSYSTEM_NAME} · 月度主权开发者系统")
    print(f"   DNA: {ECOSYSTEM_DNA}")
    print(f"   确认码: {CONFIRM}")
    print("   🟢 服务启动: http://localhost:8800")
    uvicorn.run(app, host="0.0.0.0", port=8800)
