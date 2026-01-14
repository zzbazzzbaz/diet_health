# 快速开始 - 使用 GitHub Actions 打包

## 🚀 三步完成跨平台打包

### 1️⃣ 推送代码到 GitHub

```bash
cd diet_health

# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Add build configuration"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/你的仓库名.git

# 推送
git push -u origin main
```

### 2️⃣ 等待自动构建

- 访问 GitHub 仓库页面
- 点击 **Actions** 标签
- 查看构建进度（约 10-15 分钟）

### 3️⃣ 下载打包文件

构建完成后：

1. 在 Actions 页面点击最新的工作流运行
2. 滚动到底部找到 **Artifacts** 部分
3. 下载对应平台的文件：
   - 📦 `diet-health-windows.zip` - Windows 版本
   - 📦 `diet-health-macos.tar.gz` - macOS 版本
   - 📦 `diet-health-linux.tar.gz` - Linux 版本

## 📝 发布正式版本

如果要创建正式发布版本：

```bash
# 创建版本标签
git tag v1.0.0

# 推送标签
git push origin v1.0.0
```

然后访问仓库的 **Releases** 页面下载。

## 🎯 手动触发构建

不想推送代码也可以手动触发：

1. 访问 GitHub 仓库的 **Actions** 页面
2. 点击左侧的 **Build Executables**
3. 点击右上角的 **Run workflow** 按钮
4. 选择分支，点击 **Run workflow**

## ✅ 优势

- ✨ 自动在 Windows、macOS、Linux 三个平台打包
- 🆓 完全免费（公开仓库）
- ⚡ 并行构建，速度快
- 📦 自动压缩和上传
- 🔄 可重复构建

## 📖 详细文档

查看 `GITHUB_ACTIONS_README.md` 了解更多配置选项。

## ❓ 常见问题

**Q: 我没有 GitHub 账号怎么办？**
A: 访问 https://github.com 免费注册一个账号。

**Q: 构建失败了怎么办？**
A: 点击失败的工作流查看日志，通常是依赖安装问题。

**Q: 可以只打包 Windows 版本吗？**
A: 可以，编辑 `.github/workflows/build.yml`，修改 `os: [windows-latest]`。

**Q: 打包文件在哪里？**
A: Actions 页面 → 点击工作流运行 → 底部 Artifacts 部分。

**Q: Artifacts 保留多久？**
A: 默认 30 天，可以在配置中修改。
