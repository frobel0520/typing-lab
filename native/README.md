# Typing Lab 原生桌面版

這個資料夾是實際的 Windows 桌面應用程式，不是瀏覽器頁面。

## 直接啟動

若電腦已安裝 Python 3.12，直接雙擊 `TypingLab.pyw`。它會開啟獨立的 800×600 原生視窗，不會開瀏覽器。

也可以在 PowerShell 執行：

```powershell
py -3.12 native/TypingLab.pyw
```

## 目前功能

- 英文 QWERTY 與注音大千鍵位練習
- 中文模式顯示目標中文字句，只驗證注音鍵位序列
- 11,282 個不重複英文練習項目（含 10,000 個依頻率排序的英文單字）與 1,259 句繁體中文本機字庫；每輪洗牌後用完才重抽，避免固定詞彙反覆連續出現
- 無限補充練習內容
- 不計時、不顯示正確率、不設完成畫面
- 錯誤輸入不前進，也不累計錯誤字數
- 英文與中文分開保存累計字數與每日練習字數，右側熱點圖會隨目前模式切換
- 目前按鍵、手指、左右手與虛擬鍵盤提示
- 虛擬鍵盤只顯示按鍵，不在鍵帽上顯示指法文字
- 本機保存模式與鍵帽指法設定

中文模式請先切換至 ENG 英文鍵盤。一聲的 Space 是聲調鍵；二、三、四聲與輕聲則按各自的聲調鍵，按完即完成，不再追加 Space。例如 `ㄍㄨㄥ` 是 `E`、`J`、`/`、`Space`。不需要選字，也不需要 Enter。

英文擴充字庫採用 Google 10,000 English USA no-swears 詞表，並以 COCA 詞頻樣本補足可輸入的字母詞；中文資料則由臺灣 TOCFL/TBCL 詞表與教育部字典注音欄位整理而成。資料已內嵌於 `bank_data.py`，啟動時不需要網路。

## 打包成 exe

若環境有 PyInstaller，可以從專案根目錄執行：

```powershell
py -3.12 -m PyInstaller --noconfirm --clean native/TypingLab.spec
```

輸出會在 `dist/TypingLab.exe`。本次環境已確認有 Python 3.12、Tkinter 與 PyInstaller。
