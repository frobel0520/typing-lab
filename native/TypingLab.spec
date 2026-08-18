# PyInstaller recipe for the native desktop build.
# Run from the project folder with:
#   py -3.12 -m PyInstaller --noconfirm --clean native/TypingLab.spec

from pathlib import Path

project = Path(SPECPATH)

a = Analysis(
    [str(project / "typing_lab.py")],
    pathex=[str(project)],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="TypingLab",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)
