---
dna: '#龍芯⚡️丙午·丙申·辛酉·申时·䷺涣-CLIPBOARD-VAULT-SAVE-V1.0-P1-ca8968dd'
source: clipboard
topic: CNSH/龍魂
tags:
- Python
- Bash
- 龍魂
- DNA
- 审计
- CNSH/龍魂
timestamp: '2026-08-15T15:13:23+08:00'
content_hash: f45fac8084e6b34d11a25b7d3cab48bad372a9867258cb1675208f8152b47626
parent_dna: []
vault_version: v1.0
---

# 剪贴内容

● CNSH-Harness 插件套件已按参考方式落地，并接入龍魂统一入口。          
                                                                        
   完成内容：                                                           
                                                                        
   • 创建 packages/cnsh_suite/ 插件包（因 Python 包名不支持连字符，将规 
     格中的 cnsh-suite 目录改为 cnsh_suite）。                          
   • 实现全部模块：core.py / engine.py / tools.py / hooks.py / events.py
      / agents.py / cli.py / test_suite.py / setup.py / README.md。     
   • 修复原参考代码 3 处 bug：                                          
       • DNA 输出格式缺少 UID 前缀                                      
       • 三色审计 score = sum(...) 误用 sum                             
       • CNSH 变量替换模式缺少花括号，导致 ${变量} 无法替换             
   • 完整测试通过：python3 -m pytest packages/cnsh_suite/test_suite.py  
     -v → 9 passed。                                                    
   • 接入 bin/lh：新增 lh cnsh-suite / lh cnsh / lh cns 三个别名。      
   • 实测通过：生成 DNA、三色审计、执行 CNSH、查看状态。                
   • 协议与记录：                                                       
       • 01_protocols/LH-CNSH-HARNESS-v1.0.md                           
       • 02_執行記錄/2026-08-15-CNSH-HARNESS.md                         
   • 所有相关文件已 GPG 签名并验证通过。                                
                                                                        
   实测命令：                                                           
                                                                        
   ```bash                                                              
     # 测试                                                             
     python3 -m pytest packages/cnsh_suite/test_suite.py -v             
                                                                        
     # 通过 lh 入口使用                                                 
     lh cnsh-suite --command "生成DNA: 我的文档"                        
     lh cnsh --command "审计内容: 待审计内容"                           
     lh cns --command "运行CNSH: 输出 '你好，龍魂'"                     
     lh cnsh-suite --status                                             
                                                                        
     # 独立安装后使用                                                   
     cd ~/longhun-system/packages/cnsh_suite                            
     pip install -e .                                                   
     cnsh --command "生成DNA: 我的文档"

---

*归档于 2026-08-15T15:13:23+08:00 · DNA `#龍芯⚡️丙午·丙申·辛酉·申时·䷺涣-CLIPBOARD-VAULT-SAVE-V1.0-P1-ca8968dd`*
