// 🐉 Context扩展
// DNA: #龍芯⚡️2026-08-06-CONTEXT-EXT-V1.0-UID9622
// License: MulanPSL v2

import 'package:flutter/material.dart';
import '../theme/colors.dart';
import '../theme/text_styles.dart';

extension LonghunContextExtension on BuildContext {
  ThemeData get longhunTheme => Theme.of(this);
  bool get isLonghunDark => Theme.of(this).brightness == Brightness.dark;
  void showLonghunSnack(String msg, {Color? color}) {
    ScaffoldMessenger.of(this).showSnackBar(SnackBar(
      content: Text(msg, style: LonghunTextStyles.bodyMedium),
      backgroundColor: color ?? LonghunColors.card,
      behavior: SnackBarBehavior.floating,
    ));
  }
}
