<!--#龍芯⚡️2026-06-21-DOC-README-FILE2-v1.0-3 -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

# 龍魂桌面主开关

一键控制整个龍魂系统，无需记任何命令。

## 桌面入口

`~/Desktop/龍魂主开关.app`

点两下后会弹出菜单，选择要执行的操作即可。

## 如何新增菜单项

以后每次新增功能，不用再改 AppleScript，只要做以下其中一种：

### 方法一：编辑总注册表

修改 `desktop/menu-registry.json`，在 `items` 阵列中追加项目：

```json
{
  "id": "my-new-action",
  "label": "我的新功能",
  "type": "shell",
  "command": "cd {root} && python3 my_script.py",
  "description": "简短说明",
  "confirm": false
}
```

### 方法二：模块自带菜单（推荐）

在新增模块的根目录放一个 `desktop-menu.json`：

```json
{
  "items": [
    {
      "id": "module-action",
      "label": "运行我的模块",
      "type": "shell",
      "command": "cd {root} && bash my-module/run.sh",
      "description": "自动出现在主开关菜单",
      "confirm": false
    }
  ]
}
```

系统会自动扫描所有 `desktop-menu.json` 并合并进主菜单。

## 重新生成桌面菜单

新增或修改后，执行：

```bash
bash bin/build-desktop-switch.sh
```

或直接点击主开关里的 **🔄 重新生成主开关菜单**。

## 菜单项类型

- `shell`：执行 shell 命令（最常用）
- `open_url`：用浏览器打开网址
- `open_app`：用指定 App 打开路径
- `quit`：关闭菜单

命令中可用 `{root}` 占位符，会自动替换为项目根目录。
