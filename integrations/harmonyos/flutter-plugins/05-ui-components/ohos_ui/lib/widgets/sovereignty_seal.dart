// 🐉 主权印章组件
// DNA: #龍芯⚡️2026-08-06-SOVEREIGNTY-SEAL-V1.0-UID9622
// License: MulanPSL v2

import 'package:flutter/material.dart';
import '../theme/colors.dart';
import '../theme/text_styles.dart';

/// 主权印章 - 显示龙魂主权锚定
class SovereigntySeal extends StatelessWidget {
  final double size;
  final bool showText;
  final VoidCallback? onTap;

  const SovereigntySeal({
    super.key, this.size = 80, this.showText = true, this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            width: size, height: size,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              gradient: LonghunColors.goldGradient,
              border: Border.all(color: LonghunColors.gold, width: 2),
              boxShadow: [
                BoxShadow(
                  color: LonghunColors.gold.withValues(alpha: 0.3),
                  blurRadius: 20, spreadRadius: 4,
                ),
              ],
            ),
            child: Center(
              child: Text('🐉', style: TextStyle(fontSize: size * 0.45, color: Colors.white)),
            ),
          ),
          if (showText) ...[
            const SizedBox(height: 10),
            Text('主权锚定 · UID9622',
              style: LonghunTextStyles.caption.copyWith(
                color: LonghunColors.gold, letterSpacing: 1.5,
              )),
            const SizedBox(height: 2),
            Text('#ZHUGEXIN⚡️2025',
              style: LonghunTextStyles.caption.copyWith(
                color: LonghunColors.textTertiary, fontSize: 9,
              )),
          ],
        ],
      ),
    );
  }
}
