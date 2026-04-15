import * as vscode from 'vscode';

export class APILeakDetector {
    
    detect(_text: string, lines: string[]): vscode.Diagnostic[] {
        const diagnostics: vscode.Diagnostic[] = [];
        
        const apiKeyPatterns = [
            /(?:api[_-]?key|apikey|api[_-]?secret|secret[_-]?key|access[_-]?token|auth[_-]?token)[\s:=]+["']?([a-zA-Z0-9_-]{20,})["']?/gi,
            /sk-[a-zA-Z0-9_-]{48}/gi,
            /ghp_[a-zA-Z0-9_-]{36}/gi,
            /glpat-[a-zA-Z0-9_-]{20}/gi,
            /AKIA[0-9A-Z]{16}/gi
        ];
        
        lines.forEach((line, index) => {
            apiKeyPatterns.forEach(pattern => {
                let match;
                while ((match = pattern.exec(line)) !== null) {
                    const diagnostic = new vscode.Diagnostic(
                        new vscode.Range(
                            new vscode.Position(index, match.index),
                            new vscode.Position(index, match.index + match[0].length)
                        ),
                        `🔑 检测到敏感信息：API密钥 - 存在泄露风险`,
                        vscode.DiagnosticSeverity.Error
                    );
                    diagnostic.code = 'api_key_leak';
                    diagnostics.push(diagnostic);
                }
            });
        });
        
        return diagnostics;
    }
}