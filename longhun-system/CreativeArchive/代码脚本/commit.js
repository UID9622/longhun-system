"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.parseCommit = exports.parseCommits = exports.REFS_SEPARATOR = exports.CommitIndex2 = exports.CommitIndex = void 0;
var CommitIndex;
(function (CommitIndex) {
    CommitIndex[CommitIndex["HASH"] = 0] = "HASH";
    CommitIndex[CommitIndex["REF_NAMES"] = 1] = "REF_NAMES";
    CommitIndex[CommitIndex["MESSAGE"] = 2] = "MESSAGE";
    CommitIndex[CommitIndex["PARENTS"] = 3] = "PARENTS";
    CommitIndex[CommitIndex["COMMIT_DATE"] = 4] = "COMMIT_DATE";
    CommitIndex[CommitIndex["AUTHOR_EMAIL"] = 5] = "AUTHOR_EMAIL";
    CommitIndex[CommitIndex["AUTHOR_NAME"] = 6] = "AUTHOR_NAME";
    CommitIndex[CommitIndex["AUTHOR_DATE"] = 7] = "AUTHOR_DATE";
    CommitIndex[CommitIndex["GRAPH_SLICE"] = 8] = "GRAPH_SLICE";
})(CommitIndex = exports.CommitIndex || (exports.CommitIndex = {}));
var CommitIndex2;
(function (CommitIndex2) {
    CommitIndex2[CommitIndex2["BRANCHES"] = 0] = "BRANCHES";
    CommitIndex2[CommitIndex2["HASH"] = 1] = "HASH";
    CommitIndex2[CommitIndex2["REF_NAMES"] = 2] = "REF_NAMES";
    CommitIndex2[CommitIndex2["MESSAGE"] = 3] = "MESSAGE";
    CommitIndex2[CommitIndex2["PARENTS"] = 4] = "PARENTS";
    CommitIndex2[CommitIndex2["COMMIT_DATE"] = 5] = "COMMIT_DATE";
    CommitIndex2[CommitIndex2["AUTHOR_EMAIL"] = 6] = "AUTHOR_EMAIL";
    CommitIndex2[CommitIndex2["AUTHOR_NAME"] = 7] = "AUTHOR_NAME";
    CommitIndex2[CommitIndex2["AUTHOR_DATE"] = 8] = "AUTHOR_DATE";
    CommitIndex2[CommitIndex2["GRAPH_SLICE"] = 9] = "GRAPH_SLICE";
})(CommitIndex2 = exports.CommitIndex2 || (exports.CommitIndex2 = {}));
exports.REFS_SEPARATOR = ", ";
function parseCommits(data) {
    const commitRegex = /([0-9a-f]{40})\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)(?:\n([^]*?))?(?:\x00)/gm;
    let commits = [];
    let commitData;
    let ref;
    let parents;
    let match;
    do {
        match = commitRegex.exec(data);
        if (match === null) {
            break;
        }
        [commitData, ref, , , , , , parents] = match;
        // Stop excessive memory usage by using substr -- https://bugs.chromium.org/p/v8/issues/detail?id=2869
        const commit = [
            ` ${ref}`.substr(1),
            parents ? parents.split(" ") : [],
            commitData,
        ];
        commits.push(commit);
    } while (true);
    return commits;
}
exports.parseCommits = parseCommits;
function parseCommit(commitData) {
    const commitRegex = /([0-9a-f]{40})\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)\n(.*)(?:\n([^]*?))?(?:\x00)(.*)\n(.*)\n(.*)/g;
    let ref;
    let refNames;
    let authorName;
    let authorEmail;
    let authorDate;
    let commitDate;
    let parents;
    let message;
    let commitPosition;
    let commitColor;
    let stringifiedLines;
    let match;
    match = commitRegex.exec(commitData);
    [
        ,
        ref,
        refNames,
        authorName,
        authorEmail,
        authorDate,
        commitDate,
        parents,
        message,
        commitPosition,
        commitColor,
        stringifiedLines,
    ] = match;
    if (message[message.length - 1] === "\n") {
        message = message.substr(0, message.length - 1);
    }
    // Stop excessive memory usage by using substr -- https://bugs.chromium.org/p/v8/issues/detail?id=2869
    return [
        ` ${ref}`.substr(1),
        refNames ? refNames.split(exports.REFS_SEPARATOR) : [],
        ` ${message}`.substr(1),
        parents ? parents.split(" ") : [],
        new Date(Number(authorDate) * 1000).toLocaleString(),
        ` ${authorEmail}`.substr(1),
        ` ${authorName}`.substr(1),
        new Date(Number(commitDate) * 1000).toLocaleString(),
        [Number(commitPosition), commitColor, JSON.parse(stringifiedLines)],
    ];
}
exports.parseCommit = parseCommit;
//# sourceMappingURL=commit.js.map