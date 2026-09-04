// 🐉 龙魂·自定义异常
// DNA: #龍芯⚡️2026-08-06-BRIDGE-EXCEPTIONS-V1.0-UID9622
// License: MulanPSL v2

/// 龙魂基础异常
class LonghunException implements Exception {
  final String message;
  final String? code;
  final dynamic data;

  LonghunException(this.message, {this.code, this.data});

  @override
  String toString() => 'LonghunException: $message (code: $code)';
}

/// 主权验证异常
class SovereigntyException extends LonghunException {
  SovereigntyException(String message, {String? code, dynamic data})
      : super(message, code: code ?? 'SOVEREIGNTY_ERROR', data: data);
}

/// DNA生成异常
class DNAException extends LonghunException {
  DNAException(String message, {String? code, dynamic data})
      : super(message, code: code ?? 'DNA_ERROR', data: data);
}

/// 审计异常
class AuditException extends LonghunException {
  AuditException(String message, {String? code, dynamic data})
      : super(message, code: code ?? 'AUDIT_ERROR', data: data);
}

/// 通道通信异常
class ChannelException extends LonghunException {
  ChannelException(String message, {String? code, dynamic data})
      : super(message, code: code ?? 'CHANNEL_ERROR', data: data);
}
