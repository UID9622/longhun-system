"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getChangePair = exports.parseGitChanges = void 0;
const path_1 = __importDefault(require("path"));
const vscode_1 = require("vscode");
function parseGitChanges(repoPath, gitResult) {
    const entries = gitResult.split('\x00');
    let index = 0;
    const result = [];
    const statusMap = { M: 5 /* Status.MODIFIED */, A: 1 /* Status.INDEX_ADDED */, D: 6 /* Status.DELETED */ };
    while (index < entries.length - 1) {
        const change = entries[index++];
        const resourcePath = entries[index++];
        if (!change || !resourcePath) {
            break;
        }
        const originalUri = vscode_1.Uri.file(path_1.default.isAbsolute(resourcePath) ? resourcePath : path_1.default.join(repoPath, resourcePath));
        let status = 7 /* Status.UNTRACKED */;
        // Copy or Rename status comes with a number, e.g. 'R100'. We don't need the number, so we use only first character of the status.
        switch (change[0]) {
            case 'M':
            case 'A':
            case 'D': {
                status = statusMap[change[0]];
                break;
            }
            // Rename contains two paths, the second one is what the file is renamed/copied to.
            case 'R': {
                if (index >= entries.length) {
                    break;
                }
                const newPath = entries[index++];
                if (!newPath) {
                    break;
                }
                const uri = vscode_1.Uri.file(path_1.default.isAbsolute(newPath) ? newPath : path_1.default.join(repoPath, newPath));
                result.push({
                    uri,
                    renameUri: uri,
                    originalUri,
                    status: 3 /* Status.INDEX_RENAMED */,
                });
                continue;
            }
            default:
                // Unknown status
                break;
        }
        result.push({
            status,
            originalUri,
            uri: originalUri,
            renameUri: originalUri,
        });
    }
    return result;
}
exports.parseGitChanges = parseGitChanges;
function getChangePair(originalChangeStack = [], changeStack) {
    const originalChangeItem = originalChangeStack.find(({ change }) => change);
    return [
        originalChangeItem || changeStack[0],
        changeStack[changeStack.length - 1],
    ];
}
exports.getChangePair = getChangePair;
//# sourceMappingURL=changes.js.map