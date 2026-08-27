// DNA: #龍芯⚡️丙午·丙申·辛未·未时·䷕贲-TOUCHID-GATE-v1.0
// 创建者: 诸葛鑫（UID9622）
// 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 指纹门 · 触发 macOS Touch ID / 密码验证，成功 exit 0
// 用法: lh_touchid_gate "验证原因"
import Foundation
import LocalAuthentication

let reason = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "龍魂变量环境调用"

let context = LAContext()
var policyError: NSError?
guard context.canEvaluatePolicy(.deviceOwnerAuthentication, error: &policyError) else {
    fputs("UNAVAILABLE: \(policyError?.localizedDescription ?? "unknown")\n", stderr)
    exit(2)
}

context.evaluatePolicy(.deviceOwnerAuthentication, localizedReason: reason) { success, error in
    if success {
        exit(0)
    } else {
        fputs("DENIED: \(error?.localizedDescription ?? "unknown")\n", stderr)
        exit(1)
    }
}

RunLoop.main.run()
