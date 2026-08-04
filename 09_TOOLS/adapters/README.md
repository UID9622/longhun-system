# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# lh_standard_adapter

> DNA: `#LongHun⚡️BingWu·GuiWei·JiaZi·ZiShi·䷾JiJi-ADAPTER-v1.0`
> Author: LongHun Core · UID9622
> License: CC BY-NC-SA 4.0

**LongHun Standard Adapter** — wrap any JSON payload with DNA traceability and seven-factor behavioral audit metadata.

This adapter is an **open-source shell tool**. It formats your data in the LongHun standard.
It does NOT contain core compiler logic, training scripts, or algorithm optimization code.

---

## Installation

```bash
pip install lh_standard_adapter

# Or from local:
cd tools/adapters
pip install -e .
```

## Quick Start

```python
from lh_standard_adapter import LongHunAdapter

# Create adapter with your identity
adapter = LongHunAdapter(uid="9622", device="HM-9622-001")

# Wrap any JSON payload
raw = {"code": "print('hello')", "language": "python"}

compliant = adapter.wrap(
    data=raw,
    task_type="code",
    persona="P04-Luban"
)

print(compliant["dna"])
# → #LongHun⚡️BingWu·GuiWei·JiaZi·WeiShi·䷝Li-ADAPTER-CODE-WRAP-V1.0-a3f8c1d9

# Validate the output
result = adapter.validate(compliant)
print(result["summary"])
# → ✅ VALID — 0 errors, 0 warnings
```

## One-Shot Usage

```python
from lh_standard_adapter import wrap

result = wrap(
    {"action": "deploy", "target": "portal"},
    task_type="deploy",
    persona="P14-Lvmeng"
)
```

## Output Format

```json
{
  "dna": "#LongHun⚡️BingWu·GuiWei·JiaZi·ZiShi·䷝Li-ADAPTER-CODE-WRAP-V1.0-a3f8c1d9",
  "audit": {
    "audit_version": "v1.0",
    "uid": "UID9622",
    "persona": "P04",
    "task_type": "code",
    "behavior_signature": {
      "P": "HasPromise",
      "F": "Fulfilled",
      "T": 0.0,
      "E": "Willing",
      "C": 0,
      "R": 0,
      "A": "Self",
      "X": "Genuine",
      "Y": "NoResponse",
      "Z": 1.0
    },
    "behavior_pattern": "MODE-StableDisciplined",
    "behavior_labels": [
      "7F-P-有承诺",
      "7F-F-已兑现",
      "7F-E-心甘情愿",
      "MODE-StableDisciplined"
    ],
    "color": "🟢",
    "timestamp": "2026-07-24T...",
    "payload_hash": "abcd1234ef567890"
  },
  "payload": { ... your original data ... },
  "meta": {
    "adapter_version": "1.0.0",
    "uid": "9622",
    "device": "HM-9622-001",
    "task_type": "code",
    "persona": "P04-Luban",
    "generated_at": "2026-07-24T...",
    "format": "longhun-v∞"
  }
}
```

## API Reference

### `LongHunAdapter(uid, device, locale)`

| Param | Type | Default | Description |
|:---|:---|:---|:---|
| `uid` | str | `"9622"` | User identifier |
| `device` | str | `"HM-9622-001"` | Device identifier |
| `locale` | str | `"Asia/Shanghai"` | Timezone locale |

### `.wrap(data, task_type, persona)`

| Param | Type | Default | Description |
|:---|:---|:---|:---|
| `data` | any | — | Raw payload (dict, list, or JSON-serializable) |
| `task_type` | str | `"default"` | Task category (code, deploy, audit, etc.) |
| `persona` | str | `"P04"` | Persona identifier (P04-Luban, P00-Wenxin, etc.) |

Returns: `dict` with `dna`, `audit`, `payload`, `meta` keys.

### `.validate(wrapped)`

Returns: `{"valid": bool, "errors": [...], "warnings": [...]}`

### `.get_schemas()`

Returns: `{"dna_schema": {...}, "audit_schema": {...}}`

## What's Open vs Closed

| Layer | Status | Content |
|:---|:---|:---|
| DNA Format | ✅ Open | v∞ format spec, field definitions, regeneration rules |
| Audit Schema | ✅ Open | JSON Schema, seven-factor field definitions |
| Reference Adapter | ✅ Open | This package (shell tool) |
| Validation Regex | ✅ Open | DNA and naming convention regex patterns |
| Behavior Labels | ✅ Open | Factor value mappings (Fulfilled, Willing, etc.) |
| Core Engine | 🔒 Protected | Compiler, training, hexagram mapping models |
| Scoring Formulas | 🔒 Protected | Credit score, confidence weights, neural network logic |
| GPG Private Keys | 🔒 Protected | Never network-exposed |

> **Principle: Open the standard. Guard the engine.**

## Testing

```bash
cd tools/adapters
python -m pytest tests/ -v

# Or directly:
python tests/test_dna_generator.py
python tests/test_audit_wrapper.py
python tests/test_validator.py
```

## Dependencies

`lh_standard_adapter` uses **Python standard library only**. Zero external dependencies.

## License

CC BY-NC-SA 4.0

- **BY**: Attribute to LongHun System Founder UID9622
- **NC**: Non-Commercial (core engine protection)
- **SA**: ShareAlike (derivatives must use same license)

---

Signed: LongHun Core · UID9622 · 龍芯北辰
