// explicitly creating a dev proxy in order to turn on changeOrigin
// this is required for tusd to work in dev


const { createProxyMiddleware } = require('http-proxy-middleware');



module.exports = function (app) {
	app.use(
		'/',
		createProxyMiddleware({
			target: 'http://localhost:80/',
			changeOrigin: true,
		}));
}