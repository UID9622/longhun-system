# 🐉 龍魂主权技术栈·华为云 Terraform 变量
# DNA: #龍芯⚡️2026-08-31-TERRAFORM-HUAWEI-VARIABLES-V1.0-UID9622
# 创建者: 诸葛鑫（UID9622）· 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: MulanPSL v2（工程实现层）

variable "region" {
  default     = "cn-north-4"    # 北京四区
  description = "华为云区域（cn-north-4=北京·cn-east-3=上海·cn-south-1=广州）"
}

variable "az" {
  default     = "cn-north-4a"
  description = "可用区"
}

variable "access_key" {
  description = "华为云 Access Key ID（不要提交到 git）"
  sensitive   = true
}

variable "secret_key" {
  description = "华为云 Secret Access Key（不要提交到 git）"
  sensitive   = true
}

variable "image_id" {
  default     = "Ubuntu 22.04 server 64bit"
  description = "ECS 镜像 ID（华为云控制台查询）"
}

variable "flavor_id" {
  default     = "s6.small.1"
  description = "规格（s6.small.1=1核1G·约0.1元/小时）"
}

variable "gateway_api_key" {
  description = "API 网关密钥"
  sensitive   = true
}

variable "backend_url" {
  default     = "http://localhost:8080"
  description = "后端服务地址"
}
