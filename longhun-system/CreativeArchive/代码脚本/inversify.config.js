"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.initializeContainer = exports.container = void 0;
require("reflect-metadata");
const inversify_1 = require("inversify");
const service_1 = require("../git/service");
const graph_1 = require("../git/graph");
const ChangeTreeDataProvider_1 = require("../views/changes/ChangeTreeDataProvider");
const source_1 = require("../views/common/data/source");
const disposables_1 = require("../disposables");
const GitStatusFileDecorationProvider_1 = require("../views/changes/GitStatusFileDecorationProvider");
const HistoryViewProvider_1 = require("../views/history/HistoryViewProvider");
const ChangeTreeView_1 = require("../views/changes/ChangeTreeView");
const DetailViewProvider_1 = require("../views/detail/DetailViewProvider");
const types_1 = require("./types");
const container = new inversify_1.Container();
exports.container = container;
function initializeContainer(context) {
    container
        .bind(types_1.TYPES.ExtensionContext)
        .toConstantValue(context);
    container.bind(source_1.Source).toSelf().inSingletonScope();
    container.bind(service_1.GitService).toSelf().inSingletonScope();
    container.bind(graph_1.GitGraph).toSelf().inSingletonScope();
    container
        .bind(HistoryViewProvider_1.HistoryWebviewViewProvider)
        .toSelf()
        .inSingletonScope();
    container
        .bind(ChangeTreeDataProvider_1.ChangeTreeDataProvider)
        .toSelf()
        .inSingletonScope();
    container.bind(ChangeTreeView_1.ChangeTreeView).toSelf().inSingletonScope();
    container
        .bind(GitStatusFileDecorationProvider_1.GitStatusFileDecorationProvider)
        .toSelf()
        .inSingletonScope();
    container
        .bind(DetailViewProvider_1.DetailViewProvider)
        .toSelf()
        .inSingletonScope();
    container
        .bind(disposables_1.DisposableController)
        .toSelf()
        .inSingletonScope();
}
exports.initializeContainer = initializeContainer;
//# sourceMappingURL=inversify.config.js.map