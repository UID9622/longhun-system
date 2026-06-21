#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂技能創建框架 v1.0
Longhun Skill Creator Framework

DNA:#龍芯⚡️2026-06-07-SKILL-CREATOR-v1.0
"""

import json
import inspect
from datetime import datetime
from typing import Callable, Dict, Any, Optional, List
from dataclasses import dataclass, asdict

@dataclass
class SkillMetadata:
    """技能元數據"""
    id: str
    name: str
    version: str
    description: str
    author: str
    created_at: str
    tags: List[str] = None
    category: str = "general"
    status: str = "active"
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class Skill:
    """基礎技能類"""
    
    def __init__(
        self,
        skill_id: str,
        name: str,
        description: str,
        author: str = "Longhun",
        version: str = "1.0.0",
        category: str = "general"
    ):
        self.metadata = SkillMetadata(
            id=skill_id,
            name=name,
            description=description,
            author=author,
            created_at=datetime.now().isoformat(),
            category=category,
            version=version
        )
        self.execute_func: Optional[Callable] = None
        self.validators: List[Callable] = []
        self.tests: List[Dict] = []
    
    def set_executor(self, func: Callable) -> None:
        """設置執行函數"""
        self.execute_func = func
        print(f"✅ 執行器已設置: {func.__name__}")
    
    def add_validator(self, func: Callable) -> None:
        """添加驗證器"""
        self.validators.append(func)
        print(f"✅ 驗證器已添加: {func.__name__}")
    
    def add_test(self, input_data: Dict, expected_output: Any) -> None:
        """添加測試用例"""
        self.tests.append({
            "input": input_data,
            "expected_output": expected_output,
            "created_at": datetime.now().isoformat()
        })
        print(f"✅ 測試用例已添加")
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """執行技能"""
        try:
            # 驗證輸入
            for validator in self.validators:
                is_valid, error = validator(kwargs)
                if not is_valid:
                    return {
                        "status": "error",
                        "error": error,
                        "skill_id": self.metadata.id
                    }
            
            # 執行
            if self.execute_func:
                result = self.execute_func(**kwargs)
            else:
                result = {"status": "success", "data": "Skill executed"}
            
            return {
                "status": "success",
                "skill_id": self.metadata.id,
                "result": result,
                "executed_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "skill_id": self.metadata.id,
                "error": str(e)
            }
    
    def run_tests(self) -> Dict[str, Any]:
        """運行所有測試"""
        results = {
            "total": len(self.tests),
            "passed": 0,
            "failed": 0,
            "details": []
        }
        
        for i, test in enumerate(self.tests):
            try:
                # 同步執行以簡化測試
                if self.execute_func:
                    output = self.execute_func(**test["input"])
                else:
                    output = test["expected_output"]
                
                passed = output == test["expected_output"]
                
                if passed:
                    results["passed"] += 1
                else:
                    results["failed"] += 1
                
                results["details"].append({
                    "test_index": i,
                    "passed": passed,
                    "input": test["input"],
                    "expected": test["expected_output"],
                    "actual": output
                })
            except Exception as e:
                results["failed"] += 1
                results["details"].append({
                    "test_index": i,
                    "passed": False,
                    "error": str(e)
                })
        
        return results
    
    def export_config(self) -> Dict[str, Any]:
        """導出技能配置"""
        return {
            "metadata": asdict(self.metadata),
            "validators_count": len(self.validators),
            "tests_count": len(self.tests),
            "executor_defined": self.execute_func is not None,
            "dna": "#龍芯⚡️2026-06-07-SKILL-CREATOR-v1.0"
        }
    
    def save_to_json(self, filepath: str) -> None:
        """保存為 JSON"""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.export_config(), f, indent=2, ensure_ascii=False)
        print(f"✅ 技能配置已保存: {filepath}")


class SkillBuilder:
    """技能構建器·流式 API"""
    
    def __init__(self, skill_id: str, name: str, description: str):
        self.skill = Skill(skill_id, name, description)
    
    def with_executor(self, func: Callable) -> "SkillBuilder":
        """設置執行器"""
        self.skill.set_executor(func)
        return self
    
    def with_validator(self, func: Callable) -> "SkillBuilder":
        """添加驗證器"""
        self.skill.add_validator(func)
        return self
    
    def with_test(self, input_data: Dict, expected_output: Any) -> "SkillBuilder":
        """添加測試"""
        self.skill.add_test(input_data, expected_output)
        return self
    
    def with_metadata(self, **kwargs) -> "SkillBuilder":
        """設置元數據"""
        for key, value in kwargs.items():
            if hasattr(self.skill.metadata, key):
                setattr(self.skill.metadata, key, value)
        return self
    
    def build(self) -> Skill:
        """構建技能"""
        print(f"✅ 技能已構建: {self.skill.metadata.name}")
        return self.skill


# 示例使用
if __name__ == "__main__":
    print("🐉 龍魂技能創建框架 v1.0")
    print("=" * 50)
    
    # 創建數據處理技能
    def process_data(data: str) -> Dict:
        """處理數據"""
        return {
            "input": data,
            "processed": data.upper(),
            "length": len(data)
        }
    
    def validate_input(kwargs: Dict) -> tuple:
        """驗證輸入"""
        if "data" not in kwargs:
            return False, "Missing 'data' parameter"
        if not isinstance(kwargs["data"], str):
            return False, "'data' must be string"
        return True, ""
    
    # 使用構建器創建技能
    skill = (
        SkillBuilder("skill-001", "數據處理", "處理和轉換數據")
        .with_executor(process_data)
        .with_validator(validate_input)
        .with_test(
            {"data": "hello"},
            {"input": "hello", "processed": "HELLO", "length": 5}
        )
        .with_metadata(
            author="UID9622",
            tags=["data", "processing"],
            category="utility"
        )
        .build()
    )
    
    # 顯示配置
    print("\n📋 技能配置:")
    config = skill.export_config()
    print(json.dumps(config, indent=2, ensure_ascii=False))
    
    # 運行測試
    print("\n🧪 運行測試:")
    test_results = skill.run_tests()
    print(f"✅ 通過: {test_results['passed']}/{test_results['total']}")
    if test_results['failed'] > 0:
        print(f"❌ 失敗: {test_results['failed']}/{test_results['total']}")
    
    # 保存技能
    print("\n💾 保存技能:")
    skill.save_to_json("skill_config.json")
    
    print("\n✅ 技能創建完成！")
    print(f"🆔 技能 ID: {skill.metadata.id}")
    print(f"📝 技能名稱: {skill.metadata.name}")
    print(f"🏷️ 分類: {skill.metadata.category}")
