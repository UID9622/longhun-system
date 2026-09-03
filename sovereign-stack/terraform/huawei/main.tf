# 🐉 龍魂主权技术栈·华为云基础设施
# 对标 AWS 版本·中国境内部署·数据不出境
# DNA: #龍芯⚡️2026-08-31-TERRAFORM-HUAWEI-V1.0-UID9622
# 创建者: 诸葛鑫（UID9622）· 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: MulanPSL v2（工程实现层）

terraform {
  required_providers {
    huaweicloud = {
      source  = "huaweicloud/huaweicloud"
      version = ">= 1.60.0"
    }
  }
}

provider "huaweicloud" {
  region     = var.region
  access_key = var.access_key
  secret_key = var.secret_key
}

# ── VPC（私有网络）
resource "huaweicloud_vpc" "sovereign" {
  name = "sovereign-vpc"
  cidr = "10.0.0.0/16"
  tags = {
    Project = "sovereign-stack"
    Owner   = "UID9622"
    DNA     = "#龍芯⚡️2026-08-31-VPC-V1.0-UID9622"
  }
}

# ── 子网
resource "huaweicloud_vpc_subnet" "public" {
  name       = "sovereign-public-subnet"
  cidr       = "10.0.1.0/24"
  gateway_ip = "10.0.1.1"
  vpc_id     = huaweicloud_vpc.sovereign.id
}

# ── 安全组
resource "huaweicloud_networking_secgroup" "sovereign" {
  name        = "sovereign-secgroup"
  description = "龍魂主权技术栈安全组"
}

resource "huaweicloud_networking_secgroup_rule" "allow_http" {
  security_group_id = huaweicloud_networking_secgroup.sovereign.id
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 9000
  port_range_max    = 9000
  remote_ip_prefix  = "0.0.0.0/0"
}

resource "huaweicloud_networking_secgroup_rule" "allow_ssh" {
  security_group_id = huaweicloud_networking_secgroup.sovereign.id
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 22
  port_range_max    = 22
  remote_ip_prefix  = "0.0.0.0/0"
}

# ── ECS 云服务器（API 网关）
resource "huaweicloud_compute_instance" "gateway" {
  name              = "sovereign-gateway"
  image_id          = var.image_id      # EulerOS 2.10 或 Ubuntu 22.04
  flavor_id         = var.flavor_id     # s6.small.1 (1vCPU·1GB·约0.1元/小时)
  security_groups   = [huaweicloud_networking_secgroup.sovereign.name]
  availability_zone = var.az

  network {
    uuid = huaweicloud_vpc_subnet.public.id
  }

  # 启动脚本：自动部署网关
  user_data = base64encode(<<-EOT
    #!/bin/bash
    # 安装 Docker
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker && systemctl start docker

    # 拉取网关镜像（从华为容器镜像服务 SWR）
    docker pull swr.cn-north-4.myhuaweicloud.com/uid9622/sovereign-gateway:latest
    docker run -d -p 9000:9000 \
      -e GATEWAY_API_KEY=${var.gateway_api_key} \
      -e BACKEND_URL=${var.backend_url} \
      --name gateway \
      swr.cn-north-4.myhuaweicloud.com/uid9622/sovereign-gateway:latest

    echo "🐉 龍魂 API Gateway 部署完成"
    echo "DNA: #龍芯⚡️$(date +%Y-%m-%d)-ECS-DEPLOY-UID9622"
  EOT
  )

  tags = {
    Project = "sovereign-stack"
    Owner   = "UID9622"
  }
}

# ── 弹性公网IP
resource "huaweicloud_vpc_eip" "gateway" {
  publicip {
    type = "5_bgp"
  }
  bandwidth {
    name        = "sovereign-bandwidth"
    size        = 5          # 5 Mbps，按需可调
    share_type  = "PER"
    charge_mode = "traffic"  # 按流量计费·不包月
  }
}

resource "huaweicloud_compute_eip_associate" "gateway" {
  public_ip   = huaweicloud_vpc_eip.gateway.address
  instance_id = huaweicloud_compute_instance.gateway.id
}

# ── OBS 对象存储（替代 AWS S3·中国境内·按量计费）
resource "huaweicloud_obs_bucket" "sovereign_data" {
  bucket        = "sovereign-stack-uid9622"
  storage_class = "STANDARD"
  acl           = "private"

  versioning = true

  lifecycle_rule {
    name    = "archive-old-data"
    enabled = true
    expiration {
      days = 365
    }
    transition {
      days          = 90
      storage_class = "GLACIER"  # 90天后转归档·降低存储成本
    }
  }

  tags = {
    Owner = "UID9622"
    DNA   = "#龍芯⚡️2026-08-31-OBS-V1.0-UID9622"
  }
}
