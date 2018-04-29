# -*- mode: python -*-

block_cipher = None


a = Analysis(['labelme\\app.py'],
             pathex=['F:\\MyPythonCode2\\Qt5\\labelme-master2'],
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
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='app',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='favicon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='app')
