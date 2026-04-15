"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getGitBinPath = exports.getBuiltInGitApi = void 0;
const vscode_1 = require("vscode");
function getBuiltInGitApi() {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const extension = vscode_1.extensions.getExtension("vscode.git");
            if (extension !== undefined) {
                const gitExtension = extension.isActive
                    ? extension.exports
                    : yield extension.activate();
                return gitExtension.getAPI(1);
            }
        }
        catch (err) {
            console.error(err);
        }
        return undefined;
    });
}
exports.getBuiltInGitApi = getBuiltInGitApi;
function getGitBinPath() {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const extension = vscode_1.extensions.getExtension("vscode.git");
            if (extension !== undefined) {
                const gitExtension = extension.isActive
                    ? extension.exports
                    : yield extension.activate();
                return gitExtension.getAPI(1).git.path;
            }
        }
        catch (err) {
            console.error(err);
        }
        return undefined;
    });
}
exports.getGitBinPath = getGitBinPath;
//# sourceMappingURL=api.js.map