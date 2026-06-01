# 龍魂·自适应微调参数系统 v3.0

**DNA**: `#龍芯⚡️2026-05-31-自适应参数-v3.0`

## 新增特性 (v3.0)

1. 异常事件分级 (CRITICAL / WARNING / INFO)
2. 冷启动保护 (样本不足时用默认参数)
3. 参数漂移检测 (连续同向调整警告)
4. 铁律钩子接口 (动态注入铁律)
5. 实时健康评分 (0-100分·四维评估)
6. 草日志自动入册 (每次调整自动记录)
7. Web 仪表板接口 (JSON 导出)
8. 参数上下文注释 (便于终端接入)
9. 多账本支持 (按项目分账本)
10. 自动修复建议 (黄线时给出方案)

## 使用

```bash
python3 longhun_adaptive_tuner_v3.0.py --status       # 查看状态
python3 longhun_adaptive_tuner_v3.0.py --health       # 健康评分
python3 longhun_adaptive_tuner_v3.0.py --analyze      # 趋势分析
python3 longhun_adaptive_tuner_v3.0.py --apply        # 真正调整
python3 longhun_adaptive_tuner_v3.0.py --web-export   # JSON 导出
```
