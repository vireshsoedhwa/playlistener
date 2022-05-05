const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');
const BrowserSyncPlugin = require('browser-sync-webpack-plugin');

module.exports = merge(common, {
    mode: 'development',
    devtool: 'inline-source-map',
    //   devServer: {
    //     contentBase: './dist',
    //   },
    plugins: [
        // new BrowserSyncPlugin({
        //     // browse to http://localhost:3000/ during development,
        //     // ./public directory is being served
        //     host: 'localhost',
        //     port: 9000,
        //     proxy: 'http://localhost:8000/',
        // },
            // // plugin options
            // {
            //     // prevent BrowserSync from reloading the page
            //     // and let Webpack Dev Server take care of this
            //     injectCss: true,
            //     reload: false
            // }
        )
    ]

});
