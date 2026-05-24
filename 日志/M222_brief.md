# 战报 M222 · 草日志（入口块已焊）

时间: 2026-05-23

要点摘要:

- 已准备「爸爸本机三连刀」的操作支持文件与执行脚本：
  - 刀 A (Cloudflare DNS 改 CNAME)：操作需在浏览器 Cloudflare 控制台手动完成，已提供验证命令。
  - 刀 B (cloudflared ingress 写入)：已在仓库放置样例配置 .cloudflared/config.yml.sample，请复制到 ~/.cloudflared/config.yml 并重启 tunnel。
  - 刀 C (华为云切模型)：已生成 scripts/huawei_switch_model_and_trace.sh，需在华为云主机上执行（含 IAM trace 写入）。

- 已修复 longhun_dragon.py 的 persona→model 路由优先级：现在会优先读取 persona-engine.json 中的 persona_to_model 覆盖映射（若存在），避免默认全部回退到 qwen2.5:7b。

- 已创建/补齐仓库内文件骨架：
  - bin/启动所有服务.sh
  - agent_daemon.py
  - .cloudflared/config.yml.sample
  - scripts/huawei_switch_model_and_trace.sh

验证与下一步（用户执行）:

1. 刀 A（Cloudflare） — 在浏览器操作：
   - 打开 Cloudflare → longhun888.com → DNS → 编辑 ollama 记录，改为 CNAME 指向 7869dd91-cd25-45c8-981e-19d707700f6e.cfargotunnel.com，Proxy status 设为 DNS only（灰云）。
   - 验证命令: dig ollama.longhun888.com CNAME +short

2. 刀 B（cloudflared ingress） — 在运行 cloudflared 的主机上复制样例并重启：
   - cp longhun-system/.cloudflared/config.yml.sample ~/.cloudflared/config.yml
   - pkill cloudflared || true
   - cloudflared tunnel run longhun-webhook
   - 验证: curl -i https://ollama.longhun888.com/api/tags

3. 刀 C（华为云模型切换） — 在华为云主机上执行：
   - bash ~/longhun-system/scripts/huawei_switch_model_and_trace.sh
   - 或手动执行: ollama pull qwen2.5:7b
   - 写 IAM trace: mkdir -p /root/CNSH/audit && echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | IAM-UID=3e53a2df623044e499b9227c93d55955 | IP=$(hostname -I | awk '{print $1}') | DIR=/root/CNSH | MODEL=qwen2.5:7b | DNA=#龍芯⚡️2026-05-23-20:02-EXTERNAL-CLOUD-IAM-VERBATIM-TRACE-v1.0" > /root/CNSH/audit/iam_trace.log

4. 验证 longhun_dragon.py 路由修复（在本机）：
   - 查看本地模型列表: curl -s http://127.0.0.1:11434/api/tags | jq .
   - 运行扫描: python3 longhun_dragon.py --scan
   - 单次问答示例: python3 longhun_dragon.py --ask "帮我审计这个 API 接口"

需要我代你把 Cloudflare 改为 CNAME 或 SSH 到华为云并执行脚本吗？如果需要，请提供 Cloudflare 账号/操作授权或远程主机 SSH 凭据（或允许我执行哪些具体步骤）。
