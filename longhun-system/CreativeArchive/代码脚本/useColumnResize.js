"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.useColumnResize = void 0;
const react_1 = require("@use-gesture/react");
const react_2 = require("react");
function useColumnResize(columns, totalWidth = 0) {
    const sizes = (0, react_2.useMemo)(() => getSizes(columns, totalWidth), [columns, totalWidth]);
    const [dragStartSizes, setDragStartSizes] = (0, react_2.useState)(sizes);
    const [realtimeSizes, setRealTimeSizes] = (0, react_2.useState)(sizes);
    (0, react_2.useEffect)(() => {
        setRealTimeSizes(sizes);
    }, [sizes]);
    const dragBind = (0, react_1.useDrag)(({ type, movement: [mx], args: [index] }) => {
        if (type === "pointerdown") {
            setDragStartSizes(realtimeSizes);
            return;
        }
        const newSizes = [...dragStartSizes];
        newSizes[index] = newSizes[index] - mx;
        newSizes[index - 1] = newSizes[index - 1] + mx;
        const isExceedSize = newSizes[index] < columns[index].minWidth ||
            (columns[index].maxWidth && newSizes[index] > columns[index].maxWidth) ||
            newSizes[index - 1] < columns[index - 1].minWidth ||
            (columns[index - 1].maxWidth && newSizes[index - 1] > columns[index - 1].maxWidth);
        (!isExceedSize && setRealTimeSizes(newSizes));
    });
    return {
        columns: columns.map((column, index) => (Object.assign(Object.assign({}, column), { hasDivider: index !== 0, size: realtimeSizes[index], dragBind, minWidth: column.minWidth }))),
    };
}
exports.useColumnResize = useColumnResize;
function getSizes(columns, totalWidth) {
    let fillIndex = -1;
    const sizes = columns.map(({ width }, index) => {
        if (width === "fill") {
            fillIndex = index;
            return 0;
        }
        return width;
    });
    if (fillIndex !== -1) {
        sizes[fillIndex] = totalWidth - sum(sizes);
    }
    return sizes;
}
function sum(array) {
    return array.reduce((total, current) => total + current, 0);
}
//# sourceMappingURL=useColumnResize.js.map