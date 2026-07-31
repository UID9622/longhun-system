# DNA: #龍芯⚡️丙午·乙未·乙丑·泰-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动为鲲鹏服务器 119.13.90.27 的 ECS 安全组放行 TCP 22 端口。
读取 ~/.longhun/huawei-credentials.json 中的 AK/SK。
"""
import json
import os
import sys

from huaweicloudsdkcore.auth.credentials import BasicCredentials, GlobalCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkecs.v2 import EcsClient, ListServersDetailsRequest
from huaweicloudsdkecs.v2.region.ecs_region import EcsRegion
from huaweicloudsdkiam.v3 import IamClient, KeystoneListProjectsRequest
from huaweicloudsdkiam.v3.region.iam_region import IamRegion
from huaweicloudsdkvpc.v2 import VpcClient, ListSecurityGroupsRequest, CreateSecurityGroupRuleRequest, CreateSecurityGroupRuleOption
from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion

CRED_PATH = os.path.expanduser("~/.longhun/huawei-credentials.json")
TARGET_IP = "119.13.90.27"


def load_credentials():
    with open(CRED_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["access_key"]["id"], data["access_key"]["secret"], data.get("project", "cn-north-4")


def get_project_id(ak, sk, region_name):
    """根据区域名从 IAM 查询对应的项目 ID (UUID)"""
    credentials = GlobalCredentials(ak, sk)
    client = IamClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(IamRegion.CN_NORTH_4) \
        .build()
    try:
        response = client.keystone_list_projects(KeystoneListProjectsRequest())
        for project in response.projects:
            if project.name == region_name:
                return project.id
        raise RuntimeError(f"未在 IAM 中找到区域 {region_name} 对应的项目 ID")
    except exceptions.ClientRequestException as e:
        raise RuntimeError(f"查询 IAM 项目失败: {e.status_code} {e.error_msg}")


def get_ecs_security_group_id(ecs_client, ip):
    """根据公网 IP 查找 ECS 实例，返回其安全组 ID"""
    try:
        request = ListServersDetailsRequest()
        response = ecs_client.list_servers_details(request)
        for server in response.servers:
            for addr in server.addresses.values():
                for a in addr:
                    if a.addr == ip:
                        if server.security_groups:
                            return server.security_groups[0].id, server.id
        return None, None
    except exceptions.ClientRequestException as e:
        raise RuntimeError(f"查询 ECS 失败: {e.status_code} {e.error_msg}")


def find_server_across_regions(ak, sk, projects, ip):
    """跨所有项目/区域查找指定公网 IP 的 ECS"""
    for project in projects:
        region_name = project.name.replace("-", "_").upper()
        ecs_region = getattr(EcsRegion, region_name, None)
        if ecs_region is None:
            continue
        credentials = BasicCredentials(ak, sk, project.id)
        ecs_client = EcsClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(ecs_region) \
            .build()
        sg_id, server_id = get_ecs_security_group_id(ecs_client, ip)
        if sg_id:
            return project, sg_id, server_id
    raise RuntimeError(f"在所有区域中均未找到公网 IP 为 {ip} 的 ECS 实例")


def rule_exists(vpc_client, sg_id):
    """检查安全组是否已有 TCP 22 入口规则"""
    try:
        request = ListSecurityGroupsRequest()
        response = vpc_client.list_security_groups(request)
        for sg in response.security_groups:
            if sg.id != sg_id:
                continue
            for rule in sg.security_group_rules:
                if (rule.direction == "ingress" and
                        rule.protocol == "tcp" and
                        rule.port_range_min == 22 and
                        rule.port_range_max == 22):
                    return True
        return False
    except exceptions.ClientRequestException as e:
        raise RuntimeError(f"查询安全组失败: {e.status_code} {e.error_msg}")


def add_ssh_rule(vpc_client, sg_id):
    """添加 TCP 22 入口规则"""
    try:
        option = CreateSecurityGroupRuleOption(
            security_group_id=sg_id,
            direction="ingress",
            protocol="tcp",
            port_range_min="22",
            port_range_max="22",
            remote_ip_prefix="0.0.0.0/0",
            action="allow"
        )
        request = CreateSecurityGroupRuleRequest()
        request.security_group_rule = option
        response = vpc_client.create_security_group_rule(request)
        return response.security_group_rule.id
    except exceptions.ClientRequestException as e:
        raise RuntimeError(f"添加安全组规则失败: {e.status_code} {e.error_msg}")


def main():
    ak, sk, project = load_credentials()

    print(f"[0/4] 查询 IAM 获取所有项目...")
    iam_creds = GlobalCredentials(ak, sk)
    iam_client = IamClient.new_builder() \
        .with_credentials(iam_creds) \
        .with_region(IamRegion.CN_NORTH_4) \
        .build()
    projects = iam_client.keystone_list_projects(KeystoneListProjectsRequest()).projects
    print(f"       共 {len(projects)} 个项目/区域")

    print(f"[1/4] 跨所有区域查找 ECS {TARGET_IP}...")
    found_project, sg_id, server_id = find_server_across_regions(ak, sk, projects, TARGET_IP)
    print(f"       找到于区域: {found_project.name}")
    print(f"       ECS: {server_id}")
    print(f"       安全组: {sg_id}")

    region_name = found_project.name.replace("-", "_").upper()
    vpc_region = getattr(VpcRegion, region_name, VpcRegion.CN_NORTH_4)
    credentials = BasicCredentials(ak, sk, found_project.id)
    vpc_client = VpcClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(vpc_region) \
        .build()

    print("[2/4] 检查是否已有 TCP 22 规则...")
    if rule_exists(vpc_client, sg_id):
        print("       已存在，无需重复添加。")
        return 0

    print("[3/4] 添加 TCP 22 入方向规则...")
    rule_id = add_ssh_rule(vpc_client, sg_id)
    print(f"       规则已创建: {rule_id}")

    print("[4/4] 等待规则生效（约 10 秒）...")
    import time
    time.sleep(10)
    print("       完成。现在可以尝试 SSH 连接。")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
