const path = require('path');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = (argv) => {
    const isWatch = argv.WEBPACK_WATCH;
    const plugins = [];
    if (isWatch) {
        plugins.push(new BundleAnalyzerPlugin({
            openAnalyzer: false,
            analyzerMode: 'static'
        }));
    }

    return {
        entry: './src/plugin.ts',
        mode: isWatch ? 'development' : 'production',
        module: {
            exprContextCritical: false,
            rules: [
                {
                    test: /\.ts$/,
                    use: 'ts-loader',
                    exclude: /node_modules/,
                }
            ]
        },
        optimization: {
            usedExports: true,
        },
        externals: {
            "codearts": "commonjs codearts",
            "@codearts/plugin": "commonjs @codearts/plugin",
        },
        resolve: {
            extensions: ['.ts', '.js']
        },
        output: {
            path: path.resolve(__dirname, 'dist'),
            filename: 'plugin.js',
            libraryTarget: 'commonjs2',
            devtoolModuleFilenameTemplate: '../[resource-path]',
            clean: true
        },
        target: 'node',
        devtool: isWatch ? 'source-map' : 'nosources-source-map',
        plugins
    };
};