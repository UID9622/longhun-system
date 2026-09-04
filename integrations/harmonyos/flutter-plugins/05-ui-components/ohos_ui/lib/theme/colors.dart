// 🐉 龙魂颜色常量
// DNA: #龍芯⚡️2026-08-06-COLORS-V1.0-UID9622
// License: MulanPSL v2

import 'package:flutter/material.dart';

class LonghunColors {
  // 主色 - 暗金
  static const Color gold = Color(0xFFD4AF37);
  static const Color goldLight = Color(0xFFE8C84A);
  static const Color goldDark = Color(0xFFB8962A);
  static const Color goldDim = Color(0x33D4AF37);

  // 背景色
  static const Color background = Color(0xFF0A0A12);
  static const Color card = Color(0xFF12121F);
  static const Color input = Color(0xFF1A1A2E);
  static const Color surface = Color(0xFF1E1E32);

  // 文本色
  static const Color textPrimary = Color(0xFFE8E6E3);
  static const Color textSecondary = Color(0xFFA8A6A3);
  static const Color textTertiary = Color(0xFF6A6865);

  // 边框
  static const Color border = Color(0xFF2A2A3E);
  static const Color borderGold = Color(0x44D4AF37);

  // 三色审计
  static const Color green = Color(0xFF4ADE80);
  static const Color yellow = Color(0xFFFBBF24);
  static const Color red = Color(0xFFF87171);

  // 状态
  static const Color success = green;
  static const Color warning = yellow;
  static const Color error = red;
  static const Color info = Color(0xFF60A5FA);

  // 渐变
  static const LinearGradient goldGradient = LinearGradient(
    begin: Alignment.topLeft, end: Alignment.bottomRight,
    colors: [gold, goldDark],
  );

  static const LinearGradient darkGradient = LinearGradient(
    begin: Alignment.topCenter, end: Alignment.bottomCenter,
    colors: [Color(0xFF12121F), Color(0xFF0A0A12)],
  );
}
