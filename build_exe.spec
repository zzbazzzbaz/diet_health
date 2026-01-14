# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

# 项目根目录
project_root = Path('.').resolve()

# 收集所有需要的数据文件
datas = [
    ('templates', 'templates'),
    ('static', 'static'),
    ('media', 'media'),
    ('logs', 'logs'),
    # 收集各个应用的模板文件
    ('apps/quiz/templates', 'apps/quiz/templates'),
    ('apps/game/templates', 'apps/game/templates'),
    # 收集配置模块（作为 Python 包）
    ('config', 'config'),
    ('apps', 'apps'),
]

# 如果数据库文件存在，则打包
if os.path.exists('db.sqlite3'):
    datas.append(('db.sqlite3', '.'))

# 如果 core 应用有模板，也打包
if os.path.exists('apps/core/templates'):
    datas.append(('apps/core/templates', 'apps/core/templates'))

# 收集 Django 和其他包的模板文件
hiddenimports = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.template.loaders.filesystem',
    'django.template.loaders.app_directories',
    'whitenoise',
    'whitenoise.middleware',
    'simpleui',
    'PIL',
    'PIL._imaging',
    'dashscope',
    # 项目配置模块
    'config',
    'config.settings',
    'config.urls',
    'config.wsgi',
    # 应用模块
    'apps',
    'apps.quiz',
    'apps.game',
    'apps.core',
    'apps.quiz.models',
    'apps.quiz.views',
    'apps.quiz.admin',
    'apps.quiz.urls',
    'apps.game.models',
    'apps.game.views',
    'apps.game.admin',
    'apps.game.urls',
    'apps.core.models',
    'apps.core.views',
    'apps.core.admin',
]

a = Analysis(
    ['run_server.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=['.'],  # 使用当前目录的 hook 文件
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='膳食健康知识问答系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='膳食健康知识问答系统',
)
