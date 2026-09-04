# 🐉 龍魂主权技术栈·华为云 Terraform 输出
# DNA: #龍芯⚡️2026-08-31-TERRAFORM-HUAWEI-OUTPUTS-V1.0-UID9622
# 创建者: 诸葛鑫（UID9622）· 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: MulanPSL v2（工程实现层）

output "gateway_public_ip" {
  value       = huaweicloud_vpc_eip.gateway.address
  description = "网关公网 IP（部署完成后复制此地址）"
}

output "obs_bucket_name" {
  value       = huaweicloud_obs_bucket.sovereign_data.bucket
  description = "OBS 存储桶名称"
}

output "dna" {
  value = "#龍芯⚡️2026-08-31-TERRAFORM-HUAWEI-OUTPUT-UID9622"
}
