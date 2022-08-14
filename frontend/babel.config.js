module.exports = {
    presets: [
        '@vue/cli-plugin-babel/preset'
    ],
    plugins: [
        ["prismjs", {
            "languages": ["javascript", "css", "markup", "shell"],
            "plugins": ["line-numbers"],
            "theme": "coy",
            "css": true
        }]
    ]
}