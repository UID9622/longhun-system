#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-08-30-丙午·丙申·丙子·未时-TOPOLOGY-VIEWER-v1.1-BUILD-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂 · 拓扑可视化构建器 v1.1
────────────────────────────────────────────
读取 .codebuddy/longhun_neural_net.json，生成三端可用的离线单页应用：
  web/topology-viewer/index.html            ← 单页应用（内嵌数据·可离线）
  web/topology-viewer/sw.js                 ← Service Worker（PWA 真离线缓存）
  web/topology-viewer/manifest.webmanifest  ← PWA 清单
  web/topology-viewer/icon.svg              ← 龍字印章图标（矢量）
  web/topology-viewer/icon-{180,192,512}.png ← 位图图标（iOS/鸿蒙主屏必需）

v1.1 审计修复（2026-08-30）:
  - 前端: 删死代码·边图改为按真实 edges 自适应同心环布局·全段 try/catch 错误边界（单模块失败不再白屏）·引擎状态判空
  - PWA:  注册 Service Worker（真离线）·生成 PNG 位图图标（Safari 不认 SVG 主屏图标）·manifest 图标补全
  - 流程: 内置拓扑契约校验（缺字段即 🔴 拒绝产出）·转换器自动探测（rsvg-convert/magick/qlmanage）

v1.2 结构补全（2026-08-30·老大指令"审查完善结构·自动补全区块"）:
  - 新增 sec-security「安全 · 语义盾 · 三色审计」: 语义防火墙 5 文件 · 三色审计规则 · 红线清单 · 扫描即修复(P77) · DNA 时间轴 L0-L4
  - 新增 sec-runtime「系统运行时 · 自动化守护」: 健康三色 · 每小时自愈 · 记忆加载 · 算力瘦身 · 环境状态 —— 突出自动化
  - footer 补 GPG 指纹 · 确认码 · 分层许可（CC BY-NC-SA 4.0 / MulanPSL v2）
  - 数据契约 11 必填字段 → 页面区块全覆盖（原 runtime_state 仅头部健康计数·无独立区块）

v1.3 3D 递进 + 交互接口（2026-08-30·老大指令"神经网络不该是3D的吗·层层递进·留接口"）:
  - 3D 穹顶: 九层同心壳（L0 内核→L9 外壳）·纯 CSS 3D（perspective+preserve-3d+translateZ）·零外联·自动缓旋·悬停暂停·移动端自适应缩放
  - 层层递进: 「▶ 层层递进动画」逐层弹出（0.22s 级联）·环=层·光点=真实模块（architecture.layers.content）
  - 交互接口: ①点击层/光点 → 层详情浮层（palace/role/content/锚点）②模式切换 3D穹顶↔平面边图 ③区块互钻 xref（各 section 标题旁 ↗关联链）④header 健康三色点击 → 跳 sec-runtime
  - Service Worker 缓存号 bump（防旧缓存白屏）· 边图 2D 保留为第二模式

v1.4 3D 银河星系 + 联动公式（2026-08-30·老大指令"神经网络该像银河系·每颗星球主打专业技能·联动有计算公式"）:
  - 形态升级: 3D 穹顶 → 3D 银河星系（黄金角 137.508° 斐波那契螺旋布星·银心=UID9622 龙核·9 星团=九层·星球=真实模块）
  - 星球=模块: 每颗星球按数字根→五行着色（金白金/木青绿/水深蓝/火朱红/土琥珀）·悬停显示名字+五行·点击出层详情
  - 联动=公式（零黑箱·全公开）: 点两颗星球 → 联动计算面板全链路 ①数字根 ②五行映射 ③五行关系系数 ④洛书亲和 ⑤数字根对称 ⑥W=0.60×③+0.25×④+0.15×⑤ ⑦三色判定（数字根3/9熔断）
  - 公式锚点: bin/lh_wuxing_core.py v3.0（五行生克表）· bin/lh_digital_root.py v1.0（数字根引擎）· 洛书369(sn=369) · 公式公示卡入页
  - 层层递进保留: 「▶ 层层递进动画」星团 L0→L9 级联弹出 · 平面边图仍为第二模式

v1.5 全集成银河 · 3D 拖拽 · 星爆（2026-08-30·老大指令"这就是主力引擎·全部集成进去·3D可拖拽·还能播爆"）:
  - 全集成: 银河系 = 全系统 3D 全景（14 星域: 九层 L0-L8 + 引擎域 + 技能域 + 人格域 + 数字人域 + 生态域）
  - 星域=星团: 层团=真实模块星 · 引擎域=状态分组星云球(全部引擎可查) · 技能域=9分类星云球 · 人格域=20人格星 · 数字人域=7星 · 生态域=4层级星云球
  - 3D 拖拽: 鼠标/触屏自由旋转（绕 X/Y 轴）· JS rAF 自动旋转（拖拽暂停 · 🔄 按钮开关）
  - 星爆脉冲: 💥 一键引爆全星系（星球炸散成星尘 → 再聚拢）· 银心同步膨胀
  - 联动公式: 任意两颗星 → 联动计算面板（数字根→五行→关系系数→洛书亲和→对称度→加权 W→三色）
  - 零外联: 纯 CSS 3D + JS · 离线可用 · 层层递进动画保留 · 平面边图为第二模式

用法:
  python3 bin/lh_topology_viewer_build.py
  可选: --json <path> --out <dir>

配套:
  bin/lh_topology_verify.py   产物校验（三色）
  bin/lh_topology_publish.sh  一键 构建→校验→打包→签名→部署
  bin/lh_topology_make_dmg.sh macOS dmg 打包
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_JSON = ROOT / ".codebuddy" / "longhun_neural_net.json"
DEFAULT_OUT = ROOT / "web" / "topology-viewer"

VERSION = "v1.5"

# ── 拓扑契约（build 前强校验，缺字段 🔴 拒绝产出 ─────────────────
REQUIRED_TOP = [
    "architecture", "persona_matrix", "neural_edges", "skill_bus",
    "digital_humans", "ecosystem", "gates", "human_nature_dimensions",
    "thinking_cycle", "runtime_state", "_meta",
]
REQUIRED_ARCH = [
    "L0_神圣层", "L1_内核层", "L2_技能层", "L3_路由层", "L4_闸门层",
    "L5_服务层", "L6_集成层", "L7_数据层", "L8_治理层",
]

# ══════════════════════════════════════════════════════════════
# 图标（龍字印章·SVG）
# ══════════════════════════════════════════════════════════════
ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="96" fill="#0a0e14"/>
  <rect x="24" y="24" width="464" height="464" rx="72" fill="none" stroke="#c9a227" stroke-width="10"/>
  <text x="256" y="330" font-family="Songti SC, STSong, SimSun, serif" font-size="290" font-weight="700" fill="#c9a227" text-anchor="middle">龍</text>
  <text x="256" y="450" font-family="sans-serif" font-size="40" letter-spacing="14" fill="#e8e8e8" text-anchor="middle">LONGHUN</text>
</svg>"""

# ── Service Worker（PWA 真离线缓存）─────────────────────────────
SW_JS = """// 龍魂拓扑 · Service Worker v1.1 · 离线缓存
const C = 'longhun-topology-v1.5';
const ASSETS = ['./', './index.html', './manifest.webmanifest',
  './icon.svg', './icon-180.png', './icon-192.png', './icon-512.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(C).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== C).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then(r => r || fetch(e.request).then(res => {
      const cp = res.clone();
      caches.open(C).then(c => c.put(e.request, cp));
      return res;
    }).catch(() => caches.match('./index.html')))
  );
});
"""

# ══════════════════════════════════════════════════════════════
# HTML 模板
# ══════════════════════════════════════════════════════════════
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="龍魂拓扑">
<meta name="theme-color" content="#0a0e14">
<meta name="description" content="龍魂系统神经网络拓扑总览 · L0-L9 九层架构 · 人格矩阵 · 三端离线可用">
<title>龍魂拓扑 · 神经网络全览</title>
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="apple-touch-icon" sizes="192x192" href="icon-192.png">
<link rel="apple-touch-icon" sizes="512x512" href="icon-512.png">
<style>
:root{
  --bg:#0a0e14; --bg2:#0f1520; --card:#121a28; --card2:#0c1220;
  --line:#1e2a3a; --gold:#c9a227; --gold2:#e8c95a; --ink:#e8e8e8;
  --sub:#8fa3b8; --dim:#5c6f82; --green:#37c871; --yellow:#e0b64a; --red:#e5484d;
  --serif:"Songti SC","STSong",Georgia,serif; --mono:"SF Mono",Menlo,monospace;
}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Noto Sans CJK SC",sans-serif;line-height:1.6;overflow-x:hidden}
a{color:var(--gold);text-decoration:none}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px 80px}
/* 头部 */
header{padding:40px 0 8px;text-align:center}
.dna-chip{display:inline-flex;gap:10px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:999px;padding:8px 18px;font-family:var(--mono);font-size:12px;color:var(--sub)}
h1{font-family:var(--serif);font-size:44px;letter-spacing:6px;color:var(--gold);margin:22px 0 4px;text-shadow:0 0 40px rgba(201,162,39,.25)}
.sub{color:var(--sub);font-size:15px}
.health{display:flex;gap:14px;justify-content:center;margin:18px 0 4px;font-family:var(--mono);font-size:13px}
.health b{font-weight:700}
.g{color:var(--green)} .y{color:var(--yellow)} .r{color:var(--red)}
.nav{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:26px 0 34px}
.nav button{background:var(--card);border:1px solid var(--line);color:var(--sub);border-radius:999px;padding:8px 16px;font-size:13px;cursor:pointer;transition:.2s}
.nav button.on{background:var(--gold);border-color:var(--gold);color:#0a0e14;font-weight:600}
.nav button:hover{border-color:var(--gold);color:var(--gold)}
section{display:none;animation:fade .35s ease}
section.on{display:block}
@keyframes fade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.sec-title{font-family:var(--serif);font-size:26px;color:var(--gold);margin:10px 0 6px;letter-spacing:3px}
.sec-sub{color:var(--dim);font-size:13px;margin-bottom:22px}
/* 通用卡片 */
.grid{display:grid;gap:14px}
.c2{grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}
.c3{grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
.c4{grid-template-columns:repeat(auto-fit,minmax(180px,1fr))}
.card{background:linear-gradient(160deg,var(--card),var(--card2));border:1px solid var(--line);border-radius:14px;padding:16px 18px;transition:.2s}
.card:hover{border-color:var(--gold);transform:translateY(-2px)}
.card h3{font-size:15px;color:var(--gold2);margin-bottom:6px}
.card p{font-size:13px;color:var(--sub)}
.card .tag{display:inline-block;font-family:var(--mono);font-size:11px;background:#1a2434;border:1px solid var(--line);color:var(--sub);border-radius:6px;padding:2px 8px;margin:4px 6px 0 0}
.card.warn{border-color:var(--yellow)}
/* 九宫格 */
.luosh{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:780px;margin:0 auto}
.luo{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 16px;text-align:center;position:relative;min-height:120px;transition:.2s}
.luo:hover{border-color:var(--gold);transform:translateY(-2px)}
.luo .p{font-family:var(--serif);font-size:34px;color:var(--gold);opacity:.9}
.luo .n{font-size:13px;color:var(--gold2);margin:6px 0 2px}
.luo .d{font-size:11px;color:var(--dim);line-height:1.5}
.luo.center{background:radial-gradient(circle at 50% 30%,rgba(201,162,39,.16),transparent 70%),var(--card);border-color:var(--gold);box-shadow:0 0 60px rgba(201,162,39,.12)}
/* 人格 */
.persona{display:flex;gap:10px;align-items:flex-start}
.persona .id{font-family:var(--mono);font-size:13px;color:var(--gold);background:#1a2434;border:1px solid var(--line);border-radius:8px;padding:6px 9px;white-space:nowrap}
.persona .nm{font-size:14px;color:var(--ink);font-weight:600}
.persona .wt{font-family:var(--mono);font-size:11px;color:var(--dim)}
.persona .rl{font-size:12px;color:var(--sub);margin-top:2px}
/* 边图 */
#edgeSvg{width:100%;height:auto;display:block;background:radial-gradient(circle at 50% 45%,rgba(201,162,39,.05),transparent 60%)}
.edge{stroke:#2a3a4e;stroke-width:1.2;fill:none}
.edge.hot{stroke:var(--gold);stroke-opacity:.55}
.node circle{fill:#16202e;stroke:var(--line)}
.node.hot circle{fill:#1a2434;stroke:var(--gold)}
.node text{fill:var(--sub);font-size:10px;font-family:var(--mono)}
.node.hot text{fill:var(--gold2)}
.legend{display:flex;gap:16px;justify-content:center;font-size:12px;color:var(--dim);margin-top:8px}
.legend i{display:inline-block;width:14px;height:3px;vertical-align:middle;margin-right:4px}
/* 3D 穹顶（v1.3 层层递进 · 纯 CSS 零外联） */
#domeWrap{position:relative;height:560px;perspective:1300px;overflow:hidden;border-radius:14px;border:1px solid var(--line);background:radial-gradient(circle at 50% 40%,rgba(201,162,39,.07),transparent 65%),var(--card2)}
#domeScene{position:absolute;left:50%;top:50%;width:0;height:0;transform-style:preserve-3d;cursor:grab;transform:rotateX(-18deg) rotateY(0);will-change:transform}
#domeScene.grabbing{cursor:grabbing}
.shell{position:absolute;transform-style:preserve-3d;transform:translateZ(var(--z,0))}
.shell .ring{position:absolute;inset:0;border:1px solid rgba(201,162,39,.28);border-radius:50%;box-shadow:0 0 34px rgba(201,162,39,.07)}
.shell .dot{position:absolute;width:9px;height:9px;margin:-4.5px 0 0 -4.5px;border-radius:50%;background:var(--gold);box-shadow:0 0 12px rgba(201,162,39,.85);cursor:pointer;transition:.2s}
.shell .dot:hover{background:#fff;transform:scale(1.7)}
.shell .lab{position:absolute;font-family:var(--mono);font-size:10px;color:var(--sub);white-space:nowrap;transform:translate(-50%,-150%);cursor:pointer;padding:3px 8px;border-radius:999px;background:rgba(10,14,20,.75);border:1px solid var(--line)}
.shell .lab:hover{color:var(--gold2);border-color:var(--gold)}
@keyframes layerPop{from{opacity:0;transform:translate(var(--cx,0px),var(--cy,0px)) translateZ(var(--cz,0px)) scale(.2)}to{opacity:1;transform:translate(var(--cx,0px),var(--cy,0px)) translateZ(var(--cz,0px)) scale(1)}}
.cluster.pop{animation:layerPop .6s cubic-bezier(.17,.9,.32,1.25) both}
/* 银河系（v1.4 · 星球=模块 · 联动=公式 · 零黑箱） */
#galCore{position:absolute;left:-44px;top:-44px;width:88px;height:88px;border-radius:50%;
  background:radial-gradient(circle,#fffbe6 0%,#ffd76a 32%,rgba(201,162,39,.3) 68%,transparent 74%);
  box-shadow:0 0 44px rgba(255,215,106,.65),0 0 130px rgba(255,215,106,.28);
  animation:corePulse 3.2s ease-in-out infinite}
#galCore .lab{position:absolute;left:50%;top:100%;transform:translateX(-50%);margin-top:12px;
  font-family:var(--mono);font-size:11px;color:var(--gold2);white-space:nowrap}
@keyframes corePulse{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.16);opacity:.86}}
.cluster{position:absolute;left:0;top:0;transform-style:preserve-3d;transform:translate(var(--cx,0px),var(--cy,0px)) translateZ(var(--cz,0px))}
.cluster .halo{position:absolute;left:50%;top:50%;border-radius:50%;
  border:1px dashed rgba(201,162,39,.2);box-shadow:inset 0 0 36px rgba(201,162,39,.06)}
.cluster .lab{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);font-family:var(--mono);
  font-size:10px;color:var(--dim);white-space:nowrap;pointer-events:none;z-index:2;text-shadow:0 0 8px rgba(10,14,20,.9)}
.cluster.hot .lab{color:var(--gold2)}
.star{position:absolute;width:var(--sz,11px);height:var(--sz,11px);margin:calc(var(--sz,11px)/-2) 0 0 calc(var(--sz,11px)/-2);
  border-radius:50%;background:var(--sc,#e6c56a);box-shadow:0 0 10px var(--sc,#e6c56a),0 0 22px var(--sc,#e6c56a);
  cursor:pointer;transition:.18s}
.star:hover{transform:scale(1.7);z-index:5}
.star.sel{outline:2px solid #fff;outline-offset:2px;z-index:6;animation:starSel .9s ease-in-out infinite}
@keyframes starSel{50%{outline-color:var(--gold)}}
.star .lab{position:absolute;left:50%;bottom:135%;transform:translateX(-50%);font-family:var(--mono);font-size:9px;
  color:var(--sub);white-space:nowrap;background:rgba(10,14,20,.82);padding:2px 6px;border-radius:6px;
  border:1px solid var(--line);opacity:0;transition:.15s;pointer-events:none;max-width:150px;overflow:hidden;text-overflow:ellipsis}
.star:hover .lab{opacity:1}
.star.sel .lab{opacity:1;color:var(--gold2);border-color:var(--gold)}
/* 联动公式公示表 */
.frm{width:100%;border-collapse:collapse;font-size:12px;margin-top:8px}
.frm td{border:1px solid var(--line);padding:7px 10px;vertical-align:top}
.frm td:first-child{color:var(--gold2);white-space:nowrap;font-family:var(--mono)}
/* 星云球（聚合体·引擎/技能/生态域成员） */
.nova{box-shadow:0 0 14px var(--sc),0 0 38px var(--sc)}
.cluster .lab small{display:block;font-size:9px;color:var(--dim);text-align:center;font-weight:400}
/* 星爆脉冲（v1.5） */
.star.boom{animation:starBoom 1.3s cubic-bezier(.19,1,.22,1) forwards}
.star.boom:hover{transform:none}
.star.unboom{animation:starUnboom 1.3s cubic-bezier(.19,1,.22,1) forwards}
@keyframes starBoom{to{transform:translate(var(--bx,0px),var(--by,0px)) scale(.3);opacity:.3}}
@keyframes starUnboom{from{transform:translate(var(--bx,0px),var(--by,0px)) scale(.3);opacity:.3}to{transform:translate(0,0) scale(1);opacity:1}}
.cluster.boom{animation:clusterBoom 1.3s cubic-bezier(.19,1,.22,1) forwards}
.cluster.unboom{animation:clusterUnboom 1.3s cubic-bezier(.19,1,.22,1) forwards}
@keyframes clusterBoom{to{transform:translate(calc(var(--cx,0px) + var(--dx,0px)),calc(var(--cy,0px) + var(--dy,0px))) translateZ(calc(var(--cz,0px) + var(--dz,0px))) scale(1.06)}}
@keyframes clusterUnboom{from{transform:translate(calc(var(--cx,0px) + var(--dx,0px)),calc(var(--cy,0px) + var(--dy,0px))) translateZ(calc(var(--cz,0px) + var(--dz,0px))) scale(1.06)}to{transform:translate(var(--cx,0px),var(--cy,0px)) translateZ(var(--cz,0px)) scale(1)}}
#galCore.boom{animation:coreBoom 1.3s cubic-bezier(.19,1,.22,1) forwards}
#galCore.unboom{animation:coreUnboom 1.3s cubic-bezier(.19,1,.22,1) forwards}
@keyframes coreBoom{to{transform:scale(2.6);opacity:.35}}
@keyframes coreUnboom{from{transform:scale(2.6);opacity:.35}to{transform:scale(1);opacity:1}}
@media(max-width:640px){#domeWrap{height:420px}}
.domebar{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin:14px 0 16px}
.domebar button{background:var(--card);border:1px solid var(--line);color:var(--sub);border-radius:999px;padding:8px 16px;font-size:13px;cursor:pointer;transition:.2s}
.domebar button.on{background:var(--gold);border-color:var(--gold);color:#0a0e14;font-weight:600}
.domebar button:hover{border-color:var(--gold);color:var(--gold)}
.mode{display:none}.mode.on{display:block}
/* 层详情浮层 */
#layerModal{position:fixed;inset:0;background:rgba(5,8,12,.74);display:none;align-items:center;justify-content:center;z-index:50;backdrop-filter:blur(4px)}
#layerModal.on{display:flex}
#layerModal .box{max-width:560px;width:92%;max-height:80vh;overflow:auto;background:linear-gradient(160deg,var(--card),var(--card2));border:1px solid var(--gold);border-radius:16px;padding:22px 24px;box-shadow:0 0 90px rgba(201,162,39,.18)}
#layerModal .box h3{font-family:var(--serif);color:var(--gold);font-size:20px;margin-bottom:10px}
#layerModal .close{float:right;cursor:pointer;color:var(--dim);font-size:18px}
#layerModal .close:hover{color:var(--gold)}
/* 区块互钻 */
.xref{display:inline-flex;gap:8px;flex-wrap:wrap;margin-left:12px;vertical-align:middle}
.xref button{background:transparent;border:1px dashed var(--line);color:var(--sub);border-radius:999px;padding:2px 10px;font-size:11px;cursor:pointer;transition:.2s}
.xref button:hover{border-color:var(--gold);color:var(--gold)}
/* 引擎 */
.search{width:100%;max-width:480px;background:var(--card);border:1px solid var(--line);color:var(--ink);border-radius:999px;padding:11px 20px;font-size:14px;outline:none;margin-bottom:18px}
.search:focus{border-color:var(--gold)}
.eng{border-left:3px solid var(--gold)}
.eng.dep{border-left-color:var(--dim);opacity:.55}
.eng.shelved{border-left-color:var(--yellow)}
/* 数字人 */
.dh .no{font-family:var(--mono);font-size:11px;color:var(--dim)}
/* 生态 */
.tier{display:flex;justify-content:space-between;align-items:baseline}
.tier .price{font-family:var(--mono);color:var(--gold)}
/* 闸门流 */
.gates{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:center}
.gate{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px;min-width:170px}
.gate .gn{font-family:var(--serif);color:var(--gold);font-size:15px}
.gate .gr{font-family:var(--mono);font-size:11px;color:var(--dim);margin-top:4px}
.arrow{color:var(--dim);font-size:18px}
/* 阶段 */
.stage{display:flex;gap:14px;padding:12px 0;border-bottom:1px dashed var(--line)}
.stage .sn{font-family:var(--serif);color:var(--gold);font-size:16px;min-width:28px}
/* 搜索框下计数 */
.count{font-family:var(--mono);font-size:12px;color:var(--dim);margin-bottom:12px}
/* 页脚 */
footer{margin-top:50px;padding-top:22px;border-top:1px solid var(--line);text-align:center;color:var(--dim);font-size:12px}
footer .stamp{font-family:var(--mono);margin-top:6px;color:var(--sub)}
/* 响应式 */
@media(max-width:640px){
  h1{font-size:30px;letter-spacing:3px}
  .dna-chip{font-size:10px;flex-wrap:wrap;justify-content:center}
  .luosh{grid-template-columns:repeat(3,1fr);gap:8px}
  .luo{min-height:96px;padding:12px 8px}
  .luo .p{font-size:24px}
  .nav button{padding:6px 12px;font-size:12px}
}
</style>
</head>
<body>
<div class="wrap">

<header>
  <div class="dna-chip" id="dnaChip">#龍芯⚡️TOPOLOGY-v4.0 · UID9622 · 龍芯北辰</div>
  <h1>龍魂 · 神经网络拓扑</h1>
  <div class="sub">L0-L9 九层架构 · 洛书九宫骨架 · 三色审计 · 全链可追溯</div>
  <div class="health" id="healthLine"></div>
  <div class="nav" id="navBar"></div>
</header>

<section id="sec-arch" class="on">
  <h2 class="sec-title">九层架构 · 洛书九宫</h2>
  <p class="sec-sub">中宫为根，八方为翼。每一层皆锚定洛书方位，不可错位。</p>
  <div class="luosh" id="luoshGrid"></div>
</section>

<section id="sec-persona">
  <h2 class="sec-title">人格矩阵</h2>
  <p class="sec-sub" id="personaStat"></p>
  <div class="grid c2" id="personaGrid"></div>
  <h3 style="margin:26px 0 10px;color:var(--gold2);font-size:17px">应用人格小队</h3>
  <div class="grid c2" id="teamGrid"></div>
</section>

<section id="sec-neural">
  <h2 class="sec-title">神经网络 · 3D 层层递进</h2>
  <p class="sec-sub">九层同心 · L0 内核 → L9 外壳 · 环=层 · 光点=真实模块 · 点按层名或光点查看详情</p>
  <div class="domebar">
    <button id="btn3d" class="on">🌌 3D 银河星系</button>
    <button id="btn2d">🗺 平面边图</button>
    <button id="btnPop">▶ 层层递进动画</button>
    <button id="btnRotate">🔄 自动旋转</button>
    <button id="btnBoom">💥 星爆脉冲</button>
  </div>
  <div class="mode on" id="mode3d">
    <div id="domeWrap"><div id="domeScene"></div></div>
    <div class="legend">
      <span><i style="background:#e6c56a"></i>金</span><span><i style="background:#7ecb8b"></i>木</span>
      <span><i style="background:#6fb1e8"></i>水</span><span><i style="background:#e8836a"></i>火</span><span><i style="background:#d0a25e"></i>土</span>
      <span>🖱 拖拽旋转 3D · 🌌 14 星域全系统集成 · ⭐ 星球=模块 · 点两颗星球 → 联动计算公式</span>
    </div>
    <div class="card" style="margin-top:14px">
      <h3>🪐 星球联动 · 计算公式（零黑箱 · 全公开 · 可复核）</h3>
      <table class="frm">
        <tr><td>① 数字根</td><td>dr(名) = 提取名内数字 → 反复相加 → 1位(0-9) · 无数字 → 退化取 名长（公开规则）</td></tr>
        <tr><td>② 五行映射</td><td>dr → 五行：1/6=水 · 2/7=火 · 3/8=木 · 4/9=金 · 5/0=土</td></tr>
        <tr><td>③ 五行关系</td><td>比和=0.85 · 相生=1.00 · 相泄=0.75 · 相克=0.55 · 相耗=0.65 · 混合=0.70</td></tr>
        <tr><td>④ 洛书亲和</td><td>河图数对 (1-6)(2-7)(3-8)(4-9)(5-0)：同对=1.00 · 不同=0.85</td></tr>
        <tr><td>⑤ 数字根对称</td><td>|drA-drB| → 0:1.00 · 1:0.95 · 2:0.90 · 3:0.80 · ≥4:0.70</td></tr>
        <tr><td>⑥ 联动指数</td><td>W = 0.60×③ + 0.25×④ + 0.15×⑤（公开权重）</td></tr>
        <tr><td>⑦ 三色判定</td><td>W≥0.90 🟢 · 0.75≤W&lt;0.90 🟡 · W&lt;0.75 🔴 · 数字根 3/9 → 熔断标记</td></tr>
      </table>
      <p style="font-size:11px;color:var(--dim);margin-top:8px">锚点: <b>bin/lh_wuxing_core.py v3.0</b>（五行生克表） · <b>bin/lh_digital_root.py v1.0</b>（数字根引擎） · 洛书369（sn=369）· 生: 金→水→木→火→土→金 · 克: 金→木→土→水→火→金</p>
    </div>
  </div>
  <div class="mode" id="mode2d">
    <div class="card" style="background:var(--card2)">
      <svg id="edgeSvg" viewBox="0 0 900 640" role="img" aria-label="龍魂神经网络连接图"></svg>
      <div class="legend"><span><i style="background:var(--gold)"></i>主干边 ≥90%</span><span><i style="background:#2a3a4e"></i>支撑边</span></div>
    </div>
    <div class="grid c3" id="edgeList" style="margin-top:14px"></div>
  </div>
</section>

<section id="sec-engine">
  <h2 class="sec-title">引擎清单</h2>
  <p class="sec-sub">192 个可执行引擎 · 算力瘦身 · 金色左边条=活跃核心</p>
  <input class="search" id="engSearch" placeholder="🔍 搜索引擎名称 / 功能 / 分类…">
  <div class="count" id="engCount"></div>
  <div class="grid c2" id="engGrid"></div>
</section>

<section id="sec-skill">
  <h2 class="sec-title">技能总线</h2>
  <p class="sec-sub" id="skillStat"></p>
  <div class="grid c3" id="skillGrid"></div>
</section>

<section id="sec-digital">
  <h2 class="sec-title">数字人 · 7 联动</h2>
  <p class="sec-sub">数字人 → DNA 登记 → 生态通行证 → 技能总线</p>
  <div class="grid c3" id="dhGrid"></div>
</section>

<section id="sec-eco">
  <h2 class="sec-title">生态 · 四层级</h2>
  <p class="sec-sub" id="ecoStat"></p>
  <div class="grid c2" id="ecoGrid"></div>
</section>

<section id="sec-security">
  <h2 class="sec-title">安全 · 语义盾 · 三色审计</h2>
  <p class="sec-sub">语义防火墙 · 红线清单 · 扫描即修复 · DNA 全链可追溯</p>
  <div class="grid c2" id="shieldGrid"></div>
  <h3 style="margin:26px 0 10px;color:var(--gold2);font-size:17px">红线 · 不可触碰</h3>
  <div class="card" id="redlineList"></div>
  <h3 style="margin:26px 0 10px;color:var(--gold2);font-size:17px">自动修复 · P77 黑天使军团</h3>
  <div class="card" id="autofixBox"></div>
  <h3 style="margin:26px 0 10px;color:var(--gold2);font-size:17px">DNA 时间轴 · 全链追溯</h3>
  <div id="dnaTimeline" style="margin-top:6px"></div>
</section>

<section id="sec-runtime">
  <h2 class="sec-title">系统运行时 · 自动化守护</h2>
  <p class="sec-sub">健康三色 · 每小时自愈 · 算力瘦身 · 记忆加载</p>
  <div class="card" style="text-align:center;font-family:var(--mono)" id="rtHealth"></div>
  <div class="grid c2" id="rtAuto"></div>
  <div class="grid c2" id="rtEnv"></div>
</section>

<section id="sec-gate">
  <h2 class="sec-title">三闸门决策流场</h2>
  <p class="sec-sub">数字根熔断 → 身份认证 → 伦理防火墙 → 路由分发</p>
  <div class="gates" id="gateFlow"></div>
  <h3 style="margin:28px 0 12px;color:var(--gold2);font-size:17px">人性 11 维 · 敏感度映射</h3>
  <div class="grid c3" id="dimGrid"></div>
  <h3 style="margin:28px 0 12px;color:var(--gold2);font-size:17px">思考循环 · 7 阶段</h3>
  <div id="stageList" style="margin-top:6px"></div>
</section>

<footer>
  <div>龍魂系统 · 归属名：诸葛鑫 | UID9622 · 龍芯北辰</div>
  <div class="stamp" id="footerStamp"></div>
  <div style="margin-top:6px">GPG A2D0092CEE2E5BA87035600924C3704A8CC26D5F · #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z</div>
  <div style="margin-top:2px;opacity:.75">思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2 · 三端离线 · 零外联</div>
</footer>

<div id="layerModal"><div class="box"><span class="close" id="modalClose">✕</span><h3 id="modalTitle"></h3><div id="modalBody"></div></div></div>

</div>

<script id="topoData" type="application/json">
__TOPODATA__
</script>
<script>
(function(){
  var T = null, $ = function(s){ return document.querySelector(s); };
  var esc = function(s){ return String(s == null ? '' : s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); };
  var ok = false;
  try { T = JSON.parse(document.getElementById('topoData').textContent); ok = true; } catch(e){}
  if(!ok){
    document.body.insertAdjacentHTML('afterbegin','<div style="padding:20px;text-align:center;color:var(--red)">🔴 拓扑数据解析失败 · 请重新运行构建脚本</div>');
    return;
  }
  /* 单模块错误边界：任何一段渲染失败只降级该段，不白屏 */
  function safe(name, fn){
    try { fn(); }
    catch(err){
      console.error('[龍魂拓扑] ' + name + ' 渲染失败:', err);
      var el = $('#sec-' + name);
      if(el) el.insertAdjacentHTML('afterbegin','<div class="card warn">🟡 '+esc(name)+' 模块加载失败 · 请检查数据契约 '+esc(String(err&&err.message||err))+'</div>');
    }
  }

  /* Service Worker 真离线（http/https 下注册；file:// 静默跳过） */
  if('serviceWorker' in navigator && location.protocol.indexOf('http') === 0){
    navigator.serviceWorker.register('sw.js').catch(function(){});
  }

  /* 版本 + 健康行 */
  safe('all', function(){
    var m = T._meta || {};
    var dna = document.getElementById('dnaChip');
    if(dna && m.dna) dna.textContent = m.dna;
    var h = (T.runtime_state && T.runtime_state.health) || {};
    var s = (T._meta && T._meta.system_health) || '';
    $('#healthLine').innerHTML =
      '<span class="g">🟢 ' + (h['🟢']||0) + '</span>' +
      '<span class="y">🟡 ' + (h['🟡']||0) + '</span>' +
      '<span class="r">🔴 ' + (h['🔴']||0) + '</span>' +
      '<span style="color:var(--dim)"> · ' + esc(s) + '</span>';
    $('#footerStamp').textContent = (m.dna||'') + ' · ' + (m.confirm||'');
    /* v1.3 · 健康三色可点击 → 跳系统运行时 */
    var hl = $('#healthLine');
    if(hl){
      hl.style.cursor = 'pointer';
      hl.title = '点按查看系统运行时';
      hl.addEventListener('click', function(){ if(window.gotoSection) gotoSection('runtime'); });
    }
  });

  /* 导航 + 区块互钻（v1.3 · 接口） */
  (function(){
    var NAV = [
      ['arch','九层架构'],['persona','人格矩阵'],['neural','神经网络'],
      ['engine','引擎'],['skill','技能'],['digital','数字人'],
      ['eco','生态'],['security','安全·语义盾'],['runtime','运行时·自动化'],
      ['gate','闸门·人性·思考']
    ];
    var NAV_MAP = {};
    NAV.forEach(function(x){ NAV_MAP[x[0]] = x[1]; });
    $('#navBar').innerHTML = NAV.map(function(x){
      return '<button data-k="' + x[0] + '">' + x[1] + '</button>';
    }).join('');
    window.gotoSection = function(k){
      Array.prototype.forEach.call(document.querySelectorAll('.nav button'), function(x){ x.classList.remove('on'); });
      Array.prototype.forEach.call(document.querySelectorAll('section'), function(x){ x.classList.remove('on'); });
      var b = document.querySelector('.nav button[data-k="' + k + '"]');
      if(b) b.classList.add('on');
      var s = $('#sec-' + k);
      if(s) s.classList.add('on');
      window.scrollTo({top:0,behavior:'smooth'});
    };
    var btns = document.querySelectorAll('.nav button');
    Array.prototype.forEach.call(btns, function(b){
      b.addEventListener('click', function(){ gotoSection(b.dataset.k); });
    });
    if(btns[0]) btns[0].classList.add('on');
    /* 区块互钻：各 section 标题旁加 ↗关联链 */
    var XREF = {
      'arch':['neural','runtime'],'persona':['engine','digital','gate'],
      'neural':['arch','engine'],'engine':['skill','neural'],
      'skill':['engine','persona'],'digital':['persona','skill'],
      'eco':['digital','engine'],'security':['runtime','gate'],
      'runtime':['security','arch'],'gate':['security','persona']
    };
    Array.prototype.forEach.call(document.querySelectorAll('section'), function(sec){
      var k = sec.id.replace('sec-','');
      var rel = XREF[k] || [];
      if(!rel.length) return;
      var h = sec.querySelector('.sec-title');
      if(!h) return;
      var span = document.createElement('span');
      span.className = 'xref';
      span.innerHTML = rel.map(function(r){
        return '<button data-goto="' + r + '">↗ ' + esc(NAV_MAP[r] || r) + '</button>';
      }).join('');
      h.appendChild(span);
    });
    Array.prototype.forEach.call(document.querySelectorAll('.xref button'), function(b){
      b.addEventListener('click', function(){ gotoSection(b.dataset.goto); });
    });
  })();

  /* 九宫格（洛书九宫 · 龍魂方位映射） */
  safe('arch', function(){
    var arch = T.architecture.layers;
    var num = {'nw4':'4','n9':'9','ne8':'8','e3':'3','w7':'7','se2':'2','s1':'1','sw6':'6'};
    var slots = [
      ['L8_治理层','nw4'],['L0_神圣层','n9'],['L2_技能层','ne8'],
      ['L3_路由层','e3'],['CENTER',null],['L7_数据层','w7'],
      ['L4_闸门层','se2'],['L5_服务层','s1'],['L6_集成层','sw6']
    ];
    $('#luoshGrid').innerHTML = slots.map(function(s){
      var k = s[0];
      if(k === 'CENTER'){
        var cont = (arch['L1_内核层'] && arch['L1_内核层'].content) || ['未知'];
        return '<div class="luo center"><div class="p">5</div><div class="n">UID9622 · 中宫</div><div class="d">' + esc(cont.join(' · ')) + '</div></div>';
      }
      var L = arch[k];
      if(!L) return '<div class="luo warn"><div class="p">?</div><div class="n">' + esc(k) + '</div><div class="d">缺失</div></div>';
      return '<div class="luo"><div class="p">' + num[s[1]] + '</div><div class="n">' + esc(L.palace || k) + ' · ' + esc(k) + '</div><div class="d">' + esc((L.content||[]).join(' · ')) + '</div></div>';
    }).join('');
  });

  /* 人格矩阵 */
  safe('persona', function(){
    var P = T.persona_matrix;
    var all = Object.assign({}, P.personas, P.subsystem_personas);
    $('#personaStat').textContent = P.total + ' 人格 · ' + P.core + ' 核心 + ' + P.subsystem + ' 子系统 · ' + P.landed + ' 已落地 · 0 红色';
    $('#personaGrid').innerHTML = Object.keys(all).map(function(id){
      var p = all[id] || {};
      return '<div class="card persona"><div class="id">' + esc(id) + '</div><div>' +
        '<div class="nm">' + esc(p.name) + ' <span class="wt">' + esc(p.weight || '') + '</span></div>' +
        '<div class="rl">' + esc(p.role) + '</div>' +
        '<div class="tag">' + esc(p.status) + '</div>' + (p.isolated ? '<div class="tag">隔离区</div>' : '') + '</div></div>';
    }).join('');
    var teams = (P.application_personas && P.application_personas.teams) || {};
    $('#teamGrid').innerHTML = Object.keys(teams).map(function(id){
      var t = teams[id] || {};
      return '<div class="card"><h3>' + esc(t.icon||'') + ' ' + esc(t.name) + '</h3>' +
        '<p>' + esc((t.members||[]).join(' + ')) + '</p><div class="tag">' + esc(t.workflow) + '</div></div>';
    }).join('');
  });

  /* 神经网络边图（按真实 edges 自适应 · 洛书八方固定 + 双外环按度数） */
  safe('neural', function(){
    var edges = (T.neural_edges && T.neural_edges.edges) || [];
    var svg = $('#edgeSvg');
    if(!svg) return;
    var CX = 450, CY = 320;
    var deg = {};
    edges.forEach(function(e){ deg[e.from] = (deg[e.from]||0) + 1; deg[e.to] = (deg[e.to]||0) + 1; });
    var nodes = Object.keys(deg);
    var center = 'center_5(UID9622)';
    var fixed = {
      'north_9(L0神圣)':0, 'northeast_8(L2技能)':1, 'east_3(L3路由)':2,
      'southeast_2(L4闸门)':3, 'south_1(L5服务)':4, 'southwest_6(L6集成)':5,
      'west_7(L7数据)':6, 'northwest_4(L8治理)':7
    };
    var pt = {}; pt[center] = [CX, CY];
    var R1 = 148, R2 = 262, R3 = 366;
    Object.keys(fixed).forEach(function(n){
      var a = fixed[n] / 8 * Math.PI * 2 - Math.PI / 2;
      pt[n] = [CX + Math.cos(a) * R1, CY + Math.sin(a) * R1 * 0.94];
    });
    var rest = nodes.filter(function(n){ return n !== center && !fixed[n]; })
      .sort(function(a,b){ return deg[b] - deg[a]; });
    var ring2 = rest.filter(function(_,i){ return i % 2 === 0; });
    var ring3 = rest.filter(function(_,i){ return i % 2 === 1; });
    ring2.forEach(function(n,i){
      var a = i / Math.max(ring2.length,1) * Math.PI * 2 - Math.PI / 2;
      pt[n] = [CX + Math.cos(a) * R2, CY + Math.sin(a) * R2 * 0.92];
    });
    ring3.forEach(function(n,i){
      var a = i / Math.max(ring3.length,1) * Math.PI * 2 - Math.PI / 2;
      pt[n] = [CX + Math.cos(a) * R3, CY + Math.sin(a) * R3 * 0.9];
    });
    var out = '';
    edges.forEach(function(e){
      var p1 = pt[e.from], p2 = pt[e.to];
      if(!p1 || !p2) return;
      var hot = (e.weight||0) >= 0.9;
      out += '<line class="edge' + (hot ? ' hot' : '') + '" x1="' + p1[0] + '" y1="' + p1[1] +
        '" x2="' + p2[0] + '" y2="' + p2[1] + '"><title>' + esc(e.from) + ' → ' + esc(e.to) +
        ' · ' + esc(e.type) + ' · ' + Math.round((e.weight||0)*100) + '%</title></line>';
    });
    Object.keys(pt).forEach(function(n){
      var p = pt[n];
      var hot = (deg[n]||0) >= 3;
      var isC = n === center;
      out += '<g class="node' + (hot ? ' hot' : '') + '"><circle cx="' + p[0] + '" cy="' + p[1] + '" r="' + (isC?24:9) + '"/>' +
        '<text x="' + p[0] + '" y="' + (p[1] + (isC?-30:16)) + '" text-anchor="middle">' + esc(n) + '</text></g>';
    });
    svg.innerHTML = out;
    /* 边明细（前 18 条按权重） */
    var top = edges.slice().sort(function(a,b){ return (b.weight||0) - (a.weight||0); }).slice(0,18);
    $('#edgeList').innerHTML = top.map(function(e){
      return '<div class="card" style="padding:10px 14px"><div class="tag">' + Math.round((e.weight||0)*100) + '%</div>' +
        '<p style="font-size:12px"><b style="color:var(--gold2)">' + esc(e.from) + '</b> → ' + esc(e.to) + '<br>' +
        '<span style="color:var(--dim)">' + esc(e.type) + '</span></p></div>';
    }).join('');

    /* v1.5 · 3D 银河星系（主力引擎 3D 全景 · 14 星域全集成 · 拖拽旋转 · 星爆脉冲 · 零黑箱联动公式） */
    /* 联动公式引擎（锚点: lh_digital_root.py v1.0 · lh_wuxing_core.py v3.0 · 洛书369 sn=369） */
    var WUXING = {0:'土',1:'水',2:'火',3:'木',4:'金',5:'土',6:'水',7:'火',8:'木',9:'金'};
    var WUXING_CLR = {金:'#e6c56a',木:'#7ecb8b',水:'#6fb1e8',火:'#e8836a',土:'#d0a25e'};
    var SHENG = {金:'水',水:'木',木:'火',火:'土',土:'金'};
    var KE    = {金:'木',木:'土',土:'水',水:'火',火:'金'};
    var REL_W = {比和:0.85,相生:1.0,相泄:0.75,相克:0.55,相耗:0.65,混合:0.70};
    var lhDr = function(txt){
      var s = String(txt||'');
      var digits = s.split('').filter(function(c){ return c >= '0' && c <= '9'; });
      if(!digits.length) return s.length % 10;              /* 退化规则: 名长（公开公示） */
      var sum = digits.reduce(function(a,b){ return a + parseInt(b,10); }, 0);
      while(sum >= 10){ sum = String(sum).split('').reduce(function(a,b){ return a + parseInt(b,10); }, 0); }
      return sum;
    };
    var wuxingRel = function(a,b){
      if(a === b) return '比和';
      if(SHENG[a] === b) return '相生';
      if(SHENG[b] === a) return '相泄';
      if(KE[a] === b) return '相克';
      if(KE[b] === a) return '相耗';
      return '混合';
    };
    var luoAffin = function(drA, drB){ return (drA % 5) === (drB % 5) ? 1.0 : 0.85; };
    var drSym = function(drA, drB){
      var d = Math.abs(drA - drB);
      return d >= 4 ? 0.70 : d === 3 ? 0.80 : d === 2 ? 0.90 : d === 1 ? 0.95 : 1.0;
    };
    var linkIndex = function(drA, drB){
      var wa = WUXING[drA], wb = WUXING[drB];
      var rel = wuxingRel(wa, wb);
      var W = Math.round((0.60*REL_W[rel] + 0.25*luoAffin(drA,drB) + 0.15*drSym(drA,drB)) * 1000) / 1000;
      var fuse = (drA === 3 || drA === 9 || drB === 3 || drB === 9);
      var color = (W >= 0.90 && !fuse) ? '🟢' : ((W >= 0.75 && !fuse) ? '🟡' : '🔴');
      return {wa:wa, wb:wb, rel:rel, wRel:REL_W[rel], luo:luoAffin(drA,drB), sym:drSym(drA,drB), W:W, fuse:fuse, color:color};
    };
    /* ── 14 星域数据构建（全系统集成: 层+引擎+技能+人格+数字人+生态） ── */
    var SECTORS = [];
    var LAY = T.architecture.layers || {};
    var layerKeys = Object.keys(LAY).sort(function(a,b){
      return parseInt(String(a).replace(/\D/g,'')) - parseInt(String(b).replace(/\D/g,''));
    });
    layerKeys.forEach(function(k){
      var L = LAY[k] || {};
      SECTORS.push({ id:'sec-' + k, type:'layer', title:k + ' · ' + (L.palace||''), sub:(L.role||''),
        anchors:L.anchors, rules:L.rules,
        items:(L.content||[]).map(function(x){ return {n:x, kind:'star'}; }) });
    });
    var ENGS = (T.engines && T.engines.highlights) || {};
    var engGroups = {'🔥 活跃引擎':[], '💤 休眠引擎':[], '⚰️ 退役引擎':[]};
    Object.keys(ENGS).forEach(function(k){
      var v = ENGS[k] || {};
      var st = String(v.status||'');
      var g = '🔥 活跃引擎';
      if(st.indexOf('shelved') >= 0) g = '💤 休眠引擎';
      else if(st.indexOf('deprecat') >= 0 || st.indexOf('inactive') >= 0) g = '⚰️ 退役引擎';
      engGroups[g].push({name:k, file:v.file, fn:v.function, status:st, port:v.port});
    });
    SECTORS.push({ id:'sec-engine', type:'engine', title:'🧠 引擎域',
      sub:Object.keys(ENGS).length + ' 引擎全部集成 · 按状态分组',
      items:Object.keys(engGroups).map(function(g){
        var lst = engGroups[g];
        return {n:g, kind:'nova', sub:lst.length + ' 引擎', detail:lst};
      }) });
    var CATS = ((T.skill_bus||{}).categories) || {};
    SECTORS.push({ id:'sec-skill', type:'skill', title:'🛠 技能域',
      sub:((T.skill_bus||{}).description||'') + ' · ' + Object.keys(CATS).length + ' 分类',
      items:Object.keys(CATS).map(function(c){
        var co = CATS[c] || {};
        return {n:c, kind:'nova', sub:(co.count||0) + ' 工具', detail:(co.skills||[])};
      }) });
    var PM = T.persona_matrix || {};
    var allP = Object.assign({}, PM.personas || {}, PM.subsystem_personas || {});
    SECTORS.push({ id:'sec-persona', type:'persona', title:'👤 人格域',
      sub:(PM.total||'') + ' 人格全集成',
      items:Object.keys(allP).map(function(k){
        var p = allP[k] || {};
        return {n:(p.name||k), kind:'star', sub:(p.role||p.function||'')};
      }) });
    var HUMANS = ((T.digital_humans||{}).humans) || [];
    SECTORS.push({ id:'sec-digital', type:'digital', title:'🤖 数字人域',
      sub:HUMANS.length + ' 数字人全集成',
      items:HUMANS.map(function(h){
        h = h || {};
        return {n:(h.name||h.id||''), kind:'star', sub:(h.persona||'') + ' · ' + (h.type||'')};
      }) });
    var TIERS = ((T.ecosystem||{}).tiers) || {};
    SECTORS.push({ id:'sec-eco', type:'eco', title:'🌍 生态域',
      sub:((T.ecosystem||{}).description||'') + ' · ' + Object.keys(TIERS).length + ' 层级',
      items:Object.keys(TIERS).map(function(t){
        var t2 = TIERS[t] || {};
        return {n:t, kind:'nova', sub:'¥' + (t2.price||0), detail:(t2.services||[])};
      }) });
    var SECTOR_MAP = {};
    SECTORS.forEach(function(s){ SECTOR_MAP[s.id] = s; });
    var scene = $('#domeScene');
    if(scene && SECTORS.length){
      var kf = Math.min(1, (document.documentElement.clientWidth || 900) / 880);
      var html = '<div id="galCore"><div class="lab">UID9622 · 龍核</div></div>';
      SECTORS.forEach(function(sec, i){
        var ang = i * 137.508 * Math.PI / 180;              /* 黄金角螺旋（银河旋臂真实数学） */
        var R = Math.round((58 + i * 40) * kf);
        var cz = Math.round((i - (SECTORS.length - 1) / 2) * 15);
        var cx = Math.round(Math.cos(ang) * R), cy = Math.round(Math.sin(ang) * R);
        var n = sec.items.length;
        var r2 = Math.max(40, Math.min(200, 18 + n * 17)) * kf;
        html += '<div class="cluster" data-sec="' + esc(sec.id) + '" data-type="' + esc(sec.type) + '" style="--cx:' + cx + 'px;--cy:' + cy + 'px;--cz:' + cz + 'px;transform:translate(' + cx + 'px,' + cy + 'px) translateZ(' + cz + 'px)">' +
          '<div class="halo" style="width:' + (r2*2) + 'px;height:' + (r2*2) + 'px;margin:-' + r2 + 'px 0 0 -' + r2 + 'px"></div>';
        sec.items.forEach(function(it, j){
          var a2 = j * 137.508 * Math.PI / 180;
          var rr = Math.max(8, Math.min(r2 * 0.88, 14 + j * 18)) * kf;
          var sx = Math.round(Math.cos(a2) * rr), sy = Math.round(Math.sin(a2) * rr);
          var dr = lhDr(it.n), wu = WUXING[dr], clr = WUXING_CLR[wu];
          var isNova = it.kind === 'nova';
          var sz = isNova ? 26 : (sec.type === 'persona' ? 13 : 11);
          html += '<div class="star' + (isNova ? ' nova' : '') + '" data-name="' + esc(it.n) + '" data-dr="' + dr + '" data-wu="' + wu + '" data-sec="' + esc(sec.id) + '" style="left:' + sx + 'px;top:' + sy + 'px;--sz:' + sz + 'px;--sc:' + clr + '">' +
            '<div class="lab">' + esc(it.n) + (it.sub ? '<small>' + esc(it.sub) + '</small>' : '') + '</div></div>';
        });
        html += '<div class="lab" data-sec="' + esc(sec.id) + '">' + esc(sec.title) + '<small>' + esc(sec.sub || '') + '</small></div></div>';
      });
      scene.innerHTML = html;
      /* 星域详情（14 域全量可查 · 点击星团标签） */
      var openSector = function(id){
        var sec = SECTOR_MAP[id];
        if(!sec) return;
        $('#modalTitle').textContent = sec.title;
        var h = sec.sub ? '<p style="font-size:13px;color:var(--sub)">' + esc(sec.sub) + '</p>' : '';
        if(sec.type === 'layer'){
          h += '<div style="margin-top:10px">' + sec.items.map(function(x){ return '<span class="tag">' + esc(x.n) + '</span>'; }).join('') + '</div>' +
            (sec.anchors ? '<p style="margin-top:10px;font-size:12px;color:var(--dim)">锚点: ' + esc(sec.anchors) + '</p>' : '') +
            (sec.rules ? '<p style="margin-top:4px;font-size:12px;color:var(--dim)">' + esc(sec.rules) + '</p>' : '');
        } else if(sec.type === 'engine'){
          h += '<div style="margin-top:10px">' + sec.items.map(function(g){
            return '<div class="card" style="padding:10px 14px;margin-bottom:8px"><h3>' + esc(g.n) + ' <span class="tag">' + esc(g.sub) + '</span></h3>' +
              (g.detail||[]).slice(0,40).map(function(e){
                return '<div style="font-size:11px;font-family:var(--mono);color:var(--dim);padding:3px 0;border-bottom:1px dashed var(--line)">' +
                  esc(e.name) + (e.port ? ' <span style="color:var(--gold)">:' + esc(e.port) + '</span>' : '') + ' · ' + esc(e.status) +
                  (e.file ? '<br><span style="color:var(--sub3)">' + esc(e.file) + '</span>' : '') + '</div>';
              }).join('') +
              ((g.detail||[]).length > 40 ? '<p style="font-size:11px;color:var(--dim);margin-top:4px">… 共 ' + g.detail.length + ' 引擎，全部已集成于本星云</p>' : '') + '</div>';
          }).join('') + '</div>';
        } else if(sec.type === 'skill' || sec.type === 'eco'){
          h += '<div style="margin-top:10px">' + sec.items.map(function(g){
            return '<div class="card" style="padding:10px 14px;margin-bottom:8px"><h3>' + esc(g.n) + ' <span class="tag">' + esc(g.sub) + '</span></h3>' +
              '<p>' + (g.detail||[]).map(function(s){ return '<span class="tag">' + esc(s) + '</span>'; }).join('') + '</p></div>';
          }).join('') + '</div>';
        } else if(sec.type === 'persona'){
          h += '<div style="margin-top:10px">' + sec.items.map(function(p){
            return '<div style="padding:8px 0;border-bottom:1px dashed var(--line)"><b style="color:var(--gold2)">' + esc(p.n) + '</b>' +
              '<span style="color:var(--dim);font-size:12px"> · ' + esc(p.sub || '') + '</span></div>';
          }).join('') + '</div>';
        } else if(sec.type === 'digital'){
          h += '<div style="margin-top:10px">' + sec.items.map(function(d){
            return '<div class="card" style="padding:10px 14px;margin-bottom:8px"><h3>' + esc(d.n) + '</h3>' +
              '<p style="font-size:12px;color:var(--dim)">' + esc(d.sub || '') + '</p></div>';
          }).join('') + '</div>';
        }
        $('#modalBody').innerHTML = h;
        $('#layerModal').classList.add('on');
      };
      Array.prototype.forEach.call(scene.querySelectorAll('.cluster > .lab'), function(el){
        el.addEventListener('click', function(){ openSector(el.getAttribute('data-sec')); });
      });
      /* 双星联动：点第一颗选星 → 点第二颗出公式（任意星域任意两颗星） */
      var selStar = null;
      var openLink = function(a, b){
        var r = linkIndex(parseInt(a.getAttribute('data-dr'),10), parseInt(b.getAttribute('data-dr'),10));
        var na = a.getAttribute('data-name'), nb = b.getAttribute('data-name');
        var da = a.getAttribute('data-dr'), db = b.getAttribute('data-dr');
        $('#modalTitle').textContent = '🪐 星球联动 · 计算公式';
        $('#modalBody').innerHTML =
          '<div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center">' +
            '<div class="card" style="flex:1;min-width:150px;padding:12px;text-align:center">' +
              '<div style="width:16px;height:16px;border-radius:50%;background:' + WUXING_CLR[r.wa] + ';margin:0 auto 6px;box-shadow:0 0 12px ' + WUXING_CLR[r.wa] + '"></div>' +
              '<div style="font-size:13px;color:var(--gold2)">' + esc(na) + '</div>' +
              '<div class="tag">dr=' + da + ' · ' + r.wa + '</div></div>' +
            '<div style="color:var(--gold);font-size:22px">⇄</div>' +
            '<div class="card" style="flex:1;min-width:150px;padding:12px;text-align:center">' +
              '<div style="width:16px;height:16px;border-radius:50%;background:' + WUXING_CLR[r.wb] + ';margin:0 auto 6px;box-shadow:0 0 12px ' + WUXING_CLR[r.wb] + '"></div>' +
              '<div style="font-size:13px;color:var(--gold2)">' + esc(nb) + '</div>' +
              '<div class="tag">dr=' + db + ' · ' + r.wb + '</div></div>' +
          '</div>' +
          '<table class="frm" style="margin-top:12px">' +
            '<tr><td>③ 五行关系</td><td>' + r.wa + ' vs ' + r.wb + ' → <b style="color:var(--gold2)">' + r.rel + '</b> · 系数 ' + r.wRel.toFixed(2) + '</td></tr>' +
            '<tr><td>④ 洛书亲和</td><td>数对 ' + (da % 5) + '-' + (db % 5) + ' → ' + r.luo.toFixed(2) + '</td></tr>' +
            '<tr><td>⑤ 数字根对称</td><td>|' + da + '−' + db + '|=' + Math.abs(da-db) + ' → ' + r.sym.toFixed(2) + '</td></tr>' +
            '<tr><td>⑥ 联动指数</td><td>W = 0.60×' + r.wRel.toFixed(2) + ' + 0.25×' + r.luo.toFixed(2) + ' + 0.15×' + r.sym.toFixed(2) + ' = <b style="color:var(--gold2)">' + r.W.toFixed(3) + '</b>' + (r.fuse ? ' · ⚠️ 含熔断数字根(3/9)' : '') + '</td></tr>' +
            '<tr><td>⑦ 三色判定</td><td style="font-size:16px">' + r.color + ' ' + (r.W >= 0.90 ? '联动畅通' : r.W >= 0.75 ? '联动待核' : '联动受克') + '</td></tr>' +
          '</table>' +
          '<p style="font-size:11px;color:var(--dim);margin-top:8px">公式: 数字根→五行→关系系数·洛书亲和·对称度 → 加权合成。锚点: lh_wuxing_core.py v3.0 · lh_digital_root.py v1.0 · 洛书369</p>';
        $('#layerModal').classList.add('on');
      };
      Array.prototype.forEach.call(scene.querySelectorAll('.star'), function(s){
        s.addEventListener('click', function(e){
          e.stopPropagation();
          if(selStar === s){ s.classList.remove('sel'); selStar = null; return; }
          if(!selStar){ selStar = s; s.classList.add('sel'); }
          else { openLink(selStar, s); selStar.classList.remove('sel'); selStar = null; }
        });
      });
      /* 详情弹层关闭 */
      var mc = $('#modalClose');
      if(mc) mc.addEventListener('click', function(){ $('#layerModal').classList.remove('on'); });
      var lm = $('#layerModal');
      if(lm) lm.addEventListener('click', function(e){ if(e.target === this) this.classList.remove('on'); });
      /* 3D 拖拽旋转（鼠标 + 触屏） */
      var wrap = $('#domeWrap');
      var rx = -18, ry = 0, drg = null, auto = true, raf = null;
      var apply = function(){ scene.style.transform = 'rotateX(' + rx + 'deg) rotateY(' + ry + 'deg)'; };
      var tick = function(){
        if(auto && !drg) ry += 0.045;
        apply();
        raf = requestAnimationFrame(tick);
      };
      wrap.addEventListener('mousedown', function(e){
        if(e.target.closest('.star') || e.target.closest('#galCore') || e.target.closest('.cluster > .lab')) return;
        drg = { x:e.clientX, y:e.clientY, rx:rx, ry:ry };
        scene.classList.add('grabbing');
      });
      window.addEventListener('mousemove', function(e){
        if(!drg) return;
        ry = drg.ry + (e.clientX - drg.x) * 0.35;
        rx = Math.max(-85, Math.min(85, drg.rx - (e.clientY - drg.y) * 0.35));
      });
      window.addEventListener('mouseup', function(){ if(drg){ drg = null; scene.classList.remove('grabbing'); } });
      wrap.addEventListener('touchstart', function(e){
        if(e.target.closest('.star') || e.target.closest('#galCore') || e.target.closest('.cluster > .lab')) return;
        var t = e.touches[0];
        drg = { x:t.clientX, y:t.clientY, rx:rx, ry:ry };
        scene.classList.add('grabbing');
      }, {passive:true});
      window.addEventListener('touchmove', function(e){
        if(!drg) return;
        var t = e.touches[0];
        ry = drg.ry + (t.clientX - drg.x) * 0.35;
        rx = Math.max(-85, Math.min(85, drg.rx - (t.clientY - drg.y) * 0.35));
      }, {passive:true});
      window.addEventListener('touchend', function(){ if(drg){ drg = null; scene.classList.remove('grabbing'); } });
      raf = requestAnimationFrame(tick);
      var br = $('#btnRotate');
      if(br) br.addEventListener('click', function(){
        auto = !auto;
        br.classList.toggle('on', auto);
        br.textContent = auto ? '🔄 自动旋转' : '⏸ 暂停旋转';
      });
      /* 星爆脉冲：全星系炸散 → 聚拢 */
      var boomed = false;
      var boom = function(){
        boomed = !boomed;
        var bb = $('#btnBoom');
        if(bb){ bb.classList.toggle('on', boomed); bb.textContent = boomed ? '🧲 聚拢星系' : '💥 星爆脉冲'; }
        Array.prototype.forEach.call(scene.querySelectorAll('.cluster'), function(c, i){
          c.classList.remove('boom','unboom');
          void c.offsetWidth;
          var a = i * 137.508 * Math.PI / 180;
          var dist = 60 + (i % 5) * 26;
          c.style.setProperty('--dx', Math.round(Math.cos(a) * dist) + 'px');
          c.style.setProperty('--dy', Math.round(Math.sin(a) * dist) + 'px');
          c.style.setProperty('--dz', Math.round(((i % 7) - 3) * 18) + 'px');
          c.classList.add(boomed ? 'boom' : 'unboom');
        });
        Array.prototype.forEach.call(scene.querySelectorAll('.star'), function(s, j){
          s.classList.remove('boom','unboom');
          void s.offsetWidth;
          var a = (j * 137.508 + Math.sin(j) * 37) * Math.PI / 180;
          var dist = 140 + (j % 9) * 70;
          s.style.setProperty('--bx', Math.round(Math.cos(a) * dist) + 'px');
          s.style.setProperty('--by', Math.round(Math.sin(a) * dist) + 'px');
          s.classList.add(boomed ? 'boom' : 'unboom');
        });
        var core = $('#galCore');
        if(core){ core.classList.remove('boom','unboom'); void core.offsetWidth; core.classList.add(boomed ? 'boom' : 'unboom'); }
      };
      var bb = $('#btnBoom');
      if(bb) bb.addEventListener('click', boom);
      /* 层层递进动画：星团 0 → N 级联弹出 */
      var popBtn = $('#btnPop');
      if(popBtn) popBtn.addEventListener('click', function(){
        Array.prototype.forEach.call(scene.querySelectorAll('.cluster'), function(s, i){
          s.classList.remove('pop');
          void s.offsetWidth;
          s.style.animationDelay = (i * 0.22) + 's';
          s.classList.add('pop');
        });
      });
      /* 模式切换：3D 银河 ↔ 平面边图 */
      var b3 = $('#btn3d'), b2 = $('#btn2d');
      var switchMode = function(m){
        $('#mode3d').classList.toggle('on', m === '3d');
        $('#mode2d').classList.toggle('on', m !== '3d');
        b3.classList.toggle('on', m === '3d');
        b2.classList.toggle('on', m !== '3d');
      };
      if(b3) b3.addEventListener('click', function(){ switchMode('3d'); });
      if(b2) b2.addEventListener('click', function(){ switchMode('2d'); });
    }
  });

  /* 引擎（搜索过滤 + 状态判空） */
  safe('engine', function(){
    var H = (T.engines && T.engines.highlights) || {};
    var items = Object.keys(H).map(function(k){
      var v = H[k] || {};
      return { k:k, name:k, file:v.file, fn:v.function, status:v.status, port:v.port };
    });
    var render = function(kw){
      kw = (kw||'').toLowerCase();
      var list = items.filter(function(i){
        return !kw || i.name.toLowerCase().indexOf(kw) >= 0 ||
          (i.fn||'').toLowerCase().indexOf(kw) >= 0 ||
          (i.file||'').toLowerCase().indexOf(kw) >= 0;
      });
      $('#engCount').textContent = '显示 ' + list.length + ' / ' + items.length + ' 引擎';
      $('#engGrid').innerHTML = list.map(function(i){
        var st = String(i.status||'');
        var cls = 'eng';
        if(st.indexOf('shelved') >= 0) cls = 'eng shelved';
        else if(st.indexOf('deprecat') >= 0 || st.indexOf('inactive') >= 0) cls = 'eng dep';
        return '<div class="card ' + cls + '"><h3>' + esc(i.name) + (i.port ? '<span class="tag">:' + esc(i.port) + '</span>' : '') + '</h3>' +
          '<p style="font-size:12px;color:var(--dim);font-family:var(--mono)">' + esc(i.file) + '</p>' +
          '<p style="margin-top:4px">' + esc(i.fn) + '</p>' +
          '<div class="tag">' + esc(st) + '</div></div>';
      }).join('');
    };
    render('');
    $('#engSearch').addEventListener('input', function(e){ render(e.target.value); });
  });

  /* 技能总线 */
  safe('skill', function(){
    var S = T.skill_bus || {};
    var cats = S.categories || {};
    $('#skillStat').textContent = (S.total||0) + ' 工具 · ' + Object.keys(cats).length + ' 分类 · ' + (S.description||'');
    $('#skillGrid').innerHTML = Object.keys(cats).map(function(cat){
      var c = cats[cat] || {};
      return '<div class="card"><h3>' + esc(cat) + ' <span class="tag" style="float:right">' + (c.count||0) + '</span></h3>' +
        '<p>' + (c.skills||[]).map(function(s){ return '<span class="tag">' + esc(s) + '</span>'; }).join('') + '</p></div>';
    }).join('');
  });

  /* 数字人 */
  safe('digital', function(){
    var hs = (T.digital_humans && T.digital_humans.humans) || [];
    $('#dhGrid').innerHTML = hs.map(function(h){
      h = h || {};
      return '<div class="card dh"><div class="no">' + esc(h.id) + '</div><h3>' + esc(h.name) + '</h3>' +
        '<p>' + esc(h.persona) + ' · ' + esc(h.type) + '</p><div class="tag">' + esc(h.status) + '</div></div>';
    }).join('');
  });

  /* 生态 */
  safe('eco', function(){
    var E = T.ecosystem || {};
    var tiers = E.tiers || {};
    $('#ecoStat').textContent = (E.description||'') + ' · ' + (E.passport_engine||'');
    $('#ecoGrid').innerHTML = Object.keys(tiers).map(function(tier){
      var t = tiers[tier] || {};
      return '<div class="card"><div class="tier"><h3 style="text-transform:capitalize">' + esc(tier) + '</h3>' +
        '<span class="price">¥' + t.price + '</span></div>' +
        '<p>' + (t.services||[]).map(function(s){ return '<span class="tag">' + esc(s) + '</span>'; }).join('') + '</p></div>';
    }).join('');
  });

  /* 安全 · 语义盾 + 红线 + 自动修复 + DNA 时间轴 */
  safe('security', function(){
    var S = T.semantic_shield || {}, Sec = T.security || {};
    var files = S.files || {};
    $('#shieldGrid').innerHTML =
      '<div class="card"><h3>语义防火墙</h3><p>' + esc(S.description||'') + '</p>' +
      Object.keys(files).map(function(f){
        return '<span class="tag">' + esc(f) + '</span>';
      }).join('') + '</div>' +
      '<div class="card"><h3>三色审计</h3>' +
      Object.keys((Sec.three_color_audit)||{}).map(function(k){
        return '<p style="font-size:13px">' + esc(k) + ' ' + esc(Sec.three_color_audit[k]) + '</p>';
      }).join('') + '</div>';
    $('#redlineList').innerHTML = '<p style="font-size:13px">' +
      ((Sec.redlines)||[]).map(function(r){ return '<span class="tag" style="color:var(--red);border-color:var(--red)">' + esc(r) + '</span>'; }).join('') + '</p>';
    $('#autofixBox').innerHTML = '<p style="font-size:13px">' + esc(Sec.auto_fix_principle||'') + '</p>' +
      '<p style="font-size:12px;color:var(--sub);margin-top:6px">' + esc(Sec.auto_heal_schedule||'') + '</p>';
    var TL = (T.dna_timeline && T.dna_timeline.layers) || {};
    $('#dnaTimeline').innerHTML = Object.keys(TL).map(function(k){
      var v = TL[k] || {};
      return '<div class="stage"><div class="sn">' + esc(k) + '</div><div><b style="color:var(--gold2)">' + esc(v.timescale||'') + '</b>' +
        '<p style="font-size:12px;color:var(--sub)">' + esc(v.content||'') + '</p></div></div>';
    }).join('');
  });

  /* 系统运行时 · 自动化守护 */
  safe('runtime', function(){
    var R = T.runtime_state || {}, m = T._meta || {};
    var h = R.health || {};
    $('#rtHealth').innerHTML =
      '<span class="g">🟢 ' + (h['🟢']||0) + '</span> &nbsp; ' +
      '<span class="y">🟡 ' + (h['🟡']||0) + '</span> &nbsp; ' +
      '<span class="r">🔴 ' + (h['🔴']||0) + '</span>' +
      ' &nbsp;·&nbsp; ' + esc(R.description||'') + ' · ' + esc(m.evolution||'');
    var ah = R.auto_heal || {}, mem = R.memory || {};
    $('#rtAuto').innerHTML =
      '<div class="card"><h3>自动自愈 · 每小时</h3>' +
      '<p>' + esc(ah.schedule||'') + '</p>' +
      '<div class="tag">' + esc(ah.mechanism||'') + '</div><div class="tag">' + esc(ah.plist||'') + '</div></div>' +
      '<div class="card"><h3>记忆加载</h3>' +
      '<div class="tag">每日 ' + esc(mem.daily_log||'') + '</div><div class="tag">长期 ' + esc(mem.long_term||'') + '</div>' +
      '<p style="font-size:12px;color:var(--sub);margin-top:6px">会话记忆 ' + (mem.session_loaded ? '已加载' : '未加载') + '</p></div>';
    $('#rtEnv').innerHTML =
      '<div class="card"><h3>算力瘦身</h3><p style="font-size:12px">' + esc(R.compute_slim||'') + '</p></div>' +
      '<div class="card"><h3>环境</h3>' +
      '<div class="tag">Python ' + esc(R.python||'') + '</div><div class="tag">磁盘 ' + esc(R.disk||'') + '</div>' +
      '<div class="tag">网络 ' + esc(R.network||'') + '</div></div>';
  });

  /* 闸门 + 人性 + 思考 */
  safe('gate', function(){
    var G = T.gates || {};
    var gs = Object.keys(G).filter(function(k){ return k.indexOf('GATE') === 0; });
    $('#gateFlow').innerHTML = gs.map(function(k, i){
      var g = G[k] || {};
      return '<div class="gate"><div class="gn">' + esc(g.name) + '</div><div class="gr">' + esc(g.rule) + '</div>' +
        '<div style="font-size:11px;color:var(--sub);margin-top:2px">' + esc(g.persona) + '</div></div>' +
        (i < gs.length-1 ? '<span class="arrow">→</span>' : '');
    }).join('');
    var D = (T.human_nature_dimensions && T.human_nature_dimensions.dimensions) || {};
    $('#dimGrid').innerHTML = Object.keys(D).map(function(k){
      var v = D[k] || {};
      return '<div class="card"><h3>' + esc(k) + '</h3><p>' + esc(v.description) + '</p>' +
        '<div class="tag">' + esc(v.top_persona) + '</div></div>';
    }).join('');
    var Ph = (T.thinking_cycle && T.thinking_cycle.phases) || {};
    $('#stageList').innerHTML = Object.keys(Ph).map(function(k){
      return '<div class="stage"><div class="sn">' + esc(String(k).split('_')[0]) + '</div><div><b style="color:var(--gold2)">' + esc(k) + '</b>' +
        '<p style="font-size:12px;color:var(--sub)">' + esc(Ph[k]) + '</p></div></div>';
    }).join('');
  });
})();
</script>
</body>
</html>
"""

# ── Manifest（含位图图标）──────────────────────────────────────
def make_manifest(data) -> str:
    m = data.get("_meta", {})
    return json.dumps({
        "name": "龍魂拓扑 · 神经网络全览",
        "short_name": "龍魂拓扑",
        "description": "龍魂系统 L0-L9 九层架构 / 人格矩阵 / 神经网络可视化（离线可用）",
        "start_url": "./index.html",
        "display": "standalone",
        "background_color": "#0a0e14",
        "theme_color": "#0a0e14",
        "lang": "zh-CN",
        "categories": ["productivity", "developer"],
        "version": VERSION,
        "dna": m.get("dna", ""),
        "icons": [
            {"src": "icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"},
            {"src": "icon-180.png", "sizes": "180x180", "type": "image/png"},
            {"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
            {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
        ],
    }, ensure_ascii=False, indent=2)


# ── 契约校验 ──────────────────────────────────────────────────
def validate_contract(data) -> list:
    errs = []
    for k in REQUIRED_TOP:
        if k not in data:
            errs.append(f"缺失顶层字段: {k}")
    arch = (data.get("architecture") or {}).get("layers") or {}
    for k in REQUIRED_ARCH:
        if k not in arch:
            errs.append(f"缺失架构层: {k}")
    edges = (data.get("neural_edges") or {}).get("edges") or []
    if not isinstance(edges, list) or len(edges) < 5:
        errs.append(f"neural_edges.edges 异常: {len(edges)} 条（应 ≥5）")
    if "personas" not in (data.get("persona_matrix") or {}):
        errs.append("persona_matrix.personas 缺失")
    return errs


# ── PNG 位图图标（探测转换器：rsvg-convert > magick > qlmanage）──
def detect_icon_tool() -> str | None:
    for tool in ("rsvg-convert", "magick"):
        if shutil.which(tool):
            return tool
    if shutil.which("qlmanage"):
        return "qlmanage"
    return None


def make_png(svg: Path, out: Path, size: int, tool: str) -> bool:
    try:
        if tool == "rsvg-convert":
            subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size),
                            "-o", str(out), str(svg)], check=True, capture_output=True)
        elif tool == "magick":
            subprocess.run(["magick", "-background", "none", "-density", "300",
                            str(svg), "-resize", f"{size}x{size}", str(out)],
                           check=True, capture_output=True)
        elif tool == "qlmanage":
            tmp = out.parent / ".ql_tmp"
            tmp.mkdir(exist_ok=True)
            subprocess.run(["qlmanage", "-t", "-s", str(size), "-o", str(tmp), str(svg)],
                           check=True, capture_output=True)
            gen = tmp / (svg.name + ".png")
            if not gen.exists():
                return False
            gen.replace(out)
        return out.stat().st_size > 500
    except Exception:
        return False


# ── 主构建 ────────────────────────────────────────────────────
def build(json_path: Path, out_dir: Path) -> int:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. 契约校验
    errs = validate_contract(data)
    if errs:
        print("🔴 拓扑契约校验失败 · 拒绝产出:")
        for e in errs:
            print(f"   - {e}")
        return 1
    print(f"🟢 契约校验通过 · {len(REQUIRED_TOP)} 顶层字段 · {len(REQUIRED_ARCH)} 架构层")

    # 2. 单页 HTML
    html = HTML_TEMPLATE.replace("__TOPODATA__", json.dumps(data, ensure_ascii=False, indent=1))
    (out_dir / "index.html").write_text(html, encoding="utf-8")

    # 3. Service Worker + Manifest + SVG 图标
    (out_dir / "sw.js").write_text(SW_JS, encoding="utf-8")
    (out_dir / "manifest.webmanifest").write_text(make_manifest(data), encoding="utf-8")
    (out_dir / "icon.svg").write_text(ICON_SVG, encoding="utf-8")

    # 4. PNG 位图图标（iOS/鸿蒙主屏必需）
    tool = detect_icon_tool()
    png_ok = True
    if tool:
        for size in (180, 192, 512):
            ok = make_png(out_dir / "icon.svg", out_dir / f"icon-{size}.png", size, tool)
            if not ok:
                png_ok = False
                print(f"🟡 icon-{size}.png 生成失败（{tool}）")
        print(f"🟢 PNG 位图图标已生成（{tool}）" if png_ok else "🟡 PNG 图标不完整 · iOS 主屏图标可能缺失")
    else:
        print("🟡 未找到 rsvg-convert/magick/qlmanage · 跳过 PNG 图标 · iOS 主屏图标缺失")

    # 5. 汇总
    files = sorted(p.name for p in out_dir.iterdir())
    size = sum(p.stat().st_size for p in out_dir.iterdir())
    print(f"🟢 龍魂拓扑构建完成 → {out_dir}")
    print(f"   产物: {', '.join(files)} · {size/1024:.1f} KB · 三端离线可用")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="龍魂拓扑可视化构建器")
    ap.add_argument("--json", type=Path, default=DEFAULT_JSON)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    if not args.json.exists():
        print(f"🔴 拓扑文件不存在: {args.json}")
        sys.exit(1)
    sys.exit(build(args.json, args.out))


if __name__ == "__main__":
    main()
