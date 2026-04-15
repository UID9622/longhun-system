import * as vscode from 'vscode';

export class DependencyDetector {
    
    detect(_text: string, lines: string[]): vscode.Diagnostic[] {
        const diagnostics: vscode.Diagnostic[] = [];
        
        const pythonPackages = [
            'requests', 'pandas', 'numpy', 'matplotlib', 'scipy', 'sklearn',
            'tensorflow', 'torch', 'flask', 'django', 'fastapi', 'asyncio',
            'pillow', 'opencv-python', 'beautifulsoup4', 'selenium'
        ];
        
        const jsPackages = [
            'express', 'axios', 'lodash', 'react', 'vue', 'angular',
            'moment', 'jquery', 'bootstrap', 'webpack', 'babel', 'eslint'
        ];
        
        lines.forEach((line, index) => {
            const pythonImport = line.match(/^\s*import\s+([a-zA-Z_]\w*)|from\s+([a-zA-Z_]\w*)/);
            if (pythonImport) {
                const pkgName = pythonImport[1] || pythonImport[2];
                if (pythonPackages.includes(pkgName)) {
                    const diagnostic = new vscode.Diagnostic(
                        new vscode.Range(new vscode.Position(index, 0), new vscode.Position(index, line.length)),
                        `📦 Python包 "${pkgName}" 可能需要安装`,
                        vscode.DiagnosticSeverity.Information
                    );
                    diagnostic.code = 'missing_dependency';
                    diagnostics.push(diagnostic);
                }
            }
            
            const jsRequire = line.match(/(?:require|import)\s*\(?['"]([^'"]+)['"]\)?/);
            if (jsRequire) {
                const pkgName = jsRequire[1].split('/')[0];
                if (jsPackages.includes(pkgName)) {
                    const diagnostic = new vscode.Diagnostic(
                        new vscode.Range(new vscode.Position(index, 0), new vscode.Position(index, line.length)),
                        `📦 Node.js包 "${pkgName}" 可能需要安装`,
                        vscode.DiagnosticSeverity.Information
                    );
                    diagnostic.code = 'missing_dependency';
                    diagnostics.push(diagnostic);
                }
            }
        });
        
        return diagnostics;
    }
}