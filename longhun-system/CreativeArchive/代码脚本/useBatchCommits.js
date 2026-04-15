"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.useBatchCommits = void 0;
const react_1 = require("react");
function useBatchCommits([headerRef, scrollContainerRef], [hideProgressBar, setDescription]) {
    const [commits, _setCommits] = (0, react_1.useState)([]);
    const loadingRef = (0, react_1.useRef)(false);
    const hasMoreCommitsRef = (0, react_1.useRef)(true);
    const commitsRef = (0, react_1.useRef)(commits);
    const optionRef = (0, react_1.useRef)({});
    const [commitsCount, setCommitsCount] = (0, react_1.useState)(0);
    const setCommits = (0, react_1.useCallback)((commits) => {
        commitsRef.current = commits;
        _setCommits(commits);
    }, []);
    const setBatchedCommits = (0, react_1.useCallback)((batchedCommits) => {
        var _a, _b;
        const [totalCount, batchNumber, ref, stringifiedAuthors, keyword, maxLength, repo, ...commits] = batchedCommits;
        setCommitsCount(totalCount);
        Object.assign(optionRef.current, { repo, ref, authors: JSON.parse(stringifiedAuthors), keyword, maxLength });
        loadingRef.current = false;
        hasMoreCommitsRef.current = true;
        hideProgressBar();
        if (commits.length === 0) {
            hasMoreCommitsRef.current = false;
        }
        setCommits(batchNumber === 0 ? commits : commitsRef.current.concat(commits));
        if (batchNumber === 0) {
            (_a = headerRef.current) === null || _a === void 0 ? void 0 : _a.scrollTo(0, 0);
            (_b = scrollContainerRef.current) === null || _b === void 0 ? void 0 : _b.scrollTo(0, 0);
            setDescription(commits.length);
        }
        else {
            setDescription(commitsRef.current.length);
        }
    }, [headerRef, scrollContainerRef, hideProgressBar, setCommits, setDescription]);
    return { commits, commitsCount, optionRef, setBatchedCommits, loadingRef, hasMoreCommitsRef };
}
exports.useBatchCommits = useBatchCommits;
//# sourceMappingURL=useBatchCommits.js.map