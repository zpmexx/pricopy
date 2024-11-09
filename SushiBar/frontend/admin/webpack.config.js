const path = require('path')
const webpack = require('webpack')

module.exports = {
  plugins: [
    new webpack.HotModuleReplacementPlugin()
  ],
  entry: path.resolve(__dirname, 'src', 'index.js'),
  output: {
    path: path.resolve(__dirname, 'static'),
    //publicPath: "\\"+path.resolve(__dirname, 'static')+"\\",
    publicPath: "\\static\\",
    filename: 'bundle.js'
  },
  devServer: {
    contentBase: path.resolve(__dirname, 'static'),
    open: true,
    clientLogLevel: 'silent',
    port: 9000,
    hot: true
  },
  module: {
    rules: [
      {
        test: /\.(jsx|js)$/,
        include: path.resolve(__dirname, 'src'),
        exclude: /node_modules/,
        use: [{
          loader: 'babel-loader',
          options: {
            presets: [
              ['@babel/preset-env', {
                "targets": "defaults" 
              }],
              '@babel/preset-react'
            ],
			"plugins": [
				'@babel/plugin-proposal-class-properties',
				'@babel/plugin-transform-runtime'
			],
          }
        }]
      },
	  {
        test: /\.css$/i,
        use: ["style-loader", "css-loader"],
      },
    ]
  },
  resolve: {
        alias: {
            'react-redux': path.join(__dirname, '/node_modules/react-redux/dist/react-redux.min')
        }
  }
}