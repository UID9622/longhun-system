"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.removeItemsByIndexList = exports.compareFileTreeNode = exports.getUser = exports.sanitizePath = exports.assign = exports.getDiffUriPair = exports.parseGitAuthors = exports.parseGitConfig = void 0;
const inversify_config_1 = require("../container/inversify.config");
const changes_1 = require("./changes/changes");
const tree_1 = require("./changes/tree");
const service_1 = require("./service");
function parseGitConfig(data) {
    const configRex = /(.*)=(.*)\n?/gm;
    const config = {};
    let key;
    let value;
    let match;
    do {
        match = configRex.exec(data);
        if (match === null) {
            break;
        }
        [, key, value] = match;
        config[key] = value;
    } while (true);
    return config;
}
exports.parseGitConfig = parseGitConfig;
function parseGitAuthors(data) {
    const authorRex = / *[0-9]+\t(.+) +<(.*)>\n?/gm;
    const authors = [];
    let name;
    let email;
    let match;
    do {
        match = authorRex.exec(data);
        if (match === null) {
            break;
        }
        [, name, email] = match;
        authors.push({ name, email });
    } while (true);
    return authors;
}
exports.parseGitAuthors = parseGitAuthors;
function getDiffUriPair(node) {
    const gitService = inversify_config_1.container.get(service_1.GitService);
    const { uri, originalChangeStack, changeStack } = node;
    const [{ change: preChange, ref: preRef }, { ref: curRef }] = (0, changes_1.getChangePair)(originalChangeStack, changeStack);
    return [
        gitService.toGitUri(preChange.originalUri, `${preRef}~`),
        gitService.toGitUri(uri, curRef),
    ];
}
exports.getDiffUriPair = getDiffUriPair;
function assign(destination, ...sources) {
    for (const source of sources) {
        Object.keys(source).forEach((key) => (destination[key] = source[key]));
    }
    return destination;
}
exports.assign = assign;
function sanitizePath(path) {
    return path.replace(/^([a-z]):\\/i, (_, letter) => `${letter.toUpperCase()}:\\`);
}
exports.sanitizePath = sanitizePath;
/** @deprecated */
function getUser(shortLog) {
    const matches = shortLog.match(/ *[0-9]+\t(.+) +<(.*)>/);
    return {
        name: (matches === null || matches === void 0 ? void 0 : matches[1]) || "",
        email: (matches === null || matches === void 0 ? void 0 : matches[2]) || "",
    };
}
exports.getUser = getUser;
// TODO: take functions below to another directory
function compareFileTreeNode([name, node], [anotherName, anotherNode]) {
    node;
    if (node.type === tree_1.PathType.FOLDER && anotherNode.type === tree_1.PathType.FILE) {
        return -1;
    }
    if (anotherNode.type === tree_1.PathType.FOLDER && node.type === tree_1.PathType.FILE) {
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
function removeItemsByIndexList(array, indexList) {
    for (var i = indexList.length - 1; i >= 0; i--) {
        array.splice(indexList[i], 1);
    }
}
exports.removeItemsByIndexList = removeItemsByIndexList;
//# sourceMappingURL=utils.js.map