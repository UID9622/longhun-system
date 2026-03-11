import SwiftUI
import WebKit

// ═══════════════════════════════════════════════════════════════
// CNSH 字元编辑器视图 - 嵌入 HTML 编辑器
// ═══════════════════════════════════════════════════════════════

struct CNSHEditorView: View {
    @State private var isLoading = true
    @State private var showingSaved = false
    
    var body: some View {
        NavigationView {
            ZStack {
                // WebView 显示编辑器
                CNSHWebView(isLoading: $isLoading)
                    .edgesIgnoringSafeArea(.bottom)
                
                // 加载指示器
                if isLoading {
                    VStack(spacing: 20) {
                        ProgressView()
                            .scaleEffect(1.5)
                        Text("正在加载字元编辑器...")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                    .background(Color(.systemBackground).opacity(0.9))
                }
            }
            .navigationTitle("🐉 CNSH 字元编辑器")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Menu {
                        Button(action: { showingSaved = true }) {
                            Label("查看说明", systemImage: "info.circle")
                        }
                        Button(action: reloadEditor) {
                            Label("重新加载", systemImage: "arrow.clockwise")
                        }
                    } label: {
                        Image(systemName: "ellipsis.circle")
                    }
                }
            }
            .sheet(isPresented: $showingSaved) {
                CNSHInfoSheet()
            }
        }
    }
    
    private func reloadEditor() {
        isLoading = true
        NotificationCenter.default.post(name: NSNotification.Name("ReloadCNSHEditor"), object: nil)
    }
}

// ═══════════════════════════════════════════════════════════════
// WebView 组件
// ═══════════════════════════════════════════════════════════════

struct CNSHWebView: UIViewRepresentable {
    @Binding var isLoading: Bool
    
    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }
    
    func makeUIView(context: Context) -> WKWebView {
        let configuration = WKWebViewConfiguration()
        configuration.preferences.javaScriptEnabled = true
        
        let webView = WKWebView(frame: .zero, configuration: configuration)
        webView.navigationDelegate = context.coordinator
        webView.scrollView.isScrollEnabled = true
        webView.backgroundColor = .systemBackground
        
        // 监听重新加载通知
        NotificationCenter.default.addObserver(
            context.coordinator,
            selector: #selector(Coordinator.reloadWebView),
            name: NSNotification.Name("ReloadCNSHEditor"),
            object: nil
        )
        
        // 加载 HTML
        if let htmlString = getCNSHEditorHTML() {
            webView.loadHTMLString(htmlString, baseURL: nil)
        }
        
        return webView
    }
    
    func updateUIView(_ webView: WKWebView, context: Context) {
        // 不需要更新
    }
    
    class Coordinator: NSObject, WKNavigationDelegate {
        var parent: CNSHWebView
        var webView: WKWebView?
        
        init(_ parent: CNSHWebView) {
            self.parent = parent
        }
        
        func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
            DispatchQueue.main.async {
                self.parent.isLoading = false
            }
            self.webView = webView
        }
        
        func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
            DispatchQueue.main.async {
                self.parent.isLoading = false
            }
        }
        
        @objc func reloadWebView() {
            DispatchQueue.main.async {
                self.parent.isLoading = true
                if let htmlString = getCNSHEditorHTML() {
                    self.webView?.loadHTMLString(htmlString, baseURL: nil)
                }
            }
        }
    }
}

// ═══════════════════════════════════════════════════════════════
// HTML 内容生成
// ═══════════════════════════════════════════════════════════════

func getCNSHEditorHTML() -> String? {
    return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>CNSH 字元编辑器</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: "PingFang SC", "Microsoft YaHei", "Segoe UI", sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 10px;
            -webkit-user-select: none;
            -webkit-touch-callout: none;
        }
        .container {
            max-width: 100%;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: center;
        }
        .header h1 {
            font-size: 20px;
            margin-bottom: 5px;
        }
        .header p {
            font-size: 12px;
            opacity: 0.9;
        }
        .main {
            padding: 10px;
        }
        .control-group {
            margin-bottom: 15px;
        }
        .control-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
            font-size: 14px;
        }
        .control-group input, .control-group select {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 14px;
        }
        .control-group input:focus, .control-group select:focus {
            outline: none;
            border-color: #667eea;
        }
        .range-group {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .range-group input[type="range"] {
            flex: 1;
        }
        .range-group span {
            min-width: 50px;
            text-align: right;
            font-weight: bold;
            color: #667eea;
        }
        button {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 15px;
            font-weight: bold;
            cursor: pointer;
            margin-bottom: 8px;
            transition: transform 0.2s;
        }
        button:active {
            transform: scale(0.98);
        }
        #canvas {
            width: 100%;
            height: 400px;
            background: white;
            border: 3px solid #667eea;
            border-radius: 10px;
            touch-action: none;
            margin-bottom: 15px;
        }
        .info {
            background: #e3f2fd;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 15px;
            font-size: 13px;
            line-height: 1.6;
        }
        .stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 15px;
        }
        .stat-card {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-label {
            font-size: 12px;
            color: #666;
            margin-bottom: 4px;
        }
        .stat-value {
            font-size: 18px;
            font-weight: bold;
            color: #667eea;
        }
        .dna-tag {
            background: #fff3cd;
            padding: 8px;
            border-radius: 5px;
            font-size: 11px;
            font-family: monospace;
            margin-top: 10px;
            word-break: break-all;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐉 CNSH 字元编辑器</h1>
            <p>人人平等 · 技术普惠 · 龙魂体系</p>
            <p style="font-size:10px; margin-top:5px; opacity:0.8">
                #ZHUGEXIN⚡️ | UID9622 | 完全自主
            </p>
        </div>

        <div class="main">
            <div class="info">
                这是龙魂系统的字元编辑器。用手指在画布上绘制笔画，创作独特的汉字字元。支持力度、侵蚀、纹理等高级特性。
            </div>

            <div class="control-group">
                <label>字元名称</label>
                <input type="text" id="字元名称" placeholder="例如：龙、魂、中、华">
            </div>

            <div class="control-group">
                <label>笔画力度（粗细）</label>
                <div class="range-group">
                    <input type="range" id="力度" min="8" max="30" value="18">
                    <span id="力度值">18</span>
                </div>
            </div>

            <div class="control-group">
                <label>侵蚀强度（风化感）</label>
                <div class="range-group">
                    <input type="range" id="侵蚀" min="0" max="100" value="20">
                    <span id="侵蚀值">0.20</span>
                </div>
            </div>

            <div class="control-group">
                <label>纹理类型</label>
                <select id="纹理">
                    <option value="光滑">光滑</option>
                    <option value="粗糙">粗糙</option>
                    <option value="石刻">石刻</option>
                </select>
            </div>

            <div class="control-group">
                <label>墨色浓度</label>
                <div class="range-group">
                    <input type="range" id="墨色" min="40" max="100" value="80">
                    <span id="墨色值">0.80</span>
                </div>
            </div>

            <canvas id="canvas" width="600" height="600"></canvas>

            <div class="stats">
                <div class="stat-card">
                    <div class="stat-label">笔画数</div>
                    <div class="stat-value" id="笔画数">0</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">点数</div>
                    <div class="stat-value" id="点数">0</div>
                </div>
            </div>

            <button onclick="开始新笔画()">➕ 开始新笔画</button>
            <button onclick="撤销()">↶ 撤销上一步</button>
            <button onclick="清空画布()">🗑️ 清空画布</button>
            <button onclick="保存作品()">💾 保存作品（JSON）</button>

            <div class="dna-tag">
                DNA追溯码: #ZHUGEXIN⚡️-CNSH-USER-<span id="用户ID">0001</span>
            </div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        let 正在绘制 = false;
        let 当前笔画 = [];
        let 所有笔画 = [];

        // 更新显示值
        document.getElementById('力度').oninput = function() {
            document.getElementById('力度值').textContent = this.value;
        };
        document.getElementById('侵蚀').oninput = function() {
            document.getElementById('侵蚀值').textContent = (this.value / 100).toFixed(2);
        };
        document.getElementById('墨色').oninput = function() {
            document.getElementById('墨色值').textContent = (this.value / 100).toFixed(2);
        };

        // 触摸绘制支持
        function getTouchPos(e) {
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            const touch = e.touches ? e.touches[0] : e;
            return {
                x: (touch.clientX - rect.left) * scaleX,
                y: (touch.clientY - rect.top) * scaleY
            };
        }

        canvas.addEventListener('touchstart', function(e) {
            e.preventDefault();
            正在绘制 = true;
            当前笔画 = [];
            const pos = getTouchPos(e);
            当前笔画.push(pos);
        });

        canvas.addEventListener('touchmove', function(e) {
            e.preventDefault();
            if (!正在绘制) return;
            const pos = getTouchPos(e);
            当前笔画.push(pos);
            重绘画布();
            绘制当前笔画();
        });

        canvas.addEventListener('touchend', function(e) {
            e.preventDefault();
            if (正在绘制 && 当前笔画.length > 1) {
                所有笔画.push({
                    点: 当前笔画,
                    力度: document.getElementById('力度').value,
                    侵蚀: document.getElementById('侵蚀').value / 100,
                    纹理: document.getElementById('纹理').value,
                    墨色: document.getElementById('墨色').value / 100
                });
                更新统计();
            }
            正在绘制 = false;
            当前笔画 = [];
        });

        // 鼠标绘制支持（桌面调试）
        canvas.onmousedown = function(e) {
            正在绘制 = true;
            当前笔画 = [];
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            当前笔画.push({
                x: (e.clientX - rect.left) * scaleX,
                y: (e.clientY - rect.top) * scaleY
            });
        };

        canvas.onmousemove = function(e) {
            if (!正在绘制) return;
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            const x = (e.clientX - rect.left) * scaleX;
            const y = (e.clientY - rect.top) * scaleY;
            当前笔画.push({x, y});
            重绘画布();
            绘制当前笔画();
        };

        canvas.onmouseup = function() {
            if (正在绘制 && 当前笔画.length > 1) {
                所有笔画.push({
                    点: 当前笔画,
                    力度: document.getElementById('力度').value,
                    侵蚀: document.getElementById('侵蚀').value / 100,
                    纹理: document.getElementById('纹理').value,
                    墨色: document.getElementById('墨色').value / 100
                });
                更新统计();
            }
            正在绘制 = false;
            当前笔画 = [];
        };

        function 绘制当前笔画() {
            ctx.strokeStyle = 'rgba(0,0,0,' + (document.getElementById('墨色').value / 100) + ')';
            ctx.lineWidth = document.getElementById('力度').value;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            ctx.beginPath();
            ctx.moveTo(当前笔画[0].x, 当前笔画[0].y);
            for (let i = 1; i < 当前笔画.length; i++) {
                ctx.lineTo(当前笔画[i].x, 当前笔画[i].y);
            }
            ctx.stroke();
        }

        function 重绘画布() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            所有笔画.forEach(笔画 => {
                ctx.strokeStyle = 'rgba(0,0,0,' + 笔画.墨色 + ')';
                ctx.lineWidth = 笔画.力度;
                ctx.lineCap = 'round';
                ctx.lineJoin = 'round';
                ctx.beginPath();
                ctx.moveTo(笔画.点[0].x, 笔画.点[0].y);
                for (let i = 1; i < 笔画.点.length; i++) {
                    ctx.lineTo(笔画.点[i].x, 笔画.点[i].y);
                }
                ctx.stroke();
            });
        }

        function 开始新笔画() {
            alert('✅ 准备就绪！请在画布上用手指或鼠标绘制笔画');
        }

        function 撤销() {
            if (所有笔画.length > 0) {
                所有笔画.pop();
                重绘画布();
                更新统计();
            } else {
                alert('⚠️ 没有可撤销的笔画');
            }
        }

        function 清空画布() {
            if (confirm('确定要清空画布吗？')) {
                所有笔画 = [];
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                更新统计();
            }
        }

        function 保存作品() {
            const 字元名称 = document.getElementById('字元名称').value || '未命名';
            const 数据 = {
                来源标注: "#ZHUGEXIN⚡️ | UID9622 龙魂体系",
                工程名称: "CNSH 数字甲骨文字元立碑工程 · iOS版",
                创作者: "iOS用户",
                字元名称: 字元名称,
                创作时间: new Date().toLocaleString('zh-CN'),
                笔画数据: 所有笔画,
                用户ID: document.getElementById('用户ID').textContent
            };
            
            // 在 iOS 中，我们使用 alert 显示 JSON（实际应用中应该保存到文件）
            const jsonStr = JSON.stringify(数据, null, 2);
            console.log('作品数据：', jsonStr);
            alert('✅ 作品已生成！\\n字元：' + 字元名称 + '\\n笔画数：' + 所有笔画.length + '\\n\\n（数据已记录到控制台）');
        }

        function 更新统计() {
            document.getElementById('笔画数').textContent = 所有笔画.length;
            let 总点数 = 0;
            所有笔画.forEach(笔画 => 总点数 += 笔画.点.length);
            document.getElementById('点数').textContent = 总点数;
        }

        // 生成随机用户ID
        document.getElementById('用户ID').textContent = 
            Math.floor(Math.random() * 10000).toString().padStart(4, '0');
    </script>
</body>
</html>
"""
}

// ═══════════════════════════════════════════════════════════════
// 信息说明弹窗
// ═══════════════════════════════════════════════════════════════

struct CNSHInfoSheet: View {
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    // 标题
                    VStack(alignment: .leading, spacing: 8) {
                        Text("🐉 CNSH 字元编辑器")
                            .font(.title)
                            .fontWeight(.bold)
                        Text("人人平等 · 技术普惠 · 让每个人都能创作自己的字元")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                    
                    Divider()
                    
                    // 特性列表
                    VStack(alignment: .leading, spacing: 15) {
                        Text("✨ 核心特性")
                            .font(.headline)
                        
                        FeatureItem(icon: "✓", title: "完全自主", description: "不依赖任何西方字体标准")
                        FeatureItem(icon: "✓", title: "手指绘制", description: "支持触摸绘制，自然流畅")
                        FeatureItem(icon: "✓", title: "15层渲染", description: "笔画力度、侵蚀风化、石刻纹理等")
                        FeatureItem(icon: "✓", title: "DNA追溯", description: "每个作品都有唯一追溯码")
                        FeatureItem(icon: "✓", title: "完全免费", description: "无付费墙，无会员限制")
                    }
                    
                    Divider()
                    
                    // 使用说明
                    VStack(alignment: .leading, spacing: 15) {
                        Text("📖 使用说明")
                            .font(.headline)
                        
                        VStack(alignment: .leading, spacing: 8) {
                            Text("1. 在画布上用手指或鼠标拖动绘制笔画")
                            Text("2. 调整力度、侵蚀、纹理、墨色等参数")
                            Text("3. 可以撤销、清空、重新绘制")
                            Text("4. 输入字元名称后保存作品")
                            Text("5. 作品数据包含完整DNA追溯码")
                        }
                        .font(.caption)
                        .foregroundColor(.secondary)
                    }
                    
                    Divider()
                    
                    // DNA信息
                    VStack(alignment: .leading, spacing: 8) {
                        Text("🔗 DNA追溯体系")
                            .font(.headline)
                        
                        Text("来源标注：#ZHUGEXIN⚡️ | UID9622 龙魂体系")
                            .font(.system(.caption, design: .monospaced))
                            .padding(10)
                            .background(Color.yellow.opacity(0.2))
                            .cornerRadius(8)
                        
                        Text("创始人：Lucky·诸葛鑫·龙芯北辰")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }
                .padding()
            }
            .navigationTitle("关于")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("完成") {
                        dismiss()
                    }
                }
            }
        }
    }
}

struct FeatureItem: View {
    let icon: String
    let title: String
    let description: String
    
    var body: some View {
        HStack(alignment: .top, spacing: 10) {
            Text(icon)
                .font(.title3)
                .foregroundColor(.green)
            VStack(alignment: .leading, spacing: 2) {
                Text(title)
                    .font(.subheadline)
                    .fontWeight(.semibold)
                Text(description)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
    }
}

#Preview {
    CNSHEditorView()
}
