/**
 * 龍魂五行計算器 · Three.js 流場動畫
 *
 * 🐉 DNA:#龍芯⚡️2026-06-07-WUXING-FLOW-FIELD-v3.5
 * 責任: UID9622 · 不免責
 */

import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

interface WuxingFlowFieldProps {
  activeRiver?: string | null;
  wuxing?: 'metal' | 'wood' | 'water' | 'fire' | 'earth';
  speed?: number;
}

/**
 * 五行流場動畫組件
 *
 * 使用 Three.js 渲染實時水流動畫效果
 */
export const WuxingFlowField: React.FC<WuxingFlowFieldProps> = ({
  activeRiver,
  wuxing = 'water',
  speed = 1,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const particlesRef = useRef<THREE.Points | null>(null);
  const animationIdRef = useRef<number | null>(null);

  // 五行對應的顏色
  const wuxingColors: Record<string, THREE.Color> = {
    metal: new THREE.Color(0xFFD700), // 金 - 黃金色
    wood: new THREE.Color(0x90EE90),  // 木 - 綠色
    water: new THREE.Color(0x87CEEB), // 水 - 藍色
    fire: new THREE.Color(0xFF6347),  // 火 - 紅色
    earth: new THREE.Color(0xCD853F), // 土 - 棕色
  };

  useEffect(() => {
    if (!containerRef.current) return;

    // ========================================================================
    // [場景初始化]
    // ========================================================================

    const width = containerRef.current.clientWidth;
    const height = containerRef.current.clientHeight;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0f172a); // 深藍黑色

    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    camera.position.z = 5;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio);
    containerRef.current.appendChild(renderer.domElement);

    sceneRef.current = scene;
    rendererRef.current = renderer;

    // ========================================================================
    // [粒子系統]
    // ========================================================================

    const particleCount = 2000;
    const geometry = new THREE.BufferGeometry();

    const positions = new Float32Array(particleCount * 3);
    const velocities = new Float32Array(particleCount * 3);

    // 初始化粒子位置和速度
    for (let i = 0; i < particleCount * 3; i += 3) {
      // 位置: 隨機分佈在立方體內
      positions[i] = (Math.random() - 0.5) * 10;      // x
      positions[i + 1] = (Math.random() - 0.5) * 10;  // y
      positions[i + 2] = (Math.random() - 0.5) * 10;  // z

      // 速度: 根據河道方向設定
      const velScale = 0.02 * speed;
      velocities[i] = (Math.random() - 0.5) * velScale;     // vx
      velocities[i + 1] = (Math.random() - 0.5) * velScale; // vy
      velocities[i + 2] = (Math.random() - 0.5) * velScale; // vz
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('velocity', new THREE.BufferAttribute(velocities, 3));

    // 材質: 使用點材質
    const color = wuxingColors[wuxing] || wuxingColors.water;
    const material = new THREE.PointsMaterial({
      color: color,
      size: 0.05,
      transparent: true,
      opacity: 0.6,
      sizeAttenuation: true,
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);
    particlesRef.current = particles;

    // ========================================================================
    // [流場力場計算]
    // ========================================================================

    const perlinNoise = (x: number, y: number, z: number): number => {
      // 簡化版 Perlin 噪聲 (實際可使用 noise.js 庫)
      return Math.sin(x * 0.5) * Math.cos(y * 0.5) + Math.sin(z * 0.3);
    };

    // ========================================================================
    // [動畫循環]
    // ========================================================================

    let time = 0;

    const animate = () => {
      animationIdRef.current = requestAnimationFrame(animate);

      time += 0.01 * speed;

      const positionArray = geometry.attributes.position.array as Float32Array;
      const velocityArray = geometry.attributes.velocity.array as Float32Array;

      // 更新每個粒子
      for (let i = 0; i < particleCount * 3; i += 3) {
        const x = positionArray[i];
        const y = positionArray[i + 1];
        const z = positionArray[i + 2];

        // 計算流場力
        const forceX = perlinNoise(x + time, y, z) * 0.01;
        const forceY = perlinNoise(x, y + time, z) * 0.01;
        const forceZ = perlinNoise(x, y, z + time) * 0.01;

        // 更新速度 (施加力)
        velocityArray[i] += forceX;
        velocityArray[i + 1] += forceY;
        velocityArray[i + 2] += forceZ;

        // 阻尼 (速度衰減)
        velocityArray[i] *= 0.98;
        velocityArray[i + 1] *= 0.98;
        velocityArray[i + 2] *= 0.98;

        // 更新位置
        positionArray[i] += velocityArray[i];
        positionArray[i + 1] += velocityArray[i + 1];
        positionArray[i + 2] += velocityArray[i + 2];

        // 邊界反彈
        const bound = 5;
        if (positionArray[i] > bound) positionArray[i] = -bound;
        if (positionArray[i] < -bound) positionArray[i] = bound;
        if (positionArray[i + 1] > bound) positionArray[i + 1] = -bound;
        if (positionArray[i + 1] < -bound) positionArray[i + 1] = bound;
        if (positionArray[i + 2] > bound) positionArray[i + 2] = -bound;
        if (positionArray[i + 2] < -bound) positionArray[i + 2] = bound;
      }

      geometry.attributes.position.needsUpdate = true;
      geometry.attributes.velocity.needsUpdate = true;

      // 旋轉視角
      particles.rotation.x += 0.0005;
      particles.rotation.y += 0.0008;

      renderer.render(scene, camera);
    };

    animate();

    // ========================================================================
    // [處理窗口縮放]
    // ========================================================================

    const handleResize = () => {
      if (!containerRef.current) return;

      const newWidth = containerRef.current.clientWidth;
      const newHeight = containerRef.current.clientHeight;

      camera.aspect = newWidth / newHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(newWidth, newHeight);
    };

    window.addEventListener('resize', handleResize);

    // ========================================================================
    // [清理]
    // ========================================================================

    return () => {
      window.removeEventListener('resize', handleResize);

      if (animationIdRef.current) {
        cancelAnimationFrame(animationIdRef.current);
      }

      if (containerRef.current && renderer.domElement.parentNode === containerRef.current) {
        containerRef.current.removeChild(renderer.domElement);
      }

      geometry.dispose();
      material.dispose();
      renderer.dispose();
    };
  }, [wuxing, speed]);

  return (
    <div
      ref={containerRef}
      style={{
        width: '100%',
        height: '400px',
        borderRadius: '8px',
        overflow: 'hidden',
        marginTop: '20px',
      }}
    />
  );
};

// ========================================================================
// [預設場景]
// ========================================================================

export const WuxingFlowFieldPresets = {
  // 金流場 - 秋季之氣·肅殺·收斂
  metal: (
    <WuxingFlowField
      wuxing="metal"
      speed={0.8}
    />
  ),

  // 木流場 - 春季之氣·生長·展開
  wood: (
    <WuxingFlowField
      wuxing="wood"
      speed={1.2}
    />
  ),

  // 水流場 - 冬季之氣·潤澤·下行
  water: (
    <WuxingFlowField
      wuxing="water"
      speed={1.0}
    />
  ),

  // 火流場 - 夏季之氣·炎上·向上
  fire: (
    <WuxingFlowField
      wuxing="fire"
      speed={1.3}
    />
  ),

  // 土流場 - 中央之氣·承載·居中
  earth: (
    <WuxingFlowField
      wuxing="earth"
      speed={0.9}
    />
  ),
};

export default WuxingFlowField;
