var path = require("path");
module.exports = {
    configureWebpack: {
        resolve: {
            alias: {
                src: path.resolve(__dirname, "src"),
            },
        },
    },
    devServer: {
        host: "localhost",
    },
};
