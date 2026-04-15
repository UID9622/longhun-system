# 演示文件：伪代码检测示例
# DNA: #UID9622⚡️20260111-DEMO-001

def 观天(场景: str) -> str:
    """
    观察天象并分析场景特征
    这个函数包含伪代码，用于演示检测功能
    """
    指纹 = 取象(场景)    # 🔴 伪代码：未定义函数
    卦象 = 起卦(指纹)    # 🔴 伪代码：未定义函数
    天机 = 悟道(卦象)    # 🔴 伪代码：未定义函数
    return 天机

def 创世(参数: dict[str, any]) -> dict[str, any]:
    """
    另一个伪代码函数示例
    """
    世界 = 化生(参数)    # 🔴 伪代码：未定义函数
    return 世界

def 数据处理(数据: list[any]) -> any:
    """
    这个函数有一些真实的代码和伪代码混合
    """
    import pandas as pd  # 真实的import
    df = pd.DataFrame(数据)
    
    结果 = 分析数据(df)  # 🔴 伪代码：未定义函数
    洞察 = 提取智慧(结果)  # 🔴 伪代码：未定义函数
    
    return 洞察

# 正常的函数（不会被标记为伪代码）
def normal_function(input_data: int) -> int:
    """这是一个正常的函数"""
    return input_data * 2

# 有中文变量名但可能是真实代码
def process_chinese_data() -> int:
    用户数据 = [1, 2, 3]  # 🟡 可能是伪代码变量
    计算结果 = sum(用户数据)  # 🟡 可能是伪代码变量
    return 计算结果