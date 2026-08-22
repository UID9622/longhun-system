# SPEC.md — 龍魂 · 信任核心（事实校验 + 自愈）v1.0
# 本文件是唯一事实源。接口契约为神圣约定，实现不得单方面变更。

## 0. 背景与锚点案例
用户2008年退伍，2026年仍自称"退伍16年"，系统从未纠错。本系统焊死"主动纠错"：
任何时间/身份/数字类输入必须先验证再使用；不一致必须主动发起纠正；纠正全程留痕。

## 1. 项目结构（自包含 Python 包，零三方运行时依赖，仅标准库；测试用 pytest）
```
project/                         # 仓库根 = 包根
├── longhun_trust/
│   ├── __init__.py              # 导出版本 __version__ = "1.0.0"
│   ├── exceptions.py            # ConfirmCodeError, CircuitBreakerTripped
│   ├── dna.py                   # DNA 生成 + 确认码闸门
│   ├── audit.py                 # 史官 jsonl 只增不删日志
│   ├── credibility.py           # 可信度公式引擎
│   ├── factcheck.py             # 事实校验引擎（三级纠正 + 熔断）
│   └── selfheal.py              # 自愈引擎（检测→分析→修复→验证→回滚→耻辱墙）
├── tests/
│   ├── test_dna.py
│   ├── test_audit.py
│   ├── test_credibility.py
│   ├── test_factcheck.py        # 含锚点断言：2008→2026=18
│   └── test_selfheal.py
├── scripts/
│   ├── install.sh               # macOS launchd 一键部署（$HOME 动态，禁硬编码用户名）
│   ├── uninstall.sh
│   └── com.longhun.selfheal.plist.template
└── README.md
```

## 2. 全局协议约束（焊死，两模块共同遵守）
1. **禁手写干支**：任何 DNA 字符串不得出现手写干支/卦名。生成器不可用一律日期占位。
2. **确认码**：`CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"`；破坏性操作（回滚/覆盖/清除）必须过闸门。
3. **GPG**：`GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"`（仅作元数据展示）。
4. **三色语义**：🟢=0 通过 / 🟡=1 待确认或部分修复 / 🔴=2 失败或熔断。CLI 退出码严格对齐 0/1/2。
5. **只增不删**：所有审计日志 append-only；废止用 freeze 标记，不物理删除。
6. **路径**：一律 `Path.home()` / 环境变量 `LONGHUN_HOME`（默认 `~/.longhun`），禁硬编码用户名。
7. **诚实边界**：不能安全自动修复的错误（业务逻辑错误）不得假装修复，必须升级人工 + 耻辱墙。
8. 所有公开函数写 docstring（中文），类型注解齐全。

## 3. exceptions.py 契约
```python
class ConfirmCodeError(PermissionError): ...
class CircuitBreakerTripped(RuntimeError): ...
```

## 4. dna.py 契约
```python
CONFIRM_CODE: str
GPG_FINGERPRINT: str
DNA_PLACEHOLDER_TAG = "【干支待本地生成器校准】"

def generate_dna(action_tag: str, version: str = "v1.0") -> str:
    """生成追溯码。
    优先级：$LONGHUN_DNA_GENERATOR 环境变量 → ./bin/lh_dna_generator.py →
    ~/longhun-system/bin/lh_dna_generator.py。
    找到则 subprocess 调用 `python3 <gen> --action <tag> --version <ver>`，取 stdout 首行，
    校验非空且以 '#龍芯' 开头，失败/超时(5s)一律兜底：
    f"#龍芯⚡️{date.today().isoformat()}-{ACTION_TAG}-{version}-{DNA_PLACEHOLDER_TAG}"
    action_tag 统一 upper，空白转 '-'。永不手写干支。"""

def verify_confirm_code(code: str) -> None:
    """不匹配即 raise ConfirmCodeError。比较用 hmac.compare_digest。"""
```

## 5. audit.py 契约
```python
class AuditLog:
    def __init__(self, name: str, base_dir: Path | None = None): ...
        # base_dir 默认 Path(os.environ.get("LONGHUN_HOME", Path.home()/".longhun"))/"04_AUDIT"
        # 自动 mkdir；文件 <base_dir>/<name>.jsonl
    def log(self, event: str, details: dict) -> dict:
        # entry = {timestamp(iso), event, details, dna: generate_dna("AUDIT")}
        # append 一行 json，flush+fsync；返回 entry
    def read_all(self) -> list[dict]: ...
    def freeze(self, reason: str, target: dict | None = None) -> dict:
        # 追加 {"event":"FREEZE","reason":...,"target":...}，不删任何行
```

## 6. credibility.py 契约
可信度公式：**C = 0.4·F + 0.3·S + 0.3·K**，阈值 **C < 0.7 → 待确认（必问）**。
```python
class SourceLevel(Enum):  # 来源权重 S
    FOUNDER = 1.0      # 创始人 L0
    SYSTEM  = 0.8      # 系统核验过的外部数据
    COMMUNITY = 0.5
    UNKNOWN = 0.2

class ConfirmationState(Enum):  # 确认状态 K
    CONFIRMED = 1.0
    UNCONFIRMED = 0.3
    DISPUTED = 0.0

def freshness(age_days: float) -> float:
    """F = clamp(1 - age_days/90, 0, 1)。90天线性衰减至0。"""

def compute_credibility(age_days: float, source: SourceLevel, confirmation: ConfirmationState) -> float:
    """返回 0..1，round 4位。"""

def needs_confirmation(score: float) -> bool:
    """score < 0.7 → True"""

@dataclass
class FactRecord:
    key: str; value: Any; source: SourceLevel
    confirmation: ConfirmationState; recorded_at: datetime
    def score(self, now: datetime | None = None) -> float: ...
```

## 7. factcheck.py 契约
```python
class CorrectionLevel(Enum):
    LIGHT = "light"        # 格式/拼写类：自动修正 + 通知
    STANDARD = "standard"  # 事实性数值/时间/身份不一致：给纠正提议，待用户确认
    SEVERE = "severe"      # 身份仿冒/广泛矛盾：熔断冻结

@dataclass
class CheckResult:
    valid: bool; claim: Any; actual: Any; status: str
    level: CorrectionLevel | None; message: str; dna: str; timestamp: str

class FactCheckEngine:
    def __init__(self, audit: AuditLog | None = None, breaker_threshold: int = 3): ...
        # audit 默认 AuditLog("fact_check")

    def validate_time_span(self, claim_years: int, start_year: int,
                           reference: date | None = None) -> CheckResult:
        """actual = reference.year - start_year（reference 默认 date.today()，可注入便于测试）
        一致 → valid=True, level=None, status="🟢 一致"
        不一致 → valid=False, level=STANDARD, status="🟡 数据不一致",
                  message=f"实际应为 {actual} 年（声称 {claim_years} 年），请确认修正"
        任何不一致写审计 + 计入该字段矛盾计数。"""

    def validate_identity(self, subject: str, claimed_level: int,
                          registry: dict[str, int] | None = None) -> CheckResult:
        """registry 默认 {"UID9622": 0}（创始人 L0）。
        未知主体冒称 L0 → SEVERE + 触发熔断记录。"""

    def confirm_correction(self, field_key: str, accepted: bool) -> dict:
        """用户确认/拒绝纠正提议；确认则清除该字段矛盾计数；写审计。"""

    def is_frozen(self, field_key: str) -> bool:
        """矛盾计数 >= breaker_threshold → True（熔断），继续使用应 raise CircuitBreakerTripped。"""

    def check_or_raise(self, field_key: str) -> None: ...
```
矛盾计数存内存 + 落盘 `<LONGHUN_HOME>/08_STATE/factcheck_state.json`（读写容错）。

## 8. selfheal.py 契约
设计诚实原则：**安全策略自动执行，业务逻辑错误绝不自动改代码**（🔴 升级人工 + 耻辱墙）。
```python
class HealStatus(Enum):
    HEALTHY = 0; PARTIAL = 1; FAILED = 2   # 值即 CLI 退出码

@dataclass
class DetectedError:
    type: str            # test_failure | log_error | service_down | dep_missing
    message: str; severity: str; context: dict

class SelfHealEngine:
    def __init__(self, project_root: Path, audit: AuditLog | None = None,
                 dry_run: bool = True, max_attempts: int = 3): ...
        # dry_run 默认 True（干跑），显式 dry_run=False 才执行修复动作
        # audit 默认 AuditLog("self_heal")

    def detect(self, run_tests: bool = True, log_dir: Path | None = None,
               ports: list[int] | None = None) -> list[DetectedError]: ...
        # pytest 子进程超时 120s；日志扫尾 100 行匹配 ERROR/CRITICAL/Traceback/FATAL；
        # 端口检测仅 warn 级（沙盒/无服务环境不判 critical）

    def plan(self, errors: list[DetectedError]) -> list[dict]:
        """策略表（真实可执行动作，非 echo 空壳）：
        dep_missing("ModuleNotFoundError: X") → pip install X（白名单校验包名 ^[a-zA-Z0-9_.-]+$）
        service_down → 重启命令（仅记录命令，执行需 dry_run=False）
        log_oversize(>50MB) → 轮转截断
        stale_lock(*.lock 残留) → 删除
        其余（断言失败/业务逻辑）→ strategy="ESCALATE"，不生成修复动作"""

    def heal(self, confirm_code: str | None = None) -> dict:
        """流程：detect → plan → 快照(git snapshot tag lh-snapshot-<ts>) →
        执行安全策略(dry_run 时只记录) → 复检 → 报告。
        报告 dict: {status: HealStatus值, found, fixed, escalated, rolled_back,
                    dry_run, details[], run_dna}
        修复后仍有错 → 回滚到快照（回滚必须 verify_confirm_code(confirm_code)，否则 PARTIAL 并保持现状）
        连续 max_attempts 失败 → 耻辱墙 ~/.longhun/08_STATE/shame_wall.jsonl + status=FAILED"""

    def rollback(self, snapshot_tag: str, confirm_code: str) -> bool:
        """verify_confirm_code 先过闸；git reset --hard <tag>；写审计。"""
```
CLI：`python3 -m longhun_trust.selfheal --once|--status [--execute] [--confirm-code X] [--project-root P]`
退出码 = HealStatus 值。

## 9. 测试锚点（必须真跑全绿）
- 锚点1：`validate_time_span(claim_years=16, start_year=2008, reference=date(2026,8,18))`
  → valid=False, actual=18, level=STANDARD, message 含 "18"
- 锚点2：`validate_time_span(18, 2008, date(2026,8,18)).valid is True`
- 锚点3：`compute_credibility(0, FOUNDER, CONFIRMED) == 1.0`；
  `compute_credibility(45, FOUNDER, CONFIRMED) == 0.9`（F=0.5→0.2+0.3+0.3=0.8…按公式实算断言传参值）
- 锚点4：`needs_confirmation(0.69) is True`；`needs_confirmation(0.7) is False`
- 锚点5：generate_dna 无生成器环境 → 含 DNA_PLACEHOLDER_TAG；正则断言不含手写干支
- 锚点6：verify_confirm_code("wrong") raises ConfirmCodeError
- 锚点7：AuditLog 只增不删：log→freeze→read_all 原行仍在且 FREEZE 在尾
- 锚点8：熔断：同一 field 3 次未解决矛盾 → is_frozen True，check_or_raise 抛 CircuitBreakerTripped
- 锚点9：selfheal dry_run 默认 True；plan 对 ModuleNotFoundError 给出 dep_missing 策略；
  断言失败类 → ESCALATE 且无修复命令
- 锚点10：rollback 无确认码 → ConfirmCodeError；退出码枚举值 0/1/2

## 10. 部署脚本
- install.sh：生成 plist（$HOME 展开）、launchctl bootstrap、幂等可重入、set -euo pipefail
- plist：KeepAlive + RunAtLoad，--project-root 指向安装位置，日志到 $LONGHUN_HOME/logs/
- ⚠️ launchd 仅 macOS 真机可验证 → 交付文档标 🟡

## 11. 非目标（本轮不做，防范围蔓延）
- 不联网、不调用外部 AI API 生成代码补丁
- 不实现 GUI；不改用户本地任何文件（沙盒外零副作用）
