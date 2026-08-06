// 🐉 三色徽章组件
// DNA: #龍芯⚡️2026-08-06-TRICOLOR-BADGE-V1.0-UID9622
// License: MulanPSL v2

import 'package:flutter/material.dart';
import '../theme/colors.dart';
import '../theme/text_styles.dart';

/// 三色审计徽章
class TricolorBadge extends StatelessWidget {
  final String status; // 🟢 🟡 🔴
  final int score;
  final String? label;

  const TricolorBadge({
    super.key, required this.status, required this.score, this.label,
  });

  Color get _color {
    switch (status) {
      case '🟢': return LonghunColors.green;
      case '🟡': return LonghunColors.yellow;
      case '🔴': return LonghunColors.red;
      default: return LonghunColors.textTertiary;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: _color.withValues(alpha: 0.15),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: _color.withValues(alpha: 0.5), width: 1),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(status, style: const TextStyle(fontSize: 14)),
          const SizedBox(width: 6),
          Text(label ?? '$score/100',
            style: LonghunTextStyles.bodySmall.copyWith(color: _color)),
        ],
      ),
    );
  }
}
