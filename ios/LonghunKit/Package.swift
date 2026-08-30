// swift-tools-version: 5.9
// DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-IOS-PACKAGE-v1.0-UID9622
// CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 创建者: 诸葛鑫（UID9622）

import PackageDescription

let package = Package(
    name: "LonghunKit",
    platforms: [
        .iOS(.v17),
        .macOS(.v14),
        .watchOS(.v10),
    ],
    products: [
        .library(
            name: "LonghunKit",
            targets: ["LonghunKit"]
        ),
    ],
    targets: [
        // 龍魂国密底座（纯 C99 · 与鸿蒙 harmonyos-universe 同源 · 三端同一加密内核）
        .target(
            name: "CGuomi",
            path: "Sources/CGuomi",
            publicHeadersPath: ".",
            cSettings: [
                .headerSearchPath(".")
            ]
        ),
        .target(
            name: "LonghunKit",
            dependencies: ["CGuomi"],
            path: "Sources/LonghunKit",
            resources: [
                .process("Resources")
            ]
        ),
        .testTarget(
            name: "LonghunKitTests",
            dependencies: ["LonghunKit"],
            path: "Tests/LonghunKitTests"
        ),
    ]
)
