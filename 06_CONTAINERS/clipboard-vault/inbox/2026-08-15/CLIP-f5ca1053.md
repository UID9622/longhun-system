---
dna: '#龍芯⚡️丙午·丙申·辛酉·酉时·䷃蒙-CLIPBOARD-VAULT-SAVE-V1.0-P1-689a4aba'
source: clipboard
topic: 代码/脚本
tags:
- Python
- Bash
- 龍魂
- 审计
- 代码/脚本
timestamp: '2026-08-15T17:08:32+08:00'
content_hash: f5ca105397890a162625aca8c6186de0e9054326e86340c3d94887361a331e91
parent_dna: []
vault_version: v1.0
---

# 剪贴内容

主权网关自动硬控协议已落地，并与别名映射环境对齐。                   
                                                                        
   已交付文件                                                           
                                                                        
   ┌─────────────────────┬──────────────────────────┬──────────────────┐
   │ 文件                │ 路径                     │ 说明             │
   ├─────────────────────┼──────────────────────────┼──────────────────┤
   │ 硬控配置            │ ~/.longhun/configs/gatew │ 超时、fallback   │
   │                     │ ay-hardcode.yaml         │ 链、耻辱墙、审计 │
   │                     │                          │ 路径             │
   ├─────────────────────┼──────────────────────────┼──────────────────┤
   │ 自动流引擎（规范名  │ 05_ENGINES/L1_引擎_自动  │ L1 引擎层        │
   │ ）                  │ 流_☯UID9622·丙午·丙申·辛 │                  │
   │                     │ 酉·丙申·䷉履.py          │                  │
   ├─────────────────────┼──────────────────────────┼──────────────────┤
   │ 自动流引擎（别名入  │ 05_ENGINES/lh_autoflow.p │ symlink → 规范名 │
   │ 口）                │ y                        │                  │
   ├─────────────────────┼──────────────────────────┼──────────────────┤
   │ 知识图谱            │ 03_KNOWLEDGE_GRAPH/03_龍 │ 协议文档         │
   │                     │ 魂主权网关自动硬控协议   │                  │
   │                     │ _☯UID9622·丙午·丙申·辛酉 │                  │
   │                     │ ·丙申·䷉履               │                  │
   │                     │ _SOVEREIGN-CTRL-v1.0.md  │                  │
   ├─────────────────────┼──────────────────────────┼──────────────────┤
   │ CNSH 知识库         │ 08_BIN/CNSH_知识库.json  │ 已追加主权网关条 │
   │                     │                          │ 目               │
   ├─────────────────────┼──────────────────────────┼──────────────────┤
   │ 别名注册表          │ config/naming_alias_regi │ 已注册           │
   │                     │ stry.json                │ lh_autoflow.py   │
   │                     │                          │ 别名             │
   └─────────────────────┴──────────────────────────┴──────────────────┘
                                                                        
   核心能力                                                             
                                                                        
   • 硬控超时：所有外部 AI 调用 5 秒超时，超则切换                      
   • 自动故障转移：kimi → deepseek → local_qwen → local_llama           
   • 拒绝审计：AI 拒绝执行 → 自动写入耻辱墙 + 切换                      
   • 耻辱墙：~/.longhun/08_STATE/shame_wall.jsonl                       
   • 本地兜底：全部外部 AI 失败时返回本地响应                           
   • 全链路审计：~/.longhun/04_AUDIT/sovereign_gateway.jsonl            
                                                                        
   实测结果                                                             
                                                                        
   ```bash                                                              
     ./05_ENGINES/lh_autoflow.py ask "龍魂系统状态检查"                 
     # → ✅ 命中: kimi                                                  
                                                                        
     ./05_ENGINES/lh_autoflow.py test-timeout                           
     # → ⏰ kimi 超时(5s) → ✅ 命中: deepseek，耻辱墙记录 timeout       
                                                                        
     ./05_ENGINES/lh_autoflow.py test-refuse                            
     # → 🧱 耻辱墙记录: kimi → refused → ✅ 命中: deepseek              
                                                                        
     ./05_ENGINES/lh_autoflow.py test-fail                              
     # → 全部外部AI失败 → 🛡️ 本地兜底                                   
   ```                                                                  
                                                                        
   命名合规                                                             
                                                                        
   • 已注册别名：lh_autoflow.py → 05_ENGINES/L1_引擎_自动流_...py [L1]  
   • python3 bin/lh_naming_engine.py alias 显示映射总数 5               
   • 同时修复了命名引擎对 Python shebang 的识别逻辑，.py 文件标识头可在 
     第二行，避免所有脚本被误报                                         
                                                                        
   老入口 ./05_ENGINES/lh_autoflow.py 可用，新规范名也已识别。

---

*归档于 2026-08-15T17:08:32+08:00 · DNA `#龍芯⚡️丙午·丙申·辛酉·酉时·䷃蒙-CLIPBOARD-VAULT-SAVE-V1.0-P1-689a4aba`*
