// 🐉 String扩展
// DNA: #龍芯⚡️2026-08-06-STRING-EXT-V1.0-UID9622
// License: MulanPSL v2

extension LonghunStringExtension on String {
  bool get isValidDNA => contains('UID9622') && contains('⚡️');
  String get toDNAIfValid => isValidDNA ? this : '';
}
