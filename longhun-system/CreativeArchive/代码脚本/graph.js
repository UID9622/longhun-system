"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.GitGraph = void 0;
const inversify_1 = require("inversify");
let GitGraph = class GitGraph {
    constructor() {
        this.batchedCommitsCollection = [];
        this.postIndex = 0;
        this.colorPicker = getColorPicker();
        /** record chains cross current commit */
        this.hashChains = [];
        this.colorChains = [];
        /**  */
        this.curLines = [];
        /**  */
        this.curParents = [];
    }
    registerHandler(postHandler, batchNumber) {
        this.clear(batchNumber);
        this.postHandler = postHandler;
    }
    attachGraphAndPost(batchedCommits) {
        var _a, _b, _c, _d;
        const { batchNumber, initializing } = batchedCommits;
        this.batchedCommitsCollection[batchNumber] = batchedCommits;
        while (this.currentBatchedCommits) {
            const { batchNumber, totalCount, options } = this.currentBatchedCommits;
            const graphicCommits = this.setGraphToCommits(this.currentBatchedCommits.commits, !(options.authors || options.keyword));
            (_a = this.postHandler) === null || _a === void 0 ? void 0 : _a.call(this, [
                totalCount,
                initializing ? 0 : batchNumber,
                (_b = options.ref) !== null && _b !== void 0 ? _b : '',
                JSON.stringify(options.authors),
                (_c = options.keyword) !== null && _c !== void 0 ? _c : '',
                (_d = options.maxLength) !== null && _d !== void 0 ? _d : 0,
                options.repo,
                ...graphicCommits,
            ]);
            this.postIndex++;
        }
    }
    clear(batchNumber) {
        this.postIndex = batchNumber;
        this.batchedCommitsCollection = [];
        this.hashChains = [];
        this.colorChains = [];
        this.curParents = [];
        this.curLines = [];
        this.colorPicker.reset();
    }
    get currentBatchedCommits() {
        return this.batchedCommitsCollection[this.postIndex];
    }
    setGraphToCommits(commits, setGraph = true) {
        return commits.map(([hash, parents, commitData]) => `${commitData}${setGraph ? this.getGraphSlice(hash, parents) : this.getSingleLineGraphSlice(hash, parents)}`);
    }
    getSingleLineGraphSlice(hash, parents) {
        const commitColor = '#06A77D';
        const lines = [];
        if (this.curParents.includes(hash)) {
            lines.push(-2, -1, commitColor);
        }
        this.curParents = [...parents];
        return `0\n${commitColor}\n${JSON.stringify(lines)}`;
    }
    getGraphSlice(hash, parents) {
        const lines = [...this.curLines];
        const [firstParent, ...forkParents] = parents;
        let commitPosition;
        let commitColor;
        const firstIndex = this.hashChains.indexOf(hash);
        if (firstIndex !== -1) {
            // not first node of a chain
            const otherIndexes = this.getAllIndexes(this.hashChains, hash, firstIndex);
            commitPosition = firstIndex;
            commitColor = this.colorChains[firstIndex];
            this.hashChains[firstIndex] = firstParent;
            const mergedIndexes = firstParent ? otherIndexes : [firstIndex, ...otherIndexes];
            if (mergedIndexes.length) {
                // remove merged chains
                // TODO: iterate into #getAllIndexes
                this.updateChainsByMergedIndexes(this.hashChains, this.colorChains, mergedIndexes);
                this.collapseMergedLines(lines, this.curLines, mergedIndexes);
            }
        }
        else {
            commitColor = this.colorPicker.get();
            commitPosition = this.hashChains.length;
            if (firstParent) {
                this.hashChains.push(firstParent);
                this.colorChains.push(commitColor);
            }
            // first node of a chain
            const bottom = firstParent ? this.hashChains.length - 1 : -1;
            lines.push(-1, bottom, commitColor);
            this.curLines.push(bottom, bottom, commitColor);
        }
        // handle multiple parents of the node
        forkParents.forEach((parent) => {
            const firstParentIndex = this.hashChains.indexOf(parent);
            if (firstParentIndex !== -1) {
                // flow into the existed chain
                const color = this.colorChains[firstParentIndex];
                if (firstParentIndex !== undefined) {
                    lines.push(-1, firstParentIndex, color);
                }
            }
            else {
                // new chain
                commitColor = this.colorPicker.get();
                this.hashChains.push(parent);
                this.colorChains.push(commitColor);
                const bottom = this.hashChains.length - 1;
                lines.push(-1, bottom, commitColor);
                this.curLines.push(bottom, bottom, commitColor);
            }
        });
        return `${commitPosition}\n${commitColor}\n${JSON.stringify(lines)}`;
    }
    getAllIndexes(list, hash, start = -1) {
        const indexes = [];
        let i = start;
        while ((i = list.indexOf(hash, i + 1)) !== -1) {
            indexes.push(i);
        }
        return indexes;
    }
    updateChainsByMergedIndexes(hashChains, colorChains, indexes) {
        for (var i = indexes.length - 1; i >= 0; i--) {
            hashChains.splice(indexes[i], 1);
            colorChains.splice(indexes[i], 1);
        }
    }
    collapseMergedLines(lines, nextInitialLines, mergedIndexList) {
        const firstMergedIndex = mergedIndexList[0];
        let collapsedCount = 0;
        for (let i = firstMergedIndex * 3; i < lines.length; i += 3) {
            if (mergedIndexList.includes(i / 3)) {
                // line bottom = -1
                lines[i + 1] = -1;
                nextInitialLines.splice(i - collapsedCount * 3, 3);
                collapsedCount++;
            }
            else {
                // line bottom sub collapsed count
                const lineBottomIndex = i + 1;
                const bottom = lines[lineBottomIndex] - collapsedCount;
                lines[lineBottomIndex] = bottom;
                const nextInitialLineTopIndex = i - collapsedCount * 3;
                const nextInitialLineBottomIndex = nextInitialLineTopIndex + 1;
                nextInitialLines[nextInitialLineTopIndex] = bottom;
                nextInitialLines[nextInitialLineBottomIndex] = bottom;
            }
        }
    }
};
GitGraph = __decorate([
    (0, inversify_1.injectable)()
], GitGraph);
exports.GitGraph = GitGraph;
function getColorPicker() {
    let index = -1;
    const colors = [
        "#06A77D",
        "#C62E65",
        "#005377",
        "#D5C67A",
        "#F1A208",
        "#D36135",
        "#D63AF9",
    ];
    return {
        get() {
            if (index >= colors.length - 1) {
                index = 0;
            }
            else {
                index++;
            }
            return colors[index];
        },
        reset() {
            index = -1;
        },
    };
}
//# sourceMappingURL=graph.js.map