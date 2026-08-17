#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
🐉 CNSH 可视化引擎
代码流程图 + 数据流图 + 调用链图

DNA: #龍芯⚡️丙午·丙申·辛酉·寅时-VISUALIZER-UID9622
"""

import re
from typing import Dict, List, Any


class CNSHVisualizer:
    """CNSH可视化引擎"""

    @staticmethod
    def _safe_id(name: str) -> str:
        """生成Mermaid安全节点ID"""
        return re.sub(r"[^a-zA-Z0-9_\u4e00-\u9fff]", "_", name)[:40]

    @staticmethod
    def generate_flowchart(code: str) -> str:
        """生成Mermaid流程图"""
        lines = ["```mermaid", "flowchart TD"]

        # 解析函数
        functions = re.findall(r"函数\s+([\u4e00-\u9fff\w]+)\s*\(([^)]*)\)", code)
        node_ids = []
        for idx, (name, params) in enumerate(functions):
            node_id = CNSHVisualizer._safe_id(f"fn_{name}_{idx}")
            node_ids.append(node_id)
            lines.append(f"    {node_id}[\"{name}({params})\"]")

        if node_ids:
            lines.append("    start([开始]) --> " + node_ids[0])
            for i in range(len(node_ids) - 1):
                lines.append(f"    {node_ids[i]} --> {node_ids[i + 1]}")
            lines.append(f"    {node_ids[-1]} --> end_node([结束])")
        else:
            lines.append("    start([开始]) --> end_node([结束])")

        # 解析控制流节点
        if "如果" in code:
            if_id = CNSHVisualizer._safe_id("if_node")
            lines.append(f"    {if_id}{{条件判断}}")
            lines.append(f"    {node_ids[0] if node_ids else 'start'} --> {if_id}")
            lines.append(f"    {if_id} -->|是| then_branch[执行分支]")
            lines.append(f"    {if_id} -->|否| else_branch[其他分支]")
            lines.append("    then_branch --> end_node")
            lines.append("    else_branch --> end_node")

        if "循环" in code:
            loop_id = CNSHVisualizer._safe_id("loop_node")
            lines.append(f"    {loop_id}[/循环执行/]")
            lines.append(f"    {node_ids[0] if node_ids else 'start'} --> {loop_id}")
            lines.append(f"    {loop_id} -->|继续| {loop_id}")
            lines.append(f"    {loop_id} -->|结束| end_node")

        lines.append("```")
        return "\n".join(lines)

    @staticmethod
    def generate_call_graph(receipts: List[Dict]) -> str:
        """生成调用链图（Sequence Diagram）"""
        lines = ["```mermaid", "sequenceDiagram"]

        for receipt in receipts:
            func_name = receipt.get("function_name", "未知")
            dna = receipt.get("dna", "")
            rid = receipt.get("receipt_id", "")
            result = receipt.get("result", "")
            lines.append(f"    User->>+Runtime: 调用 {func_name}")
            lines.append(f"    Runtime->>Runtime: 执行 (DNA: {dna[:20]}...)")
            lines.append(f"    Runtime-->>-User: 回执 {rid[:20]}... 结果 {str(result)[:30]}")

        lines.append("```")
        return "\n".join(lines)

    @staticmethod
    def generate_dataflow(data: Dict) -> str:
        """生成数据流图"""
        lines = ["```mermaid", "graph LR"]

        node_counter = 0
        for key, value in data.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    node_id = f"n{node_counter}"
                    node_counter += 1
                    label = f"{key}.{subkey}"
                    lines.append(f"    {node_id}[\"{label}\"]")
                    out_id = f"out_{node_counter}"
                    lines.append(
                        f"    {out_id}[\"输出: {str(subvalue)[:30]}\"]"
                    )
                    lines.append(f"    {node_id} --> {out_id}")
            else:
                node_id = f"n{node_counter}"
                node_counter += 1
                lines.append(f"    {node_id}[\"{key}\"]")
                out_id = f"out_{node_counter}"
                lines.append(f"    {out_id}[\"输出: {str(value)[:30]}\"]")
                lines.append(f"    {node_id} --> {out_id}")

        lines.append("```")
        return "\n".join(lines)


# ============================================================
# 测试可视化
# ============================================================


def test_visualizer():
    """测试可视化引擎"""
    code = """
    函数 计算折扣(价格, 折扣率):
        如果 价格 > 100:
            返回 价格 * 折扣率 * 0.9
        否则:
            返回 价格 * 折扣率
    """

    print("🐉 CNSH 可视化测试")
    print("=" * 50)

    print("\n📊 流程图:")
    print(CNSHVisualizer.generate_flowchart(code))

    print("\n📊 数据流:")
    data = {"价格": 100, "折扣率": 0.85, "计算折扣": {"结果": 85, "状态": "成功"}}
    print(CNSHVisualizer.generate_dataflow(data))

    # 调用链 (使用运行时的回执)
    import sys
    sys.path.insert(0, str(__file__).rsplit("/", 1)[0])
    from cnsh_runtime import build_cnsh_runtime, test_runtime

    runtime = test_runtime()
    receipts = [r.to_dict() for r in runtime.get_all_receipts()[-3:]]
    if receipts:
        print("\n📊 调用链:")
        print(CNSHVisualizer.generate_call_graph(receipts))


if __name__ == "__main__":
    test_visualizer()
