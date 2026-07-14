# 🐉 龍魂系統 DNA 對齐審計報告

**DNA**: #龍芯⚡️2026-06-21-DNA-ALIGNMENT-AUDIT-v1.0
**時間**: 2026-06-21 13:38 CST
**掃描目錄**: `/Users/zuimeidedeyihan/longhun-system`
**狀態**: 🟢 良好

---

## 📊 全系統統計

| 指標 | 數值 | 狀態 |
|------|------|------|
| **核心文件無 DNA** | 1395 個 | 🟢 |
| **已關聯 DNA 文件** | 5185 個 | 🟢 |
| **DNA 重複** | 214 個 | 🔴 |
| **核心文件總數** | 6580 個 | - |
| **DNA 對齐率** | 78.8% | 🟢 |

---

## 📁 按文件類型統計

| 文件類型 | 總數 | 有DNA | 無DNA | 對齐率 |
|----------|------|-------|-------|--------|
| Markdown文檔 | 2308 | 2297 | 11 | 🟢 99.5% |
| 其他 | 1896 | 1659 | 237 | 🟢 87.5% |
| Python腳本 | 1735 | 700 | 1035 | 🟡 40.3% |
| JSON配置 | 216 | 144 | 72 | 🟡 66.7% |
| Shell腳本 | 128 | 128 | 0 | 🟢 100.0% |
| HTML | 110 | 108 | 2 | 🟢 98.2% |
| 文本文件 | 104 | 68 | 36 | 🟡 65.4% |
| JavaScript | 57 | 55 | 2 | 🟢 96.5% |
| TypeScript | 13 | 13 | 0 | 🟢 100.0% |
| CSS | 8 | 8 | 0 | 🟢 100.0% |
| YAML配置 | 5 | 5 | 0 | 🟢 100.0% |

## 🔴 DNA 重複問題

發現 **214** 個DNA被多個文件共享:

🔴 **1.** `#龍芯⚡️2026-06-21-CNSH-UNNAMED-v1.0` → **139** 個文件
   - `releases/v5.1/staging/cnsh/flow_decision/tests/__init__.py`
   - `releases/v5.1/staging/cnsh/tests/__init__.py`
   - `cnsh/flow_decision/tests/__init__.py`
   - `cnsh/tests/__init__.py`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CNSH-DragonSoul-Complete/dragonsoul_terminal/__init__.py.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CNSH-DragonSoul-Complete/dragonsoul_terminal/backend/__init__.py.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CNSH-DragonSoul-Complete/security_core/__init__.py.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/stylegan3-main 2/metrics/__init__.py.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/stylegan3-main 2/torch_utils/__init__.py.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/stylegan3-main 2/torch_utils/ops/__init__.py.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/stylegan3-main 2/training/__init__.py.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/stylegan3-main 2/viz/__init__.py.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/stylegan3-main 2/dnnlib/__init__.py.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/stylegan3-main 2/gui_utils/__init__.py.bak`
   - `_archive/cnsh-history/CNSH-整理版/严肃沟通/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/严肃沟通/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/严肃沟通/_索引.md.sig`
   - `_archive/cnsh-history/CNSH-整理版/工具配置/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/工具配置/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/产品文档类/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/产品文档类/_完整索引.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/产品文档类/_完整清单.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/产品文档类/_完整清单.md.sig`
   - `_archive/cnsh-history/CNSH-整理版/产品文档类/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/产品文档类/_索引.md.sig`
   - `_archive/cnsh-history/CNSH-整理版/系统保护/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/系统保护/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/数据库页面/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/数据库页面/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/人格-宝宝/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/人格-宝宝/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/人格-宝宝/_索引.md.sig`
   - `_archive/cnsh-history/CNSH-整理版/项目发布/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/项目发布/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/数据分析/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/数据分析/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/其他类/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/其他类/_完整索引.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/其他类/_完整清单.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/其他类/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/架构设计/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/架构设计/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/AI智能/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/AI智能/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/开发环境/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/开发环境/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/龍魂系统/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/龍魂系统/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/知识库/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/知识库/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/价值体系/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/价值体系/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/人格-雯雯/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/人格-雯雯/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/人格-雯雯/_索引.md.sig`
   - `_archive/cnsh-history/CNSH-整理版/阅读学习/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/阅读学习/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/核心价值/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/核心价值/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/情感支持/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/情感支持/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/问题解决/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/问题解决/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/用户服务/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/用户服务/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/快速执行/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/快速执行/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/目标规划/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/目标规划/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/无标题页面/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/无标题页面/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/资源打包/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/资源打包/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/安全防护/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/安全防护/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/代码类/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/代码类/_完整索引.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/代码类/_完整清单.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/代码类/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/全球化/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/全球化/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/法律合规/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/法律合规/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/块级页面/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/块级页面/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/设计创作/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/设计创作/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/对话交流/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/对话交流/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/人格系统/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/人格系统/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/人格系统/_索引.md.sig`
   - `_archive/cnsh-history/CNSH-整理版/日常对话/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/日常对话/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/角色扮演/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/角色扮演/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/创意想法/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/创意想法/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/道德经/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/道德经/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/数据管理/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/数据管理/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/网络服务/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/网络服务/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/增长分析/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/增长分析/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/论文类/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/论文类/_完整索引.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/论文类/_完整清单.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/论文类/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/DNA追溯/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/DNA追溯/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/想法讨论/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/想法讨论/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/系统设置/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/系统设置/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/子页面/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/子页面/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/翻译系统/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/翻译系统/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/监控系统/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/监控系统/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/人格-Lucky/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/人格-Lucky/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/人格-Lucky/_索引.md.sig`
   - `_archive/cnsh-history/CNSH-整理版/任务清单/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/任务清单/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/文档笔记/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/文档笔记/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/技术研究/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/技术研究/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/核心控制/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/核心控制/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/工作区页面/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/工作区页面/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/安全加密/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/安全加密/_索引.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/同步备份/_INDEX.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/同步备份/_索引.md.bak`

🔴 **2.** `#龍芯⚡️2026-06-21-CNSH-README-MD-v1.0` → **106** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/README.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/git-extensions/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/龍魂永世唯一身份系统/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/tools/quantize/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/tools/batched-bench/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/tools/cvector-generator/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/tools/mtmd/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/tools/export-lora/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/tools/server/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/tools/server/bench/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/tools/server/tests/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/tools/server/webui/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/tools/server/themes/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/tools/server/themes/buttons-top/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/tools/server/themes/wild/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/tools/server/public_simplechat/readme.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/tools/imatrix/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/tools/perplexity/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/tools/gguf-split/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/tools/llama-bench/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/tools/tts/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/tools/run/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/tools/rpc/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/tools/main/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/ci/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/gguf-py/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/models/templates/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/docs/backend/hexagon/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/grammars/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/convert-llama2c-to-ggml/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/gguf-hash/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/eval-callback/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/parallel/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/lookahead/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/passkey/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/model-conversion/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/simple-cmake-pkg/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/batched/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/training/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/embedding/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/lookup/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/diffusion/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/batched.swift/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/simple/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.swiftui/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/retrieval/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/sycl/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/simple-chat/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.android/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/speculative/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/speculative-simple/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/deprecation-warning/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/legal-knowledge/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/ecny-global-system/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/ecny-global-system/blockchain/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/龍魂Notion自动化系统/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/README.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/README.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251204055052/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251205041543/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251207144453/CNSH_SecureSpace/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251207144453/MulanNotion/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251207144453/cnsh-uid9622-system/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251207144453/cnsh-uid9622-system/api-server/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251207144453/DNA_MATE_System/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251207144453/CNSH_DNA_Audit_System/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251207144453/notion_api_starter/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251207144453/CNSH_IDE_and_Compiler/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130124719/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251205214827/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/U盘文件解压后/UID9622_Starter_Packet/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/ai-security-toolkit/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/五大后台自运行人格配置/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/zhugeliang-digital/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/19bd8da9-1792-8267-8000-093407b99859/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/LU-Taiji-Bundle/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/LU-Taiji-Bundle/docs/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/UID9622-LocalServer/README.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/UID9622-LocalServer/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/UID9622-LocalServer/UID9622-WorldSystem/README.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/UID9622-LocalServer/UID9622-WorldSystem/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/sync-setup/README.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/sync-setup/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/cnsh-project/README.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/cnsh-project/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/docs/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/BaoBao-AI-Assistant/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/templates/README.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/dev-tools/README.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/dev-tools/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/anti-fraud-sentinel/README.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/龍芯龍魂/README.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/README.md.sig`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/stylegan3-main 2/README.md.sig`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/stylegan3-main 2/README.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/README.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/packages/dragon_soul_extension/README.md.sig`
   - `_archive/cnsh-history/CNSH-整理版/packages/dragon_soul_extension/README.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/packages/dragon_soul_extension/assets/icons/README.md.sig`
   - `_archive/cnsh-history/CNSH-整理版/packages/dragon_soul_extension/assets/icons/README.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/packages/cnsh-editor/README.md.bak`

🔴 **3.** `#龍芯⚡️2026-06-21-CORE-UNNAMED-v1.0` → **16** 個文件
   - `cnsh-core.backup/wuxing_calculator/__init__.py`
   - `cnsh-core.backup/identity/__init__.py`
   - `cnsh-core.backup/scheduler/__init__.py`
   - `cnsh-core.backup/mathematics/__init__.py`
   - `cnsh-core.backup/permissions/__init__.py`
   - `cnsh-core.backup/constitution/__init__.py`
   - `cnsh-core.backup/dna/__init__.py`
   - `cnsh-core.backup/logging/__init__.py`
   - `cnsh-core/wuxing_calculator/__init__.py`
   - `cnsh-core/identity/__init__.py`
   - `cnsh-core/scheduler/__init__.py`
   - `cnsh-core/mathematics/__init__.py`
   - `cnsh-core/permissions/__init__.py`
   - `cnsh-core/constitution/__init__.py`
   - `cnsh-core/dna/__init__.py`
   - `cnsh-core/logging/__init__.py`

🔴 **4.** `#龍芯⚡️2026-06-21-ENGINE-UNNAMED-v1.0` → **15** 個文件
   - `__init__.py`
   - `releases/v5.1/staging/xpay/__init__.py`
   - `releases/v5.1/staging/xpay/src/__init__.py`
   - `releases/v5.1/staging/xpay/src/adapters/__init__.py`
   - `xpay/__init__.py`
   - `xpay/src/__init__.py`
   - `xpay/src/adapters/__init__.py`
   - `integrated-modules/skills.integrated/__init__.py`
   - `integrated-modules/longhun_logging/__init__.py`
   - `integrated-modules/longhun_config/__init__.py`
   - `integrated-modules/sync/__init__.py`
   - `integrated-modules/monitoring/__init__.py`
   - `integrated-modules/gateway/__init__.py`
   - `integrated-modules/kimi_agent/__init__.py`
   - `monitoring/__init__.py`

🔴 **5.** `#龍芯⚡️2026-06-21-DOC-README-v1.0` → **11** 個文件
   - `README.md`
   - `releases/v5.1/staging/README.md`
   - `releases/v5.1/staging/desktop/README.md`
   - `desktop/README.md`
   - `docs/dragon-soul-open-hub/README.md`
   - `docs/dragon-soul-philosophy/README.md`
   - `docs/claude-backlog/07_开源模板/README.md`
   - `docs/uid9622-hosted/README.md`
   - `docs/yixuetang/README.md`
   - `docs/longhun-tech/README.md`
   - `vault/README.md`

🔴 **6.** `#龍芯⚡️2026-06-21-CNSH-CONTRIBUTING-MD-v1.0` → **10** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CONTRIBUTING.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/龍魂永世唯一身份系统/docs/CONTRIBUTING.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/CONTRIBUTING.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/ecny-global-system/CONTRIBUTING.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251207144453/MulanNotion/CONTRIBUTING.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130124719/CONTRIBUTING.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251205214827/CONTRIBUTING.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/cnsh-project/CONTRIBUTING.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/cnsh-project/CONTRIBUTING.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/BaoBao-AI-Assistant/CONTRIBUTING.md.bak`

🔴 **7.** `#龍芯⚡️2026-06-21-UI-INDEX-v1.0` → **9** 個文件
   - `baobao-guardian/frontend/index.html`
   - `baobao-guardian/public/wuxing-dashboard/index.html`
   - `releases/v5.1/staging/baobao-guardian/frontend/index.html`
   - `releases/v5.1/staging/baobao-guardian/public/wuxing-dashboard/index.html`
   - `releases/v5.1/staging/control-panel/static/index.html`
   - `phase3/frontend/public/index.html`
   - `ops-console/index.html`
   - `control-panel/static/index.html`
   - `sovereignty/portal/static/index.html`

🔴 **8.** ` #龍芯⚡️2026-05-24-22:57-CNSH-RUNTIME-ACCESS-v2.0` → **8** 個文件
   - `releases/v5.1/staging/protocols/_DEPRECATED_CNSH_v2.0_v3.0_2026-06-08/CNSH_v2.0_ROOT_PROTOCOL.md`
   - `releases/v5.1/staging/protocols/_DEPRECATED_CNSH_v2.0_v3.0_2026-06-08/CNSH_v2.0_ROOT_PROTOCOL_BILINGUAL.md`
   - `releases/v5.1/staging/protocols/_archive/v2.0_2026-06-07/CNSH_v2.0_ROOT_PROTOCOL.md`
   - `releases/v5.1/staging/protocols/_archive/v2.0_2026-06-07/CNSH_v2.0_ROOT_PROTOCOL_BILINGUAL.md`
   - `protocols/_DEPRECATED_CNSH_v2.0_v3.0_2026-06-08/CNSH_v2.0_ROOT_PROTOCOL.md`
   - `protocols/_DEPRECATED_CNSH_v2.0_v3.0_2026-06-08/CNSH_v2.0_ROOT_PROTOCOL_BILINGUAL.md`
   - `protocols/_archive/v2.0_2026-06-07/CNSH_v2.0_ROOT_PROTOCOL.md`
   - `protocols/_archive/v2.0_2026-06-07/CNSH_v2.0_ROOT_PROTOCOL_BILINGUAL.md`

🔴 **9.** `#龍芯⚡️2026-06-21-CNSH-LICENSE-MD-v1.0` → **7** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/dna_training_env/lib/python3.14/site-packages/uvicorn-0.38.0.dist-info/licenses/LICENSE.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/dna_training_env/lib/python3.14/site-packages/pip-25.3.dist-info/licenses/src/pip/_vendor/idna/LICENSE.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/dna_training_env/lib/python3.14/site-packages/idna-3.11.dist-info/licenses/LICENSE.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/dna_training_env/lib/python3.14/site-packages/pip/_vendor/idna/LICENSE.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/dna_training_env/lib/python3.14/site-packages/starlette-0.50.0.dist-info/licenses/LICENSE.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/cnsh-project/LICENSE.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/cnsh-project/LICENSE.md.sig`

🔴 **10.** `#龍芯⚡️2026-06-21-CNSH-HELLO-v1.0` → **6** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/hello.longhun`
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-v1.0-完整实现/hello.cnsh`
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-v1.0-完整实现/hello`
   - `_archive/cnsh-history/CNSH_备份_20260211/19bd8da9-1792-8267-8000-093407b99859/hello.longhun`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/hello.cnsh`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/hello`

🔴 **11.** `#龍芯⚡️2026-06-21-CNSH-LICENSE-v1.0` → **6** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/dna_training_env/lib/python3.14/site-packages/uvicorn-0.38.0.dist-info/licenses/LICENSE.md`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/dna_training_env/lib/python3.14/site-packages/pip-25.3.dist-info/licenses/src/pip/_vendor/idna/LICENSE.md`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/dna_training_env/lib/python3.14/site-packages/idna-3.11.dist-info/licenses/LICENSE.md`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/dna_training_env/lib/python3.14/site-packages/pip/_vendor/idna/LICENSE.md`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/dna_training_env/lib/python3.14/site-packages/starlette-0.50.0.dist-info/licenses/LICENSE.md`
   - `_archive/cnsh-history/CNSH-整理版/LICENSE`

🔴 **12.** `#龍芯⚡️2026-06-21-CNSH-CHANGELOG-MD-v1.0` → **5** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CHANGELOG.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/CHANGELOG.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130124719/CHANGELOG.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/CHANGELOG.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/CHANGELOG.md.bak`

🔴 **13.** `#龍芯⚡️2026-06-21-CNSH-IC_LAUNCHER-v1.0` → **5** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.android/app/src/main/res/mipmap-mdpi/ic_launcher.webp`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.android/app/src/main/res/mipmap-hdpi/ic_launcher.webp`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.webp`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.android/app/src/main/res/mipmap-xxhdpi/ic_launcher.webp`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.android/app/src/main/res/mipmap-xhdpi/ic_launcher.webp`

🔴 **14.** `#龍芯⚡️2026-06-21-CNSH-IC_LAUNCHER_ROUND-v1.0` → **5** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.android/app/src/main/res/mipmap-mdpi/ic_launcher_round.webp`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.android/app/src/main/res/mipmap-hdpi/ic_launcher_round.webp`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.android/app/src/main/res/mipmap-xxxhdpi/ic_launcher_round.webp`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.android/app/src/main/res/mipmap-xxhdpi/ic_launcher_round.webp`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.android/app/src/main/res/mipmap-xhdpi/ic_launcher_round.webp`

🟡 **15.** `#龍芯⚡️2026-06-21-DOC-REQUIREMENTS-v1.0` → **4** 個文件
   - `baobao-guardian/backend/requirements.txt`
   - `releases/v5.1/staging/baobao-guardian/backend/requirements.txt`
   - `releases/v5.1/staging/control-panel/requirements.txt`
   - `control-panel/requirements.txt`

🟡 **16.** `#龍芯⚡️2026-06-21-PROTOCOL-CNSH_V3-0_COMPLETE_CHARTER-v1.0` → **4** 個文件
   - `releases/v5.1/staging/protocols/CNSH_v3.0_COMPLETE_CHARTER.epub`
   - `releases/v5.1/staging/protocols/CNSH_v3.0_COMPLETE_CHARTER.docx`
   - `protocols/CNSH_v3.0_COMPLETE_CHARTER.epub`
   - `protocols/CNSH_v3.0_COMPLETE_CHARTER.docx`

🟡 **17.** `#龍芯⚡️2026-06-21-CORE-HELLO-v1.0` → **4** 個文件
   - `cnsh-core.backup/language/hello.cnsh`
   - `cnsh-core.backup/language/hello`
   - `cnsh-core/language/hello.cnsh`
   - `cnsh-core/language/hello`

🟡 **18.** `#龍芯⚡️2026-06-21-CNSH-INDEX-HTML-v1.0` → **4** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH编辑器_普惠版/index.html.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH编辑器/index.html.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/CNSH编辑器_普惠版/index.html.bak`
   - `_archive/cnsh-history/CNSH-整理版/packages/cnsh-editor/index.html.bak`

🟡 **19.** `#龍芯⚡️2026-06-21-CNSH-ARTICLE_TEMPLATE-MD-v1.0` → **4** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/templates/article_template.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/templates/article_template.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/templates/combat-ready/article_template.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/templates/combat-ready/article_template.md.sig`

🟡 **20.** `#龍芯⚡️2026-06-06-THREE-INTEGRATION-SYNC-HUB-v1.0` → **3** 個文件
   - `releases/v5.1/staging/cnsh/sancai_sync/README.md`
   - `releases/v5.1/staging/cnsh/sancai_sync/sancai_sync_hub.py`
   - `cnsh/sancai_sync/README.md`

🟡 **21.** `#龍芯⚡️2026-06-21-CNSH-REQUIREMENTS-v1.0` → **3** 個文件
   - `releases/v5.1/staging/cnsh-terminal/requirements.txt`
   - `cnsh_terminal_v5.0/requirements.txt`
   - `cnsh-terminal/requirements.txt`

🟡 **22.** `#龍芯⚡️2026-06-21-CNSH-TEST-v1.0` → **3** 個文件
   - `releases/v5.1/staging/cnsh-terminal/test.cnsh`
   - `cnsh_terminal_v5.0/test.cnsh`
   - `cnsh-terminal/test.cnsh`

🟡 **23.** ` #龍芯⚡️2026-06-21-CNSH-TERMINOLOGY-v1.0` → **3** 個文件
   - `releases/v5.1/staging/cnsh-terminal/data/terminology.db`
   - `cnsh_terminal_v5.0/data/terminology.db`
   - `cnsh-terminal/data/terminology.db`

🟡 **24.** `#龍芯⚡️2026-06-21-UI-SKILL-4-DOC-COAUTHORING-v1.0` → **3** 個文件
   - `releases/v5.1/staging/skills/html-skills/skill-4-doc-coauthoring.html`
   - `skills.backup/html-skills/skill-4-doc-coauthoring.html`
   - `skills/html-skills/skill-4-doc-coauthoring.html`

🟡 **25.** `#龍芯⚡️2026-06-21-UI-SKILL-3-CANVAS-DESIGN-v1.0` → **3** 個文件
   - `releases/v5.1/staging/skills/html-skills/skill-3-canvas-design.html`
   - `skills.backup/html-skills/skill-3-canvas-design.html`
   - `skills/html-skills/skill-3-canvas-design.html`

🟡 **26.** `#龍芯⚡️2026-06-06-KIMI-WEBBRIDGE-FILE1-v1.0` → **3** 個文件
   - `03_知識圖譜/graph_data.json`
   - `06_技術文檔/skill_kimi-webbridge.md`
   - `01_技能庫/kimi-webbridge.md`

🟡 **27.** `#龍芯⚡️2026-06-21-CNSH-CODE_OF_CONDUCT-MD-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CODE_OF_CONDUCT.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/cnsh-project/CODE_OF_CONDUCT.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/cnsh-project/CODE_OF_CONDUCT.md.bak`

🟡 **28.** `#龍芯⚡️2026-06-21-CNSH-TO_PUBLISH-MD-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/to_publish.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/to_publish.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251207144453/to_publish.md.bak`

🟡 **29.** `#龍芯⚡️2026-06-21-CNSH-API-MD-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/龍魂永世唯一身份系统/docs/API.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130124719/API.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/BaoBao-AI-Assistant/docs/api.md.bak`

🟡 **30.** `#龍芯⚡️2026-06-21-CNSH-INSTALL-MD-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/docs/install.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/ecny-global-system/INSTALL.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/packages/dragon_soul_extension/INSTALL.md.bak`

🟡 **31.** `#龍芯⚡️2026-06-21-CNSH-PROJECT_SUMMARY-MD-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/ecny-global-system/PROJECT_SUMMARY.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/PROJECT_SUMMARY.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/packages/dragon_soul_extension/PROJECT_SUMMARY.md.bak`

🟡 **32.** `#龍芯⚡️2026-06-21-CNSH-CNSH_AUDIO_RENDER_V1-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/龍魂系统核心/cnsh_audio_render_v1.cnsh_副本`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/龍魂系统核心/cnsh_audio_render_v1.cnsh`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/龍魂系统核心/files/cnsh_audio_render_v1.cnsh`

🔵 **33.** `#龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-v2.0` → **2** 個文件
   - `SESSION_SUMMARY_20260603.md`
   - `_archive/cnsh-history/CNSH_备份_20260211/.claude.json`

🔵 **34.** `#龍芯⚡️2026-06-07-BRAIN-NOTION-SYNC-FILE3-v1.1` → **2** 個文件
   - `brain_notion_sync.py`
   - `brain/brain_notion_sync.py`

🔵 **35.** `#龍芯⚡️2026-06-21-DOC-ATTRIBUTION-v1.0` → **2** 個文件
   - `ATTRIBUTION.md`
   - `docs/claude-backlog/07_开源模板/ATTRIBUTION.md`

🔵 **36.** `#龍芯⚡️2026-06-08-GRAFANA-DASHBOARD-CONFIG-FILE1-v1.0` → **2** 個文件
   - `DASHBOARD_TEST_CONFIRMATION.md`
   - `monitoring/grafana_dashboard_config.json`

🔵 **37.** `#龍芯⚡️2026-06-21-UI-PERSONA_CERT_TEMPLATE-v1.0` → **2** 個文件
   - `persona_cert_template.html`
   - `docs/persona_cert_template.html`

🔵 **38.** `#龍芯⚡️2026-06-21-ENGINE-VITE-CONFIG-v1.0` → **2** 個文件
   - `baobao-guardian/frontend/vite.config.ts`
   - `releases/v5.1/staging/baobao-guardian/frontend/vite.config.ts`

🔵 **39.** `#龍芯⚡️2026-06-21-MODULE-MAIN-v1.0` → **2** 個文件
   - `baobao-guardian/frontend/src/main.tsx`
   - `releases/v5.1/staging/baobao-guardian/frontend/src/main.tsx`

🔵 **40.** ` #龍芯⚡️2026-06-04-BAOBAO-ENV-v1.0` → **2** 個文件
   - `baobao-guardian/backend/.env`
   - `releases/v5.1/staging/baobao-guardian/backend/.env`

🔵 **41.** `#龍芯⚡️2026-06-18-STARRY-MEMORY-v1.0` → **2** 個文件
   - `releases/v5.1/staging/memory-universe/星辰记忆系统.py`
   - `releases/v5.1/staging/memory-universe/README.md`

🔵 **42.** `#龍芯⚡️2026-06-18-STARRY-MEMORY-FILE1-v1.0` → **2** 個文件
   - `releases/v5.1/staging/memory-universe/index.md`
   - `memory-universe/星辰记忆系统.py`

🔵 **43.** ` #龍芯⚡️2026-06-21-MODULE-星辰记忆-v1.0` → **2** 個文件
   - `releases/v5.1/staging/memory-universe/星辰记忆.db`
   - `memory-universe/星辰记忆.db`

🔵 **44.** `#龍芯⚡️2026-06-21-ENGINE-INTEGRATE_PRIVATE_SHARED_BATCH2-v1.0` → **2** 個文件
   - `releases/v5.1/staging/bin/integrate_private_shared_batch2.py`
   - `bin/integrate_private_shared_batch2.py`

🔵 **45.** `#龍芯⚡️2026-06-21-ENGINE-INTEGRATE_CNSH_UID9622-v1.0` → **2** 個文件
   - `releases/v5.1/staging/bin/integrate_cnsh_uid9622.py`
   - `bin/integrate_cnsh_uid9622.py`

🔵 **46.** `#龍芯⚡️2026-06-21-TOOL-START_PERSONA_API-v1.0` → **2** 個文件
   - `releases/v5.1/staging/bin/start_persona_api.sh`
   - `bin/start_persona_api.sh`

🔵 **47.** `#龍芯⚡️2026-06-21-ENGINE-GENERATE_WORKSPACE_METADATA-v1.0` → **2** 個文件
   - `releases/v5.1/staging/bin/generate_workspace_metadata.py`
   - `bin/generate_workspace_metadata.py`

🔵 **48.** `#龍芯⚡️2026-06-21-ENGINE-PERSONA_SCHEDULER-v1.0` → **2** 個文件
   - `releases/v5.1/staging/bin/persona_scheduler.py`
   - `bin/persona_scheduler.py`

🔵 **49.** `#龍芯⚡️2026-06-21-TOOL-SKILL-LAUNCHER-V3-v1.0` → **2** 個文件
   - `releases/v5.1/staging/bin/skill-launcher-v3.sh`
   - `bin/skill-launcher-v3.sh`

🔵 **50.** `#龍芯⚡️2026-06-21-ENGINE-RUN_PERSONA_API-v1.0` → **2** 個文件
   - `releases/v5.1/staging/bin/run_persona_api.py`
   - `bin/run_persona_api.py`

🔵 **51.** `#龍芯⚡️2026-06-21-ENGINE-ORGANIZE_LONGHUN_TECH-v1.0` → **2** 個文件
   - `releases/v5.1/staging/bin/organize_longhun_tech.py`
   - `bin/organize_longhun_tech.py`

🔵 **52.** `#龍芯⚡️2026-06-21-ENGINE-SKILL_WRAPPERS-v1.0` → **2** 個文件
   - `releases/v5.1/staging/control-panel/api/skill_wrappers.py`
   - `control-panel/api/skill_wrappers.py`

🔵 **53.** `#龍芯⚡️2026-06-21-ENGINE-FOUNDATION_WRAPPERS-v1.0` → **2** 個文件
   - `releases/v5.1/staging/control-panel/api/foundation_wrappers.py`
   - `control-panel/api/foundation_wrappers.py`

🔵 **54.** `#龍芯⚡️2026-06-06-CODE-AUDIT-v3.0` → **2** 個文件
   - `releases/v5.1/staging/06_技術文檔/skill_code-audit.md`
   - `releases/v5.1/staging/01_技能庫/code-audit.md`

🔵 **55.** `#龍芯⚡️2026-06-06-KIMI-WEBBRIDGE-v1.0` → **2** 個文件
   - `releases/v5.1/staging/06_技術文檔/skill_kimi-webbridge.md`
   - `releases/v5.1/staging/01_技能庫/kimi-webbridge.md`

🔵 **56.** `#龍芯⚡️2026-06-21-CNSH-INFO-v1.0` → **2** 個文件
   - `releases/v5.1/staging/cnsh/info.md`
   - `cnsh/info.md`

🔵 **57.** ` #龍芯⚡️2026-06-06-SANCAI-SYNC-TEST-SUITE-v1.0` → **2** 個文件
   - `releases/v5.1/staging/cnsh/sancai_sync/tests/test_sancai_sync_hub.py`
   - `cnsh/sancai_sync/tests/test_sancai_sync_hub.py`

🔵 **58.** `#龍芯⚡️2026-06-21-DOC-DNA-GEN-v1.0` → **2** 個文件
   - `releases/v5.1/staging/01_技能庫/dna-gen.md`
   - `01_技能庫/dna-gen.md`

🔵 **59.** `#龍芯⚡️2026-06-21-DOC-ON-TRANSLATE-v1.0` → **2** 個文件
   - `releases/v5.1/staging/01_技能庫/on-translate.md`
   - `01_技能庫/on-translate.md`

🔵 **60.** `#龍芯⚡️2026-06-21-DOC-ON-IDENTITY-v1.0` → **2** 個文件
   - `releases/v5.1/staging/01_技能庫/on-identity.md`
   - `01_技能庫/on-identity.md`

🔵 **61.** ` #龍芯⚡️2026-06-21-BRAIN-MEMORIES-v1.0` → **2** 個文件
   - `releases/v5.1/staging/brain/memories.db`
   - `brain/memories.db`

🔵 **62.** `#龍芯⚡️2026-06-07-ALGORITHMIC-ART-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/html-skills/skill-1-algorithmic-art.html`
   - `docs/v3/HTML交互工具启动指南.md`

🔵 **63.** `#龍芯⚡️2026-06-21-ENGINE-SHIELD_TEST_EXAMPLE-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/longhun-shield/shield_test_example.py`
   - `skills/longhun-shield/shield_test_example.py`

🔵 **64.** `#龍芯⚡️2026-06-02-LONGHUN-AUDIT-INTEGRATED-v2.0` → **2** 個文件
   - `releases/v5.1/staging/skills/longhun-audit-integrated/longhun_audit_integrated.py`
   - `releases/v5.1/staging/skills/longhun-audit-integrated/LONGHUN_AUDIT_INTEGRATED_GUIDE.md`

🔵 **65.** `#龍芯⚡️2026-06-21-DOC-SKILL-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/warehouse-audit/SKILL.md`
   - `skills/warehouse-audit/SKILL.md`

🔵 **66.** ` #龍芯⚡️2026-06-21-MODULE-DEMO_WMS-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/warehouse-audit/demo_wms_data/demo_wms.db`
   - `skills/warehouse-audit/demo_wms_data/demo_wms.db`

🔵 **67.** `#龍芯⚡️2026-06-21-MODULE-ORDERS-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/warehouse-audit/demo_wms_data/demo_wms_csv/orders.csv`
   - `skills/warehouse-audit/demo_wms_data/demo_wms_csv/orders.csv`

🔵 **68.** `#龍芯⚡️2026-06-21-MODULE-OPERATIONS-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/warehouse-audit/demo_wms_data/demo_wms_csv/operations.csv`
   - `skills/warehouse-audit/demo_wms_data/demo_wms_csv/operations.csv`

🔵 **69.** `#龍芯⚡️2026-06-21-MODULE-WAREHOUSE_METRICS-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/warehouse-audit/demo_wms_data/demo_wms_csv/warehouse_metrics.csv`
   - `skills/warehouse-audit/demo_wms_data/demo_wms_csv/warehouse_metrics.csv`

🔵 **70.** `#龍芯⚡️2026-06-21-MODULE-INVENTORY-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/warehouse-audit/demo_wms_data/demo_wms_csv/inventory.csv`
   - `skills/warehouse-audit/demo_wms_data/demo_wms_csv/inventory.csv`

🔵 **71.** `#龍芯⚡️2026-06-16-LONGHUN-SELF-AUDIT-FILE1-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/warehouse-audit/reports/longhun-self-audit-20260616-041121.md`
   - `releases/v5.1/staging/skills/warehouse-audit/reports/longhun-self-audit-20260616-041121.json`

🔵 **72.** `#龍芯⚡️2026-06-16-LONGHUN-SELF-AUDIT-FILE2-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/warehouse-audit/reports/longhun-self-audit-20260616-041247.md`
   - `releases/v5.1/staging/skills/warehouse-audit/reports/longhun-self-audit-20260616-120859.json`

🔵 **73.** `#龍芯⚡️2026-06-17-LONGHUN-SELF-AUDIT-FILE1-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/warehouse-audit/reports/longhun-self-audit-20260617-112656.json`
   - `releases/v5.1/staging/skills/warehouse-audit/reports/longhun-self-audit-20260617-111300.md`

🔵 **74.** `#龍芯⚡️2026-06-16-LONGHUN-SELF-AUDIT-FILE3-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/warehouse-audit/reports/longhun-self-audit-20260616-120859.md`
   - `skills/warehouse-audit/reports/longhun-self-audit-20260616-041247.json`

🔵 **75.** `#龍芯⚡️2026-06-17-LONGHUN-SELF-AUDIT-FILE2-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/warehouse-audit/reports/longhun-self-audit-20260617-111027.json`
   - `releases/v5.1/staging/skills/warehouse-audit/reports/longhun-self-audit-20260617-103654.md`

🔵 **76.** `#龍芯⚡️2026-06-17-LONGHUN-SELF-AUDIT-FILE3-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/warehouse-audit/reports/longhun-self-audit-20260617-112656.md`
   - `releases/v5.1/staging/skills/warehouse-audit/reports/longhun-self-audit-20260617-110927.json`

🔵 **77.** `#龍芯⚡️2026-06-17-LONGHUN-SELF-AUDIT-FILE4-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/warehouse-audit/reports/longhun-self-audit-20260617-111027.md`
   - `releases/v5.1/staging/skills/warehouse-audit/reports/longhun-self-audit-20260617-111300.json`

🔵 **78.** `#龍芯⚡️2026-06-17-LONGHUN-SELF-AUDIT-FILE5-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/warehouse-audit/reports/longhun-self-audit-20260617-112617.md`
   - `releases/v5.1/staging/skills/warehouse-audit/reports/longhun-self-audit-20260617-103654.json`

🔵 **79.** `#龍芯⚡️2026-06-17-LONGHUN-SELF-AUDIT-FILE6-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/warehouse-audit/reports/longhun-self-audit-20260617-110927.md`
   - `releases/v5.1/staging/skills/warehouse-audit/reports/longhun-self-audit-20260617-110921.json`

🔵 **80.** `#龍芯⚡️2026-06-04-KFPP-EXECUTOR-v1.0` → **2** 個文件
   - `releases/v5.1/staging/systems/kfpp/kfpp_executor_v1.0.py`
   - `releases/v5.1/staging/systems/kfpp/README.md`

🔵 **81.** `#龍芯⚡️2026-06-21-PROTOCOL-PROTOCOL_UNIFICATION_COMPLETION_REPORT-v1.0` → **2** 個文件
   - `releases/v5.1/staging/protocols/PROTOCOL_UNIFICATION_COMPLETION_REPORT.md`
   - `protocols/PROTOCOL_UNIFICATION_COMPLETION_REPORT.md`

🔵 **82.** `#龍芯⚡️2026-06-21-PROTOCOL-CNSH_V3-0_COMPLETE_FULL_NO_EMOJI-v1.0` → **2** 個文件
   - `releases/v5.1/staging/protocols/_DEPRECATED_CNSH_v2.0_v3.0_2026-06-08/CNSH_v3.0_COMPLETE_FULL_no_emoji.md`
   - `protocols/_DEPRECATED_CNSH_v2.0_v3.0_2026-06-08/CNSH_v3.0_COMPLETE_FULL_no_emoji.md`

🔵 **83.** `#龍芯⚡️2026-06-18-LONGHUN-CHINESE-EDITOR-v1.0` → **2** 個文件
   - `releases/v5.1/staging/editor/README.md`
   - `releases/v5.1/staging/editor/龍碼編輯器.py`

🔵 **84.** `#龍芯⚡️2026-06-21-DOC-AUDIT_THREE_COLOR-v1.0` → **2** 個文件
   - `releases/v5.1/staging/crypto-stack/audit_three_color.md`
   - `crypto-stack/audit_three_color.md`

🔵 **85.** `#龍芯⚡️2026-06-21-ENGINE-L6_SOUL-v1.0` → **2** 個文件
   - `releases/v5.1/staging/crypto-stack/src/l6_soul.py`
   - `crypto-stack/src/l6_soul.py`

🔵 **86.** `#龍芯⚡️2026-06-21-ENGINE-WEIGHT_TUNER-v1.0` → **2** 個文件
   - `releases/v5.1/staging/crypto-stack/src/weight_tuner.py`
   - `crypto-stack/src/weight_tuner.py`

🔵 **87.** `#龍芯⚡️2026-06-21-ENGINE-L1_PHYSICAL-v1.0` → **2** 個文件
   - `releases/v5.1/staging/crypto-stack/src/l1_physical.py`
   - `crypto-stack/src/l1_physical.py`

🔵 **88.** `#龍芯⚡️2026-06-21-ENGINE-STACK_RUNNER-v1.0` → **2** 個文件
   - `releases/v5.1/staging/crypto-stack/src/stack_runner.py`
   - `crypto-stack/src/stack_runner.py`

🔵 **89.** `#龍芯⚡️2026-06-21-ENGINE-L4_SEVEN_FACTOR-v1.0` → **2** 個文件
   - `releases/v5.1/staging/crypto-stack/src/l4_seven_factor.py`
   - `crypto-stack/src/l4_seven_factor.py`

🔵 **90.** `#龍芯⚡️2026-06-16-LONGHUN-SELF-AUDIT-FILE4-v1.0` → **2** 個文件
   - `bin/longhun-self-audit.sh`
   - `skills/warehouse-audit/reports/longhun-self-audit-20260616-041121.json`

🔵 **91.** `#龍芯⚡️2026-06-16-LONGHUN-CONTROL-PANEL-FILE1-v1.1` → **2** 個文件
   - `control-panel/README.md`
   - `control-panel/main.py`

🔵 **92.** `#龍芯⚡️2026-06-21-PROTOCOL-CNSH-GITHUB-README-v1.0` → **2** 個文件
   - `docs/private-shared-imports/cnsh-protocols/📄 CNSH GitHub README.md`
   - `docs/private-shared-imports/cnsh-protocols/CNSH-GitHub-README.md`

🔵 **93.** `#龍芯⚡️2026-06-21-DOC-INDEX-v1.0` → **2** 個文件
   - `docs/v3/INDEX.md`
   - `project-memory/index.md`

🔵 **94.** `#龍芯⚡️2026-06-21-DOC-PLAN-v1.0` → **2** 個文件
   - `docs/v3/plan.md`
   - `integrated-modules/kimi_agent/plan.md`

🔵 **95.** `#龍芯⚡️2026-06-16-PERSONA-ROUTER-v3.0` → **2** 個文件
   - `docs/v3/人格矩阵路由系统配置说明.md`
   - `systems/v3/人格矩阵路由系统_v3.0.py`

🔵 **96.** `#龍芯⚡️2026-06-21-MODULE-HELLO-v1.0` → **2** 個文件
   - `docs/claude-backlog/02_CNSH语言/hello.cnsh`
   - `docs/claude-backlog/02_CNSH语言/hello`

🔵 **97.** `#龍芯⚡️2026-06-21-CNSH-README-v1.0` → **2** 個文件
   - `docs/cnsh-uid9622/README.md`
   - `extensions/cnsh-chrome-plugin/README.md`

🔵 **98.** `#龍芯⚡️2026-06-21-CNSH-POPUP-v1.0` → **2** 個文件
   - `extensions/cnsh-chrome-plugin/popup.js`
   - `extensions/cnsh-chrome-plugin/popup.html`

🔵 **99.** `#龍芯⚡️2026-06-21-CNSH-OPTIONS-v1.0` → **2** 個文件
   - `extensions/cnsh-chrome-plugin/options.js`
   - `extensions/cnsh-chrome-plugin/options.html`

🔵 **100.** `#龍芯⚡️2026-06-21-MODULE-SIDEPANEL-HTML-v1.0` → **2** 個文件
   - `extensions/LongHunWidget/sidepanel.html.bak2`
   - `extensions/LongHunWidget/sidepanel.html.bak`

🔵 **101.** `#龍芯⚡️2026-06-06-CODE-AUDIT-FILE1-v3.0` → **2** 個文件
   - `06_技術文檔/skill_code-audit.md`
   - `01_技能庫/code-audit.md`

🔵 **102.** `#龍芯⚡️2026-06-04-KFPP-EXECUTOR-FILE1-v1.0` → **2** 個文件
   - `executors/kfpp/longhun_kfpp_executor_v1.0.py`
   - `systems/kfpp/README.md`

🔵 **103.** `#龍芯⚡️2026-06-21-SCRIPT-DEMO_INPUT-v1.0` → **2** 個文件
   - `scripts/demo_input.txt`
   - `scripts/demo_input.shortcode`

🔵 **104.** `#龍芯⚡️2026-06-18-LONGHUN-CHRONICLE-v1.0` → **2** 個文件
   - `project-memory/龍魂編年史.py`
   - `project-memory/README.md`

🔵 **105.** `#龍芯⚡️2026-06-21-CORE-FEARLESS_STEVE_PROTOCOL_V2-0_USAGE_GUIDE-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/FEARLESS_STEVE_PROTOCOL_v2.0_USAGE_GUIDE.md.bak`
   - `cnsh-core/FEARLESS_STEVE_PROTOCOL_v2.0_USAGE_GUIDE.md.bak`

🔵 **106.** `#龍芯⚡️2026-06-21-CORE-MEMORY_PACK_V3-PY-v1.0` → **2** 個文件
   - `cnsh-core.backup/memory_pack_v3.py.bak`
   - `cnsh-core/memory_pack_v3.py.bak`

🔵 **107.** `#龍芯⚡️2026-06-21-CORE-PARSE_NOTION-v1.0` → **2** 個文件
   - `cnsh-core.backup/parse_notion.py`
   - `cnsh-core/parse_notion.py`

🔵 **108.** `#龍芯⚡️2026-06-21-CORE-NOTION_TASK5_SETUP-PY-v1.0` → **2** 個文件
   - `cnsh-core.backup/notion_task5_setup.py.bak`
   - `cnsh-core/notion_task5_setup.py.bak`

🔵 **109.** `#龍芯⚡️2026-06-21-CORE-FEARLESS_STEVE_PROTOCOL_V2-0_IMPLEMENTATION-CPP-v1.0` → **2** 個文件
   - `cnsh-core.backup/FEARLESS_STEVE_PROTOCOL_v2.0_IMPLEMENTATION.cpp.bak`
   - `cnsh-core/FEARLESS_STEVE_PROTOCOL_v2.0_IMPLEMENTATION.cpp.bak`

🔵 **110.** `#龍芯⚡️2026-06-21-CORE-AUDIT_README-v1.0` → **2** 個文件
   - `cnsh-core.backup/AUDIT_README.md`
   - `cnsh-core/AUDIT_README.md`

🔵 **111.** ` #龍芯⚡️2026-06-03-CORE-SYSTEM-LAUNCHER-v1.0` → **2** 個文件
   - `cnsh-core.backup/core_system_launcher.py`
   - `cnsh-core/core_system_launcher.py`

🔵 **112.** `#龍芯⚡️2026-06-21-CORE-MAIN_FEARLESS_STEVE-CPP-v1.0` → **2** 個文件
   - `cnsh-core.backup/main_fearless_steve.cpp.bak`
   - `cnsh-core/main_fearless_steve.cpp.bak`

🔵 **113.** `#龍芯⚡️2026-06-21-CORE-M05_WUXING_CALCULATOR-v1.0` → **2** 個文件
   - `cnsh-core.backup/m05_wuxing_calculator.py`
   - `cnsh-core/m05_wuxing_calculator.py`

🔵 **114.** `#龍芯⚡️2026-06-21-CORE-FEARLESS_STEVE_PROTOCOL_V2-0_MULTI_PERSONA_ENGINE-CPP-v1.0` → **2** 個文件
   - `cnsh-core.backup/FEARLESS_STEVE_PROTOCOL_v2.0_MULTI_PERSONA_ENGINE.cpp.bak`
   - `cnsh-core/FEARLESS_STEVE_PROTOCOL_v2.0_MULTI_PERSONA_ENGINE.cpp.bak`

🔵 **115.** `#龍芯⚡️2026-06-21-CORE-M04_YIJING_ENGINE-v1.0` → **2** 個文件
   - `cnsh-core.backup/m04_yijing_engine.py`
   - `cnsh-core/m04_yijing_engine.py`

🔵 **116.** `#龍芯⚡️2026-06-21-CORE-LONGHUN_WUXING_MVP-v1.0` → **2** 個文件
   - `cnsh-core.backup/wuxing/longhun_wuxing_mvp.py`
   - `cnsh-core/wuxing/longhun_wuxing_mvp.py`

🔵 **117.** `#龍芯⚡️2026-06-21-CORE-TEST-FUNCTION-CALL-v1.0` → **2** 個文件
   - `cnsh-core.backup/language/test-function-call.cnsh`
   - `cnsh-core/language/test-function-call.cnsh`

🔵 **118.** `#龍芯⚡️2026-06-21-CORE-CNSH_RUNTIME_CORE-PY-v1.0` → **2** 個文件
   - `cnsh-core.backup/runtime-governance/cnsh_runtime_core.py.bak`
   - `cnsh-core/runtime-governance/cnsh_runtime_core.py.bak`

🔵 **119.** `#龍芯⚡️2026-06-21-CORE-PYTEST-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/pytest.ini`
   - `cnsh-core/ai-tools/operation_log_engine/pytest.ini`

🔵 **120.** `#龍芯⚡️2026-05-30-OPERATION-LOG-ENGINE-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/IMPLEMENTATION_GUIDE.md.bak`
   - `cnsh-core.backup/ai-tools/operation_log_engine/operation_log_engine/__init__.py.bak`

🔵 **121.** `#龍芯⚡️2026-05-30-LOCAL-SYNC-ENGINE-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/PHASE_2_2_GUIDE.md.bak`
   - `cnsh-core.backup/ai-tools/operation_log_engine/core/sync_engine.py.bak`

🔵 **122.** `#龍芯⚡️2026-06-21-CORE-ENCRYPTION_ENFORCE_REPORT-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/ENCRYPTION_ENFORCE_REPORT.md.bak`
   - `cnsh-core/ai-tools/operation_log_engine/ENCRYPTION_ENFORCE_REPORT.md.bak`

🔵 **123.** `#龍芯⚡️2026-05-30-QUERY-TOOL-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/PHASE_2_3_GUIDE.md.bak`
   - `cnsh-core.backup/ai-tools/operation_log_engine/core/query_tool.py.bak`

🔵 **124.** `#龍芯⚡️2026-05-30-ENV-CONFIG-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/.env.example`
   - `cnsh-core/ai-tools/operation_log_engine/.env.example`

🔵 **125.** `#龍芯⚡️2026-06-21-CORE-ENCRYPTION_ENFORCE-PY-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/operation_log_engine/encryption_enforce.py.bak`
   - `cnsh-core/ai-tools/operation_log_engine/operation_log_engine/encryption_enforce.py.bak`

🔵 **126.** `#龍芯⚡️2026-06-21-CORE-TOP_LEVEL-TXT-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/top_level.txt.bak`
   - `cnsh-core/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/top_level.txt.bak`

🔵 **127.** `#龍芯⚡️2026-06-21-CORE-PKG-INFO-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/PKG-INFO`
   - `cnsh-core/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/PKG-INFO`

🔵 **128.** `#龍芯⚡️2026-06-21-CORE-DEPENDENCY_LINKS-TXT-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/dependency_links.txt.bak`
   - `cnsh-core/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/dependency_links.txt.bak`

🔵 **129.** `#龍芯⚡️2026-06-21-CORE-NOT-ZIP-SAFE-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/not-zip-safe`
   - `cnsh-core/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/not-zip-safe`

🔵 **130.** `#龍芯⚡️2026-06-21-CORE-ENTRY_POINTS-TXT-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/entry_points.txt.bak`
   - `cnsh-core/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/entry_points.txt.bak`

🔵 **131.** `#龍芯⚡️2026-06-21-CORE-REQUIRES-TXT-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/requires.txt.bak`
   - `cnsh-core/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/requires.txt.bak`

🔵 **132.** `#龍芯⚡️2026-06-21-CORE-SOURCES-TXT-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/SOURCES.txt.bak`
   - `cnsh-core/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/SOURCES.txt.bak`

🔵 **133.** `#龍芯⚡️2026-06-21-CORE-START_SENTINEL-SH-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/longhu_sentinel_bot/start_sentinel.sh.bak`
   - `cnsh-core/ai-tools/longhu_sentinel_bot/start_sentinel.sh.bak`

🔵 **134.** `#龍芯⚡️2026-06-21-CORE-TOKEN_MANAGER-PY-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/longhu_sentinel_bot/token_manager.py.bak`
   - `cnsh-core/ai-tools/longhu_sentinel_bot/token_manager.py.bak`

🔵 **135.** `#龍芯⚡️2026-06-21-CORE-SENTINEL_BOT-PY-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/longhu_sentinel_bot/sentinel_bot.py.bak`
   - `cnsh-core/ai-tools/longhu_sentinel_bot/sentinel_bot.py.bak`

🔵 **136.** `#龍芯⚡️2026-06-21-CORE-README-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/longhu_sentinel_bot/README.md.bak`
   - `cnsh-core/ai-tools/longhu_sentinel_bot/README.md.bak`

🔵 **137.** `#龍芯⚡️2026-06-21-CORE-TELEGRAM_HANDLER-PY-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/longhu_sentinel_bot/telegram_handler.py.bak`
   - `cnsh-core/ai-tools/longhu_sentinel_bot/telegram_handler.py.bak`

🔵 **138.** `#龍芯⚡️2026-06-21-CORE-AUDIT_ENGINE-v1.0` → **2** 個文件
   - `cnsh-core.backup/engines/audit_engine.py`
   - `cnsh-core/engines/audit_engine.py`

🔵 **139.** `#龍芯⚡️2026-06-21-CORE-DRAGON_SOUL_9622-v1.0` → **2** 個文件
   - `cnsh-core.backup/longhun-flow-system/dragon_soul_9622.html`
   - `cnsh-core/longhun-flow-system/dragon_soul_9622.html`

🔵 **140.** ` #龍芯⚡️2026-04-19-三才流場-v8` → **2** 個文件
   - `cnsh-core.backup/longhun-flow-system/current.html`
   - `cnsh-core/longhun-flow-system/current.html`

🔵 **141.** `#龍芯⚡️2026-06-21-CORE-LONGHUN-28MANSIONS-V1-v1.0` → **2** 個文件
   - `cnsh-core.backup/longhun-flow-system/longhun-28mansions-v1.html`
   - `cnsh-core/longhun-flow-system/longhun-28mansions-v1.html`

🔵 **142.** `#龍芯⚡️2026-06-21-CORE-CNSH_GATEWAY-v1.0` → **2** 個文件
   - `cnsh-core.backup/gateway/cnsh_gateway.py`
   - `cnsh-core/gateway/cnsh_gateway.py`

🔵 **143.** `#龍芯⚡️2026-06-03-PERSONA-ROUTER-v1.0` → **2** 個文件
   - `cnsh-core.backup/router/persona_router.py`
   - `cnsh-core.backup/router/PERSONA_ROUTER_README.md`

🔵 **144.** `#龍芯⚡️2026-06-16-LONGHUN-SELF-AUDIT-FILE5-v1.0` → **2** 個文件
   - `skills/warehouse-audit/reports/longhun-self-audit-20260616-041121.md`
   - `skills/warehouse-audit/reports/longhun-self-audit-20260616-120859.json`

🔵 **145.** `#龍芯⚡️2026-06-18-LONGHUN-SELF-AUDIT-FILE1-v1.0` → **2** 個文件
   - `skills/warehouse-audit/reports/longhun-self-audit-20260618-154318.json`
   - `skills/warehouse-audit/reports/longhun-self-audit-20260618-154318.md`

🔵 **146.** `#龍芯⚡️2026-06-17-LONGHUN-SELF-AUDIT-FILE7-v1.0` → **2** 個文件
   - `skills/warehouse-audit/reports/longhun-self-audit-20260617-112617.json`
   - `skills/warehouse-audit/reports/longhun-self-audit-20260617-110921.md`

🔵 **147.** `#龍芯⚡️2026-06-17-LONGHUN-SELF-AUDIT-FILE8-v1.0` → **2** 個文件
   - `skills/warehouse-audit/reports/longhun-self-audit-20260617-112656.json`
   - `skills/warehouse-audit/reports/longhun-self-audit-20260617-111300.md`

🔵 **148.** `#龍芯⚡️2026-06-17-LONGHUN-SELF-AUDIT-FILE9-v1.0` → **2** 個文件
   - `skills/warehouse-audit/reports/longhun-self-audit-20260617-111027.json`
   - `skills/warehouse-audit/reports/longhun-self-audit-20260617-103654.md`

🔵 **149.** `#龍芯⚡️2026-06-17-LONGHUN-SELF-AUDIT-FILE10-v1.0` → **2** 個文件
   - `skills/warehouse-audit/reports/longhun-self-audit-20260617-112656.md`
   - `skills/warehouse-audit/reports/longhun-self-audit-20260617-110927.json`

🔵 **150.** `#龍芯⚡️2026-06-17-LONGHUN-SELF-AUDIT-FILE11-v1.0` → **2** 個文件
   - `skills/warehouse-audit/reports/longhun-self-audit-20260617-111027.md`
   - `skills/warehouse-audit/reports/longhun-self-audit-20260617-111300.json`

🔵 **151.** `#龍芯⚡️2026-06-17-LONGHUN-SELF-AUDIT-FILE12-v1.0` → **2** 個文件
   - `skills/warehouse-audit/reports/longhun-self-audit-20260617-112617.md`
   - `skills/warehouse-audit/reports/longhun-self-audit-20260617-103654.json`

🔵 **152.** `#龍芯⚡️2026-06-17-LONGHUN-SELF-AUDIT-FILE13-v1.0` → **2** 個文件
   - `skills/warehouse-audit/reports/longhun-self-audit-20260617-110927.md`
   - `skills/warehouse-audit/reports/longhun-self-audit-20260617-110921.json`

🔵 **153.** `#龍芯⚡️2026-06-21-CNSH-CNSH-PUBLIC-PAGES-OVERVIEW-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/cnsh-public-pages-overview.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/cnsh-public-pages-overview.md.bak`

🔵 **154.** `#龍芯⚡️2026-06-21-CNSH-HELLO_ENGLISH-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/hello_english.longhun`
   - `_archive/cnsh-history/CNSH_备份_20260211/19bd8da9-1792-8267-8000-093407b99859/hello_english.longhun`

🔵 **155.** `#龍芯⚡️2026-06-21-CNSH-ZHX-20251212-LUCKY-DIGITAL-HUMAN-DEMO-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-LUCKY-DIGITAL-HUMAN-DEMO.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-LUCKY-DIGITAL-HUMAN-DEMO.md.bak`

🔵 **156.** `#龍芯⚡️2026-06-21-CNSH-UID9622_AUTOMATION_CONFIG-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/uid9622_automation_config.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/uid9622_automation_config.md.sig`

🔵 **157.** `#龍芯⚡️2026-06-21-CNSH-LONGHUN-COMPILER-JS-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/longhun-compiler.js.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/19bd8da9-1792-8267-8000-093407b99859/longhun-compiler.js.bak`

🔵 **158.** `#龍芯⚡️2026-06-21-CNSH-PLATFORM-SETUP-GUIDE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/platform-setup-guide.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/platform-setup-guide.md.bak`

🔵 **159.** `#龍芯⚡️2026-06-21-CNSH-MANUAL_SETUP_GUIDE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/manual_setup_guide.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/manual_setup_guide.md.bak`

🔵 **160.** `#龍芯⚡️2026-06-21-CNSH-CNSH_PARSER-PY-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/cnsh_parser.py.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/19bd8da9-1792-8267-8000-093407b99859/cnsh_parser.py.bak`

🔵 **161.** `#龍芯⚡️2026-06-21-CNSH-ZHX-20251212-OLLAMA-SYSTEM-SUMMARY-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-OLLAMA-SYSTEM-SUMMARY.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-OLLAMA-SYSTEM-SUMMARY.md.bak`

🔵 **162.** `#龍芯⚡️2026-06-21-CNSH-README_ORIGINAL-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/README_ORIGINAL.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/README_ORIGINAL.md.sig`

🔵 **163.** `#龍芯⚡️2026-06-21-CNSH-QUICK-START-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/QUICK-START.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/QUICK-START.md.sig`

🔵 **164.** `#龍芯⚡️2026-06-21-CNSH-ZHX-20251212-DAILY-REVIEW-SYSTEM-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-DAILY-REVIEW-SYSTEM.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-DAILY-REVIEW-SYSTEM.md.bak`

🔵 **165.** `#龍芯⚡️2026-06-21-CNSH-PAYMENT_DEMO-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/PAYMENT_DEMO.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/PAYMENT_DEMO.md.sig`

🔵 **166.** `#龍芯⚡️2026-06-21-CNSH-CNSH_CLEANER-PY-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/cnsh_cleaner.py.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/19bd8da9-1792-8267-8000-093407b99859/cnsh_cleaner.py.bak`

🔵 **167.** `#龍芯⚡️2026-06-21-CNSH-ZHX-20251212-OLLAMA-IMPLEMENTATION-GUIDE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-OLLAMA-IMPLEMENTATION-GUIDE.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-OLLAMA-IMPLEMENTATION-GUIDE.md.bak`

🔵 **168.** `#龍芯⚡️2026-06-21-CNSH-ZHX-20251212-OLLAMA-COMPLETE-GUIDE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-OLLAMA-COMPLETE-GUIDE.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-OLLAMA-COMPLETE-GUIDE.md.bak`

🔵 **169.** `#龍芯⚡️2026-06-21-CNSH-ZHX-20251212-OLLAMA-MASTER-SYSTEM-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-OLLAMA-MASTER-SYSTEM.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-OLLAMA-MASTER-SYSTEM.md.sig`

🔵 **170.** `#龍芯⚡️2026-06-21-CNSH-MATE60_HOTSPOT_GUIDE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/mate60_hotspot_guide.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/mate60_hotspot_guide.md.bak`

🔵 **171.** `#龍芯⚡️2026-06-21-CNSH-README_PAYMENT-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/README_PAYMENT.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/README_PAYMENT.md.bak`

🔵 **172.** `#龍芯⚡️2026-06-21-CNSH-ZHX-20251212-EXECUTION-PLAN-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-EXECUTION-PLAN.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-EXECUTION-PLAN.md.bak`

🔵 **173.** `#龍芯⚡️2026-06-21-CNSH-ZHX-20251212-AUTOCLASSIFIER-001-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-AUTOCLASSIFIER-001.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-AUTOCLASSIFIER-001.md.sig`

🔵 **174.** `#龍芯⚡️2026-06-21-CNSH-ZHX-20251212-OLLAMA-QUICK-START-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-OLLAMA-QUICK-START.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-OLLAMA-QUICK-START.md.sig`

🔵 **175.** `#龍芯⚡️2026-06-21-CNSH-FAQ-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/龍魂永世唯一身份系统/docs/FAQ.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/FAQ.md.bak`

🔵 **176.** `#龍芯⚡️2026-06-21-CNSH-CNSH_AI_STANDARDS-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/CNSH_AI_STANDARDS.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/CNSH_AI_STANDARDS.md.bak`

🔵 **177.** `#龍芯⚡️2026-06-21-CNSH-NOTION-DATABASES-INTEGRATION-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/notion-databases-integration.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/notion-databases-integration.md.bak`

🔵 **178.** `#龍芯⚡️2026-06-21-CNSH-DNA_CODING_SYSTEM-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/DNA_CODING_SYSTEM.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/DNA_CODING_SYSTEM.md.bak`

🔵 **179.** `#龍芯⚡️2026-06-21-CNSH-CNSH_INITIAL_MISSION-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/CNSH_INITIAL_MISSION.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/CNSH_INITIAL_MISSION.md.bak`

🔵 **180.** `#龍芯⚡️2026-06-21-CNSH-NOTION_MONITOR_GUIDE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/NOTION_MONITOR_GUIDE.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/NOTION_MONITOR_GUIDE.md.bak`

🔵 **181.** `#龍芯⚡️2026-06-21-CNSH-CNSH_VISION-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/CNSH_VISION.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/CNSH_VISION.md.bak`

🔵 **182.** `#龍芯⚡️2026-06-21-CNSH-DEPLOYMENT_GUIDE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/DEPLOYMENT_GUIDE.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/DEPLOYMENT_GUIDE.md.bak`

🔵 **183.** `#龍芯⚡️2026-06-21-CNSH-FINAL_INSTRUCTIONS-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/FINAL_INSTRUCTIONS.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/FINAL_INSTRUCTIONS.md.bak`

🔵 **184.** `#龍芯⚡️2026-06-21-CNSH-CNSH-CORE-WHITEPAPER-ZH-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/docs/CNSH-Core-Whitepaper-ZH.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/CNSH-Core-Whitepaper-ZH.md.bak`

🔵 **185.** `#龍芯⚡️2026-06-21-CNSH-NORTH-STAR-B-PROTOCOL-V1-0-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/docs/North-Star-B-Protocol-v1.0.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/North-Star-B-Protocol-v1.0.md.bak`

🔵 **186.** `#龍芯⚡️2026-06-21-CNSH-MULAN-PROTOCOL-V1-0-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/📖协议文档/正式版/Mulan-Protocol-v1.0.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/📖协议文档/正式版/Mulan-Protocol-v1.0.md.sig`

🔵 **187.** `#龍芯⚡️2026-06-21-CNSH-QUICK_START-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251207144453/MulanNotion/guides/QUICK_START.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/packages/cnsh-editor/QUICK_START.md.bak`

🔵 **188.** `#龍芯⚡️2026-02-09-CNSH-ENGINE-MANAGER-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-Engine-Manager/README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-Engine-Manager/cnsh_engine_manager.py.bak`

🔵 **189.** `#龍芯⚡️2026-06-21-CNSH-TEST-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/sample_notion_export/test.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/sample_notion_export/test.md.sig`

🔵 **190.** `#龍芯⚡️2026-06-21-CNSH-HEALTHCHECK_20251224_055736-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/health_reports/healthcheck_20251224_055736.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/health_reports/healthcheck_20251224_055736.md.bak`

🔵 **191.** `#龍芯⚡️2026-06-21-CNSH-TEST-FUNCTION-CALL-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-v1.0-完整实现/test-function-call.cnsh`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/test-function-call.cnsh`

🔵 **192.** `#龍芯⚡️2026-06-21-CNSH-CNSH-COMPILER-JS-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-v1.0-完整实现/cnsh-compiler.js.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/cnsh-compiler.js.bak`

🔵 **193.** `#龍芯⚡️2026-06-21-CNSH-VALIDATION-REPORT-20260130_155300-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/validation-layer/reports/VALIDATION-REPORT-20260130_155300.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/validation-layer/reports/VALIDATION-REPORT-20260130_155300.md.sig`

🔵 **194.** `#龍芯⚡️2026-06-21-CNSH-VALIDATION-REPORT-20260130_154834-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/validation-layer/reports/VALIDATION-REPORT-20260130_154834.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/validation-layer/reports/VALIDATION-REPORT-20260130_154834.md.sig`

🔵 **195.** `#龍芯⚡️2026-06-21-CNSH-MANIFEST-JSON-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/LU-Taiji-Bundle/manifest.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/packages/dragon_soul_extension/manifest.json.bak`

🔵 **196.** `#龍芯⚡️2026-06-21-CNSH-START-SH-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/LU-Taiji-Bundle/devices/huawei/start.sh.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/LU-Taiji-Bundle/devices/asus/start.sh.bak`

🔵 **197.** `#龍芯⚡️2026-06-21-CNSH-AUTOFILL_RULES-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/UID9622-LocalServer/UID9622-WorldSystem/AutoFill_Rules.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/UID9622-LocalServer/UID9622-WorldSystem/AutoFill_Rules.md.bak`

🔵 **198.** `#龍芯⚡️2026-06-21-CNSH-CODE_TEMPLATE-PY-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/templates/code_template.py.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/templates/combat-ready/code_template.py.bak`

🔵 **199.** `#龍芯⚡️2026-06-21-CNSH-INNOVATION_TEMPLATE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/templates/combat-ready/innovation_template.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/templates/combat-ready/innovation_template.md.bak`

🔵 **200.** `#龍芯⚡️2026-06-21-CNSH-LATEST-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/manifests/registry.ollama.ai/library/llama3.2/latest`
   - `_archive/cnsh-history/CNSH_备份_20260211/manifests/registry.ollama.ai/firerootlad/ROOT_UID9622/latest`

🔵 **201.** `#龍芯⚡️2026-06-21-CNSH-README_CN-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/anti-fraud-sentinel/global-reference/README_CN.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/anti-fraud-sentinel/global-reference/README_CN.md.bak`

🔵 **202.** `#龍芯⚡️2026-06-21-CNSH-LONGHUN_DATA_SOVEREIGNTY_DEFENSE_TOOLKIT_GUIDE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/longhun_data_sovereignty_defense_toolkit_guide.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/longhun_data_sovereignty_defense_toolkit_guide.md.sig`

🔵 **203.** `#龍芯⚡️2026-06-21-CNSH-NOTION_AUTO_EMAIL_GUIDE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/notion_auto_email_guide.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/notion_auto_email_guide.md.sig`

🔵 **204.** `#龍芯⚡️2026-06-21-CNSH-PROJECT_SETUP-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/PROJECT_SETUP.md.sig`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/PROJECT_SETUP.md.bak`

🔵 **205.** `#龍芯⚡️2026-06-21-CNSH-CNSH_COMPLETE_SPEC_V2-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/龍魂系统核心/cnsh_complete_spec_v2.cnsh`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/龍魂系统核心/files/cnsh_complete_spec_v2.cnsh`

🔵 **206.** `#龍芯⚡️2026-06-21-CNSH-CNSH_VISUAL_RENDER_V1-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/龍魂系统核心/cnsh_visual_render_v1.cnsh`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/龍魂系统核心/files/cnsh_visual_render_v1.cnsh`

🔵 **207.** `#龍芯⚡️2026-06-21-CNSH-TROUBLESHOOTING-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/stylegan3-main 2/docs/troubleshooting.md.sig`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/stylegan3-main 2/docs/troubleshooting.md.bak`

🔵 **208.** `#龍芯⚡️2026-06-21-CNSH-CONFIGS-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/stylegan3-main 2/docs/configs.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/stylegan3-main 2/docs/configs.md.sig`

🔵 **209.** `#龍芯⚡️2026-06-21-CNSH-CLAUDE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/files/CLAUDE.md.sig`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/files/CLAUDE.md.bak`

🔵 **210.** `#龍芯⚡️2026-06-21-CNSH-CLAUDE_CODE_ANCHORING_ARCHITECTURE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/files/claude_code_anchoring_architecture.md.sig`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/files/claude_code_anchoring_architecture.md.bak`

🔵 **211.** `#龍芯⚡️2026-06-21-SCRIPT-INSTALL-SH-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-整理版/scripts/install.sh.bak`
   - `_archive/cnsh-history/CNSH-整理版/packages/cnsh-core/scripts/install.sh.bak`

🔵 **212.** `#龍芯⚡️2026-06-21-CORE-OLLAMA-JS-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-整理版/packages/cnsh-core/src/routes/ollama.js.bak`
   - `_archive/cnsh-history/CNSH-整理版/packages/cnsh-core/src/services/ollama.js.bak`

🔵 **213.** `#龍芯⚡️2026-06-03-PERSONA-ROUTER-FILE1-v1.0` → **2** 個文件
   - `cnsh-core/router/persona_router.py`
   - `cnsh-core/router/PERSONA_ROUTER_README.md`

🔵 **214.** `#龍芯⚡️2026-06-18-LONGHUN-CHINESE-EDITOR-FILE1-v1.0` → **2** 個文件
   - `editor/README.md`
   - `editor/龍碼編輯器.py`

---

## 💡 修復建議

- 🔴 高優先: 存在214個重複DNA，違反「一文件一DNA」原則，需拆分
- 🟡 中優先: 135個文件DNA格式無效，需修正格式為 #龍芯⚡️YYYY-MM-DD-MODULE-vX.X
- 🟡 Python腳本: 對齐率40.3%，需補充1035個文件

## 📊 對齐進度

```
DNA 對齐進度 [███████████████░░░░░] 78.8%
```

---

**DNA**: #龍芯⚡️2026-06-21-DNA-ALIGNMENT-AUDIT-v1.0
**簽署**: DNA對齐審計系統·不免責

🐉 龍魂系統·DNA追溯·完整性驗證