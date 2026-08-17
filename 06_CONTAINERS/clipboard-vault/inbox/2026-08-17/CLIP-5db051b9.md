---
dna: '#龍芯⚡️丙午·丙申·癸亥·辰时·䷉履-CLIPBOARD-VAULT-SAVE-V1.0-P1-d7fff0f2'
source: clipboard
topic: 代码/脚本
tags:
- Python
- Bash
- 代码/脚本
timestamp: '2026-08-17T07:38:56+08:00'
content_hash: 5db051b9d5e6a9234bf103113d20e994465bc6a6b7d643ec4072343c2b6b9b42
parent_dna: []
vault_version: v1.0
---

# 剪贴内容

对的，你指出了一个关键问题：不能让中文成为计算机底座。底座应该是语言 
   无关的规范名（英文），中文只是其中一种人类友好别名。所有命令都应该支 
   持「规范英文名 + 设备本地语言别名」双轨并行。                        
                                                                        
   我已经在行业痛点治理系统上做了完整试点，可以复用到全系统。           
                                                                        
   现状                                                                 
                                                                        
   • 文件/模块名：混用（lh_industry_governance.py 英文 + L2_工具_媒体播 
     放器_...py 中文）                                                  
   • CLI 子命令：大多是英文，但用户文档是中文                           
   • 痛点名称：中文为主，计算机解析需要先映射                           
                                                                        
   已落地方案                                                           
                                                                        
   核心原则：英文为 canonical（机器稳定名），中文/其他语言为 alias（人类
   入口）。                                                             
                                                                        
   新增文件                                                             
                                                                        
   ┌─────────────────────────────────────┬─────────────────────────────┐
   │ 文件                                │ 用途                        │
   ├─────────────────────────────────────┼─────────────────────────────┤
   │ 08_BIN/lh_bilingual_router.py       │ 双语命令路由器              │
   ├─────────────────────────────────────┼─────────────────────────────┤
   │ config/bilingual_command_map.json   │ 中英映射表（命令 + 八大痛点 │
   │                                     │ ）                          │
   ├─────────────────────────────────────┼─────────────────────────────┤
   │ 已更新                              │ 注册双语路由器和映射表别名  │
   │ config/naming_alias_registry.json   │                             │
   ├─────────────────────────────────────┼─────────────────────────────┤
   │ 已更新                              │ CLI 和 dispatch 支持中英双  │
   │ 05_ENGINES/lh_industry_governance.p │ 语                          │
   │ y                                   │                             │
   ├─────────────────────────────────────┼─────────────────────────────┤
   │ 已更新                              │ REST API 支持中文痛点/动作  │
   │ 05_ENGINES/lh_governance_api.py     │                             │
   ├─────────────────────────────────────┼─────────────────────────────┤
   │ 已更新                              │ 新增 4 个双语测试           │
   │ 13_TESTS/test_industry_governance.p │                             │
   │ y                                   │                             │
   └─────────────────────────────────────┴─────────────────────────────┘
                                                                        
   映射表示例                                                           
                                                                        
   ```json                                                              
     {                                                                  
       "commands": {                                                    
         "assess": { "zh": ["评估","评价","诊断"], "en":                
   ["assess","evaluate"] },                                             
         "act":    { "zh": ["执行","行动","治理"], "en": ["act","do"] },
         "all-assess": { "zh": ["全评估","批量评估"], "en":             
   ["all-assess"] }                                                     
       },                                                               
       "pain_points": {                                                 
         "auto_factory": { "zh": ["AI落地高投入低回报","自动工厂"],     
   "en": ["auto_factory","ai-roi"] },                                   
         "shadow_ai":    { "zh": ["影子AI横行","影子AI"], "en":         
   ["shadow_ai","shadow-ai"] }                                          
       }                                                                
     }                                                                  
   ```                                                                  
                                                                        
   验证结果                                                             
                                                                        
   • pytest：18/18 passed                                               
   • CLI 中文命令：                                                     
     ```bash                                                            
       python3 05_ENGINES/lh_industry_governance.py 评估 数据主权       
       python3 05_ENGINES/lh_industry_governance.py 全评估              
     ```                                                                
     均正确执行并归一为英文规范名。                                     
   • API 中文调用：                                                     
     ```bash                                                            
       curl -X POST http://127.0.0.1:8781/assess \                      
         -d '{"pain_point":"影子AI","context":{"gateway_enabled":true}}'
       # 返回 pain_point: "shadow_ai"                                   
     ```                                                                
   • 命名检查：双语路由器与映射表文件已注册别名，不再被 lh naming check 
     标黄。                                                             
                                                                        
   用法示例                                                             
                                                                        
   ```bash                                                              
     # 解析任意别名                                                     
     python3 08_BIN/lh_bilingual_router.py 影子AI --category pain_points
     # 影子AI -> shadow_ai                                              
                                                                        
     # CLI 中文命令                                                     
     python3 05_ENGINES/lh_industry_governance.py 执行 数据主权         
   --context '{"local_storage":true}'                                   
     python3 05_ENGINES/lh_industry_governance.py 看板                  
                                                                        
     # API 中文                                                         
     curl -X POST http://127.0.0.1:8781/act \                           
       -H "Content-Type: application/json" \                            
       -d '{"pain_point":"数据主权","context":{"local_storage":true}}'  
   ```                                                                  
                                                                        
   扩展到全系统                                                         
                                                                        
   这套 lh_bilingual_router 已经通用化。下一步只需：                    
                                                                        
   1. 在 config/bilingual_command_map.json 的 commands 里追加其他命令的 
      别名                                                              
   2. 在各区 CLI 入口用 _cmd_router.resolve_command() 归一化子命令      
   3. 所有内部逻辑继续用英文规范名，不绑定任何自然语言                  
                                                                        
   这样无论是中文终端、英文 CI、鸿蒙设备还是鲲鹏服务器，都能用各自母语 +
   英文双轨调用，计算机底座始终保持语言中性。

---

*归档于 2026-08-17T07:38:56+08:00 · DNA `#龍芯⚡️丙午·丙申·癸亥·辰时·䷉履-CLIPBOARD-VAULT-SAVE-V1.0-P1-d7fff0f2`*
