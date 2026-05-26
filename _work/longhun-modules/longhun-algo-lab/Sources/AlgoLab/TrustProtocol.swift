import Foundation
import CryptoKit

struct CreatorIdentity {
    let creatorID: String
    let privateKey: P256.Signing.PrivateKey

    var publicKeyData: Data {
        privateKey.publicKey.rawRepresentation
    }
}

struct CreationRecord {
    let creatorID: String
    let content: String
    let timestamp: Date
    let signature: Data
    let publicKey: Data

    var shortSignature: String {
        String(signature.base64EncodedString().prefix(24)) + "..."
    }
}

struct UsagePolicy: Codable {
    var allowRedistribute: Bool
    var allowTraining: Bool
    var ownerOnly: Bool
}

struct ProtocolProof {
    let dnaTag: String
    let record: CreationRecord
    let policy: UsagePolicy
    let verified: Bool

    var summary: String {
        "\(dnaTag) | \(verified ? "PASS" : "FAIL")"
    }
}

struct PortableProof: Codable {
    let dnaTag: String
    let creatorID: String
    let content: String
    let timestamp: TimeInterval
    let signatureBase64: String
    let publicKeyBase64: String
    let allowRedistribute: Bool
    let allowTraining: Bool
    let ownerOnly: Bool
}

enum TrustProtocol {
    private static let creatorIDKey = "trust_protocol_creator_id"
    private static let privateKeyKey = "trust_protocol_private_key"

    static func loadOrCreateIdentity() -> CreatorIdentity {
        let defaults = UserDefaults.standard

        if
            let creatorID = defaults.string(forKey: creatorIDKey),
            let privateKeyData = defaults.data(forKey: privateKeyKey),
            let privateKey = try? P256.Signing.PrivateKey(rawRepresentation: privateKeyData)
        {
            return CreatorIdentity(creatorID: creatorID, privateKey: privateKey)
        }

        let privateKey = P256.Signing.PrivateKey()
        let creatorIDSeed = UUID().uuidString.replacingOccurrences(of: "-", with: "")
        let creatorID = "DNA-" + String(creatorIDSeed.prefix(12))

        defaults.set(creatorID, forKey: creatorIDKey)
        defaults.set(privateKey.rawRepresentation, forKey: privateKeyKey)

        return CreatorIdentity(creatorID: creatorID, privateKey: privateKey)
    }

    static func sign(content: String, by identity: CreatorIdentity) -> CreationRecord? {
        let timestamp = Date()
        guard let payload = payloadData(content: content, creatorID: identity.creatorID, timestamp: timestamp) else {
            return nil
        }

        guard let signature = try? identity.privateKey.signature(for: payload) else {
            return nil
        }

        return CreationRecord(
            creatorID: identity.creatorID,
            content: content,
            timestamp: timestamp,
            signature: signature.rawRepresentation,
            publicKey: identity.publicKeyData
        )
    }

    static func verify(_ record: CreationRecord) -> Bool {
        guard let publicKey = try? P256.Signing.PublicKey(rawRepresentation: record.publicKey) else {
            return false
        }
        guard let signature = try? P256.Signing.ECDSASignature(rawRepresentation: record.signature) else {
            return false
        }
        guard let payload = payloadData(content: record.content, creatorID: record.creatorID, timestamp: record.timestamp) else {
            return false
        }
        return publicKey.isValidSignature(signature, for: payload)
    }

    static func createProof(
        content: String,
        topic: String,
        version: String,
        identity: CreatorIdentity,
        policy: UsagePolicy
    ) -> ProtocolProof? {
        guard let record = sign(content: content, by: identity) else {
            return nil
        }
        let date = dateString(from: record.timestamp)
        let normalizedTopic = topic.replacingOccurrences(of: " ", with: "-").uppercased()
        let dnaTag = dnaTag(date: date, topic: normalizedTopic, version: version)
        let result = verify(record)
        return ProtocolProof(dnaTag: dnaTag, record: record, policy: policy, verified: result)
    }

    static func exportJSON(_ proof: ProtocolProof) -> String? {
        let portable = PortableProof(
            dnaTag: proof.dnaTag,
            creatorID: proof.record.creatorID,
            content: proof.record.content,
            timestamp: proof.record.timestamp.timeIntervalSince1970,
            signatureBase64: proof.record.signature.base64EncodedString(),
            publicKeyBase64: proof.record.publicKey.base64EncodedString(),
            allowRedistribute: proof.policy.allowRedistribute,
            allowTraining: proof.policy.allowTraining,
            ownerOnly: proof.policy.ownerOnly
        )

        let encoder = JSONEncoder()
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        guard let data = try? encoder.encode(portable) else { return nil }
        return String(data: data, encoding: .utf8)
    }

    static func importAndVerifyJSON(_ text: String) -> ProtocolProof? {
        guard let data = text.data(using: .utf8) else { return nil }
        guard let portable = try? JSONDecoder().decode(PortableProof.self, from: data) else { return nil }
        guard let signature = Data(base64Encoded: portable.signatureBase64) else { return nil }
        guard let publicKey = Data(base64Encoded: portable.publicKeyBase64) else { return nil }

        let record = CreationRecord(
            creatorID: portable.creatorID,
            content: portable.content,
            timestamp: Date(timeIntervalSince1970: portable.timestamp),
            signature: signature,
            publicKey: publicKey
        )
        let policy = UsagePolicy(
            allowRedistribute: portable.allowRedistribute,
            allowTraining: portable.allowTraining,
            ownerOnly: portable.ownerOnly
        )
        let result = verify(record)
        return ProtocolProof(dnaTag: portable.dnaTag, record: record, policy: policy, verified: result)
    }

    private static func dnaTag(date: String, topic: String, version: String) -> String {
        let raw = "\(topic)\(date)\(version)"
        let digest = SHA256.hash(data: Data(raw.utf8))
        let hex = digest.compactMap { String(format: "%02x", $0) }.joined()
        let sha8 = String(hex.prefix(8))
        return "#龍芯⚡️\(date)|\(topic)|\(version)|\(sha8)"
    }

    private static func dateString(from date: Date) -> String {
        let formatter = DateFormatter()
        formatter.calendar = Calendar(identifier: .gregorian)
        formatter.locale = Locale(identifier: "zh_CN")
        formatter.timeZone = TimeZone.current
        formatter.dateFormat = "yyyyMMdd"
        return formatter.string(from: date)
    }

    private static func payloadData(content: String, creatorID: String, timestamp: Date) -> Data? {
        let payload = "\(creatorID)|\(Int(timestamp.timeIntervalSince1970))|\(content)"
        return payload.data(using: .utf8)
    }
}
