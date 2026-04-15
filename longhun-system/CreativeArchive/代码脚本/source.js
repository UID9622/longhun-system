"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
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
exports.Source = void 0;
/* eslint-disable no-undef */
const path_1 = require("path");
const inversify_1 = require("inversify");
const vscode_1 = require("vscode");
const types_1 = require("../../../container/types");
const service_1 = require("../../../git/service");
const graph_1 = require("../../../git/graph");
const tree_1 = require("../../../git/changes/tree");
const ChangeTreeDataProvider_1 = require("../../changes/ChangeTreeDataProvider");
const switch_1 = require("../../../commands/switch");
const filter_1 = require("../../../commands/filter");
const input_1 = require("../../../commands/input");
const link_1 = require("./link");
const state_1 = __importDefault(require("./state"));
const DEBOUNCE_INTERVAL = 750;
const focusOnChanges = 'git-history.changes.focus';
const focusOnDetail = 'git-history.detail.focus';
let Source = class Source {
    constructor(context, git, graph, ChangeTreeDataProvider) {
        this.context = context;
        this.git = git;
        this.graph = graph;
        this.ChangeTreeDataProvider = ChangeTreeDataProvider;
        this.repositoryRefBatchnumberMap = new Map();
        this.commitsEventEmitter = new vscode_1.EventEmitter();
        this.INITIAL_FETCH_SIZE = 100;
        this.totalCount = 0;
        this.debouncedRefresh = debounceDelay(() => vscode_1.commands.executeCommand(switch_1.REFRESH_COMMAND), DEBOUNCE_INTERVAL);
        this.changesCollection = [];
        this.fileDisplayMode = 'tree';
        this.repoStateChangeHandler = (repository) => {
            const fsPath = repository.rootUri.fsPath;
            if (!this.repositoryRefBatchnumberMap.has(fsPath)) {
                this.repositoryRefBatchnumberMap.set(fsPath, new Map());
            }
            const repo = state_1.default.logOptions.repo;
            if (fsPath === repo) {
                this.debouncedRefresh();
            }
        };
        this.git.reposEvent.event(() => {
            this.git.onDidRepoChange(this.repoStateChangeHandler);
        });
        const timer = setInterval(() => {
            const succeed = this.git.onDidRepoChange(this.repoStateChangeHandler);
            if (succeed) {
                clearInterval(timer);
            }
        }, 100);
    }
    getSwitchSubscriber() {
        return this.switchSubscriber;
    }
    getCommitsEventEmitter() {
        return this.commitsEventEmitter;
    }
    getWorkspacePath() {
        return Promise.resolve(vscode_1.workspace.workspaceFolders[0].uri.fsPath);
    }
    getDefaultRepository() {
        const repoPath = this.git.getDefaultRepository();
        if (!repoPath) {
            return Promise.resolve();
        }
        return Promise.resolve({
            name: (0, path_1.parse)(repoPath).base,
            path: repoPath,
        });
    }
    subscribeSwitcher(handler) {
        return __awaiter(this, void 0, void 0, function* () {
            this.switchSubscriber = handler;
        });
    }
    setDetailSubscriber(handler) {
        return __awaiter(this, void 0, void 0, function* () {
            this.detailSubscriber = handler;
        });
    }
    setShowProgressSubscriber(handler) {
        return __awaiter(this, void 0, void 0, function* () {
            this.showProgressSubscriber = handler;
        });
    }
    resetLog() {
        return vscode_1.commands.executeCommand(switch_1.RESET_COMMAND);
    }
    switchReference() {
        return __awaiter(this, void 0, void 0, function* () {
            yield vscode_1.commands.executeCommand(switch_1.SWITCH_BRANCH_COMMAND);
        });
    }
    filterMessage() {
        return __awaiter(this, void 0, void 0, function* () {
            yield vscode_1.commands.executeCommand(filter_1.FILTER_MESSAGE_COMMAND);
        });
    }
    filterAuthor() {
        return __awaiter(this, void 0, void 0, function* () {
            yield vscode_1.commands.executeCommand(filter_1.FILTER_AUTHOR_COMMAND);
        });
    }
    inputHash() {
        return __awaiter(this, void 0, void 0, function* () {
            return vscode_1.commands.executeCommand(input_1.INPUT_HASH_COMMAND);
        });
    }
    showWarningMessage(message) {
        return __awaiter(this, void 0, void 0, function* () {
            vscode_1.window.showWarningMessage(message);
        });
    }
    getCommits(handler, options) {
        return __awaiter(this, void 0, void 0, function* () {
            const { repo, ref } = options;
            const batchNumber = this.getBatchNumber(repo, ref, false);
            const count = (batchNumber + 1) * this.INITIAL_FETCH_SIZE;
            this.showProgressSubscriber && this.showProgressSubscriber();
            const firstBatchCommits = yield this.git.getCommits(Object.assign(Object.assign({}, options), { count }));
            const totalCount = Number(yield this.git.getCommitsTotalCount(options));
            this.totalCount = totalCount;
            this.commitsEventEmitter.fire({ totalCount, count });
            this.graph.registerHandler(handler, batchNumber);
            this.graph.attachGraphAndPost({
                totalCount,
                batchNumber,
                commits: firstBatchCommits !== null && firstBatchCommits !== void 0 ? firstBatchCommits : [],
                options,
                initializing: true
            });
        });
    }
    loadMoreCommits(handler, options) {
        return __awaiter(this, void 0, void 0, function* () {
            const { repo, ref } = options;
            const batchNumber = this.getBatchNumber(repo, ref, true);
            const skip = (batchNumber + 1) * this.INITIAL_FETCH_SIZE;
            this.showProgressSubscriber && this.showProgressSubscriber();
            const batchCommits = yield this.git.getCommits(Object.assign(Object.assign({}, options), { count: this.INITIAL_FETCH_SIZE, skip }));
            const totalCount = Number(yield this.git.getCommitsTotalCount(options));
            this.totalCount = totalCount;
            this.commitsEventEmitter.fire({ totalCount, count: skip + this.INITIAL_FETCH_SIZE });
            this.graph.attachGraphAndPost({
                totalCount,
                batchNumber: batchNumber + 1,
                commits: batchCommits !== null && batchCommits !== void 0 ? batchCommits : [],
                options,
                initializing: false,
            });
        });
    }
    setDescription(_handler, count) {
        this.commitsEventEmitter.fire({ totalCount: this.totalCount, count });
    }
    getBatchNumber(repo, ref, increaseBatchNumber) {
        var _a, _b;
        let batchNumber = 0;
        if (!this.repositoryRefBatchnumberMap.has(repo)) {
            this.repositoryRefBatchnumberMap.set(repo, new Map());
        }
        const refBatchnumberMap = this.repositoryRefBatchnumberMap.get(repo);
        if (ref) {
            if (refBatchnumberMap.has(ref)) {
                batchNumber = (_a = refBatchnumberMap.get(ref)) !== null && _a !== void 0 ? _a : 0;
                increaseBatchNumber && refBatchnumberMap.set(ref, batchNumber + 1);
            }
            else {
                refBatchnumberMap.set(ref, 0);
            }
        }
        else {
            if (refBatchnumberMap.has('all')) {
                batchNumber = (_b = refBatchnumberMap.get('all')) !== null && _b !== void 0 ? _b : 0;
                increaseBatchNumber && refBatchnumberMap.set('all', batchNumber + 1);
            }
            else {
                refBatchnumberMap.set('all', 0);
            }
        }
        return batchNumber;
    }
    toggleDisplay() {
        this.fileDisplayMode = this.fileDisplayMode === 'tree' ? 'inline' : 'tree';
        const newFileTree = (0, tree_1.resolveChangesCollection)(this.changesCollection, this.fileDisplayMode, (0, path_1.normalize)(vscode_1.workspace.workspaceFolders[0].uri.path));
        this.updateTreeView(newFileTree);
    }
    viewChanges(refs) {
        return __awaiter(this, void 0, void 0, function* () {
            yield vscode_1.commands.executeCommand(focusOnChanges);
            const changesCollection = yield this.git.getChangesCollection(state_1.default.logOptions.repo || '', refs);
            this.changesCollection = changesCollection;
            const newFileTree = (0, tree_1.resolveChangesCollection)(changesCollection, this.fileDisplayMode, (0, path_1.normalize)(vscode_1.workspace.workspaceFolders[0].uri.path));
            this.updateTreeView(newFileTree);
        });
    }
    viewDetails(commits) {
        return __awaiter(this, void 0, void 0, function* () {
            yield vscode_1.commands.executeCommand(focusOnDetail);
            this.detailSubscriber && this.detailSubscriber(commits);
        });
    }
    autoRefreshLog() {
        return __awaiter(this, void 0, void 0, function* () {
            vscode_1.commands.executeCommand(switch_1.REFRESH_COMMAND);
        });
    }
    onReposChange(handler) {
        this.git.onReposChange((repos) => {
            handler(repos.map((repoPath) => ({
                name: (0, path_1.parse)(repoPath).base,
                path: repoPath,
            })));
        });
    }
    updateTreeView(fileTree) {
        this.ChangeTreeDataProvider.refresh(fileTree);
    }
};
__decorate([
    (0, link_1.link)('promise'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", void 0)
], Source.prototype, "getWorkspacePath", null);
__decorate([
    (0, link_1.link)('promise'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", void 0)
], Source.prototype, "getDefaultRepository", null);
__decorate([
    (0, link_1.link)('subscription'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Function]),
    __metadata("design:returntype", Promise)
], Source.prototype, "subscribeSwitcher", null);
__decorate([
    (0, link_1.link)('subscription'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Function]),
    __metadata("design:returntype", Promise)
], Source.prototype, "setDetailSubscriber", null);
__decorate([
    (0, link_1.link)('subscription'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Function]),
    __metadata("design:returntype", Promise)
], Source.prototype, "setShowProgressSubscriber", null);
__decorate([
    (0, link_1.link)('promise'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", void 0)
], Source.prototype, "resetLog", null);
__decorate([
    (0, link_1.link)('subscription'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], Source.prototype, "switchReference", null);
__decorate([
    (0, link_1.link)('subscription'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], Source.prototype, "filterMessage", null);
__decorate([
    (0, link_1.link)('subscription'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], Source.prototype, "filterAuthor", null);
__decorate([
    (0, link_1.link)('promise'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], Source.prototype, "inputHash", null);
__decorate([
    (0, link_1.link)('promise'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [String]),
    __metadata("design:returntype", Promise)
], Source.prototype, "showWarningMessage", null);
__decorate([
    (0, link_1.link)('subscription'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Function, Object]),
    __metadata("design:returntype", Promise)
], Source.prototype, "getCommits", null);
__decorate([
    (0, link_1.link)('subscription'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Function, Object]),
    __metadata("design:returntype", Promise)
], Source.prototype, "loadMoreCommits", null);
__decorate([
    (0, link_1.link)('subscription'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Function, Number]),
    __metadata("design:returntype", void 0)
], Source.prototype, "setDescription", null);
__decorate([
    (0, link_1.link)('promise'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Array]),
    __metadata("design:returntype", Promise)
], Source.prototype, "viewChanges", null);
__decorate([
    (0, link_1.link)('promise'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Array]),
    __metadata("design:returntype", Promise)
], Source.prototype, "viewDetails", null);
__decorate([
    (0, link_1.link)('promise'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], Source.prototype, "autoRefreshLog", null);
__decorate([
    (0, link_1.link)('subscription'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Function]),
    __metadata("design:returntype", void 0)
], Source.prototype, "onReposChange", null);
Source = __decorate([
    (0, inversify_1.injectable)(),
    __param(0, (0, inversify_1.inject)(types_1.TYPES.ExtensionContext)),
    __metadata("design:paramtypes", [Object, service_1.GitService,
        graph_1.GitGraph,
        ChangeTreeDataProvider_1.ChangeTreeDataProvider])
], Source);
exports.Source = Source;
function debounceDelay(fn, wait) {
    let timer = null;
    return () => {
        if (timer) {
            clearTimeout(timer);
        }
        timer = setTimeout(() => {
            fn();
            clearTimeout(timer);
        }, wait);
    };
}
//# sourceMappingURL=source.js.map