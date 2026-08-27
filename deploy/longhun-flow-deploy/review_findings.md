<!-- DNA: #龍芯⚡️丙午·丙申·甲戌·卯时·䷐随-QUAD-SYNC-v1.0-ATTRIBUTION-8c26d5f -->
<!-- 归属名: 诸葛鑫 | UID9622 · 龍芯北辰 -->
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# 审查官十大类过堂结果（落地依据，全部必须处理）

## 🔴 致命级（16条）
1. deploy heredoc 占位符：deploy 脚本 cat 只写注释，nginx.conf 被覆盖成废配置。修法：完整配置嵌入 heredoc，写临时文件→`nginx -t`→原子替换，失败自动从备份恢复（trap）。
2. Prometheus 指标不存在：stub_status 只有7个标量，不产生 nginx_up/nginx_http_requests_total{status}/nginx_ssl_cert_expiry_days。修法：nginx-prometheus-exporter 提供 nginx_up/nginx_http_requests_total（无status标签）；5xx率走 access log json + mtail/textfile；证书天数用 textfile 脚本；metric名同步改，整体标🟡。
3. `add_header Content-Type` 在 return 块内无效，只会追加第二个 Content-Type。修法：`error_page 403 = @p0_denied;` + 命名location `default_type application/json; return 403 '{...}';`
4. location级 add_header 屏蔽 server 级继承：/health、静态资源、/collab/ 一旦有自己的 add_header，X-LongHun-* 全丢。修法：这些 location 内重复全部 P0/安全头。
5. P0检查形同虚设：`if ($http_x_dragon_dna = "")` 只查存在性。修法：降级表述为「审计标记头，非鉴权」，删「不可绕过」字样；鉴权交给后端 auth_request（本期工程包实现 auth_request 子请求到 API网关 /auth/verify，验 DNA 格式+长度，HMAC 验签标🟡待真机）。
6. ModSecurity 白名单 allow = WAF 全旁路。修法：删除该规则，文档改为「如需降误报用 ctl:ruleRemoveById」。
7. autoindex on 公网裸奔 + CDN 缓存 /collab/*。修法：collab/handoffs 加 auth_request 到协作中枢验证；CDN 缓存排除；补 GET-only。
8. /collab/ 拓扑矛盾：设计说反代19622，配置是静态 alias。修法：工程包采用「/collab/ 静态只读 + /collab/api/ 反代19622」双路由，文档拓扑同步修正。
9. `proxy_pass http://longhun_bridge/api/v1/chat` 无尾斜杠路径拼接bug。修法：改 `location = /chat/ { proxy_pass http://longhun_bridge/api/v1/chat; }` 精确匹配 + `location /chat/ { ... /api/v1/chat/; }`。
10. `echo ... | crontab -` 覆盖式清空现有cron。修法：写 /etc/cron.d/longhun。
11. 回滚命令 date 格式不匹配备份名，永远找不到文件；流程图声称自动回滚但脚本没有。修法：备份打 manifest 时间戳目录，rollback 取最新；deploy 内置 trap 回滚。
12. SSL 证书前置未闭环。修法：两段式——证书不存在时先起80-only临时配置跑 certbot，再切443全配置；前置检查加 DNS 解析断言（dig uid9622.cn 对得上本机公网IP）。
13. /var/log/longhun 未创建导致 nohup 重定向失败。修法：mkdir + logrotate + systemd 接管（journald）。
14. 对话桥接同步 requests 阻塞 event loop 且无超时。修法：httpx.AsyncClient stream + timeout=180 + raise_for_status + 异常兜底。
15. ip_local_port_range=1024 65535 把后端端口纳入源端口池。修法：删除该项，用系统默认。
16. DNA 干支错误：正确口径 丙午·丙申·己未·乙亥时·旅；稿2/稿3 日柱「庚申」错；三稿共用同一DNA串违规。修法：统一用生成器输出，一文件一功能码。

## 🟡 重要级（11条）
17. 参数对照表与配置不一致（keepalive 75 vs 65、gzip_comp_level 但无 gzip on 等）。修法：配置补 gzip 段，表随配置改齐。
18. 限流表与配置不一致（/chat 5r/s 表 vs 复用 api_limit）。修法：新增 chat_limit zone 5r/s，表配对齐。
19. 签名区统计造假（18节点/15指标等数不对）。修法：数字如实数准。
20. health_check.sh 死变量 all_ok、curl 无 --max-time、未 chmod +x。修法：全部修。
21. 史官 verify_chain 恒 True 是 stub。修法：实现真实 prev_hash 链校验。
22. generate_dna 同秒撞码。修法：掺 uuid4 随机段。
23. 缺 systemd×3、logrotate、前端 index.html、requirements.txt 锁定版本、PEP668 用 venv（/opt/longhun-system/venv）。
24. 删 X-XSS-Protection，加 HSTS；`listen 443 ssl http2` 改 `http2 on;`；`location ~ /\.` 会挡 certbot webroot——用 `location ^~ /.well-known/` 放行。
25. LICENSE 落盘：MulanPSL-2.0 标准拼写 + LICENSE-CODE/LICENSE-DOC 文件 + SPDX 头。
26. 模型名 longhun-v4.1.4 虚构需注明先 ollama create；鲲鹏无CUDA纯CPU推理指标标🟡；ModSecurity arm64 需源码编译标🟡；Ubuntu 22.04 arm64 默认 Python3.10，requirements 兼容 3.10。
27. `location ~ /\.` 与 webroot 续期冲突已在24处理。

## 待验清单（沙箱不可验，文档必须标🟡）
- 鲲鹏 arm64 sysctl conntrack 可写性、IPv6 listen
- Ollama CPU 推理延迟/内存真实值、延迟预算全部回填前标🟡
- DNS 解析/安全组/443 80 入向
- Cloudflare 回源兼容
- ModSecurity arm64 编译 + emoji 头误报率
- 限流误杀率无历史数据

## 可保留（勿动）
- upstream keepalive 写法、JSON log_format、80→443 301、TLS1.2/1.3 cipher 基线、备份思路+nginx -t 前置、限流 zone 写法、Q1-Q5 排障命令、四层架构划分、五步节点手册骨架、签名区风格
