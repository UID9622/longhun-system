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
Object.defineProperty(exports, "__esModule", { value: true });
exports.ChangeTreeDataProvider = void 0;
const vscode_1 = require("vscode");
const inversify_1 = require("inversify");
const utils_1 = require("../../git/utils");
const constants_1 = require("../common/constants");
const tree_1 = require("../../git/changes/tree");
let ChangeTreeDataProvider = class ChangeTreeDataProvider {
    constructor() {
        this._onDidChangeTreeData = new vscode_1.EventEmitter();
        this.onDidChangeTreeData = this._onDidChangeTreeData.event;
        this.fileTree = {};
    }
    getTreeItem(element) {
        return element;
    }
    getChildren(element) {
        return Promise.resolve(Object.entries(element ? element.children : this.fileTree)
            .sort(utils_1.compareFileTreeNode)
            .map(([name, props]) => new Path(name, props)));
    }
    refresh(fileTree) {
        this.fileTree = fileTree;
        this._onDidChangeTreeData.fire();
    }
};
ChangeTreeDataProvider = __decorate([
    (0, inversify_1.injectable)(),
    __metadata("design:paramtypes", [])
], ChangeTreeDataProvider);
exports.ChangeTreeDataProvider = ChangeTreeDataProvider;
class Path extends vscode_1.TreeItem {
    constructor(label, props) {
        super(label);
        this.label = label;
        this.props = props;
        this.children = this.props.children;
        this.iconPath = vscode_1.ThemeIcon[this.props.type];
        this.resourceUri = this.getResourceUri();
        this.collapsibleState = this.getCollapsibleState();
        this.command = this.getCommand();
    }
    getResourceUri() {
        if (this.props.type === tree_1.PathType.FILE) {
            const { uri } = this.props;
            return uri.with({
                scheme: constants_1.EXTENSION_SCHEME,
                query: JSON.stringify({ status: this.props.status }),
            });
        }
        if (this.props.type === tree_1.PathType.FOLDER) {
            return vscode_1.Uri.file(this.label);
        }
    }
    getCollapsibleState() {
        const { type } = this.props;
        const STATE_MAP = {
            [tree_1.PathType.FOLDER]: vscode_1.TreeItemCollapsibleState.Expanded,
            [tree_1.PathType.FILE]: vscode_1.TreeItemCollapsibleState.None,
        };
        return STATE_MAP[type];
    }
    getCommand() {
        if (this.props.type === tree_1.PathType.FILE) {
            return {
                title: "diff",
                command: "vscode.diff",
                arguments: (0, utils_1.getDiffUriPair)(this.props),
            };
        }
    }
}
//# sourceMappingURL=ChangeTreeDataProvider.js.map