import * as vscode from 'vscode';
import * as path from 'path';

export class PathErrorDetector {
    
    detect(text: string, lines: string[]): vscode.Diagnostic[] {
        const diagnostics: vscode.Diagnostic[] = [];
        
        lines.forEach((line, index) => {
            // 检测绝对路径
            const absolutePathPatterns = [
                /["']\/Users\/[^"']+["']/,           // macOS绝对路径
                /["']C:\\\\[^"']+["']/,             // Windows绝对路径
                /["']\/home\/[^"']+["']/,           // Linux绝对路径
                /["'][A-Za-z]:\\\\[^"']+["']/       // Windows路径
            ];
            
            absolutePathPatterns.forEach(pattern => {
                const match = line.match(pattern);
                if (match && match.index !== undefined) {
                    const diagnostic = new vscode.Diagnostic(
                        new vscode.Range(
                            new vscode.Position(index, match.index),
                            new vscode.Position(index, match.index + match[0].length)
                        ),
                        `📂 检测到绝对路径 "${match[0]}" - 跨平台兼容性问题`,
                        vscode.DiagnosticSeverity.Warning
                    );
                    diagnostic.code = 'path_error';
                    diagnostics.push(diagnostic);
                }
            });
            
            // 检测反斜杠路径
            if (line.includes('\\') && !line.includes('\\\\')) {
                const backslashMatch = line.match(/[^\\]([^\\]*\\[^\\]*)+/);
                if (backslashMatch) {
                    const diagnostic = new vscode.Diagnostic(
                        new vscode.Range(
                            new vscode.Position(index, line.indexOf('\\')),
                            new vscode.Position(index, line.lastIndexOf('\\') + 1)
                        ),
                        `📂 检测到反斜杠路径 - 在Linux/Mac上可能有问题`,
                        vscode.DiagnosticSeverity.Information
                    );
                    diagnostic.code = 'path_error';
                    diagnostics.push(diagnostic);
                }
            }
        });
        
        return diagnostics;
    }
}