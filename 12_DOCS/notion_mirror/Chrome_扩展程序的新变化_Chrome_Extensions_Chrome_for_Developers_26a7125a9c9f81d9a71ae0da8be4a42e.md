# Chrome 扩展程序的新变化  |  Chrome Extensions  |  Chrome for Developers

> Notion URL: https://app.notion.com/p/Chrome-Chrome-Extensions-Chrome-for-Developers-26a7125a9c9f81d9a71ae0da8be4a42e
> Created: 2025-09-10T22:51:00.000Z
> Last edited: 2025-09-18T19:39:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
请经常查看此页面，了解 Chrome 扩展程序、扩展程序文档或相关政策或其他方面的变化。您可以在 Chrome 扩展程序邮寄名单中找到其他通知。Chrome 时间表列出了稳定版和 Beta 版的发布日期。
## Chrome 140：新增了 sidePanel.getLayout() API
从 Chrome 140 开始，您可以使用新的 sidePanel.getLayout() API 来确定侧边栏位于屏幕的左侧还是右侧。如果您支持 RTL 语言，而新安装的 Chrome 的默认语言不同，此功能就特别有用。
## Chrome 139：在 Chrome 品牌 build 中移除 -extensions-on-chrome-urls 和 -disable-extensions-except flag
从 Chrome 139 开始，在官方 Chrome 品牌 build 中，将移除 --extensions-on-chrome-urls 和 --disable-extensions-except 命令行标志。详细了解邮寄名单。
## Chrome 138：对新标签页的更改
从 Chrome 138 开始，我们将更新新标签页界面，添加新的页脚。 您可以访问邮寄名单页面了解详情。
## 博文：在书签即将发生变更之前更新扩展程序
我们将对书签同步功能进行一些更改，这可能会影响您的扩展程序。如需了解详情，请参阅这篇博文。
## 博文：Chrome 扩展程序的最新动态，2025 年 6 月
我们一直在忙碌着，因为 Google I/O 大会即将召开，并且 Chrome 和 Chrome 应用商店中也推出了多项新功能。请参阅Chrome 扩展程序最新动态（2025 年 6 月），了解最新资讯！
## 视频：在浏览器中玩打地鼠游戏 - 这是真的吗？
观看我们的最新视频，了解如何在浏览器中制作游戏。
## 视频：Chrome 的新扩展程序菜单说明
观看我们的最新视频“Chrome 的新扩展程序菜单详解” ，了解实验性的新扩展程序菜单。
在“扩展程序真棒”第 1 集中了解如何开始扩展程序开发，并在第 2 集中了解 Chrome 自定义功能的灵活性！
## Chrome 135：新增了 userScripts.execute() API
从 Chrome 135 开始，chrome.userScripts API 中提供了一个新的 userScripts.execute() 方法。您可以使用此方法在任意时间注入用户脚本一次，而无需永久注册该脚本。
## Chrome 132：在开发者工具中查看和修改扩展程序存储空间
从 Chrome 132 开始，您可以在开发者工具中查看和修改使用 chrome.storage API 存储的数据。如需了解详情，请参阅开发者工具文档中的新页面查看和修改扩展程序存储空间。
在 Google I/O 2024 大会上，我们分享了扩展程序菜单即将发生的一些早期设计变更，这些变更可让用户更好地控制扩展程序可以访问的网站。我们很快就会开始测试这些变更，首先会在 Canary 中面向一小部分用户进行测试，并希望在未来更广泛地推出这些变更。
我们还推出了 chrome.permissions.addHostAccessRequest() API。
如需了解详情，请参阅我们的博文。
## Chrome 132：Tabs API 中的新冻结属性
从 Chrome 132 开始，Tabs API 中的 frozen 属性用于指示标签页是否已被浏览器冻结。发送到冻结标签页的消息将排队，并在标签页解除冻结状态后进行处理。
## Chrome 扩展程序中的 Prompt API
扩展程序专用 Prompt API 现已在初始版本试用中推出，因此您可以在浏览器中构建使用 Gemini Nano（我们最高效的语言模型）的 Chrome 扩展程序。
加入 Prompt API 源试用（在 Chrome 131 至 136 中运行），并分享您的反馈。您的反馈可以直接影响我们构建和实现此 API 及所有内置 AI API 的未来版本的方式。
## 博文：2024 年 10 月 Chrome 扩展程序的最新动态
又到了盘点 Chrome 扩展程序最新动态的时候了：我们在 AI 集成、新 API、活动和视频方面都有令人兴奋的更新。如需了解详情，请参阅 Chrome 扩展程序 10 月刊！
## 加入内置 AI 挑战
Chrome 推出了内置 AI 挑战赛：诚邀您使用 Chrome 的集成式 AI 模型和 API 创建创新型 Web 应用和 Chrome 扩展程序，赢取总计 65,000 美元的奖品。
如需注册并详细了解相关信息，请访问 Built-in AI Challenge 网站。我们迫不及待地想看看您在为网络注入 AI 后会创作出什么作品！
## Chrome 130：action.onUserSettingsChanged
从 Chrome 130 开始，action.onUserSettingsChanged 事件可用。这是根据 WebExtensions 社区组中的提案实现的。感谢 Microsoft 为 Chromium 做出的贡献。
## Chrome 130：StorageArea.getKeys()
从 Chrome 130 开始，getKeys() 方法可在 chrome.storage API 使用的 StorageArea 接口上使用。这是根据 WebExtensions 社区组中的提案实现的。
## Chrome 128：声明式网络请求中的响应标头匹配
从 Chrome 128 开始，我们将在 Declarative Net Request API 中添加对响应标头匹配的支持。这是一个常见的要求，尤其是在匹配 Content-Type 标头时，我们与 WebExtensions 社区组一起设计了一个合适的 API。
我们已更新 API 参考文档，以纳入新的 responseHeaders 和 excludedResponseHeaders 字段。您可以使用这些方法来检查指定标头的存在情况和值。
在此次更新中，我们向文档添加了一个新的规则评估部分，其中介绍了规则的匹配方式。对于标头匹配，规则只能在收到响应标头后运行，因此它们的应用阶段比其他规则晚。这意味着，请求在被屏蔽或重定向之前确实到达了服务器。
## 视频：什么是内容脚本？
了解 Chrome 扩展程序中的内容脚本，包括如何注册 CSS 和 JavaScript 以在特定网页上运行。观看完整视频。
## 重要政策更新
Chrome 应用商店团队发布了一系列更新，对开发者计划政策页面进行了修改，旨在鼓励开发高质量的产品、防止欺骗性行为，并确保用户在知情的情况下同意。Chrome 应用商店政策经理 Rebecca Soares 在 Chrome 扩展程序：重要政策更新这篇博文中总结了所有更新。
## 博文：Chrome 扩展程序的最新动态，2024 年 7 月
在过去三个月内，我们推出了一些重大更新和新功能，包括开始逐步淘汰清单 V2。快来了解 Chrome 扩展程序 7 月版中的新变化！
## 视频：什么是远程托管代码？
Chrome 扩展程序团队的 Patrick 介绍了 Chrome 扩展程序中远程托管代码 (RHC) 的概念。了解为何不再允许使用 RHC、如何检测 RHC，以及如果您的扩展程序需要更新，该怎么做。观看完整视频。
## Chrome 127：新增了 action.openPopup API
从 Chrome 127 开始，所有扩展程序都可以使用 action.openPopup API。以前，它仅在 Canary 中提供，或仅适用于根据政策安装的扩展程序。
Chrome 扩展程序开发者关系团队与负责 Chrome 应用商店审核的信任与安全团队进行了交流，询问了您提出的问题。观看完整视频。
## 博文：Manifest V2 淘汰阶段即将开始
从 6 月 3 日开始，在 Chrome Beta 版、Dev 版和 Canary 版渠道中，如果用户仍安装了 Manifest V2 扩展程序，那么当他们访问扩展程序管理页面 (chrome://extensions) 时，部分用户会开始看到警告横幅，告知他们所安装的部分（Manifest V2）扩展程序很快将不再受支持。如需了解详情，请参阅官方公告
我们最近对侧边栏界面进行了一些更改，包括添加了固定图标并移除了全局侧边栏图标。如需了解详情，请参阅公告，并查看我们更新的文档和示例。
## 博文：2024 年 Google I/O 大会上的 Chrome 扩展程序
又一届 Google I/O 大会已经结束，我们报道了所有令人兴奋的扩展程序更新！前往 YouTube 观看完整视频，并阅读我们的博文，了解一些精彩内容。
## 跳过对符合条件的声明式网络请求变更的审核
现在，当您使用 Declarative Net Request API 时，Chrome 应用商店允许您跳过对符合条件的更改的审核。如需详细了解资格要求以及如何选择启用，请参阅 Chrome 应用商店文档。
## Chrome 应用商店 API 中提供的 deployPercentage
我们最近更新了 Chrome 应用商店 API 文档，其中包含有关 deployPercentage 的信息。借助该功能，您可以分配部分发布部署的百分比。了解 deployPercentage。
## Chrome 126：扩展程序中的源试用
Chrome 126 引入了一个新的 manifest.json 字段 - trial_tokens，让您可以在所有扩展程序界面中选择加入源试用和弃用试用。如需了解详情，请参阅指南。
## 博文：Chrome 扩展程序的最新动态 - 2024 年 4 月
我们发布了新一期Chrome 扩展程序动态。该帖子讨论了扩展程序团队在过去几个月中的工作。这包括：Chrome 应用商店中的版本回滚、更好的 Firebase Auth 支持，以及更多 API 发布和更新。
## Chrome 应用商店开发者信息中心中的版本回滚
将扩展程序回滚到 Chrome 应用商店中之前发布的版本，无需额外审核！如需了解详情，请参阅这篇博文和文档。
## Chrome 124：高级 documentScan API
ChromeOS 上现已提供高级 documentScan API，用于发现和检索连接的文档扫描仪中的图片。
## Chrome 124：在 Service Worker 中支持 WebGPU
自 Chrome 124 起，服务工作线程支持 WebGPU。如需快速入门，请查看 WebGPU 扩展程序示例。
## Chrome 123：Events API 支持按 CIDR 块进行过滤
Events API 现在支持按无类别域间路由 (CIDR) 区块进行过滤。CIDR 块是指共享相同网络前缀和相同位数的 IP 地址集合。以前，如果开发者需要过滤多个 IP 地址，则需要为屏蔽范围内的每个地址配置过滤规则。现在，当扩展程序调用 addListener() 时，传入的规则意味着只有当网址的主机部分是 IP 地址且包含在数组中指定的任何 CIDR 块中时，才会调用事件处理脚本。
## Chrome 应用商店：扩展程序名称长度要求更新
在 Chrome 应用商店中，清单文件 (manifest.json) 的 "name" 字段现在有 75 个字符的通用限制。之前，英文的限制为 45 个字符，其他语言区域的 "name" 字段没有限制。
此功能最初旨在允许存在文化和语言差异，而这些差异可能无法用相同数量的字符来表达。遗憾的是，一小部分开发者滥用了此功能，向商店发送垃圾内容。因此，我们推出了新的通用限制，将字符数上限提高到 75 个。 此限制涵盖了目前商店中的几乎所有扩展程序，因此您很可能无需因这一变化而采取任何行动。如果您尝试上传的扩展程序的名称超过了上限，商店会阻止上传。
在 eyeo 的扩展程序引擎团队的这篇博文中，我们将探讨测试扩展程序服务工作线程的问题。在 Manifest V2 中，扩展程序位于后台网页中，在整个扩展程序生命周期内都处于唤醒状态。Manifest V3 使用的是服务工作器，而服务工作器在不需要时会关闭，从而节省资源。这会带来一定的测试挑战。这篇博文介绍了 eyeo 如何应对这些挑战。
## Chrome 123：闹钟现在可在设备处于休眠状态时运行
当设备进入休眠状态时，使用 chrome.alarms API 设置的闹钟不再延迟。当设备唤醒时，无论错过了多少个闹钟，闹钟都会响一次。例如，假设闹钟设置为每小时响一次，而设备在凌晨 12:55 到凌晨 2:05 处于休眠状态，那么只有凌晨 2:00 的闹钟会触发 onAlarm 事件。它会在尽可能接近凌晨 2:00 时触发，如果设备处于休眠状态，则会在设备唤醒时立即触发。
此更改使 Chrome 符合 Web 扩展程序社区组中达成的共识。
## 博文：扩展程序消息端口对 bfcache 行为的更改
往返缓存 (bfcache) 是一种浏览器优化，可实现即时后退和前进导航。从 Chrome 123 开始，当具有开放扩展程序端口的网页存储在 bfcache 中时，消息渠道会关闭，这意味着不会向该网页发送任何消息。因此，扩展程序脚本应监听 onDisconnect 等生命周期事件，并在网页从 BFCache 恢复时设置新连接。
如需了解详情和查看示例代码，请参阅扩展消息端口对 BFCache 行为的更改。
## Chrome 122：异步扩展程序 API 中的 Promise 支持
我们已完成为所有异步扩展 API 方法实现 Promise 支持。这样做是为了通过改进处理异步操作的人体工程学来使 API 方法现代化。少数方法（例如 desktopCapture.chooseDesktopMedia()）仍仅支持回调，因为其当前界面与 Promise 不兼容。为了实现向后兼容性，系统仍支持回调。如果您发现 Promise 失败，请提交 bug 报告。
我们刚刚发布了有关扩展程序中实时选项的指南。实时更新可提供从服务器直接到扩展程序安装的即时通信路径。此外，我们还针对使用 chrome.gcm、Web 推送提供了新的指南。
## 新指南和示例：测试 Service Worker 终止
我们刚刚发布了一篇指南，介绍了如何使用 Puppeteer 测试 Service Worker 终止。随附的示例在 Puppeteer 和 Selenium 中演示了这一点。
## 更新了原生消息传递的示例
我们刚刚发布了原生消息的更新版示例。此 API 可让您的扩展程序启动其他应用并与之通信。感谢 GitHub 贡献者 Shubham-Rasal 为此做出的贡献。
## Chrome 121：为 tabs.Tab 新增了 lastAccessed 属性
向 tabs.Tab 对象添加了一个名为 lastAccessed 的新属性。此属性表示标签页上次处于活动状态的时间。返回的值以毫秒为单位，从纪元起算。
## Chrome 121：不支持的“background”键现在会发出警告
在从 Manifest V2 更改为 Manifest V3 的过程中，"background" 清单键的子项发生了更改，以适应将后台脚本替换为扩展程序服务工作线程。以前，如果将 Manifest V2 键 "scripts"、"page" 或 "persistent" 添加到 Manifest V3 扩展程序的 "background" 键中，系统会抛出错误。现在，如果存在这些键，系统会触发警告。
这样做是为了能够按照社区组中的提案，在多个浏览器中的扩展程序中使用单个清单文件。
## Chrome 120：将最低闹钟粒度缩短为 30 秒
从 Chrome 120 开始，Manifest V3 扩展程序可以使用延迟时间或周期为 30 秒的 chrome.alarms API，而不再要求延迟时间或周期为 60 秒或更长时间。
## 博文：继续向 Manifest V3 过渡
Manifest V2 支持时间表已更新。如需了解详情，请参阅我们的2023 年 11 月份的博文。
## 博文：Manifest V3 中内容过滤支持方面的改进
如需了解我们如何在这篇新博文中改进 declarativeNetRequest API，请参阅该博文。
## 博文：Chrome 120 中针对扩展程序的新变化
Chrome 120 Beta 版已于最近发布。如需简要了解与扩展程序开发者相关的重要更新，请参阅我们的新博文：Chrome 120 中的扩展程序新功能。此版本还标志着一个重要里程碑，因为它从关键平台差距列表中移除了最后两项（userScripts、ChromeOS 上的文件处理程序）。
## 公告：开发者信息中心内隐私权政策网址的处理方式发生变化
开发者信息中心内的隐私权政策现在是在商品级别添加的。这样，您就可以为每个商品提供不同的隐私权政策。如需详细了解此变更，请参阅我们的PSA。
## 视频：与 Matt Frisbie 的对话
我们刚刚在 Chrome for Developers YouTube 频道上发布了一段新视频，其中与 Google 开发者专家兼作者 Matt Frisbie 进行了对话。点击此处观看。
## 有关测试扩展程序的新指南
我们刚刚发布了有关如何为扩展程序编写自动化测试的新指南，包括如何编写单元测试，以及有关端到端测试的一般指南和教程。
## 博文：Chrome 扩展程序动态 - 2023 年 10 月
我们刚刚发布了第二期Chrome 扩展程序动态。这篇博文讨论了扩展程序团队在过去几个月内所做的工作，包括解决服务工作线程稳定性问题，以及在弥合所有 MV3 平台差距方面取得的良好进展。我们还分享了即将发布的令人期待的 API，例如 Reading List API 和 User Scripts API。
## 增加了声明式网络请求 API 中的静态规则集限制
根据 Web Extensions 社区组中的反馈，我们将启用静态规则集的数量上限从 10 大幅提高到 50。此外，我们将允许的静态规则集总数从 50 个增加到 100 个。此功能目前已在 Canary 中推出。
## 改进了有关远程托管代码的指南
Manifest V3 的一项要求是，扩展程序不得再使用远程托管的代码。虽然这从一开始就包含在我们的迁移指南中，但我们认为有必要改进有关此问题的指南。该页面现在提供了更多信息，介绍了在 Manifest V3 中仍然可以执行的操作，并提供了有关升级策略的更多信息。
我们还对排查 Chrome 应用商店违规行为添加了相关内容。新增了一个部分，介绍了具有远程托管代码的扩展程序遭拒的常见原因。
## Chrome 118：isUrlFilterCaseSensitive 现在默认设置为 false
从 Chrome 118 开始，chrome.declarativeNetRequest API 中的 isUrlFilterCaseSensitive 属性已更改为默认使用 false。如果您希望保留旧行为，可以在 declarativeNetRequest 规则中将 isUrlFilterCaseSensitive 明确设置为 true。
这遵循了 Web Extensions 社区群组中的讨论。Firefox 和 Safari 已经实施了类似的更改。
## 有关 Cookie 和 Web 存储 API 的文档
我们发布了一份新指南，介绍了 Cookie 和 Web 存储 API 在 Chrome 扩展程序中的运作方式。其中包含有关 Privacy Sandbox 中 Cookie 和存储分区变更的详细信息。Privacy Sandbox 是一个正在进行的项目，旨在通过创建一系列新的 Web 平台 API 来弃用第三方 Cookie，并详细说明这些 API 在扩展程序中的运作方式。
## 现在可以搜索扩展程序示例了
我们最近创建了一个页面，可让您搜索 Chrome 扩展程序示例。搜索页面上有多个选项。您可以使用搜索框搜索示例标题中的文字。您可以按权限或扩展程序 API 限制搜索范围。借助其他过滤条件，您可以将搜索范围限制为 API 或功能（使用情形）示例。
这个新示例网页由 Google Summer of Code 参与者薛舟戴构建，他还贡献了多个新示例。您可以在我们的博客上查看他们的博文，了解他们去年夏天的经历。
与之前一样，您仍然可以在 GitHub 上克隆或派生我们的代码示例。
## Chrome 118：对打开文件方案网址的更改
从 Chrome 118 开始，扩展程序需要从 chrome://extensions 页面启用“允许访问文件网址”设置，才能使用 Tabs 或 Windows API 打开 file:// 方案网址。您可以通过调用 chrome.extension.isAllowedFileSchemeAccess() 以编程方式检查此访问权限。Firefox 已经限制了文件网址，Safari 也支持这项更改。如需了解详情，请参阅 Chrome 扩展程序邮寄名单中的帖子。
## Chrome 117：扩展了对扩展程序 API 导航的网址保护
之前，通过扩展程序 API 调用触发的针对 tabs.update()、tabs.create() 和 windows.create() 的导航会针对某些 chrome:// 网址发出错误。此外，禁止使用 JavaScript 网址调用 tabs.update()。在 117 中，这些针对 JavaScript 网址的保护措施已扩展到 tabs.create() 方法，并且已将许多其他 chrome:// 网址添加到禁止的网址列表中，该列表适用于上述所有方法。
chrome.declarativeNetRequest API 通过指定声明式规则来阻止或修改网络请求。这样一来，扩展程序就可以修改网络请求，而无需拦截这些请求并查看其内容，从而为用户提供更高的隐私保护。而且使用起来也很棘手。鉴于此，我们重写了相关指南，以便更清晰地说明如何实现声明性规则集。请点击上方的链接，阅读新部分。
## 将您的 Google Analytics 账号与 Chrome 应用商店搭配使用
Chrome 应用商店与 Google Analytics 集成，因此除了开发者信息中心提供的视图之外，您还可以查看 Chrome 应用商店商品详情的分析数据。如需了解详情，请参阅将 Google Analytics 账号与 Chrome 应用商店搭配使用。
## Chrome 115：开发者工具默认跳过内容脚本
注入的内容脚本现在默认位于开发者工具的忽略列表中。这不会影响断点，但意味着在调试期间，系统会跳过内容脚本，并忽略这些脚本中的异常。当内容脚本在 Sources 标签页中打开时，如果此功能处于开启状态，系统会显示一个横幅提醒您，并提供用于从忽略列表中移除内容脚本的选项。如需关闭此行为，请打开开发者工具，前往设置，然后前往忽略列表。如需了解详情，请参阅开发者工具的新变化。
## Chrome 116 Beta 版：功能非常丰富，此处无法一一列举
Chrome 116 是一个重要的扩展程序版本。您现在可以以编程方式打开侧边栏。借助一种新方法，您可以了解是否存在有效的屏幕外文档。Service Worker 得到了多项改进。116 版中包含的改进非常多，我们专门撰写了一篇博文来介绍这些改进。截至 7 月 19 日，Chrome 116 处于 Beta 版阶段。
## 博文：Chrome 扩展程序方面的最新动态
我们刚刚发布了有关今年扩展程序变更和改进的概览。该博文讨论了本年度的新功能，包括侧边栏 API、Service Worker 增强功能和屏幕外文档。您还可以了解我们本季度正在开展的工作。该文章列出了更多内容，并提供了指向所有内容的链接。
## 新指南和示例：了解如何在 Chrome 扩展程序中使用 Google Analytics 4
我们发布了新的 Google Analytics 和地理定位指南及示例：
- 更新后的 Google Analytics 指南，说明了如何在 Chrome 扩展程序中使用 Google Analytics 4。我们还在 GitHub 示例代码库中添加了一个可正常运行的 Google Analytics 4 示例。如需查看与 Google Analytics 相关的代码，请参阅 google-analytics.js。
- 新的地理定位指南和三个示例，演示了如何在服务工作线程、内容脚本、弹出式窗口和侧边栏中访问地理定位信息。
## Chrome 115：在 chrome.offscreen.createDocument() 中指定多个原因
现在，您可以在调用 chrome.offscreen.createDocument() 时指定多个 reason 枚举。当屏幕外文档将用于多种不同用途时，请使用此值。浏览器会使用提供的原因来确定屏幕外文档的生命周期。
## 新工具：扩展程序更新测试工具
我们刚刚发布了扩展程序更新测试工具，这是一个本地扩展程序更新服务器，可在本地开发期间用于测试 Chrome 扩展程序的更新，包括权限授予。该工具会显示用户的更新流程，包括在用户授予任何新请求的权限之前，保持扩展程序处于停用状态。此工具特别适合用于模拟将扩展程序从 Manifest V2 更新到 Manifest V3 时所请求的权限变更。
## Chrome 114：新的 Side Panel API
我们推出了新的 Side Panel API，这是一个配套界面，可让用户在浏览内容的同时访问工具。如需了解详情，请参阅边栏 API 参考文档。此外，我们还在 GitHub 示例代码库中添加了许多侧边栏示例。我们还在新博文利用新的边栏 API 设计出色的用户体验中详细介绍了边栏。我们还审核了质量指南政策和最佳实践，以便为创建高质量的侧边栏扩展程序提供更多指导。
您的反馈对于打造此 API 至关重要；请在 chromium-groups 中分享您的想法和功能请求。我们会继续改进侧边栏 API，敬请关注最新动态。
## 新示例：扩展程序中的 WASM
现在有两个新示例可供使用，它们演示了如何在扩展程序中使用 WASM：
- 在 Manifest V3 中将 WASM 用作模块介绍了如何在模块中使用 WASM。
特别感谢 GitHub 贡献者 @daidr 提供这些示例。
## 更新了 Manifest V3 迁移指南
我们更新了 Manifest V3 迁移指南的已知问题部分，其中包含一份更新后的扩展平台差距列表，我们计划在宣布新的 Manifest V2 弃用时间表之前弥合这些差距。
## 使用清单 V3 录制音频和视频
我们刚刚发布了一篇新文章，名为音频录制和屏幕捕获，其中介绍了如何在 Manifest V3 中录制标签页、窗口或屏幕中的音频或视频。本文介绍了涉及 chrome.tabCapture API 和 getDisplayMedia() 函数的多种录制方法。
## Chrome 114：提高了 storage.local 配额
我们已将 storage.local 属性的配额增加到大约 10 MB。这一点已在 Web 扩展程序社区群组中达成一致。这使得 storage.local 与 Chrome 112 中更改的 storage.session 保持一致。
## 新的扩展程序服务工作线程教程和帮助
Service Worker 是 Chrome 扩展程序不可或缺的一部分。我们刚刚发布了一篇教程，介绍了注册、调试和与 Service Worker 互动的基础知识。我们还添加了新的 Service worker 指南，其中更详细地介绍了重要概念。我们将在未来几个月内扩充此部分的内容。
## 有关 Web 应用商店违规问题的更多问题排查提示
为了帮助您在 Chrome 应用商店中发布内容，我们在以下两个方面添加了新的指导。有关最基本的功能的指南侧重于为用户提供益处并丰富其浏览体验。联属营销广告指南旨在让用户了解广告客户使用联属营销链接或代码创收的扩展服务，并通过要求用户在添加之前执行操作来赋予用户一定程度的控制权。
## 针对扩展程序清单转换器的新说明
我们重写了扩展程序清单转换器的 README，以便您更轻松地了解运行该工具后需要执行的操作。该转换器可帮助将基于 Manifest V2 构建的扩展程序迁移到 Manifest V3。新版 README 使用与迁移指南的清单中非常相似的字词描述了该工具的功能。转换器并非万能，但确实可以省去许多不需要人工判断的任务。
## Chrome 113：新增了离屏文档的原因
我们已向 Offscreen Documents API 添加了两种新的原因类型。使用 LOCAL_STORAGE 访问 Web 平台的 localStorage API。创建 Web 工作器时使用 WORKER。
## Google Analytics 4 现已在开发者信息中心内提供
Chrome 应用商店开发者信息中心现已支持 Google Analytics 4 (GA4)。我们简化了 Google Analytics 的设置流程，并使群组发布商的访问权限管理更加简单明了。如果您之前使用 Google Universal Analytics 跟踪商店详情活动，则需要在 2023 年 7 月 1 日之前采取行动，以确保您能继续接收有关商店详情的数据。如需了解详情，请参阅 Chrome 扩展程序邮寄名单中的帖子。
## File Handling API 登陆 ChromeOS
文件处理程序 API 可在 ChromeOS Canary 版中进行实验，适用于 112 和 113 版。它允许 ChromeOS 上的扩展程序打开具有指定 MIME 类型和文件扩展名的文件。如需实现文件处理，请向 manifest.json 添加一组规则。此功能的工作方式与渐进式 Web 应用相同。如需了解详情，请参阅本网站上的这篇文章。
如需启用文件处理，请执行以下操作：
- 从 112 开始，使用 -enable-features=ExtensionWebFileHandlers 标志启动 Chrome，从 112 开始
- 从 113 版开始，将 os://flags/#extension-web-file-handlers 粘贴到 Chrome 多功能框中，然后从下拉菜单中选择“启用”。
我们希望在 6 月下旬推出 Chrome 115 时发布此功能。请关注此空间，了解最新动态。
## 新示例：动态声明和程序化注入
我们为 chrome.scripting API 构建了一个新示例。它演示了动态声明（在运行时注册内容脚本）和程序化注入（在已打开的标签页中执行脚本）。
## 新示例：声明式网络请求使用情形
我们提供了三个新示例，用于演示声明式网络请求 API。每个示例都演示了单个用例的实现。第一个示例展示了如何屏蔽 Cookie。其余两个演示了如何屏蔽和重定向网址。
## Chrome 112：增加了 storage.session 配额
自 Chrome 112 起，storage.session 属性的配额已增加到大约 10 MB。Web 扩展程序社区群组已就此达成一致意见：https://github.com/w3c/webextensions/issues/350
## Chrome 109：屏幕外文档
屏幕外文档现已在 Manifest V3 扩展程序中提供。这些 API 可支持与 DOM 相关的功能和 API，从而帮助实现从后台网页到扩展程序服务工作线程的过渡。如需了解详情，请阅读此博文。
## Chrome 110：扩展程序是否已启用
chrome.action.isEnabled() 方法以编程方式检查是否已为特定标签页启用扩展程序。这样一来，您就无需维护标签页的启用状态。此新方法接受标签页 ID 和对回调的引用，并返回一个布尔值。但它有一个限制：使用 chrome.declarativeContent 创建的标签页始终返回 false。
（chrome.action 命名空间最近新增了一些用于控制扩展程序徽章外观的方法。如需了解详情，请参阅设置徽章颜色。）
## Chrome 110：Service Worker 空闲超时时间发生变化
以前，扩展程序服务工作线程通常会在 5 分钟时关闭。我们已更改此行为，使其更接近于 Web 上的 service worker 生命周期。扩展程序服务工作线程会在处于非活动状态 30 秒后关闭，或者在单个活动的处理时间超过 5 分钟时关闭。如需了解详情，请参阅延长扩展服务工作器的生命周期。
## 帖子：暂停 Manifest V2 淘汰计划
我们正在审核 Manifest V2 弃用时间表，并推迟原定于 2023 年初进行的实验。如需了解详情，请阅读 Chrome 扩展程序邮寄名单中的更新。
## Chrome 110：设置徽章颜色
chrome.action 命名空间新增了两种方法，可让您更好地控制外观扩展程序徽章。setBadgeTextColor() 和 getBadgeTextColor() 方法允许扩展程序更改和查询其工具栏图标的徽章文本颜色。与 setBadgeBackgroundColor 和 getBadgeBackgroundColor 搭配使用时，这些新方法可让您强制保持设计和品牌的一致性。
## 博文：详细了解向 Manifest V3 的过渡
我们明确了 Manifest V2 弃用时间表。我们还更新了 Manifest V2 支持时间表，以反映此信息。
## 文档更新：迁移到 Manifest V3 时遇到的已知问题
我们整理了一份目前正在开发中的主要功能和公开 bug 的列表。我们希望通过此页面帮助开发者更好地了解平台的当前状态，以及在为未来做准备时可以考虑哪些功能。
## Chrome 应用商店：已移除“大型宣传块”图片上传功能
Chrome 应用商店已从开发者信息中心的商品详情标签页中移除了“大型宣传块”上传界面。此更改不会影响最终用户体验，因为这些图片未在消费者界面中使用。如需了解详情，请参阅这篇关于 chromium-extensions 的帖子。
## Chrome 106：允许 file:// 网址上的网页访问可从网络访问的资源
根据 crbug.com/1219825#c11，不透明源（例如沙盒 iframe 和动态导入）也应该能够访问可通过网络访问的资源。
## Chrome 106：修复了允许在某些异步 API 函数上使用错误最终实参的 bug
之前，调用异步 API 的 Manifest V3 可以提供无效的最终实参，而 Chrome 不会出错。通过此修复，Chrome 现在可以正确报告错误，并指出没有匹配的签名。建议开发者在 Canary 上检查其扩展程序是否存在任何错误，以免因意外使用错误的签名进行 API 调用而导致此 bug 修复破坏扩展程序。
## 博文：Chrome 应用商店分析功能改版
Chrome 应用商店为 Chrome 应用商店开发者信息中心推出了经过改进的商品分析体验。新信息中心更易于一目了然地了解，并且会预先整合最有用的信息。如需了解详情，请阅读这篇博文。
## Chrome 105：Identity API 的 promise
Identity API 上的函数现在支持基于 Promise 的调用。这会略微改变 identity.getAuthToken() 的界面，其中设置为基于 Promise 的调用的异步返回将具有“token”和“grantedScopes”作为单个对象上的参数（而不是回调版本将它们作为单独的实参接收到回调中）。
## Chrome 104：适用于 Manifest V3 的新 favicon API
Manifest V3 扩展程序现在可以使用新的网址格式 chrome-extension://<id>/_favicon/ 访问收藏夹图标，其中  是扩展程序的 ID。这取代了 Manifest V2 平台的 chrome://favicons API。如需了解详情，请参阅 Favicon API 文档。
## 文档更新：开发者交易者/非交易者信息披露
添加了交易者/非交易者开发者身份标识，可提醒开发者准确自行声明其交易者/非交易者状态。
## Chrome 103：Manifest V3 中的 Wasm 需要 wasm-unsafe-eval
Chrome 不再默认向扩展程序授予 script-src: wasm-unsafe-eval。使用 WebAssembly 的扩展程序现在必须在其 content_security_policy 声明中明确添加此指令和值到 extension_pages。
## Chrome 103：更改 MV3 快捷键会立即生效
在 chrome://extensions/shortcuts 上更改 Manifest V3 扩展程序的键盘快捷键时，更新现在会立即应用。之前，必须重新加载扩展程序，更改才会生效。
## Chrome 102：主世界中的动态内容脚本
动态注册的内容脚本现在可以指定要将资源注入到的 world。如需了解详情，请参阅 scripting.registerContentScripts()。
## Chrome 102：新的清单字段“optional_host_permissions”
Manifest V3 扩展程序现在可以在 manifest.json 中指定 optional_host_permissions 键。这样一来，Manifest V3 扩展程序就可以像 Manifest V2 扩展程序那样，使用 optional_permissions 键来声明主机的可选匹配模式。
## Chrome 102：scripting.executeScript() 中的 injectImmediately 属性
chrome.scripting.executeScript() 现在接受其 injection 实参中的可选 injectImmediately 属性。如果存在且设置为 true，脚本将尽快注入到目标中，而不是等待 document_idle。请注意，这并不能保证脚本会在网页加载之前注入，因为在进行 API 调用时，网页会继续加载。
## Chrome 102：Manifest V3 中的多功能框 API 支持
现在，基于 Service Worker 的扩展程序可以使用 Omnibox API。之前，由于内部依赖于 DOM 功能，此 API 的某些方法会在调用时抛出异常。
## Chrome 102：允许在 Manifest V3 CSP 中使用 wasm-unsafe-eval
Manifest V3 扩展程序现在可以在其 content_security_policy 声明中包含 wasm-unsafe-eval。此变更允许 Manifest V3 扩展程序使用 WebAssembly。
## Chrome 102：新的 storage.session API
Manifest V3 扩展程序现在可以使用内存存储空间 storage.session。
## 文档更新：Chrome 应用商店商品发现
在 Chrome 应用商店中发现内容一文概述了用户如何在 Chrome 应用商店中查找商品，以及我们的编辑如何选择要重点展示的商品。
## Chrome 101：改进了 declarativeNetRequest 网域条件
更新了 declarativeNetRequest 规则条件，以允许扩展程序根据请求的“request”和“initiator”网域更好地定位请求。相关的条件属性为 initiatorDomains、excludedInitiatorDomains、requestDomains 和 excludedRequestDomains。另请参阅此 chromium-extensions 帖子。
## Chrome 100：修复了新创建的标签页上 scripting.executeScript() 的问题
修复了在新建的标签页或窗口上调用 scripting.executeScript() 可能会失败的长期存在的问题。
## Chrome 100：原生消息传递端口可使 Service Worker 保持活跃状态
警告：此更改并未完全解决根本问题。当我们确信原生消息传递端口的行为符合预期时，我们会分享另一条更新。
在扩展程序的服务工作器中使用 chrome.runtime.connectNative() 连接到原生消息传递主机应使服务工作器在端口打开期间保持活跃状态。
## Chrome 100：omnibox.setDefaultSuggestion() 支持 promise 和回调
omnibox.setDefaultSuggestion() 方法现在会返回一个 promise 或接受一个回调，以允许开发者确定建议何时已正确设置。
## Chrome 100：在扩展程序服务工作线程中支持 i18n.getMessage()
扩展程序服务工作线程上下文现在支持 chrome.i18n.getMessage() API。
## Chrome 99：Canary 版中的 match_origin_as_fallback
内容脚本现在可以指定 match_origin_as_fallback 键，以注入到与匹配框架相关的框架中，包括具有 about:、data:、blob: 和 filesystem: 网址的框架。如需了解详情，请参阅内容脚本文档。
## Chrome 99：Canary 版中针对 file: 方案的扩展程序服务工作线程支持
基于 Service Worker 的 Manifest V2 和 Manifest V3 扩展程序现在可以使用 Fetch API 请求 file: 方案网址。访问 file: 方案网址仍需要用户在 chrome://extensions 页面中为扩展程序启用“允许访问文件网址”。
## Chrome 99：在 Canary 版中为消息传递 API 提供 Promise 支持
为基于 Manifest V3 构建的扩展程序向 tabs.sendMessage、runtime.sendMessage 和 runtime.sendNativeMessage 添加了 Promise 支持。
## Google 文档更新：Chrome 应用商店审核文档
添加了新参考页面，其中概述了 Chrome 应用商店审核流程，并说明了如何处理开发者计划政策的违规行为。
## Chrome 98：scripting.executeScript() 和 scripting.insertCSS() 接受多个文件
脚本 API 的 executeScript() 和 insertCSS() 方法现在接受多个文件。以前，这些方法需要包含单个文件条目的数组。
## 文档更新：查看违规问题排查更新
我们更新了排查 Chrome 应用商店违规行为页面，为开发者提供了有关常见拒绝原因的更详细指导。
## Chrome 96：将 Promise 支持范围扩大到另外 27 个 API
此版本包含的 promise 更新明显多于任何之前的版本。更新包括常规扩展程序 API 和 ChromeOS 专用扩展程序 API。展开即可下部分即可查看详细信息。
扩展程序 API
许多 API 现在在清单 V3 中支持 Promise。
此外，使用 ChromeSetting 原型的 API 现在也支持 promise。以下 API 会受到此变更的影响。
ChromeOS API
## Chrome 96：动态内容脚本
chrome.scripting API 现在支持在运行时注册、更新、取消注册和获取列表内容脚本。以前，内容脚本只能在扩展程序的 manifest.json 中静态声明，或者在运行时通过 chrome.scripting.executeScript() 以编程方式注入。
## 文档更新：Manifest V2 支持时间表
这篇博文中公布了从 Manifest V2 到 V3 的过渡时间表，并发布了更详细的时间表页面。
## Chrome 96：declarativeNetRequestWithHostAccess 权限
借助新的 declarativeNetRequestWithHostAccess 权限，扩展程序可以在具有主机权限的网站上使用 chrome.declarativeNetRequest API。这还使使用 webRequest、webRequestBlocking 和特定于网站的主机权限的现有 Manifest V2 扩展程序能够迁移到 chrome.declarativeNetRequest API，而无需用户批准新权限。
## Chrome 95：直接将脚本注入网页
chrome.scripting API 的 executeScript() 方法现在可以直接将脚本注入到网页的主世界中。以前，扩展程序只能直接注入到扩展程序的隔离世界中。如需详细了解隔离的世界，请参阅有关内容脚本的文档。
## Chrome 95：为 Storage API 提供 Promise 支持
Manifest V3 版 chrome.storage API 中的方法现在会返回 promise。
## 政策更新：强制执行两步验证
我们已更新 2021 年 6 月 29 日发布的政策更新博文，以更正两步验证部署时间表。
## Chrome 94：声明性网络请求静态规则集变更
chrome.declarativeNetRequest 现在支持指定最多 50 个静态规则集 (MAX_NUMBER_OF_STATIC_RULESETS)，并同时启用最多 10 个规则集 (MAX_NUMBER_OF_ENABLED_STATIC_RULESETS)。
## Chrome 93：支持跨源隔离
现在，Manifest V2 和 Manifest V3 扩展程序都可以选择启用跨源隔离。此功能可限制哪些跨源资源可以加载扩展程序的网页，并支持使用 SharedArrayBuffer 等低级 Web 平台功能。从 Chrome 95 版开始，必须选择启用。
## 政策更新：开发者计划政策已更新
我们更新了 Chrome 应用商店开发者计划政策，对欺骗性安装策略、垃圾内容和重复性内容政策进行了阐明。 此更新还新增了一项要求，即必须进行两步验证才能在 Chrome 应用商店中发布内容。如需了解详情，请阅读这篇博文。
## 博文：Manifest V3 中的扩展程序操作
Chrome 扩展程序多年来一直使用 chrome.browserAction 和 chrome.pageActions API，但 Manifest V3 将两者都替换为通用的 chrome.actions API。这篇博文探讨了这些 API 的历史记录以及 Manifest V3 中的变化。阅读博文。
chrome.scripting API 是一种新的 Manifest V3 API，专注于脚本。在这篇博文中，我们将深入探讨这项变更背后的动机，并仔细了解其新功能。阅读博文。
## Chrome 92：模块服务工作线程支持
Chrome 现在支持在服务工作线程中使用 JavaScript 模块。如需在清单中指定模块，请执行以下操作：
```plain text
"background": {
  "service_worker": "script.js",
  "type": "module"
}

```
这会将 worker 脚本加载为 ES 模块，从而让您可以在 worker 的脚本中使用 import 关键字来导入其他模块。
## Chrome 91：chrome.action.getUserSettings()
新的 chrome.action.getUserSettings() 方法允许扩展程序确定用户是否已将扩展程序固定到主工具栏。
## Chrome 90：chrome.scripting.removeCSS()
新的 chrome.scripting.removeCSS() 方法允许扩展程序移除之前通过 chrome.scripting.insertCSS() 插入的 CSS。它取代了 chrome.tabs.removeCSS()。
## Chrome 90：从 scripting.executeScript() 返回 promise
chrome.scripting.executeScript() 现在支持返回 promise。如果脚本执行的最终值是 Promise，Chrome 会等待 Promise 得到解决，并返回其最终值。
## Chrome 90：chrome.scripting.executeScript() 结果包含 frameId
从 chrome.scripting.executeScript() 返回的结果现在包含 frameId。frameId 属性用于指明结果来自哪个框架，以便扩展程序在多个框架中注入时轻松将结果与各个框架相关联。
## Chrome 89：用于管理标签页分组的新 API
新的 chrome.tabGroups API 和 chrome.tabs 中的新功能可让扩展程序读取和操纵标签页组。 需要使用 Manifest V3。
## Chrome 89：可自定义的 Web 可访问资源权限
Manifest V3 中的可供 Web 访问的资源定义已更改，以便扩展程序根据请求者的来源或扩展程序 ID 限制资源访问权限。
## 博文：扩展程序清单转换器
Chrome 扩展程序团队已开源“扩展程序清单转换器”，这是一款 Python 工具，可自动执行将扩展程序转换为 Manifest V3 的部分机械性工作。请参阅公告博文，并从 GitHub 获取。
## Chrome 88：Manifest V3 正式版
Manifest V3 是对扩展平台进行的一项重大更新；如需了解新功能和变更的摘要，请参阅 Manifest V3 概览。扩展程序目前可以继续使用 Manifest V2，但我们会在不久的将来逐步淘汰这一版本。我们强烈建议您为所有新扩展程序使用 Manifest V3，并尽快开始将现有扩展程序迁移到 Manifest V3。
