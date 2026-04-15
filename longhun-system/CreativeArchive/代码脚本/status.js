"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getFileExistStatus = exports.mergeStatus = exports.getStatusText = exports.getColor = void 0;
const vscode_1 = require("vscode");
const nls = __importStar(require("vscode-nls"));
const localize = nls.loadMessageBundle();
function getColor(status) {
    switch (status) {
        case 0 /* Status.INDEX_MODIFIED */:
            return new vscode_1.ThemeColor("gitDecoration.stageModifiedResourceForeground");
        case 5 /* Status.MODIFIED */:
            return new vscode_1.ThemeColor("gitDecoration.modifiedResourceForeground");
        case 2 /* Status.INDEX_DELETED */:
            return new vscode_1.ThemeColor("gitDecoration.stageDeletedResourceForeground");
        case 6 /* Status.DELETED */:
            return new vscode_1.ThemeColor("gitDecoration.deletedResourceForeground");
        case 1 /* Status.INDEX_ADDED */:
        case 9 /* Status.INTENT_TO_ADD */:
            return new vscode_1.ThemeColor("gitDecoration.addedResourceForeground");
        case 4 /* Status.INDEX_COPIED */:
        case 3 /* Status.INDEX_RENAMED */:
            return new vscode_1.ThemeColor("gitDecoration.renamedResourceForeground");
        case 7 /* Status.UNTRACKED */:
            return new vscode_1.ThemeColor("gitDecoration.untrackedResourceForeground");
        case 8 /* Status.IGNORED */:
            return new vscode_1.ThemeColor("gitDecoration.ignoredResourceForeground");
        case 15 /* Status.BOTH_DELETED */:
        case 10 /* Status.ADDED_BY_US */:
        case 13 /* Status.DELETED_BY_THEM */:
        case 11 /* Status.ADDED_BY_THEM */:
        case 12 /* Status.DELETED_BY_US */:
        case 14 /* Status.BOTH_ADDED */:
        case 16 /* Status.BOTH_MODIFIED */:
            return new vscode_1.ThemeColor("gitDecoration.conflictingResourceForeground");
        default:
            throw new Error("Unknown git status: " + status);
    }
}
exports.getColor = getColor;
function getStatusText(status) {
    switch (status) {
        case 0 /* Status.INDEX_MODIFIED */:
            return localize("index modified", "Index Modified");
        case 5 /* Status.MODIFIED */:
            return localize("modified", "Modified");
        case 1 /* Status.INDEX_ADDED */:
            return localize("added", "Added");
        case 2 /* Status.INDEX_DELETED */:
            return localize("index deleted", "Index Deleted");
        case 6 /* Status.DELETED */:
            return localize("deleted", "Deleted");
        case 3 /* Status.INDEX_RENAMED */:
            return localize("renamed", "Renamed");
        case 4 /* Status.INDEX_COPIED */:
            return localize("index copied", "Index Copied");
        case 7 /* Status.UNTRACKED */:
            return localize("untracked", "Untracked");
        case 8 /* Status.IGNORED */:
            return localize("ignored", "Ignored");
        case 9 /* Status.INTENT_TO_ADD */:
            return localize("intent to add", "Intent to Add");
        case 15 /* Status.BOTH_DELETED */:
            return localize("both deleted", "Conflict: Both Deleted");
        case 10 /* Status.ADDED_BY_US */:
            return localize("added by us", "Conflict: Added By Us");
        case 13 /* Status.DELETED_BY_THEM */:
            return localize("deleted by them", "Conflict: Deleted By Them");
        case 11 /* Status.ADDED_BY_THEM */:
            return localize("added by them", "Conflict: Added By Them");
        case 12 /* Status.DELETED_BY_US */:
            return localize("deleted by us", "Conflict: Deleted By Us");
        case 14 /* Status.BOTH_ADDED */:
            return localize("both added", "Conflict: Both Added");
        case 16 /* Status.BOTH_MODIFIED */:
            return localize("both modified", "Conflict: Both Modified");
        default:
            return "";
    }
}
exports.getStatusText = getStatusText;
function mergeStatus({ change: firstChange }, { change: lastChange, hidden }) {
    if (hidden) {
        return;
    }
    const { status: firstStatus = 6 /* Status.DELETED */, originalUri: { path: firstPath }, } = firstChange || {};
    const { status: lastStatus = 6 /* Status.DELETED */, renameUri: { path: lastPath } = lastChange.originalUri, } = lastChange || {};
    const firstFileExistStatus = getFileExistStatus(firstStatus);
    const lastFileExistStatus = getFileExistStatus(lastStatus);
    if ((firstFileExistStatus === null || firstFileExistStatus === void 0 ? void 0 : firstFileExistStatus.isExistBefore) &&
        (lastFileExistStatus === null || lastFileExistStatus === void 0 ? void 0 : lastFileExistStatus.isExistAfter)) {
        return firstPath === lastPath ? 5 /* Status.MODIFIED */ : 3 /* Status.INDEX_RENAMED */;
    }
    if (!(firstFileExistStatus === null || firstFileExistStatus === void 0 ? void 0 : firstFileExistStatus.isExistBefore) &&
        (lastFileExistStatus === null || lastFileExistStatus === void 0 ? void 0 : lastFileExistStatus.isExistAfter)) {
        return firstStatus;
    }
    if ((firstFileExistStatus === null || firstFileExistStatus === void 0 ? void 0 : firstFileExistStatus.isExistBefore) &&
        !(lastFileExistStatus === null || lastFileExistStatus === void 0 ? void 0 : lastFileExistStatus.isExistAfter)) {
        return 6 /* Status.DELETED */;
    }
}
exports.mergeStatus = mergeStatus;
function getFileExistStatus(status) {
    if ([1 /* Status.INDEX_ADDED */, 3 /* Status.INDEX_RENAMED */].includes(status)) {
        return { isExistBefore: false, isExistAfter: true };
    }
    if (status === 6 /* Status.DELETED */) {
        return { isExistBefore: true, isExistAfter: false };
    }
    if (status === 5 /* Status.MODIFIED */) {
        return { isExistBefore: true, isExistAfter: true };
    }
}
exports.getFileExistStatus = getFileExistStatus;
//# sourceMappingURL=status.js.map