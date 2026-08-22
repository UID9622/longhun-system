# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂生态 · 数据模型
DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-DEV-MODELS-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

import hashlib
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from .config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# 手机号占位邮箱域名（数据主权：不暴露真实手机号，占位邮箱不可对外展示）
PLACEHOLDER_EMAIL_DOMAIN = "longhun.local"


def placeholder_email(phone: str) -> str:
    """由手机号生成稳定占位邮箱（仅内部使用·不对外展示）"""
    return f"user{hashlib.sha256(phone.encode()).hexdigest()[:12]}@{PLACEHOLDER_EMAIL_DOMAIN}"


def mask_phone(phone: str) -> str:
    """手机号脱敏: 138****1234"""
    if phone and len(phone) == 11:
        return f"{phone[:3]}****{phone[-4:]}"
    return phone or ""


class Developer(Base):
    """开发者主表"""
    __tablename__ = "developers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dna = Column(String(128), unique=True, nullable=False)          # 开发者DNA
    name = Column(String(64), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    phone = Column(String(32), nullable=True)                       # 手机号（快捷登录·业务层保证唯一）
    nickname = Column(String(64), nullable=False)
    gpg_public_key = Column(Text, nullable=True)
    registered_at = Column(DateTime, default=datetime.now)
    paid_at = Column(DateTime, nullable=True)                       # 支付时间
    payment_amount = Column(Float, default=0.0)
    status = Column(String(20), default="active")                  # active / pending / suspended / revoked
    contribution_score = Column(Integer, default=0)                 # 贡献分
    dna_count = Column(Integer, default=0)                          # 生成的DNA数量

    # ---- 月度主权确认金（公约 v1.0）----
    monthly_fee_status = Column(String(20), default="active")       # active / grace / frozen
    last_paid_month = Column(String(7), nullable=True)              # 最近缴费月份 YYYY-MM
    fee_arrears = Column(Integer, default=0)                        # 欠费月数
    total_contributed = Column(Float, default=0.0)                  # 累计缴纳总额（元）
    fee_start_month = Column(String(7), nullable=True)              # 计费起始月（注册月免缴）
    is_enterprise = Column(Boolean, default=False)                  # 企业/机构标记（可自愿上浮）

    def to_dict(self):
        # 占位邮箱不对外展示（数据主权·手机号用户不暴露内部邮箱）
        email = None
        if self.email and not self.email.endswith(f"@{PLACEHOLDER_EMAIL_DOMAIN}"):
            email = self.email
        return {
            "id": self.id,
            "dna": self.dna,
            "name": self.name,
            "email": email,
            "phone": mask_phone(self.phone),
            "nickname": self.nickname,
            "gpg_public_key": bool(self.gpg_public_key),
            "registered_at": self.registered_at.isoformat() if self.registered_at else None,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "paid": self.paid_at is not None,
            "status": self.status,
            "contribution_score": self.contribution_score,
            "dna_count": self.dna_count,
            "monthly_fee_status": self.monthly_fee_status,
            "last_paid_month": self.last_paid_month,
            "fee_arrears": self.fee_arrears,
            "total_contributed": self.total_contributed,
            "fee_start_month": self.fee_start_month,
            "is_enterprise": self.is_enterprise,
        }


class CodeDNA(Base):
    """代码 DNA 登记表"""
    __tablename__ = "code_dna"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dna = Column(String(128), unique=True, nullable=False)          # 代码DNA
    developer_dna = Column(String(128), nullable=False)             # 关联开发者
    file_path = Column(String(512), nullable=False)
    file_hash = Column(String(64), nullable=False)                  # 文件内容哈希
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    line_count = Column(Integer, default=0)
    language = Column(String(32), nullable=True)

    def to_dict(self):
        return {
            "dna": self.dna,
            "developer_dna": self.developer_dna,
            "file_path": self.file_path,
            "file_hash": self.file_hash,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "line_count": self.line_count,
            "language": self.language,
        }


class Contribution(Base):
    """贡献记录表"""
    __tablename__ = "contributions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    developer_dna = Column(String(128), nullable=False)
    contribution_type = Column(String(32), nullable=False)          # code / protocol / doc / community / registration
    content = Column(Text, nullable=True)
    score = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    dna = Column(String(128), unique=True, nullable=False)

    def to_dict(self):
        return {
            "dna": self.dna,
            "developer_dna": self.developer_dna,
            "contribution_type": self.contribution_type,
            "content": self.content,
            "score": self.score,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class PaymentOrder(Base):
    """支付订单表（正规网关·持久化·可追溯）"""
    __tablename__ = "payment_orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String(64), unique=True, nullable=False)      # 商户订单号（幂等键）
    developer_dna = Column(String(128), nullable=False)
    amount = Column(Float, nullable=False)                          # 支付金额（元）
    channel = Column(String(16), default="sandbox")                 # wechat / alipay / cbpay / sandbox
    subject = Column(String(128), nullable=True)                    # 订单标题（如 "2026-08 月费"）
    status = Column(String(20), default="pending")                  # pending / paid / closed
    created_at = Column(DateTime, default=datetime.now)
    paid_at = Column(DateTime, nullable=True)
    notify_raw = Column(Text, nullable=True)                        # 网关回调原文（审计留痕）
    transaction_id = Column(String(64), nullable=True)              # 网关交易号

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "developer_dna": self.developer_dna,
            "amount": self.amount,
            "channel": self.channel,
            "subject": self.subject,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "transaction_id": self.transaction_id,
        }


class MonthlyFeeRecord(Base):
    """月度主权确认金记录表"""
    __tablename__ = "monthly_fee_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    developer_dna = Column(String(128), nullable=False)
    year_month = Column(String(7), nullable=False)                  # YYYY-MM
    amount = Column(Float, default=1.0)
    paid_at = Column(DateTime, nullable=True)
    status = Column(String(20), default="pending")                  # pending / paid / refunded
    order_id = Column(String(64), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "developer_dna": self.developer_dna,
            "year_month": self.year_month,
            "amount": self.amount,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "status": self.status,
            "order_id": self.order_id,
        }


def migrate():
    """轻量迁移（幂等）：developers 表补 phone 列（SQLite ALTER TABLE 不支持加 UNIQUE，业务层保证唯一）"""
    from sqlalchemy import inspect, text

    insp = inspect(engine)
    if "developers" in insp.get_table_names():
        cols = [c["name"] for c in insp.get_columns("developers")]
        if "phone" not in cols:
            with engine.begin() as conn:
                conn.execute(text("ALTER TABLE developers ADD COLUMN phone VARCHAR(32)"))
            print("[DB][migrate] developers.phone 列已补充")


def init_db():
    """初始化数据库（幂等）"""
    Base.metadata.create_all(engine)
    migrate()
