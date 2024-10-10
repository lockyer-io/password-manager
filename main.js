const {app, BrowserWindow} = require('electron');
const url = require('url');
const path =require('path');

function createMainWindow() {

    const createMainWindow = new BrowserWindow({
        title: 'Password Manager',
        width: 1000,
        height: 600
    });

    const startUrl = url.format({
        pathname: path.join(__dirname, 'index.html'),
        protocol: 'file',
    });
    createMainWindow.loadURL(startUrl);
}


app.whenReady().then(createMainWindow);