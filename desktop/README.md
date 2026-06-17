# 龍魂桌面主开关

一鍵控制整個龍魂系統，無需記任何命令。

## 桌面入口

`~/Desktop/龍魂主开关.app`

點兩下後會彈出菜單，選擇要執行的操作即可。

## 如何新增菜單項

以後每次新增功能，不用再改 AppleScript，只要做以下其中一種：

### 方法一：編輯總註冊表

修改 `desktop/menu-registry.json`，在 `items` 陣列中追加項目：

```json
{
  "id": "my-new-action",
  "label": "我的新功能",
  "type": "shell",
  "command": "cd {root} && python3 my_script.py",
  "description": "簡短說明",
  "confirm": false
}
```

### 方法二：模塊自帶菜單（推薦）

在新增模塊的根目錄放一個 `desktop-menu.json`：

```json
{
  "items": [
    {
      "id": "module-action",
      "label": "運行我的模塊",
      "type": "shell",
      "command": "cd {root} && bash my-module/run.sh",
      "description": "自動出現在主开关菜單",
      "confirm": false
    }
  ]
}
```

系統會自動掃描所有 `desktop-menu.json` 並合併進主菜單。

## 重新生成桌面菜單

新增或修改後，執行：

```bash
bash bin/build-desktop-switch.sh
```

或直接點擊主开关裡的 **🔄 重新生成主开关菜單**。

## 菜單項類型

- `shell`：執行 shell 命令（最常用）
- `open_url`：用瀏覽器打開網址
- `open_app`：用指定 App 打開路徑
- `quit`：關閉菜單

命令中可用 `{root}` 占位符，會自動替換為項目根目錄。
