import SwiftUI

// ═══════════════════════════════════════════════════════════════
// 龍魂数据主权防御工具 iOS 版本 v1.0 - 主应用文件
// Longhun Data Sovereignty Defense Toolkit for iOS
// 包含 CNSH 字元编辑器
// ═══════════════════════════════════════════════════════════════

@main
struct LonghunDefenseApp: App {
    @StateObject private var appState = AppState()
    
    var body: some Scene {
        WindowGroup {
            MainContentView()
                .environmentObject(appState)
        }
    }
}

// ═══════════════════════════════════════════════════════════════
// 【核心常量】P0-ETERNAL 永恒不变
// ═══════════════════════════════════════════════════════════════

struct Constants {
    // 创始人锚点（永远不可修改）
    static let founderUID = "UID9622"
    static let founderName = "Lucky·诸葛鑫·龍芯北辰"
    static let founderGPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
    static let founderConfirmationCode = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    
    // 数字人民币激活账号（P0-ETERNAL保护）
    static let ecnyAccount = "0061901030627652"
    static let ecnyBank = "微众银行"
    static let networkIdentity = "T38C89R75U"
    
    // DNA前缀
    static let dnaPrefix = "#ZHUGEXIN⚡️"
    
    // 版本信息
    static let toolkitVersion = "v1.0"
    static let toolkitDNA = "\(dnaPrefix)20260227-DATA-SOVEREIGNTY-DEFENSE-TOOLKIT-\(toolkitVersion)"
    
    // 激活配置
    static let ecnyActivationPrefix = "e-CNY-"
    static let tempDNAValidityDays = 365
}

// ═══════════════════════════════════════════════════════════════
// 【应用状态管理】
// ═══════════════════════════════════════════════════════════════

@MainActor
class AppState: ObservableObject {
    @Published var ecnySystem: ECNYActivationSystem
    @Published var ruleEngine: DataSovereigntyRuleEngine
    @Published var selectedTab = 0
    
    init() {
        self.ecnySystem = ECNYActivationSystem()
        self.ruleEngine = DataSovereigntyRuleEngine()
    }
}

// ═══════════════════════════════════════════════════════════════
// 【主界面 - 包含 CNSH 编辑器】
// ═══════════════════════════════════════════════════════════════

struct MainContentView: View {
    @EnvironmentObject var appState: AppState
    
    var body: some View {
        TabView(selection: $appState.selectedTab) {
            HomeView()
                .tabItem {
                    Label("主页", systemImage: "house.fill")
                }
                .tag(0)
            
            ActivationView()
                .tabItem {
                    Label("激活", systemImage: "creditcard.fill")
                }
                .tag(1)
            
            DNAGeneratorView()
                .tabItem {
                    Label("DNA", systemImage: "lock.shield.fill")
                }
                .tag(2)
            
            RulesView()
                .tabItem {
                    Label("规则", systemImage: "list.bullet.rectangle")
                }
                .tag(3)
            
            DefenseView()
                .tabItem {
                    Label("防御", systemImage: "shield.checkered")
                }
                .tag(4)
            
            CNSHEditorView()
                .tabItem {
                    Label("字元", systemImage: "pencil.and.outline")
                }
                .tag(5)
        }
        .accentColor(.blue)
    }
}

// ═══════════════════════════════════════════════════════════════
// 【主页视图】
// ═══════════════════════════════════════════════════════════════

struct HomeView: View {
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // 横幅
                    BannerView()
                    
                    // 核心原则
                    CorePrinciplesView()
                    
                    // 系统信息
                    SystemInfoView()
                    
                    // CNSH 编辑器入口
                    CNSHEntryCard()
                }
                .padding()
            }
            .navigationTitle("龍魂防御工具")
        }
    }
}

struct BannerView: View {
    var body: some View {
        VStack(spacing: 12) {
            Text("🐉")
                .font(.system(size: 60))
            
            Text("龍魂数据主权防御工具")
                .font(.title)
                .fontWeight(.bold)
            
            Text("Longhun Data Sovereignty Defense Toolkit")
                .font(.caption)
                .foregroundColor(.secondary)
            
            Divider()
            
            VStack(alignment: .leading, spacing: 8) {
                InfoRow(title: "DNA追溯", value: Constants.toolkitDNA)
                InfoRow(title: "创始人", value: Constants.founderName)
                InfoRow(title: "UID", value: Constants.founderUID)
                InfoRow(title: "理论指导", value: "曾老师（永恒显示）")
            }
            .font(.caption)
        }
        .padding()
        .background(Color.blue.opacity(0.1))
        .cornerRadius(12)
    }
}

struct CorePrinciplesView: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("核心原则")
                .font(.headline)
            
            PrincipleRow(text: "所有权不可改（UID9622永远是创始人）")
            PrincipleRow(text: "逻辑算法必须明确（开源透明）")
            PrincipleRow(text: "用户可自定义群体规则（插件化）")
            PrincipleRow(text: "数字人民币激活机制（付款单号绑定临时DNA）")
            PrincipleRow(text: "所有激活DNA带时间戳（不可篡改）")
        }
        .padding()
        .background(Color.green.opacity(0.1))
        .cornerRadius(12)
    }
}

struct PrincipleRow: View {
    let text: String
    
    var body: some View {
        HStack(alignment: .top, spacing: 8) {
            Text("✅")
                .font(.caption)
            Text(text)
                .font(.caption)
                .fixedSize(horizontal: false, vertical: true)
        }
    }
}

struct SystemInfoView: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("💳 数字人民币激活通道")
                .font(.headline)
            
            InfoRow(title: "账号", value: "\(Constants.ecnyAccount)（\(Constants.ecnyBank)）")
            InfoRow(title: "网络身份", value: Constants.networkIdentity)
            InfoRow(title: "激活有效期", value: "\(Constants.tempDNAValidityDays)天")
            
            Text("激活方式：扫码支付后填写付款单号即可激活临时DNA")
                .font(.caption)
                .foregroundColor(.secondary)
                .padding(.top, 4)
        }
        .padding()
        .background(Color.orange.opacity(0.1))
        .cornerRadius(12)
    }
}

struct CNSHEntryCard: View {
    @EnvironmentObject var appState: AppState
    
    var body: some View {
        Button(action: {
            appState.selectedTab = 5
        }) {
            VStack(spacing: 12) {
                Text("🐉")
                    .font(.system(size: 50))
                
                Text("CNSH 字元编辑器")
                    .font(.title2)
                    .fontWeight(.bold)
                
                Text("人人平等 · 技术普惠 · 创作独特字元")
                    .font(.caption)
                    .foregroundColor(.secondary)
                
                HStack(spacing: 15) {
                    FeatureBadge(icon: "✓", text: "完全自主")
                    FeatureBadge(icon: "✓", text: "手指绘制")
                    FeatureBadge(icon: "✓", text: "DNA追溯")
                }
                .padding(.top, 8)
                
                Text("点击进入编辑器 →")
                    .font(.caption)
                    .fontWeight(.semibold)
                    .foregroundColor(.blue)
                    .padding(.top, 4)
            }
            .padding()
            .frame(maxWidth: .infinity)
            .background(
                LinearGradient(
                    gradient: Gradient(colors: [
                        Color.purple.opacity(0.15),
                        Color.blue.opacity(0.15)
                    ]),
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
            )
            .cornerRadius(12)
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(Color.blue.opacity(0.3), lineWidth: 2)
            )
        }
        .buttonStyle(PlainButtonStyle())
    }
}

struct FeatureBadge: View {
    let icon: String
    let text: String
    
    var body: some View {
        HStack(spacing: 4) {
            Text(icon)
                .font(.caption2)
                .foregroundColor(.green)
            Text(text)
                .font(.caption2)
                .foregroundColor(.secondary)
        }
        .padding(.horizontal, 8)
        .padding(.vertical, 4)
        .background(Color.white.opacity(0.5))
        .cornerRadius(4)
    }
}

struct InfoRow: View {
    let title: String
    let value: String
    
    var body: some View {
        HStack(alignment: .top) {
            Text(title + ":")
                .foregroundColor(.secondary)
            Text(value)
                .fontWeight(.medium)
            Spacer()
        }
    }
}

// ═══════════════════════════════════════════════════════════════
// 【激活视图】
// ═══════════════════════════════════════════════════════════════

struct ActivationView: View {
    @EnvironmentObject var appState: AppState
    @State private var paymentOrder = ""
    @State private var userName = ""
    @State private var userID = ""
    @State private var showingResult = false
    @State private var activationResult: ActivationInfo?
    @State private var errorMessage: String?
    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("💳 数字人民币激活")) {
                    VStack(alignment: .leading, spacing: 12) {
                        Text("付款账号：\(Constants.ecnyAccount)")
                        Text("开户银行：\(Constants.ecnyBank)")
                        Text("网络身份：\(Constants.networkIdentity)")
                    }
                    .font(.caption)
                    .foregroundColor(.secondary)
                }
                
                Section(header: Text("付款单号")) {
                    TextField("e-CNY-YYYYMMDD-XXXXXX", text: $paymentOrder)
                        .autocapitalization(.allCharacters)
                        .disableAutocorrection(true)
                    
                    Text("格式示例：e-CNY-20260227-ABC123")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                
                Section(header: Text("用户信息")) {
                    TextField("姓名", text: $userName)
                    TextField("身份证号（可选）", text: $userID)
                }
                
                Section {
                    Button(action: performActivation) {
                        HStack {
                            Spacer()
                            Text("激活临时DNA")
                                .fontWeight(.semibold)
                            Spacer()
                        }
                    }
                    .disabled(paymentOrder.isEmpty || userName.isEmpty)
                }
                
                Section(header: Text("激活记录")) {
                    if appState.ecnySystem.activations.isEmpty {
                        Text("暂无激活记录")
                            .foregroundColor(.secondary)
                    } else {
                        ForEach(Array(appState.ecnySystem.activations.values), id: \.paymentOrder) { info in
                            ActivationRecordRow(info: info)
                        }
                    }
                }
            }
            .navigationTitle("激活系统")
            .alert("激活结果", isPresented: $showingResult) {
                Button("确定", role: .cancel) { }
            } message: {
                if let result = activationResult {
                    Text("""
                    ✅ 激活成功！
                    
                    付款单号：\(result.paymentOrder)
                    临时DNA：\(result.tempDNA)
                    激活时间：\(result.activationTime.formatted())
                    有效期至：\(result.expiryTime.formatted())
                    """)
                } else if let error = errorMessage {
                    Text("❌ " + error)
                }
            }
        }
    }
    
    private func performActivation() {
        let userInfo = UserInfo(name: userName, idNumber: userID.isEmpty ? "未提供" : userID)
        
        if let result = appState.ecnySystem.activate(paymentOrder: paymentOrder, userInfo: userInfo) {
            activationResult = result
            errorMessage = nil
            
            // 清空表单
            paymentOrder = ""
            userName = ""
            userID = ""
        } else {
            activationResult = nil
            errorMessage = "付款单号格式错误或已被使用"
        }
        
        showingResult = true
    }
}

struct ActivationRecordRow: View {
    let info: ActivationInfo
    
    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(info.paymentOrder)
                .font(.headline)
            Text("用户：\(info.userInfo.name)")
                .font(.caption)
            Text("激活：\(info.activationTime.formatted())")
                .font(.caption)
                .foregroundColor(.secondary)
            Text("状态：\(info.status.displayName)")
                .font(.caption)
                .foregroundColor(info.status == .active ? .green : .red)
        }
        .padding(.vertical, 4)
    }
}

// ═══════════════════════════════════════════════════════════════
// 【DNA生成器视图】
// ═══════════════════════════════════════════════════════════════

struct DNAGeneratorView: View {
    @State private var description = ""
    @State private var version = "v1.0"
    @State private var generatedDNA: String?
    @State private var dnaHistory: [String] = []
    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("🔐 DNA追溯码生成")) {
                    TextField("描述信息（如：DATA-BACKUP）", text: $description)
                    TextField("版本号", text: $version)
                    
                    Button(action: generateDNA) {
                        HStack {
                            Spacer()
                            Text("生成DNA追溯码")
                                .fontWeight(.semibold)
                            Spacer()
                        }
                    }
                    .disabled(description.isEmpty)
                }
                
                if let dna = generatedDNA {
                    Section(header: Text("生成结果")) {
                        Text(dna)
                            .font(.system(.caption, design: .monospaced))
                            .textSelection(.enabled)
                        
                        Button(action: { copyToClipboard(dna) }) {
                            Label("复制到剪贴板", systemImage: "doc.on.doc")
                        }
                    }
                }
                
                if !dnaHistory.isEmpty {
                    Section(header: Text("历史记录")) {
                        ForEach(dnaHistory, id: \.self) { dna in
                            Text(dna)
                                .font(.system(.caption, design: .monospaced))
                                .textSelection(.enabled)
                        }
                    }
                }
            }
            .navigationTitle("DNA生成器")
        }
    }
    
    private func generateDNA() {
        let dna = DNAGenerator.generate(description: description, version: version)
        generatedDNA = dna
        dnaHistory.insert(dna, at: 0)
        
        // 清空输入
        description = ""
    }
    
    private func copyToClipboard(_ text: String) {
        UIPasteboard.general.string = text
    }
}

// ═══════════════════════════════════════════════════════════════
// 【规则管理视图】
// ═══════════════════════════════════════════════════════════════

struct RulesView: View {
    @EnvironmentObject var appState: AppState
    @State private var showingAddRule = false
    
    var body: some View {
        NavigationView {
            List {
                ForEach(Array(appState.ruleEngine.rules.keys.sorted()), id: \.self) { key in
                    if let rule = appState.ruleEngine.rules[key] {
                        NavigationLink(destination: RuleDetailView(ruleName: key, rule: rule)) {
                            RuleRow(ruleName: key, rule: rule)
                        }
                    }
                }
            }
            .navigationTitle("防御规则")
            .toolbar {
                Button(action: { appState.ruleEngine.validateFounder() }) {
                    Label("验证", systemImage: "checkmark.shield")
                }
            }
        }
    }
}

struct RuleRow: View {
    let ruleName: String
    let rule: DefenseRule
    
    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            HStack {
                Text(ruleName)
                    .font(.headline)
                Spacer()
                if rule.eternal == true {
                    Image(systemName: "lock.fill")
                        .foregroundColor(.orange)
                }
                if rule.enabled == true {
                    Circle()
                        .fill(Color.green)
                        .frame(width: 8, height: 8)
                }
            }
            
            if let description = rule.description {
                Text(description)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
}

struct RuleDetailView: View {
    let ruleName: String
    let rule: DefenseRule
    
    var body: some View {
        Form {
            Section(header: Text("规则信息")) {
                InfoRow(title: "名称", value: ruleName)
                if let enabled = rule.enabled {
                    InfoRow(title: "状态", value: enabled ? "启用" : "禁用")
                }
                if let eternal = rule.eternal {
                    InfoRow(title: "永恒保护", value: eternal ? "是" : "否")
                }
                if let editable = rule.editable {
                    InfoRow(title: "可编辑", value: editable ? "是" : "否")
                }
            }
            
            if let description = rule.description {
                Section(header: Text("描述")) {
                    Text(description)
                }
            }
            
            Section(header: Text("详细配置")) {
                Text(rule.debugDescription)
                    .font(.system(.caption, design: .monospaced))
                    .textSelection(.enabled)
            }
        }
        .navigationTitle(ruleName)
    }
}

// ═══════════════════════════════════════════════════════════════
// 【防御执行视图】
// ═══════════════════════════════════════════════════════════════

struct DefenseView: View {
    @EnvironmentObject var appState: AppState
    @State private var executionLog: [String] = []
    
    var body: some View {
        NavigationView {
            List {
                Section(header: Text("防御操作")) {
                    Button(action: executeNetworkIsolation) {
                        Label("执行网络隔离", systemImage: "network")
                    }
                    
                    Button(action: executeSyncControl) {
                        Label("执行同步控制", systemImage: "arrow.triangle.2.circlepath")
                    }
                    
                    Button(action: executeAppAudit) {
                        Label("执行应用审计", systemImage: "doc.text.magnifyingglass")
                    }
                    
                    Button(action: executeAll) {
                        Label("执行所有防御", systemImage: "shield.fill")
                    }
                    .foregroundColor(.blue)
                    .fontWeight(.semibold)
                }
                
                if !executionLog.isEmpty {
                    Section(header: Text("执行日志")) {
                        ForEach(executionLog, id: \.self) { log in
                            Text(log)
                                .font(.caption)
                        }
                    }
                }
            }
            .navigationTitle("防御执行")
            .toolbar {
                Button(action: { executionLog.removeAll() }) {
                    Label("清空", systemImage: "trash")
                }
            }
        }
    }
    
    private func executeNetworkIsolation() {
        let executor = DataSovereigntyDefenseExecutor(ruleEngine: appState.ruleEngine)
        if executor.executeNetworkIsolation() {
            addLog("✅ 网络隔离执行成功")
        } else {
            addLog("⚠️ 网络隔离规则未启用")
        }
    }
    
    private func executeSyncControl() {
        let executor = DataSovereigntyDefenseExecutor(ruleEngine: appState.ruleEngine)
        if executor.executeSyncControl() {
            addLog("✅ 同步控制执行成功")
        } else {
            addLog("⚠️ 同步控制规则未启用")
        }
    }
    
    private func executeAppAudit() {
        let executor = DataSovereigntyDefenseExecutor(ruleEngine: appState.ruleEngine)
        if let report = executor.executeAppAudit() {
            addLog("✅ 应用审计完成")
            addLog("审计时间：\(report.auditTime.formatted())")
        } else {
            addLog("⚠️ 应用审计规则未启用")
        }
    }
    
    private func executeAll() {
        executeNetworkIsolation()
        executeSyncControl()
        executeAppAudit()
        addLog("🛡️ 所有防御措施已执行")
    }
    
    private func addLog(_ message: String) {
        let timestamp = Date().formatted(date: .omitted, time: .standard)
        executionLog.insert("[\(timestamp)] \(message)", at: 0)
    }
}

#Preview {
    MainContentView()
        .environmentObject(AppState())
}
