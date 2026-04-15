"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const assert_1 = require("assert");
const vscode_1 = require("vscode");
const tree_1 = require("./tree");
suite("#getPathMap()", () => {
    test("should return path map when given a changes collection", () => {
        const CHANGES_COLLECTION = [
            {
                ref: "1",
                repoPath: "",
                changes: [
                    {
                        uri: vscode_1.Uri.parse("/src/app.ts"),
                        originalUri: vscode_1.Uri.parse("/src/app.ts"),
                        renameUri: vscode_1.Uri.parse("/src/app.ts"),
                        status: 5 /* Status.MODIFIED */,
                    },
                    {
                        uri: vscode_1.Uri.parse("/index.ts"),
                        originalUri: vscode_1.Uri.parse("/index.ts"),
                        renameUri: vscode_1.Uri.parse("/index.ts"),
                        status: 1 /* Status.INDEX_ADDED */,
                    },
                    {
                        uri: vscode_1.Uri.parse("/package.json"),
                        originalUri: vscode_1.Uri.parse("/package.json"),
                        renameUri: vscode_1.Uri.parse("/package.json"),
                        status: 5 /* Status.MODIFIED */,
                    },
                ],
            },
            {
                ref: "2",
                repoPath: "",
                changes: [
                    {
                        uri: vscode_1.Uri.parse("/src/enter.ts"),
                        originalUri: vscode_1.Uri.parse("/src/app.ts"),
                        renameUri: vscode_1.Uri.parse("/src/enter.ts"),
                        status: 3 /* Status.INDEX_RENAMED */,
                    },
                    {
                        uri: vscode_1.Uri.parse("/package.json"),
                        originalUri: vscode_1.Uri.parse("/package.json"),
                        renameUri: vscode_1.Uri.parse("/package.json"),
                        status: 5 /* Status.MODIFIED */,
                    },
                ],
            },
            {
                ref: "3",
                repoPath: "",
                changes: [
                    {
                        uri: vscode_1.Uri.parse("/assets/icons/logo.svg"),
                        originalUri: vscode_1.Uri.parse("/assets/icons/logo.svg"),
                        renameUri: vscode_1.Uri.parse("/assets/icons/logo.svg"),
                        status: 6 /* Status.DELETED */,
                    },
                    {
                        uri: vscode_1.Uri.parse("/index.ts"),
                        originalUri: vscode_1.Uri.parse("/index.ts"),
                        renameUri: vscode_1.Uri.parse("/index.ts"),
                        status: 5 /* Status.MODIFIED */,
                    },
                ],
            },
        ];
        const pathMap = (0, tree_1.getPathMap)(CHANGES_COLLECTION);
        (0, assert_1.equal)(pathMap["/src/app.ts"].changeStack.length, 2);
        (0, assert_1.equal)(pathMap["/src/app.ts"].changeStack[0].ref, "2");
        (0, assert_1.equal)(pathMap["/src/app.ts"].changeStack[0].change.uri.path, "/src/app.ts");
        (0, assert_1.equal)(pathMap["/src/app.ts"].changeStack[0].isDeletedByRename, true);
        (0, assert_1.equal)(pathMap["/src/app.ts"].changeStack[0].hidden, true);
        (0, assert_1.equal)(pathMap["/src/app.ts"].changeStack[1].ref, "1");
        (0, assert_1.equal)(pathMap["/src/app.ts"].changeStack[1].change.status, 5 /* Status.MODIFIED */);
        (0, assert_1.equal)(pathMap["/index.ts"].changeStack.length, 2);
        (0, assert_1.equal)(pathMap["/src/enter.ts"].changeStack.length, 1);
        (0, assert_1.equal)(pathMap["/src/enter.ts"].changeStack[0].ref, "2");
        (0, assert_1.equal)(pathMap["/src/enter.ts"].changeStack[0].change.status, 3 /* Status.INDEX_RENAMED */);
    });
});
suite("#getOriginalChangeStackAndUpdateChange()", () => {
    test("should assemble the original change stack chain when given multiple chainable change stacks", () => {
        const PATH_MAP = {
            "/assets/temp.svg": {
                type: tree_1.PathType.FILE,
                uri: vscode_1.Uri.parse(""),
                repoPath: "",
                changeStack: [
                    {
                        ref: "7",
                        change: {
                            uri: vscode_1.Uri.parse("/assets/temp.svg"),
                            originalUri: vscode_1.Uri.parse("/assets/enter.svg"),
                            renameUri: vscode_1.Uri.parse("/assets/temp.svg"),
                            status: 3 /* Status.INDEX_RENAMED */,
                        },
                    },
                    {
                        ref: "9",
                        change: {
                            uri: vscode_1.Uri.parse("/assets/temp.svg"),
                            originalUri: vscode_1.Uri.parse("/assets/temp.svg"),
                            renameUri: vscode_1.Uri.parse("/assets/temp.svg"),
                            status: 6 /* Status.DELETED */,
                        },
                        isDeletedByRename: true,
                        hidden: true,
                    },
                ],
            },
            "/assets/enter.svg": {
                type: tree_1.PathType.FILE,
                uri: vscode_1.Uri.parse("/assets/enter.svg"),
                repoPath: "",
                changeStack: [
                    {
                        ref: "3",
                        change: {
                            uri: vscode_1.Uri.parse("/assets/enter.svg"),
                            originalUri: vscode_1.Uri.parse("/assets/enter.svg"),
                            renameUri: vscode_1.Uri.parse("/assets/enter.svg"),
                            status: 6 /* Status.DELETED */,
                        },
                        isDeletedByRename: true,
                        hidden: true,
                    },
                ],
                originalChangeStack: [],
            },
        };
        const RENAMED_CHANGE_STACK = [
            {
                ref: "10",
                change: {
                    uri: vscode_1.Uri.parse("/assets/temp_renamed.svg"),
                    originalUri: vscode_1.Uri.parse("/assets/temp.svg"),
                    renameUri: vscode_1.Uri.parse("/assets/temp_renamed.svg"),
                    status: 3 /* Status.INDEX_RENAMED */,
                },
            },
            {
                ref: "15",
                change: {
                    uri: vscode_1.Uri.parse("/assets/temp_renamed.svg"),
                    originalUri: vscode_1.Uri.parse("/assets/temp_renamed.svg"),
                    renameUri: vscode_1.Uri.parse("/assets/temp_renamed.svg"),
                    status: 5 /* Status.MODIFIED */,
                },
            },
            {
                ref: "18",
                change: {
                    uri: vscode_1.Uri.parse("/assets/temp_renamed.svg"),
                    originalUri: vscode_1.Uri.parse("/assets/temp_renamed.svg"),
                    renameUri: vscode_1.Uri.parse("/assets/temp_renamed.svg"),
                    status: 5 /* Status.MODIFIED */,
                },
            },
        ];
        const originalChangeStack = (0, tree_1.getOriginalChangeStackAndUpdateChange)(PATH_MAP, RENAMED_CHANGE_STACK);
        (0, assert_1.equal)(originalChangeStack.length, 3);
        (0, assert_1.equal)(originalChangeStack[0].ref, "3");
        (0, assert_1.equal)(originalChangeStack[0].change.uri.path, "/assets/enter.svg");
        (0, assert_1.equal)(originalChangeStack[0].change.originalUri.path, "/assets/enter.svg");
        (0, assert_1.equal)(originalChangeStack[0].isDeletedByRename, true);
        (0, assert_1.equal)(originalChangeStack[0].hidden, true);
        (0, assert_1.equal)(originalChangeStack[1].ref, "7");
        (0, assert_1.equal)(originalChangeStack[1].change.uri.path, "/assets/temp.svg");
        (0, assert_1.equal)(originalChangeStack[1].change.originalUri.path, "/assets/enter.svg");
        (0, assert_1.equal)(originalChangeStack[1].isDeletedByRename, undefined);
        (0, assert_1.equal)(originalChangeStack[1].hidden, undefined);
        (0, assert_1.equal)(originalChangeStack[2].ref, "9");
        (0, assert_1.equal)(originalChangeStack[2].change.uri.path, "/assets/temp.svg");
        (0, assert_1.equal)(originalChangeStack[2].change.originalUri.path, "/assets/temp.svg");
        (0, assert_1.equal)(originalChangeStack[2].isDeletedByRename, true);
        (0, assert_1.equal)(originalChangeStack[2].hidden, true);
    });
});
//# sourceMappingURL=tree.test.js.map