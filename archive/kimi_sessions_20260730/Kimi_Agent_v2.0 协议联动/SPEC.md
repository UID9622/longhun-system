# SPEC · 龍魂联动桥 lh_tuner_bridge.py（单一事实源）

## 〇、铁律
1. 调节器本体（自适应调节器_v2.0.py）核心逻辑**一行不改**·只在 4 个发射点追加 hook 调用
2. 桥与适配器**全部 fail-isolated**：任何异常只记警告·绝不抛回调节器
3. DNA 一律走 bin/lh_dna_generator.py·禁止手写干支
4. 零新增第三方依赖（标准库 only）

## 一、文件布局（落点 governance/adaptive-tuner/bridge/）
```
bridge/
├── lh_tuner_bridge.py      # 事件总线 + 注册表加载 + 适配器调度（单文件）
└── README.md               # 联动说明
```
适配器内嵌于 lh_tuner_bridge.py（每适配器一个类·共 4 个·避免多文件碎片）

## 二、事件契约（焊死）
事件类型枚举（字符串）：
- `TUNE_SIMULATED` 模拟微调完成
- `TUNE_APPLIED` 落盘微调完成
- `TUNE_MELTDOWN` 红线熔断（dr∈{3,9}）
- `TUNE_ROLLBACK` 回滚完成
- `TUNE_AUDIT` 审计报告生成

事件载荷 schema（dict·键名焊死）：
```json
{
  "事件": "TUNE_APPLIED",
  "时间戳": "ISO8601毫秒",
  "DNA": "生成器输出或占位",
  "三色": "🟢|🟡|🔴",
  "dr": 7,
  "参数哈希": "...",
  "父哈希": "...",
  "调整数": 0,
  "调整记录": ["..."],
  "数据摘要": {"甩锅率":0.0,"自扛率":0.0,"没立正率":0.0,"威胁率":0.0,"补救率":0.0,"惯犯率":0.0},
  "趋势": {},
  "来源": "自适应调节器v2.0"
}
```

## 三、注册表契约 ~/.龍魂/聯動註冊表.json
```json
{
  "版本": "1.0",
  "引擎": {
    "rules_engine":  {"开关": true,  "超时秒": 5, "快照路径": "~/.龍魂/引擎態/rules_engine_params.json"},
    "audit":         {"开关": true,  "超时秒": 10, "审计模块路径": "skills/longhun-audit-integrated/longhun_audit_integrated.py", "仓库根": ""},
    "caolog":        {"开关": true,  "超时秒": 3, "草日誌目录": "~/.龍魂/草日誌"},
    "dna_registry":  {"开关": true,  "超时秒": 3, "登记册": "~/.龍魂/DNA登記冊.jsonl"}
  }
}
```
注册表缺席 → 桥自动写入上述默认值再使用。

## 四、适配器契约（每适配器一个类·方法签名焊死）
```python
class 适配器基类:
    名称: str
    def __init__(self, 配置: dict): ...
    def receive(self, 事件: dict) -> dict:   # 返回 {"状态":"🟢|🟡|🔴","说明":str}·自身吞异常
```

### 适配器 A · RulesEngineAdapter（规则引擎联动）
- 收 `TUNE_APPLIED` → 写参数快照到 快照路径：
  `{"更新时间","参数哈希","父哈希","三色","dr","参数":{自扛加分,逃避扣分,没立正扣分,补救加分,惯犯扣分,惯犯触发次数}}`
  （快照须从 ~/.龍魂/微調參數.json 现读·不从事件载荷猜）
- 收 `TUNE_MELTDOWN` → 快照同目录追加写 `rules_engine.LOCK.json`：`{"锁定":true,"原因","dr","时间戳"}`（规则引擎从严模式信号）
- 收 `TUNE_ROLLBACK` → 若 LOCK 存在则写 `{"锁定":false,...}` 解除

### 适配器 B · AuditAdapter（三色审计联动）
- 仅收 `TUNE_APPLIED`/`TUNE_ROLLBACK`
- 用 importlib.util.spec_from_file_location 懒加载 审计模块路径（仓库根 + 相对路径；仓库根为空则跳过并返回 🟡）
- 调 `LonghunIntegratedAudit().audit_script(参数JSON路径)` · 取 color → 写入 `~/.龍魂/引擎態/audit_crosscheck.json`：`{"调节器dr","审计color","一致":bool,"时间戳"}`
- 模块缺席/异常 → 🟡 跳过·绝不失败

### 适配器 C · CaoLogAdapter（草日志联动·对齐 LocalLogger 格式）
- 收全部 5 类事件
- 写 `草日誌目录/YYYY-MM-DD.log`（JSONL 追加）·记录格式：
  `{"时间戳":ISO毫秒,"类型":"tuner.<事件小写>","系统":"自适应调节器v2.0","DNA","三色","dr","参数哈希","父哈希","摘要":首条调整记录或状态}`
- 文件名与 LocalLogger 一致（YYYY-MM-DD.log）·无需 import 该引擎

### 适配器 D · DNARegistryAdapter（DNA 登记联动·§14 条款）
- 收 `TUNE_APPLIED`/`TUNE_ROLLBACK`/`TUNE_MELTDOWN`
- append `登记册`：`{"登记时间","DNA","事件","参数哈希","父哈希","链式存根":sha256(父哈希+参数哈希+DNA)[:16],"条款":"§14 自适应调节器哈希链"}`

## 五、桥本体 API（焊死）
```python
class 联动桥:
    def __init__(self, 注册表路径: str = "~/.龍魂/聯動註冊表.json"): ...
    def emit(self, 事件类型: str, 载荷: dict) -> list[dict]:
        """补齐事件契约字段 → 逐适配器分发（signal.alarm 不可用·用 concurrent.futures.ThreadPoolExecutor+timeout 实现超时）
        返回各适配器结果 [{"适配器","状态","说明"}]·永不抛异常"""
    def 自检(self) -> list[dict]:
        """每适配器发 TUNE_AUDIT 测试事件·返回结果表"""
def 取桥() -> 联动桥:
    """模块级单例·供调节器 hook 调用"""
```

## 六、调节器本体 hook（仅 4 处追加·try/except 包裹）
```python
def _发射联动(事件类型: str, 载荷: dict):
    """可选联动·桥缺席或异常零影响"""
    try:
        from pathlib import Path as _P
        import importlib.util as _iu
        桥文件 = _P(__file__).resolve().parent / "bridge" / "lh_tuner_bridge.py"
        if not 桥文件.is_file():
            return
        spec = _iu.spec_from_file_location("lh_tuner_bridge", 桥文件)
        mod = _iu.module_from_spec(spec); spec.loader.exec_module(mod)
        mod.取桥().emit(事件类型, 载荷)
    except Exception:
        pass
```
发射点：
1. `微调()` return 前：`TUNE_APPLIED`（非模拟且有落盘）/ `TUNE_SIMULATED`（模拟）/ `TUNE_MELTDOWN`（🔴熔断·含未落盘的熔断返回）
2. `回滚()` 成功 return 前：`TUNE_ROLLBACK`
3. `生成审计报告()` 末尾：`TUNE_AUDIT`
载荷从 微调结果 dict 直接取字段组装。

## 七、调节器 CLI 新增（追加·不改旧分支）
- `--link-status`：打印注册表 + 桥自检结果表
- （--link-test 合并进 --link-status 自检·不另设）

## 八、验收标准（Stage 4 实测项）
1. 旧 10 项实测不回归（analyze/simulate/apply/verify/rollback/熔断/demo）
2. --apply 后：rules snapshot 存在且参数值正确 · 草日誌当日 .log 有 tuner.tune_applied · DNA登記冊.jsonl 有 §14 记录且链式存根可复算
3. 熔断场景：rules_engine.LOCK.json 生成 · 草日誌有 tuner.tune_meltdown
4. 回滚后：LOCK 解除记录
5. 把某适配器配置改坏（路径指不存在）→ emit 返回该适配器 🟡/🔴 但调节器主流程 exit 0
6. --link-status 输出四适配器自检表
