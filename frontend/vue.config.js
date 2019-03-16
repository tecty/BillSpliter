module.exports = {
  assetsDir: "static",

  devServer: {
    proxy: "http://localhost:8000/"
  },

  chainWebpack: config => {
    config.module
      .rule("eslint")
      .use("eslint-loader")
      .options({
        fix: true
      });
  },

  pwa: {
    themeColor: '#2196F3'
  }
};
