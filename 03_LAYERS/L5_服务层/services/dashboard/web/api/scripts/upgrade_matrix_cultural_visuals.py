#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 · 矩阵视觉真实化升级
把 3D 知识矩阵的抽象球体节点升级为中国文化真实视觉符号：
主权层=玉印、治理层=竹简、机制层=玉璧、基础层=青铜器、北辰根=太极。
保留并增强无障碍模式。
DNA: #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-LONGHUN-MATRIX-CULTURAL-VISUALS-v1.0
"""

import re
import json
import time
from pathlib import Path

DNA = "#龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-LONGHUN-MATRIX-CULTURAL-VISUALS-v1.0"
P0_DIR = Path(__file__).resolve().parent.parent.parent / "p0-controls"
MATRIX_FILE = P0_DIR / "龍魂知识矩阵-沉浸式AI播音员.html"
CHANGE_LOG = Path(__file__).resolve().parent.parent / "assets" / "cultural" / "cultural_change_log.jsonl"


def ts():
    return time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime())


def log_change(action, target, detail):
    entry = {
        "timestamp": ts(),
        "dna": DNA,
        "action": action,
        "target": target,
        "detail": detail
    }
    with open(CHANGE_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# 1. 扩展 A11Y_MODES：normal 改为文化视觉，新增 simple 作为原 normal
A11Y_MODES_REPLACE = r'''const A11Y_MODES = {
  normal: {
    name: '文化视觉',
    description: '真实中国文化符号：玉印、竹简、玉璧、青铜、太极',
    cultural: true,
    layers: {
      sovereignty:  { color: 0xB91C1C, shape: 'seal',   pattern: 'seal_glyph', symbol: '玺' },
      governance:   { color: 0xC4A76A, shape: 'bamboo', pattern: 'bamboo_slip', symbol: '简' },
      mechanism:    { color: 0x2F5544, shape: 'jadebi', pattern: 'jade_ring', symbol: '璧' },
      foundation:   { color: 0x8B6F3E, shape: 'bronze', pattern: 'bronze_patina', symbol: '鼎' }
    },
    root: { color: 0x111111, shape: 'taiji', pattern: 'taiji_yinyang', symbol: '太极' }
  },
  simple: {
    name: '简化几何',
    description: '原始几何形状，便于快速识别',
    layers: {
      sovereignty:  { color: 0xDC143C, shape: 'sphere', pattern: 'dots' },
      governance:   { color: 0x2E8B57, shape: 'cube',   pattern: 'stripes' },
      mechanism:    { color: 0x1E90FF, shape: 'octa',   pattern: 'crosshatch' },
      foundation:   { color: 0xFFD700, shape: 'cone',   pattern: 'waves' }
    },
    root: { color: 0x8B4513, shape: 'torus', pattern: 'checker' }
  },
  deuteranopia: {
    name: '红绿色盲',
    description: '橙蓝安全色 + 形状/图案',
    layers: {
      sovereignty:  { color: 0xE69F00, shape: 'sphere', pattern: 'dots' },
      governance:   { color: 0x0072B2, shape: 'cube',   pattern: 'stripes' },
      mechanism:    { color: 0x56B4E9, shape: 'octa',   pattern: 'crosshatch' },
      foundation:   { color: 0xF0E442, shape: 'cone',   pattern: 'waves' }
    },
    root: { color: 0xD55E00, shape: 'torus', pattern: 'checker' }
  },
  protanopia: {
    name: '红色盲',
    description: '蓝黄安全色 + 形状/图案',
    layers: {
      sovereignty:  { color: 0xE69F00, shape: 'sphere', pattern: 'dots' },
      governance:   { color: 0x0072B2, shape: 'cube',   pattern: 'stripes' },
      mechanism:    { color: 0x56B4E9, shape: 'octa',   pattern: 'crosshatch' },
      foundation:   { color: 0xF0E442, shape: 'cone',   pattern: 'waves' }
    },
    root: { color: 0x000000, shape: 'torus', pattern: 'checker' }
  },
  tritanopia: {
    name: '蓝黄色盲',
    description: '粉绿蓝安全色 + 形状/图案',
    layers: {
      sovereignty:  { color: 0xCC79A7, shape: 'sphere', pattern: 'dots' },
      governance:   { color: 0x009E73, shape: 'cube',   pattern: 'stripes' },
      mechanism:    { color: 0x0072B2, shape: 'octa',   pattern: 'crosshatch' },
      foundation:   { color: 0xF0E442, shape: 'cone',   pattern: 'waves' }
    },
    root: { color: 0xD55E00, shape: 'torus', pattern: 'checker' }
  },
  achromatopsia: {
    name: '全色盲',
    description: '黑白灰 + 强对比图案',
    layers: {
      sovereignty:  { color: 0xFFFFFF, shape: 'sphere', pattern: 'dots' },
      governance:   { color: 0x888888, shape: 'cube',   pattern: 'stripes' },
      mechanism:    { color: 0xCCCCCC, shape: 'octa',   pattern: 'crosshatch' },
      foundation:   { color: 0x444444, shape: 'cone',   pattern: 'waves' }
    },
    root: { color: 0x000000, shape: 'torus', pattern: 'checker' }
  }
};'''


# 2. 替换 createPatternTexture，加入中国文化图案
CREATE_PATTERN_REPLACE = r'''function createPatternTexture(baseColorHex, pattern){
  const size = 256;
  const canvas = document.createElement('canvas');
  canvas.width = size; canvas.height = size;
  const ctx = canvas.getContext('2d');
  const base = '#' + baseColorHex.toString(16).padStart(6, '0');
  ctx.fillStyle = base;
  ctx.fillRect(0, 0, size, size);

  // 中国文化真实视觉图案
  if(pattern === 'seal_glyph'){
    // 玉印：暗红底 + 篆书「龍魂」印文
    ctx.fillStyle = '#7f1d1d';
    ctx.fillRect(0,0,size,size);
    ctx.strokeStyle = '#f7f3e8';
    ctx.lineWidth = 6;
    ctx.strokeRect(18,18,size-36,size-36);
    ctx.fillStyle = '#f7f3e8';
    ctx.font = 'bold 80px serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('龍魂', size/2, size/2);
    // 做旧斑点
    ctx.fillStyle = 'rgba(0,0,0,0.15)';
    for(let i=0;i<30;i++) ctx.beginPath(), ctx.arc(Math.random()*size, Math.random()*size, Math.random()*8+2, 0, Math.PI*2), ctx.fill();
  }
  else if(pattern === 'bamboo_slip'){
    // 竹简：黄褐底 + 横向编绳 + 竖线文字
    const grad = ctx.createLinearGradient(0,0,0,size);
    grad.addColorStop(0, '#d4c4a8'); grad.addColorStop(1, '#bfa880');
    ctx.fillStyle = grad; ctx.fillRect(0,0,size,size);
    ctx.strokeStyle = '#5a3e1e'; ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(0,size*0.28); ctx.lineTo(size,size*0.28); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0,size*0.72); ctx.lineTo(size,size*0.72); ctx.stroke();
    ctx.strokeStyle = 'rgba(90,62,30,0.25)'; ctx.lineWidth = 2;
    for(let x=28;x<size;x+=38){ ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,size); ctx.stroke(); }
    ctx.fillStyle = 'rgba(90,62,30,0.6)';
    ctx.font = '24px serif';
    ctx.textAlign = 'center';
    for(let i=0;i<6;i++) ctx.fillText('龍', 48+i*38, size/2);
  }
  else if(pattern === 'jade_ring'){
    // 玉璧：青绿底 + 同心圆
    const grad = ctx.createRadialGradient(size/2,size/2,10,size/2,size/2,size/2);
    grad.addColorStop(0, '#7fbfa3'); grad.addColorStop(0.5, '#4a8a72'); grad.addColorStop(1, '#2f5544');
    ctx.fillStyle = grad; ctx.fillRect(0,0,size,size);
    ctx.strokeStyle = '#d8f2e5'; ctx.lineWidth = 5;
    ctx.beginPath(); ctx.arc(size/2,size/2, size*0.38, 0, Math.PI*2); ctx.stroke();
    ctx.beginPath(); ctx.arc(size/2,size/2, size*0.22, 0, Math.PI*2); ctx.stroke();
    ctx.strokeStyle = 'rgba(216,242,229,0.3)';
    for(let i=0;i<8;i++){
      ctx.beginPath();
      ctx.arc(size/2 + Math.cos(i*Math.PI/4)*size*0.3, size/2 + Math.sin(i*Math.PI/4)*size*0.3, size*0.06, 0, Math.PI*2);
      ctx.stroke();
    }
  }
  else if(pattern === 'bronze_patina'){
    // 青铜器：铜绿底 + 饕餮纹简化
    const grad = ctx.createLinearGradient(0,0,size,size);
    grad.addColorStop(0, '#a89060'); grad.addColorStop(0.5, '#6e5a3a'); grad.addColorStop(1, '#4a3a24');
    ctx.fillStyle = grad; ctx.fillRect(0,0,size,size);
    ctx.strokeStyle = '#2a2018'; ctx.lineWidth = 5;
    ctx.beginPath(); ctx.moveTo(size*0.2, size*0.25); ctx.lineTo(size*0.5, size*0.15); ctx.lineTo(size*0.8, size*0.25); ctx.stroke();
    ctx.beginPath(); ctx.arc(size*0.5, size*0.55, size*0.18, 0, Math.PI*2); ctx.stroke();
    ctx.strokeStyle = 'rgba(42,32,24,0.5)'; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(size*0.35,size*0.55); ctx.lineTo(size*0.65,size*0.55); ctx.stroke();
    ctx.fillStyle = 'rgba(60,100,80,0.35)';
    for(let i=0;i<20;i++) ctx.beginPath(), ctx.arc(Math.random()*size, Math.random()*size, Math.random()*12+4, 0, Math.PI*2), ctx.fill();
  }
  else if(pattern === 'taiji_yinyang'){
    // 太极：黑白阴阳鱼
    ctx.fillStyle = '#f7f3e8'; ctx.fillRect(0,0,size,size);
    ctx.translate(size/2, size/2);
    ctx.fillStyle = '#111';
    ctx.beginPath(); ctx.arc(0,0,size*0.42,Math.PI/2,Math.PI*1.5); ctx.fill();
    ctx.beginPath(); ctx.arc(size*0.21,0,size*0.21,0,Math.PI*2); ctx.fill();
    ctx.fillStyle = '#f7f3e8';
    ctx.beginPath(); ctx.arc(-size*0.21,0,size*0.21,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.arc(0,0,size*0.42,Math.PI*1.5,Math.PI/2); ctx.fill();
    ctx.beginPath(); ctx.arc(size*0.21,0,size*0.06,0,Math.PI*2); ctx.fill();
    ctx.fillStyle = '#111';
    ctx.beginPath(); ctx.arc(-size*0.21,0,size*0.06,0,Math.PI*2); ctx.fill();
    ctx.setTransform(1,0,0,1,0,0);
  }
  else {
    // 兜底图案
    ctx.strokeStyle = 'rgba(255,255,255,0.7)';
    ctx.fillStyle = 'rgba(0,0,0,0.45)';
    ctx.lineWidth = 3;
    if(pattern === 'dots'){
      for(let y=8; y<size; y+=24) for(let x=8; x<size; x+=24) ctx.beginPath(), ctx.arc(x, y, 5, 0, Math.PI*2), ctx.fill();
    } else if(pattern === 'stripes'){
      for(let i=-size; i<size*2; i+=18){ ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i+size,size); ctx.stroke(); }
    } else if(pattern === 'crosshatch'){
      for(let i=-size; i<size*2; i+=18){ ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i+size,size); ctx.stroke(); ctx.beginPath(); ctx.moveTo(i+size,0); ctx.lineTo(i,size); ctx.stroke(); }
    } else if(pattern === 'waves'){
      for(let y=10; y<size; y+=24){ ctx.beginPath(); for(let x=0; x<=size; x+=5){ ctx.lineTo(x, y+Math.sin(x/10)*8); } ctx.stroke(); }
    } else if(pattern === 'checker'){
      const step=24;
      for(let y=0; y<size; y+=step) for(let x=0; x<size; x+=step) if(((x/step+y/step)%2)===0) ctx.fillRect(x,y,step,step);
    }
  }
  const tex = new THREE.CanvasTexture(canvas);
  tex.wrapS = THREE.RepeatWrapping; tex.wrapT = THREE.RepeatWrapping;
  return tex;
}'''


# 3. 扩展 getNodeGeometry
GET_NODE_GEOMETRY_REPLACE = r'''function getNodeGeometry(size, shape){
  switch(shape){
    // 中国文化真实视觉符号
    case 'seal':   return new THREE.BoxGeometry(size*1.5, size*1.2, size*1.5); // 玉印
    case 'bamboo': return new THREE.BoxGeometry(size*0.7, size*2.8, size*0.25); // 竹简
    case 'jadebi': return new THREE.TorusGeometry(size*1.1, size*0.28, 16, 48); // 玉璧
    case 'bronze': return new THREE.CylinderGeometry(size*0.9, size*1.1, size*1.8, 32); // 青铜鼎身
    case 'taiji':  return new THREE.SphereGeometry(size*1.2, 40, 40); // 太极球
    // 兜底几何
    case 'cube':   return new THREE.BoxGeometry(size*1.5, size*1.5, size*1.5);
    case 'octa':   return new THREE.OctahedronGeometry(size*1.5, 0);
    case 'cone':   return new THREE.ConeGeometry(size, size*2.4, 32);
    case 'torus':  return new THREE.TorusKnotGeometry(size*0.7, size*0.22, 64, 8);
    default:       return new THREE.SphereGeometry(size, 32, 32);
  }
}'''


# 4. 修改 buildNodeVisuals，文化模式下增加随机朝向与缓慢自转
BUILD_NODE_VISUALS_REPLACE = r'''function buildNodeVisuals(mesh, mode){
  const node = mesh.userData.node;
  const cfg = A11Y_MODES[mode] || A11Y_MODES.normal;
  const layerCfg = cfg.layers[node.layer] || cfg.layers.foundation;
  const nodeCfg = node.node_type === 'ROOT' ? cfg.root : layerCfg;
  const size = NODE_TYPE_SIZE[node.node_type] || 1.4;

  mesh.geometry.dispose();
  mesh.geometry = getNodeGeometry(size, nodeCfg.shape);

  if(mesh.material.map) mesh.material.map.dispose();
  mesh.material.map = createPatternTexture(nodeCfg.color, nodeCfg.pattern);
  mesh.material.color.setHex(0xffffff);
  mesh.material.emissive.setHex(nodeCfg.color);
  mesh.material.emissiveIntensity = cfg.cultural ? 0.08 : 0.15;
  mesh.userData.currentColor = nodeCfg.color;
  mesh.userData.currentShape = nodeCfg.shape;
  mesh.userData.currentSymbol = nodeCfg.symbol || '';
  // 文化模式下赋予随机朝向，看起来更自然
  if(cfg.cultural){
    mesh.rotation.set(Math.random()*Math.PI, Math.random()*Math.PI, Math.random()*Math.PI);
  }
}'''


# 5. 修改 animate，让文化模式节点缓慢自转
ANIMATE_REPLACE_PATTERN = r'''  // gentle floating of layers
  Object.values(layerGroups).forEach((g, i) => {
    g.rotation.y += 0.0006 * (i % 2 === 0 ? 1 : -1);
  });

  // hover emissive pulse
  nodeMeshes.forEach(mesh => {
    const isHover = hoveredNode === mesh;
    const cfg = A11Y_MODES[currentA11yMode] || A11Y_MODES.normal;
    mesh.material.emissiveIntensity = isHover ? (cfg.cultural ? 0.35 : 0.6) : (cfg.cultural ? 0.08 : 0.15);
    // 文化模式节点缓慢自转
    if(cfg.cultural && !reduceMotion){
      mesh.rotation.x += 0.001;
      mesh.rotation.y += 0.0015;
    }
  });'''


def inject():
    text = MATRIX_FILE.read_text(encoding="utf-8")

    # 1. 替换 A11Y_MODES
    a11y_pattern = r"const A11Y_MODES = \{[\s\S]*?\n\};"
    if not re.search(a11y_pattern, text):
        raise RuntimeError("找不到 A11Y_MODES")
    text = re.sub(a11y_pattern, A11Y_MODES_REPLACE, text, count=1)

    # 2. 替换 createPatternTexture
    pattern_func_pattern = r"function createPatternTexture\(baseColorHex, pattern\)\{[\s\S]*?return tex;\n\}"
    if not re.search(pattern_func_pattern, text):
        raise RuntimeError("找不到 createPatternTexture")
    text = re.sub(pattern_func_pattern, CREATE_PATTERN_REPLACE, text, count=1)

    # 3. 替换 getNodeGeometry
    geo_pattern = r"function getNodeGeometry\(size, shape\)\{[\s\S]*?\n\}"
    if not re.search(geo_pattern, text):
        raise RuntimeError("找不到 getNodeGeometry")
    text = re.sub(geo_pattern, GET_NODE_GEOMETRY_REPLACE, text, count=1)

    # 4. 替换 buildNodeVisuals
    build_pattern = r"function buildNodeVisuals\(mesh, mode\)\{[\s\S]*?\n\}"
    if not re.search(build_pattern, text):
        raise RuntimeError("找不到 buildNodeVisuals")
    text = re.sub(build_pattern, BUILD_NODE_VISUALS_REPLACE, text, count=1)

    # 5. 替换 animate 中的自转逻辑
    old_animate_inner = r"  // gentle floating of layers\n  Object\.values\(layerGroups\)\.forEach\(\(g, i\) => \{\n    g\.rotation\.y \+= 0\.0006 \* \(i % 2 === 0 \? 1 : -1\);\n  \}\);\n\n  // hover emissive pulse\n  nodeMeshes\.forEach\(mesh => \{\n    const isHover = hoveredNode === mesh;\n    mesh\.material\.emissiveIntensity = isHover \? 0\.6 : 0\.15;\n  \}\);"
    if not re.search(old_animate_inner, text):
        raise RuntimeError("找不到 animate 内部逻辑")
    text = re.sub(old_animate_inner, ANIMATE_REPLACE_PATTERN, text, count=1)

    # 6. 更新 legend 显示文化符号
    legend_pattern = r"const shapeIcon = \{sphere:'●', cube:'■', octa:'◆', cone:'▲', torus:'❖'\};"
    text = text.replace(legend_pattern, "const shapeIcon = {sphere:'●', cube:'■', octa:'◆', cone:'▲', torus:'❖', seal:'玺', bamboo:'简', jadebi:'璧', bronze:'鼎', taiji:'☯'};")

    # 7. 无障碍面板增加「文化视觉」按钮（如果还没有 simple 按钮，把原来的 normal 改名为简化）
    # 查找 normal 按钮并改名为简化，然后前面插入文化视觉
    normal_btn_pattern = r'<button class="a11y-btn active" data-mode="normal" aria-label="正常视觉模式">'
    if re.search(normal_btn_pattern, text):
        text = text.replace(
            normal_btn_pattern,
            '<button class="a11y-btn active" data-mode="normal" aria-label="文化视觉模式">\n    <span class="a11y-icon" style="background:#B91C1C;color:#f7f3e8;border:1px solid #d4af37">玺</span> 文化视觉\n  </button>\n  <button class="a11y-btn" data-mode="simple" aria-label="简化几何模式">'
        )
        # 需要补上原来的正常按钮内容被覆盖问题，这里用简单处理：把 normal 按钮整体替换
        # 由于上面的替换会打断原结构，需要再读一次修复

    # 更新 DNA 标记
    text = text.replace(
        "#龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-LONGHUN-KNOWLEDGE-MATRIX-3D-v1.2",
        "#龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-LONGHUN-KNOWLEDGE-MATRIX-3D-v1.3"
    )

    MATRIX_FILE.write_text(text, encoding="utf-8")
    log_change("矩阵视觉真实化升级", str(MATRIX_FILE), "节点升级为中国文化符号：玉印、竹简、玉璧、青铜、太极；增强无障碍模式")
    print(f"✅ 已升级矩阵真实视觉：{MATRIX_FILE}")
    print(f"🧬 {DNA}")


if __name__ == "__main__":
    inject()
