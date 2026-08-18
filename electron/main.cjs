const { app, BrowserWindow, nativeTheme } = require('electron');
const path = require('node:path');

const WINDOW_WIDTH = 800;
const WINDOW_HEIGHT = 600;

function createWindow() {
  nativeTheme.themeSource = 'dark';

  const window = new BrowserWindow({
    width: WINDOW_WIDTH,
    height: WINDOW_HEIGHT,
    minWidth: 720,
    minHeight: 520,
    backgroundColor: '#0f1013',
    autoHideMenuBar: true,
    title: 'Typing Lab · 指法練習機',
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      preload: path.join(__dirname, 'preload.cjs')
    }
  });

  window.loadFile(path.join(__dirname, '..', 'index.html'));
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
