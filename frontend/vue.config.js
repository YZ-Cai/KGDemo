module.exports = {
  transpileDependencies: [
    'vuetify'
  ],

  devServer: {
    proxy: {
      '/': {                              // 用于前端开发的接口请求抽象地址
        changeOrigin: true,               // 允许跨域
        target: 'http://localhost:5000/'  // 后端接收请求的地址
      },
    }
  }
}
