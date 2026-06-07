// 龍魂粒子系统容器
// DNA: #龍芯⚡️2026-06-04-PARTICLE-CONTAINER-v1.0

import React, { useEffect, useRef } from 'react'
import * as THREE from 'three'

export const ParticleContainer: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null)
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null)
  const sceneRef = useRef<THREE.Scene | null>(null)
  const particlesRef = useRef<THREE.Points | null>(null)

  useEffect(() => {
    if (!containerRef.current) return

    // 初始化 Three.js
    const width = window.innerWidth
    const height = window.innerHeight

    // 场景
    const scene = new THREE.Scene()
    sceneRef.current = scene

    // 摄像机
    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000)
    camera.position.z = 50

    // 渲染器
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true })
    renderer.setSize(width, height)
    renderer.setClearColor(0x000000, 0)
    containerRef.current.appendChild(renderer.domElement)
    rendererRef.current = renderer

    // 粒子几何体
    const particleCount = 1000
    const geometry = new THREE.BufferGeometry()
    const positions = new Float32Array(particleCount * 3)

    for (let i = 0; i < particleCount; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 100 // X
      positions[i * 3 + 1] = Math.random() * 100 // Y
      positions[i * 3 + 2] = (Math.random() - 0.5) * 100 // Z
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))

    // 粒子材质
    const material = new THREE.PointsMaterial({
      color: 0xff1493,
      size: 0.5,
      sizeAttenuation: true,
      transparent: true,
      opacity: 0.6,
    })

    // 粒子网格
    const particles = new THREE.Points(geometry, material)
    scene.add(particles)
    particlesRef.current = particles

    // 动画循环
    let animationId: number

    const animate = () => {
      animationId = requestAnimationFrame(animate)

      // 粒子上升动画
      const positions = geometry.attributes.position.array as Float32Array
      for (let i = 1; i < positions.length; i += 3) {
        positions[i] += 0.3 // Y 轴上升速度

        // 重置到底部
        if (positions[i] > 100) {
          positions[i] = -50
        }
      }
      geometry.attributes.position.needsUpdate = true

      // 旋转
      particles.rotation.z += 0.0001

      renderer.render(scene, camera)
    }

    animate()

    // 处理窗口缩放
    const handleResize = () => {
      const newWidth = window.innerWidth
      const newHeight = window.innerHeight

      camera.aspect = newWidth / newHeight
      camera.updateProjectionMatrix()
      renderer.setSize(newWidth, newHeight)
    }

    window.addEventListener('resize', handleResize)

    // 清理
    return () => {
      window.removeEventListener('resize', handleResize)
      cancelAnimationFrame(animationId)
      containerRef.current?.removeChild(renderer.domElement)
      geometry.dispose()
      material.dispose()
      renderer.dispose()
    }
  }, [])

  return (
    <div
      ref={containerRef}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        zIndex: 0,
        pointerEvents: 'none',
      }}
    />
  )
}
