"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.compareFileTreeNode = exports.getOriginalChangeStackAndUpdateChange = exports.getPathMap = exports.resolveChangesCollection = exports.PathType = void 0;
const path_1 = __importDefault(require("path"));
const changes_1 = require("./changes");
const status_1 = require("./status");
var PathType;
(function (PathType) {
    PathType["FOLDER"] = "Folder";
    PathType["FILE"] = "File";
})(PathType = exports.PathType || (exports.PathType = {}));
function resolveChangesCollection(changesCollection, fileDisplayMode, workspaceRootPath = '') {
    const pathMap = getPathMap(changesCollection);
    let fileTree = {};
    Object.entries(pathMap).forEach(([path, node]) => {
        const { originalChangeStack, changeStack } = node;
        const [firstChangeItem, lastChangeItem] = (0, changes_1.getChangePair)(originalChangeStack, changeStack);
        const mergedStatus = (0, status_1.mergeStatus)(firstChangeItem, lastChangeItem);
        if (!mergedStatus) {
            delete pathMap[path];
            return;
        }
        node.status = mergedStatus;
        attachFileNode(fileTree, path, workspaceRootPath, node, fileDisplayMode);
    });
    return fileTree;
}
exports.resolveChangesCollection = resolveChangesCollection;
function getPathMap(changesCollection) {
    const pathMap = {};
    const renamedPaths = [];
    handleChangesCollection(changesCollection, pathMap, renamedPaths);
    renamedPaths.reverse().forEach((renamedPath) => {
        const renamedChangeStack = pathMap[renamedPath].changeStack;
        pathMap[renamedPath].originalChangeStack =
            getOriginalChangeStackAndUpdateChange(pathMap, renamedChangeStack);
    });
    return pathMap;
}
exports.getPathMap = getPathMap;
function handleChangesCollection(changesCollection, pathMap, renamedPaths) {
    changesCollection.reverse().forEach(({ ref, repoPath, changes }) => {
        changes.forEach((change) => {
            const { status, uri, originalUri } = change;
            const { path } = uri;
            const { path: originalPath } = originalUri;
            if (status === 3 /* Status.INDEX_RENAMED */) {
                if (!pathMap[path]) {
                    renamedPaths.push(path);
                }
                const deleteChange = { status: 6 /* Status.DELETED */, uri: originalUri, originalUri, renameUri: originalUri };
                if (pathMap[originalPath]) {
                    pathMap[originalPath].changeStack.push({ ref, change: deleteChange, isDeletedByRename: true, hidden: true });
                }
                else {
                    pathMap[originalPath] = {
                        type: PathType.FILE,
                        repoPath,
                        uri: originalUri,
                        changeStack: [{ ref, change: deleteChange, isDeletedByRename: true, hidden: true }],
                    };
                }
            }
            if (pathMap[path]) {
                pathMap[path].changeStack.push({ ref, change });
                return;
            }
            pathMap[path] = { type: PathType.FILE, repoPath, uri, changeStack: [{ ref, change }] };
        });
    });
}
function getOriginalChangeStackAndUpdateChange(pathMap, renamedChangeStack) {
    var _a;
    const lastChangeItem = renamedChangeStack[renamedChangeStack.length - 1];
    const renamedChangeItem = renamedChangeStack[0];
    const renamedChange = renamedChangeItem.change;
    const originalChangeStack = (_a = pathMap[renamedChange.originalUri.path]) === null || _a === void 0 ? void 0 : _a.changeStack;
    if (!originalChangeStack) {
        return [];
    }
    const lastOriginalChangeItem = originalChangeStack[originalChangeStack.length - 1];
    if (!lastOriginalChangeItem.isDeletedByRename) {
        return [];
    }
    // TODO: consider about rename chain
    if (renamedChangeItem.ref === lastOriginalChangeItem.ref &&
        lastChangeItem.change.status === 6 /* Status.DELETED */ &&
        (!lastChangeItem.isDeletedByRename || !lastChangeItem.hidden)) {
        lastOriginalChangeItem.hidden = false;
        lastChangeItem.hidden = true;
    }
    if (originalChangeStack[0].change.status === 3 /* Status.INDEX_RENAMED */) {
        return [
            ...getOriginalChangeStackAndUpdateChange(pathMap, originalChangeStack),
            ...originalChangeStack,
        ];
    }
    return originalChangeStack;
}
exports.getOriginalChangeStackAndUpdateChange = getOriginalChangeStackAndUpdateChange;
function attachFileNode(fileTree, filePath, workspaceRootPath, node, fileDisplayMode) {
    const { dir, base } = path_1.default.parse(filePath);
    const normalizedDir = path_1.default.normalize(dir);
    const workspaceDir = normalizedDir.substring(workspaceRootPath.length + 1);
    const dirSegments = workspaceDir.split(path_1.default.sep);
    let fileNode = fileTree;
    if (fileDisplayMode === 'tree') {
        dirSegments.reduce((prePath, dirSegment) => {
            if (!dirSegment) {
                return prePath;
            }
            const currentPath = `${prePath}${path_1.default.sep}${dirSegment}`;
            if (!fileNode[dirSegment]) {
                fileNode[dirSegment] = {
                    type: PathType.FOLDER,
                    path: currentPath,
                    children: {},
                };
            }
            fileNode = fileNode[dirSegment].children;
            return currentPath;
        }, workspaceRootPath);
    }
    fileNode[base] = node;
}
function compareFileTreeNode([name, node], [anotherName, anotherNode]) {
    node;
    if (node.type === PathType.FOLDER && anotherNode.type === PathType.FILE) {
        return -1;
    }
    if (anotherNode.type === PathType.FOLDER && node.type === PathType.FILE) {
        return 1;
    }
    return compareAndDisambiguateByLength(name, anotherName);
}
exports.compareFileTreeNode = compareFileTreeNode;
function compareAndDisambiguateByLength(one, other) {
    const collator = new Intl.Collator(undefined, { numeric: true });
    // Check for differences
    let result = collator.compare(one, other);
    if (result !== 0) {
        return result;
    }
    // In a numeric comparison, `foo1` and `foo01` will compare as equivalent.
    // Disambiguate by sorting the shorter string first.
    if (one.length !== other.length) {
        return one.length < other.length ? -1 : 1;
    }
    return 0;
}
//# sourceMappingURL=tree.js.map