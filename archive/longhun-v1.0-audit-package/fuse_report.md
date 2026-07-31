# 合并报告 (fuse_report)

### fuse_export.log
```
[飞书] 未配置 FEISHU_WEBHOOK_URL，跳过推送
🔍 检查依赖...
   ✅ MLX 0.32.0 | Metal: True
   ✅ mlx_lm
   ✅ transformers 4.49.0
   ✅ 所有依赖就绪

🔗 合并 LoRA adapter...
Loading pretrained model
   ✅ 合并完成 → /Users/zuimeidedeyihan/longhun-system/models/longhun-v1.0/lora_output/merged
   下一步: python3 bin/lh_lora_trainer.py export
Traceback (most recent call last):
  File "/tmp/convert_hf_to_gguf.py", line 18, in <module>
    from conversion import (
ModuleNotFoundError: No module named 'conversion'
🔍 检查依赖...
   ✅ MLX 0.32.0 | Metal: True
   ✅ mlx_lm
   ✅ transformers 4.49.0
   ✅ 所有依赖就绪

📦 导出 GGUF...
   HF→GGUF (f16): convert_hf_to_gguf.py
Traceback (most recent call last):
  File "/Users/zuimeidedeyihan/longhun-system/bin/lh_lora_trainer.py", line 637, in <module>
    commands[sys.argv[1]]()
  File "/Users/zuimeidedeyihan/longhun-system/bin/lh_lora_trainer.py", line 559, in export_gguf
    subprocess.run(
  File "/opt/homebrew/Cellar/python@3.12/3.12.13/Frameworks/Python.framework/Versions/3.12/lib/python3.12/subprocess.py", line 571, in run
    raise CalledProcessError(retcode, process.args,
subprocess.CalledProcessError: Command '['/opt/homebrew/opt/python@3.12/bin/python3.12', '/tmp/convert_hf_to_gguf.py', '/Users/zuimeidedeyihan/longhun-system/models/longhun-v1.0/lora_output/merged', '--outfile', '/Users/zuimeidedeyihan/longhun-system/models/longhun-v1.0/lora_output/gguf/ggml-model-f16.gguf']' returned non-zero exit status 1.
EXITCODE=1

```