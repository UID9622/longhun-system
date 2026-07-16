#!/bin/bash
# 🐉 龙魂系统 · ChatTTS 离线/弱网安装脚本
# 在网络可用时一键安装；支持多镜像回退与模型下载镜像。
# DNA: #龍芯⚡️2026-06-27-LONGHUN-CHATTTS-INSTALL-v1.0

set -e

WORKSPACE="/Users/zuimeidedeyihan/Downloads/Kimi_Agent_小龙虾扩展与人格/UID9622_Workspace"
VENV="${WORKSPACE}/.venv-chattts"
PY="${VENV}/bin/python"
PIP="${VENV}/bin/pip"

REPOS=(
  "https://github.com/2noise/ChatTTS.git"
  "https://ghproxy.com/https://github.com/2noise/ChatTTS.git"
  "https://github.moeyy.xyz/https://github.com/2noise/ChatTTS.git"
  "https://mirror.ghproxy.com/https://github.com/2noise/ChatTTS.git"
)

echo "🐉 龙魂 ChatTTS 安装器启动"
echo "DNA: #龍芯⚡️2026-06-27-LONGHUN-CHATTTS-INSTALL-v1.0"

# 确保虚拟环境存在
if [ ! -x "$PY" ]; then
  echo "创建虚拟环境: $VENV"
  /usr/local/bin/python3.11 -m venv "$VENV"
fi

"$PIP" install --upgrade pip wheel setuptools

# 使用国内镜像下载 HuggingFace 模型权重
export HF_ENDPOINT="${HF_ENDPOINT:-https://hf-mirror.com}"

installed=0
for repo in "${REPOS[@]}"; do
  echo "尝试安装: $repo"
  if "$PIP" install "git+$repo"; then
    installed=1
    echo "✅ 安装成功: $repo"
    break
  else
    echo "⚠️  失败，切换镜像..."
  fi
done

if [ $installed -eq 0 ]; then
  echo "❌ 所有镜像均无法访问。请检查网络，或手动将 ChatTTS 源码放到 ${WORKSPACE}/ChatTTS 后执行："
  echo "   $PIP install ${WORKSPACE}/ChatTTS"
  exit 1
fi

# 验证
"$PY" - <<'PY'
import ChatTTS
print("ChatTTS 版本验证通过:", ChatTTS.__version__ if hasattr(ChatTTS, '__version__') else 'unknown')
PY

echo "🎙️ ChatTTS 已就绪，首次推理时会自动下载模型权重（走 $HF_ENDPOINT）"
echo "测试播报: tools/baobao_speak.sh '龙魂语音引擎已上线'"
