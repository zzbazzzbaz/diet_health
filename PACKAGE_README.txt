========================================
膳食健康知识问答系统 - 打包说明
========================================

【推荐方式：使用 GitHub Actions 自动打包】

✨ 优势：自动在 Windows、macOS、Linux 三个平台打包，完全免费！

1. 推送代码到 GitHub
2. 等待自动构建（10-15 分钟）
3. 下载对应平台的打包文件

详细步骤请查看：QUICK_START.md


【本地打包方式】

如果不想使用 GitHub Actions，可以本地打包：

1. 双击运行打包脚本：
   - Windows: build.bat
   - macOS/Linux: ./build.sh

2. 等待打包完成（可能需要几分钟）

3. 打包完成后会自动打开 dist 文件夹

4. 将整个 "膳食健康知识问答系统" 文件夹复制到目标电脑

5. 双击可执行文件启动应用：
   - Windows: 膳食健康知识问答系统.exe
   - macOS: 膳食健康知识问答系统
   - Linux: 膳食健康知识问答系统

⚠️ 注意：本地打包只能生成当前系统的可执行文件
   - macOS 上只能打包 macOS 版本
   - Windows 上只能打包 Windows 版本
   - Linux 上只能打包 Linux 版本


【重要提示】

✓ 打包成功！应用已经过测试，可以正常运行
✓ 所有模板文件、静态文件、数据库都已正确打包
✓ 启动后会自动打开浏览器访问 http://127.0.0.1:8000
✓ 所有文件都在 _internal 目录下，这是正常的 PyInstaller 打包结构
✓ 不要删除 _internal 目录，它包含所有必需的文件


【详细步骤】

一、打包前准备

1. 确保已安装 Python 3.10 或更高版本
2. 确保已安装所有依赖：
   uv sync
   或
   pip install -r requirements.txt

3. 运行数据库迁移：
   uv run python manage.py migrate

4. 创建管理员账号（如果还没有）：
   uv run python manage.py createsuperuser

5. 收集静态文件：
   uv run python manage.py collectstatic


二、开始打包

方法1：使用打包脚本（推荐）
   Windows: 双击 build.bat
   macOS/Linux: ./build.sh

方法2：手动打包
   uv run pyinstaller build_exe.spec


三、打包后的文件结构

dist/膳食健康知识问答系统/
├── 膳食健康知识问答系统(.exe)  ← 双击启动
└── _internal/                    ← 所有数据文件
    ├── templates/                ← 模板文件
    ├── static/                   ← 静态文件
    ├── media/                    ← 媒体文件
    ├── db.sqlite3                ← 数据库
    ├── logs/                     ← 日志目录
    ├── config/                   ← 配置模块
    ├── apps/                     ← 应用模块
    └── 其他依赖文件...


四、在目标电脑上使用

1. 复制整个 "膳食健康知识问答系统" 文件夹到目标电脑
2. 双击可执行文件
3. 等待几秒，浏览器会自动打开
4. 访问地址：
   - 前台：http://127.0.0.1:8000
   - 后台：http://127.0.0.1:8000/admin


五、常见问题

Q: 打包后文件很大？
A: 正常现象，包含了 Python 和所有依赖库，通常 100-300MB

Q: 双击 exe 没反应？
A: 检查是否有杀毒软件拦截，或查看 _internal/logs 目录下的日志

Q: 提示端口被占用？
A: 关闭其他占用 8000 端口的程序，或修改 run_server.py 中的端口号

Q: 静态文件无法加载？
A: 确保打包前运行了 uv run python manage.py collectstatic

Q: 数据库错误？
A: 确保 _internal/db.sqlite3 文件存在且有读写权限

Q: 找不到模板文件？
A: 确保 _internal/apps/quiz/templates 等目录存在

Q: macOS 提示"无法打开，因为无法验证开发者"？
A: 右键点击可执行文件，选择"打开"，然后点击"打开"按钮


六、注意事项

1. 首次运行可能需要几秒钟启动
2. 不要删除 _internal 目录下的任何文件
3. 数据库文件 db.sqlite3 包含所有数据，注意备份
4. 关闭程序时按 Ctrl+C 或直接关闭控制台窗口
5. 打包后的应用只能在相同操作系统上运行：
   - Windows 打包的只能在 Windows 上运行
   - macOS 打包的只能在 macOS 上运行
   - Linux 打包的只能在 Linux 上运行


七、更新应用

如果代码有更新：
1. 修改代码
2. 重新运行打包脚本
3. 用新的 dist 文件夹替换旧的


八、跨平台打包

如果需要为不同操作系统打包：
- Windows 版本：在 Windows 电脑上运行 build.bat
- macOS 版本：在 macOS 电脑上运行 ./build.sh
- Linux 版本：在 Linux 电脑上运行 ./build.sh

PyInstaller 不支持交叉编译，必须在目标平台上打包。


九、技术支持

详细文档：build_instructions.md
启动脚本：run_server.py
打包配置：build_exe.spec
测试脚本：test_package.py

如有问题，请查看控制台输出的错误信息。


十、测试打包结果

打包前可以运行测试脚本检查文件：
uv run python test_package.py

这会检查所有需要打包的文件是否存在。
