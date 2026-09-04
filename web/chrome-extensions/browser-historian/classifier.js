/**
 * 龍魂 · 浏览器史官 — 分类引擎 v1.0
 * DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-BROWSER-CLASSIFIER-v1.0
 * 创建者: 诸葛鑫（UID9622）
 * 协议: CC BY-NC-SA 4.0
 *
 * 三级分类：域名精确匹配 → 域名模糊匹配 → 关键词匹配
 * 全本地运行，数据不离开浏览器。
 */

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 一级：域名精确匹配（最高优先级）
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const DOMAIN_MAP = {
  // 🤖 AI / 技术
  'github.com': 'ai-tech',
  'gist.github.com': 'ai-tech',
  'gitlab.com': 'ai-tech',
  'stackoverflow.com': 'ai-tech',
  'serverfault.com': 'ai-tech',
  'superuser.com': 'ai-tech',
  'askubuntu.com': 'ai-tech',
  'arxiv.org': 'ai-tech',
  'paperswithcode.com': 'ai-tech',
  'huggingface.co': 'ai-tech',
  'huggingface.com': 'ai-tech',
  'pytorch.org': 'ai-tech',
  'tensorflow.org': 'ai-tech',
  'openai.com': 'ai-tech',
  'platform.openai.com': 'ai-tech',
  'chat.openai.com': 'ai-tech',
  'chatgpt.com': 'ai-tech',
  'anthropic.com': 'ai-tech',
  'claude.ai': 'ai-tech',
  'deepmind.google': 'ai-tech',
  'deepmind.com': 'ai-tech',
  'kaggle.com': 'ai-tech',
  'colab.research.google.com': 'ai-tech',
  'huggingface.co': 'ai-tech',
  'modelscope.cn': 'ai-tech',
  'kimi.moonshot.cn': 'ai-tech',
  'tongyi.aliyun.com': 'ai-tech',
  'yiyan.baidu.com': 'ai-tech',
  'xinghuo.xfyun.cn': 'ai-tech',
  'deepseek.com': 'ai-tech',
  'chat.deepseek.com': 'ai-tech',
  'bard.google.com': 'ai-tech',
  'gemini.google.com': 'ai-tech',
  'aistudio.google.com': 'ai-tech',
  'wandb.ai': 'ai-tech',
  'mlflow.org': 'ai-tech',
  'langchain.com': 'ai-tech',
  'llamaindex.ai': 'ai-tech',
  'ollama.com': 'ai-tech',
  'ollama.ai': 'ai-tech',
  'vllm.ai': 'ai-tech',
  'nvidia.com': 'ai-tech',
  'developer.nvidia.com': 'ai-tech',
  'catalog.ngc.nvidia.com': 'ai-tech',
  'docs.nvidia.com': 'ai-tech',
  'mlx.ai': 'ai-tech',
  'cloudbase.net': 'ai-tech',
  'tcb.cloud.tencent.com': 'ai-tech',
  'console.cloud.tencent.com': 'ai-tech',
  'aliyun.com': 'ai-tech',
  'developer.aliyun.com': 'ai-tech',
  'huaweicloud.com': 'ai-tech',
  'docker.com': 'ai-tech',
  'hub.docker.com': 'ai-tech',
  'kubernetes.io': 'ai-tech',
  'k8s.io': 'ai-tech',
  'helm.sh': 'ai-tech',
  'terraform.io': 'ai-tech',
  'ansible.com': 'ai-tech',
  'npmjs.com': 'ai-tech',
  'pypi.org': 'ai-tech',
  'crates.io': 'ai-tech',
  'docs.python.org': 'ai-tech',
  'developer.mozilla.org': 'ai-tech',
  'w3schools.com': 'ai-tech',
  'codepen.io': 'ai-tech',
  'jsfiddle.net': 'ai-tech',
  'codesandbox.io': 'ai-tech',
  'replit.com': 'ai-tech',
  'leetcode.com': 'ai-tech',
  'leetcode.cn': 'ai-tech',
  'nowcoder.com': 'ai-tech',
  'lintcode.com': 'ai-tech',
  'dev.to': 'ai-tech',
  'hackernoon.com': 'ai-tech',
  'freecodecamp.org': 'ai-tech',
  'codecademy.com': 'ai-tech',
  'udemy.com': 'ai-tech',
  'coursera.org': 'ai-tech',
  'csdn.net': 'ai-tech',
  'blog.csdn.net': 'ai-tech',
  'juejin.cn': 'ai-tech',
  'segmentfault.com': 'ai-tech',
  'v2ex.com': 'ai-tech',
  'infoq.cn': 'ai-tech',
  'infoq.com': 'ai-tech',
  'oschina.net': 'ai-tech',
  'gitee.com': 'ai-tech',
  'sourceforge.net': 'ai-tech',
  'bitbucket.org': 'ai-tech',
  'codeberg.org': 'ai-tech',
  'linux.org': 'ai-tech',
  'kernel.org': 'ai-tech',
  'ubuntu.com': 'ai-tech',
  'archlinux.org': 'ai-tech',
  'debian.org': 'ai-tech',
  'centos.org': 'ai-tech',
  'redhat.com': 'ai-tech',
  'apache.org': 'ai-tech',
  'gnu.org': 'ai-tech',
  'fsf.org': 'ai-tech',
  'raspberrypi.org': 'ai-tech',
  'arduino.cc': 'ai-tech',
  'espressif.com': 'ai-tech',
  'notion.so': 'ai-tech',
  'linear.app': 'ai-tech',
  'figma.com': 'ai-tech',
  'postman.com': 'ai-tech',
  'swagger.io': 'ai-tech',
  'graphql.org': 'ai-tech',
  'redis.io': 'ai-tech',
  'mongodb.com': 'ai-tech',
  'postgresql.org': 'ai-tech',
  'mysql.com': 'ai-tech',
  'sqlite.org': 'ai-tech',
  'elastic.co': 'ai-tech',
  'prometheus.io': 'ai-tech',
  'grafana.com': 'ai-tech',
  'opentelemetry.io': 'ai-tech',
  'jenkins.io': 'ai-tech',
  'gitlab-ci': 'ai-tech',
  'travis-ci.org': 'ai-tech',
  'circleci.com': 'ai-tech',
  'github.io': 'ai-tech',
  'vercel.com': 'ai-tech',
  'netlify.com': 'ai-tech',
  'cloudflare.com': 'ai-tech',
  'workers.dev': 'ai-tech',
  'supabase.com': 'ai-tech',
  'firebase.google.com': 'ai-tech',
  'aws.amazon.com': 'ai-tech',
  'digitalocean.com': 'ai-tech',
  'linode.com': 'ai-tech',
  'heroku.com': 'ai-tech',
  'railway.app': 'ai-tech',
  'fly.io': 'ai-tech',
  'render.com': 'ai-tech',

  // 🔞 成人内容
  'pornhub.com': 'adult',
  'pornhubpremium.com': 'adult',
  'xvideos.com': 'adult',
  'xnxx.com': 'adult',
  'xhamster.com': 'adult',
  'redtube.com': 'adult',
  'youporn.com': 'adult',
  'spankbang.com': 'adult',
  'tube8.com': 'adult',
  'youjizz.com': 'adult',
  'porntrex.com': 'adult',
  'tnaflix.com': 'adult',
  'fuq.com': 'adult',
  'eporner.com': 'adult',
  'beeg.com': 'adult',
  'motherless.com': 'adult',
  'literotica.com': 'adult',
  'chaturbate.com': 'adult',
  'livejasmin.com': 'adult',
  'stripchat.com': 'adult',
  'bongacams.com': 'adult',
  'camsoda.com': 'adult',
  'onlyfans.com': 'adult',
  'fansly.com': 'adult',
  'nhentai.net': 'adult',
  'hentaihaven.com': 'adult',
  'hanime.tv': 'adult',
  'rule34.xxx': 'adult',
  'e-hentai.org': 'adult',
  'exhentai.org': 'adult',
  'gelbooru.com': 'adult',
  'danbooru.donmai.us': 'adult',
  'sankakucomplex.com': 'adult',
  'f95zone.to': 'adult',
  'adulttime.com': 'adult',
  'brazzers.com': 'adult',
  'naughtyamerica.com': 'adult',
  'realitykings.com': 'adult',
  'bangbros.com': 'adult',
  'digitalplayground.com': 'adult',
  'adultfriendfinder.com': 'adult',
  'ashleymadison.com': 'adult',
  'tinder.com': 'adult',
  'grindr.com': 'adult',
  'fetlife.com': 'adult',
  'thisvid.com': 'adult',

  // 📱 社交媒体
  'twitter.com': 'social',
  'x.com': 'social',
  'facebook.com': 'social',
  'instagram.com': 'social',
  'linkedin.com': 'social',
  'tiktok.com': 'social',
  'reddit.com': 'social',
  'old.reddit.com': 'social',
  'weibo.com': 'social',
  'weibo.cn': 'social',
  'douban.com': 'social',
  'zhihu.com': 'social',
  'tieba.baidu.com': 'social',
  'douyin.com': 'social',
  'xiaohongshu.com': 'social',
  'hupu.com': 'social',
  'nga.cn': 'social',
  'bbs.nga.cn': 'social',
  'discord.com': 'social',
  'telegram.org': 'social',
  'web.telegram.org': 'social',
  'slack.com': 'social',
  'matrix.org': 'social',
  'mastodon.social': 'social',
  'truthsocial.com': 'social',
  'threads.net': 'social',
  'snapchat.com': 'social',
  'pinterest.com': 'social',
  'tumblr.com': 'social',
  'quora.com': 'social',
  'medium.com': 'social',
  'substack.com': 'social',

  // 📰 新闻资讯
  'news.google.com': 'news',
  'news.ycombinator.com': 'news',
  '36kr.com': 'news',
  'ithome.com': 'news',
  'solidot.org': 'news',
  'cnbeta.com': 'news',
  'thepaper.cn': 'news',
  'guancha.cn': 'news',
  'huxiu.com': 'news',
  'geekpark.net': 'news',
  'pingwest.com': 'news',
  'techcrunch.com': 'news',
  'theverge.com': 'news',
  'arstechnica.com': 'news',
  'wired.com': 'news',
  'engadget.com': 'news',
  'theinformation.com': 'news',
  'bloomberg.com': 'news',
  'reuters.com': 'news',
  'apnews.com': 'news',
  'bbc.com': 'news',
  'bbc.co.uk': 'news',
  'cnn.com': 'news',
  'nytimes.com': 'news',
  'wsj.com': 'news',
  'ft.com': 'news',
  'economist.com': 'news',
  'people.com.cn': 'news',
  'xinhuanet.com': 'news',
  'cctv.com': 'news',
  'chinadaily.com.cn': 'news',
  'sina.com.cn': 'news',
  'sohu.com': 'news',
  '163.com': 'news',
  'ifeng.com': 'news',
  'qq.com': 'news',
  'toutiao.com': 'news',

  // 🛒 购物
  'taobao.com': 'shopping',
  'tmall.com': 'shopping',
  'jd.com': 'shopping',
  'amazon.com': 'shopping',
  'amazon.cn': 'shopping',
  'pinduoduo.com': 'shopping',
  'yangkeduo.com': 'shopping',
  'suning.com': 'shopping',
  'vip.com': 'shopping',
  'mogujie.com': 'shopping',
  'yanxuan.com': 'shopping',
  'smzdm.com': 'shopping',
  'ebay.com': 'shopping',
  'aliexpress.com': 'shopping',
  'shopee.com': 'shopping',
  'walmart.com': 'shopping',
  'bestbuy.com': 'shopping',
  'etsy.com': 'shopping',
  'z.cn': 'shopping',
  '1688.com': 'shopping',

  // 🎬 视频娱乐
  'youtube.com': 'video',
  'youtu.be': 'video',
  'bilibili.com': 'video',
  'b23.tv': 'video',
  'youku.com': 'video',
  'iqiyi.com': 'video',
  'iq.com': 'video',
  'tencentvideo.com': 'video',
  'v.qq.com': 'video',
  'mgtv.com': 'video',
  'netflix.com': 'video',
  'hulu.com': 'video',
  'disneyplus.com': 'video',
  'hbomax.com': 'video',
  'primevideo.com': 'video',
  'twitch.tv': 'video',
  'vimeo.com': 'video',
  'dailymotion.com': 'video',
  'acfun.cn': 'video',
  'huya.com': 'video',
  'douyu.com': 'video',
  'chzzk.naver.com': 'video',
  'afreecatv.com': 'video',
  'sooplive.com': 'video',

  // 🔍 搜索引擎
  'google.com': 'search',
  'www.google.com': 'search',
  'baidu.com': 'search',
  'bing.com': 'search',
  'sogou.com': 'search',
  'so.com': 'search',
  'duckduckgo.com': 'search',
  'yandex.com': 'search',
  'yahoo.com': 'search',
  'kagi.com': 'search',
  'perplexity.ai': 'search',
  'search.brave.com': 'search',
};

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 二级：域名模糊关键词匹配
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const DOMAIN_FUZZY = [
  // AI/Tech
  { pattern: /github/i, cat: 'ai-tech' },
  { pattern: /gitlab/i, cat: 'ai-tech' },
  { pattern: /stackoverflow|stackexchange/i, cat: 'ai-tech' },
  { pattern: /huggingface/i, cat: 'ai-tech' },
  { pattern: /arxiv/i, cat: 'ai-tech' },
  { pattern: /kaggle/i, cat: 'ai-tech' },
  { pattern: /pypi|npmjs|crates\.io|maven|nuget/i, cat: 'ai-tech' },
  { pattern: /docker|kubernetes|k8s|helm/i, cat: 'ai-tech' },
  { pattern: /tensorflow|pytorch|jax|mlx|keras|caffe|onnx/i, cat: 'ai-tech' },
  { pattern: /openai|anthropic|deepmind|gemini|bard|llama|mistral/i, cat: 'ai-tech' },
  { pattern: /ollama|vllm|langchain|llamaindex|chromadb|pinecone|weaviate|qdrant/i, cat: 'ai-tech' },
  { pattern: /mlflow|wandb|neptune|comet/i, cat: 'ai-tech' },
  { pattern: /deploy|devops|ci[_-]?cd|jenkins|travis|circleci|drone/i, cat: 'ai-tech' },
  { pattern: /nginx|apache|haproxy|traefik|caddy/i, cat: 'ai-tech' },
  { pattern: /redis|mongodb|postgres|mysql|mariadb|sqlite|cassandra|neo4j|elasticsearch|kafka|rabbitmq|nats/i, cat: 'ai-tech' },
  { pattern: /grafana|prometheus|opentelemetry|datadog|newrelic|sentry/i, cat: 'ai-tech' },
  { pattern: /aws|azure|gcp|cloudflare|vercel|netlify|heroku|digitalocean|alicloud|tencentcloud|huaweicloud|cloudbase/i, cat: 'ai-tech' },
  { pattern: /vscode|jetbrains|intellij|webstorm|pycharm|goland/i, cat: 'ai-tech' },
  { pattern: /jupyter|colab\.|notebook|deepnote/i, cat: 'ai-tech' },
  { pattern: /leetcode|lintcode|nowcoder|codewars|hackerrank/i, cat: 'ai-tech' },
  { pattern: /csdn|juejin|segmentfault|oschina|v2ex|infoq|51cto/i, cat: 'ai-tech' },
  { pattern: /dev\.to|hackernoon|freecodecamp|codecademy|coursera|udemy|udacity|edx/i, cat: 'ai-tech' },
  { pattern: /kernel|linux\.org|ubuntu|debian|archlinux|centos|fedora|opensuse/i, cat: 'ai-tech' },
  { pattern: /npm|nodejs|deno|bun\.sh|rust|golang|python\.org|java\.com/i, cat: 'ai-tech' },
  { pattern: /docs\.|documentation|api-reference|sdk/i, cat: 'ai-tech' },

  // Adult
  { pattern: /porn|xxx|sex|adult|hentai|nsfw|nude|erot|fuck|milf|teen|anal|dick|pussy|boob|tits|ass|bdsm|gay.*tube|tranny|shemale/i, cat: 'adult' },
  { pattern: /cam|livejasmin|stripchat|chaturbate|onlyfans|fansly/i, cat: 'adult' },
  { pattern: /rule34|e-hentai|exhentai|gelbooru|danbooru|sankaku/i, cat: 'adult' },
  { pattern: /jav|japanese.*adult|tokyo.*hot|caribbeancom|heyzo|avgle/i, cat: 'adult' },
  { pattern: /f95zone|naughty|brazzers|bangbros|realitykings|digitalplayground|adulttime/i, cat: 'adult' },

  // Social
  { pattern: /twitter|facebook|instagram|linkedin|tiktok|snapchat|pinterest/i, cat: 'social' },
  { pattern: /weibo|douban|zhihu|tieba|douyin|xiaohongshu|hupu|nga/i, cat: 'social' },
  { pattern: /discord|telegram|slack|matrix|mastodon/i, cat: 'social' },
  { pattern: /reddit|quora|medium|substack/i, cat: 'social' },
  { pattern: /bbs|forum|community/i, cat: 'social' },

  // News
  { pattern: /news|press|media|journal|report/i, cat: 'news' },
  { pattern: /36kr|ithome|cnbeta|solidot|thepaper|guancha|huxiu|geekpark|pingwest/i, cat: 'news' },
  { pattern: /techcrunch|theverge|arstechnica|wired|engadget|theinformation/i, cat: 'news' },
  { pattern: /bloomberg|reuters|apnews|bbc|cnn|nytimes|wsj|ft\.com|economist/i, cat: 'news' },
  { pattern: /people\.com|chinadaily|chinanews|globaltimes/i, cat: 'news' },

  // Shopping
  { pattern: /taobao|tmall|jd\.com|pinduoduo|amazon|ebay|shop|mall|buy|store|price/i, cat: 'shopping' },
  { pattern: /suning|vip\.com|mogujie|yanxuan|smzdm|1688/i, cat: 'shopping' },

  // Video/Entertainment
  { pattern: /youtube|youtu\.be|bilibili|youku|iqiyi|tv\.qq|mgtv|netflix|hulu|disneyplus/i, cat: 'video' },
  { pattern: /twitch|vimeo|dailymotion|acfun|huya|douyu|afreecatv|chzzk/i, cat: 'video' },
  { pattern: /movie|anime|drama|series|episode|stream|watch|live|broadcast/i, cat: 'video' },

  // Search
  { pattern: /baidu|bing|sogou|duckduckgo|yandex|yahoo|perplexity|search/i, cat: 'search' },

  // Finance
  { pattern: /bank|pay|wallet|alipay|weixin.*pay|unionpay|stripe|paypal/i, cat: 'finance' },
  { pattern: /stock|fund|etf|bond|crypto|bitcoin|ethereum|blockchain|exchange/i, cat: 'finance' },
];

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 三级：URL/标题关键词匹配（最低优先级）
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const KEYWORD_PATTERNS = [
  { pattern: /人工智能|机器学习|深度学习|神经网络|大模型|LLM|GPT|Transformer|NLP|CV|RL|AGI|fine.?tun|训练|推理|微调|对齐|提示词|prompt/i, cat: 'ai-tech' },
  { pattern: /python|javascript|typescript|rust|golang|java|c\+\+|编程|代码|算法|数据结构|debug|异常|报错|bug|性能优化/i, cat: 'ai-tech' },
  { pattern: /API|接口|部署|上线|发布|运维|监控|日志|数据库|缓存|队列|微服务/i, cat: 'ai-tech' },
  { pattern: /开源|open.?source|github|pull.*request|issue|commit|merge|release/i, cat: 'ai-tech' },
  { pattern: /Linux|macOS|Windows|Shell|Bash|终端|命令行|终端|环境变量|配置/i, cat: 'ai-tech' },
  { pattern: /域名|DNS|IP|端口|网络安全|防火墙|加密|签名|证书|HTTPS/i, cat: 'ai-tech' },

  { pattern: /成人|色情|约炮|一夜情|援交|卖淫|嫖娼|包养|性伴侣|换妻|淫|乱伦/i, cat: 'adult' },
  { pattern: /AV|番号|无码|有码|中出|口交|肛交|潮吹|巨乳|美腿|丝袜|制服/i, cat: 'adult' },

  { pattern: /微博|微信|朋友圈|抖音|快手|小红书|知乎|豆瓣|贴吧|虎扑/i, cat: 'social' },
  { pattern: /点赞|评论|转发|关注|粉丝|私信|群聊|好友|动态/i, cat: 'social' },

  { pattern: /新闻|热点|报道|快讯|突发|最新|事件|政策|法规/i, cat: 'news' },

  { pattern: /购买|价格|优惠|折扣|包邮|秒杀|满减|优惠券|拼团/i, cat: 'shopping' },

  { pattern: /视频|电影|电视剧|综艺|动漫|纪录片|直播|弹幕|追剧|看片/i, cat: 'video' },

  { pattern: /搜索|查找|查询|检索/i, cat: 'search' },
];

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 分类标签中文名
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const CATEGORY_LABELS = {
  'ai-tech': { name: 'AI/技术', icon: '🤖', color: '#F5A623' },
  'adult': { name: '成人内容', icon: '🔞', color: '#E74C3C' },
  'social': { name: '社交媒体', icon: '📱', color: '#3498DB' },
  'news': { name: '新闻资讯', icon: '📰', color: '#2ECC71' },
  'shopping': { name: '购物消费', icon: '🛒', color: '#9B59B6' },
  'video': { name: '视频娱乐', icon: '🎬', color: '#E67E22' },
  'search': { name: '搜索引擎', icon: '🔍', color: '#1ABC9C' },
  'finance': { name: '金融财经', icon: '💰', color: '#C0392B' },
  'other': { name: '其他', icon: '📌', color: '#7F8C8D' },
};

/**
 * 提取域名（去掉 www 前缀）
 */
function extractDomain(url) {
  try {
    let hostname = new URL(url).hostname;
    return hostname.replace(/^www\./, '').toLowerCase();
  } catch {
    return '';
  }
}

/**
 * 主分类函数
 * @param {string} url - 完整URL
 * @param {string} title - 页面标题
 * @returns {{cat: string, label: string, icon: string, color: string, matchedBy: string}}
 */
function classify(url, title = '') {
  if (!url) {
    return makeResult('other', 'no-url');
  }

  const domain = extractDomain(url);
  const urlLower = url.toLowerCase();
  const titleLower = (title || '').toLowerCase();

  // 一级：精确域名匹配
  if (domain && DOMAIN_MAP[domain]) {
    return makeResult(DOMAIN_MAP[domain], `domain-exact:${domain}`);
  }

  // 二级：模糊域名匹配
  if (domain) {
    for (const rule of DOMAIN_FUZZY) {
      if (rule.pattern.test(domain)) {
        return makeResult(rule.cat, `domain-fuzzy:${domain}`);
      }
    }
  }

  // 三级：URL/标题关键词匹配
  const combined = urlLower + ' ' + titleLower;
  for (const rule of KEYWORD_PATTERNS) {
    if (rule.pattern.test(combined)) {
      return makeResult(rule.cat, `keyword:${rule.pattern.source.slice(0, 30)}`);
    }
  }

  return makeResult('other', 'none');
}

function makeResult(cat, matchedBy) {
  const label = CATEGORY_LABELS[cat] || CATEGORY_LABELS['other'];
  return {
    cat,
    name: label.name,
    icon: label.icon,
    color: label.color,
    matchedBy,
  };
}

/**
 * 批量分类
 * @param {Array<{url: string, title?: string}>} items
 * @returns {Array} 输入items + cat分类字段
 */
function classifyBatch(items) {
  return items.map(item => {
    const result = classify(item.url, item.title || '');
    return { ...item, ...result };
  });
}

/**
 * 生成分类统计
 * @param {Array} classifiedItems
 * @returns {Object} {cat: {count, items, name, icon, color}}
 */
function getStats(classifiedItems) {
  const stats = {};
  for (const item of classifiedItems) {
    if (!stats[item.cat]) {
      stats[item.cat] = {
        count: 0,
        items: [],
        name: item.name,
        icon: item.icon,
        color: item.color,
      };
    }
    stats[item.cat].count++;
    stats[item.cat].items.push(item);
  }
  return stats;
}

// 导出（ES module + global 兼容）
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { classify, classifyBatch, getStats, CATEGORY_LABELS, DOMAIN_MAP, DOMAIN_FUZZY, KEYWORD_PATTERNS };
}
