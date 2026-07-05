#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂知识矩阵 3D 沉浸式页面构建脚本
DNA: #龍芯⚡️2026-07-04-LONGHUN-KNOWLEDGE-MATRIX-3D-BUILDER-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
import json
import shutil
from pathlib import Path

BASE = Path("/Users/zuimeidedeyihan/longhun-system")
NODES_FILE = BASE / "knowledge-graph/nodes/all_nodes.json"
EDGES_FILE = BASE / "knowledge-graph/edges/all_edges.json"
FONT_SRC = BASE / "longhun-font/assets/LonghunFont-Regular-v0004.otf"
FONT_DEST_DIR = BASE / "web/assets/fonts"
HTML_PATH = BASE / "web/p0-controls/龍魂知识矩阵-3D-沉浸式.html"

GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
DNA = "#龍芯⚡️2026-07-04-LONGHUN-KNOWLEDGE-MATRIX-3D-v1.1"

HTML_TEMPLATE = r'''<!-- {dna} 自动注入·三维知识矩阵·来源可查 -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🐉 龍魂知识矩阵 · 三维沉浸式 · UID9622</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E🐉%3C/text%3E%3C/svg%3E">
<style>
@font-face {
  font-family: 'LonghunFont';
  src: url('../assets/fonts/LonghunFont-Regular-v0004.otf') format('opentype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}
.longhun{font-family:'LonghunFont','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;}
:root{
  --lh-gold:#FFD700;--lh-red:#DC143C;--lh-green:#2E8B57;--lh-blue:#1E90FF;--lh-brown:#8B4513;
  --lh-accent:#a78bfa;--lh-bg:#0a0a0f;--lh-text:#e4e4e7;
}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:100%;height:100%;overflow:hidden;background:#0a0a0f;color:#e4e4e7;font-family:'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;}
#canvas-container{position:fixed;inset:0;z-index:1}
#nebula{position:fixed;inset:0;z-index:0;background:
  radial-gradient(circle at 20% 30%,rgba(220,20,60,.12),transparent 35%),
  radial-gradient(circle at 80% 20%,rgba(46,139,87,.12),transparent 35%),
  radial-gradient(circle at 40% 80%,rgba(30,144,255,.12),transparent 35%),
  radial-gradient(circle at 70% 70%,rgba(255,215,0,.10),transparent 30%);animation:nebulaDrift 30s ease-in-out infinite alternate}
@keyframes nebulaDrift{from{transform:scale(1)}to{transform:scale(1.08)}}

/* HUD */
#hud{position:fixed;top:14px;left:14px;right:14px;z-index:10;display:flex;gap:12px;align-items:center;flex-wrap:wrap;pointer-events:none}
.hud-panel{background:rgba(10,10,15,0.78);border:1px solid rgba(167,139,250,0.25);border-radius:14px;padding:8px 14px;backdrop-filter:blur(8px);pointer-events:auto}
#title{font-size:16px;font-weight:800;letter-spacing:0.08em;color:#FFD700;text-shadow:0 0 12px rgba(255,215,0,0.35)}
#subtitle{font-size:11px;color:#a78bfa;margin-top:2px}
#dna-line{font-size:10px;color:#d4a574;font-family:monospace;margin-top:3px;word-break:break-all;max-width:360px}
#stats{font-size:12px;color:#94a3b8}
#stats b{color:#4ade80}
#search{background:rgba(18,18,26,0.9);border:1px solid rgba(167,139,250,0.35);border-radius:8px;padding:6px 10px;color:#e4e4e7;font-size:12px;outline:none;width:180px}
#search::placeholder{color:#64748b}
#legend{display:flex;gap:8px;align-items:center}
.legend-item{display:flex;align-items:center;gap:4px;font-size:11px;color:#94a3b8}
.legend-dot{width:8px;height:8px;border-radius:50%;box-shadow:0 0 6px currentColor}

/* Detail panel */
#detail{position:fixed;top:14px;right:-340px;bottom:14px;width:320px;background:rgba(10,10,15,0.92);border:1px solid rgba(167,139,250,0.25);border-radius:16px;padding:16px;z-index:20;overflow-y:auto;backdrop-filter:blur(10px);transition:right .35s ease}
#detail.open{right:14px}
#detail h2{font-size:15px;color:#FFD700;margin-bottom:10px;display:flex;align-items:center;gap:8px}
#detail .tag{display:inline-block;font-size:10px;padding:2px 8px;border-radius:10px;background:rgba(255,215,0,0.12);color:#FFD700;border:1px solid rgba(255,215,0,0.25);margin-bottom:10px}
#detail .field{margin-bottom:10px}
#detail .field-label{font-size:10px;color:#64748b;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:2px}
#detail .field-value{font-size:12px;color:#e4e4e7;line-height:1.5}
#detail .dna{font-size:10px;color:#d4a574;font-family:monospace;word-break:break-all}
#detail table{width:100%;border-collapse:collapse;font-size:11px;margin-top:6px}
#detail th,#detail td{text-align:left;padding:4px 6px;border-bottom:1px solid rgba(255,255,255,0.06}
#detail th{color:#a78bfa}
#detail .close{position:absolute;top:10px;right:10px;background:none;border:none;color:#94a3b8;font-size:18px;cursor:pointer}
#detail .close:hover{color:#fff}
#edges-list{margin-top:8px}
.edge-row{font-size:11px;padding:6px;border-radius:6px;background:rgba(255,255,255,0.03);margin-bottom:4px;color:#cbd5e1}
.edge-row b{color:#60a5fa}

/* Tooltip */
#tooltip{position:fixed;z-index:30;background:rgba(10,10,15,0.95);border:1px solid rgba(255,215,0,0.3);border-radius:8px;padding:8px 12px;font-size:12px;color:#e4e4e7;pointer-events:none;opacity:0;transition:opacity .15s;max-width:280px;box-shadow:0 0 20px rgba(255,215,0,0.12)}
#tooltip .tt-title{color:#FFD700;font-weight:700;margin-bottom:3px}
#tooltip .tt-meta{font-size:10px;color:#94a3b8}

/* Loading overlay */
#loader{position:fixed;inset:0;background:#0a0a0f;z-index:50;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;transition:opacity .8s}
#loader.hidden{opacity:0;pointer-events:none}
#loader .logo{font-size:52px;animation:pulse 2s infinite}
#loader .motto{font-size:18px;font-weight:700;color:transparent;background:linear-gradient(135deg,#FFD700,#ef4444,#8b5cf6);-webkit-background-clip:text;background-clip:text;letter-spacing:.1em}
#loader .sub{font-size:12px;color:#64748b;letter-spacing:.06em}
@keyframes pulse{0%,100%{opacity:.6}50%{opacity:1}}

/* Help overlay */
#help{position:fixed;bottom:14px;left:50%;transform:translateX(-50%);background:rgba(10,10,15,0.88);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:12px 18px;z-index:15;display:none;gap:10px 18px;flex-wrap:wrap;font-size:11px;color:#94a3b8}
#help.open{display:flex}
#help kbd{background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.15);border-radius:3px;padding:1px 5px;color:#e2e8f0;font-family:monospace}

/* Floating controls */
#floating-controls{position:fixed;bottom:14px;right:14px;z-index:16;display:flex;gap:8px}
#floating-controls button{background:rgba(10,10,15,.88);border:1px solid rgba(255,215,0,.25);border-radius:10px;color:#e4e4e7;padding:8px 12px;font-size:12px;cursor:pointer;transition:.2s}
#floating-controls button:hover{border-color:#FFD700;color:#FFD700}

/* Root card footer */
#root-card{position:fixed;bottom:10px;left:14px;z-index:10;font-size:9px;color:#64748b;max-width:420px;line-height:1.4}
</style>
</head>
<body>
<div id="loader">
  <div class="logo">🐉</div>
  <div class="motto"><span class="longhun">龍魂</span>知识矩阵 · 三维沉浸</div>
  <div class="sub">北辰不动点 · 天地人三才 · 五行四象</div>
</div>

<div id="canvas-container"></div>
<div id="nebula"></div>

<div id="hud">
  <div class="hud-panel">
    <div id="title">☰ <span class="longhun">龍🇨🇳魂</span> ☷ 知识矩阵</div>
    <div id="subtitle">三维沉浸式 · 中国文化主题 · 真实光影</div>
    <div id="dna-line">{dna}</div>
  </div>
  <div class="hud-panel" id="stats">
    节点 <b id="node-count">-</b> · 关系 <b id="edge-count">-</b> · 层级 <b>4</b>
  </div>
  <div class="hud-panel">
    <input id="search" type="text" placeholder="搜索节点 / 变量 / DNA…" autocomplete="off">
  </div>
  <div class="hud-panel" id="legend">
    <div class="legend-item"><span class="legend-dot" style="background:#DC143C;color:#DC143C"></span>主权·朱雀</div>
    <div class="legend-item"><span class="legend-dot" style="background:#2E8B57;color:#2E8B57"></span>治理·青龙</div>
    <div class="legend-item"><span class="legend-dot" style="background:#1E90FF;color:#1E90FF"></span>机制·玄武</div>
    <div class="legend-item"><span class="legend-dot" style="background:#FFD700;color:#FFD700"></span>基础·白虎</div>
    <div class="legend-item"><span class="legend-dot" style="background:#8B4513;color:#8B4513"></span>北辰·太极</div>
  </div>
</div>

<div id="tooltip">
  <div class="tt-title"></div>
  <div class="tt-meta"></div>
</div>

<div id="detail">
  <button class="close">×</button>
  <h2 id="detail-title">节点详情</h2>
  <div id="detail-content"></div>
</div>

<div id="help">
  <span><kbd>左键拖拽</kbd> 旋转</span>
  <span><kbd>滚轮</kbd> 缩放</span>
  <span><kbd>右键</kbd> 平移</span>
  <span><kbd>点击节点</kbd> 详情</span>
  <span><kbd>F</kbd> 自动旋转</span>
  <span><kbd>R</kbd> 复位</span>
  <span><kbd>H</kbd> 帮助</span>
</div>

<div id="floating-controls">
  <button onclick="toggleAutoRotate()" id="btn-rotate">⏵ 旋转</button>
  <button onclick="resetView()">↺ 复位</button>
  <button onclick="toggleFullscreen()">⛶ 全屏</button>
  <button onclick="toggleHelp()">? 帮助</button>
</div>

<div id="root-card">
  ROOT_CARD | 系统: UID9622 龍魂系统 | 模块: 知识矩阵三维沉浸式可视化 | DNA: {dna} | CONFIRM: {confirm} | GPG: {gpg}
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script>
const KNOWLEDGE_NODES = __NODES_JSON__;
const KNOWLEDGE_EDGES = __EDGES_JSON__;

const LAYER_CONFIG = {
  sovereignty:  { y:  45, radius: 32, color: 0xDC143C, name: '主权层·朱雀', beast: '朱雀' },
  governance:   { y:  15, radius: 26, color: 0x2E8B57, name: '治理层·青龙', beast: '青龙' },
  mechanism:    { y: -15, radius: 26, color: 0x1E90FF, name: '机制层·玄武', beast: '玄武' },
  foundation:   { y: -45, radius: 32, color: 0xFFD700, name: '基础层·白虎', beast: '白虎' }
};

const NODE_TYPE_SIZE = { ROOT: 3.2, TERM: 1.8, CLAIM: 1.8, COMMITMENT: 1.5, BEHAVIOR: 1.3, MECHANISM: 1.5, FOUNDATION: 1.5 };

let scene, camera, renderer, controls, raycaster, mouse;
let nodeMeshes = [], edgeLines = [], labelSprites = [], layerGroups = {};
let hoveredNode = null, selectedNode = null, autoRotate = false;

function init() {
  const container = document.getElementById('canvas-container');
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0a0f);
  scene.fog = new THREE.FogExp2(0x0a0a0f, 0.0035);

  camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 2000);
  camera.position.set(0, 0, 160);

  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.outputEncoding = THREE.sRGBEncoding;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  container.appendChild(renderer.domElement);

  controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.minDistance = 40;
  controls.maxDistance = 300;
  controls.autoRotate = false;
  controls.autoRotateSpeed = 0.6;

  raycaster = new THREE.Raycaster();
  mouse = new THREE.Vector2();

  setupLights();
  createStarField();
  createCentralCore();
  buildGraph();

  window.addEventListener('resize', onResize);
  window.addEventListener('mousemove', onMouseMove);
  window.addEventListener('click', onClick);
  window.addEventListener('keydown', onKeyDown);

  document.getElementById('search').addEventListener('input', onSearch);
  document.querySelector('#detail .close').addEventListener('click', closeDetail);

  document.getElementById('node-count').textContent = KNOWLEDGE_NODES.nodes.length;
  document.getElementById('edge-count').textContent = KNOWLEDGE_EDGES.edges.length;

  setTimeout(() => document.getElementById('loader').classList.add('hidden'), 900);
  document.getElementById('help').classList.add('open');
  setTimeout(() => document.getElementById('help').classList.remove('open'), 6000);

  animate();
}

function setupLights() {
  scene.add(new THREE.AmbientLight(0x404060, 1.2));
  const centerLight = new THREE.PointLight(0xFFD700, 1.5, 250);
  centerLight.position.set(0, 0, 0);
  scene.add(centerLight);

  Object.values(LAYER_CONFIG).forEach((cfg, i) => {
    const light = new THREE.PointLight(cfg.color, 0.7, 120);
    light.position.set(0, cfg.y, 0);
    scene.add(light);
  });

  const rim = new THREE.DirectionalLight(0xa78bfa, 0.5);
  rim.position.set(80, 60, 100);
  scene.add(rim);
}

function createStarField() {
  const count = 2500;
  const geom = new THREE.BufferGeometry();
  const pos = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  const palette = [new THREE.Color(0xFFD700), new THREE.Color(0xa78bfa), new THREE.Color(0x60a5fa), new THREE.Color(0xffffff)];
  for (let i = 0; i < count; i++) {
    const r = 180 + Math.random() * 400;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    pos[i*3] = r * Math.sin(phi) * Math.cos(theta);
    pos[i*3+1] = r * Math.sin(phi) * Math.sin(theta);
    pos[i*3+2] = r * Math.cos(phi);
    const c = palette[Math.floor(Math.random() * palette.length)];
    colors[i*3] = c.r; colors[i*3+1] = c.g; colors[i*3+2] = c.b;
  }
  geom.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  const mat = new THREE.PointsMaterial({ size: 0.7, vertexColors: true, transparent: true, opacity: 0.8 });
  scene.add(new THREE.Points(geom, mat));
}

function createCentralCore() {
  const group = new THREE.Group();
  const coreMat = new THREE.MeshPhysicalMaterial({
    color: 0x8B4513, emissive: 0xFFD700, emissiveIntensity: 0.25,
    metalness: 0.7, roughness: 0.25, clearcoat: 1.0
  });
  group.add(new THREE.Mesh(new THREE.SphereGeometry(4.5, 48, 48), coreMat));

  const ringMat = new THREE.MeshBasicMaterial({ color: 0xFFD700, transparent: true, opacity: 0.25, side: THREE.DoubleSide });
  const ring1 = new THREE.Mesh(new THREE.RingGeometry(7, 7.6, 64), ringMat);
  ring1.rotation.x = Math.PI / 2;
  group.add(ring1);
  const ring2 = new THREE.Mesh(new THREE.RingGeometry(9, 9.4, 64), ringMat);
  ring2.rotation.x = Math.PI / 3;
  group.add(ring2);

  scene.add(group);
}

function buildGraph() {
  const nodes = KNOWLEDGE_NODES.nodes;
  const edges = KNOWLEDGE_EDGES.edges;
  const nodeMap = {};

  nodes.forEach(n => { nodeMap[n.node_id] = n; });

  Object.keys(LAYER_CONFIG).forEach(layer => { layerGroups[layer] = new THREE.Group(); scene.add(layerGroups[layer]); });

  // Position nodes per layer
  const layerNodes = {};
  Object.keys(LAYER_CONFIG).forEach(l => layerNodes[l] = []);
  nodes.forEach(n => { if (LAYER_CONFIG[n.layer]) layerNodes[n.layer].push(n); });

  Object.entries(layerNodes).forEach(([layer, list]) => {
    const cfg = LAYER_CONFIG[layer];
    const root = list.find(n => n.node_type === 'ROOT') || list[0];
    const others = list.filter(n => n !== root);

    // root at center of layer
    placeNode(root, 0, cfg.y, 0, cfg);

    // others distributed around root via Fibonacci sphere
    const count = others.length;
    const golden = Math.PI * (3 - Math.sqrt(5));
    others.forEach((n, i) => {
      const yOff = 1 - (i / (count - 1 || 1)) * 2;
      const radius = Math.sqrt(1 - yOff * yOff);
      const theta = golden * i;
      const x = cfg.radius * radius * Math.cos(theta);
      const z = cfg.radius * radius * Math.sin(theta);
      const y = cfg.y + yOff * (cfg.radius * 0.45);
      placeNode(n, x, y, z, cfg);
    });
  });

  // Edges
  const lineMat = new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.55 });
  edges.forEach(e => {
    const s = nodeMap[e.source], t = nodeMap[e.target];
    if (!s || !t || !s.__mesh || !t.__mesh) return;
    const geom = new THREE.BufferGeometry().setFromPoints([s.__mesh.position, t.__mesh.position]);
    const sc = new THREE.Color(LAYER_CONFIG[s.layer].color);
    const tc = new THREE.Color(LAYER_CONFIG[t.layer].color);
    const colors = new Float32Array([sc.r, sc.g, sc.b, tc.r, tc.g, tc.b]);
    geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    const line = new THREE.Line(geom, lineMat.clone());
    line.userData = { edge: e, sourceNode: s, targetNode: t };
    edgeLines.push(line);
    scene.add(line);
  });
}

function placeNode(node, x, y, z, cfg) {
  const size = NODE_TYPE_SIZE[node.node_type] || 1.4;
  const geometry = new THREE.SphereGeometry(size, 32, 32);
  const material = new THREE.MeshPhysicalMaterial({
    color: cfg.color,
    emissive: cfg.color,
    emissiveIntensity: 0.15,
    metalness: 0.55,
    roughness: 0.35,
    clearcoat: 0.6,
    clearcoatRoughness: 0.2
  });
  const mesh = new THREE.Mesh(geometry, material);
  mesh.position.set(x, y, z);
  mesh.userData = { node: node, originalColor: cfg.color, layerConfig: cfg };
  node.__mesh = mesh;
  nodeMeshes.push(mesh);
  layerGroups[node.layer].add(mesh);

  const label = createLabelSprite(node.name, 0xe4e4e7, node.node_type === 'ROOT' ? 22 : 14);
  label.position.set(x, y + size + 2.5, z);
  label.userData = { node: node };
  labelSprites.push(label);
  layerGroups[node.layer].add(label);
}

function createLabelSprite(text, colorHex, fontSize) {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  const font = `${fontSize}px 'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif`;
  ctx.font = font;
  const metrics = ctx.measureText(text);
  const w = Math.ceil(metrics.width) + 16;
  const h = fontSize + 12;
  canvas.width = w;
  canvas.height = h;
  ctx.font = font;
  ctx.fillStyle = '#' + colorHex.toString(16).padStart(6, '0');
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.shadowColor = 'rgba(0,0,0,0.85)';
  ctx.shadowBlur = 4;
  ctx.fillText(text, w/2, h/2);
  const texture = new THREE.CanvasTexture(canvas);
  const spriteMat = new THREE.SpriteMaterial({ map: texture, transparent: true, opacity: 0.92 });
  const sprite = new THREE.Sprite(spriteMat);
  sprite.scale.set(w * 0.12, h * 0.12, 1);
  return sprite;
}

function onMouseMove(e) {
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(nodeMeshes);
  const tooltip = document.getElementById('tooltip');

  if (intersects.length > 0) {
    const node = intersects[0].object.userData.node;
    hoveredNode = intersects[0].object;
    document.body.style.cursor = 'pointer';
    tooltip.style.opacity = 1;
    tooltip.style.left = (e.clientX + 14) + 'px';
    tooltip.style.top = (e.clientY + 14) + 'px';
    tooltip.querySelector('.tt-title').textContent = node.name;
    tooltip.querySelector('.tt-meta').textContent = `${node.node_type} · ${LAYER_CONFIG[node.layer].name} · ${node.dna}`;
  } else {
    hoveredNode = null;
    document.body.style.cursor = 'default';
    tooltip.style.opacity = 0;
  }
}

function onClick(e) {
  if (hoveredNode) {
    selectNode(hoveredNode.userData.node);
  } else if (!e.target.closest('#detail') && !e.target.closest('#hud')) {
    closeDetail();
  }
}

function selectNode(node) {
  selectedNode = node;
  const mesh = node.__mesh;
  const targetPos = mesh.position.clone();
  const offset = camera.position.clone().sub(controls.target).normalize().multiplyScalar(45);
  const endPos = targetPos.clone().add(offset);

  // simple tween target
  controls.target.copy(targetPos);
  camera.position.copy(endPos);

  showDetail(node);
}

function showDetail(node) {
  const panel = document.getElementById('detail');
  const content = document.getElementById('detail-content');
  document.getElementById('detail-title').textContent = node.name;

  const severityColor = { critical: '🔴', high: '🟠', medium: '🟡', low: '🟢' }[node.properties?.severity] || '⚪';
  let html = `<span class="tag">${node.node_type} · ${LAYER_CONFIG[node.layer].name}</span>`;
  html += `<div class="field"><div class="field-label">描述</div><div class="field-value">${node.description || '-'}</div></div>`;
  html += `<div class="field"><div class="field-label">DNA</div><div class="field-value dna">${node.dna}</div></div>`;
  html += `<div class="field"><div class="field-label">状态 / 版本</div><div class="field-value">${node.state || '-'} / ${node.version || '-'}</div></div>`;

  if (node.properties && Object.keys(node.properties).length) {
    html += `<div class="field"><div class="field-label">变量属性 properties</div><table><tr><th>Key</th><th>Value</th></tr>`;
    Object.entries(node.properties).forEach(([k, v]) => {
      html += `<tr><td>${k}</td><td>${JSON.stringify(v)}</td></tr>`;
    });
    html += `</table></div>`;
  }

  const related = KNOWLEDGE_EDGES.edges.filter(e => e.source === node.node_id || e.target === node.node_id);
  html += `<div class="field"><div class="field-label">关联关系（${related.length}）</div><div id="edges-list">`;
  related.forEach(e => {
    const isSrc = e.source === node.node_id;
    const other = isSrc ? e.target : e.source;
    const otherNode = KNOWLEDGE_NODES.nodes.find(n => n.node_id === other);
    html += `<div class="edge-row"><b>${isSrc ? '→' : '←'}</b> ${e.relation} <b>${otherNode ? otherNode.name : other}</b><br><span style="color:#64748b">${e.description || ''}</span></div>`;
  });
  html += `</div></div>`;

  content.innerHTML = html;
  panel.classList.add('open');
}

function closeDetail() {
  document.getElementById('detail').classList.remove('open');
  selectedNode = null;
}

function onSearch(e) {
  const q = e.target.value.trim().toLowerCase();
  nodeMeshes.forEach(mesh => {
    const node = mesh.userData.node;
    const hay = `${node.name} ${node.description} ${JSON.stringify(node.properties)} ${node.dna}`.toLowerCase();
    const match = !q || hay.includes(q);
    mesh.material.opacity = match ? 1 : 0.18;
    mesh.material.transparent = true;
    mesh.visible = match;
  });
  labelSprites.forEach(sprite => {
    const node = sprite.userData.node;
    const hay = `${node.name} ${node.description} ${JSON.stringify(node.properties)} ${node.dna}`.toLowerCase();
    sprite.visible = (!q || hay.includes(q));
  });
}

function onKeyDown(e) {
  if (e.target.tagName === 'INPUT') return;
  if (e.key === 'h' || e.key === 'H') {
    document.getElementById('help').classList.toggle('open');
  } else if (e.key === 'r' || e.key === 'R') {
    controls.target.set(0, 0, 0);
    camera.position.set(0, 0, 160);
    closeDetail();
  } else if (e.key === 'f' || e.key === 'F') {
    autoRotate = !autoRotate;
    controls.autoRotate = autoRotate;
  }
}

function onResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}

function toggleAutoRotate() {
  autoRotate = !autoRotate;
  controls.autoRotate = autoRotate;
  document.getElementById('btn-rotate').textContent = autoRotate ? '⏸ 暂停' : '⏵ 旋转';
}
function resetView() {
  controls.target.set(0, 0, 0);
  camera.position.set(0, 0, 160);
  closeDetail();
}
function toggleFullscreen() {
  if (!document.fullscreenElement) document.documentElement.requestFullscreen();
  else document.exitFullscreen();
}
function toggleHelp() {
  document.getElementById('help').classList.toggle('open');
}

function animate() {
  requestAnimationFrame(animate);
  controls.update();

  // gentle floating of layers
  Object.values(layerGroups).forEach((g, i) => {
    g.rotation.y += 0.0006 * (i % 2 === 0 ? 1 : -1);
  });

  // hover emissive pulse
  nodeMeshes.forEach(mesh => {
    const isHover = hoveredNode === mesh;
    mesh.material.emissiveIntensity = isHover ? 0.6 : 0.15;
  });

  renderer.render(scene, camera);
}

init();
</script>
</body>
</html>
'''

def build():
    nodes_json = (NODES_FILE).read_text(encoding='utf-8')
    edges_json = (EDGES_FILE).read_text(encoding='utf-8')

    FONT_DEST_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(FONT_SRC, FONT_DEST_DIR / FONT_SRC.name)

    HTML_PATH.parent.mkdir(parents=True, exist_ok=True)
    html = HTML_TEMPLATE.replace('{dna}', DNA).replace('{confirm}', CONFIRM).replace('{gpg}', GPG)
    html = html.replace('__NODES_JSON__', nodes_json)
    html = html.replace('__EDGES_JSON__', edges_json)
    HTML_PATH.write_text(html, encoding='utf-8')
    print(f'[ok] {HTML_PATH}')
    print(f'[ok] font copied to {FONT_DEST_DIR / FONT_SRC.name}')

if __name__ == '__main__':
    build()
