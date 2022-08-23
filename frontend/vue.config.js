const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
    transpileDependencies: true,
    configureWebpack: {
        plugins: [
            require('unplugin-vue-components/webpack')({ /* options */ }),
            require('unplugin-element-plus/webpack')({
                // options
            }),
            require('unplugin-auto-import/webpack')({ /* options */ }),
        ],
    },
    devServer: {
        proxy: 'http://127.0.0.1:5000',
    },
})