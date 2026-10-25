const { app, BrowserWindow, nativeTheme } = require('electron');
const path = require('node:path');

const WINDOW_WIDTH = 800;
const WINDOW_HEIGHT = 600;

function createWindow() {
  nativeTheme.themeSource = 'dark';

  const window = new BrowserWindow({
    width: WINDOW_WIDTH,
    height: WINDOW_HEIGHT,
    show: !process.argv.includes('--hidden'),
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

  window.webContents.setWindowOpenHandler(() => ({ action: 'deny' }));
  window.webContents.on('will-navigate', (event) => event.preventDefault());
  window.webContents.session.setPermissionCheckHandler(() => false);
  window.webContents.session.setPermissionRequestHandler((_contents, _permission, callback) => callback(false));

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
