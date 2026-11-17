# Helix master 自动构建

[![Build Helix master](https://github.com/wjilei/helix-nightly-builds/actions/workflows/build.yml/badge.svg)](https://github.com/wjilei/helix-nightly-builds/actions/workflows/build.yml)

为 [helix-editor/helix](https://github.com/helix-editor/helix) 的 `master` 提供**非官方**构建。不修改上游源代码，不代表 Helix 官方。

## 下载与安装

打开 [Releases](https://github.com/wjilei/helix-nightly-builds/releases)，选择最新成功发布的预发布版本：

| 平台 | 下载文件 | 安装 |
| --- | --- | --- |
| Windows x64 | `helix-windows-x64.zip` | 完整解压，运行 `helix/hx.exe`；可将所在文件夹加入用户 PATH |
| Linux x64（Debian / Ubuntu） | `helix-linux-x64.deb` | `sudo apt install ./helix-linux-x64.deb` |

Windows 的 `hx.exe` 和 `runtime` 必须保留在同一目录。两种包均包含匹配的 runtime、主题、查询文件和已编译 tree-sitter 语法解析器。**语言服务器需要另外安装。**

验证：

```sh
hx --version
hx --health
```

Linux 构建环境为 Ubuntu 22.04 x64，兼容性以包内声明的依赖及实际系统为准，不支持所有 Linux 发行版。DEB 包名为 `helix`，与发行版提供的同名包互相替换；安装前请确认。自定义配置不会被打包覆盖。

## 自动更新

- 每周一北京时间 **10:23**（UTC 02:23）检查上游 `master`。
- 与最近成功发布的源码提交相同，则跳过；上次失败的构建会在下次重试。
- 修改工作流或构建脚本推送到 `main`，会自动构建。
- 两个平台编译及安装包冒烟检查全部通过后，才发布新的预发布版本。旧版保留，不会因构建失败被覆盖。
- 使用 GitHub 标准托管运行器，公开仓库正常使用免费；无需服务器、付费运行器或额外令牌。
- Actions 中转产物只保存 7 天；正式下载文件保存在 Releases。

手动触发：进入 **Actions → Build Helix master → Run workflow**。勾选 `force` 可强制重新构建。

```sh
gh workflow run build.yml --repo wjilei/helix-nightly-builds -f force=true
gh run list --repo wjilei/helix-nightly-builds --limit 5
```

GitHub 可能因公开仓库连续 60 天无活动而停用定时工作流。若发生，请在 Actions 页面重新启用；定时任务也可能延迟，不保证准点运行。

## 来源、安全与校验

每次构建先解析一个完整的上游提交 SHA，Windows 和 Linux 使用同一提交。源码压缩包、提交链接、构建日志和 SHA-256 校验文件随版本发布。Release 标签指向本仓库的工作流版本，不是 Helix 源码版本；Helix 源码版本以 `BUILD-INFO.txt` 为准。

```sh
sha256sum -c SHA256SUMS
```

Windows 可使用 `Get-FileHash .\helix-windows-x64.zip -Algorithm SHA256`，与 `SHA256SUMS` 比较。

工作流中的 Actions 固定到提交 SHA；第三方 Rust 依赖使用上游 `Cargo.lock`。上游 master、Rust stable、外部语法仓库仍会变化，构建可能失败；本项目不提供稳定版承诺。Windows 包不含付费代码签名，下载时可能显示系统信誉提示。

Helix 使用 MPL-2.0，许可证保留于 Windows 包及随附源码中。外部语法解析器保留各自上游许可证。

## 本地测试

```sh
python -m unittest discover -s tests -v
```
