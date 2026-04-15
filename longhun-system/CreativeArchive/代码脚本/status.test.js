"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const assert_1 = require("assert");
const vscode_1 = require("vscode");
const status_1 = require("./status");
suite("#getFileExistStatus()", () => {
    test("should return { isExistBefore: false, isExistAfter: true } when given added status", () => {
        (0, assert_1.deepEqual)((0, status_1.getFileExistStatus)(1 /* Status.INDEX_ADDED */), {
            isExistBefore: false,
            isExistAfter: true,
        });
    });
    test("should return { isExistBefore: false, isExistAfter: true } when given renamed status", () => {
        (0, assert_1.deepEqual)((0, status_1.getFileExistStatus)(3 /* Status.INDEX_RENAMED */), {
            isExistBefore: false,
            isExistAfter: true,
        });
    });
    test("should return { isExistBefore: true, isExistAfter: false } when given deleted status", () => {
        (0, assert_1.deepEqual)((0, status_1.getFileExistStatus)(6 /* Status.DELETED */), {
            isExistBefore: true,
            isExistAfter: false,
        });
    });
    test("should return { isExistBefore: true, isExistAfter: true } when given modified status", () => {
        (0, assert_1.deepEqual)((0, status_1.getFileExistStatus)(5 /* Status.MODIFIED */), {
            isExistBefore: true,
            isExistAfter: true,
        });
    });
    test("should return undefined when given other status", () => {
        (0, assert_1.deepEqual)((0, status_1.getFileExistStatus)(8 /* Status.IGNORED */), undefined);
    });
});
suite("#mergeStatus()", () => {
    const dummyUri = vscode_1.Uri.parse("");
    test("should merge the status as undefined when added at first and deleted at last", () => {
        const CHANGE_STACK = [
            {
                ref: "",
                change: {
                    uri: dummyUri,
                    originalUri: dummyUri,
                    renameUri: dummyUri,
                    status: 1 /* Status.INDEX_ADDED */,
                },
            },
            {
                ref: "",
                change: {
                    uri: dummyUri,
                    originalUri: dummyUri,
                    renameUri: dummyUri,
                    status: 5 /* Status.MODIFIED */,
                },
            },
            {
                ref: "",
                change: {
                    uri: dummyUri,
                    originalUri: dummyUri,
                    renameUri: dummyUri,
                    status: 6 /* Status.DELETED */,
                },
                isDeletedByRename: false,
            },
        ];
        (0, assert_1.equal)((0, status_1.mergeStatus)(CHANGE_STACK[0], CHANGE_STACK[2]), undefined);
    });
    test("should merge the status as deleted when deleted at last", () => {
        const CHANGE_STACK = [
            {
                ref: "",
                change: {
                    uri: dummyUri,
                    originalUri: dummyUri,
                    renameUri: dummyUri,
                    status: 5 /* Status.MODIFIED */,
                },
            },
            {
                ref: "",
                change: {
                    uri: dummyUri,
                    originalUri: dummyUri,
                    renameUri: dummyUri,
                    status: 6 /* Status.DELETED */,
                },
            },
        ];
        (0, assert_1.equal)((0, status_1.mergeStatus)(CHANGE_STACK[0], CHANGE_STACK[1]), 6 /* Status.DELETED */);
    });
    test("should merge the status as added when added at first", () => {
        const CHANGE_STACK = [
            {
                ref: "",
                change: {
                    uri: dummyUri,
                    originalUri: dummyUri,
                    renameUri: dummyUri,
                    status: 1 /* Status.INDEX_ADDED */,
                },
            },
            {
                ref: "",
                change: {
                    uri: dummyUri,
                    originalUri: dummyUri,
                    renameUri: dummyUri,
                    status: 5 /* Status.MODIFIED */,
                },
            },
        ];
        (0, assert_1.equal)((0, status_1.mergeStatus)(CHANGE_STACK[0], CHANGE_STACK[1]), 1 /* Status.INDEX_ADDED */);
    });
    test("should merge the status as modified when just modified", () => {
        const CHANGE_STACK = [
            {
                ref: "",
                change: {
                    uri: dummyUri,
                    originalUri: dummyUri,
                    renameUri: dummyUri,
                    status: 5 /* Status.MODIFIED */,
                },
            },
            {
                ref: "",
                change: {
                    uri: dummyUri,
                    originalUri: dummyUri,
                    renameUri: dummyUri,
                    status: 5 /* Status.MODIFIED */,
                },
            },
        ];
        (0, assert_1.equal)((0, status_1.mergeStatus)(CHANGE_STACK[0], CHANGE_STACK[1]), 5 /* Status.MODIFIED */);
    });
    test("should merge the status as deleted when deleted by rename at last", () => {
        const CHANGE_STACK = [
            {
                ref: "",
                change: {
                    uri: dummyUri,
                    originalUri: dummyUri,
                    renameUri: dummyUri,
                    status: 5 /* Status.MODIFIED */,
                },
            },
            {
                ref: "",
                change: {
                    uri: dummyUri,
                    originalUri: dummyUri,
                    renameUri: dummyUri,
                    status: 6 /* Status.DELETED */,
                },
                isDeletedByRename: true,
                hidden: true,
            },
        ];
        (0, assert_1.equal)((0, status_1.mergeStatus)(CHANGE_STACK[0], CHANGE_STACK[1]), undefined);
    });
    test("should merge the status as deleted when deleted by rename at last but show", () => {
        const CHANGE_STACK = [
            {
                ref: "",
                change: {
                    uri: dummyUri,
                    originalUri: dummyUri,
                    renameUri: dummyUri,
                    status: 5 /* Status.MODIFIED */,
                },
                isDeletedByRename: false,
            },
            {
                ref: "",
                change: {
                    uri: dummyUri,
                    originalUri: dummyUri,
                    renameUri: dummyUri,
                    status: 6 /* Status.DELETED */,
                },
                isDeletedByRename: true,
                hidden: false,
            },
        ];
        (0, assert_1.equal)((0, status_1.mergeStatus)(CHANGE_STACK[0], CHANGE_STACK[1]), 6 /* Status.DELETED */);
    });
});
//# sourceMappingURL=status.test.js.map