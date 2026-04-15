"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const worker_1 = require("threads/worker");
const commit_1 = require("./commit");
const gitWorker = {
    parseCommits: commit_1.parseCommits,
};
(0, worker_1.expose)(gitWorker);
//# sourceMappingURL=worker.js.map