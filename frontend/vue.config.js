module.exports = {
  // Should be STATIC_URL + path/to/build
  // publicPath: '/static/src/vue/dist/',

  // // Output to a directory in STATICFILES_DIRS
  // outputDir: path.resolve(__dirname, '../api/static/src/vue/dist/'),

  // filenameHashing: false,
  // runtimeCompiler: true,

  // devServer: {
  //   writeToDisk: true, // Write files to disk in dev mode, so Django can serve the assets
  // },
  pluginOptions: {
    quasar: {
      importStrategy: 'kebab',
      rtlSupport: false
    }
  },
  transpileDependencies: [
    'quasar'
  ]
}
