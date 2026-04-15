import * as vscode from 'vscode';

export class CommentQualityDetector {
    
    detect(_text: string, lines: string[]): vscode.Diagnostic[] {
        const diagnostics: vscode.Diagnostic[] = [];
        
        lines.forEach((line, index) => {
            // 检测函数但没有文档字符串
            const funcMatch = line.match(/^\s*(def|function)\s+([a-zA-Z_]\w*)/);
            if (funcMatch) {
                const funcName = funcMatch[2];
                // 检查后面几行是否有文档字符串
                const hasDocstring = this.hasDocstring(lines, index);
                if (!hasDocstring) {
                    const diagnostic = new vscode.Diagnostic(
                        new vscode.Range(new vscode.Position(index, 0), new vscode.Position(index, line.length)),
                        `💬 函数 "${funcName}" 缺少文档字符串`,
                        vscode.DiagnosticSeverity.Information
                    );
                    diagnostic.code = 'comment_quality';
                    diagnostics.push(diagnostic);
                }
            }
        });
        
        return diagnostics;
    }
    
    private hasDocstring(lines: string[], startIndex: number): boolean {
        for (let i = startIndex + 1; i < Math.min(startIndex + 5, lines.length); i++) {
            const line = lines[i].trim();
            if (line.startsWith('"""') || line.startsWith("'''") || line.startsWith('/*')) {
                return true;
            }
            if (line.length > 0 && !line.startsWith('#')) {
                return false;
            }
        }
        return false;
    }
}