/*
╔═══════════════════════════════════════════════════════════════╗
║  🐉 龍魂系统 | UID9622                                        ║
║  📦 模块：未定义变量检测器                                    ║
║  🧬 DNA：#ZHUGEXIN⚡️2026-01-11-UNDEFINED-VARIABLE-DETECTOR-v1.0  ║
╚═══════════════════════════════════════════════════════════════╝
*/

import * as vscode from 'vscode';

export class UndefinedVariableDetector {
    
    detect(text: string, lines: string[]): vscode.Diagnostic[] {
        const diagnostics: vscode.Diagnostic[] = [];
        
        // 提取已定义的变量和函数
        const defined = this.extractDefinedVariables(text, lines);
        const used = this.extractUsedVariables(text, lines);
        
        // 检查未定义的使用
        used.forEach((usage, index) => {
            if (!defined.has(usage.name) && !this.isBuiltinVariable(usage.name)) {
                const diagnostic = new vscode.Diagnostic(
                    new vscode.Range(
                        new vscode.Position(usage.line, usage.column),
                        new vscode.Position(usage.line, usage.column + usage.name.length)
                    ),
                    `⚠️ 变量 '${usage.name}' 未定义` + this.getSuggestion(usage.name, Array.from(defined)),
                    vscode.DiagnosticSeverity.Warning
                );
                diagnostic.code = 'undefined_variable';
                diagnostics.push(diagnostic);
            }
        });
        
        return diagnostics;
    }
    
    private extractDefinedVariables(text: string, lines: string[]): Set<string> {
        const defined = new Set<string>();
        
        lines.forEach((line, index) => {
            // 函数定义
            const funcMatch = line.match(/(?:def|function)\s+([a-zA-Z_]\w*)\s*\(/);
            if (funcMatch) {
                defined.add(funcMatch[1]);
            }
            
            // 类定义
            const classMatch = line.match(/class\s+([a-zA-Z_]\w*)/);
            if (classMatch) {
                defined.add(classMatch[1]);
            }
            
            // 变量赋值 (Python)
            const pythonAssignMatch = line.match(/^([a-zA-Z_]\w*)\s*=/);
            if (pythonAssignMatch) {
                defined.add(pythonAssignMatch[1]);
            }
            
            // 变量赋值 (JavaScript/TypeScript)
            const jsAssignMatch = line.match(/(?:const|let|var)\s+([a-zA-Z_]\w*)\s*=/);
            if (jsAssignMatch) {
                defined.add(jsAssignMatch[1]);
            }
            
            // 参数定义
            const paramMatch = line.match(/\(([^)]*)\)/);
            if (paramMatch) {
                const params = paramMatch[1].split(',').map(p => p.trim());
                params.forEach(param => {
                    const paramDef = param.match(/([a-zA-Z_]\w*)/);
                    if (paramDef) {
                        defined.add(paramDef[1]);
                    }
                });
            }
        });
        
        return defined;
    }
    
    private extractUsedVariables(text: string, lines: string[]): Array<{name: string, line: number, column: number}> {
        const used: Array<{name: string, line: number, column: number}> = [];
        
        lines.forEach((line, index) => {
            // 匹配变量使用（简单的正则，可以改进）
            const variablePattern = /\b([a-zA-Z_]\w*)\b(?!\s*[=(])/g;
            let match;
            
            while ((match = variablePattern.exec(line)) !== null) {
                const name = match[1];
                const column = match.index;
                
                // 跳过关键字
                if (!this.isKeyword(name) && !this.isFunctionDefinition(line, column)) {
                    used.push({ name, line: index, column });
                }
            }
        });
        
        return used;
    }
    
    private isBuiltinVariable(name: string): boolean {
        const builtins = [
            'print', 'console', 'log', 'len', 'str', 'int', 'float', 'bool',
            'list', 'dict', 'set', 'tuple', 'range', 'enumerate', 'zip',
            'Math', 'Date', 'Array', 'Object', 'String', 'Number', 'Boolean',
            'require', 'import', 'export', 'default', 'this', 'self'
        ];
        return builtins.includes(name);
    }
    
    private isKeyword(name: string): boolean {
        const keywords = [
            'if', 'else', 'elif', 'for', 'while', 'def', 'class', 'import', 'from',
            'return', 'break', 'continue', 'pass', 'try', 'except', 'finally',
            'with', 'as', 'in', 'is', 'not', 'and', 'or', 'True', 'False', 'None',
            'var', 'let', 'const', 'function', 'async', 'await', 'new', 'typeof'
        ];
        return keywords.includes(name);
    }
    
    private isFunctionDefinition(line: string, column: number): boolean {
        const before = line.substring(0, column).trim();
        return before.endsWith('def ') || before.endsWith('function ') || 
               Boolean(before.match(/(?:const|let|var)\s+\w+\s*=\s*$/));
    }
    
    private getSuggestion(unknownName: string, definedNames: string[]): string {
        // 简单的相似度匹配
        const suggestions = definedNames.filter(name => 
            this.levenshteinDistance(unknownName.toLowerCase(), name.toLowerCase()) <= 2
        );
        
        if (suggestions.length > 0) {
            return `\n你可能想用: ${suggestions.join(' • ')}`;
        }
        
        return '';
    }
    
    private levenshteinDistance(str1: string, str2: string): number {
        const matrix = [];
        
        for (let i = 0; i <= str2.length; i++) {
            matrix[i] = [i];
        }
        
        for (let j = 0; j <= str1.length; j++) {
            matrix[0][j] = j;
        }
        
        for (let i = 1; i <= str2.length; i++) {
            for (let j = 1; j <= str1.length; j++) {
                if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
                    matrix[i][j] = matrix[i - 1][j - 1];
                } else {
                    matrix[i][j] = Math.min(
                        matrix[i - 1][j - 1] + 1,
                        matrix[i][j - 1] + 1,
                        matrix[i - 1][j] + 1
                    );
                }
            }
        }
        
        return matrix[str2.length][str1.length];
    }
}