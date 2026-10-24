# SEC-P2-20261025：typing-lab

日期：2026-10-25。基準：05e4af4455ea2d1cc90b0337d3bfd1565f958049（main）。

狀態：隔離修補已備妥，待整合。未推送／合併／部署；原始工作目錄保留。

Electron37更新已驗證44.9.3，新增package-lock；本地CSP、拒絕外部導航／新視窗及權限要求，保留sandbox與contextIsolation。

- 真實隱藏Electron44.9.3：30次鍵盤輸入、注音切換、設定操作
- CSP遠端fetch／新視窗／導航拒絕，無Node暴露
- 20暖鍵盤roundtrip p95<100ms；npm audit0；原生Python版未更動

npm公告：{"info":0,"low":0,"moderate":0,"high":0,"critical":0,"total":0}。
Python公告：不適用／未做Python解析。



效能：{"result":"not_applicable","reason":"Only CI source/pins changed or separately recorded runtime fixture metric; no production performance claim"}。

範圍與成本：只跑本機及合成fixture，不啟用付費API或遠端CI。沒有完整正式安全或發布驗收；未評項目not_scored。

- 原始工作目錄、未提交修改與分支全部保留；本報告僅適用此隔離分支。
- 完整history／秘密輪替／正式服務與二進位鑑識不在此輪驗收，未評項目not_scored。

Task契約：輸入為固定基準及既有測試；交付為獨立修補分支、manifest/lockfile或來源修補與此去敏證據；無跨專案依賴。驗收是原生工具成功、已知發現逐項處置、適當真實回歸及影響範圍效能門檻；未完成項目明記，不以fixture代表正式環境。
