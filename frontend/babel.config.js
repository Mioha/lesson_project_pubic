module.exports = {
  presets: [
    ['@babel/preset-env', { modules: false }]
  ],
  env: {
    test: {
      presets: [
        ['@babel/preset-env', { targets: { node: 'current' } }]
      ]
    }
  },
  // for fixing error of async await
  plugins: ['@babel/plugin-transform-runtime']
}
