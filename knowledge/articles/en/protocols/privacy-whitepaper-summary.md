# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# The Privacy Whitepaper of the Longhun System

## Data Sovereignty, Local-First Architecture, and Five-Layer Data Black Hole Protocol

> **DNA:** `#龍芯⚡️2026-07-08-PRIVACY-WHITEPAPER-v2.0`  
> **CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-777L`  
> **Author:** UID9622 · 龍芯北辰  
> **Translation:** Executive Summary · 2026-07-21  
> **License:** CC BY-NC-SA 4.0

---

## Executive Summary

The Longhun System's privacy architecture is built on a single premise: **user data belongs to the user, not the platform.** Every technical decision flows from this principle.

This whitepaper (originally 8,000+ Chinese characters) defines the privacy architecture of the Longhun System. Key components:

---

## 1. Data Classification (D1-D4)

| Level | Label | Examples | Storage Rule |
|:---|:---|:---|:---|
| **D1** | Top Secret 🔴 | GPG private keys, DNA seeds, cryptographic roots | Never in cloud. Physical isolation. Request → auto meltdown. |
| **D2** | Confidential 🟠 | Full user profiles, behavioral patterns, location history | Local + end-to-end encrypted cloud backup (cloud stores ciphertext only) |
| **D3** | Internal 🟡 | Audit logs, system metrics, error traces | Cloud OK but all sensitive fields → `***MELTDOWN***` |
| **D4** | Public 🟢 | Documentation, open protocols, published research | Free flow |

---

## 2. Five-Layer Data Black Hole Protocol

Every component that handles user data must implement five layers of protection:

| Layer | Name | Rule |
|:---|:---|:---|
| **L0** | Frontend Sandbox | All user input processed in isolated browser context. No raw data transmitted. |
| **L1** | Hash-Only Transit | Only irreversible hashes cross network boundaries. Plaintext never in transit. |
| **L2** | Memory < 500ms | Plaintext data in RAM for < 500ms. Immediately overwritten after processing. |
| **L3** | Irreversible Storage | Only salted, hashed representations stored persistently. |
| **L4** | Log MELTDOWN | Logging of sensitive fields triggers automatic `***MELTDOWN***` replacement. |

---

## 3. Local-First Architecture

- User data lives on the user's device by default.
- Cloud sync is optional, opt-in, and always end-to-end encrypted.
- The user holds the encryption keys. The cloud holds only ciphertext.
- "Forgot password" cannot mean "the platform can still access your data."

---

## 4. Zero Default Opt-In

- No permission is granted by default.
- Every data-sharing permission requires explicit, informed consent.
- Consent must be granular (not bundled "all or nothing").
- Consent can be revoked, and revocation must be as easy as granting.

---

## 5. The Inducement Index (I ≤ 1)

Dark patterns that nudge users toward sharing more data are measured by the Inducement Index:

```
I = (number of dark patterns in consent flow) / (number of neutral choices available)

Requirement: I ≤ 1.0
```

If I > 1.0, the consent flow is manipulative and must be redesigned.

---

## 6. Data Deletion = Real Deletion

When a user requests data deletion:
- All copies are identified via DNA traceability markers.
- All copies are cryptographically overwritten (not just "unlinked").
- Deletion is verified and the user receives a signed deletion certificate.
- No "soft delete" where data is hidden but retained.

---

## 7. Jurisdictional Integrity

- User data governed by Chinese law is stored on servers in Chinese territory.
- Cross-border data transfer requires explicit user consent + regulatory approval.
- No automated routing of Chinese user data to foreign CDNs or servers.
- API calls that might route data outside China pass through the P77 Security Legion's export review.

---

## Why This Matters Globally

While written for Chinese jurisdiction, the principles in this whitepaper are universal:

- **Data ownership**: Your data, your keys, your rules.
- **Transparency**: You should know what data exists about you and where it lives.
- **Control**: You should be able to delete, export, or correct your data at any time.
- **Consent**: Nothing happens with your data without your explicit, informed permission.

These are not radical demands. They are the minimum conditions for digital dignity.

---

> **DNA:** `#龍芯⚡️2026-07-08-PRIVACY-WHITEPAPER-v2.0`  
> **CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-777L`  
> **Full protocol:** `01_protocols/LH-DATA-PRIVACY-v2.1.md`
