// 🐉 DNA显示组件
// DNA: #龍芯⚡️2026-08-06-DNA-DISPLAY-V1.0-UID9622
// License: MulanPSL v2

import 'package:flutter/material.dart';
import '../theme/colors.dart';
import '../theme/text_styles.dart';

/// DNA追溯码显示组件
class DNADisplay extends StatelessWidget {
  final String dna;
  final bool compact;

  const DNADisplay({super.key, required this.dna, this.compact = false});

  @override
  Widget build(BuildContext context) {
    if (compact) {
      return Text(dna, style: LonghunTextStyles.dna, maxLines: 1,
        overflow: TextOverflow.ellipsis);
    }

    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: LonghunColors.card,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: LonghunColors.borderGold),
      ),
      child: Row(
        children: [
          const Text('🧬 ', style: TextStyle(fontSize: 14)),
          Expanded(
            child: Text(dna, style: LonghunTextStyles.dna),
          ),
        ],
      ),
    );
  }
}
