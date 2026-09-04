// 🐉 龙魂暗金主题
// DNA: #龍芯⚡️2026-08-06-DARK-GOLD-THEME-V1.0-UID9622
// License: MulanPSL v2

import 'package:flutter/material.dart';
import 'colors.dart';
import 'text_styles.dart';

class LonghunTheme {
  static ThemeData get dark {
    return ThemeData(
      brightness: Brightness.dark,
      scaffoldBackgroundColor: LonghunColors.background,
      primaryColor: LonghunColors.gold,
      colorScheme: const ColorScheme.dark(
        primary: LonghunColors.gold,
        secondary: LonghunColors.goldLight,
        surface: LonghunColors.card,
        error: LonghunColors.red,
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: LonghunColors.background,
        elevation: 0, centerTitle: true,
        titleTextStyle: LonghunTextStyles.h1,
        iconTheme: IconThemeData(color: LonghunColors.gold),
      ),
      cardTheme: CardTheme(
        color: LonghunColors.card,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
          side: const BorderSide(color: LonghunColors.border, width: 1),
        ),
        elevation: 4,
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true, fillColor: LonghunColors.input,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(color: LonghunColors.border),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(color: LonghunColors.border),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(color: LonghunColors.gold, width: 2),
        ),
        labelStyle: LonghunTextStyles.bodySmall,
        hintStyle: LonghunTextStyles.bodySmall.copyWith(
          color: LonghunColors.textTertiary),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: LonghunColors.gold,
          foregroundColor: LonghunColors.background,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
          textStyle: LonghunTextStyles.button,
        ),
      ),
      dividerTheme: const DividerThemeData(
        color: LonghunColors.border, thickness: 1,
      ),
    );
  }
}
