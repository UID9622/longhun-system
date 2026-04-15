"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const assert_1 = require("assert");
const changes_1 = require("./changes");
suite("#parseGitChanges()", () => {
    test("should parse git output to changes", () => {
        const GIT_OUTPUT = "D\x00babel.config.js\x00M\x00package-lock.json\x00A\x00package.json\x00";
        const changes = (0, changes_1.parseGitChanges)("/project", GIT_OUTPUT);
        (0, assert_1.equal)(changes.length, 3);
        (0, assert_1.equal)(changes[0].status, 6 /* Status.DELETED */);
        (0, assert_1.equal)(changes[0].uri.path, "/project/babel.config.js");
        (0, assert_1.equal)(changes[1].status, 5 /* Status.MODIFIED */);
        (0, assert_1.equal)(changes[1].uri.path, "/project/package-lock.json");
        (0, assert_1.equal)(changes[2].status, 1 /* Status.INDEX_ADDED */);
        (0, assert_1.equal)(changes[2].uri.path, "/project/package.json");
    });
    test("should parse git output to empty array when given nothing", () => {
        const GIT_OUTPUT = "";
        const changes = (0, changes_1.parseGitChanges)("", GIT_OUTPUT);
        (0, assert_1.equal)(changes.length, 0);
    });
});
//# sourceMappingURL=changes.test.js.map