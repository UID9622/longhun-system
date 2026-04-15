/*
╔═══════════════════════════════════════════════════════════════╗
║  🐉 龍魂系统 | UID9622                                        ║
║  📦 模块：DNA追溯头部生成器                                    ║
║  🧬 DNA：#ZHUGEXIN⚡️2026-01-11-DNA-HEADER-GENERATOR-v1.0  ║
╚═══════════════════════════════════════════════════════════════╝
*/

import * as vscode from 'vscode';
import * as path from 'path';

export class DNAHeaderGenerator {
    
    generateHeader(document: vscode.TextDocument): string {
        const now = new Date();
        const timestamp = now.toISOString().replace(/[:-]/g, '').split('T')[0] + 
                          now.toTimeString().split(' ')[0].replace(/:/g, '');
        
        const fileName = path.basename(document.fileName);
        const fileTheme = this.extractThemeFromFileName(fileName);
        const version = '001';
        
        const header = `
"""
╔═══════════════════════════════════════════════════════════════╗
║  🐉 龍魂系统 | UID9622                                        ║
╠═══════════════════════════════════════════════════════════════╣
║  📦 文件：${fileName.padEnd(48)} ║
║  📌 版本：v1.0${' '.repeat(45)} ║
║  🧬 DNA：#UID9622⚡️${timestamp}-${fileTheme}-${version}${' '.repeat(42 - fileTheme.length - version.length)} ║
║  🔐 GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F          ║
║  👤 创建者：Lucky·UID9622（诸葛鑫）${' '.repeat(30)} ║
║  📅 创建时间：${this.formatDate(now)}${' '.repeat(31)} ║
║  🌐 项目：AI Truth Protocol${' '.repeat(36)} ║
╚═══════════════════════════════════════════════════════════════╝
"""

`;
        
        return header;
    }
    
    updateHeader(document: vscode.TextDocument): string {
        const text = document.getText();
        const headerRegex = /🧬 DNA：#UID9622⚡️(\d+)-(.+)-(\d+)/;
        const match = text.match(headerRegex);
        
        if (match) {
            const [, _date, theme, version] = match;
            const newVersion = (parseInt(version) + 1).toString().padStart(3, '0');
            const now = new Date();
            const timestamp = now.toISOString().replace(/[:-]/g, '').split('T')[0] + 
                              now.toTimeString().split(' ')[0].replace(/:/g, '');
            
            const newDnaLine = `║  🧬 DNA：#UID9622⚡️${timestamp}-${theme}-${newVersion}${' '.repeat(42 - theme.length - newVersion.length)} ║`;
            
            return text.replace(headerRegex, newDnaLine);
        }
        
        return this.generateHeader(document);
    }
    
    private extractThemeFromFileName(fileName: string): string {
        const nameWithoutExt = path.parse(fileName).name;
        
        // 移除常见的前缀和后缀
        const cleanName = nameWithoutExt
            .replace(/^(index|main|app|lib|utils|config|test|spec)/i, '')
            .replace(/\.(js|ts|py|java|cpp|c|cs|php|rb|go|rs|swift|kt|html|css|json|xml|yaml|yml|md)$/i, '')
            .replace(/[-_]/g, '');
        
        if (cleanName.length === 0) {
            return 'Core'; // 默认主题
        }
        
        // 简化主题名称
        const theme = cleanName.length > 15 ? cleanName.substring(0, 15) : cleanName;
        return theme.charAt(0).toUpperCase() + theme.slice(1);
    }
    
    private formatDate(date: Date): string {
        const year = date.getFullYear();
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const day = date.getDate().toString().padStart(2, '0');
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        
        return `${year}-${month}-${day} ${hours}:${minutes}`;
    }
}