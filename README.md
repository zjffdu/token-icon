# token-icon

一个 macOS 菜单栏小工具，用来显示 token 配额信息，并支持在设置窗口里配置 `token_key` 和刷新间隔。

## 功能

- 菜单栏显示剩余额度（`Remaining`）
- 菜单显示今日消耗和新增额度
- 支持手动刷新（`Refresh Now`）
- 支持在同一个设置窗口配置：
  - `token_key`
  - `refresh_interval`（10 到 3600 秒）

## 运行环境

- macOS（基于 `rumps` 菜单栏应用）
- Python 3.11+
- `uv`

## 安装依赖

```bash
uv sync
```

## 开发模式启动

```bash
uv run python app.py
```

启动后会在菜单栏看到应用图标标题（例如 `𝗧 —`）。

## 构建 macOS Application

执行一键构建脚本：

```bash
./scripts/build_macos_app.sh
```

这个脚本会先把 `assets/icon-token-orbit-a-1024.png` 转成
`assets/icon-token-orbit-a.icns`，再进行 PyInstaller 打包。

构建完成后，应用在：

```text
dist/Token Icon.app
```

你可以直接双击 `dist/Token Icon.app` 启动，不需要再执行 `uv run python app.py`。

## 发布建议

如果要分发给其他机器，建议额外处理：

- 代码签名（code signing）
- 公证（notarization）

否则在其他 macOS 上可能会被 Gatekeeper 拦截。

## 使用说明

1. 点击菜单栏图标。
2. 点击 `Settings...`。
3. 在同一个窗口填写：
   - `Token Key`
   - `Refresh interval (10-3600)`
4. 点击 `Save` 保存配置。
5. 应用会按新的刷新间隔重新拉取数据。

## 配置文件位置

配置保存到：

```text
~/.config/token-icon/config.json
```

示例：

```json
{
  "token_key": "your-token-key",
  "refresh_interval": 60
}
```

## 常用命令

```bash
uv sync                  # 安装依赖
uv run python app.py     # 运行应用
./scripts/build_macos_app.sh  # 构建 .app
pkill -f "app.py"        # 结束运行中的进程
```

## 代码结构

- `app.py`：菜单栏主应用、定时刷新、菜单交互
- `settings_window.py`：设置窗口逻辑（单窗口配置 token 和 interval）
- `api.py`：请求 token 统计接口
- `config.py`：配置读写（`~/.config/token-icon/config.json`）
- `tests/test_settings_window.py`：设置窗口相关测试
- `packaging_config.py`：打包配置（Bundle 元数据、hidden imports）
- `scripts/build_macos_app.py`：PyInstaller 构建入口
- `scripts/build_macos_app.sh`：一键构建脚本
- `scripts/make_icns_from_png.py`：将 PNG 图标转换为 `.icns`

## 测试

```bash
uv run python -m unittest tests/test_settings_window.py tests/test_packaging_config.py
```

## 说明

- 远程接口地址在 `api.py` 中固定为：`https://his.ppchat.vip/api/token-stats`
- 若 `token_key` 未配置，标题会保持 `𝗧 —`
