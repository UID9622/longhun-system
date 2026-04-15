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
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
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
exports.GitService = void 0;
const child_process_1 = require("child_process");
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const process_1 = __importDefault(require("process"));
const inversify_1 = require("inversify");
const simple_git_1 = __importDefault(require("simple-git"));
const threads_1 = require("threads");
const vscode_1 = require("vscode");
const nls = __importStar(require("vscode-nls"));
const state_1 = __importDefault(require("../views/common/data/state"));
const types_1 = require("../container/types");
const api_1 = require("./api");
const changes_1 = require("./changes/changes");
const utils_1 = require("./utils");
const LOG_TYPE_ARGS = ['--branches', '--remotes', '--tags'];
const localize = nls.loadMessageBundle();
let GitService = class GitService {
    constructor(context) {
        this.context = context;
        this.storedRepos = [];
        this.reposEvent = new vscode_1.EventEmitter();
        this.pool = (0, threads_1.Pool)(() => (0, threads_1.spawn)(new threads_1.Worker('./worker')), 8);
        this.repositoryMap = new Map();
        const workspaceFolders = this.getWorkSpaceFolders();
        if (workspaceFolders) {
            this.rootRepoPath = workspaceFolders[0].uri.fsPath;
            if (!state_1.default.logOptions.repo) {
                Object.assign(state_1.default.logOptions, { repo: this.rootRepoPath });
            }
            this.initializeGitApi();
        }
    }
    initializeGitApi() {
        return __awaiter(this, void 0, void 0, function* () {
            this.gitExt = (yield (0, api_1.getBuiltInGitApi)());
            const gitBinPath = yield (0, api_1.getGitBinPath)();
            this.git = (0, simple_git_1.default)(this.rootRepoPath, {
                binary: gitBinPath,
                maxConcurrentProcesses: 10,
            });
            this.initializeReposEvents();
        });
    }
    initializeReposEvents() {
        var _a, _b;
        const commonHandler = () => {
            this.storedRepos = this.getRepositories() || [];
            this.reposEvent.fire(this.storedRepos);
            if (!state_1.default.logOptions.repo) {
                Object.assign(state_1.default.logOptions, { repo: this.getDefaultRepository() });
            }
        };
        const closeRepositoryHandler = (repository) => {
            var _a;
            commonHandler();
            (_a = this.repositoryMap.get(repository.rootUri.fsPath)) === null || _a === void 0 ? void 0 : _a.dispose();
            this.repositoryMap.delete(repository.rootUri.fsPath);
        };
        (_a = this.gitExt) === null || _a === void 0 ? void 0 : _a.onDidOpenRepository(commonHandler);
        (_b = this.gitExt) === null || _b === void 0 ? void 0 : _b.onDidCloseRepository(closeRepositoryHandler);
    }
    getConfig(repo) {
        var _a, _b;
        return (_b = (_a = this.git) === null || _a === void 0 ? void 0 : _a.cwd(repo)) === null || _b === void 0 ? void 0 : _b.raw('config', '--list').then((res) => (0, utils_1.parseGitConfig)(res));
    }
    getDefaultRepository() {
        const workspaceFolders = this.getWorkSpaceFolders();
        if (workspaceFolders) {
            const workspacePath = workspaceFolders[0].uri.fsPath;
            const repos = this.getRepositories();
            return repos.find((fsPath) => fsPath === workspacePath) || repos[0];
        }
        return null;
    }
    getRepositories() {
        var _a;
        return ((_a = this.gitExt) === null || _a === void 0 ? void 0 : _a.repositories.map(({ rootUri }) => rootUri.fsPath)) || [];
    }
    getRefs(options) {
        var _a;
        const { repo = this.rootRepoPath } = options;
        return (_a = this.git) === null || _a === void 0 ? void 0 : _a.cwd(repo).raw('for-each-ref', '--sort', '-committerdate', '--format=%(objectname) %(refname)').then((res) => {
            const refs = [];
            res.split('\n').forEach((item) => {
                if (!item) {
                    return;
                }
                const [, hash, type, name] = item.match(/^([A-Fa-f0-9]+) refs\/(heads|remotes|tags)\/(.*)$/) || [];
                if (hash && type && name) {
                    refs.push({ hash, type, name });
                }
            });
            return refs;
        });
    }
    getAuthors(options) {
        var _a, _b, _c, _d;
        return __awaiter(this, void 0, void 0, function* () {
            const { repo = this.rootRepoPath } = options;
            const [settledShortLogResult, settledConfigResult] = yield Promise.allSettled([(_b = (_a = this.git) === null || _a === void 0 ? void 0 : _a.cwd(repo)) === null || _b === void 0 ? void 0 : _b.raw('shortlog', '-ens', '--all'), this.getConfig(repo)]);
            if (settledShortLogResult.status !== 'fulfilled' || settledConfigResult.status !== 'fulfilled') {
                return [];
            }
            const allAuthors = (0, utils_1.parseGitAuthors)(settledShortLogResult.value || '');
            const selfAuthor = {
                name: ((_c = settledConfigResult.value) === null || _c === void 0 ? void 0 : _c['user.name']) || '',
                email: ((_d = settledConfigResult.value) === null || _d === void 0 ? void 0 : _d['user.email']) || '',
                isSelf: true,
            };
            const otherAuthors = allAuthors.filter(({ name, email }) => name !== selfAuthor.name || email !== selfAuthor.email);
            if (otherAuthors.length === allAuthors.length) {
                return allAuthors;
            }
            return [selfAuthor, ...otherAuthors];
        });
    }
    show(commitHash, filePath) {
        var _a;
        return __awaiter(this, void 0, void 0, function* () {
            const repoPath = this.getRepositories()
                .sort((fsPathA, fsPathB) => fsPathB.length - fsPathA.length)
                .find((fsPath) => filePath.startsWith(fsPath));
            return yield ((_a = this.gitExt) === null || _a === void 0 ? void 0 : _a.repositories.find((repo) => repo.rootUri.fsPath === repoPath).show(commitHash, filePath));
        });
    }
    getCommits(options) {
        var _a;
        return __awaiter(this, void 0, void 0, function* () {
            const COMMIT_FORMAT = '%H%n%D%n%aN%n%aE%n%at%n%ct%n%P%n%B';
            const { repo, authors, keyword, ref, maxLength, count, skip } = options || {};
            const args = ['-c', 'log.showSignature=false', 'log', `--format=${COMMIT_FORMAT}`, '-z', '--author-date-order'];
            if (authors && authors.length) {
                args.push(...authors.map((author) => `--author=${author}`));
            }
            if (keyword) {
                args.push(`--grep=${keyword}`);
            }
            if (maxLength) {
                args.push(`-n${maxLength}`);
            }
            if (skip) {
                args.push(`--skip=${skip}`);
            }
            if (count) {
                args.push(`-n${count}`);
            }
            if (ref) {
                args.push(ref, '--');
            }
            else {
                args.push(...LOG_TYPE_ARGS);
            }
            return yield ((_a = this.git) === null || _a === void 0 ? void 0 : _a.cwd(repo || this.rootRepoPath).raw(args).then((res) => this.pool.queue(({ parseCommits }) => parseCommits(res))).catch((err) => console.error(err)));
        });
    }
    getCommitsTotalCount(options) {
        var _a;
        return __awaiter(this, void 0, void 0, function* () {
            const { repo, ref, authors, keyword } = options || {};
            // TODO: reuse arguments assembly process in getCommits
            const args = ['rev-list', ...(ref ? [ref] : LOG_TYPE_ARGS), '--count'];
            if (authors && authors.length) {
                args.push(...authors.map((author) => `--author=${author}`));
            }
            if (keyword) {
                args.push(`--grep=${keyword}`);
            }
            return yield ((_a = this.git) === null || _a === void 0 ? void 0 : _a.cwd(repo || this.rootRepoPath).raw(args).catch((err) => console.error(err)));
        });
    }
    getChangesCollection(repoPath, refs) {
        return __awaiter(this, void 0, void 0, function* () {
            return yield Promise.all(refs.map((ref) => this.getChangesByRef(repoPath, ref).then((changes) => ({
                ref,
                repoPath,
                changes,
            }))));
        });
    }
    getChangesByRef(repoPath, ref) {
        return __awaiter(this, void 0, void 0, function* () {
            const args = ['log', '-p', '-1', '--pretty=format:', '--name-status', '-z', ref];
            return yield this.git.cwd(repoPath || this.rootRepoPath)
                .raw(args)
                .then((res) => (0, changes_1.parseGitChanges)(repoPath, res));
        });
    }
    onReposChange(handler) {
        handler(this.storedRepos);
        this.reposEvent.event((repos) => {
            handler(repos);
        });
    }
    onDidRepoChange(repoStateChangeHandler) {
        var _a, _b, _c;
        if (!((_a = this.gitExt) === null || _a === void 0 ? void 0 : _a.repositories)) {
            return false;
        }
        (_c = (_b = this.gitExt) === null || _b === void 0 ? void 0 : _b.repositories) === null || _c === void 0 ? void 0 : _c.forEach((repository) => __awaiter(this, void 0, void 0, function* () {
            this.repositoryMap.set(repository.rootUri.fsPath, repository.state.onDidChange(() => repoStateChangeHandler(repository), null, this.context.subscriptions));
        }));
        return true;
    }
    toGitUri(uri, ref) {
        var _a;
        return (_a = this.gitExt) === null || _a === void 0 ? void 0 : _a.toGitUri(uri, ref);
    }
    amendCommit(repo, editmsgCommand, callback) {
        (0, child_process_1.exec)(`git commit --amend`, {
            cwd: repo,
            env: Object.assign(Object.assign({}, process_1.default.env), { GIT_EDITOR: editmsgCommand }),
        }, (err, _stdout, stderr) => {
            if (!err) {
                callback();
            }
            else {
                vscode_1.window.showErrorMessage(stderr);
            }
        });
    }
    isMergeCommit(hash, repo) {
        var _a, _b;
        return __awaiter(this, void 0, void 0, function* () {
            const output = (_b = (yield ((_a = this.git) === null || _a === void 0 ? void 0 : _a.cwd(repo).show(['--merges', hash])))) === null || _b === void 0 ? void 0 : _b.trim();
            return output.length > 0;
        });
    }
    isCommitInCurrentRef(hash, repo) {
        var _a;
        return __awaiter(this, void 0, void 0, function* () {
            const current = (yield this.getStatus(repo)).current;
            const all = (yield ((_a = this.git) === null || _a === void 0 ? void 0 : _a.branch(['--contains', hash]))).all;
            return all.includes(current);
        });
    }
    getStatus(repo) {
        var _a;
        return __awaiter(this, void 0, void 0, function* () {
            return yield ((_a = this.git) === null || _a === void 0 ? void 0 : _a.cwd(repo).status(['--porcelain']));
        });
    }
    add(filePath, repo) {
        filePath = filePath.map((file) => `"${file}"`);
        try {
            (0, child_process_1.execSync)(`git add ${filePath.join(' ')}`, Object.assign(Object.assign({}, process_1.default.env), { cwd: repo }));
        }
        catch (error) {
            console.error(error);
        }
    }
    getPreviousCommit(hash, repo) {
        var _a;
        return __awaiter(this, void 0, void 0, function* () {
            return yield ((_a = this.git) === null || _a === void 0 ? void 0 : _a.cwd(repo).revparse([`${hash}^`]));
        });
    }
    isLastCommit(hash, repo) {
        var _a;
        return __awaiter(this, void 0, void 0, function* () {
            const lastHash = yield ((_a = this.git) === null || _a === void 0 ? void 0 : _a.cwd(repo).revparse(['HEAD']));
            return hash === lastHash;
        });
    }
    isRebasing(repo) {
        const rebaseMerge = path_1.default.join(repo, '.git', 'rebase-merge');
        const rebaseApply = path_1.default.join(repo, '.git', 'rebase-apply');
        return fs_1.default.existsSync(rebaseMerge) || fs_1.default.existsSync(rebaseApply);
    }
    skipRebase(repo) {
        var _a;
        return __awaiter(this, void 0, void 0, function* () {
            yield ((_a = this.git) === null || _a === void 0 ? void 0 : _a.cwd(repo).rebase(['--skip']));
        });
    }
    abortRebase(repo) {
        var _a;
        return __awaiter(this, void 0, void 0, function* () {
            yield ((_a = this.git) === null || _a === void 0 ? void 0 : _a.cwd(repo).rebase(['--abort']));
        });
    }
    reset(repo, mode, hash, callback) {
        (0, child_process_1.exec)(`git reset --${mode} ${hash}`, Object.assign(Object.assign({}, process_1.default.env), { cwd: repo }), (err, _stdout, stderr) => {
            if (!err) {
                callback();
            }
            else {
                vscode_1.window.showErrorMessage(stderr);
            }
        });
    }
    getWorkSpaceFolders() {
        const workspaceFolders = vscode_1.workspace.workspaceFolders;
        if (!workspaceFolders) {
            const value = localize('error.noWorkspace.open', 'No workspace is currently opened.');
            vscode_1.window.showErrorMessage(value);
            return null;
        }
        return workspaceFolders;
    }
};
GitService = __decorate([
    (0, inversify_1.injectable)(),
    __param(0, (0, inversify_1.inject)(types_1.TYPES.ExtensionContext)),
    __metadata("design:paramtypes", [Object])
], GitService);
exports.GitService = GitService;
//# sourceMappingURL=service.js.map