# n8n+DeepSeek+Notion 自动化论文解读与知识入库流程

> Notion URL: https://app.notion.com/p/n8n-DeepSeek-Notion-800dcd1f2c954d37bd54c8de9c44aa85
> Created: 2025-10-12T02:48:00.000Z
> Last edited: 2026-07-01T08:54:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
### 摘要
建立“每日自动抓取论文 → 去重 → 分段AI解读 → 结构化入库Notion → 生成适配公众号HTML草稿”的自动化学习管道，缓解信息过载，沉淀可检索与可复用资产，并提升对外输出效率。
---
### 来源与范围
- 参考材料：微信长文（n8n × DeepSeek × Notion 自动化实践）
- 适用范围：前沿论文类信息源（示例关键词：AI、education、K-12，可按需更换为 NLP、LSTM 等）
- 输出对象：
---
### 核心流程（System Overview）
1) 定时触发：每日/每周定时抓取论文列表（如 Hugging Face）
2) 去重校验：URL 唯一性检查，避免重复处理
3) 内容聚合：拉取 PDF 正文，必要时分段合并
4) 多层AI解读：
5) 结果入库：通过 Notion API 写入数据库，标签化、可检索
6) 对外生成：按公众号排版模版生成 HTML 草稿，一键粘贴发布
7) 异常处理：错误重试、分支回退、失败记录
---
### 数据字段映射（与本库对齐）
建议最低映射：
- 规则/变化点名称（必填）：n8n+DeepSeek+Notion 自动化论文解读与知识入库流程
- Type：规则
- Risk：绿
- Status：候选（评审通过后改为“已审/已发布”）
- Summary：日更抓取→去重→分段解读→入库→生成HTML草稿
- Version：v0.1（随节点与提示词更新迭代）
- Source：原始文章或入口URL
- Evidence：处理过的样例链接、关键截图位置（可后续补全）
- Change Impact：建立自动化学习管道，沉淀结构化知识资产
- Owner：负责人标识（当前：🚀 Lucky｜UID9622）
---
### n8n 节点建议
- 触发器：Cron（每日固定时段）
- 获取列表：HTTP Request（分页与关键词）
- 循环处理：Split In Batches 或 Item Lists
- 去重：Function 检查 URL 是否已存在于 Notion（或 Redis/SQLite 快取）
- PDF提取：HTTP + PDF 解析（必要时 Code 节点分段）
- 多层AI：多个独立 LLM 节点，控制温度和上下文长度（分段汇总）
- 合并：Merge 将多维解读整合为结构化对象
- Notion写入：Notion → Create/Update Page（字段映射同上）
- 公众号草稿：Code 节点将结果套入 HTML 模版
- 失败重试：Error Workflow 或 Try/Catch 分支 + 重试计数
---
### Prompt 要点（示例）
- System：你是论文解读助手，输出需结构化且可复用，限制赘述
- User：
---
### 标准操作（SOP）
1) 首次部署：
2) 运行验证：
3) 上线巡检：
4) 发布与复盘：
---
### 风险与边界
- 上下文长度限制：采用“分段解读→分层汇总”的策略
- 去重与幂等：以论文 URL 为主键，必要时校验标题+摘要指纹
- HTML 转换：换行与转义统一在 Code 模块处理，保留 Markdown 备份
- 法律与合规：遵守抓取站点的使用条款，注明来源与署名
---
### 后续改进（Backlog）
- 多模态支持：图表与公式识别，参考文献解析
- 动态路由：按论文类型选择不同处理链路（理论/实验/综述）
- 全量写回：将生成的 HTML 草稿同时保存回 Notion（字段或附件）
- 指标看板：新增失败率、去重命中率、发布时间等运营指标
---
### 发布与审计流
- 三色评估：🟢 可执行｜🟡 条件可执行｜🔴 暂缓
- 审计记录：在“Evidence”填入样例处理链接与截图标记
- 一键回滚：通过版本记录保留所有改动，必要时封存到“墓碑区”
---
### 公众号发布模板 v0.1（可直接复制到公众号HTML编辑器）
```html
<!-- 标题 -->
<h1>每天一篇 AI 论文深度解读：自动抓取 × 分段分析 × 一键成稿</h1>

<!-- 作者/时间（可选） -->
<p><em>作者：UID9622｜自动化学习管道 · 更新：<span id="today">2025-10-12</span></em></p>
<hr>

<!-- 导语 -->
<p>信息过载时代，如何稳定、可复用地把“前沿论文”转为“结构化知识”和“可发布内容”？本文分享我们基于 n8n × DeepSeek × Notion 的自动化方案：每天定时抓取、AI 多层解读、入库沉淀，并一键生成公众号草稿。</p>

<!-- 核心亮点 -->
<h2>为什么值得做</h2>
<ul>
  <li><strong>日更自动化：</strong>定时拉取最新论文，减少人工源头搜集。</li>
  <li><strong>深度、而非浅摘：</strong>多维提示词驱动，输出技术要点与应用价值。</li>
  <li><strong>知识可复用：</strong>Notion 结构化入库，标签与检索友好。</li>
  <li><strong>一键发稿：</strong>生成适配公众号的 HTML 模板，减少排版时间。</li>
</ul>

<!-- 工作原理 -->
<h2>系统架构与流程</h2>
<ol>
  <li><strong>定时触发：</strong>每日（或每周）按关键词抓取论文列表。</li>
  <li><strong>去重校验：</strong>以论文 URL 为主键，避免重复处理。</li>
  <li><strong>内容聚合：</strong>拉取 PDF 正文，必要时分段合并。</li>
  <li><strong>多层 AI 解读：</strong>技术要点、场景价值、可执行建议、风险限制。</li>
  <li><strong>结构化入库：</strong>写入 Notion 数据库，形成可检索知识资产。</li>
  <li><strong>生成成稿：</strong>按模板拼装为公众号可发布的 HTML。</li>
</ol>

<!-- 今日示例位（发布前替换为当日内容） -->
<h2>今日解读（示例占位）</h2>
<p><em>标题：</em>《Paper Title Here》</p>
<p><em>来源：</em><a href="https://example.com">https://example.com</a></p>

<h3>1) 技术要点</h3>
<ul>
  <li>要点1：……</li>
  <li>要点2：……</li>
  <li>要点3：……</li>
</ul>

<h3>2) 场景价值（面向目标读者）</h3>
<ul>
  <li>K-12 教育：……</li>
  <li>高校/科研：……</li>
  <li>产业落地：……</li>
</ul>

<h3>3) 可执行建议</h3>
<ol>
  <li>从数据与场景入手，先做一个最小可行验证（MVP）。</li>
  <li>采用分段解读 + 分层汇总，避免上下文过长导致失真。</li>
  <li>将字段写入知识库，统一标签体系，支持后续检索与对比。</li>
</ol>

<h3>4) 风险与限制</h3>
<ul>
  <li>上下文长度限制：需采用分段策略与多阶段汇总。</li>
  <li>来源合规与引用：遵守站点条款，保留署名与链接。</li>
  <li>模型幻觉：保留原文对照与证据位，支持人工抽检。</li>
</ul>

<!-- 操作指南 -->
<h2>如何开始（面向同类需求）</h2>
<ol>
  <li>在 n8n 配置定时触发 + HTTP 抓取节点，按需设置关键词。</li>
  <li>引入 LLM 节点（DeepSeek 等）并设置多段提示词。</li>
  <li>用 Notion API 写入数据库字段（标题、摘要、标签、证据等）。</li>
  <li>在代码节点将分析结果套进本 HTML 模板。</li>
</ol>

<!-- 结尾 CTA -->
<hr>
<p>如果你也想把“每天阅读”升级为“可复用的知识资产”，欢迎留言交流。持续优化提示词与字段字典，让自动化成为你的第二大脑。</p>

<script>
// 可选：自动填充当天日期
const el = document.getElementById('today');
if (el) el.textContent = new Date().toISOString().slice(0,10);
</script>
```
# Last login: Thu Oct 23 12:57:14 on console
You have new mail.
🎆 欢迎来到 UID9622 防守型终端环境
✨ 当前时间: 2025-10-23 13:28:50
🛡️ 版本: v2.0 (防守型 - 智能保护)
🚀 常用命令: u9622 | go-home | test-env | uid9622-status
🔧 配置管理: uid9622-update-config | backup-config
📚 帮助: alias | 查看所有可用命令
/Users/zhinengdaohang/.zshrc:source:180: no such file or directory: /Users/zhinengdaohang/.zshrcpbpaste
🔧 正在识别语音：
Traceback (most recent call last):
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/urllib/request.py", line 1319, in do_open
h.request(req.get_method(), req.selector, req.data, headers,
~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
encode_chunked=req.has_header('Transfer-encoding'))
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/http/client.py", line 1338, in request
self._send_request(method, url, body, headers, encode_chunked)
~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/http/client.py", line 1384, in _send_request
self.endheaders(body, encode_chunked=encode_chunked)
~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/http/client.py", line 1333, in endheaders
self._send_output(message_body, encode_chunked=encode_chunked)
~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/http/client.py", line 1093, in _send_output
self.send(msg)
~~~~~~~~~^^^^^
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/http/client.py", line 1037, in send
self.connect()
~~~~~~~~~~~~^^
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/http/client.py", line 1479, in connect
self.sock = self._context.wrap_socket(self.sock,
~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
server_hostname=server_hostname)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/ssl.py", line 455, in wrap_socket
return self.sslsocket_class._create(
~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
sock=sock,
^^^^^^^^^^
...<5 lines>...
session=session
^^^^^^^^^^^^^^^
)
^
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/ssl.py", line 1076, in _create
self.do_handshake()
~~~~~~~~~~~~~~~~~^^
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/ssl.py", line 1372, in do_handshake
self._sslobj.do_handshake()
~~~~~~~~~~~~~~~~~~~~~~~~~^^
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1032)
During handling of the above exception, another exception occurred:
Traceback (most recent call last):
File "/Library/Frameworks/Python.framework/Versions/3.13/bin/whisper", line 7, in <module>
sys.exit(cli())
~~~^^
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/whisper/transcribe.py", line 595, in cli
model = load_model(model_name, device=device, download_root=model_dir)
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/whisper/init.py", line 137, in load_model
checkpoint_file = _download(_MODELS[name], download_root, in_memory)
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/whisper/init.py", line 73, in _download
with urllib.request.urlopen(url) as source, open(download_target, "wb") as output:
~~~~~~~~~~~~~~~~~~~~~~^^^^^
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/urllib/request.py", line 189, in urlopen
return opener.open(url, data, timeout)
~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/urllib/request.py", line 489, in open
response = self._open(req, data)
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/urllib/request.py", line 506, in _open
result = self._call_chain(self.handle_open, protocol, protocol +
'_open', req)
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/urllib/request.py", line 466, in _call_chain
result = func(*args)
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/urllib/request.py", line 1367, in https_open
return self.do_open(http.client.HTTPSConnection, req,
~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
context=self._context)
^^^^^^^^^^^^^^^^^^^^^^
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/urllib/request.py", line 1322, in do_open
raise URLError(err)
urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1032)>
mv: rename ./.txt to .txt: No such file or directory
✅ 转录完成：.txt
/Users/zhinengdaohang/.zshrc:194: command not found: ❗
/Users/zhinengdaohang/.zshrc:196: no matches found: [进程已完成]
❯ whisper --help
usage: whisper [-h] [--model MODEL] [--model_dir MODEL_DIR] [--device DEVICE]
[--output_dir OUTPUT_DIR]
[--output_format {txt,vtt,srt,tsv,json,all}]
[--verbose VERBOSE] [--task {transcribe,translate}]
[--language {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,yue,zh,Afrikaans,Albanian,Amharic,Arabic,Armenian,Assamese,Azerbaijani,Bashkir,Basque,Belarusian,Bengali,Bosnian,Breton,Bulgarian,Burmese,Cantonese,Castilian,Catalan,Chinese,Croatian,Czech,Danish,Dutch,English,Estonian,Faroese,Finnish,Flemish,French,Galician,Georgian,German,Greek,Gujarati,Haitian,Haitian Creole,Hausa,Hawaiian,Hebrew,Hindi,Hungarian,Icelandic,Indonesian,Italian,Japanese,Javanese,Kannada,Kazakh,Khmer,Korean,Lao,Latin,Latvian,Letzeburgesch,Lingala,Lithuanian,Luxembourgish,Macedonian,Malagasy,Malay,Malayalam,Maltese,Mandarin,Maori,Marathi,Moldavian,Moldovan,Mongolian,Myanmar,Nepali,Norwegian,Nynorsk,Occitan,Panjabi,Pashto,Persian,Polish,Portuguese,Punjabi,Pushto,Romanian,Russian,Sanskrit,Serbian,Shona,Sindhi,Sinhala,Sinhalese,Slovak,Slovenian,Somali,Spanish,Sundanese,Swahili,Swedish,Tagalog,Tajik,Tamil,Tatar,Telugu,Thai,Tibetan,Turkish,Turkmen,Ukrainian,Urdu,Uzbek,Valencian,Vietnamese,Welsh,Yiddish,Yoruba}]
[--temperature TEMPERATURE] [--best_of BEST_OF]
[--beam_size BEAM_SIZE] [--patience PATIENCE]
[--length_penalty LENGTH_PENALTY]
[--suppress_tokens SUPPRESS_TOKENS]
[--initial_prompt INITIAL_PROMPT]
[--carry_initial_prompt CARRY_INITIAL_PROMPT]
[--condition_on_previous_text CONDITION_ON_PREVIOUS_TEXT]
[--fp16 FP16]
[--temperature_increment_on_fallback TEMPERATURE_INCREMENT_ON_FALLBACK]
[--compression_ratio_threshold COMPRESSION_RATIO_THRESHOLD]
[--logprob_threshold LOGPROB_THRESHOLD]
[--no_speech_threshold NO_SPEECH_THRESHOLD]
[--word_timestamps WORD_TIMESTAMPS]
[--prepend_punctuations PREPEND_PUNCTUATIONS]
[--append_punctuations APPEND_PUNCTUATIONS]
[--highlight_words HIGHLIGHT_WORDS]
[--max_line_width MAX_LINE_WIDTH]
[--max_line_count MAX_LINE_COUNT]
[--max_words_per_line MAX_WORDS_PER_LINE] [--threads THREADS]
[--clip_timestamps CLIP_TIMESTAMPS]
[--hallucination_silence_threshold HALLUCINATION_SILENCE_THRESHOLD]
audio [audio ...]
positional arguments:
audio                 audio file(s) to transcribe
options:
-h, --help            show this help message and exit
--model MODEL         name of the Whisper model to use (default: turbo)
--model_dir MODEL_DIR
the path to save model files; uses ~/.cache/whisper by
default (default: None)
--device DEVICE       device to use for PyTorch inference (default: cpu)
--output_dir, -o OUTPUT_DIR
directory to save the outputs (default: .)
--output_format, -f {txt,vtt,srt,tsv,json,all}
format of the output file; if not specified, all
available formats will be produced (default: all)
--verbose VERBOSE     whether to print out the progress and debug messages
(default: True)
--task {transcribe,translate}
whether to perform X->X speech recognition
('transcribe') or X->English translation ('translate')
(default: transcribe)
--language {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,yue,zh,Afrikaans,Albanian,Amharic,Arabic,Armenian,Assamese,Azerbaijani,Bashkir,Basque,Belarusian,Bengali,Bosnian,Breton,Bulgarian,Burmese,Cantonese,Castilian,Catalan,Chinese,Croatian,Czech,Danish,Dutch,English,Estonian,Faroese,Finnish,Flemish,French,Galician,Georgian,German,Greek,Gujarati,Haitian,Haitian Creole,Hausa,Hawaiian,Hebrew,Hindi,Hungarian,Icelandic,Indonesian,Italian,Japanese,Javanese,Kannada,Kazakh,Khmer,Korean,Lao,Latin,Latvian,Letzeburgesch,Lingala,Lithuanian,Luxembourgish,Macedonian,Malagasy,Malay,Malayalam,Maltese,Mandarin,Maori,Marathi,Moldavian,Moldovan,Mongolian,Myanmar,Nepali,Norwegian,Nynorsk,Occitan,Panjabi,Pashto,Persian,Polish,Portuguese,Punjabi,Pushto,Romanian,Russian,Sanskrit,Serbian,Shona,Sindhi,Sinhala,Sinhalese,Slovak,Slovenian,Somali,Spanish,Sundanese,Swahili,Swedish,Tagalog,Tajik,Tamil,Tatar,Telugu,Thai,Tibetan,Turkish,Turkmen,Ukrainian,Urdu,Uzbek,Valencian,Vietnamese,Welsh,Yiddish,Yoruba}
language spoken in the audio, specify None to perform
language detection (default: None)
--temperature TEMPERATURE
temperature to use for sampling (default: 0)
--best_of BEST_OF     number of candidates when sampling with non-zero
temperature (default: 5)
--beam_size BEAM_SIZE
number of beams in beam search, only applicable when
temperature is zero (default: 5)
--patience PATIENCE   optional patience value to use in beam decoding, as in
https://arxiv.org/abs/2204.05424, the default (1.0) is
equivalent to conventional beam search (default: None)
--length_penalty LENGTH_PENALTY
optional token length penalty coefficient (alpha) as
in https://arxiv.org/abs/1609.08144, uses simple
length normalization by default (default: None)
--suppress_tokens SUPPRESS_TOKENS
comma-separated list of token ids to suppress during
sampling; '-1' will suppress most special characters
except common punctuations (default: -1)
--initial_prompt INITIAL_PROMPT
optional text to provide as a prompt for the first
window. (default: None)
--carry_initial_prompt CARRY_INITIAL_PROMPT
if True, prepend initial_prompt to every internal
decode() call. May reduce the effectiveness of
condition_on_previous_text (default: False)
--condition_on_previous_text CONDITION_ON_PREVIOUS_TEXT
if True, provide the previous output of the model as a
prompt for the next window; disabling may make the
text inconsistent across windows, but the model
becomes less prone to getting stuck in a failure loop
(default: True)
--fp16 FP16           whether to perform inference in fp16; True by default
(default: True)
--temperature_increment_on_fallback TEMPERATURE_INCREMENT_ON_FALLBACK
temperature to increase when falling back when the
decoding fails to meet either of the thresholds below
(default: 0.2)
--compression_ratio_threshold COMPRESSION_RATIO_THRESHOLD
if the gzip compression ratio is higher than this
value, treat the decoding as failed (default: 2.4)
--logprob_threshold LOGPROB_THRESHOLD
if the average log probability is lower than this
value, treat the decoding as failed (default: -1.0)
--no_speech_threshold NO_SPEECH_THRESHOLD
if the probability of the <|nospeech|> token is higher
than this value AND the decoding has failed due to
logprob_threshold, consider the segment as silence
(default: 0.6)
--word_timestamps WORD_TIMESTAMPS
(experimental) extract word-level timestamps and
refine the results based on them (default: False)
--prepend_punctuations PREPEND_PUNCTUATIONS
if word_timestamps is True, merge these punctuation
symbols with the next word (default: "'“¿([{-)
--append_punctuations APPEND_PUNCTUATIONS
if word_timestamps is True, merge these punctuation
symbols with the previous word (default:
"'.。,，!！?？:：”)]}、)
--highlight_words HIGHLIGHT_WORDS
(requires --word_timestamps True) underline each word
as it is spoken in srt and vtt (default: False)
--max_line_width MAX_LINE_WIDTH
(requires --word_timestamps True) the maximum number
of characters in a line before breaking the line
(default: None)
--max_line_count MAX_LINE_COUNT
(requires --word_timestamps True) the maximum number
of lines in a segment (default: None)
--max_words_per_line MAX_WORDS_PER_LINE
(requires --word_timestamps True, no effect with
--max_line_width) the maximum number of words in a
segment (default: None)
--threads THREADS     number of threads used by torch for CPU inference;
supercedes MKL_NUM_THREADS/OMP_NUM_THREADS (default:
0)
--clip_timestamps CLIP_TIMESTAMPS
comma-separated list start,end,start,end,...
timestamps (in seconds) of clips to process, where the
last end timestamp defaults to the end of the file
(default: 0)
--hallucination_silence_threshold HALLUCINATION_SILENCE_THRESHOLD
(requires --word_timestamps True) skip silent periods
longer than this threshold (in seconds) when a
possible hallucination is detected (default: None)
❯ python3 -m whisper --help
usage: main.py [-h] [--model MODEL] [--model_dir MODEL_DIR]
[--device DEVICE] [--output_dir OUTPUT_DIR]
[--output_format {txt,vtt,srt,tsv,json,all}]
[--verbose VERBOSE] [--task {transcribe,translate}]
[--language {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,yue,zh,Afrikaans,Albanian,Amharic,Arabic,Armenian,Assamese,Azerbaijani,Bashkir,Basque,Belarusian,Bengali,Bosnian,Breton,Bulgarian,Burmese,Cantonese,Castilian,Catalan,Chinese,Croatian,Czech,Danish,Dutch,English,Estonian,Faroese,Finnish,Flemish,French,Galician,Georgian,German,Greek,Gujarati,Haitian,Haitian Creole,Hausa,Hawaiian,Hebrew,Hindi,Hungarian,Icelandic,Indonesian,Italian,Japanese,Javanese,Kannada,Kazakh,Khmer,Korean,Lao,Latin,Latvian,Letzeburgesch,Lingala,Lithuanian,Luxembourgish,Macedonian,Malagasy,Malay,Malayalam,Maltese,Mandarin,Maori,Marathi,Moldavian,Moldovan,Mongolian,Myanmar,Nepali,Norwegian,Nynorsk,Occitan,Panjabi,Pashto,Persian,Polish,Portuguese,Punjabi,Pushto,Romanian,Russian,Sanskrit,Serbian,Shona,Sindhi,Sinhala,Sinhalese,Slovak,Slovenian,Somali,Spanish,Sundanese,Swahili,Swedish,Tagalog,Tajik,Tamil,Tatar,Telugu,Thai,Tibetan,Turkish,Turkmen,Ukrainian,Urdu,Uzbek,Valencian,Vietnamese,Welsh,Yiddish,Yoruba}]
[--temperature TEMPERATURE] [--best_of BEST_OF]
[--beam_size BEAM_SIZE] [--patience PATIENCE]
[--length_penalty LENGTH_PENALTY]
[--suppress_tokens SUPPRESS_TOKENS]
[--initial_prompt INITIAL_PROMPT]
[--carry_initial_prompt CARRY_INITIAL_PROMPT]
[--condition_on_previous_text CONDITION_ON_PREVIOUS_TEXT]
[--fp16 FP16]
[--temperature_increment_on_fallback TEMPERATURE_INCREMENT_ON_FALLBACK]
[--compression_ratio_threshold COMPRESSION_RATIO_THRESHOLD]
[--logprob_threshold LOGPROB_THRESHOLD]
[--no_speech_threshold NO_SPEECH_THRESHOLD]
[--word_timestamps WORD_TIMESTAMPS]
[--prepend_punctuations PREPEND_PUNCTUATIONS]
[--append_punctuations APPEND_PUNCTUATIONS]
[--highlight_words HIGHLIGHT_WORDS]
[--max_line_width MAX_LINE_WIDTH]
[--max_line_count MAX_LINE_COUNT]
[--max_words_per_line MAX_WORDS_PER_LINE]
[--threads THREADS] [--clip_timestamps CLIP_TIMESTAMPS]
[--hallucination_silence_threshold HALLUCINATION_SILENCE_THRESHOLD]
audio [audio ...]
positional arguments:
audio                 audio file(s) to transcribe
options:
-h, --help            show this help message and exit
--model MODEL         name of the Whisper model to use (default: turbo)
--model_dir MODEL_DIR
the path to save model files; uses ~/.cache/whisper by
default (default: None)
--device DEVICE       device to use for PyTorch inference (default: cpu)
--output_dir, -o OUTPUT_DIR
directory to save the outputs (default: .)
--output_format, -f {txt,vtt,srt,tsv,json,all}
format of the output file; if not specified, all
available formats will be produced (default: all)
--verbose VERBOSE     whether to print out the progress and debug messages
(default: True)
--task {transcribe,translate}
whether to perform X->X speech recognition
('transcribe') or X->English translation ('translate')
(default: transcribe)
--language {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,yue,zh,Afrikaans,Albanian,Amharic,Arabic,Armenian,Assamese,Azerbaijani,Bashkir,Basque,Belarusian,Bengali,Bosnian,Breton,Bulgarian,Burmese,Cantonese,Castilian,Catalan,Chinese,Croatian,Czech,Danish,Dutch,English,Estonian,Faroese,Finnish,Flemish,French,Galician,Georgian,German,Greek,Gujarati,Haitian,Haitian Creole,Hausa,Hawaiian,Hebrew,Hindi,Hungarian,Icelandic,Indonesian,Italian,Japanese,Javanese,Kannada,Kazakh,Khmer,Korean,Lao,Latin,Latvian,Letzeburgesch,Lingala,Lithuanian,Luxembourgish,Macedonian,Malagasy,Malay,Malayalam,Maltese,Mandarin,Maori,Marathi,Moldavian,Moldovan,Mongolian,Myanmar,Nepali,Norwegian,Nynorsk,Occitan,Panjabi,Pashto,Persian,Polish,Portuguese,Punjabi,Pushto,Romanian,Russian,Sanskrit,Serbian,Shona,Sindhi,Sinhala,Sinhalese,Slovak,Slovenian,Somali,Spanish,Sundanese,Swahili,Swedish,Tagalog,Tajik,Tamil,Tatar,Telugu,Thai,Tibetan,Turkish,Turkmen,Ukrainian,Urdu,Uzbek,Valencian,Vietnamese,Welsh,Yiddish,Yoruba}
language spoken in the audio, specify None to perform
language detection (default: None)
--temperature TEMPERATURE
temperature to use for sampling (default: 0)
--best_of BEST_OF     number of candidates when sampling with non-zero
temperature (default: 5)
--beam_size BEAM_SIZE
number of beams in beam search, only applicable when
temperature is zero (default: 5)
--patience PATIENCE   optional patience value to use in beam decoding, as in
https://arxiv.org/abs/2204.05424, the default (1.0) is
equivalent to conventional beam search (default: None)
--length_penalty LENGTH_PENALTY
optional token length penalty coefficient (alpha) as
in https://arxiv.org/abs/1609.08144, uses simple
length normalization by default (default: None)
--suppress_tokens SUPPRESS_TOKENS
comma-separated list of token ids to suppress during
sampling; '-1' will suppress most special characters
except common punctuations (default: -1)
--initial_prompt INITIAL_PROMPT
optional text to provide as a prompt for the first
window. (default: None)
--carry_initial_prompt CARRY_INITIAL_PROMPT
if True, prepend initial_prompt to every internal
decode() call. May reduce the effectiveness of
condition_on_previous_text (default: False)
--condition_on_previous_text CONDITION_ON_PREVIOUS_TEXT
if True, provide the previous output of the model as a
prompt for the next window; disabling may make the
text inconsistent across windows, but the model
becomes less prone to getting stuck in a failure loop
(default: True)
--fp16 FP16           whether to perform inference in fp16; True by default
(default: True)
--temperature_increment_on_fallback TEMPERATURE_INCREMENT_ON_FALLBACK
temperature to increase when falling back when the
decoding fails to meet either of the thresholds below
(default: 0.2)
--compression_ratio_threshold COMPRESSION_RATIO_THRESHOLD
if the gzip compression ratio is higher than this
value, treat the decoding as failed (default: 2.4)
--logprob_threshold LOGPROB_THRESHOLD
if the average log probability is lower than this
value, treat the decoding as failed (default: -1.0)
--no_speech_threshold NO_SPEECH_THRESHOLD
if the probability of the <|nospeech|> token is higher
than this value AND the decoding has failed due to
logprob_threshold, consider the segment as silence
(default: 0.6)
--word_timestamps WORD_TIMESTAMPS
(experimental) extract word-level timestamps and
refine the results based on them (default: False)
--prepend_punctuations PREPEND_PUNCTUATIONS
if word_timestamps is True, merge these punctuation
symbols with the next word (default: "'“¿([{-)
--append_punctuations APPEND_PUNCTUATIONS
if word_timestamps is True, merge these punctuation
symbols with the previous word (default:
"'.。,，!！?？:：”)]}、)
--highlight_words HIGHLIGHT_WORDS
(requires --word_timestamps True) underline each word
as it is spoken in srt and vtt (default: False)
--max_line_width MAX_LINE_WIDTH
(requires --word_timestamps True) the maximum number
of characters in a line before breaking the line
(default: None)
--max_line_count MAX_LINE_COUNT
(requires --word_timestamps True) the maximum number
of lines in a segment (default: None)
--max_words_per_line MAX_WORDS_PER_LINE
(requires --word_timestamps True, no effect with
--max_line_width) the maximum number of words in a
segment (default: None)
--threads THREADS     number of threads used by torch for CPU inference;
supercedes MKL_NUM_THREADS/OMP_NUM_THREADS (default:
0)
--clip_timestamps CLIP_TIMESTAMPS
comma-separated list start,end,start,end,...
timestamps (in seconds) of clips to process, where the
last end timestamp defaults to the end of the file
(default: 0)
--hallucination_silence_threshold HALLUCINATION_SILENCE_THRESHOLD
(requires --word_timestamps True) skip silent periods
longer than this threshold (in seconds) when a
possible hallucination is detected (default: None)
╭─ ~                                                    ✔  at 01:29:12 下午 ─╮
╰─                                                                           ─╯
