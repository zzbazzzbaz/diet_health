# GitHub Actions 自动打包说明

## 功能

这个 GitHub Actions 工作流会自动在三个平台上打包应用：
- ✅ Windows (.exe)
- ✅ macOS
- ✅ Linux

## 触发条件

工作流会在以下情况自动运行：

1. **推送代码到 main/master 分支**
   ```bash
   git push origin main
   ```

2. **创建版本标签**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

3. **手动触发**
   - 在 GitHub 仓库页面
   - 点击 "Actions" 标签
   - 选择 "Build Executables"
   - 点击 "Run workflow"

## 使用步骤

### 1. 推送代码到 GitHub

```bash
cd diet_health
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/你的用户名/你的仓库名.git
git push -u origin main
```

### 2. 等待构建完成

- 访问 GitHub 仓库的 Actions 页面
- 查看构建进度
- 通常需要 5-15 分钟

### 3. 下载打包文件

#### 方法 1：从 Artifacts 下载（推送代码后）

1. 进入 Actions 页面
2. 点击最新的工作流运行
3. 在页面底部找到 "Artifacts" 部分
4. 下载对应平台的文件：
   - `diet-health-windows.zip` - Windows 版本
   - `diet-health-macos.tar.gz` - macOS 版本
   - `diet-health-linux.tar.gz` - Linux 版本

#### 方法 2：从 Releases 下载（创建标签后）

1. 创建版本标签：
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. 访问仓库的 Releases 页面
3. 下载对应平台的文件

## 文件说明

### Windows 版本
- 文件：`diet-health-windows.zip`
- 解压后双击 `膳食健康知识问答系统.exe` 启动

### macOS 版本
- 文件：`diet-health-macos.tar.gz`
- 解压：`tar -xzf diet-health-macos.tar.gz`
- 启动：`./diet-health-macos/膳食健康知识问答系统`
- 如果提示无法验证开发者，右键点击选择"打开"

### Linux 版本
- 文件：`diet-health-linux.tar.gz`
- 解压：`tar -xzf diet-health-linux.tar.gz`
- 启动：`./diet-health-linux/膳食健康知识问答系统`
- 可能需要添加执行权限：`chmod +x diet-health-linux/膳食健康知识问答系统`

## 工作流配置文件

位置：`.github/workflows/build.yml`

### 主要步骤

1. **检出代码** - 获取仓库代码
2. **设置 Python** - 安装 Python 3.10
3. **安装 uv** - 安装包管理器
4. **安装依赖** - 安装项目依赖和 PyInstaller
5. **收集静态文件** - 运行 Django collectstatic
6. **打包** - 使用 PyInstaller 打包
7. **创建压缩包** - 压缩打包结果
8. **上传** - 上传到 Artifacts 或 Releases

## 自定义配置

### 修改触发分支

编辑 `.github/workflows/build.yml`：

```yaml
on:
  push:
    branches: [ main, develop ]  # 添加其他分支
```

### 修改 Python 版本

```yaml
python-version: ['3.11']  # 改为其他版本
```

### 只在特定平台打包

```yaml
strategy:
  matrix:
    os: [windows-latest]  # 只打包 Windows
```

## 注意事项

1. **首次运行可能较慢**
   - GitHub Actions 需要下载依赖
   - 后续运行会使用缓存

2. **Artifacts 保留时间**
   - 默认保留 30 天
   - 可以在配置中修改 `retention-days`

3. **私有仓库限制**
   - 免费账户有使用时长限制
   - 公开仓库无限制

4. **数据库文件**
   - 打包会包含当前的 `db.sqlite3`
   - 建议在打包前确保数据库是干净的测试数据

5. **文件大小**
   - 打包后每个平台约 100-300MB
   - GitHub Artifacts 有大小限制（通常 2GB）

## 故障排查

### 构建失败

1. 查看 Actions 日志
2. 检查依赖是否正确安装
3. 确保 `pyproject.toml` 配置正确

### 下载的文件无法运行

1. 确保下载了正确平台的版本
2. Windows：检查杀毒软件是否拦截
3. macOS：右键选择"打开"而不是双击
4. Linux：添加执行权限

### 文件太大

1. 在 `build_exe.spec` 中添加排除项：
   ```python
   excludes=['tkinter', 'matplotlib', 'test']
   ```

2. 使用 UPX 压缩（已启用）

## 版本发布流程

### 1. 准备发布

```bash
# 确保代码已提交
git add .
git commit -m "Release v1.0.0"
```

### 2. 创建标签

```bash
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0
```

### 3. 等待构建

- 访问 Actions 页面查看进度
- 构建完成后会自动创建 Release

### 4. 编辑 Release 说明

1. 访问 Releases 页面
2. 点击编辑最新的 Release
3. 添加更新日志和说明

## 高级用法

### 并行构建多个版本

```yaml
strategy:
  matrix:
    os: [windows-latest, macos-latest, ubuntu-latest]
    python-version: ['3.10', '3.11', '3.12']
```

### 添加测试步骤

在打包前添加测试：

```yaml
- name: Run tests
  run: |
    uv run python manage.py test
```

### 自动部署

可以添加部署步骤，将打包文件上传到服务器或云存储。

## 成本

- **公开仓库**：完全免费
- **私有仓库**：
  - 免费账户：每月 2000 分钟
  - 每次构建约 10-20 分钟
  - 三个平台并行约 15 分钟

## 相关链接

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [PyInstaller 文档](https://pyinstaller.org/)
- [uv 文档](https://docs.astral.sh/uv/)
