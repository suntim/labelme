# -*- mode: python -*-
# vim: ft=python


block_cipher = None


a = Analysis(
    ['labelme/app.py'],
    pathex=['labelme'],
    binaries=[],
    datas=[
        ('labelme/config/default_config.yaml', 'labelme/config'),
        ('labelme/icons/*', 'labelme/icons'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='labelme',
    debug=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False,
    icon='labelme/icons/favicon.ico',
)
app = BUNDLE(
    exe,
    name='labelme',
    icon='labelme/icons/favicon.ico',
    bundle_identifier=None,
    info_plist={'NSHighResolutionCapable': 'True'},
)
