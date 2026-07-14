"""声纹DNA注册与验证示例"""

from longhun.voice import VoiceDNA

vdna = VoiceDNA()

# 注册声纹
print("=== 注册声纹 ===")
result = vdna.register(
    user_id="UID9622",
    text="龍魂系统启动",
)
print(f"用户: {result.user_id}")
print(f"DNA: {result.dna}")
print(f"指纹: {result.fingerprint}")
print(f"已注册: {'✅' if result.registered else '❌'}")

# 验证身份
print("\n=== 验证身份 ===")
result = vdna.verify(
    user_id="UID9622",
    audio_file="verify.wav",
)
print(f"匹配: {'✅' if result.match else '❌'}")
print(f"置信度: {result.confidence:.0%}")

# 导出备份
print("\n=== 导出备份 ===")
path = vdna.export("UID9622", "backup.enc")
print(f"已导出: {path}")
