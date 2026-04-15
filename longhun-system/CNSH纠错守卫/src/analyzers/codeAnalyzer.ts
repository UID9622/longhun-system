/*
╔═══════════════════════════════════════════════════════════════╗
║  🐉 龍魂系统 | UID9622                                        ║
║  📦 模块：代码分析器                                          ║
║  🧬 DNA：#ZHUGEXIN⚡️2026-01-11-CODE-ANALYZER-v1.0          ║
╚═══════════════════════════════════════════════════════════════╝
*/

import * as vscode from 'vscode';
import { PseudoCodeDetector } from '../detectors/pseudoCodeDetector';
import { UndefinedVariableDetector } from '../detectors/undefinedVariableDetector';
import { DependencyDetector } from '../detectors/dependencyDetector';
import { PathErrorDetector } from '../detectors/pathErrorDetector';
import { EncodingDetector } from '../detectors/encodingDetector';
import { APILeakDetector } from '../detectors/apiLeakDetector';
import { CommentQualityDetector } from '../detectors/commentQualityDetector';

export class CodeAnalyzer {
    private pseudoCodeDetector: PseudoCodeDetector;
    private undefinedVariableDetector: UndefinedVariableDetector;
    private dependencyDetector: DependencyDetector;
    private pathErrorDetector: PathErrorDetector;
    private encodingDetector: EncodingDetector;
    private apiLeakDetector: APILeakDetector;
    private commentQualityDetector: CommentQualityDetector;

    constructor() {
        this.pseudoCodeDetector = new PseudoCodeDetector();
        this.undefinedVariableDetector = new UndefinedVariableDetector();
        this.dependencyDetector = new DependencyDetector();
        this.pathErrorDetector = new PathErrorDetector();
        this.encodingDetector = new EncodingDetector();
        this.apiLeakDetector = new APILeakDetector();
        this.commentQualityDetector = new CommentQualityDetector();
    }

    analyzeDocument(document: vscode.TextDocument): vscode.Diagnostic[] {
        const text = document.getText();
        return this.analyzeText(text, document);
    }

    analyzeText(text: string, _document: vscode.TextDocument): vscode.Diagnostic[] {
        const diagnostics: vscode.Diagnostic[] = [];
        const lines = text.split('\n');

        // 获取用户配置
        const config = vscode.workspace.getConfiguration('cnsh');
        const enabledFeatures = config.get<any>('enabledFeatures');

        // 1. 伪代码检测
        if (enabledFeatures.pseudoCodeDetector) {
            const pseudoCodeIssues = this.pseudoCodeDetector.detect(text, lines);
            diagnostics.push(...pseudoCodeIssues);
        }

        // 2. 未定义变量检测
        if (enabledFeatures.undefinedVariableDetector) {
            const undefinedVarIssues = this.undefinedVariableDetector.detect(text, lines);
            diagnostics.push(...undefinedVarIssues);
        }

        // 3. 依赖缺失检测
        if (enabledFeatures.missingDependencyReminder) {
            const dependencyIssues = this.dependencyDetector.detect(text, lines);
            diagnostics.push(...dependencyIssues);
        }

        // 4. 路径错误检测
        if (enabledFeatures.pathErrorCorrection) {
            const pathIssues = this.pathErrorDetector.detect(text, lines);
            diagnostics.push(...pathIssues);
        }

        // 5. 编码格式检测
        if (enabledFeatures.encodingFormatGuard) {
            const encodingIssues = this.encodingDetector.detect(text, lines);
            diagnostics.push(...encodingIssues);
        }

        // 6. API密钥泄露检测
        if (enabledFeatures.apiKeyLeakProtection) {
            const apiLeakIssues = this.apiLeakDetector.detect(text, lines);
            diagnostics.push(...apiLeakIssues);
        }

        // 7. 注释质量检测
        if (enabledFeatures.commentQualityCheck) {
            const commentIssues = this.commentQualityDetector.detect(text, lines);
            diagnostics.push(...commentIssues);
        }

        return diagnostics;
    }

    generateQuickFix(diagnostic: vscode.Diagnostic): vscode.CodeAction[] {
        const actions: vscode.CodeAction[] = [];

        switch (diagnostic.code) {
            case 'pseudo_code':
                actions.push(this.createAddTodoAction(diagnostic));
                actions.push(this.createGenerateFrameworkAction(diagnostic));
                break;
            case 'undefined_variable':
                actions.push(this.createFixVariableAction(diagnostic));
                break;
            case 'missing_dependency':
                actions.push(this.createInstallDependencyAction(diagnostic));
                break;
            case 'path_error':
                actions.push(this.createFixPathAction(diagnostic));
                break;
            case 'encoding_error':
                actions.push(this.createFixEncodingAction(diagnostic));
                break;
            case 'api_key_leak':
                actions.push(this.createFixAPIKeyAction(diagnostic));
                break;
            case 'comment_quality':
                actions.push(this.createGenerateDocstringAction(diagnostic));
                break;
        }

        return actions;
    }

    private createAddTodoAction(diagnostic: vscode.Diagnostic): vscode.CodeAction {
        const action = new vscode.CodeAction('📝 添加TODO注释', vscode.CodeActionKind.QuickFix);
        action.diagnostics = [diagnostic];
        action.edit = new vscode.WorkspaceEdit();
        const uri = vscode.window.activeTextEditor?.document.uri;
        if (uri) {
            action.edit.insert(uri, diagnostic.range.end, '  # TODO: 实现此函数 - 伪代码占位符');
        }
        return action;
    }

    private createGenerateFrameworkAction(diagnostic: vscode.Diagnostic): vscode.CodeAction {
        const action = new vscode.CodeAction('✏️ 生成实现框架', vscode.CodeActionKind.QuickFix);
        action.diagnostics = [diagnostic];
        return action;
    }

    private createFixVariableAction(diagnostic: vscode.Diagnostic): vscode.CodeAction {
        const action = new vscode.CodeAction('🔧 修正变量名', vscode.CodeActionKind.QuickFix);
        action.diagnostics = [diagnostic];
        return action;
    }

    private createInstallDependencyAction(diagnostic: vscode.Diagnostic): vscode.CodeAction {
        const action = new vscode.CodeAction('🚀 立即安装依赖', vscode.CodeActionKind.QuickFix);
        action.diagnostics = [diagnostic];
        return action;
    }

    private createFixPathAction(diagnostic: vscode.Diagnostic): vscode.CodeAction {
        const action = new vscode.CodeAction('📂 修正路径', vscode.CodeActionKind.QuickFix);
        action.diagnostics = [diagnostic];
        return action;
    }

    private createFixEncodingAction(diagnostic: vscode.Diagnostic): vscode.CodeAction {
        const action = new vscode.CodeAction('🔤 添加编码参数', vscode.CodeActionKind.QuickFix);
        action.diagnostics = [diagnostic];
        return action;
    }

    private createFixAPIKeyAction(diagnostic: vscode.Diagnostic): vscode.CodeAction {
        const action = new vscode.CodeAction('🔒 改用环境变量', vscode.CodeActionKind.QuickFix);
        action.diagnostics = [diagnostic];
        return action;
    }

    private createGenerateDocstringAction(diagnostic: vscode.Diagnostic): vscode.CodeAction {
        const action = new vscode.CodeAction('💬 生成文档字符串', vscode.CodeActionKind.QuickFix);
        action.diagnostics = [diagnostic];
        return action;
    }
}