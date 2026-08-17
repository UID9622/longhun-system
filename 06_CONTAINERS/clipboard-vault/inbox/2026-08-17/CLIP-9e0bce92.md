---
dna: '#龍芯⚡️丙午·丙申·癸亥·辰时·䷸巽-CLIPBOARD-VAULT-SAVE-V1.0-P1-d4b45299'
source: clipboard
topic: 法律/主权
tags:
- Notion
- 审计
- 法律/主权
timestamp: '2026-08-17T08:30:56+08:00'
content_hash: 9e0bce9292fd5ef6e7412be5784ca2be685efcfb8878bff4ec5dbed48f94405b
parent_dna: []
vault_version: v1.0
---

# 剪贴内容

已完成「龍字规范化协议」落地与 basedpyright 收尾。                   
                                                                        
   已交付                                                               
                                                                        
   1. 龍字规范化守护程序                                                
                                                                        
   • 文件：08_BIN/lh_dragon_glyph_guard.py                              
   • 功能：                                                             
       • 简体 龙 → 繁体 龍                                              
       • 绝对保护 龍芯⚡️ 文化主权符号                                   
       • 英文品牌名 Dragon Soul / Longhun → LongHun                     
       • 保留小写 longhun-system 等仓库/包名                            
       • 默认排除 venv、site-packages、_work、_archive、_private 等外部/
         缓存目录                                                       
       • 干跑模式 + 备份 + JSON 审计报告                                
                                                                        
   2. 徽章套件已规范化落地                                              
                                                                        
   • 保存为：03_KNOWLEDGE_GRAPH/03_仓库徽章套件_☯UID9622·丙午·甲申·丁未·
     鼎-BADGE-SUITE-v1.1.md                                             
   • 该文件中所有简体 龙 已改为 龍，英文品牌已规范                      
   • README.md 顶部徽章区已同步替换为新套件（核心身份 / 快速入口 / 许可 
     证 / 技术栈 / 自动化 / 社区 / 主权宣言）                           
                                                                        
   3. 全仓库扫描结果                                                    
                                                                        
   执行一次全量规范化后：                                               
   • 处理文件：6360 个                                                  
   • 简体 龙 → 繁体 龍：133167 处                                       
   • 英文品牌规范化：9742 处                                            
   • 龍芯⚡️ 主权保护：224466 处                                         
                                                                        
   再次干跑验证：0 文件需要变更（非排除目录内）。                       
                                                                        
   4. basedpyright 收尾                                                 
                                                                        
   • cryptography 与 pytest 已确认安装在 .venv 中                       
   • bin/lh_base_trace_collector.py 已补文件级 pyright 忽略配置         
   • tests/test_code_audit.py、tests/test_smoke.py 的 import pytest 已有
     # type: ignore                                                     
   • 指定文件检查：0 errors, 0 warnings, 0 notes                        
   • 测试：9 passed, 4 skipped                                          
                                                                        
   还需要你手动做一件事                                                 
                                                                        
   VSCode 必须重新加载窗口，basedpyright 才会识别 .venv 配置：          
                                                                        
   Cmd + Shift + P → Developer: Reload Window                           
                                                                        
   已知边界                                                             
                                                                        
   • 未重命名文件/目录本身（如 龙魂Notion自动化系统 这类路径名），仅规范
     化文件内容；如需重命名路径，需要单独跑一轮 git mv 式批量重命名。   
   • _work、_archive、_private、venv、site-packages、11_DATA 内部分第三 
     方/抓取数据仍保留原样，未被修改。                                  
                                                                        
   全仓库 basedpyright 扫描正在后台继续跑，完成后会自动通知。

---

*归档于 2026-08-17T08:30:56+08:00 · DNA `#龍芯⚡️丙午·丙申·癸亥·辰时·䷸巽-CLIPBOARD-VAULT-SAVE-V1.0-P1-d4b45299`*
