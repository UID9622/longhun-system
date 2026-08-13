# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/Users/zuimeidedeyihan/longhun-system/08_BIN/cnsh_web_ide.py'],
    pathex=['/Users/zuimeidedeyihan/longhun-system/08_BIN'],
    binaries=[],
    datas=[('/Users/zuimeidedeyihan/longhun-system/static', 'static')],
    hiddenimports=['fastapi', 'uvicorn', 'uvicorn.logging', 'uvicorn.loops', 'uvicorn.loops.auto', 'uvicorn.protocols', 'uvicorn.protocols.http', 'uvicorn.protocols.http.auto', 'uvicorn.lifespan', 'uvicorn.lifespan.on', 'starlette', 'pydantic', 'requests', 'requests.adapters', 'urllib3', 'cnsh_editor', 'cnsh_compiler', 'cnsh_ui', 'cnsh_complete', 'cnsh_interpreter', 'cnsh_gateway', 'cnsh_ai_providers', 'cnsh_bagua_router', 'lh_agent_cosmos'],
    hookspath=[],
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
    name='CNSH_IDE',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CNSH_IDE',
)
app = BUNDLE(
    coll,
    name='CNSH_IDE.app',
    icon=None,
    bundle_identifier='cn.longhun.cnsh.ide.1.0.0',
)
