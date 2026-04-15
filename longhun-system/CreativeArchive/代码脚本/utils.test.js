"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const assert_1 = require("assert");
const tree_1 = require("./changes/tree");
const utils_1 = require("./utils");
suite("Git utils", () => {
    test("should parse the output to config object", () => {
        (0, assert_1.deepStrictEqual)((0, utils_1.parseGitConfig)(`user.name=rabbit
user.email=MonsHuygens@moon.com`), {
            "user.name": "rabbit",
            "user.email": "MonsHuygens@moon.com",
        });
    });
    test("should parse the output to author list", () => {
        (0, assert_1.deepStrictEqual)((0, utils_1.parseGitAuthors)(`100	rabbit <MonsHuygens@moon.com>
50	elephant <MonsGanau@moon.com>
42	panda <MonsPico@moon.com>`), [
            {
                name: "rabbit",
                email: "MonsHuygens@moon.com",
            },
            {
                name: "elephant",
                email: "MonsGanau@moon.com",
            },
            {
                name: "panda",
                email: "MonsPico@moon.com",
            },
        ]);
    });
    test("should sort the given file nodes", () => {
        (0, assert_1.deepStrictEqual)((0, utils_1.compareFileTreeNode)([
            "utils",
            {
                type: tree_1.PathType.FOLDER,
            },
        ], [
            "utils",
            {
                type: tree_1.PathType.FILE,
            },
        ]), -1);
        (0, assert_1.deepStrictEqual)((0, utils_1.compareFileTreeNode)([
            "tests",
            {
                type: tree_1.PathType.FILE,
            },
        ], [
            "tests",
            {
                type: tree_1.PathType.FOLDER,
            },
        ]), 1);
        (0, assert_1.deepStrictEqual)((0, utils_1.compareFileTreeNode)([
            "state",
            {
                type: tree_1.PathType.FILE,
            },
        ], [
            "tsconfig.json",
            {
                type: tree_1.PathType.FILE,
            },
        ]), -1);
        (0, assert_1.deepStrictEqual)((0, utils_1.compareFileTreeNode)([
            ".gitignore",
            {
                type: tree_1.PathType.FILE,
            },
        ], [
            ".editorconfig",
            {
                type: tree_1.PathType.FILE,
            },
        ]), 1);
    });
    test("should convert to user info when given shortlog", () => {
        (0, assert_1.deepStrictEqual)((0, utils_1.getUser)("    65\tWolfgang Amadeus Mozart <mozart@mail.com>"), {
            name: "Wolfgang Amadeus Mozart",
            email: "mozart@mail.com",
        });
        (0, assert_1.deepStrictEqual)((0, utils_1.getUser)("3\tMichael Jackson <michael@mail.com>"), {
            name: "Michael Jackson",
            email: "michael@mail.com",
        });
        (0, assert_1.deepStrictEqual)((0, utils_1.getUser)("1\tanonymous <anonymous@mail.com>"), {
            name: "anonymous",
            email: "anonymous@mail.com",
        });
    });
});
//# sourceMappingURL=utils.test.js.map