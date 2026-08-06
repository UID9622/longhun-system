// 🐉 审计卡片组件
// DNA: #龍芯⚡️2026-08-06-AUDIT-CARD-V1.0-UID9622
// License: MulanPSL v2

import 'package:flutter/material.dart';
import '../theme/colors.dart';
import '../theme/text_styles.dart';

/// 审计结果卡片
class AuditCard extends StatelessWidget {
  final String status;
  final int score;
  final List<String> violations;
  final List<String> warnings;

  const AuditCard({
    super.key, required this.status, required this.score,
    this.violations = const [], this.warnings = const [],
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Text(status, style: const TextStyle(fontSize: 24)),
                const SizedBox(width: 8),
                Text('审计评分: $score/100', style: LonghunTextStyles.cardTitle),
              ],
            ),
            const SizedBox(height: 12),
            if (violations.isNotEmpty) ...[
              const Divider(color: LonghunColors.red),
              ...violations.map((v) => Padding(
                padding: const EdgeInsets.only(bottom: 4),
                child: Row(children: [
                  const Icon(Icons.error, color: LonghunColors.red, size: 16),
                  const SizedBox(width: 6),
                  Expanded(child: Text(v, style: LonghunTextStyles.bodySmall)),
                ]),
              )),
            ],
            if (warnings.isNotEmpty) ...[
              const Divider(color: LonghunColors.yellow),
              ...warnings.map((w) => Padding(
                padding: const EdgeInsets.only(bottom: 4),
                child: Row(children: [
                  const Icon(Icons.warning_amber, color: LonghunColors.yellow, size: 16),
                  const SizedBox(width: 6),
                  Expanded(child: Text(w, style: LonghunTextStyles.bodySmall)),
                ]),
              )),
            ],
          ],
        ),
      ),
    );
  }
}
