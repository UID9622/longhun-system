# 训练日志 (TRAIN_LOG)

> 生成时间: 2026-07-15 23:48:56

## 样本数

- 有效: 5406
- 原始段落: 8895
- 训练: 4892
- 验证: 544

## 超参

- iters: 10782
- model: "Qwen/Qwen2.5-1.5B-Instruct"
- num_layers: 8
- lora_parameters: 
- rank: 16
- batch_size: 2
- learning_rate: 0.0002
- save_every: 500

## Loss 曲线 (496 点)

```
step,loss
0,2.885
1,5.105
2,8.208
3,13.033
4,10.878
5,10.932
6,10.78
7,10.924
8,10.322
9,9.831
10,9.9
11,9.316
12,9.83
13,9.487
14,9.214
15,9.313
16,8.804
17,8.981
18,8.739
19,8.77
20,9.09
21,8.614
22,8.81
23,9.125
24,8.612
25,8.662
26,8.768
27,8.66
28,8.975
29,8.449
30,8.912
31,8.039
32,8.584
33,7.801
34,8.359
35,8.444
36,8.354
37,8.472
38,8.83
39,8.492
40,8.581
41,8.149
42,8.31
43,8.277
44,8.597
45,8.215
46,8.922
47,8.752
48,7.834
49,8.045
50,8.196
51,8.239
52,8.672
53,8.538
54,7.682
55,8.161
56,8.146
57,8.345
58,8.078
59,8.507
60,8.21
61,8.457
62,7.663
63,7.823
64,8.086
65,8.459
66,8.014
67,7.901
68,7.627
69,7.405
70,7.839
71,8.361
72,7.836
73,7.967
74,7.867
75,8.1
76,7.718
77,8.052
78,7.877
79,7.762
80,7.952
81,7.857
82,8.065
83,7.964
84,7.843
85,7.643
86,7.578
87,7.969
88,8.173
89,7.857
90,7.599
91,7.597
92,7.684
93,7.732
94,8.159
95,8.027
96,8.107
97,7.342
98,7.517
99,7.528
100,8.401
101,8.299
102,7.896
103,7.563
104,7.35
105,7.396
106,7.512
107,7.988
108,7.509
109,7.77
110,7.64
111,7.217
112,7.473
113,7.682
114,7.527
115,7.482
116,7.247
117,7.512
118,7.451
119,7.879
120,7.844
121,7.61
122,7.415
123,7.495
124,7.392
125,7.849
126,7.707
127,7.042
128,7.569
129,7.487
130,7.014
131,7.418
132,7.452
133,7.456
134,7.09
135,7.325
136,7.22
137,7.725
138,7.306
139,7.685
140,7.762
141,7.039
142,7.147
143,7.803
144,7.202
145,7.35
146,7.258
147,7.585
148,7.185
149,7.849
150,6.873
151,7.495
152,7.615
153,6.894
154,7.457
155,7.54
156,7.333
157,7.033
158,7.264
159,7.245
160,7.108
161,7.122
162,7.061
163,7.6
164,7.072
165,7.637
166,7.257
167,7.342
168,7.334
169,7.091
170,7.485
171,7.224
172,6.714
173,7.33
174,6.823
175,6.885
176,7.117
177,7.255
178,7.159
179,7.537
180,7.017
181,7.123
182,7.022
183,7.267
184,7.572
185,7.58
186,7.38
187,7.133
188,7.421
189,7.132
190,7.31
191,7.218
192,7.258
193,7.196
194,6.794
195,7.501
196,7.305
197,7.189
198,7.281
199,7.004
... (共 496 点, 详见原始日志)
```

## 原始日志块

### train.log
```
==================================================
🐉 龍魂 longhun LoRA 微调训练
   底模: Qwen2.5-1.5B-Instruct
   镜像: https://hf-mirror.com
==================================================

📦 Step 0/4: 检查依赖...
MLX OK

📝 Step 1/4: 准备训练数据...
None of PyTorch, TensorFlow >= 2.0, or Flax have been found. Models won't be available and only tokenizers, configuration and file/data utilities can be used.
🔍 检查依赖...
   ✅ MLX 0.32.0 | Metal: True
   ✅ mlx_lm
   ✅ transformers 4.49.0
   ✅ 所有依赖就绪

📝 准备训练数据...
   原始段落: 8895 → 有效样本: 5406
   ✅ train.jsonl: 4892 样本 → /Users/zuimeidedeyihan/longhun-system/models/longhun-v1.0/lora_output/data/train.jsonl
   ✅ valid.jsonl: 544 样本 → /Users/zuimeidedeyihan/longhun-system/models/longhun-v1.0/lora_output/data/valid.jsonl

📊 数据统计:
   训练集: 4892 样本
   验证集: 544 样本
   总字符: 861,625

✅ 数据准备完成！运行: python3 bin/lh_lora_trainer.py train

🚀 Step 2/4: LoRA 微调...
None of PyTorch, TensorFlow >= 2.0, or Flax have been found. Models won't be available and only tokenizers, configuration and file/data utilities can be used.
🔍 检查依赖...
   ✅ MLX 0.32.0 | Metal: True
   ✅ mlx_lm
   ✅ transformers 4.49.0
   ✅ 所有依赖就绪

🚀 开始 LoRA 微调...
   样本数: 4892, 7338 iters (=3 epochs × 2446 iters/epoch)
   底模: Qwen/Qwen2.5-1.5B-Instruct
   LoRA rank=16, alpha=32
   设备: M4 Max GPU (Metal)

Loading pretrained model

Fetching 7 files:   0%|          | 0/7 [00:00<?, ?it/s]
Fetching 7 files:  57%|█████▋    | 4/7 [01:06<00:49, 16.64s/it]
Fetching 7 files: 100%|██████████| 7/7 [01:06<00:00,  9.51s/it]
Loading datasets
Training
Trainable parameters: 0.342% (5.276M/1543.714M)
Starting training..., iters: 7338

Calculating loss...:   0%|          | 0/25 [00:00<?, ?it/s]
Calculating loss...:   4%|▍         | 1/25 [00:01<00:32,  1.37s/it]
Calculating loss...:  12%|█▏        | 3/25 [00:02<00:13,  1.57it/s]
Calculating loss...:  16%|█▌        | 4/25 [00:02<00:09,  2.18it/s]
Calculating loss...:  20%|██        | 5/25 [00:02<00:06,  2.91it/s]
Calculating loss...:  24%|██▍       | 6/25 [00:03<00:08,  2.19it/s]
Calculating loss...:  32%|███▏      | 8/25 [00:03<00:04,  3.49it/s]
Calculating loss...:  36%|███▌      | 9/25 [00:03<00:05,  2.86it/s]
Calculating loss...:  40%|████      | 10/25 [00:03<00:04,  3.24it/s]
Calculating loss...:  44%|████▍     | 11/25 [00:04<00:03,  3.71it/s]
Calculating loss...:  48%|████▊     | 12/25 [00:04<00:04,  2.62it/s]
Calculating loss...:  52%|█████▏    | 13/25 [00:05<00:05,  2.32it/s]
Calculating loss...:  60%|██████    | 15/25 [00:05<00:02,  3.62it/s]
Calculating loss...:  68%|██████▊   | 17/25 [00:05<00:01,  4.90it/s]
Calculating loss...:  76%|███████▌  | 19/25 [00:05<00:00,  6.44it/s]
Calculating loss...:  84%|████████▍ | 21/25 [00:06<00:00,  7.57it/s]
Calculating loss...:  92%|█████████▏| 23/25 [00:06<00:00,  8.28it/s]
Calculating loss...: 100%|██████████| 25/25 [00:06<00:00,  7.77it/s]
Calculating loss...: 100%|██████████| 25/25 [00:06<00:00,  3.83it/s]
Iter 1: Val loss 2.885, Val took 6.535s
Iter 10: Train loss 5.105, Learning Rate 2.000e-04, It/sec 2.871, Tokens/sec 276.169, Trained Tokens 962, Peak mem 4.527 GB
Iter 20: Train loss 8.208, Learning Rate 2.000e-04, It/sec 5.697, Tokens/sec 676.277, Trained Tokens 2149, Peak mem 4.527 GB
Iter 30: Train loss 13.033, Learning Rate 2.000e-04, It/sec 4.818, Tokens/sec 591.229, Trained Tokens 3376, Peak mem 4.527 GB
Iter 40: Train loss 10.878, Learning Rate 2.000e-04, It/sec 3.479, Tokens/sec 669.725, Trained Tokens 5301, Peak mem 5.113 GB

Calculating loss...:   0%|          | 0/25 [00:00<?, ?it/s]
Calculating loss...:   4%|▍         | 1/25 [00:00<00:05,  4.29it/s]
Calculating loss...:   8%|▊         | 2/25 [00:01<00:18,  1.26it/s]
Calculating loss...:  12%|█▏        | 3/25 [00:02<00:16,  1.30it/s]
Calculating loss...:  16%|█▌        | 4/25 [00:02<00:10,  1.95it/s]
Calculating loss...:  20%|██        | 5/25 [00:02<00:11,  1.78it/s]
Calculating loss...:  24%|██▍       | 6/25 [00:03<00:08,  2.21it/s]
Calculating loss...:  32%|███▏      | 8/25 [00:03<00:04,  3.48it/s]
Calculating loss..
```

### train_run.log
```
🔍 检查依赖...
   ✅ MLX 0.32.0 | Metal: True
   ✅ mlx_lm
   ✅ transformers 4.49.0
   ✅ 所有依赖就绪

🚀 开始 LoRA 微调...
   样本数: 324, 810 iters (=5 epochs × 162 iters/epoch)
   底模: /Users/zuimeidedeyihan/longhun-system/models/longhun-v1.0/base_model
   LoRA rank=8, alpha=32
   设备: M4 Max GPU (Metal)

Loading pretrained model
Loading datasets
Training
Trainable parameters: 0.171% (2.638M/1543.714M)
Starting training..., iters: 810

Calculating loss...:   0%|          | 0/18 [00:00<?, ?it/s]huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks...
To disable this warning, you can either:
	- Avoid using `tokenizers` before the fork if possible
	- Explicitly set the environment variable TOKENIZERS_PARALLELISM=(true | false)

Calculating loss...:   6%|▌         | 1/18 [00:00<00:02,  6.36it/s]
Calculating loss...:  11%|█         | 2/18 [00:00<00:02,  6.96it/s]
Calculating loss...:  17%|█▋        | 3/18 [00:00<00:02,  7.19it/s]
Calculating loss...:  22%|██▏       | 4/18 [00:00<00:01,  7.52it/s]
Calculating loss...:  28%|██▊       | 5/18 [00:00<00:01,  7.65it/s]
Calculating loss...:  33%|███▎      | 6/18 [00:00<00:01,  7.55it/s]
Calculating loss...:  39%|███▉      | 7/18 [00:00<00:01,  7.68it/s]
Calculating loss...:  44%|████▍     | 8/18 [00:01<00:01,  7.79it/s]
Calculating loss...:  50%|█████     | 9/18 [00:01<00:01,  7.67it/s]
Calculating loss...:  56%|█████▌    | 10/18 [00:01<00:01,  7.81it/s]
Calculating loss...:  61%|██████    | 11/18 [00:01<00:00,  7.88it/s]
Calculating loss...:  67%|██████▋   | 12/18 [00:01<00:00,  8.27it/s]
Calculating loss...:  72%|███████▏  | 13/18 [00:01<00:00,  8.57it/s]
Calculating loss...:  78%|███████▊  | 14/18 [00:01<00:00,  8.20it/s]
Calculating loss...:  83%|████████▎ | 15/18 [00:01<00:00,  8.15it/s]
Calculating loss...:  89%|████████▉ | 16/18 [00:02<00:00,  8.47it/s]
Calculating loss...:  94%|█████████▍| 17/18 [00:02<00:00,  8.33it/s]
Calculating loss...: 100%|██████████| 18/18 [00:02<00:00,  8.23it/s]
Calculating loss...: 100%|██████████| 18/18 [00:02<00:00,  7.92it/s]
Iter 1: Val loss 3.506, Val took 2.284s
Iter 10: Train loss 2.628, Learning Rate 1.500e-04, It/sec 4.130, Tokens/sec 397.320, Trained Tokens 962, Peak mem 4.103 GB
Iter 20: Train loss 2.756, Learning Rate 1.500e-04, It/sec 4.032, Tokens/sec 429.787, Trained Tokens 2028, Peak mem 4.266 GB
Iter 30: Train loss 1.848, Learning Rate 1.500e-04, It/sec 4.290, Tokens/sec 377.083, Trained Tokens 2907, Peak mem 4.266 GB
Iter 40: Train loss 1.877, Learning Rate 1.500e-04, It/sec 4.233, Tokens/sec 381.851, Trained Tokens 3809, Peak mem 4.266 GB

Calculating loss...:   0%|          | 0/18 [00:00<?, ?it/s]
Calculating loss...:   6%|▌         | 1/18 [00:00<00:01,  9.16it/s]
Calculating loss...:  11%|█         | 2/18 [00:00<00:01,  8.06it/s]
Calculating loss...:  17%|█▋        | 3/18 [00:00<00:01,  8.09it/s]
Calculating loss...:  22%|██▏       | 4/18 [00:00<00:01,  7.80it/s]
Calculating loss...:  28%|██▊       | 5/18 [00:00<00:01,  7.92it/s]
Calculating loss...:  33%|███▎      | 6/18 [00:00<00:01,  7.95it/s]
Calculating loss...:  39%|███▉      | 7/18 [00:00<00:01,  7.72it/s]
Calculating loss...:  44%|████▍     | 8/18 [00:01<00:01,  7.62it/s]
Calculating loss...:  50%|█████     | 9/18 [00:01<00:01,  7.77it/s]
Calculating loss...:  56%|█████▌    | 10/18 [00:01<00:01,  7.65it/s]
Calculating loss...:  61%|██████    | 11/18 [00:01<00:00,  8.09it/s]
Calculating loss...:  67%|██████▋   | 12/18 [00:01<00:00,  8.41it/s]
Calculating loss...:  72%|███████▏  | 13/18 [00:01<00:00,  8.30it/s]
Calculating loss...:  78%|███████▊  | 14/18 [00:01<00:00,  8.21it/s]
Calculating loss...:  83%|████████▎ | 15/18 [00:01<00:00,  8.15it/s]
Calculating loss...:  89%|████████▉ | 16/18 [00:01<00:00,  8.11it/s]
Calculating loss...:  94%|█████████▍| 17/18 [00:02<00:00,  8.09it/s]
Calculating loss...: 100%|██████████| 18/18 [00:02<00:00,  7.83it/s]
Calculating loss...: 100%|██████████| 18/18 [00:02<00:00,  7.
```

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