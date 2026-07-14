# 🐉 龍魂系統 DNA 對齐審計報告

**DNA**: #龍芯⚡️2026-06-21-DNA-ALIGNMENT-AUDIT-v1.0
**時間**: 2026-06-21 13:21 CST
**掃描目錄**: `/Users/zuimeidedeyihan/longhun-system`
**狀態**: 🟢 良好

---

## 📊 全系統統計

| 指標 | 數值 | 狀態 |
|------|------|------|
| **核心文件無 DNA** | 1395 個 | 🟢 |
| **已關聯 DNA 文件** | 5184 個 | 🟢 |
| **DNA 重複** | 299 個 | 🔴 |
| **核心文件總數** | 6579 個 | - |
| **DNA 對齐率** | 78.8% | 🟢 |

---

## 📁 按文件類型統計

| 文件類型 | 總數 | 有DNA | 無DNA | 對齐率 |
|----------|------|-------|-------|--------|
| Markdown文檔 | 2308 | 2296 | 12 | 🟢 99.5% |
| 其他 | 1896 | 1659 | 237 | 🟢 87.5% |
| Python腳本 | 1734 | 700 | 1034 | 🟡 40.4% |
| JSON配置 | 216 | 144 | 72 | 🟡 66.7% |
| Shell腳本 | 128 | 128 | 0 | 🟢 100.0% |
| HTML | 110 | 108 | 2 | 🟢 98.2% |
| 文本文件 | 104 | 68 | 36 | 🟡 65.4% |
| JavaScript | 57 | 55 | 2 | 🟢 96.5% |
| TypeScript | 13 | 13 | 0 | 🟢 100.0% |
| CSS | 8 | 8 | 0 | 🟢 100.0% |
| YAML配置 | 5 | 5 | 0 | 🟢 100.0% |

## 🔴 DNA 重複問題

發現 **299** 個DNA被多個文件共享:

🔴 **1.** ` #龍芯⚡️2026-06-21-CNSH-UNNAMED-v1.0` → **139** 個文件
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

🔴 **2.** ` #龍芯⚡️2026-06-21-CNSH-README-MD-v1.0` → **106** 個文件
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

🔴 **3.** ` #龍芯⚡️2026-06-21-CORE-UNNAMED-v1.0` → **16** 個文件
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

🔴 **4.** ` #龍芯⚡️2026-06-21-ENGINE-UNNAMED-v1.0` → **15** 個文件
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

🔴 **5.** ` #龍芯⚡️2026-06-21-DOC-README-v1.0` → **11** 個文件
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

🔴 **6.** ` #龍芯⚡️2026-06-21-CNSH-CONTRIBUTING-MD-v1.0` → **10** 個文件
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

🔴 **7.** ` #龍芯⚡️2026-06-21-UI-INDEX-v1.0` → **9** 個文件
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

🔴 **9.** ` #龍芯⚡️2026-06-21-CNSH-LICENSE-MD-v1.0` → **7** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/dna_training_env/lib/python3.14/site-packages/uvicorn-0.38.0.dist-info/licenses/LICENSE.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/dna_training_env/lib/python3.14/site-packages/pip-25.3.dist-info/licenses/src/pip/_vendor/idna/LICENSE.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/dna_training_env/lib/python3.14/site-packages/idna-3.11.dist-info/licenses/LICENSE.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/dna_training_env/lib/python3.14/site-packages/pip/_vendor/idna/LICENSE.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/dna_training_env/lib/python3.14/site-packages/starlette-0.50.0.dist-info/licenses/LICENSE.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/cnsh-project/LICENSE.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/cnsh-project/LICENSE.md.sig`

🔴 **10.** ` #龍芯⚡️2026-06-21-CNSH-HELLO-v1.0` → **6** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/hello.longhun`
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-v1.0-完整实现/hello.cnsh`
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-v1.0-完整实现/hello`
   - `_archive/cnsh-history/CNSH_备份_20260211/19bd8da9-1792-8267-8000-093407b99859/hello.longhun`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/hello.cnsh`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/hello`

🔴 **11.** ` #龍芯⚡️2026-06-21-CNSH-LICENSE-v1.0` → **6** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/dna_training_env/lib/python3.14/site-packages/uvicorn-0.38.0.dist-info/licenses/LICENSE.md`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/dna_training_env/lib/python3.14/site-packages/pip-25.3.dist-info/licenses/src/pip/_vendor/idna/LICENSE.md`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/dna_training_env/lib/python3.14/site-packages/idna-3.11.dist-info/licenses/LICENSE.md`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/dna_training_env/lib/python3.14/site-packages/pip/_vendor/idna/LICENSE.md`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/dna_training_env/lib/python3.14/site-packages/starlette-0.50.0.dist-info/licenses/LICENSE.md`
   - `_archive/cnsh-history/CNSH-整理版/LICENSE`

🔴 **12.** ` #龍芯⚡️2026-06-21-CNSH-CHANGELOG-MD-v1.0` → **5** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CHANGELOG.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/CHANGELOG.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130124719/CHANGELOG.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/CHANGELOG.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/CHANGELOG.md.bak`

🔴 **13.** ` #龍芯⚡️2026-06-21-CNSH-使用说明-MD-v1.0` → **5** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH编辑器_普惠版/使用说明.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251207144453/CNSH_SecureSpace/使用说明.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/UID9622-LocalServer/使用说明.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/CNSH编辑器_普惠版/使用说明.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/CNSH编辑器_普惠版/使用说明.md.sig`

🔴 **14.** ` #龍芯⚡️2026-06-21-CNSH-IC_LAUNCHER-v1.0` → **5** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.android/app/src/main/res/mipmap-mdpi/ic_launcher.webp`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.android/app/src/main/res/mipmap-hdpi/ic_launcher.webp`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.webp`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.android/app/src/main/res/mipmap-xxhdpi/ic_launcher.webp`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.android/app/src/main/res/mipmap-xhdpi/ic_launcher.webp`

🔴 **15.** ` #龍芯⚡️2026-06-21-CNSH-IC_LAUNCHER_ROUND-v1.0` → **5** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.android/app/src/main/res/mipmap-mdpi/ic_launcher_round.webp`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.android/app/src/main/res/mipmap-hdpi/ic_launcher_round.webp`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.android/app/src/main/res/mipmap-xxxhdpi/ic_launcher_round.webp`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.android/app/src/main/res/mipmap-xxhdpi/ic_launcher_round.webp`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/examples/llama.android/app/src/main/res/mipmap-xhdpi/ic_launcher_round.webp`

🔴 **16.** ` #龍芯⚡️2026-06-21-CNSH-快速开始-MD-v1.0` → **5** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251207144453/MulanNotion/快速开始.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130124719/快速开始.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130124719/快速开始.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251205214827/快速开始.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/docs/快速开始.md.bak`

🟡 **17.** ` #龍芯⚡️2026-06-21-DOC-REQUIREMENTS-v1.0` → **4** 個文件
   - `baobao-guardian/backend/requirements.txt`
   - `releases/v5.1/staging/baobao-guardian/backend/requirements.txt`
   - `releases/v5.1/staging/control-panel/requirements.txt`
   - `control-panel/requirements.txt`

🟡 **18.** ` #龍芯⚡️2026-06-21-PROTOCOL-CNSH_V3-0_COMPLETE_CHARTER-v1.0` → **4** 個文件
   - `releases/v5.1/staging/protocols/CNSH_v3.0_COMPLETE_CHARTER.epub`
   - `releases/v5.1/staging/protocols/CNSH_v3.0_COMPLETE_CHARTER.docx`
   - `protocols/CNSH_v3.0_COMPLETE_CHARTER.epub`
   - `protocols/CNSH_v3.0_COMPLETE_CHARTER.docx`

🟡 **19.** ` #龍芯⚡️2026-06-21-CORE-HELLO-v1.0` → **4** 個文件
   - `cnsh-core.backup/language/hello.cnsh`
   - `cnsh-core.backup/language/hello`
   - `cnsh-core/language/hello.cnsh`
   - `cnsh-core/language/hello`

🟡 **20.** ` #龍芯⚡️2026-06-21-CNSH-快速启动-HTML-v1.0` → **4** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH编辑器_普惠版/快速启动.html.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH编辑器/快速启动.html.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/CNSH编辑器_普惠版/快速启动.html.bak`
   - `_archive/cnsh-history/CNSH-整理版/packages/cnsh-editor/快速启动.html.bak`

🟡 **21.** ` #龍芯⚡️2026-06-21-CNSH-INDEX-HTML-v1.0` → **4** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH编辑器_普惠版/index.html.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH编辑器/index.html.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/CNSH编辑器_普惠版/index.html.bak`
   - `_archive/cnsh-history/CNSH-整理版/packages/cnsh-editor/index.html.bak`

🟡 **22.** ` #龍芯⚡️2026-06-21-CNSH-快速启动指南-MD-v1.0` → **4** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/🚀快速启动指南.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/🚀快速启动指南.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251207144453/快速启动指南.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251207144453/cnsh-uid9622-system/快速启动指南.md.bak`

🟡 **23.** ` #龍芯⚡️2026-06-21-CNSH-ARTICLE_TEMPLATE-MD-v1.0` → **4** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/templates/article_template.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/templates/article_template.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/templates/combat-ready/article_template.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/templates/combat-ready/article_template.md.sig`

🟡 **24.** ` #龍芯⚡️2026-06-21-DOC-建立四库协作系统-4D1C016F996B4F9A9FC321AD29325DEB-v1.0` → **3** 個文件
   - `releases/v5.1/staging/04_決策日誌/decision-records/建立四库协作系统 4d1c016f996b4f9a9fc321ad29325deb.md`
   - `04_決策日誌/decision-records/建立四库协作系统 4d1c016f996b4f9a9fc321ad29325deb.md`
   - `docs/private-shared-imports/decision-records/建立四库协作系统 4d1c016f996b4f9a9fc321ad29325deb.md`

🟡 **25.** ` #龍芯⚡️2026-06-21-DOC-是否开源CNSH框架核心代码-356F230F4DA8486EA1C64DEE27105CA2-v1.0` → **3** 個文件
   - `releases/v5.1/staging/04_決策日誌/decision-records/是否开源CNSH框架核心代码 356f230f4da8486ea1c64dee27105ca2.md`
   - `04_決策日誌/decision-records/是否开源CNSH框架核心代码 356f230f4da8486ea1c64dee27105ca2.md`
   - `docs/private-shared-imports/decision-records/是否开源CNSH框架核心代码 356f230f4da8486ea1c64dee27105ca2.md`

🟡 **26.** ` #龍芯⚡️2026-06-21-CNSH-REQUIREMENTS-v1.0` → **3** 個文件
   - `releases/v5.1/staging/cnsh-terminal/requirements.txt`
   - `cnsh_terminal_v5.0/requirements.txt`
   - `cnsh-terminal/requirements.txt`

🟡 **27.** ` #龍芯⚡️2026-06-21-CNSH-TEST-v1.0` → **3** 個文件
   - `releases/v5.1/staging/cnsh-terminal/test.cnsh`
   - `cnsh_terminal_v5.0/test.cnsh`
   - `cnsh-terminal/test.cnsh`

🟡 **28.** ` #龍芯⚡️2026-06-21-CNSH-TERMINOLOGY-v1.0` → **3** 個文件
   - `releases/v5.1/staging/cnsh-terminal/data/terminology.db`
   - `cnsh_terminal_v5.0/data/terminology.db`
   - `cnsh-terminal/data/terminology.db`

🟡 **29.** ` #龍芯⚡️2026-06-21-DOC-SKILL-LAUNCHER使用说明-v1.0` → **3** 個文件
   - `releases/v5.1/staging/skills/SKILL-LAUNCHER使用说明.md`
   - `docs/v3/SKILL-LAUNCHER使用说明.md`
   - `skills/SKILL-LAUNCHER使用说明.md`

🟡 **30.** ` #龍芯⚡️2026-06-21-UI-SKILL-4-DOC-COAUTHORING-v1.0` → **3** 個文件
   - `releases/v5.1/staging/skills/html-skills/skill-4-doc-coauthoring.html`
   - `skills.backup/html-skills/skill-4-doc-coauthoring.html`
   - `skills/html-skills/skill-4-doc-coauthoring.html`

🟡 **31.** ` #龍芯⚡️2026-06-21-UI-SKILL-3-CANVAS-DESIGN-v1.0` → **3** 個文件
   - `releases/v5.1/staging/skills/html-skills/skill-3-canvas-design.html`
   - `skills.backup/html-skills/skill-3-canvas-design.html`
   - `skills/html-skills/skill-3-canvas-design.html`

🟡 **32.** ` #龍芯⚡️2026-06-21-CNSH-CODE_OF_CONDUCT-MD-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CODE_OF_CONDUCT.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/cnsh-project/CODE_OF_CONDUCT.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/cnsh-project/CODE_OF_CONDUCT.md.bak`

🟡 **33.** ` #龍芯⚡️2026-06-21-CNSH-TO_PUBLISH-MD-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/to_publish.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/to_publish.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251207144453/to_publish.md.bak`

🟡 **34.** ` #龍芯⚡️2026-06-21-CNSH-API-MD-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/龍魂永世唯一身份系统/docs/API.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130124719/API.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/BaoBao-AI-Assistant/docs/api.md.bak`

🟡 **35.** ` #龍芯⚡️2026-06-21-CNSH-INSTALL-MD-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/llama.cpp/docs/install.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/ecny-global-system/INSTALL.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/packages/dragon_soul_extension/INSTALL.md.bak`

🟡 **36.** ` #龍芯⚡️2026-06-21-CNSH-PROJECT_SUMMARY-MD-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/ecny-global-system/PROJECT_SUMMARY.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/PROJECT_SUMMARY.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/packages/dragon_soul_extension/PROJECT_SUMMARY.md.bak`

🟡 **37.** ` #龍芯⚡️2026-06-21-CNSH-可证明回滚机制部署-30C0717172428072A5D3CA87E24F98DE-MD-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/主控指令/LU主控指令库/可证明回滚机制部署 30c0717172428072a5d3ca87e24f98de.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/lu指令库/LU主控指令库/可证明回滚机制部署 30c0717172428072a5d3ca87e24f98de.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/lu指令库/LU主控指令库/可证明回滚机制部署 30c0717172428072a5d3ca87e24f98de.md.sig`

🟡 **38.** ` #龍芯⚡️2026-06-21-CNSH-自动翻译兼容系统激活-30C07171724280CAA997E9E7EB160B57-MD-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/主控指令/LU主控指令库/自动翻译兼容系统激活 30c07171724280caa997e9e7eb160b57.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/lu指令库/LU主控指令库/自动翻译兼容系统激活 30c07171724280caa997e9e7eb160b57.md.sig`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/lu指令库/LU主控指令库/自动翻译兼容系统激活 30c07171724280caa997e9e7eb160b57.md.bak`

🟡 **39.** ` #龍芯⚡️2026-06-21-CNSH-因果图索引系统建立-30C07171724280978C2FC2B6107DEF94-MD-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/主控指令/LU主控指令库/因果图索引系统建立 30c07171724280978c2fc2b6107def94.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/lu指令库/LU主控指令库/因果图索引系统建立 30c07171724280978c2fc2b6107def94.md.sig`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/lu指令库/LU主控指令库/因果图索引系统建立 30c07171724280978c2fc2b6107def94.md.bak`

🟡 **40.** ` #龍芯⚡️2026-06-21-CNSH-量子神经网络架构部署-30C07171724280388E56FFA24A8D50F8-MD-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/主控指令/LU主控指令库/量子神经网络架构部署 30c07171724280388e56ffa24a8d50f8.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/lu指令库/LU主控指令库/量子神经网络架构部署 30c07171724280388e56ffa24a8d50f8.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/lu指令库/LU主控指令库/量子神经网络架构部署 30c07171724280388e56ffa24a8d50f8.md.sig`

🟡 **41.** ` #龍芯⚡️2026-06-21-CNSH-三色审计系统注册激活-30C071717242808DA649D47129FB8C1B-MD-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/主控指令/LU主控指令库/三色审计系统注册激活 30c071717242808da649d47129fb8c1b.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/lu指令库/LU主控指令库/三色审计系统注册激活 30c071717242808da649d47129fb8c1b.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/lu指令库/LU主控指令库/三色审计系统注册激活 30c071717242808da649d47129fb8c1b.md.sig`

🟡 **42.** ` #龍芯⚡️2026-06-21-CNSH-龍魂精神核心价值观注入-30C07171724280579F70E90DF2B93A9F-MD-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/主控指令/LU主控指令库/龍魂精神核心价值观注入 30c07171724280579f70e90df2b93a9f.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/lu指令库/LU主控指令库/龍魂精神核心价值观注入 30c07171724280579f70e90df2b93a9f.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/lu指令库/LU主控指令库/龍魂精神核心价值观注入 30c07171724280579f70e90df2b93a9f.md.sig`

🟡 **43.** ` #龍芯⚡️2026-06-21-CNSH-DNA追溯系统永久记录启用-30C07171724280EE997BFE3CABE0BBD0-MD-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/主控指令/LU主控指令库/DNA追溯系统永久记录启用 30c07171724280ee997bfe3cabe0bbd0.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/lu指令库/LU主控指令库/DNA追溯系统永久记录启用 30c07171724280ee997bfe3cabe0bbd0.md.sig`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/lu指令库/LU主控指令库/DNA追溯系统永久记录启用 30c07171724280ee997bfe3cabe0bbd0.md.bak`

🟡 **44.** ` #龍芯⚡️2026-06-21-CNSH-冷热分层存储策略配置-30C07171724280339B91E0DC19400BD8-MD-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/主控指令/LU主控指令库/冷热分层存储策略配置 30c07171724280339b91e0dc19400bd8.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/lu指令库/LU主控指令库/冷热分层存储策略配置 30c07171724280339b91e0dc19400bd8.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/lu指令库/LU主控指令库/冷热分层存储策略配置 30c07171724280339b91e0dc19400bd8.md.sig`

🟡 **45.** ` #龍芯⚡️2026-06-21-CNSH-无标题-30C071717242805CBE1EE340C056DF47-MD-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/主控指令/LU主控指令库/无标题 30c071717242805cbe1ee340c056df47.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/lu指令库/LU主控指令库/无标题 30c071717242805cbe1ee340c056df47.md.sig`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/lu指令库/LU主控指令库/无标题 30c071717242805cbe1ee340c056df47.md.bak`

🟡 **46.** ` #龍芯⚡️2026-06-21-CNSH-多维度多位面执行引擎启动-30C07171724280408D68C85FB9BE6A97-MD-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/主控指令/LU主控指令库/多维度多位面执行引擎启动 30c07171724280408d68c85fb9be6a97.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/lu指令库/LU主控指令库/多维度多位面执行引擎启动 30c07171724280408d68c85fb9be6a97.md.sig`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/lu指令库/LU主控指令库/多维度多位面执行引擎启动 30c07171724280408d68c85fb9be6a97.md.bak`

🟡 **47.** ` #龍芯⚡️2026-06-21-CNSH-CNSH_AUDIO_RENDER_V1-v1.0` → **3** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/龍魂系统核心/cnsh_audio_render_v1.cnsh_副本`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/龍魂系统核心/cnsh_audio_render_v1.cnsh`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/龍魂系统核心/files/cnsh_audio_render_v1.cnsh`

🔵 **48.** ` #龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-v2.0` → **2** 個文件
   - `SESSION_SUMMARY_20260603.md`
   - `_archive/cnsh-history/CNSH_备份_20260211/.claude.json`

🔵 **49.** `#龍芯⚡️2026-06-07-BRAIN-NOTION-SYNC-FILE3-v1.1` → **2** 個文件
   - `brain_notion_sync.py`
   - `brain/brain_notion_sync.py`

🔵 **50.** ` #龍芯⚡️2026-06-21-DOC-ATTRIBUTION-v1.0` → **2** 個文件
   - `ATTRIBUTION.md`
   - `docs/claude-backlog/07_开源模板/ATTRIBUTION.md`

🔵 **51.** ` #龍芯⚡️2026-06-21-UI-PERSONA_CERT_TEMPLATE-v1.0` → **2** 個文件
   - `persona_cert_template.html`
   - `docs/persona_cert_template.html`

🔵 **52.** ` #龍芯⚡️2026-06-21-ENGINE-VITE-CONFIG-v1.0` → **2** 個文件
   - `baobao-guardian/frontend/vite.config.ts`
   - `releases/v5.1/staging/baobao-guardian/frontend/vite.config.ts`

🔵 **53.** ` #龍芯⚡️2026-06-21-MODULE-MAIN-v1.0` → **2** 個文件
   - `baobao-guardian/frontend/src/main.tsx`
   - `releases/v5.1/staging/baobao-guardian/frontend/src/main.tsx`

🔵 **54.** ` #龍芯⚡️2026-06-04-BAOBAO-ENV-v1.0` → **2** 個文件
   - `baobao-guardian/backend/.env`
   - `releases/v5.1/staging/baobao-guardian/backend/.env`

🔵 **55.** `#龍芯⚡️2026-06-18-STARRY-MEMORY-FILE1-v1.0` → **2** 個文件
   - `releases/v5.1/staging/memory-universe/index.md`
   - `memory-universe/星辰记忆系统.py`

🔵 **56.** ` #龍芯⚡️2026-06-21-MODULE-星辰记忆-v1.0` → **2** 個文件
   - `releases/v5.1/staging/memory-universe/星辰记忆.db`
   - `memory-universe/星辰记忆.db`

🔵 **57.** ` #龍芯⚡️2026-06-21-ENGINE-INTEGRATE_PRIVATE_SHARED_BATCH2-v1.0` → **2** 個文件
   - `releases/v5.1/staging/bin/integrate_private_shared_batch2.py`
   - `bin/integrate_private_shared_batch2.py`

🔵 **58.** ` #龍芯⚡️2026-06-21-ENGINE-INTEGRATE_CNSH_UID9622-v1.0` → **2** 個文件
   - `releases/v5.1/staging/bin/integrate_cnsh_uid9622.py`
   - `bin/integrate_cnsh_uid9622.py`

🔵 **59.** ` #龍芯⚡️2026-06-21-TOOL-START_PERSONA_API-v1.0` → **2** 個文件
   - `releases/v5.1/staging/bin/start_persona_api.sh`
   - `bin/start_persona_api.sh`

🔵 **60.** ` #龍芯⚡️2026-06-21-ENGINE-GENERATE_WORKSPACE_METADATA-v1.0` → **2** 個文件
   - `releases/v5.1/staging/bin/generate_workspace_metadata.py`
   - `bin/generate_workspace_metadata.py`

🔵 **61.** ` #龍芯⚡️2026-06-21-ENGINE-PERSONA_SCHEDULER-v1.0` → **2** 個文件
   - `releases/v5.1/staging/bin/persona_scheduler.py`
   - `bin/persona_scheduler.py`

🔵 **62.** ` #龍芯⚡️2026-06-21-TOOL-SKILL-LAUNCHER-V3-v1.0` → **2** 個文件
   - `releases/v5.1/staging/bin/skill-launcher-v3.sh`
   - `bin/skill-launcher-v3.sh`

🔵 **63.** ` #龍芯⚡️2026-06-21-ENGINE-RUN_PERSONA_API-v1.0` → **2** 個文件
   - `releases/v5.1/staging/bin/run_persona_api.py`
   - `bin/run_persona_api.py`

🔵 **64.** ` #龍芯⚡️2026-06-21-TOOL-启动人格代理-v1.0` → **2** 個文件
   - `releases/v5.1/staging/bin/启动人格代理.sh`
   - `bin/启动人格代理.sh`

🔵 **65.** ` #龍芯⚡️2026-06-21-ENGINE-ORGANIZE_LONGHUN_TECH-v1.0` → **2** 個文件
   - `releases/v5.1/staging/bin/organize_longhun_tech.py`
   - `bin/organize_longhun_tech.py`

🔵 **66.** ` #龍芯⚡️2026-06-21-ENGINE-SKILL_WRAPPERS-v1.0` → **2** 個文件
   - `releases/v5.1/staging/control-panel/api/skill_wrappers.py`
   - `control-panel/api/skill_wrappers.py`

🔵 **67.** ` #龍芯⚡️2026-06-21-ENGINE-FOUNDATION_WRAPPERS-v1.0` → **2** 個文件
   - `releases/v5.1/staging/control-panel/api/foundation_wrappers.py`
   - `control-panel/api/foundation_wrappers.py`

🔵 **68.** ` #龍芯⚡️2026-06-21-CNSH-INFO-v1.0` → **2** 個文件
   - `releases/v5.1/staging/cnsh/info.md`
   - `cnsh/info.md`

🔵 **69.** `#龍芯⚡️2026-06-06-THREE-INTEGRATION-SYNC-HUB-v1.0` → **2** 個文件
   - `releases/v5.1/staging/cnsh/sancai_sync/README.md`
   - `cnsh/sancai_sync/README.md`

🔵 **70.** ` #龍芯⚡️2026-06-06-SANCAI-SYNC-TEST-SUITE-v1.0` → **2** 個文件
   - `releases/v5.1/staging/cnsh/sancai_sync/tests/test_sancai_sync_hub.py`
   - `cnsh/sancai_sync/tests/test_sancai_sync_hub.py`

🔵 **71.** ` #龍芯⚡️2026-06-21-DOC-DNA-GEN-v1.0` → **2** 個文件
   - `releases/v5.1/staging/01_技能庫/dna-gen.md`
   - `01_技能庫/dna-gen.md`

🔵 **72.** ` #龍芯⚡️2026-06-21-DOC-ON-TRANSLATE-v1.0` → **2** 個文件
   - `releases/v5.1/staging/01_技能庫/on-translate.md`
   - `01_技能庫/on-translate.md`

🔵 **73.** ` #龍芯⚡️2026-06-21-DOC-ON-IDENTITY-v1.0` → **2** 個文件
   - `releases/v5.1/staging/01_技能庫/on-identity.md`
   - `01_技能庫/on-identity.md`

🔵 **74.** ` #龍芯⚡️2026-06-21-CNSH-龍魂协议-v1.0` → **2** 個文件
   - `releases/v5.1/staging/cnsh-terminal/龍魂协议.txt`
   - `cnsh-terminal/龍魂协议.txt`

🔵 **75.** ` #龍芯⚡️2026-06-21-BRAIN-MEMORIES-v1.0` → **2** 個文件
   - `releases/v5.1/staging/brain/memories.db`
   - `brain/memories.db`

🔵 **76.** ` #龍芯⚡️2026-06-21-ENGINE-SHIELD_TEST_EXAMPLE-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/longhun-shield/shield_test_example.py`
   - `skills/longhun-shield/shield_test_example.py`

🔵 **77.** ` #龍芯⚡️2026-06-21-DOC-SKILL-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/warehouse-audit/SKILL.md`
   - `skills/warehouse-audit/SKILL.md`

🔵 **78.** ` #龍芯⚡️2026-06-21-MODULE-DEMO_WMS-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/warehouse-audit/demo_wms_data/demo_wms.db`
   - `skills/warehouse-audit/demo_wms_data/demo_wms.db`

🔵 **79.** ` #龍芯⚡️2026-06-21-MODULE-ORDERS-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/warehouse-audit/demo_wms_data/demo_wms_csv/orders.csv`
   - `skills/warehouse-audit/demo_wms_data/demo_wms_csv/orders.csv`

🔵 **80.** ` #龍芯⚡️2026-06-21-MODULE-OPERATIONS-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/warehouse-audit/demo_wms_data/demo_wms_csv/operations.csv`
   - `skills/warehouse-audit/demo_wms_data/demo_wms_csv/operations.csv`

🔵 **81.** ` #龍芯⚡️2026-06-21-MODULE-WAREHOUSE_METRICS-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/warehouse-audit/demo_wms_data/demo_wms_csv/warehouse_metrics.csv`
   - `skills/warehouse-audit/demo_wms_data/demo_wms_csv/warehouse_metrics.csv`

🔵 **82.** ` #龍芯⚡️2026-06-21-MODULE-INVENTORY-v1.0` → **2** 個文件
   - `releases/v5.1/staging/skills/warehouse-audit/demo_wms_data/demo_wms_csv/inventory.csv`
   - `skills/warehouse-audit/demo_wms_data/demo_wms_csv/inventory.csv`

🔵 **83.** ` #龍芯⚡️2026-06-21-PROTOCOL-PROTOCOL_UNIFICATION_COMPLETION_REPORT-v1.0` → **2** 個文件
   - `releases/v5.1/staging/protocols/PROTOCOL_UNIFICATION_COMPLETION_REPORT.md`
   - `protocols/PROTOCOL_UNIFICATION_COMPLETION_REPORT.md`

🔵 **84.** ` #龍芯⚡️2026-06-21-PROTOCOL-CNSH_V3-0_COMPLETE_FULL_NO_EMOJI-v1.0` → **2** 個文件
   - `releases/v5.1/staging/protocols/_DEPRECATED_CNSH_v2.0_v3.0_2026-06-08/CNSH_v3.0_COMPLETE_FULL_no_emoji.md`
   - `protocols/_DEPRECATED_CNSH_v2.0_v3.0_2026-06-08/CNSH_v3.0_COMPLETE_FULL_no_emoji.md`

🔵 **85.** ` #龍芯⚡️2026-06-21-DOC-AUDIT_THREE_COLOR-v1.0` → **2** 個文件
   - `releases/v5.1/staging/crypto-stack/audit_three_color.md`
   - `crypto-stack/audit_three_color.md`

🔵 **86.** ` #龍芯⚡️2026-06-21-ENGINE-L6_SOUL-v1.0` → **2** 個文件
   - `releases/v5.1/staging/crypto-stack/src/l6_soul.py`
   - `crypto-stack/src/l6_soul.py`

🔵 **87.** ` #龍芯⚡️2026-06-21-ENGINE-WEIGHT_TUNER-v1.0` → **2** 個文件
   - `releases/v5.1/staging/crypto-stack/src/weight_tuner.py`
   - `crypto-stack/src/weight_tuner.py`

🔵 **88.** ` #龍芯⚡️2026-06-21-ENGINE-L1_PHYSICAL-v1.0` → **2** 個文件
   - `releases/v5.1/staging/crypto-stack/src/l1_physical.py`
   - `crypto-stack/src/l1_physical.py`

🔵 **89.** ` #龍芯⚡️2026-06-21-ENGINE-STACK_RUNNER-v1.0` → **2** 個文件
   - `releases/v5.1/staging/crypto-stack/src/stack_runner.py`
   - `crypto-stack/src/stack_runner.py`

🔵 **90.** ` #龍芯⚡️2026-06-21-ENGINE-L4_SEVEN_FACTOR-v1.0` → **2** 個文件
   - `releases/v5.1/staging/crypto-stack/src/l4_seven_factor.py`
   - `crypto-stack/src/l4_seven_factor.py`

🔵 **91.** ` #龍芯⚡️2026-06-21-DNA-MODULE-DNA库建库-本地回写-实时展现-v1.0` → **2** 個文件
   - `docs/private-shared-imports/memory-dna/DNA库建库·本地回写·实时展现.md`
   - `docs/private-shared-imports/memory-dna/DNA库建库-本地回写-实时展现.md`

🔵 **92.** ` #龍芯⚡️2026-06-21-PROTOCOL-CNSH-GITHUB-README-v1.0` → **2** 個文件
   - `docs/private-shared-imports/cnsh-protocols/📄 CNSH GitHub README.md`
   - `docs/private-shared-imports/cnsh-protocols/CNSH-GitHub-README.md`

🔵 **93.** ` #龍芯⚡️2026-06-21-GOVERNANCE-ETHICS_REVIEW_MVP-PY-伦理审查终端MVP-v1.0` → **2** 個文件
   - `docs/private-shared-imports/governance/🐍 ethics_review_mvp py（伦理审查终端MVP）.md`
   - `docs/private-shared-imports/governance/⚖️ ethics_review_mvp py (伦理审查终端MVP).md`

🔵 **94.** ` #龍芯⚡️2026-06-21-GOVERNANCE-龍魂七維AI治理-數字主權執行表-V1-0-v1.0` → **2** 個文件
   - `docs/private-shared-imports/governance/⚖️ 龍魂七維AI治理×數字主權執行表 v1 0.csv`
   - `docs/private-shared-imports/governance/龍魂七維AI治理×數字主權執行表-v1.0.csv`

🔵 **95.** ` #龍芯⚡️2026-06-21-DOC-INDEX-v1.0` → **2** 個文件
   - `docs/v3/INDEX.md`
   - `project-memory/index.md`

🔵 **96.** ` #龍芯⚡️2026-06-21-DOC-PLAN-v1.0` → **2** 個文件
   - `docs/v3/plan.md`
   - `integrated-modules/kimi_agent/plan.md`

🔵 **97.** ` #龍芯⚡️2026-06-21-MODULE-HELLO-v1.0` → **2** 個文件
   - `docs/claude-backlog/02_CNSH语言/hello.cnsh`
   - `docs/claude-backlog/02_CNSH语言/hello`

🔵 **98.** ` #龍芯⚡️2026-06-21-DOC-权限管理与审计追踪中心-v1.0` → **2** 個文件
   - `docs/uid9622-hosted/control-panel/🛡️ 权限管理与审计追踪中心.md`
   - `docs/longhun-tech/audit/🛡️ 权限管理与审计追踪中心.md`

🔵 **99.** ` #龍芯⚡️2026-06-21-CNSH-README-v1.0` → **2** 個文件
   - `docs/cnsh-uid9622/README.md`
   - `extensions/cnsh-chrome-plugin/README.md`

🔵 **100.** ` #龍芯⚡️2026-06-21-CNSH-POPUP-v1.0` → **2** 個文件
   - `extensions/cnsh-chrome-plugin/popup.js`
   - `extensions/cnsh-chrome-plugin/popup.html`

🔵 **101.** ` #龍芯⚡️2026-06-21-CNSH-OPTIONS-v1.0` → **2** 個文件
   - `extensions/cnsh-chrome-plugin/options.js`
   - `extensions/cnsh-chrome-plugin/options.html`

🔵 **102.** ` #龍芯⚡️2026-06-21-MODULE-SIDEPANEL-HTML-v1.0` → **2** 個文件
   - `extensions/LongHunWidget/sidepanel.html.bak2`
   - `extensions/LongHunWidget/sidepanel.html.bak`

🔵 **103.** `#龍芯⚡️2026-06-06-CODE-AUDIT-FILE1-v3.0` → **2** 個文件
   - `06_技術文檔/skill_code-audit.md`
   - `01_技能庫/code-audit.md`

🔵 **104.** `#龍芯⚡️2026-06-06-KIMI-WEBBRIDGE-FILE1-v1.0` → **2** 個文件
   - `06_技術文檔/skill_kimi-webbridge.md`
   - `01_技能庫/kimi-webbridge.md`

🔵 **105.** `#龍芯⚡️2026-06-04-KFPP-EXECUTOR-FILE1-v1.0` → **2** 個文件
   - `executors/kfpp/longhun_kfpp_executor_v1.0.py`
   - `systems/kfpp/README.md`

🔵 **106.** ` #龍芯⚡️2026-06-21-SCRIPT-DEMO_INPUT-v1.0` → **2** 個文件
   - `scripts/demo_input.txt`
   - `scripts/demo_input.shortcode`

🔵 **107.** ` #龍芯⚡️2026-06-21-CORE-FEARLESS_STEVE_PROTOCOL_V2-0_USAGE_GUIDE-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/FEARLESS_STEVE_PROTOCOL_v2.0_USAGE_GUIDE.md.bak`
   - `cnsh-core/FEARLESS_STEVE_PROTOCOL_v2.0_USAGE_GUIDE.md.bak`

🔵 **108.** ` #龍芯⚡️2026-06-21-CORE-MEMORY_PACK_V3-PY-v1.0` → **2** 個文件
   - `cnsh-core.backup/memory_pack_v3.py.bak`
   - `cnsh-core/memory_pack_v3.py.bak`

🔵 **109.** ` #龍芯⚡️2026-06-21-CORE-PARSE_NOTION-v1.0` → **2** 個文件
   - `cnsh-core.backup/parse_notion.py`
   - `cnsh-core/parse_notion.py`

🔵 **110.** ` #龍芯⚡️2026-06-21-CORE-NOTION_TASK5_SETUP-PY-v1.0` → **2** 個文件
   - `cnsh-core.backup/notion_task5_setup.py.bak`
   - `cnsh-core/notion_task5_setup.py.bak`

🔵 **111.** ` #龍芯⚡️2026-06-21-CORE-FEARLESS_STEVE_PROTOCOL_V2-0_IMPLEMENTATION-CPP-v1.0` → **2** 個文件
   - `cnsh-core.backup/FEARLESS_STEVE_PROTOCOL_v2.0_IMPLEMENTATION.cpp.bak`
   - `cnsh-core/FEARLESS_STEVE_PROTOCOL_v2.0_IMPLEMENTATION.cpp.bak`

🔵 **112.** ` #龍芯⚡️2026-06-21-CORE-AUDIT_README-v1.0` → **2** 個文件
   - `cnsh-core.backup/AUDIT_README.md`
   - `cnsh-core/AUDIT_README.md`

🔵 **113.** ` #龍芯⚡️2026-06-03-CORE-SYSTEM-LAUNCHER-v1.0` → **2** 個文件
   - `cnsh-core.backup/core_system_launcher.py`
   - `cnsh-core/core_system_launcher.py`

🔵 **114.** ` #龍芯⚡️2026-06-21-CORE-MAIN_FEARLESS_STEVE-CPP-v1.0` → **2** 個文件
   - `cnsh-core.backup/main_fearless_steve.cpp.bak`
   - `cnsh-core/main_fearless_steve.cpp.bak`

🔵 **115.** ` #龍芯⚡️2026-06-21-CORE-M05_WUXING_CALCULATOR-v1.0` → **2** 個文件
   - `cnsh-core.backup/m05_wuxing_calculator.py`
   - `cnsh-core/m05_wuxing_calculator.py`

🔵 **116.** ` #龍芯⚡️2026-06-21-CORE-FEARLESS_STEVE_PROTOCOL_V2-0_MULTI_PERSONA_ENGINE-CPP-v1.0` → **2** 個文件
   - `cnsh-core.backup/FEARLESS_STEVE_PROTOCOL_v2.0_MULTI_PERSONA_ENGINE.cpp.bak`
   - `cnsh-core/FEARLESS_STEVE_PROTOCOL_v2.0_MULTI_PERSONA_ENGINE.cpp.bak`

🔵 **117.** ` #龍芯⚡️2026-06-21-CORE-M04_YIJING_ENGINE-v1.0` → **2** 個文件
   - `cnsh-core.backup/m04_yijing_engine.py`
   - `cnsh-core/m04_yijing_engine.py`

🔵 **118.** ` #龍芯⚡️2026-06-21-CORE-LONGHUN_WUXING_MVP-v1.0` → **2** 個文件
   - `cnsh-core.backup/wuxing/longhun_wuxing_mvp.py`
   - `cnsh-core/wuxing/longhun_wuxing_mvp.py`

🔵 **119.** ` #龍芯⚡️2026-06-21-CORE-CNSH-第一批创建完成报告-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/language/CNSH-第一批创建完成报告.md.bak`
   - `cnsh-core/language/CNSH-第一批创建完成报告.md.bak`

🔵 **120.** ` #龍芯⚡️2026-06-21-CORE-设置-CNSH文件关联-SH-v1.0` → **2** 個文件
   - `cnsh-core.backup/language/设置-cnsh文件关联.sh.bak`
   - `cnsh-core/language/设置-cnsh文件关联.sh.bak`

🔵 **121.** ` #龍芯⚡️2026-06-21-CORE-TEST-FUNCTION-CALL-v1.0` → **2** 個文件
   - `cnsh-core.backup/language/test-function-call.cnsh`
   - `cnsh-core/language/test-function-call.cnsh`

🔵 **122.** ` #龍芯⚡️2026-06-21-CORE-CNSH_本地人格配置_V1-0-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/language/CNSH_本地人格配置_v1.0.md.bak`
   - `cnsh-core/language/CNSH_本地人格配置_v1.0.md.bak`

🔵 **123.** ` #龍芯⚡️2026-06-21-CORE-CNSH编辑器-完成报告-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/language/CNSH编辑器-完成报告.md.bak`
   - `cnsh-core/language/CNSH编辑器-完成报告.md.bak`

🔵 **124.** ` #龍芯⚡️2026-06-21-CORE-CNSH编辑器-HTML-v1.0` → **2** 個文件
   - `cnsh-core.backup/language/CNSH编辑器.html.bak`
   - `cnsh-core/language/CNSH编辑器.html.bak`

🔵 **125.** ` #龍芯⚡️2026-06-21-CORE-编译器修复完成-立即测试-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/language/编译器修复完成-立即测试.md.bak`
   - `cnsh-core/language/编译器修复完成-立即测试.md.bak`

🔵 **126.** ` #龍芯⚡️2026-06-21-CORE-CNSH编辑器-使用指南-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/language/CNSH编辑器-使用指南.md.bak`
   - `cnsh-core/language/CNSH编辑器-使用指南.md.bak`

🔵 **127.** ` #龍芯⚡️2026-06-21-CORE-CNSH-语言配件集成-执行完成报告-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/language/CNSH-语言配件集成-执行完成报告.md.bak`
   - `cnsh-core/language/CNSH-语言配件集成-执行完成报告.md.bak`

🔵 **128.** ` #龍芯⚡️2026-06-21-CORE-编译修复报告-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/language/编译修复报告.md.bak`
   - `cnsh-core/language/编译修复报告.md.bak`

🔵 **129.** ` #龍芯⚡️2026-06-21-CORE-快速打开CNSH文件-使用指南-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/language/快速打开cnsh文件-使用指南.md.bak`
   - `cnsh-core/language/快速打开cnsh文件-使用指南.md.bak`

🔵 **130.** ` #龍芯⚡️2026-06-21-CORE-CNSH完整规范-NOTION版-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/language/CNSH完整规范-Notion版.md.bak`
   - `cnsh-core/language/CNSH完整规范-Notion版.md.bak`

🔵 **131.** ` #龍芯⚡️2026-06-21-CORE-CNSH-语言配件集成完成报告-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/language/CNSH-语言配件集成完成报告.md.bak`
   - `cnsh-core/language/CNSH-语言配件集成完成报告.md.bak`

🔵 **132.** ` #龍芯⚡️2026-06-21-CORE-编译运行-SH-v1.0` → **2** 個文件
   - `cnsh-core.backup/language/编译运行.sh.bak`
   - `cnsh-core/language/编译运行.sh.bak`

🔵 **133.** ` #龍芯⚡️2026-06-21-CORE-CNSH_龍魂底线协议_双轨治理_V1-0-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/language/CNSH_龍魂底线协议_双轨治理_v1.0.md.bak`
   - `cnsh-core/language/CNSH_龍魂底线协议_双轨治理_v1.0.md.bak`

🔵 **134.** ` #龍芯⚡️2026-06-21-CORE-个体户收支分析-v1.0` → **2** 個文件
   - `cnsh-core.backup/language/个体户收支分析.cnsh`
   - `cnsh-core/language/个体户收支分析.cnsh`

🔵 **135.** ` #龍芯⚡️2026-06-21-CORE-编译器语法修复-说明-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/language/编译器语法修复-说明.md.bak`
   - `cnsh-core/language/编译器语法修复-说明.md.bak`

🔵 **136.** ` #龍芯⚡️2026-06-21-CORE-CNSH_RUNTIME_CORE-PY-v1.0` → **2** 個文件
   - `cnsh-core.backup/runtime-governance/cnsh_runtime_core.py.bak`
   - `cnsh-core/runtime-governance/cnsh_runtime_core.py.bak`

🔵 **137.** ` #龍芯⚡️2026-06-21-CORE-CNSH_RUNTIME_GOVERNANCE_MATHEMATICS_完整版_V3-0-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/runtime-governance/CNSH_Runtime_Governance_Mathematics_完整版_v3.0.md.bak`
   - `cnsh-core/runtime-governance/CNSH_Runtime_Governance_Mathematics_完整版_v3.0.md.bak`

🔵 **138.** ` #龍芯⚡️2026-06-21-CORE-龍魂全球AI终端强制执行令_V1-0-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/规范/龍魂全球AI终端强制执行令_v1.0.md.bak`
   - `cnsh-core/规范/龍魂全球AI终端强制执行令_v1.0.md.bak`

🔵 **139.** ` #龍芯⚡️2026-06-21-CORE-龍魂老大主权令_UID9622终端规则_V1-0-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/规范/龍魂老大主权令_UID9622终端规则_v1.0.md.bak`
   - `cnsh-core/规范/龍魂老大主权令_UID9622终端规则_v1.0.md.bak`

🔵 **140.** ` #龍芯⚡️2026-06-21-CORE-审计宪法第四章-耻辱墙完整设计-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/audit-constitution/审计宪法第四章-耻辱墙完整设计.md.bak`
   - `cnsh-core/audit-constitution/审计宪法第四章-耻辱墙完整设计.md.bak`

🔵 **141.** ` #龍芯⚡️2026-06-21-CORE-审计宪法第三章-智能身份认证审计-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/audit-constitution/审计宪法第三章-智能身份认证审计.md.bak`
   - `cnsh-core/audit-constitution/审计宪法第三章-智能身份认证审计.md.bak`

🔵 **142.** ` #龍芯⚡️2026-06-21-CORE-审计宪法第六章-DNA派生自适应系统-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/audit-constitution/审计宪法第六章-DNA派生自适应系统.md.bak`
   - `cnsh-core/audit-constitution/审计宪法第六章-DNA派生自适应系统.md.bak`

🔵 **143.** ` #龍芯⚡️2026-06-21-CORE-审计宪法第一章-永恒锚与核心宪法-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/audit-constitution/审计宪法第一章-永恒锚与核心宪法.md.bak`
   - `cnsh-core/audit-constitution/审计宪法第一章-永恒锚与核心宪法.md.bak`

🔵 **144.** ` #龍芯⚡️2026-06-21-CORE-审计宪法第二章-64卦审计天气系统-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/audit-constitution/审计宪法第二章-64卦审计天气系统.md.bak`
   - `cnsh-core/audit-constitution/审计宪法第二章-64卦审计天气系统.md.bak`

🔵 **145.** ` #龍芯⚡️2026-06-21-CORE-审计宪法第五章-意见反馈五阶段审计-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/audit-constitution/审计宪法第五章-意见反馈五阶段审计.md.bak`
   - `cnsh-core/audit-constitution/审计宪法第五章-意见反馈五阶段审计.md.bak`

🔵 **146.** ` #龍芯⚡️2026-06-21-CORE-PYTEST-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/pytest.ini`
   - `cnsh-core/ai-tools/operation_log_engine/pytest.ini`

🔵 **147.** ` #龍芯⚡️2026-06-21-CORE-ENCRYPTION_ENFORCE_REPORT-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/ENCRYPTION_ENFORCE_REPORT.md.bak`
   - `cnsh-core/ai-tools/operation_log_engine/ENCRYPTION_ENFORCE_REPORT.md.bak`

🔵 **148.** ` #龍芯⚡️2026-05-30-ENV-CONFIG-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/.env.example`
   - `cnsh-core/ai-tools/operation_log_engine/.env.example`

🔵 **149.** ` #龍芯⚡️2026-06-21-CORE-ENCRYPTION_ENFORCE-PY-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/operation_log_engine/encryption_enforce.py.bak`
   - `cnsh-core/ai-tools/operation_log_engine/operation_log_engine/encryption_enforce.py.bak`

🔵 **150.** ` #龍芯⚡️2026-06-21-CORE-TOP_LEVEL-TXT-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/top_level.txt.bak`
   - `cnsh-core/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/top_level.txt.bak`

🔵 **151.** ` #龍芯⚡️2026-06-21-CORE-PKG-INFO-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/PKG-INFO`
   - `cnsh-core/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/PKG-INFO`

🔵 **152.** ` #龍芯⚡️2026-06-21-CORE-DEPENDENCY_LINKS-TXT-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/dependency_links.txt.bak`
   - `cnsh-core/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/dependency_links.txt.bak`

🔵 **153.** ` #龍芯⚡️2026-06-21-CORE-NOT-ZIP-SAFE-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/not-zip-safe`
   - `cnsh-core/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/not-zip-safe`

🔵 **154.** ` #龍芯⚡️2026-06-21-CORE-ENTRY_POINTS-TXT-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/entry_points.txt.bak`
   - `cnsh-core/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/entry_points.txt.bak`

🔵 **155.** ` #龍芯⚡️2026-06-21-CORE-REQUIRES-TXT-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/requires.txt.bak`
   - `cnsh-core/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/requires.txt.bak`

🔵 **156.** ` #龍芯⚡️2026-06-21-CORE-SOURCES-TXT-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/SOURCES.txt.bak`
   - `cnsh-core/ai-tools/operation_log_engine/longhun_operation_log_engine.egg-info/SOURCES.txt.bak`

🔵 **157.** ` #龍芯⚡️2026-06-21-CORE-START_SENTINEL-SH-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/longhu_sentinel_bot/start_sentinel.sh.bak`
   - `cnsh-core/ai-tools/longhu_sentinel_bot/start_sentinel.sh.bak`

🔵 **158.** ` #龍芯⚡️2026-06-21-CORE-TOKEN_MANAGER-PY-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/longhu_sentinel_bot/token_manager.py.bak`
   - `cnsh-core/ai-tools/longhu_sentinel_bot/token_manager.py.bak`

🔵 **159.** ` #龍芯⚡️2026-06-21-CORE-SENTINEL_BOT-PY-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/longhu_sentinel_bot/sentinel_bot.py.bak`
   - `cnsh-core/ai-tools/longhu_sentinel_bot/sentinel_bot.py.bak`

🔵 **160.** ` #龍芯⚡️2026-06-21-CORE-README-MD-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/longhu_sentinel_bot/README.md.bak`
   - `cnsh-core/ai-tools/longhu_sentinel_bot/README.md.bak`

🔵 **161.** ` #龍芯⚡️2026-06-21-CORE-TELEGRAM_HANDLER-PY-v1.0` → **2** 個文件
   - `cnsh-core.backup/ai-tools/longhu_sentinel_bot/telegram_handler.py.bak`
   - `cnsh-core/ai-tools/longhu_sentinel_bot/telegram_handler.py.bak`

🔵 **162.** ` #龍芯⚡️2026-06-21-CORE-AUDIT_ENGINE-v1.0` → **2** 個文件
   - `cnsh-core.backup/engines/audit_engine.py`
   - `cnsh-core/engines/audit_engine.py`

🔵 **163.** ` #龍芯⚡️2026-06-21-CORE-DRAGON_SOUL_9622-v1.0` → **2** 個文件
   - `cnsh-core.backup/longhun-flow-system/dragon_soul_9622.html`
   - `cnsh-core/longhun-flow-system/dragon_soul_9622.html`

🔵 **164.** ` #龍芯⚡️2026-04-19-三才流場-v8` → **2** 個文件
   - `cnsh-core.backup/longhun-flow-system/current.html`
   - `cnsh-core/longhun-flow-system/current.html`

🔵 **165.** ` #龍芯⚡️2026-06-21-CORE-LONGHUN-28MANSIONS-V1-v1.0` → **2** 個文件
   - `cnsh-core.backup/longhun-flow-system/longhun-28mansions-v1.html`
   - `cnsh-core/longhun-flow-system/longhun-28mansions-v1.html`

🔵 **166.** ` #龍芯⚡️2026-06-21-CORE-CNSH_GATEWAY-v1.0` → **2** 個文件
   - `cnsh-core.backup/gateway/cnsh_gateway.py`
   - `cnsh-core/gateway/cnsh_gateway.py`

🔵 **167.** ` #龍芯⚡️2026-06-21-CNSH-收款码配置-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/收款码配置.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/ai-security-toolkit/收款码配置.md.bak`

🔵 **168.** ` #龍芯⚡️2026-06-21-CNSH-LUCKY-专家治理部署报告-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/Lucky-专家治理部署报告.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/Lucky-专家治理部署报告.md.sig`

🔵 **169.** ` #龍芯⚡️2026-06-21-CNSH-M4-MAX-ARM部署完成总结-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/M4-Max-ARM部署完成总结.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/M4-Max-ARM部署完成总结.md.bak`

🔵 **170.** ` #龍芯⚡️2026-06-21-CNSH-解析不了问题诊断指南-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/💥 解析不了问题诊断指南.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/19bd8da9-1792-8267-8000-093407b99859/💥 解析不了问题诊断指南.md.bak`

🔵 **171.** ` #龍芯⚡️2026-06-21-CNSH-LUCKY的超级标签分类系统-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/Lucky的超级标签分类系统.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/Lucky的超级标签分类系统.md.sig`

🔵 **172.** ` #龍芯⚡️2026-06-21-CNSH-完成汇总-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/🎯 完成汇总.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/19bd8da9-1792-8267-8000-093407b99859/🎯 完成汇总.md.bak`

🔵 **173.** ` #龍芯⚡️2026-06-21-CNSH-CNSH-PUBLIC-PAGES-OVERVIEW-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/cnsh-public-pages-overview.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/cnsh-public-pages-overview.md.bak`

🔵 **174.** ` #龍芯⚡️2026-06-21-CNSH-M4-MAX-ARM部署完整指南-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/M4-Max-ARM部署完整指南.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/M4-Max-ARM部署完整指南.md.bak`

🔵 **175.** ` #龍芯⚡️2026-06-21-CNSH-V2-0升级指南-快速版-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/v2.0升级指南-快速版.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/v2.0升级指南-快速版.md.sig`

🔵 **176.** ` #龍芯⚡️2026-06-21-CNSH-NOTION避坑指南-可发布版本-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/Notion避坑指南-可发布版本.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/Notion避坑指南-可发布版本.md.bak`

🔵 **177.** ` #龍芯⚡️2026-06-21-CNSH-发布使用指南-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/发布使用指南.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/ai-security-toolkit/发布使用指南.md.bak`

🔵 **178.** ` #龍芯⚡️2026-06-21-CNSH-跨设备同步指南-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/跨设备同步指南.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/跨设备同步指南.md.bak`

🔵 **179.** ` #龍芯⚡️2026-06-21-CNSH-HELLO_ENGLISH-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/hello_english.longhun`
   - `_archive/cnsh-history/CNSH_备份_20260211/19bd8da9-1792-8267-8000-093407b99859/hello_english.longhun`

🔵 **180.** ` #龍芯⚡️2026-06-21-CNSH-ZHX-20251212-LUCKY-DIGITAL-HUMAN-DEMO-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-LUCKY-DIGITAL-HUMAN-DEMO.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-LUCKY-DIGITAL-HUMAN-DEMO.md.bak`

🔵 **181.** ` #龍芯⚡️2026-06-21-CNSH-LU-指令收集脚本-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/LU-指令收集脚本.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/LU-指令收集脚本.md.sig`

🔵 **182.** ` #龍芯⚡️2026-06-21-CNSH-签名工具使用说明-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/签名工具使用说明.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/ai-security-toolkit/签名工具使用说明.md.bak`

🔵 **183.** ` #龍芯⚡️2026-06-21-CNSH-LUCKY个人IP锚点-UID9622-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/Lucky个人IP锚点-UID9622.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/Lucky个人IP锚点-UID9622.md.sig`

🔵 **184.** ` #龍芯⚡️2026-06-21-CNSH-UID9622_AUTOMATION_CONFIG-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/uid9622_automation_config.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/uid9622_automation_config.md.sig`

🔵 **185.** ` #龍芯⚡️2026-06-21-CNSH-龍魂P0级-三层交叉监督与镜像人格完整方案-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/龍魂P0级-三层交叉监督与镜像人格完整方案.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/龍魂P0级-三层交叉监督与镜像人格完整方案.md.bak`

🔵 **186.** ` #龍芯⚡️2026-06-21-CNSH-UID9622身份验证指南-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/UID9622身份验证指南.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/UID9622身份验证指南.md.bak`

🔵 **187.** ` #龍芯⚡️2026-06-21-CNSH-LONGHUN-COMPILER-JS-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/longhun-compiler.js.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/19bd8da9-1792-8267-8000-093407b99859/longhun-compiler.js.bak`

🔵 **188.** ` #龍芯⚡️2026-06-21-CNSH-PLATFORM-SETUP-GUIDE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/platform-setup-guide.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/platform-setup-guide.md.bak`

🔵 **189.** ` #龍芯⚡️2026-06-21-CNSH-MANUAL_SETUP_GUIDE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/manual_setup_guide.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/manual_setup_guide.md.bak`

🔵 **190.** ` #龍芯⚡️2026-06-21-CNSH-净土36条-AI统一标准-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/净土36条-AI统一标准.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/净土36条-AI统一标准.md.bak`

🔵 **191.** ` #龍芯⚡️2026-06-21-CNSH-CNSH_PARSER-PY-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/cnsh_parser.py.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/19bd8da9-1792-8267-8000-093407b99859/cnsh_parser.py.bak`

🔵 **192.** ` #龍芯⚡️2026-06-21-CNSH-MCP服务器修复完成报告-最终版-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/MCP服务器修复完成报告-最终版.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/MCP服务器修复完成报告-最终版.md.sig`

🔵 **193.** ` #龍芯⚡️2026-06-21-CNSH-ZHX-20251212-OLLAMA-SYSTEM-SUMMARY-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-OLLAMA-SYSTEM-SUMMARY.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-OLLAMA-SYSTEM-SUMMARY.md.bak`

🔵 **194.** ` #龍芯⚡️2026-06-21-CNSH-OLLAMA-OBSIDIAN本地记忆系统完整指南-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/Ollama+Obsidian本地记忆系统完整指南.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/Ollama+Obsidian本地记忆系统完整指南.md.bak`

🔵 **195.** ` #龍芯⚡️2026-06-21-CNSH-全自动化解放-完成总结-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/全自动化解放-完成总结.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/全自动化解放-完成总结.md.bak`

🔵 **196.** ` #龍芯⚡️2026-06-21-CNSH-LUCKY的文件标签指南-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/Lucky的文件标签指南.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/Lucky的文件标签指南.md.sig`

🔵 **197.** ` #龍芯⚡️2026-06-21-CNSH-README_ORIGINAL-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/README_ORIGINAL.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/README_ORIGINAL.md.sig`

🔵 **198.** ` #龍芯⚡️2026-06-21-CNSH-QUICK-START-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/QUICK-START.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/QUICK-START.md.sig`

🔵 **199.** ` #龍芯⚡️2026-06-21-CNSH-ZHX-20251212-DAILY-REVIEW-SYSTEM-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-DAILY-REVIEW-SYSTEM.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-DAILY-REVIEW-SYSTEM.md.bak`

🔵 **200.** ` #龍芯⚡️2026-06-21-CNSH-PAYMENT_DEMO-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/PAYMENT_DEMO.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/PAYMENT_DEMO.md.sig`

🔵 **201.** ` #龍芯⚡️2026-06-21-CNSH-智能镜像与系统DNA-完整发布版-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/智能镜像与系统DNA-完整发布版.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/ai-security-toolkit/智能镜像与系统DNA-完整发布版.md.bak`

🔵 **202.** ` #龍芯⚡️2026-06-21-CNSH-CNSH_CLEANER-PY-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/cnsh_cleaner.py.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/19bd8da9-1792-8267-8000-093407b99859/cnsh_cleaner.py.bak`

🔵 **203.** ` #龍芯⚡️2026-06-21-CNSH-U盘文件分析报告-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/U盘文件分析报告.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/U盘文件分析报告.md.sig`

🔵 **204.** ` #龍芯⚡️2026-06-21-CNSH-ZHX-20251212-OLLAMA-IMPLEMENTATION-GUIDE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-OLLAMA-IMPLEMENTATION-GUIDE.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-OLLAMA-IMPLEMENTATION-GUIDE.md.bak`

🔵 **205.** ` #龍芯⚡️2026-06-21-CNSH-LUCKY指令执行日志-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/Lucky指令执行日志.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/Lucky指令执行日志.md.bak`

🔵 **206.** ` #龍芯⚡️2026-06-21-CNSH-MCP服务器连接问题诊断与修复指南-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/MCP服务器连接问题诊断与修复指南.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/MCP服务器连接问题诊断与修复指南.md.bak`

🔵 **207.** ` #龍芯⚡️2026-06-21-CNSH-ZHX-20251212-OLLAMA-COMPLETE-GUIDE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-OLLAMA-COMPLETE-GUIDE.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-OLLAMA-COMPLETE-GUIDE.md.bak`

🔵 **208.** ` #龍芯⚡️2026-06-21-CNSH-AI安全治理-实战工具包-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/AI安全治理-实战工具包.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/ai-security-toolkit/AI安全治理-实战工具包.md.bak`

🔵 **209.** ` #龍芯⚡️2026-06-21-CNSH-ZHX-20251212-OLLAMA-MASTER-SYSTEM-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-OLLAMA-MASTER-SYSTEM.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-OLLAMA-MASTER-SYSTEM.md.sig`

🔵 **210.** ` #龍芯⚡️2026-06-21-CNSH-龍魂多语言编译系统-完整交付-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/🎯 龍魂多语言编译系统 - 完整交付.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/19bd8da9-1792-8267-8000-093407b99859/🎯 龍魂多语言编译系统 - 完整交付.md.bak`

🔵 **211.** ` #龍芯⚡️2026-06-21-CNSH-龍魂多语言编译系统完整方案-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/龍魂多语言编译系统完整方案.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/19bd8da9-1792-8267-8000-093407b99859/龍魂多语言编译系统完整方案.md.bak`

🔵 **212.** ` #龍芯⚡️2026-06-21-CNSH-MATE60_HOTSPOT_GUIDE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/mate60_hotspot_guide.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/mate60_hotspot_guide.md.bak`

🔵 **213.** ` #龍芯⚡️2026-06-21-CNSH-N8N连接语雀-安全指南-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/n8n连接语雀-安全指南.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/n8n连接语雀-安全指南.md.bak`

🔵 **214.** ` #龍芯⚡️2026-06-21-CNSH-MCP服务器修复完成报告-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/MCP服务器修复完成报告.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/MCP服务器修复完成报告.md.sig`

🔵 **215.** ` #龍芯⚡️2026-06-21-CNSH-README_PAYMENT-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/README_PAYMENT.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/README_PAYMENT.md.bak`

🔵 **216.** ` #龍芯⚡️2026-06-21-CNSH-M4-MAX-N8N正确方案-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/M4-Max-n8n正确方案.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/M4-Max-n8n正确方案.md.sig`

🔵 **217.** ` #龍芯⚡️2026-06-21-CNSH-ZHX-20251212-EXECUTION-PLAN-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-EXECUTION-PLAN.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-EXECUTION-PLAN.md.bak`

🔵 **218.** ` #龍芯⚡️2026-06-21-CNSH-UID9622核心资产整理-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/UID9622核心资产整理.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/UID9622核心资产整理.md.sig`

🔵 **219.** ` #龍芯⚡️2026-06-21-CNSH-ZHX-20251212-AUTOCLASSIFIER-001-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-AUTOCLASSIFIER-001.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-AUTOCLASSIFIER-001.md.sig`

🔵 **220.** ` #龍芯⚡️2026-06-21-CNSH-ZHX-20251212-OLLAMA-QUICK-START-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-OLLAMA-QUICK-START.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/ZHX-20251212-OLLAMA-QUICK-START.md.sig`

🔵 **221.** ` #龍芯⚡️2026-06-21-CNSH-MVP使用指南-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/MVP使用指南.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/MVP使用指南.md.sig`

🔵 **222.** ` #龍芯⚡️2026-06-21-CNSH-MEMORY-DB系统完成总结-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/Memory-DB系统完成总结.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/Memory-DB系统完成总结.md.bak`

🔵 **223.** ` #龍芯⚡️2026-06-21-CNSH-DESKTOP_整理计划-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/desktop_整理计划.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/desktop_整理计划.md.bak`

🔵 **224.** ` #龍芯⚡️2026-06-21-CNSH-数字身份签名区块-标准版-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/数字身份签名区块-标准版.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/ai-security-toolkit/数字身份签名区块-标准版.md.bak`

🔵 **225.** ` #龍芯⚡️2026-06-21-CNSH-使用指南-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/龍魂永世唯一身份系统/docs/使用指南.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251207144453/使用指南.md.bak`

🔵 **226.** ` #龍芯⚡️2026-06-21-CNSH-FAQ-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/龍魂永世唯一身份系统/docs/FAQ.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/FAQ.md.bak`

🔵 **227.** ` #龍芯⚡️2026-06-21-CNSH-CNSH_AI_STANDARDS-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/CNSH_AI_STANDARDS.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/CNSH_AI_STANDARDS.md.bak`

🔵 **228.** ` #龍芯⚡️2026-06-21-CNSH-CNSH_统一管理系统使用指南-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/CNSH_统一管理系统使用指南.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/CNSH_统一管理系统使用指南.md.bak`

🔵 **229.** ` #龍芯⚡️2026-06-21-CNSH-NOTION-DATABASES-INTEGRATION-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/notion-databases-integration.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/notion-databases-integration.md.bak`

🔵 **230.** ` #龍芯⚡️2026-06-21-CNSH-快速部署指南-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/快速部署指南.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/快速部署指南.md.bak`

🔵 **231.** ` #龍芯⚡️2026-06-21-CNSH-DNA_CODING_SYSTEM-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/DNA_CODING_SYSTEM.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/DNA_CODING_SYSTEM.md.bak`

🔵 **232.** ` #龍芯⚡️2026-06-21-CNSH-CNSH_INITIAL_MISSION-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/CNSH_INITIAL_MISSION.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/CNSH_INITIAL_MISSION.md.bak`

🔵 **233.** ` #龍芯⚡️2026-06-21-CNSH-NOTION_MONITOR_GUIDE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/NOTION_MONITOR_GUIDE.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/NOTION_MONITOR_GUIDE.md.bak`

🔵 **234.** ` #龍芯⚡️2026-06-21-CNSH-CNSH_VISION-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/CNSH_VISION.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/CNSH_VISION.md.bak`

🔵 **235.** ` #龍芯⚡️2026-06-21-CNSH-本地数据库部署指南-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/本地数据库部署指南.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/本地数据库部署指南.md.bak`

🔵 **236.** ` #龍芯⚡️2026-06-21-CNSH-DEPLOYMENT_GUIDE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/DEPLOYMENT_GUIDE.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/DEPLOYMENT_GUIDE.md.bak`

🔵 **237.** ` #龍芯⚡️2026-06-21-CNSH-FINAL_INSTRUCTIONS-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/FINAL_INSTRUCTIONS.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/FINAL_INSTRUCTIONS.md.bak`

🔵 **238.** ` #龍芯⚡️2026-06-21-CNSH-CNSH-CORE-WHITEPAPER-ZH-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/docs/CNSH-Core-Whitepaper-ZH.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/CNSH-Core-Whitepaper-ZH.md.bak`

🔵 **239.** ` #龍芯⚡️2026-06-21-CNSH-NORTH-STAR-B-PROTOCOL-V1-0-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/cnsh-deployment/docs/North-Star-B-Protocol-v1.0.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/docs/North-Star-B-Protocol-v1.0.md.bak`

🔵 **240.** ` #龍芯⚡️2026-06-21-CNSH-README_终极封神版-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/README_终极封神版.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/README_终极封神版.md.sig`

🔵 **241.** ` #龍芯⚡️2026-06-21-CNSH-系统导航-README-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/【系统导航】README.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/【系统导航】README.md.sig`

🔵 **242.** ` #龍芯⚡️2026-06-21-CNSH-杀手锏使用指南-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/杀手锏使用指南.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/杀手锏使用指南.md.sig`

🔵 **243.** ` #龍芯⚡️2026-06-21-CNSH-紧急救援-TROUBLESHOOTING-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/【紧急救援】troubleshooting.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/【紧急救援】troubleshooting.md.bak`

🔵 **244.** ` #龍芯⚡️2026-06-21-CNSH-README_杀手锏版-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/README_杀手锏版.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/README_杀手锏版.md.sig`

🔵 **245.** ` #龍芯⚡️2026-06-21-CNSH-代码模块架构图-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/📋代码模块架构图.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/📋代码模块架构图.md.sig`

🔵 **246.** ` #龍芯⚡️2026-06-21-CNSH-合作方A签署样例-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/案例/合作方A签署样例.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/案例/合作方A签署样例.md.sig`

🔵 **247.** ` #龍芯⚡️2026-06-21-CNSH-个人签署模板-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/📖协议文档/签署模板/个人签署模板.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/📖协议文档/签署模板/个人签署模板.md.bak`

🔵 **248.** ` #龍芯⚡️2026-06-21-CNSH-木兰协议-V1-0-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/📖协议文档/正式版/木兰协议-v1.0.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/📖协议文档/正式版/木兰协议-v1.0.md.sig`

🔵 **249.** ` #龍芯⚡️2026-06-21-CNSH-MULAN-PROTOCOL-V1-0-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/📖协议文档/正式版/Mulan-Protocol-v1.0.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251130195117/木兰协议/📖协议文档/正式版/Mulan-Protocol-v1.0.md.sig`

🔵 **250.** ` #龍芯⚡️2026-06-21-CNSH-QUICK_START-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251207144453/MulanNotion/guides/QUICK_START.md.bak`
   - `_archive/cnsh-history/CNSH-整理版/packages/cnsh-editor/QUICK_START.md.bak`

🔵 **251.** ` #龍芯⚡️2026-06-21-CNSH-04-API参考-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251202054647/04-API参考.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251202054647/04-API参考.md.bak`

🔵 **252.** ` #龍芯⚡️2026-06-21-CNSH-02-技术架构-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251202054647/02-技术架构.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251202054647/02-技术架构.md.bak`

🔵 **253.** ` #龍芯⚡️2026-06-21-CNSH-01-系统概述-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251202054647/01-系统概述.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251202054647/01-系统概述.md.bak`

🔵 **254.** ` #龍芯⚡️2026-06-21-CNSH-03-使用指南-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251202054647/03-使用指南.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/本地备份/历史项目/CodeBuddy/20251202054647/03-使用指南.md.sig`

🔵 **255.** ` #龍芯⚡️2026-06-21-CNSH-TEST-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/sample_notion_export/test.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/sample_notion_export/test.md.sig`

🔵 **256.** ` #龍芯⚡️2026-06-21-CNSH-HEALTHCHECK_20251224_055736-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/health_reports/healthcheck_20251224_055736.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/health_reports/healthcheck_20251224_055736.md.bak`

🔵 **257.** ` #龍芯⚡️2026-06-21-CNSH-CNSH-第一批创建完成报告-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-v1.0-完整实现/CNSH-第一批创建完成报告.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/CNSH-第一批创建完成报告.md.bak`

🔵 **258.** ` #龍芯⚡️2026-06-21-CNSH-TEST-FUNCTION-CALL-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-v1.0-完整实现/test-function-call.cnsh`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/test-function-call.cnsh`

🔵 **259.** ` #龍芯⚡️2026-06-21-CNSH-CNSH编辑器-HTML-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-v1.0-完整实现/CNSH编辑器.html.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/CNSH编辑器.html.bak`

🔵 **260.** ` #龍芯⚡️2026-06-21-CNSH-龍魂终端V3-0-使用指南-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-v1.0-完整实现/龍魂终端v3.0-使用指南.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/龍魂终端v3.0-使用指南.md.bak`

🔵 **261.** ` #龍芯⚡️2026-06-21-CNSH-龍魂终端V3-0-完成报告-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-v1.0-完整实现/龍魂终端v3.0-完成报告.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/龍魂终端v3.0-完成报告.md.bak`

🔵 **262.** ` #龍芯⚡️2026-06-21-CNSH-CNSH-语言配件集成-执行完成报告-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-v1.0-完整实现/CNSH-语言配件集成-执行完成报告.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/CNSH-语言配件集成-执行完成报告.md.bak`

🔵 **263.** ` #龍芯⚡️2026-06-21-CNSH-一键运行-使用说明-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-v1.0-完整实现/一键运行-使用说明.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/一键运行-使用说明.md.bak`

🔵 **264.** ` #龍芯⚡️2026-06-21-CNSH-CNSH完整规范-NOTION版-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-v1.0-完整实现/CNSH完整规范-Notion版.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/CNSH完整规范-Notion版.md.bak`

🔵 **265.** ` #龍芯⚡️2026-06-21-CNSH-CNSH-语言配件集成完成报告-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-v1.0-完整实现/CNSH-语言配件集成完成报告.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/CNSH-语言配件集成完成报告.md.bak`

🔵 **266.** ` #龍芯⚡️2026-06-21-CNSH-龍魂智能终端-V3-0-漂移版-HTML-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-v1.0-完整实现/龍魂智能终端-v3.0-漂移版.html.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/龍魂智能终端-v3.0-漂移版.html.bak`

🔵 **267.** ` #龍芯⚡️2026-06-21-CNSH-CNSH-COMPILER-JS-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-v1.0-完整实现/cnsh-compiler.js.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/cnsh-compiler.js.bak`

🔵 **268.** ` #龍芯⚡️2026-06-21-CNSH-收支分析-扩展包说明-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-v1.0-完整实现/收支分析-扩展包说明.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/收支分析-扩展包说明.md.bak`

🔵 **269.** ` #龍芯⚡️2026-06-21-CNSH-网站搭建-最简指南-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-v1.0-完整实现/网站搭建-最简指南.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/网站搭建-最简指南.md.bak`

🔵 **270.** ` #龍芯⚡️2026-06-21-CNSH-个体户收支分析-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-v1.0-完整实现/个体户收支分析.cnsh`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/个体户收支分析.cnsh`

🔵 **271.** ` #龍芯⚡️2026-06-21-CNSH-龍魂主页-导航中心-HTML-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/CNSH-v1.0-完整实现/龍魂主页-导航中心.html.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/龍魂主页-导航中心.html.bak`

🔵 **272.** ` #龍芯⚡️2026-06-21-CNSH-VALIDATION-REPORT-20260130_155300-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/validation-layer/reports/VALIDATION-REPORT-20260130_155300.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/validation-layer/reports/VALIDATION-REPORT-20260130_155300.md.sig`

🔵 **273.** ` #龍芯⚡️2026-06-21-CNSH-VALIDATION-REPORT-20260130_154834-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/validation-layer/reports/VALIDATION-REPORT-20260130_154834.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/validation-layer/reports/VALIDATION-REPORT-20260130_154834.md.sig`

🔵 **274.** ` #龍芯⚡️2026-06-21-CNSH-MANIFEST-JSON-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/LU-Taiji-Bundle/manifest.json.bak`
   - `_archive/cnsh-history/CNSH-整理版/packages/dragon_soul_extension/manifest.json.bak`

🔵 **275.** ` #龍芯⚡️2026-06-21-CNSH-START-SH-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/LU-Taiji-Bundle/devices/huawei/start.sh.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/LU-Taiji-Bundle/devices/asus/start.sh.bak`

🔵 **276.** ` #龍芯⚡️2026-06-21-CNSH-DNA标签系统-统一规范-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/UID9622-LocalServer/DNA标签系统-统一规范.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/UID9622-LocalServer/DNA标签系统-统一规范.md.sig`

🔵 **277.** ` #龍芯⚡️2026-06-21-CNSH-AUTOFILL_RULES-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/UID9622-LocalServer/UID9622-WorldSystem/AutoFill_Rules.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/UID9622-LocalServer/UID9622-WorldSystem/AutoFill_Rules.md.bak`

🔵 **278.** ` #龍芯⚡️2026-06-21-CNSH-导入报告-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/UID9622-LocalServer/UID9622-WorldSystem/导入报告.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/UID9622-LocalServer/UID9622-WorldSystem/导入报告.md.sig`

🔵 **279.** ` #龍芯⚡️2026-06-21-CNSH-CODE_TEMPLATE-PY-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/templates/code_template.py.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/templates/combat-ready/code_template.py.bak`

🔵 **280.** ` #龍芯⚡️2026-06-21-CNSH-INNOVATION_TEMPLATE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/templates/combat-ready/innovation_template.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/templates/combat-ready/innovation_template.md.bak`

🔵 **281.** ` #龍芯⚡️2026-06-21-CNSH-LATEST-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/manifests/registry.ollama.ai/library/llama3.2/latest`
   - `_archive/cnsh-history/CNSH_备份_20260211/manifests/registry.ollama.ai/firerootlad/ROOT_UID9622/latest`

🔵 **282.** ` #龍芯⚡️2026-06-21-CNSH-插件拆解指南-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/dev-tools/插件拆解指南.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/dev-tools/插件拆解指南.md.sig`

🔵 **283.** ` #龍芯⚡️2026-06-21-CNSH-CODEBUDDY中文对照-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/dev-tools/CodeBuddy中文对照.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/dev-tools/CodeBuddy中文对照.md.sig`

🔵 **284.** ` #龍芯⚡️2026-06-21-CNSH-插件推荐清单-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/dev-tools/插件推荐清单.md.bak`
   - `_archive/cnsh-history/CNSH_备份_20260211/dev-tools/插件推荐清单.md.sig`

🔵 **285.** ` #龍芯⚡️2026-06-21-CNSH-README_CN-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH_备份_20260211/anti-fraud-sentinel/global-reference/README_CN.md.sig`
   - `_archive/cnsh-history/CNSH_备份_20260211/anti-fraud-sentinel/global-reference/README_CN.md.bak`

🔵 **286.** ` #龍芯⚡️2026-06-21-CNSH-LONGHUN_DATA_SOVEREIGNTY_DEFENSE_TOOLKIT_GUIDE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/longhun_data_sovereignty_defense_toolkit_guide.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/longhun_data_sovereignty_defense_toolkit_guide.md.sig`

🔵 **287.** ` #龍芯⚡️2026-06-21-CNSH-NOTION_AUTO_EMAIL_GUIDE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/notion_auto_email_guide.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/notion_auto_email_guide.md.sig`

🔵 **288.** ` #龍芯⚡️2026-06-21-CNSH-PROJECT_SETUP-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/PROJECT_SETUP.md.sig`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/PROJECT_SETUP.md.bak`

🔵 **289.** ` #龍芯⚡️2026-06-21-CNSH-LU主控指令库-30C07171724280B6B6A2FC52C23E8B68-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/主控指令/LU主控指令库 30c07171724280b6b6a2fc52c23e8b68.csv`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/lu指令库/LU主控指令库 30c07171724280b6b6a2fc52c23e8b68.csv`

🔵 **290.** ` #龍芯⚡️2026-06-21-CNSH-CNSH_COMPLETE_SPEC_V2-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/龍魂系统核心/cnsh_complete_spec_v2.cnsh`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/龍魂系统核心/files/cnsh_complete_spec_v2.cnsh`

🔵 **291.** ` #龍芯⚡️2026-06-21-CNSH-CNSH_VISUAL_RENDER_V1-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/龍魂系统核心/cnsh_visual_render_v1.cnsh`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/龍魂系统核心/files/cnsh_visual_render_v1.cnsh`

🔵 **292.** ` #龍芯⚡️2026-06-21-CNSH-TROUBLESHOOTING-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/stylegan3-main 2/docs/troubleshooting.md.sig`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/stylegan3-main 2/docs/troubleshooting.md.bak`

🔵 **293.** ` #龍芯⚡️2026-06-21-CNSH-CONFIGS-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/stylegan3-main 2/docs/configs.md.bak`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/stylegan3-main 2/docs/configs.md.sig`

🔵 **294.** ` #龍芯⚡️2026-06-21-CNSH-CLAUDE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/files/CLAUDE.md.sig`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/files/CLAUDE.md.bak`

🔵 **295.** ` #龍芯⚡️2026-06-21-CNSH-CLAUDE_CODE_ANCHORING_ARCHITECTURE-MD-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/files/claude_code_anchoring_architecture.md.sig`
   - `_archive/cnsh-history/CNSH-v1.0-完整实现/files/claude_code_anchoring_architecture.md.bak`

🔵 **296.** ` #龍芯⚡️2026-06-21-SCRIPT-INSTALL-SH-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-整理版/scripts/install.sh.bak`
   - `_archive/cnsh-history/CNSH-整理版/packages/cnsh-core/scripts/install.sh.bak`

🔵 **297.** ` #龍芯⚡️2026-06-21-CORE-OLLAMA-JS-v1.0` → **2** 個文件
   - `_archive/cnsh-history/CNSH-整理版/packages/cnsh-core/src/routes/ollama.js.bak`
   - `_archive/cnsh-history/CNSH-整理版/packages/cnsh-core/src/services/ollama.js.bak`

🔵 **298.** `#龍芯⚡️2026-06-03-PERSONA-ROUTER-FILE1-v1.0` → **2** 個文件
   - `cnsh-core/router/persona_router.py`
   - `cnsh-core/router/PERSONA_ROUTER_README.md`

🔵 **299.** `#龍芯⚡️2026-06-18-LONGHUN-CHINESE-EDITOR-FILE1-v1.0` → **2** 個文件
   - `editor/README.md`
   - `editor/龍碼編輯器.py`

---

## 💡 修復建議

- 🔴 高優先: 存在299個重複DNA，違反「一文件一DNA」原則，需拆分
- 🟡 中優先: 3332個文件DNA格式無效，需修正格式為 #龍芯⚡️YYYY-MM-DD-MODULE-vX.X
- 🟡 Python腳本: 對齐率40.4%，需補充1034個文件

## 📊 對齐進度

```
DNA 對齐進度 [███████████████░░░░░] 78.8%
```

---

**DNA**: #龍芯⚡️2026-06-21-DNA-ALIGNMENT-AUDIT-v1.0
**簽署**: DNA對齐審計系統·不免責

🐉 龍魂系統·DNA追溯·完整性驗證