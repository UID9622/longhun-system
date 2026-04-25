// swift-tools-version: 5.9
// 龍魂·算法可视化工场 · UID9622
import PackageDescription

let package = Package(
    name: "AlgoLab",
    platforms: [.macOS(.v13)],
    targets: [
        .executableTarget(
            name: "AlgoLab",
            path: "Sources/AlgoLab"
        )
    ]
)
