/*
╔═══════════════════════════════════════════════════════════════╗
║  🐉 龍魂系统 | UID9622                                        ║
║  📦 模块：AI输出类型标注生成器                                  ║
║  🧬 DNA：#ZHUGEXIN⚡️2026-01-11-AI-ANNOTATION-GENERATOR-v1.0  ║
╚═══════════════════════════════════════════════════════════════╝
*/

import * as vscode from 'vscode';

export class AIAnnotationGenerator {
    
    generateAnnotation(document: vscode.TextDocument): string {
        const selectedText = this.getSelectedText(document);
        const analysis = this.analyzeCode(selectedText);
        
        const annotation = `
## 🏷️ AI输出类型声明

**输出者：** [请填写AI名称：ChatGPT/Claude/DeepSeek/文心/通义千问/其他]
**输出类型：** ${analysis.type}
**可执行性：** ${analysis.executability}
**依赖环境：** ${analysis.environment}
**入口文件：** ${analysis.entryFile}
**验证方法：** ${analysis.verification}
**风险等级：** ${analysis.riskLevel}

---

## ❗ 未定义项清单（需要你补的）

${analysis.undefinedItems.length > 0 ? 
    analysis.undefinedItems.map((item: any) => `**${item.type}：**\n- ${item.name} → ${item.description}`).join('\n') :
    '✅ 暂未发现未定义项'
}

---

## ⚠️ 风险提示

**危险命令：** ${analysis.hasDangerousCommands ? '有' : '无'}
${analysis.dangerousCommands.length > 0 ? 
    `- ${analysis.dangerousCommands.join('\n- ')}` : ''}

**越权操作：** ${analysis.hasPrivilegeEscalation ? '有' : '无'}
**不可逆操作：** ${analysis.hasIrreversibleOps ? '有' : '无'}
**网络请求：** ${analysis.hasNetworkRequests ? '有' : '无'}

---

## 🔧 最小可运行步骤

### 1️⃣ 环境检查
\`\`\`bash
# 操作系统要求
${analysis.environmentRequirements.os}

# 语言版本
${analysis.environmentRequirements.language}

# 验证命令
${analysis.environmentRequirements.verifyCommand}
\`\`\`

### 2️⃣ 依赖安装
\`\`\`bash
${analysis.installationCommands.length > 0 ? 
    analysis.installationCommands.join('\n') : 
    '# 无需额外依赖'
}
\`\`\`

### 3️⃣ 配置设置
\`\`\`bash
${analysis.configurationSteps.length > 0 ? 
    analysis.configurationSteps.join('\n') : 
    '# 无需特殊配置'
}
\`\`\`

### 4️⃣ 运行代码
\`\`\`bash
${analysis.runCommands.join('\n')}
\`\`\`

### 5️⃣ 验证结果
\`\`\`bash
${analysis.verificationCommands.length > 0 ? 
    analysis.verificationCommands.join('\n') : 
    '# 手动验证输出结果'
}
\`\`\`

### 6️⃣ 失败回滚
\`\`\`bash
${analysis.rollbackCommands.length > 0 ? 
    analysis.rollbackCommands.join('\n') : 
    '# 无需回滚操作'
}
\`\`\`

---

## 🧬 DNA追溯码

**本次输出追溯码：** #请填写AI名称⚡️${this.getTimestamp()}-${this.generateTheme()}-001

`;
        
        return annotation;
    }
    
    private getSelectedText(document: vscode.TextDocument): string {
        const editor = vscode.window.activeTextEditor;
        if (editor && editor.document === document) {
            return editor.document.getText(editor.selection);
        }
        return document.getText();
    }
    
    private analyzeCode(code: string): any {
        const analysis = {
            type: 'C 框架代码',
            executability: '❌ 不可直接执行',
            environment: '需要分析确定',
            entryFile: '需要指定',
            verification: '需要验证命令',
            riskLevel: '🟠 高风险',
            undefinedItems: [] as any[],
            hasDangerousCommands: false,
            dangerousCommands: [] as string[],
            hasPrivilegeEscalation: false,
            hasIrreversibleOps: false,
            hasNetworkRequests: false,
            environmentRequirements: {
                os: 'Windows 10+ / macOS 12+ / Ubuntu 20.04+',
                language: '需要分析确定',
                verifyCommand: '# 请填写验证命令'
            },
            installationCommands: [] as string[],
            configurationSteps: [] as string[],
            runCommands: [] as string[],
            verificationCommands: [] as string[],
            rollbackCommands: [] as string[]
        };
        
        // 分析代码特征
        const lines = code.split('\n');
        
        // 检测导入语句
        const imports = lines.filter(line => 
            line.match(/^\s*(import|from|require|include)\s+/)
        );
        
        if (imports.length > 0) {
            analysis.environmentRequirements.language = this.detectLanguage(imports[0]);
            analysis.installationCommands = imports.map(imp => 
                this.generateInstallCommand(imp)
            ).filter((cmd): cmd is string => cmd !== null);
        }
        
        // 检测函数定义
        const functions = lines.filter(line => 
            line.match(/^\s*(def|function|class)\s+([a-zA-Z_一-龯]\w*)/)
        );
        
        // 检测未定义函数调用
        const functionCalls = lines.filter(line => 
            line.match(/([a-zA-Z_一-龯]\w*)\s*\([^)]*\)/)
        );
        
        functionCalls.forEach(call => {
            const match = call.match(/([a-zA-Z_一-龯]\w*)\s*\(/);
            if (match) {
                const funcName = match[1];
                const isDefined = functions.some(func => 
                    func.includes(`${funcName}(`) || func.includes(` ${funcName}(`)
                );
                
                if (!isDefined && !this.isBuiltinFunction(funcName)) {
                    analysis.undefinedItems.push({
                        type: '函数缺失',
                        name: funcName,
                        description: `函数未定义，需要实现${funcName}()的逻辑`
                    });
                }
            }
        });
        
        // 检测危险命令
        const dangerousPatterns = [
            /rm\s+-rf/g,
            /sudo\s+/g,
            /DROP\s+DATABASE/gi,
            /DELETE\s+FROM/gi,
            /format\s+[a-zA-Z]:/gi,
            /dd\s+if=/g
        ];
        
        dangerousPatterns.forEach(pattern => {
            const matches = code.match(pattern);
            if (matches) {
                analysis.hasDangerousCommands = true;
                analysis.dangerousCommands.push(...matches);
            }
        });
        
        // 检测网络请求
        if (code.match(/(?:fetch|axios|requests|urllib|http\.request)/)) {
            analysis.hasNetworkRequests = true;
        }
        
        // 确定代码类型
        if (analysis.undefinedItems.length === 0 && !analysis.hasDangerousCommands) {
            analysis.type = 'A 生产级真代码';
            analysis.executability = '✅ 可直接执行';
            analysis.riskLevel = '🟢 低风险';
        } else if (analysis.undefinedItems.length <= 2 && !analysis.hasDangerousCommands) {
            analysis.type = 'B 示例代码';
            analysis.executability = '⚠️ 需适配后执行';
            analysis.riskLevel = '🟡 中风险';
        } else if (analysis.undefinedItems.length <= 5) {
            analysis.type = 'C 框架代码';
            analysis.executability = '❌ 不可直接执行';
            analysis.riskLevel = '🟠 高风险';
        } else {
            analysis.type = 'D 架构伪代码';
            analysis.executability = '❌ 纯示意不可运行';
            analysis.riskLevel = '🔴 极高风险';
        }
        
        // 生成运行命令
        if (analysis.environmentRequirements.language.includes('Python')) {
            analysis.runCommands.push('python main.py');
            analysis.environmentRequirements.verifyCommand = 'python --version';
        } else if (analysis.environmentRequirements.language.includes('Node') || 
                   analysis.environmentRequirements.language.includes('JavaScript')) {
            analysis.runCommands.push('node main.js');
            analysis.environmentRequirements.verifyCommand = 'node --version';
        } else if (analysis.environmentRequirements.language.includes('Java')) {
            analysis.runCommands.push('java Main');
            analysis.environmentRequirements.verifyCommand = 'java -version';
        }
        
        // 添加回滚命令
        if (analysis.hasDangerousCommands) {
            analysis.rollbackCommands.push('# 检查并撤销危险操作');
            analysis.rollbackCommands.push('# 确认系统状态正常');
        }
        
        return analysis;
    }
    
    private detectLanguage(importLine: string): string {
        if (importLine.includes('import ') || importLine.includes('from ')) {
            return 'Python 3.8+';
        } else if (importLine.includes('require') || importLine.includes('import ')) {
            return 'Node.js 18+';
        } else if (importLine.includes('import ')) {
            return 'TypeScript 4.5+';
        } else if (importLine.includes('include')) {
            return 'C++17+';
        }
        return '需要手动确定';
    }
    
    private generateInstallCommand(importLine: string): string | null {
        const pythonPackages = [
            { import: 'requests', package: 'requests' },
            { import: 'pandas', package: 'pandas' },
            { import: 'numpy', package: 'numpy' },
            { import: 'matplotlib', package: 'matplotlib' },
            { import: 'flask', package: 'flask' },
            { import: 'django', package: 'django' }
        ];
        
        const jsPackages = [
            { import: 'express', package: 'express' },
            { import: 'axios', package: 'axios' },
            { import: 'lodash', package: 'lodash' },
            { import: 'react', package: 'react' },
            { import: 'vue', package: 'vue' }
        ];
        
        for (const pkg of pythonPackages) {
            if (importLine.includes(pkg.import)) {
                return `pip install ${pkg.package}`;
            }
        }
        
        for (const pkg of jsPackages) {
            if (importLine.includes(pkg.import)) {
                return `npm install ${pkg.package}`;
            }
        }
        
        return null;
    }
    
    private isBuiltinFunction(funcName: string): boolean {
        const builtins = [
            'print', 'console', 'log', 'len', 'str', 'int', 'float', 'bool',
            'list', 'dict', 'set', 'tuple', 'range', 'enumerate', 'zip',
            'Math', 'Date', 'Array', 'Object', 'String', 'Number',
            'require', 'import', 'export', 'default', 'this', 'self',
            'setTimeout', 'setInterval', 'clearTimeout', 'clearInterval'
        ];
        return builtins.includes(funcName);
    }
    
    private getTimestamp(): string {
        const now = new Date();
        const year = now.getFullYear();
        const month = (now.getMonth() + 1).toString().padStart(2, '0');
        const day = now.getDate().toString().padStart(2, '0');
        return `${year}${month}${day}`;
    }
    
    private generateTheme(): string {
        const themes = ['DataProcess', 'SystemTool', 'WebApp', 'Algorithm', 'Utility'];
        return themes[Math.floor(Math.random() * themes.length)];
    }
}