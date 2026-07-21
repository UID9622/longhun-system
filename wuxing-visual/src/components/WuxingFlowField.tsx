/**
 * 龍魂五行计算器 · Three.js 流场动画
 *
 * 🐉 DNA:#龍芯⚡️2026-06-07-WUXING-FLOW-FIELD-v3.5
 * 责任: UID9622 · 不免责
 */

import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

interface WuxingFlowFieldProps {
  activeRiver?: string | null;
  wuxing?: 'metal' | 'wood' | 'water' | 'fire' | 'earth';
  speed?: number;
}

/**
 * 五行流场动画组件
 *
 * 使用 Three.js 渲染实时水流动画效果
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

  // 五行对应的颜色
  const wuxingColors: Record<string, THREE.Color> = {
    metal: new THREE.Color(0xFFD700), // 金 - 黄金色
    wood: new THREE.Color(0x90EE90),  // 木 - 绿色
    water: new THREE.Color(0x87CEEB), // 水 - 蓝色
    fire: new THREE.Color(0xFF6347),  // 火 - 红色
    earth: new THREE.Color(0xCD853F), // 土 - 棕色
  };

  useEffect(() => {
    if (!containerRef.current) return;

    // ========================================================================
    // [场景初始化]
    // ========================================================================

    const width = containerRef.current.clientWidth;
    const height = containerRef.current.clientHeight;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0f172a); // 深蓝黑色

    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    camera.position.z = 5;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio);
    containerRef.current.appendChild(renderer.domElement);

    sceneRef.current = scene;
    rendererRef.current = renderer;

    // ========================================================================
    // [粒子系统]
    // ========================================================================

    const particleCount = 2000;
    const geometry = new THREE.BufferGeometry();

    const positions = new Float32Array(particleCount * 3);
    const velocities = new Float32Array(particleCount * 3);

    // 初始化粒子位置和速度
    for (let i = 0; i < particleCount * 3; i += 3) {
      // 位置: 随机分布在立方体内
      positions[i] = (Math.random() - 0.5) * 10;      // x
      positions[i + 1] = (Math.random() - 0.5) * 10;  // y
      positions[i + 2] = (Math.random() - 0.5) * 10;  // z

      // 速度: 根据河道方向设定
      const velScale = 0.02 * speed;
      velocities[i] = (Math.random() - 0.5) * velScale;     // vx
      velocities[i + 1] = (Math.random() - 0.5) * velScale; // vy
      velocities[i + 2] = (Math.random() - 0.5) * velScale; // vz
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('velocity', new THREE.BufferAttribute(velocities, 3));

    // 材质: 使用点材质
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
    // [流场力场计算]
    // ========================================================================

    const perlinNoise = (x: number, y: number, z: number): number => {
      // 简化版 Perlin 噪声 (实际可使用 noise.js 库)
      return Math.sin(x * 0.5) * Math.cos(y * 0.5) + Math.sin(z * 0.3);
    };

    // ========================================================================
    // [动画循环]
    // ========================================================================

    let time = 0;

    const animate = () => {
      animationIdRef.current = requestAnimationFrame(animate);

      time += 0.01 * speed;

      const positionArray = geometry.attributes.position.array as Float32Array;
      const velocityArray = geometry.attributes.velocity.array as Float32Array;

      // 更新每个粒子
      for (let i = 0; i < particleCount * 3; i += 3) {
        const x = positionArray[i];
        const y = positionArray[i + 1];
        const z = positionArray[i + 2];

        // 计算流场力
        const forceX = perlinNoise(x + time, y, z) * 0.01;
        const forceY = perlinNoise(x, y + time, z) * 0.01;
        const forceZ = perlinNoise(x, y, z + time) * 0.01;

        // 更新速度 (施加力)
        velocityArray[i] += forceX;
        velocityArray[i + 1] += forceY;
        velocityArray[i + 2] += forceZ;

        // 阻尼 (速度衰减)
        velocityArray[i] *= 0.98;
        velocityArray[i + 1] *= 0.98;
        velocityArray[i + 2] *= 0.98;

        // 更新位置
        positionArray[i] += velocityArray[i];
        positionArray[i + 1] += velocityArray[i + 1];
        positionArray[i + 2] += velocityArray[i + 2];

        // 边界反弹
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

      // 旋转视角
      particles.rotation.x += 0.0005;
      particles.rotation.y += 0.0008;

      renderer.render(scene, camera);
    };

    animate();

    // ========================================================================
    // [处理窗口缩放]
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
// [预设场景]
// ========================================================================

export const WuxingFlowFieldPresets = {
  // 金流场 - 秋季之气·肃杀·收敛
  metal: (
    <WuxingFlowField
      wuxing="metal"
      speed={0.8}
    />
  ),

  // 木流场 - 春季之气·生长·展开
  wood: (
    <WuxingFlowField
      wuxing="wood"
      speed={1.2}
    />
  ),

  // 水流场 - 冬季之气·润泽·下行
  water: (
    <WuxingFlowField
      wuxing="water"
      speed={1.0}
    />
  ),

  // 火流场 - 夏季之气·炎上·向上
  fire: (
    <WuxingFlowField
      wuxing="fire"
      speed={1.3}
    />
  ),

  // 土流场 - 中央之气·承载·居中
  earth: (
    <WuxingFlowField
      wuxing="earth"
      speed={0.9}
    />
  ),
};

export default WuxingFlowField;
