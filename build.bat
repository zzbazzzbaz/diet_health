@echo off
chcp 65001 >nul
echo ========================================
echo 膳食健康知识问答系统 - 打包工具
echo ========================================
echo.

echo [1/6] 检查 PyInstaller...
uv pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller 未安装，正在安装...
    uv pip install pyinstaller
) else (
    echo PyInstaller 已安装
)
echo.

echo [2/6] 检查模板文件...
if not exist "apps\quiz\templates\quiz\index.html" (
    echo 错误：找不到 quiz 应用的模板文件！
    echo 请确保 apps\quiz\templates\quiz\index.html 存在
    pause
    exit /b 1
)
echo 模板文件检查通过
echo.

echo [3/6] 收集静态文件...
uv run python manage.py collectstatic --noinput
echo.

echo [4/6] 清理旧的打包文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo.

echo [5/6] 开始打包...
echo 这可能需要几分钟，请耐心等待...
uv run pyinstaller build_exe.spec
echo.

if exist "dist\膳食健康知识问答系统\膳食健康知识问答系统.exe" (
    echo [6/6] 验证打包结果...
    
    REM 检查关键文件是否存在
    set "DIST_DIR=dist\膳食健康知识问答系统"
    
    if not exist "%DIST_DIR%\apps\quiz\templates\quiz\index.html" (
        echo 警告：quiz 模板文件未正确打包！
        echo 位置：%DIST_DIR%\apps\quiz\templates\quiz\index.html
    ) else (
        echo ✓ quiz 模板文件已打包
    )
    
    if not exist "%DIST_DIR%\templates\base.html" (
        echo 警告：基础模板文件未正确打包！
    ) else (
        echo ✓ 基础模板文件已打包
    )
    
    if not exist "%DIST_DIR%\static" (
        echo 警告：静态文件未正确打包！
    ) else (
        echo ✓ 静态文件已打包
    )
    
    echo.
    echo ========================================
    echo 打包成功！
    echo ========================================
    echo.
    echo 可执行文件位置:
    echo %DIST_DIR%\膳食健康知识问答系统.exe
    echo.
    echo 使用说明:
    echo 1. 将整个 "%DIST_DIR%" 文件夹复制到目标电脑
    echo 2. 双击 "膳食健康知识问答系统.exe" 启动应用
    echo 3. 浏览器会自动打开 http://127.0.0.1:8000
    echo.
    echo 按任意键打开打包目录...
    pause >nul
    explorer "%DIST_DIR%"
) else (
    echo [6/6] 打包失败！
    echo 请查看上面的错误信息
    echo.
    pause
)
