#!/bin/bash

echo "========================================"
echo "膳食健康知识问答系统 - 打包工具"
echo "========================================"
echo ""

echo "[1/6] 检查 PyInstaller..."
if ! uv pip show pyinstaller > /dev/null 2>&1; then
    echo "PyInstaller 未安装，正在安装..."
    uv pip install pyinstaller
else
    echo "PyInstaller 已安装"
fi
echo ""

echo "[2/6] 检查模板文件..."
if [ ! -f "apps/quiz/templates/quiz/index.html" ]; then
    echo "错误：找不到 quiz 应用的模板文件！"
    echo "请确保 apps/quiz/templates/quiz/index.html 存在"
    exit 1
fi
echo "模板文件检查通过"
echo ""

echo "[3/6] 收集静态文件..."
uv run python manage.py collectstatic --noinput
echo ""

echo "[4/6] 清理旧的打包文件..."
rm -rf build dist
echo ""

echo "[5/6] 开始打包..."
echo "这可能需要几分钟，请耐心等待..."
uv run pyinstaller build_exe.spec
echo ""

if [ -f "dist/膳食健康知识问答系统/膳食健康知识问答系统" ]; then
    echo "[6/6] 验证打包结果..."
    
    DIST_DIR="dist/膳食健康知识问答系统"
    
    if [ ! -f "$DIST_DIR/apps/quiz/templates/quiz/index.html" ]; then
        echo "警告：quiz 模板文件未正确打包！"
        echo "位置：$DIST_DIR/apps/quiz/templates/quiz/index.html"
    else
        echo "✓ quiz 模板文件已打包"
    fi
    
    if [ ! -f "$DIST_DIR/templates/base.html" ]; then
        echo "警告：基础模板文件未正确打包！"
    else
        echo "✓ 基础模板文件已打包"
    fi
    
    if [ ! -d "$DIST_DIR/static" ]; then
        echo "警告：静态文件未正确打包！"
    else
        echo "✓ 静态文件已打包"
    fi
    
    echo ""
    echo "========================================"
    echo "打包成功！"
    echo "========================================"
    echo ""
    echo "可执行文件位置:"
    echo "$DIST_DIR/膳食健康知识问答系统"
    echo ""
    echo "使用说明:"
    echo "1. 将整个 '$DIST_DIR' 文件夹复制到目标电脑"
    echo "2. 双击 '膳食健康知识问答系统' 启动应用"
    echo "3. 浏览器会自动打开 http://127.0.0.1:8000"
    echo ""
    echo "打开打包目录..."
    open "$DIST_DIR"
else
    echo "[6/6] 打包失败！"
    echo "请查看上面的错误信息"
fi
