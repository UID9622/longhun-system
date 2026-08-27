#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂全球开发者平台 · 开发者民主化层 v1.0
DNA: #龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-DEV-DEMOCRATIZER-v1.0
创建者: 诸葛鑫（UID9622）
协议: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
核心理念:
  每个人都有权在这个世界留下痕迹。
  我们把「写第一行代码」的门槛降到最低。
  不需要懂编程——说出你想做什么，系统帮你生成并部署。
  DNA 一律走统一干支卦引擎。
"""

import json
import subprocess
import textwrap
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

from lh_dna import lh_dna

# 预置模板库：让任何人一行命令生成完整的 App 骨架
APP_TEMPLATES = {
    "todo": {
        "desc":    "待办事项 App（最经典的第一个 App）",
        "ios":     "SwiftUI · List + Checkbox + CoreData",
        "harmony": "ArkTS · List组件 + Checkbox + 关系型数据库",
    },
    "diary": {
        "desc":    "日记 App（每天留下自己的痕迹）",
        "ios":     "SwiftUI · TextEditor + LocalAuthentication",
        "harmony": "ArkTS · RichText组件 + 隐私保护",
    },
    "qrcode": {
        "desc":    "二维码生成器（让信息在世界流动）",
        "ios":     "SwiftUI · CoreImage.CIFilter.qrCodeGenerator",
        "harmony": "ArkTS · 条码生成能力API",
    },
    "voice_note": {
        "desc":    "语音备忘录（用声音留下痕迹）",
        "ios":     "SwiftUI · AVFoundation · SpeechRecognition",
        "harmony": "ArkTS · 音频录制API + 语音识别API",
    },
    "world_map": {
        "desc":    "全球足迹地图（标记你去过的地方）",
        "ios":     "SwiftUI · MapKit + CoreLocation",
        "harmony": "ArkTS · Map Kit + 位置服务",
    },
    "link_card": {
        "desc":    "个人名片 App（把自己介绍给全世界）",
        "ios":     "SwiftUI · ShareLink + QR码分享",
        "harmony": "ArkTS · 分享组件 + 原子化服务卡片",
    },
}


class DevDemocratizer:
    """
    开发者民主化层
    - 任何人输入一个想法，输出完整的双平台 App 骨架代码
    - 一键在 iOS 模拟器和 HarmonyOS 设备上同时预览
    - 每次生成都留下 DNA 痕迹
    """

    def __init__(self, output_dir: Optional[str] = None):
        self.out = Path(output_dir or
                        Path.home() / "longhun-system" / "global_dev_platform" / "projects")
        self.out.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _dna(name: str) -> str:
        """统一 DNA · 干支卦引擎"""
        return lh_dna(module="DEV-DEMO", action=name[:16].upper().replace(" ", "-"), version="v1.0")

    def list_templates(self) -> None:
        """展示所有可用模板"""
        print("\n🌍 龍魂全球开发者平台 · 应用模板库")
        print("   让每个人的第一个 App 从这里出发\n")
        for tid, info in APP_TEMPLATES.items():
            print(f"  [{tid:12s}] {info['desc']}")
            print(f"              iOS:     {info['ios']}")
            print(f"              Harmony: {info['harmony']}\n")

    def generate_ios_scaffold(self, app_name: str,
                              template_id: str,
                              author: str = "UID9622") -> str:
        """生成 SwiftUI App 骨架代码"""
        dna  = self._dna(app_name)
        tpl  = APP_TEMPLATES.get(template_id, APP_TEMPLATES["todo"])
        proj = self.out / f"{app_name}_iOS"
        proj.mkdir(parents=True, exist_ok=True)

        # ContentView.swift
        swift = textwrap.dedent(f"""\
            // {app_name} · iOS · 由龍魂全球开发者平台生成
            // DNA: {dna}
            // 创建者: {author}
            // 归属名: {author} · 龍芯北辰
            // 模板: {tpl['desc']}
            // 技术栈: {tpl['ios']}
            // 生成时间: {datetime.now().isoformat()}

            import SwiftUI

            @main
            struct {app_name.replace(' ','_')}App: App {{
                var body: some Scene {{
                    WindowGroup {{
                        ContentView()
                    }}
                }}
            }}

            struct ContentView: View {{
                // TODO: 在这里构建你的 {app_name}
                // 这是你在这个世界留下的第一行代码 🌍
                @State private var items: [String] = []
                @State private var newItem: String = ""

                var body: some View {{
                    NavigationStack {{
                        VStack {{
                            HStack {{
                                TextField("输入你的想法...", text: $newItem)
                                    .textFieldStyle(.roundedBorder)
                                Button("添加") {{
                                    if !newItem.isEmpty {{
                                        items.append(newItem)
                                        newItem = ""
                                    }}
                                }}
                            }}
                            .padding()

                            List(items, id: \\.self) {{ item in
                                Text(item)
                            }}
                        }}
                        .navigationTitle("{app_name}")
                        .navigationBarTitleDisplayMode(.large)
                    }}
                }}
            }}

            #Preview {{
                ContentView()
            }}
        """)
        (proj / "ContentView.swift").write_text(swift, "utf-8")

        # 写入 DNA 标记
        meta = {"app_name": app_name, "template": template_id,
                "platform": "iOS", "author": author,
                "dna": dna, "created": datetime.now().isoformat()}
        (proj / "lh_meta.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), "utf-8")

        print(f"  🍎 iOS 骨架已生成: {proj}")
        print(f"     DNA: {dna}")
        return str(proj)

    def generate_harmony_scaffold(self, app_name: str,
                                  template_id: str,
                                  author: str = "UID9622") -> str:
        """生成 ArkTS HarmonyOS App 骨架代码"""
        dna  = self._dna(app_name + "-HOS")
        tpl  = APP_TEMPLATES.get(template_id, APP_TEMPLATES["todo"])
        proj = self.out / f"{app_name}_HarmonyOS"
        proj.mkdir(parents=True, exist_ok=True)

        # Index.ets (ArkTS 入口页)
        arkts = textwrap.dedent(f"""\
            // {app_name} · HarmonyOS · 由龍魂全球开发者平台生成
            // DNA: {dna}
            // 创建者: {author}
            // 归属名: {author} · 龍芯北辰
            // 模板: {tpl['desc']}
            // 技术栈: {tpl['harmony']}
            // 生成时间: {datetime.now().isoformat()}

            import router from '@ohos.router';

            @Entry
            @Component
            struct Index {{
              // 这是你在这个世界留下的第一行代码 🌍
              @State items: string[] = []
              @State newItem: string = ''

              build() {{
                Column() {{
                  Row() {{
                    TextInput({{ placeholder: '输入你的想法...', text: this.newItem }})
                      .onChange((value: string) => {{
                        this.newItem = value
                      }})
                      .width('75%')

                    Button('添加')
                      .onClick(() => {{
                        if (this.newItem.length > 0) {{
                          this.items.push(this.newItem)
                          this.newItem = ''
                        }}
                      }})
                      .width('20%')
                  }}
                  .width('100%')
                  .padding(12)

                  List({{ space: 8 }}) {{
                    ForEach(this.items, (item: string) => {{
                      ListItem() {{
                        Text(item)
                          .width('100%')
                          .padding(12)
                          .backgroundColor('#F5F5F5')
                          .borderRadius(8)
                      }}
                    }})
                  }}
                  .width('100%')
                  .padding({{ left: 12, right: 12 }})
                }}
                .width('100%')
                .height('100%')
                .justifyContent(FlexAlign.Start)
              }}
            }}
        """)
        (proj / "Index.ets").write_text(arkts, "utf-8")

        meta = {"app_name": app_name, "template": template_id,
                "platform": "HarmonyOS", "author": author,
                "dna": dna, "created": datetime.now().isoformat()}
        (proj / "lh_meta.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), "utf-8")

        print(f"  🤖 HarmonyOS 骨架已生成: {proj}")
        print(f"     DNA: {dna}")
        return str(proj)

    def generate_both(self, app_name: str,
                      template_id: str = "todo",
                      author: str = "UID9622") -> Dict[str, str]:
        """一次生成 iOS + HarmonyOS 双平台骨架"""
        print(f"\n🌍 正在为 [{author}] 生成双平台 App: {app_name}\n")
        ios_path = self.generate_ios_scaffold(app_name, template_id, author)
        hos_path = self.generate_harmony_scaffold(app_name, template_id, author)
        print(f"""
✅ 双平台骨架生成完毕！

   🍎 iOS 项目:      {ios_path}
   📱 HarmonyOS 项目: {hos_path}

   下一步:
   1. 用 Xcode 打开 iOS 项目，按 ▶ 运行
   2. 用 DevEco Studio 打开 HarmonyOS 项目，点 Run
   3. 你的第一个 App 就活了 🚀

   每次构建都有 DNA，你的创作永远有迹可查 🐉
        """)
        return {"ios": ios_path, "harmony": hos_path}


if __name__ == "__main__":
    demo = DevDemocratizer()
    demo.list_templates()
    # 生成你的第一个双平台 App
    result = demo.generate_both(
        app_name    = "龍魂笔记",
        template_id = "diary",
        author      = "UID9622"
    )
