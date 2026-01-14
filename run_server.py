#!/usr/bin/env python
"""
Django 应用启动脚本
用于打包成 exe 后启动服务器
"""
import os
import sys
import webbrowser
import time
from threading import Timer
from pathlib import Path

def open_browser():
    """延迟打开浏览器"""
    time.sleep(2)
    webbrowser.open('http://127.0.0.1:8000')

def main():
    """启动 Django 开发服务器"""
    # 设置环境变量
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    # 获取基础目录
    if getattr(sys, 'frozen', False):
        # 打包后的环境
        # sys._MEIPASS 是 PyInstaller 解压临时文件的目录（_internal）
        # sys.executable 的父目录是可执行文件所在目录
        base_dir = Path(sys._MEIPASS)
        exe_dir = Path(sys.executable).parent
        
        # 将 _MEIPASS 添加到 Python 路径
        sys.path.insert(0, str(base_dir))
        
        # 切换到 _internal 目录（所有数据文件都在这里）
        os.chdir(base_dir)
        
        print(f"运行目录: {base_dir}")
        print(f"可执行文件目录: {exe_dir}")
    else:
        # 开发环境
        base_dir = Path(__file__).resolve().parent
        os.chdir(base_dir)
    
    # 确保必要的目录存在
    (base_dir / 'logs').mkdir(exist_ok=True)
    (base_dir / 'media').mkdir(exist_ok=True)
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        print("错误：无法导入 Django")
        print(str(exc))
        input("按回车键退出...")
        sys.exit(1)
    
    print("=" * 60)
    print("膳食健康知识问答系统")
    print("=" * 60)
    print("正在启动服务器...")
    print("服务器地址: http://127.0.0.1:8000")
    print("管理后台: http://127.0.0.1:8000/admin")
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    # 延迟打开浏览器
    Timer(2, open_browser).start()
    
    # 启动服务器
    sys.argv = ['run_server.py', 'runserver', '127.0.0.1:8000', '--noreload']
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"\n错误: {e}")
        input("按回车键退出...")
