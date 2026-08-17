---
dna: '#龍芯⚡️丙午·丙申·辛酉·午时·䷦蹇-CLIPBOARD-VAULT-SAVE-V1.0-P1-5d6226b4'
source: clipboard
topic: 命令/CLI
tags:
- Python
- Notion
- 命令/CLI
timestamp: '2026-08-15T12:11:43+08:00'
content_hash: 4dc545f90438e891eb3f0ba68586b31dcff9daaf3f9ad121397ebd35b9b1385b
parent_dna: []
vault_version: v1.0
---

# 剪贴内容

全部体检通过，系统状态正常。

💡 常用入口
   总开关体检: python3 08_BIN/lh_notion_command_registry.py run check --all
   分布式执行: python3 08_BIN/lh_notion_command_registry.py run exec --category A --yes
   Notion 注册表: https://app.notion.com/p/3ba7125a9c9f8123a5f0df380660a176
════════════════════════════════════════════════════════

龍 ~/longhun-system ☯ 🟢 %# 1. 检查环境 
python3 -c "import mlx; import mlx_lm; print('✅ MLX 环境就绪')"

# 2. 下载 Qwen2.5-1.5B
pip install huggingface-hub
huggingface-cli download Qwen/Qwen2.5-1.5B --local-dir ./models/qwen-1.5b

# 3. 启动训练（用你已有的 45555 条数据）
python3 08_BIN/lh_lora_trainer_v419.py train --model qwen-1.5b --data ./data/train/

# 4. 导出 GGUF
python3 08_BIN/lh_export_gguf.py --model ./models/qwen-1.5b --output ./models/longhun-1.5b.gguf

# 5. 同步到鲲鹏
scp ./models/longhun-1.5b.gguf root@119.13.90.27:/opt/ollama/models/

# 6. 鲲鹏上运行
ollama run longhun-1.5b
✅ MLX 环境就绪
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try brew install
    xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a Python library that isn't in Homebrew,
    use a virtual environment:
    
    python3 -m venv path/to/venv
    source path/to/venv/bin/activate
    python3 -m pip install xyz
    
    If you wish to install a Python application that isn't in Homebrew,
    it may be easiest to use 'pipx install xyz', which will manage a
    virtual environment for you. You can install pipx with
    
    brew install pipx
    
    You may restore the old behavior of pip by passing
    the '--break-system-packages' flag to pip, or by adding
    'break-system-packages = true' to your pip.conf file. The latter
    will permanently disable this error.
    
    If you disable this error, we STRONGLY recommend that you additionally
    pass the '--user' flag to pip, or set 'user = true' in your pip.conf
    file. Failure to do this can result in a broken Homebrew installation.
    
    Read more about this behavior here: <https://peps.python.org/pep-0668/>

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.

[进程已完成]

---

*归档于 2026-08-15T12:11:43+08:00 · DNA `#龍芯⚡️丙午·丙申·辛酉·午时·䷦蹇-CLIPBOARD-VAULT-SAVE-V1.0-P1-5d6226b4`*
