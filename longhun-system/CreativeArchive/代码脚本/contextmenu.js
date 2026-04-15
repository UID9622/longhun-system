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
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getContextMenuCommandsDisposable = exports.resetCommit = exports.editMessage = exports.copyHash = exports.copyMessage = exports.RESET_COMMIT = exports.COPY_HASH = exports.EDIT_MESSAGE = exports.COPY_MESSAGE = void 0;
const child_process_1 = require("child_process");
const fs = __importStar(require("fs"));
const os_1 = __importDefault(require("os"));
const path_1 = __importDefault(require("path"));
const process_1 = __importDefault(require("process"));
const vscode_1 = require("vscode");
const nls = __importStar(require("vscode-nls"));
const simple_git_1 = require("simple-git");
const inversify_config_1 = require("../container/inversify.config");
const service_1 = require("../git/service");
const state_1 = __importDefault(require("../views/common/data/state"));
const types_1 = require("../container/types");
const switch_1 = require("./switch");
const localize = nls.loadMessageBundle();
const succeedEditMessage = localize('succeed.editMessage', 'Edit commit message successful');
const disposables = [];
exports.COPY_MESSAGE = 'git-history.history.copy.message';
exports.EDIT_MESSAGE = 'git-history.history.edit.message';
exports.COPY_HASH = 'git-history.history.copy.hash';
exports.RESET_COMMIT = 'git-history.history.reset.commit';
function copyMessage() {
    return vscode_1.commands.registerCommand(exports.COPY_MESSAGE, (context) => __awaiter(this, void 0, void 0, function* () {
        yield vscode_1.env.clipboard.writeText(context.message);
    }));
}
exports.copyMessage = copyMessage;
function copyHash() {
    return vscode_1.commands.registerCommand(exports.COPY_HASH, (context) => __awaiter(this, void 0, void 0, function* () {
        yield vscode_1.env.clipboard.writeText(context.hash);
    }));
}
exports.copyHash = copyHash;
function editMessage() {
    const gitService = inversify_config_1.container.get(service_1.GitService);
    const extensionContext = inversify_config_1.container.get(types_1.TYPES.ExtensionContext);
    return vscode_1.commands.registerCommand(exports.EDIT_MESSAGE, (context) => __awaiter(this, void 0, void 0, function* () {
        let newMessage = [''];
        const osType = getOSType();
        const message = context.message;
        const hash = context.hash;
        const repo = state_1.default.logOptions.repo;
        const options = { cwd: repo };
        const gitPath = path_1.default.join(repo, '.git');
        const rewordPath = path_1.default.join(gitPath, 'reword');
        const editMessagePath = path_1.default.join(gitPath, 'editMessage');
        const applyMessagePath = path_1.default.join(gitPath, 'applyMessage');
        const _isClean = (yield gitService.getStatus(repo)).isClean();
        const _isRebasing = gitService.isRebasing(repo);
        const _isCommitInCurrentRef = yield gitService.isCommitInCurrentRef(hash, repo);
        const _isMergeCommit = yield gitService.isMergeCommit(hash, repo);
        const previousCommit = yield gitService.getPreviousCommit(hash, repo);
        const _isLastCommit = yield gitService.isLastCommit(hash, repo);
        const checkerIterators = markCheckerIterator([
            { checker: checkClean, params: [_isClean] },
            { checker: checkRebasing, params: [_isRebasing] },
            { checker: checkFirstCommit, params: [previousCommit, _isLastCommit] },
            { checker: checkInCurrentRef, params: [_isCommitInCurrentRef] },
            { checker: checkMergeCommit, params: [_isMergeCommit, _isLastCommit] },
        ]);
        for (const iterator of checkerIterators) {
            if (iterator) {
                return;
            }
        }
        const EDIT_MESSAGE_FilePath = createEDIT_MESSAGE(gitPath, context.message, extensionContext);
        const openedDoc = yield openEDIT_MESSAGE(EDIT_MESSAGE_FilePath);
        const saveDisposable = saveEDIT_MESSAGE(openedDoc, newMessage);
        monitorDocClose(EDIT_MESSAGE_FilePath, saveDisposable, newMessage, message, _isMergeCommit, previousCommit, _isLastCommit, rewordPath, editMessagePath, applyMessagePath, repo, clear, options, gitService, osType);
        function clear() {
            disposables.forEach((disposable) => disposable.dispose());
            removeFile(EDIT_MESSAGE_FilePath);
            const paths = [];
            if (osType === 'win') {
                paths.push(`${rewordPath}.bat`, `${editMessagePath}.bat`, `${applyMessagePath}.bat`);
            }
            else {
                paths.push(`${rewordPath}.sh`, `${editMessagePath}.sh`, `${applyMessagePath}.sh`);
            }
            paths.forEach(path => {
                removeFile(path);
            });
        }
    }));
}
exports.editMessage = editMessage;
function removeFile(path) {
    if (fs.existsSync(path)) {
        fs.unlinkSync(path);
    }
}
function resetCommit() {
    const gitService = inversify_config_1.container.get(service_1.GitService);
    return vscode_1.commands.registerCommand(exports.RESET_COMMIT, (context) => __awaiter(this, void 0, void 0, function* () {
        const osType = getOSType();
        const curRepo = state_1.default.logOptions.repo;
        const repoName = osType === 'win' ? curRepo.split('\\').pop() : curRepo.split('/').pop();
        const hash = context.hash;
        const curBranch = (yield gitService.getStatus(curRepo)).current;
        const allRepos = gitService.getRepositories();
        const len = allRepos.length;
        const quickPick = vscode_1.window.createQuickPick();
        const items = [
            {
                label: localize('reset.quickpick.items.soft.label', 'Soft'),
                detail: localize('reset.quickpick.items.soft.detail', "Files won't change, differences will be staged for commit."),
                value: simple_git_1.ResetMode.SOFT,
            },
            {
                label: localize('reset.quickpick.items.mixed.label', 'Mixed'),
                detail: localize('reset.quickpick.items.mixed.detail', "Files won't change, differences won't be staged."),
                value: simple_git_1.ResetMode.MIXED,
            },
            {
                label: localize('reset.quickpick.items.hard.label', 'Hard'),
                detail: localize('reset.quickpick.items.hard.detail', 'Files will be reverted to the state of the selected commit, any local changes will be lost.'),
                value: simple_git_1.ResetMode.HARD,
            },
            {
                label: localize('reset.quickpick.items.keep.label', 'Keep'),
                detail: localize('reset.quickpick.items.keep.detail', 'Files will be reverted to the state of the selected commit, but local changes will be kept intact.'),
                value: simple_git_1.ResetMode.KEEP,
            },
        ];
        resolveQuickpick(quickPick, len, curBranch, repoName, items, gitService, curRepo, hash);
    }));
}
exports.resetCommit = resetCommit;
function getContextMenuCommandsDisposable() {
    return [copyMessage(), copyHash(), editMessage(), resetCommit()];
}
exports.getContextMenuCommandsDisposable = getContextMenuCommandsDisposable;
function checkClean(isClean) {
    if (!isClean) {
        vscode_1.window.showWarningMessage(localize('warning.unstaged.editMessage', 'You have unstaged changes'));
        return true;
    }
}
function checkRebasing(isRebasing) {
    if (isRebasing) {
        vscode_1.window.showWarningMessage(localize('warning.rebase.inProgress', 'Rebase in progress'));
        return true;
    }
}
function checkFirstCommit(previousCommit, isLastCommit) {
    if (!previousCommit && !isLastCommit) {
        vscode_1.window.showWarningMessage(localize('warning.firstCommit.editMessage', "Don't support the first commit"));
        return true;
    }
}
function checkInCurrentRef(isCommitInCurrentRef) {
    if (!isCommitInCurrentRef) {
        vscode_1.window.showWarningMessage(localize('warning.commitInOtherBranch.editMessage', "Don't support commit in other branch!"));
        return true;
    }
}
function checkMergeCommit(isMergeCommit, isLastCommit) {
    if (isMergeCommit && !isLastCommit) {
        vscode_1.window.showWarningMessage(localize('warning.mergeCommit.editMessage', "Don't support edit merge commit!"));
        return true;
    }
}
function createEDIT_MESSAGE(gitPath, message, extensionContext) {
    if (!fs.existsSync(gitPath)) {
        fs.mkdirSync(gitPath);
    }
    const displayLanguage = extensionContext.globalState.get('vscodeDisplayLanguage');
    const englishPromptMessage = `# Please enter the new commit message for your changes.
# with '#' will be ignored, and an empty message aborts the change.
# Save and close the document to continue.`;
    const localizedPromptMessage = `# 请为您的更改输入新的提交消息。
# 以‘#’开始的行将被忽略，空消息将中止更改。
# 保存并关闭文档以继续。`;
    const promptMessage = displayLanguage === 'zh-cn' ? localizedPromptMessage : englishPromptMessage;
    const EDIT_MESSAGE_FilePath = path_1.default.join(gitPath, 'EDIT_MESSAGE');
    fs.writeFileSync(EDIT_MESSAGE_FilePath, `${message}
${promptMessage}`);
    return EDIT_MESSAGE_FilePath;
}
function openEDIT_MESSAGE(path) {
    return __awaiter(this, void 0, void 0, function* () {
        const doc = yield vscode_1.workspace.openTextDocument(path);
        vscode_1.languages.setTextDocumentLanguage(doc, 'git-commit');
        yield vscode_1.window.showTextDocument(doc);
        return doc;
    });
}
function saveEDIT_MESSAGE(doc, newMessage) {
    return vscode_1.workspace.onDidSaveTextDocument((savedDoc) => __awaiter(this, void 0, void 0, function* () {
        if (savedDoc === doc) {
            newMessage[0] = savedDoc.getText();
        }
    }));
}
function gitCommitAmend(gitService, repo, editmsgCommand, clear) {
    gitService.amendCommit(repo, editmsgCommand, () => {
        vscode_1.commands.executeCommand(switch_1.REFRESH_COMMAND).then(() => __awaiter(this, void 0, void 0, function* () {
            clear();
            yield vscode_1.window.showInformationMessage(succeedEditMessage);
        }));
    });
}
function gitReabse(previousCommit, sequenceEditorCommand, editmsgCommand, handleError, clear, options, gitService, applymsgCommand, repo, osType) {
    (0, child_process_1.exec)(`git rebase --no-autosquash -i ${previousCommit}`, Object.assign(Object.assign({}, options), { env: Object.assign(Object.assign({}, process_1.default.env), { GIT_SEQUENCE_EDITOR: sequenceEditorCommand, GIT_EDITOR: editmsgCommand }) }), (error) => __awaiter(this, void 0, void 0, function* () {
        if (error) {
            yield handleError(options, gitService, error, applymsgCommand, repo, clear, osType);
        }
        else {
            clear();
            yield vscode_1.commands.executeCommand(switch_1.REFRESH_COMMAND);
            yield vscode_1.window.showInformationMessage(succeedEditMessage);
        }
    }));
}
function monitorDocClose(EDIT_MESSAGE_FilePath, saveDisposable, newMessage, message, _isMergeCommit, previousCommit, _isLastCommit, rewordPath, editMessagePath, applyMessagePath, repo, clear, options, gitService, osType) {
    const closeDisposable = vscode_1.window.onDidChangeVisibleTextEditors((editors) => __awaiter(this, void 0, void 0, function* () {
        if (!editors.some((editor) => editor.document.uri.fsPath === EDIT_MESSAGE_FilePath)) {
            closeDisposable.dispose();
            saveDisposable.dispose();
            if (newMessage[0] === '' || message === newMessage[0]) {
                return clear();
            }
            let sequenceEditorCommand = '';
            let editmsgCommand = '';
            let applymsgCommand = '';
            if (osType === 'win') {
                rewordPath += '.bat';
                editMessagePath += '.bat';
                applyMessagePath += '.bat';
                sequenceEditorCommand = rewordPath.replace(/\\/g, '\\\\');
                editmsgCommand = editMessagePath.replace(/\\/g, '\\\\');
                applymsgCommand = applyMessagePath.replace(/\\/g, '\\\\');
            }
            else {
                rewordPath += '.sh';
                editMessagePath += '.sh';
                applyMessagePath += '.sh';
                sequenceEditorCommand = `sh ${rewordPath}`;
                editmsgCommand = `sh ${editMessagePath}`;
                applymsgCommand = `sh ${applyMessagePath}`;
            }
            if ((_isMergeCommit || !previousCommit) && _isLastCommit) {
                editRewordMessage(EDIT_MESSAGE_FilePath, editMessagePath, osType);
                gitCommitAmend(gitService, repo, editmsgCommand, clear);
            }
            else {
                editRebaseTodo(rewordPath, osType);
                editRewordMessage(EDIT_MESSAGE_FilePath, editMessagePath, osType);
                applyMessage(applyMessagePath, osType);
                gitReabse(previousCommit, sequenceEditorCommand, editmsgCommand, handleError, clear, options, gitService, applymsgCommand, repo, osType);
            }
        }
    }));
}
function handleError(options, gitService, error, applymsgCommand, repo, clear, osType) {
    var _a;
    return __awaiter(this, void 0, void 0, function* () {
        if (error.message.includes('git commit --allow-empty')) {
            skipEmptyCommit(gitService, repo, clear);
            return;
        }
        const conflicted = (_a = (yield gitService.getStatus(repo))) === null || _a === void 0 ? void 0 : _a.conflicted;
        if (conflicted === null || conflicted === void 0 ? void 0 : conflicted.length) {
            monitorFile(conflicted, gitService, repo, applymsgCommand, clear, options, osType);
        }
        else {
            vscode_1.window.showErrorMessage(error.message);
        }
    });
}
function skipEmptyCommit(gitService, repo, clear) {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            yield gitService.skipRebase(repo);
            clear();
            yield vscode_1.commands.executeCommand(switch_1.REFRESH_COMMAND);
            yield vscode_1.window.showInformationMessage(succeedEditMessage);
        }
        catch (err) {
            console.error(err);
        }
    });
}
function monitorFile(conflicted, gitService, repo, applymsgCommand, clear, options, osType) {
    const conflictedSet = new Set(conflicted === null || conflicted === void 0 ? void 0 : conflicted.map((e) => {
        if (osType === 'win') {
            return state_1.default.logOptions.repo + '\\' + e;
        }
        else {
            return state_1.default.logOptions.repo + '/' + e;
        }
    }));
    const resolved = new Set();
    const abortRebaseButtonText = localize('abort.rebase', 'Abort Rebase');
    let executedonce = false;
    conflictedSet.forEach((file) => {
        let watcher = vscode_1.workspace.createFileSystemWatcher(file);
        disposables.push(watcher);
        watcher.onDidChange((e) => __awaiter(this, void 0, void 0, function* () {
            try {
                const data = fs.readFileSync(e.fsPath, 'utf-8');
                if (!data.includes('<<<<<<<') && !data.includes('=======') && !data.includes('>>>>>>>')) {
                    conflictedSet.delete(file);
                    resolved.add(file);
                    if (conflictedSet.size === 0) {
                        gitService.add([...resolved], repo);
                        const _isRebasing = gitService.isRebasing(repo);
                        if (_isRebasing && !executedonce) {
                            (0, child_process_1.exec)('git rebase --continue', Object.assign(Object.assign({}, options), { env: Object.assign(Object.assign({}, process_1.default.env), { GIT_EDITOR: applymsgCommand, GIT_SEQUENCE_EDITOR: undefined }) }), (error) => __awaiter(this, void 0, void 0, function* () {
                                if (error) {
                                    yield handleError(options, gitService, error, applymsgCommand, repo, clear, osType);
                                }
                                else {
                                    clear();
                                    yield vscode_1.commands.executeCommand(switch_1.REFRESH_COMMAND);
                                    yield vscode_1.window.showInformationMessage(succeedEditMessage);
                                }
                                executedonce = true;
                            }));
                        }
                    }
                }
                else {
                    conflictedSet.add(file);
                    resolved.delete(file);
                }
            }
            catch (err) {
                console.error(err);
            }
        }));
    });
    vscode_1.window
        .showInformationMessage(localize('info.conflict.editMessage', 'There are conflicts. Please resolve conflicts and continue.'), abortRebaseButtonText)
        .then((selection) => __awaiter(this, void 0, void 0, function* () {
        if (selection === abortRebaseButtonText) {
            if (!gitService.isRebasing(repo)) {
                return;
            }
            clear();
            yield gitService.abortRebase(repo);
        }
    }));
}
function editRebaseTodo(rewordPath, type) {
    if (type === 'win') {
        fs.writeFileSync(rewordPath, `
			@echo off
			setlocal enabledelayedexpansion
			set "todoFilePath=.git\\rebase-merge\\git-rebase-todo"
			set "newTodoList=.git\\temp.txt"
			set "firstLineDone=0"

			if exist !newTodoList! del !newTodoList!
			
			for /f "delims=" %%a in (%todoFilePath%) do (
				set "line=%%a"
				if !firstLineDone! equ 0 (
					set "line=!line:pick=reword!"
					set "firstLineDone=1"
				)
				echo !line! >> !newTodoList!
			)
			move /Y !newTodoList! %todoFilePath%
			endlocal`);
    }
    else {
        fs.writeFileSync(rewordPath, `
			#!/bin/sh

			todoFilePath=".git/rebase-merge/git-rebase-todo"

			if [ ! -f "$todoFilePath" ]; then
				echo "$todoFilePath does not exist."
				exit 1
			fi

			firstLine=$(head -n 1 $todoFilePath)

			if echo $firstLine | grep -q "^pick"; then
				sed -i '1s/^pick/reword/' $todoFilePath
			fi`);
    }
}
function editRewordMessage(path, editMessagePath, type) {
    if (type === 'win') {
        fs.writeFileSync(editMessagePath, `
			@echo off
            setlocal
            set "messageFilePath=%~1"
			type "${path}" > "%messageFilePath%"
            endlocal`);
    }
    else {
        fs.writeFileSync(editMessagePath, `
			#!/bin/sh

			messageFilePath="$1"
			cat ${path} > $messageFilePath`);
    }
}
function applyMessage(applyMessagePath, type) {
    if (type === 'win') {
        fs.writeFileSync(applyMessagePath, `
			@echo off
			setlocal
			set "gitDir=%cd%\\.git"
			set "mesgFilePath=%gitDir%\\rebase-merge\\message"
			set "messageFilePath=%~1"

			type "%mesgFilePath%" > "%messageFilePath%"
			endlocal`);
    }
    else {
        fs.writeFileSync(applyMessagePath, `
			#!/bin/sh
			gitDir=$(pwd)/.git
			mesgFilePath=$gitDir/rebase-merge/message
			messageFilePath=$1

			cat $mesgFilePath > $messageFilePath`);
    }
}
function* markCheckerIterator(checkers) {
    for (const { checker, params } of checkers) {
        yield checker(...params);
    }
}
function resolveQuickpick(quickPick, len, curBranch, repoName, items, gitService, curRepo, hash) {
    let title = '';
    if (len > 1) {
        title = localize('reset.mutiple.quickpick.title', 'Confirm Reset branch {0} • {1}', curBranch, repoName);
    }
    if (len === 1) {
        title = localize('reset.single.quickpick.title', 'Confirm Reset branch {0}', curBranch);
    }
    quickPick.title = title;
    quickPick.placeholder = localize('reset.quickpick.placeholder', 'Confirm Reset');
    quickPick.items = items;
    quickPick.onDidChangeSelection((selection) => __awaiter(this, void 0, void 0, function* () {
        const mode = selection[0].value;
        if (mode) {
            const handleResetSucceed = () => {
                vscode_1.commands.executeCommand(switch_1.REFRESH_COMMAND).then(() => __awaiter(this, void 0, void 0, function* () {
                    yield vscode_1.window.showInformationMessage(localize('succeed.reset', 'Reset successful'));
                }));
            };
            gitService.reset(curRepo, mode, hash, handleResetSucceed);
            quickPick.dispose();
        }
    }));
    quickPick.show();
    quickPick.onDidChangeValue((value) => {
        if (value === '') {
            quickPick.items = items;
        }
        else {
            quickPick.items = items.filter((item) => item.label.includes(value) || item.detail.includes(value));
        }
    });
}
function getOSType() {
    const type = os_1.default.type();
    switch (type) {
        case 'Windows_NT':
            return 'win';
        case 'Linux':
            return 'linux';
        case 'Darwin':
            return 'mac';
        default:
            break;
    }
}
//# sourceMappingURL=contextmenu.js.map