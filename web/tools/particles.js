// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-a7a24769
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/* ============================================
   龍魂 · 粒子画布系统
   ============================================ */

// —— 四叉树 ——
class QuadTree {
  constructor(boundary, capacity = 4) {
    this.boundary = boundary; // { x, y, w, h }
    this.capacity = capacity;
    this.particles = [];
    this.divided = false;
    this.northwest = null;
    this.northeast = null;
    this.southwest = null;
    this.southeast = null;
  }

  subdivide() {
    const x = this.boundary.x;
    const y = this.boundary.y;
    const w = this.boundary.w / 2;
    const h = this.boundary.h / 2;

    this.northwest = new QuadTree({ x, y, w, h }, this.capacity);
    this.northeast = new QuadTree({ x: x + w, y, w, h }, this.capacity);
    this.southwest = new QuadTree({ x, y: y + h, w, h }, this.capacity);
    this.southeast = new QuadTree({ x: x + w, y: y + h, w, h }, this.capacity);
    this.divided = true;
  }

  insert(particle, projX, projY) {
    if (!this.contains(projX, projY)) return false;

    if (this.particles.length < this.capacity) {
      this.particles.push({ particle, x: projX, y: projY });
      return true;
    }

    if (!this.divided) this.subdivide();

    return this.northwest.insert(particle, projX, projY)
      || this.northeast.insert(particle, projX, projY)
      || this.southwest.insert(particle, projX, projY)
      || this.southeast.insert(particle, projX, projY);
  }

  contains(x, y) {
    return x >= this.boundary.x && x < this.boundary.x + this.boundary.w
      && y >= this.boundary.y && y < this.boundary.y + this.boundary.h;
  }

  query(range, found = []) {
    if (!this.intersects(range)) return found;

    for (const p of this.particles) {
      if (p.x >= range.x && p.x < range.x + range.w
        && p.y >= range.y && p.y < range.y + range.h) {
        found.push(p);
      }
    }

    if (this.divided) {
      this.northwest.query(range, found);
      this.northeast.query(range, found);
      this.southwest.query(range, found);
      this.southeast.query(range, found);
    }

    return found;
  }

  intersects(range) {
    return !(range.x > this.boundary.x + this.boundary.w
      || range.x + range.w < this.boundary.x
      || range.y > this.boundary.y + this.boundary.h
      || range.y + range.h < this.boundary.y);
  }

  clear() {
    this.particles = [];
    this.divided = false;
    this.northwest = null;
    this.northeast = null;
    this.southwest = null;
    this.southeast = null;
  }
}

// —— 粒子系统 ——
class ParticleSystem {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.container = this.canvas.parentElement;
    this.dpr = window.devicePixelRatio || 1;

    this.colors = {
      bg:       { r: 0,   g: 0,   b: 0   },
      gold:     { r: 255, g: 187, b: 0   },
      red:      { r: 212, g: 36,  b: 36  },
      redGlow:  { r: 212, g: 36,  b: 36  },
      dimGold:  { r: 100, g: 75,  b: 0   },
      dimRed:   { r: 80,  g: 20,  b: 20  },
      white:    { r: 235, g: 235, b: 235 },
      dimWhite: { r: 100, g: 100, b: 100 },
    };

    this.projection = {
      depth: 800,
      cameraZ: 600,
      focalLength: 500,
    };

    this.particles = [];
    this.isDragging = false;
    this.dragStart = { x: 0, y: 0 };
    this.rotationVelocity = { x: 0, y: 0 };
    this.zoom = 1;
    this.zoomTarget = 1;
    this.framesSinceRotation = 100;
    this.mouse = { x: -9999, y: -9999 };
    this.hoveredParticle = null;
    this.tooltip = document.getElementById('cn-tooltip');
    this.animFrame = null;

    this.resize();
    this.initParticles();
    this.bindEvents();
    this.start();
  }

  resize() {
    const w = this.container.clientWidth;
    const h = this.container.clientHeight;
    this.canvas.width = w * this.dpr;
    this.canvas.height = h * this.dpr;
    this.ctx.scale(this.dpr, this.dpr);
    this.width = w;
    this.height = h;
  }

  initParticles() {
    this.particles = [];
    for (let i = 0; i < 150; i++) {
      const angle = (i / 150) * Math.PI * 2;
      const type = i % 3 === 0 ? 'bright'
        : i % 3 === 1 ? 'dim' : 'alternate';

      this.particles.push({
        x: this.width * 0.5 + Math.cos(angle) * this.width * 0.3,
        y: this.height * 0.5 + Math.sin(angle) * this.height * 0.3,
        z: Math.random() * 400 - 200,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
        vz: (Math.random() - 0.5) * 0.15,
        radius: type === 'bright' ? 8 + Math.random() * 10
          : type === 'dim' ? 3 + Math.random() * 5
          : 4 + Math.random() * 6,
        color: type === 'bright' ? { ...this.colors.gold }
          : type === 'dim' ? { ...this.colors.dimGold }
          : i % 2 === 0 ? { ...this.colors.red }
          : { ...this.colors.gold },
        isBright: type === 'bright',
        age: Math.floor(Math.random() * 500),
        lifespan: 400 + Math.floor(Math.random() * 800),
        pulsePhase: Math.random() * Math.PI * 2,
        type,
        id: i,
      });
    }
  }

  project(x, y, z) {
    const denom = this.projection.focalLength + this.projection.cameraZ - z;
    if (denom <= 0) return null;
    const scale = this.projection.focalLength / denom;
    return {
      x: this.width * 0.5 + (x - this.width * 0.5) * scale,
      y: this.height * 0.5 + (y - this.height * 0.5) * scale,
      scale,
    };
  }

  inverseProject(screenX, screenY, z) {
    const denom = this.projection.focalLength + this.projection.cameraZ - z;
    const scale = this.projection.focalLength / denom;
    const x = this.width * 0.5 + (screenX - this.width * 0.5) / scale;
    const y = this.height * 0.5 + (screenY - this.height * 0.5) / scale;
    return { x, y };
  }

  bindEvents() {
    // Drag
    this.canvas.addEventListener('mousedown', (e) => {
      this.isDragging = true;
      this.dragStart.x = e.clientX;
      this.dragStart.y = e.clientY;
      this.rotationVelocity.x = 0;
      this.rotationVelocity.y = 0;
    });

    window.addEventListener('mousemove', (e) => {
      const rect = this.canvas.getBoundingClientRect();
      this.mouse.x = e.clientX - rect.left;
      this.mouse.y = e.clientY - rect.top;

      if (this.isDragging) {
        const dx = e.clientX - this.dragStart.x;
        const dy = e.clientY - this.dragStart.y;
        this.dragStart.x = e.clientX;
        this.dragStart.y = e.clientY;

        this.rotationVelocity.x = dy * 0.01;
        this.rotationVelocity.y = dx * 0.01;
        this.framesSinceRotation = 0;

        for (const p of this.particles) {
          p.vx += dy * 0.001;
          p.vy += dx * 0.001;
        }
      }
    });

    window.addEventListener('mouseup', () => {
      this.isDragging = false;
    });

    // Wheel zoom
    this.canvas.addEventListener('wheel', (e) => {
      e.preventDefault();
      this.zoomTarget += e.deltaY * 0.001;
      this.zoomTarget = Math.max(0.3, Math.min(3, this.zoomTarget));
    }, { passive: false });

    // Resize
    window.addEventListener('resize', () => {
      this.ctx.setTransform(1, 0, 0, 1, 0, 0);
      this.resize();
    });
  }

  start() {
    this.loop();
  }

  loop() {
    this.update();
    this.render();
    this.animFrame = requestAnimationFrame(() => this.loop());
  }

  update() {
    // Zoom smoothing
    this.zoom += (this.zoomTarget - this.zoom) * 0.1;
    this.projection.cameraZ = 600 / this.zoom;

    // Rotation inertia
    if (!this.isDragging) {
      if (this.framesSinceRotation < 30) {
        for (const p of this.particles) {
          p.vx += this.rotationVelocity.x * 0.3;
          p.vy += this.rotationVelocity.y * 0.3;
        }
        this.rotationVelocity.x *= 0.95;
        this.rotationVelocity.y *= 0.95;
        this.framesSinceRotation++;
      }
    }

    // Update particles
    for (const p of this.particles) {
      p.x += p.vx;
      p.y += p.vy;
      p.z += p.vz;

      // Gravity
      p.vy += 0.005;

      // Boundary wrap
      const margin = 200;
      if (p.x < -margin) p.x = this.width + margin;
      if (p.x > this.width + margin) p.x = -margin;
      if (p.y < -margin) p.y = this.height + margin;
      if (p.y > this.height + margin) p.y = -margin;
      if (p.z < -400) p.z = 400;
      if (p.z > 400) p.z = -400;

      // Bright particles move faster
      if (p.isBright) {
        p.vx *= 1.001;
        p.vy *= 1.001;
      }

      // Age
      p.age++;

      // Respawn
      if (p.age > p.lifespan) {
        p.age = 0;
        const angle = Math.random() * Math.PI * 2;
        p.x = this.width * 0.5 + Math.cos(angle) * this.width * 0.3;
        p.y = this.height * 0.5 + Math.sin(angle) * this.height * 0.3;
        p.vx = (Math.random() - 0.5) * 0.3;
        p.vy = (Math.random() - 0.5) * 0.3;
        p.vz = (Math.random() - 0.5) * 0.15;
      }
    }
  }

  render() {
    const ctx = this.ctx;
    const w = this.width;
    const h = this.height;

    // Trail fade
    ctx.fillStyle = 'rgba(0, 0, 0, 0.08)';
    ctx.fillRect(0, 0, w, h);

    // Project all particles
    const projected = [];
    for (const p of this.particles) {
      const proj = this.project(p.x, p.y, p.z);
      if (proj && proj.scale > 0.1
        && proj.x > -50 && proj.x < w + 50
        && proj.y > -50 && proj.y < h + 50) {
        projected.push({ particle: p, ...proj });
      }
    }

    // Sort by scale (far to near)
    projected.sort((a, b) => a.scale - b.scale);

    // Build quadtree
    const qt = new QuadTree({ x: 0, y: 0, w, h });
    for (const p of projected) {
      qt.insert(p.particle, p.x, p.y);
    }

    // Render connections
    for (const p of projected) {
      const range = { x: p.x - 80, y: p.y - 80, w: 160, h: 160 };
      const neighbors = qt.query(range);
      for (const n of neighbors) {
        if (n.particle.id <= p.particle.id) continue;
        const dx = n.x - p.x;
        const dy = n.y - p.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 80 && dist > 0) {
          const alpha = 0.12 * n.particle === p.particle ? 1 : (n.particle ? 1 : 0.5) * (1 - dist / 80);
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(n.x, n.y);
          ctx.strokeStyle = `rgba(255, 187, 0, ${alpha})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }

    // Hover detection
    let closestParticle = null;
    let closestDist = Infinity;

    // Render particles
    for (const p of projected) {
      const pp = p.particle;
      const breath = 0.85 + 0.15 * Math.sin(pp.age * 0.02 + pp.pulsePhase);
      const r = pp.radius * breath * p.scale;
      const c = pp.color;
      const sr = Math.min(255, Math.floor(c.r * p.scale));
      const sg = Math.min(255, Math.floor(c.g * p.scale));
      const sb = Math.min(255, Math.floor(c.b * p.scale));
      const alpha = Math.min(0.9, Math.max(0.2, p.scale * 0.8));

      // Glow layers
      for (let i = 0; i < 4; i++) {
        const glowR = r * [1, 0.5, 0.25, 0.12][i];
        const glowA = alpha * [0.08, 0.15, 0.3, 0.6][i];
        if (glowR < 0.5) continue;
        ctx.beginPath();
        ctx.arc(p.x, p.y, glowR, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${sr}, ${sg}, ${sb}, ${glowA})`;
        ctx.fill();
      }

      // Core
      ctx.beginPath();
      ctx.arc(p.x, p.y, r * 0.6, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${Math.min(255, sr + 40)}, ${Math.min(255, sg + 40)}, ${Math.min(255, sb + 40)}, 1)`;
      ctx.fill();

      // Bright particles extra glow
      if (pp.isBright) {
        ctx.save();
        ctx.shadowBlur = 20;
        ctx.shadowColor = 'rgba(255, 187, 0, 0.4)';
        ctx.beginPath();
        ctx.arc(p.x, p.y, r * 0.5, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 220, 80, 0.8)';
        ctx.fill();
        ctx.restore();
      }

      // Alternate color extra pulse
      if (pp.type === 'alternate') {
        const pulseR = r * (1.5 + 0.5 * Math.sin(pp.age * 0.05));
        ctx.beginPath();
        ctx.arc(p.x, p.y, pulseR, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(212, 36, 36, ${0.05 * alpha})`;
        ctx.fill();
      }

      // Hover detection
      const hdx = p.x - this.mouse.x;
      const hdy = p.y - this.mouse.y;
      const hdist = Math.sqrt(hdx * hdx + hdy * hdy);
      if (hdist < 20 && hdist < closestDist) {
        closestDist = hdist;
        closestParticle = { ...pp, px: p.x, py: p.y };
      }
    }

    // Tooltip
    if (closestParticle && this.tooltip) {
      this.hoveredParticle = closestParticle;
      this.tooltip.style.opacity = '1';
      this.tooltip.style.left = (this.mouse.x + 15) + 'px';
      this.tooltip.style.top = (this.mouse.y + 15) + 'px';
      this.tooltip.innerHTML = `
        <div style="color:#F6C604;font-weight:bold;margin-bottom:4px;">粒子 #${closestParticle.id}</div>
        <div style="font-size:11px;color:#888;">类型: ${closestParticle.type === 'bright' ? '亮色' : closestParticle.type === 'dim' ? '暗色' : '交替'}</div>
        <div style="font-size:11px;color:#888;">坐标: ${Math.round(closestParticle.x)}, ${Math.round(closestParticle.y)}, ${Math.round(closestParticle.z)}</div>
        <div style="font-size:11px;color:#888;">尺寸: ${closestParticle.radius.toFixed(1)}</div>
        <div style="font-size:11px;color:#888;">状态: ${closestParticle.age < closestParticle.lifespan * 0.5 ? '生长' : '衰减'}</div>
      `;
    } else {
      this.hoveredParticle = null;
      if (this.tooltip) this.tooltip.style.opacity = '0';
    }
  }

  destroy() {
    if (this.animFrame) cancelAnimationFrame(this.animFrame);
  }
}

// —— 星空粒子 ——
class StarField {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.container = this.canvas.parentElement;
    this.dpr = window.devicePixelRatio || 1;
    this.stars = [];
    this.animFrame = null;

    this.resize();
    this.initStars();
    this.bindEvents();
    this.start();
  }

  resize() {
    const w = this.container.clientWidth;
    const h = this.container.clientHeight;
    this.canvas.width = w * this.dpr;
    this.canvas.height = h * this.dpr;
    this.ctx.scale(this.dpr, this.dpr);
    this.width = w;
    this.height = h;
  }

  initStars() {
    this.stars = [];
    for (let i = 0; i < 50; i++) {
      this.stars.push({
        x: Math.random() * this.width,
        y: Math.random() * this.height,
        size: Math.random() * 2,
        speedY: -0.1 - Math.random() * 0.3,
        opacity: Math.random(),
        opacitySpeed: 0.005 + Math.random() * 0.01,
      });
    }
  }

  bindEvents() {
    window.addEventListener('resize', () => {
      this.ctx.setTransform(1, 0, 0, 1, 0, 0);
      this.resize();
    });
  }

  start() {
    this.loop();
  }

  loop() {
    this.update();
    this.render();
    this.animFrame = requestAnimationFrame(() => this.loop());
  }

  update() {
    for (const s of this.stars) {
      s.y += s.speedY;
      if (s.y < 0) {
        s.y = this.height;
        s.x = Math.random() * this.width;
      }
      s.opacity += s.opacitySpeed;
      if (s.opacity > 1 || s.opacity < 0) {
        s.opacitySpeed *= -1;
      }
    }
  }

  render() {
    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.width, this.height);

    for (const s of this.stars) {
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(246, 198, 4, ${s.opacity * 0.6})`;
      ctx.fill();
    }
  }

  destroy() {
    if (this.animFrame) cancelAnimationFrame(this.animFrame);
  }
}

// —— 初始化 ——
document.addEventListener('DOMContentLoaded', () => {
  // Main particle system
  const mainCanvas = document.getElementById('cn-canvas-main');
  if (mainCanvas) {
    window.particleSystem = new ParticleSystem('cn-canvas-main');
  }

  // Star field
  const starCanvas = document.getElementById('cn-canvas-stars');
  if (starCanvas) {
    window.starField = new StarField('cn-canvas-stars');
  }
});
