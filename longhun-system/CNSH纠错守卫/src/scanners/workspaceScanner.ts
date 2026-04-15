/*
╔═══════════════════════════════════════════════════════════════╗
║  🐉 龍魂系统 | UID9622                                        ║
║  📦 模块：工作区扫描器                                        ║
║  🧬 DNA：#ZHUGEXIN⚡️2026-01-11-WORKSPACE-SCANNER-v1.0      ║
╚═══════════════════════════════════════════════════════════════╝
*/

import * as vscode from 'vscode';
import * as path from 'path';
// import * as fs from 'fs'; // 暂未使用，保留备用
import { GlobSync } from 'glob';

export interface ScanResult {
    file: vscode.Uri;
    issues: vscode.Diagnostic[];
    scanTime: number;
}

export class WorkspaceScanner {
    
    async scanWorkspace(progress?: vscode.Progress<{message?: string; increment?: number}>, token?: vscode.CancellationToken): Promise<ScanResult[]> {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            vscode.window.showWarningMessage('没有打开工作区');
            return [];
        }

        const results: ScanResult[] = [];
        const startTime = Date.now();

        // 获取支持的文件模式
        const filePatterns = this.getSupportedFilePatterns();
        
        for (const folder of workspaceFolders) {
            const folderPath = folder.uri.fsPath;
            
            for (const pattern of filePatterns) {
                if (token?.isCancellationRequested) {
                    return results;
                }

                progress?.report({ message: `扫描 ${pattern} 文件...`, increment: 10 });
                
                try {
                    const files = new GlobSync(pattern, { 
                        cwd: folderPath,
                        ignore: ['**/node_modules/**', '**/dist/**', '**/build/**', '**/.git/**']
                    }).found;
                    
                    for (let i = 0; i < files.length; i++) {
                        if (token?.isCancellationRequested) {
                            return results;
                        }
                        
                        const filePath = files[i];
                        progress?.report({ 
                            message: `分析 ${path.basename(filePath)}...`,
                            increment: (files.length > 0) ? 80 / files.length : 0
                        });
                        
                        const result = await this.scanFile(vscode.Uri.file(filePath));
                        if (result.issues.length > 0) {
                            results.push(result);
                        }
                    }
                } catch (error) {
                    console.error(`扫描文件模式 ${pattern} 时出错:`, error);
                }
            }
        }

        const totalTime = Date.now() - startTime;
        this.showScanResults(results, totalTime);
        
        return results;
    }
    
    async scanFile(uri: vscode.Uri): Promise<ScanResult> {
        const startTime = Date.now();
        
        try {
            const document = await vscode.workspace.openTextDocument(uri);
            const text = document.getText();
            
            // 使用代码分析器扫描
            const { CodeAnalyzer } = require('../analyzers/codeAnalyzer');
            const analyzer = new CodeAnalyzer();
            const issues = analyzer.analyzeText(text, document);
            
            return {
                file: uri,
                issues: issues,
                scanTime: Date.now() - startTime
            };
        } catch (error) {
            console.error(`扫描文件 ${uri.fsPath} 时出错:`, error);
            return {
                file: uri,
                issues: [],
                scanTime: Date.now() - startTime
            };
        }
    }
    
    private getSupportedFilePatterns(): string[] {
        return [
            '*.py',           // Python
            '*.js',           // JavaScript
            '*.ts',           // TypeScript
            '*.jsx',          // React JSX
            '*.tsx',          // React TypeScript
            '*.java',         // Java
            '*.cpp',          // C++
            '*.c',            // C
            '*.h',            // C Header
            '*.hpp',          // C++ Header
            '*.cs',           // C#
            '*.php',          // PHP
            '*.rb',           // Ruby
            '*.go',           // Go
            '*.rs',           // Rust
            '*.swift',        // Swift
            '*.kt',           // Kotlin
            '*.scala',        // Scala
            '*.sh',           // Shell Script
            '*.bash',         // Bash
            '*.zsh',          // Zsh
            '*.fish',         // Fish Shell
            '*.ps1',          // PowerShell
            '*.bat',          // Batch
            '*.cmd',          // Command
            '*.pl',           // Perl
            '*.r',            // R
            '*.m',            // MATLAB/Octave
            '*.sql',          // SQL
            '*.html',         // HTML
            '*.css',          // CSS
            '*.scss',         // SASS
            '*.less',         // LESS
            '*.vue',          // Vue.js
            '*.svelte',       // Svelte
            '*.dart',         // Dart
            '*.lua',          // Lua
            '*.elm',          // Elm
            '*.hs',           // Haskell
                '*.ml',           // OCaml
            '*.ex',           // Elixir
            '*.exs',          // Elixir Script
            '*.erl',          // Erlang
            '*.nim',          // Nim
            '*.zig',          // Zig
            '*.v',            // V
            '*.ada',          // Ada
            '*.d',            // D
            '*.factor',       // Factor
            '*.forth',        // Forth
            '*.f',            // Fortran
            '*.f90',          // Fortran 90+
            '*.cob',          // COBOL
            '*.cobol',        // COBOL
            '*.lsp',          // Lisp
            '*.el',           // Emacs Lisp
            '*.clj',          // Clojure
            '*.cljs',         // ClojureScript
            '*.hx',           // Haxe
            '*.gd',           // GDScript (Godot)
            '*.gs',           // GScript
            '*.nut',          // Squirrel
            '*.tsq',          // TorqueScript
            '*.bicep',        // Bicep
            '*.tf',           // Terraform
            '*.hcl',          // HCL
            '*.yaml',         // YAML
            '*.yml',          // YAML
            '*.toml',         // TOML
            '*.ini',          // INI
            '*.cfg',          // Configuration
            '*.conf'          // Configuration
        ];
    }
    
    private showScanResults(results: ScanResult[], totalTime: number): void {
        const totalFiles = results.length;
        const totalIssues = results.reduce((sum, result) => sum + result.issues.length, 0);
        const highSeverityIssues = results.reduce((sum, result) => 
            sum + result.issues.filter(issue => issue.severity === vscode.DiagnosticSeverity.Error).length, 0
        );
        const mediumSeverityIssues = results.reduce((sum, result) => 
            sum + result.issues.filter(issue => issue.severity === vscode.DiagnosticSeverity.Warning).length, 0
        );
        const lowSeverityIssues = results.reduce((sum, result) => 
            sum + result.issues.filter(issue => issue.severity === vscode.DiagnosticSeverity.Information).length, 0
        );
        
        const message = `
🔍 全盘扫描完成！

📊 统计信息：
• 扫描文件：${totalFiles} 个
• 发现问题：${totalIssues} 个
  🔴 严重：${highSeverityIssues} 个
  🟡 警告：${mediumSeverityIssues} 个  
  🔵 信息：${lowSeverityIssues} 个
• 扫描耗时：${(totalTime / 1000).toFixed(2)} 秒

🎯 建议优先处理严重问题，查看问题面板了解详情。
        `.trim();
        
        vscode.window.showInformationMessage(message, '查看详情').then(selection => {
            if (selection === '查看详情') {
                vscode.commands.executeCommand('workbench.panel.markers.view.focus');
            }
        });
        
        // 显示诊断结果
        const diagnosticCollection = vscode.languages.createDiagnosticCollection('cnsh-workspace-scan');
        results.forEach(result => {
            diagnosticCollection.set(result.file, result.issues);
        });
    }
}