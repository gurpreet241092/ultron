'use strict';
const app = require('app');
const BrowserWindow = require('browser-window');

// report crashes to the Electron project
require('crash-reporter').start();

// adds debug features like hotkeys for triggering dev tools and reload
// require('electron-debug')();

// prevent window being garbage collected
let mainWindow;

function onClosed() {
	// dereference the window
	// for multiple windows store them in an array
	mainWindow = null;
}

function createMainWindow() {
	const win = new BrowserWindow({
		width: 600,
		height: 400
	});
	win.setTitle('ULTRON');
	win.loadUrl(`file://${__dirname}/dist/index.html`);
	win.on('closed', onClosed);

	return win;
}

app.on('window-all-closed', function(){
	if (process.platform !== 'darwin') {
		app.quit();
	}
});

app.on('activate-with-no-open-windows', function(){
	if (!mainWindow) {
		mainWindow = createMainWindow();
	}
});

app.on('ready', function(){
	mainWindow = createMainWindow();
});
