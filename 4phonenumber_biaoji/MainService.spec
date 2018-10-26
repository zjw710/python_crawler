# -*- mode: python -*-

block_cipher = None


a = Analysis(['MainService.py'],
             pathex=['D:\\www\\1pyProject_www\\3python_crawler\\4phonenumber_biaoji'],
             binaries=[],
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='MainService',
          debug=False,
          strip=False,
          upx=True,
          console=False , version='file_version_info.txt', icon='ico.ico')
