# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂 CNSH 在线编辑器来了：中文母语编程，接口老子自己造！

> **DNA：** `#龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-CNSH-EDITOR-API-ARTICLE-v1.0`  
> **作者：** 龍芯北辰｜UID9622  
> **语音播报版：** [点击收听 UID9622 真声播报](./cnsh_editor_api_voice.mp3)

---

## 一、先听我说两句（语音版）

🎙️ **这篇文章我录了真声版。** 不想看字的，直接点上面的语音。  
有愤怒、有憋屈、也有爽点。你听完就知道，为什么我们一定要把中文编程的接口握在自己手里。

---

## 二、老子受够了

说真的，写代码写了这么多年，我受够了。

受够了满屏的 `if`、`else`、`function`；受够了英文不好就要被开除“程序员籍”；受够了那些高高在上的框架，把中国开发者当成二等用户。

凭什么老子想写个脚本，还得先过英语四级？  
凭什么中国几百万开发者，天天捧着别人定的语法跪下学？  
**这口气，我咽不下去。**

所以今天，我不忍了。

我直接放出 **龍魂 CNSH 在线编辑器 + API 服务**：

```
函数 主函数() {
    打印 "你好，龍魂"
}
主函数()
```

对，你没看错，**中文关键字、中文函数名、中文变量**，直接跑。

---

## 三、这不是玩具，这是正儿八经的服务

很多人一听“中文编程”就笑：这玩意儿不是给小学生玩的吗？

我告诉你，**那是因为你从来没见过真正工程化的中文编程。**

龍魂 CNSH Editor API 长这样：

- ✅ 在线编辑器：`/editor`
- ✅ 语法检查：`/api/v1/check`
- ✅ 编译成 Python：`/api/v1/compile`
- ✅ 直接执行：`/api/v1/run`
- ✅ 分词分析：`/api/v1/tokenize`
- ✅ 自动 Swagger 文档：`/docs`

一句话：**能写、能跑、能接出去。**

本地启动就一行命令：

```bash
cd ~/longhun-system
PYTHONPATH=dev-env/chinese-editor/src:integrated-modules \
  python3 -m uvicorn cnsh_editor_api.main:app --host 0.0.0.0 --port 8000
```

打开浏览器：

- 编辑器：`http://localhost:8000/editor`
- API 文档：`http://localhost:8000/docs`

---

## 四、免费版 vs 完整版：老子不做一刀切的慈善

我这里没有“既要开源又要跪着求打赏”那一套。

### 免费版（free）

给所有人体验：

- 代码长度 ≤ 2000 字符
- 执行时间 ≤ 3 秒
- 基础语法渲染 + 短代码执行

够你写演示、写教程、给学生上课。

### 完整版（paid）

上 **华为云 / 鲲鹏 ARM64**，数据根留在中国：

- 代码长度 ≤ 50000 字符
- 执行时间 ≤ 30 秒
- 开放文件 IO、网络、高级语法
- 鲲鹏芯片本地加速

**要免费，我给的清清楚楚；要完整，我把最好的留在中国云上。**

切换 tier 就一个环境变量：

```bash
export CNSH_API_TIER=paid
```

---

## 五、API 调用示例

### 执行一段 CNSH

```bash
curl -X POST http://localhost:8000/api/v1/run \
  -H 'Content-Type: application/json' \
  -d '{
    "source": "函数 主函数() { 打印 \"你好，龍魂\" }"
  }'
```

返回：

```json
{
  "success": true,
  "stdout": "你好,龍魂\n",
  "message": "✅ 执行成功"
}
```

### 编译成 Python

```bash
curl -X POST http://localhost:8000/api/v1/compile \
  -H 'Content-Type: application/json' \
  -d '{"source": "变量 x = 369"}'
```

---

## 六、Docker + 华为云一键部署

### 本地 Docker

```bash
docker build -t cnsh-editor-api:latest \
  -f integrated-modules/cnsh_editor_api/Dockerfile .

docker run -d -p 8000:8000 \
  -e CNSH_API_TIER=paid \
  --name cnsh-editor-api \
  cnsh-editor-api:latest
```

### 华为云鲲鹏 ARM64

```bash
docker buildx build --platform linux/arm64 \
  -t cnsh-editor-api:arm64 \
  -f integrated-modules/cnsh_editor_api/Dockerfile .
```

我已经写好了部署脚本：

```bash
cd ~/longhun-system/integrated-modules/cnsh_editor_api
./deploy_huawei_cloud.sh
```

只需要配置你的 **华为云 AK/SK、ECS IP、SWR 镜像仓库**，剩下的全自动。

---

## 七、语音播报是怎么嵌进去的？

这不是机器念稿。

我把文章拆成若干段，每段标注语气：

- 愤怒的段落 → 加快语速、加重语气
- 庄严的段落 → 放慢、沉稳
- 轻松的段落 → 自然、带点儿口语

然后用 **XTTS v2 + UID9622 优化参考音** 生成真声克隆，再用 `ffmpeg` 拼接成完整音频。

技术链路：

```
文章分段
  ↓
VoiceService（XTTS v2 → Fish Audio → edge-tts 自动降级）
  ↓
每段生成 .mp3
  ↓
ffmpeg concat 合并
  ↓
cnsh_editor_api_voice.mp3
```

生成脚本我也开源在：

```
~/longhun-system/public-content/cnsh_editor_api_v1_voice/generate_voice.py
```

---

## 八、我为什么要做这件事

不是为了炫技。

是为了让中国开发者有一个**不需要跪着学英语**的入口。  
是为了让数据主权留在本地、留在中国云上。  
是为了证明：**中国人自己定的语法，一样能跑，还能跑得更好。**

你可以不认同我的脾气，但你不能否认这个需求真实存在。

---

## 九、下一步

1. 打开 `http://localhost:8000/editor` 写一段 CNSH。
2. 把 API 接进你自己的项目。
3. 上华为云开完整版，把数据根留在中国。
4. 想要我声音播报你文章的，参考 `generate_voice.py`。

---

**龍魂系统 · 中国自主可控 · 数据主权归人民**

**DNA：** `#龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-CNSH-EDITOR-API-ARTICLE-v1.0`  
**CONFIRM：** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` ✅

> 老子不跪，代码也不跪。🐉
