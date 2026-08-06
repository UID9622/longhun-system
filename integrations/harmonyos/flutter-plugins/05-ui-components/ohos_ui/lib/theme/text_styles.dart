// 🐉 龙魂文字样式
// DNA: #龍芯⚡️2026-08-06-TEXT-STYLES-V1.0-UID9622
// License: MulanPSL v2

import 'package:flutter/material.dart';
import 'colors.dart';

class LonghunTextStyles {
  static const TextStyle h1 = TextStyle(
    fontSize: 28, fontWeight: FontWeight.bold,
    color: LonghunColors.gold, letterSpacing: 1.5,
  );

  static const TextStyle h2 = TextStyle(
    fontSize: 22, fontWeight: FontWeight.w600,
    color: LonghunColors.textPrimary, letterSpacing: 1.0,
  );

  static const TextStyle h3 = TextStyle(
    fontSize: 18, fontWeight: FontWeight.w600,
    color: LonghunColors.textPrimary,
  );

  static const TextStyle bodyLarge = TextStyle(
    fontSize: 16, fontWeight: FontWeight.normal,
    color: LonghunColors.textPrimary, height: 1.6,
  );

  static const TextStyle bodyMedium = TextStyle(
    fontSize: 14, fontWeight: FontWeight.normal,
    color: LonghunColors.textSecondary, height: 1.5,
  );

  static const TextStyle bodySmall = TextStyle(
    fontSize: 12, color: LonghunColors.textTertiary,
  );

  static const TextStyle cardTitle = TextStyle(
    fontSize: 16, fontWeight: FontWeight.w600,
    color: LonghunColors.gold,
  );

  static const TextStyle button = TextStyle(
    fontSize: 15, fontWeight: FontWeight.w600,
    color: LonghunColors.gold, letterSpacing: 1.0,
  );

  static const TextStyle caption = TextStyle(
    fontSize: 11, color: LonghunColors.textTertiary,
  );

  static const TextStyle dna = TextStyle(
    fontSize: 10, color: LonghunColors.goldDim,
    fontFamily: 'monospace', letterSpacing: 0.5,
  );
}
