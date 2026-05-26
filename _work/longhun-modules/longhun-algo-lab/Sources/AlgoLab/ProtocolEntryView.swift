import SwiftUI

@MainActor
final class ProtocolEntryVM: ObservableObject {
    @Published var identity: CreatorIdentity
    @Published var topic: String = "PROTOCOL"
    @Published var version: String = "v1.0"
    @Published var content: String = "我的第一条原创内容"
    @Published var allowRedistribute = false
    @Published var allowTraining = false
    @Published var ownerOnly = true
    @Published var lastProof: ProtocolProof?
    @Published var exportedJSON: String = ""
    @Published var importJSON: String = ""
    @Published var importResult: String = ""

    init(identity: CreatorIdentity = TrustProtocol.loadOrCreateIdentity()) {
        self.identity = identity
    }

    func runSingleEntry() {
        let trimmed = content.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else { return }

        let policy = UsagePolicy(
            allowRedistribute: allowRedistribute,
            allowTraining: allowTraining,
            ownerOnly: ownerOnly
        )

        lastProof = TrustProtocol.createProof(
            content: trimmed,
            topic: topic,
            version: version,
            identity: identity,
            policy: policy
        )

        if let proof = lastProof {
            exportedJSON = TrustProtocol.exportJSON(proof) ?? ""
        }
    }

    func verifyImportedJSON() {
        let trimmed = importJSON.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else {
            importResult = "请先粘贴凭证 JSON"
            return
        }

        guard let proof = TrustProtocol.importAndVerifyJSON(trimmed) else {
            importResult = "导入失败：JSON 格式不正确"
            return
        }

        let verdict = proof.verified ? "验真通过" : "验真失败"
        importResult = "\(verdict) | 作者: \(proof.record.creatorID) | DNA: \(proof.dnaTag)"
    }
}

struct ProtocolEntryView: View {
    @StateObject private var vm = ProtocolEntryVM()

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("🛡 协议单入口")
                .font(.system(size: 12, weight: .black))
                .foregroundColor(T.gold)

            Text("Step1 身份: \(vm.identity.creatorID)")
                .font(.system(size: 10, design: .monospaced))
                .foregroundColor(T.sub)

            HStack(spacing: 8) {
                TextField("TOPIC", text: $vm.topic)
                    .textFieldStyle(.roundedBorder)
                TextField("VERSION", text: $vm.version)
                    .textFieldStyle(.roundedBorder)
                    .frame(width: 100)
            }

            TextField("输入原创内容", text: $vm.content)
                .textFieldStyle(.roundedBorder)

            HStack(spacing: 14) {
                Toggle("允许转载", isOn: $vm.allowRedistribute)
                    .toggleStyle(.checkbox)
                Toggle("允许训练", isOn: $vm.allowTraining)
                    .toggleStyle(.checkbox)
                Toggle("仅本人可用", isOn: $vm.ownerOnly)
                    .toggleStyle(.checkbox)
            }
            .font(.system(size: 11))
            .foregroundColor(T.sub)

            Button(action: vm.runSingleEntry) {
                Label("Step2+3 一键确权并验证", systemImage: "checkmark.shield.fill")
                    .font(.system(size: 11, weight: .semibold))
                    .padding(.horizontal, 10)
                    .padding(.vertical, 6)
                    .background(T.gold.opacity(0.16))
                    .foregroundColor(T.gold)
                    .clipShape(RoundedRectangle(cornerRadius: 7))
            }
            .buttonStyle(.plain)

            if let proof = vm.lastProof {
                Text("结果: \(proof.verified ? "通过" : "失败")")
                    .font(.system(size: 11, weight: .bold))
                    .foregroundColor(proof.verified ? T.green : T.red)

                Text("DNA: \(proof.dnaTag)")
                    .font(.system(size: 10, design: .monospaced))
                    .foregroundColor(T.sub)
                    .lineLimit(2)

                Text("签名: \(proof.record.shortSignature)")
                    .font(.system(size: 10, design: .monospaced))
                    .foregroundColor(T.sub)
                    .lineLimit(1)
            }

            Text("导出凭证 JSON")
                .font(.system(size: 11, weight: .bold))
                .foregroundColor(T.sub)
            TextEditor(text: $vm.exportedJSON)
                .font(.system(size: 10, design: .monospaced))
                .frame(height: 110)
                .overlay(RoundedRectangle(cornerRadius: 6).stroke(T.border, lineWidth: 1))

            Text("导入凭证 JSON 并验真")
                .font(.system(size: 11, weight: .bold))
                .foregroundColor(T.sub)
            TextEditor(text: $vm.importJSON)
                .font(.system(size: 10, design: .monospaced))
                .frame(height: 110)
                .overlay(RoundedRectangle(cornerRadius: 6).stroke(T.border, lineWidth: 1))

            Button("验证导入凭证", action: vm.verifyImportedJSON)
                .buttonStyle(.bordered)

            if !vm.importResult.isEmpty {
                Text(vm.importResult)
                    .font(.system(size: 10, design: .monospaced))
                    .foregroundColor(T.sub)
                    .lineLimit(2)
            }
        }
    }
}
