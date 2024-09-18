# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

a = Analysis(
    ['trang_chu.py'],
    pathex=['C:\\TTNT\\OpenCv'],
    binaries=[],
    datas=[
        (r'D:\TTNT\OpenCv\trainer\trainer.yml', 'trainer'),
        (r'D:\TTNT\OpenCv\haarcascade_frontalface_default.xml', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='trang_chu',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['donga.ico'],
)
