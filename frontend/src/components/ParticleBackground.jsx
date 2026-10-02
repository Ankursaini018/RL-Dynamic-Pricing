import React, { useEffect, useRef } from "react";

export default function ParticleBackground() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationFrameId;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const handleResize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    window.addEventListener("resize", handleResize);

    // Deep dark purple/navy colors with occasional gold specks
    const palette = [
      "#24184a", // Deep purple
      "#1b1b3a", // Deep navy
      "#2d1b69", // Rich dark purple
      "#15102a", // Dark midnight
      "#381e72", // Muted violet
      "#ffd700", // Subtle gold speck
    ];

    // Subtle floating particles
    const particleCount = Math.min(55, Math.floor((width * height) / 26000));
    const particles = [];

    for (let i = 0; i < particleCount; i++) {
      const color = palette[Math.floor(Math.random() * palette.length)];
      const isGold = color === "#ffd700";

      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: isGold ? Math.random() * 1.4 + 0.6 : Math.random() * 2.2 + 1.0,
        color,
        alpha: isGold ? Math.random() * 0.25 + 0.12 : Math.random() * 0.3 + 0.12,
        vx: (Math.random() - 0.5) * 0.14, // slow moving
        vy: (Math.random() - 0.5) * 0.14,
        pulseSpeed: Math.random() * 0.015 + 0.004,
      });
    }

    let mouse = { x: -1000, y: -1000 };
    const handleMouseMove = (e) => {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
    };
    window.addEventListener("mousemove", handleMouseMove);

    const render = () => {
      ctx.clearRect(0, 0, width, height);

      // Draw occasional subtle connecting lines
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 95) {
            const lineAlpha = (1 - dist / 95) * 0.06;
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.strokeStyle = `rgba(156, 39, 176, ${lineAlpha})`;
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }
      }

      // Draw and update each particle
      particles.forEach((p) => {
        p.x += p.vx;
        p.y += p.vy;

        // Wrap around boundaries smoothly
        if (p.x < 0) p.x = width;
        if (p.x > width) p.x = 0;
        if (p.y < 0) p.y = height;
        if (p.y > height) p.y = 0;

        // Very gentle mouse avoidance
        const mdx = p.x - mouse.x;
        const mdy = p.y - mouse.y;
        const mDist = Math.sqrt(mdx * mdx + mdy * mdy);
        if (mDist < 100 && mDist > 0) {
          const force = (100 - mDist) / 100;
          p.x += (mdx / mDist) * force * 0.6;
          p.y += (mdy / mDist) * force * 0.6;
        }

        // Pulse alpha gently
        p.alpha += Math.sin(Date.now() * p.pulseSpeed) * 0.002;
        const currentAlpha = Math.max(0.08, Math.min(0.4, p.alpha));

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = currentAlpha;
        ctx.shadowBlur = p.color === "#ffd700" ? 6 : 4;
        ctx.shadowColor = p.color;
        ctx.fill();
        ctx.globalAlpha = 1.0;
        ctx.shadowBlur = 0;
      });

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener("resize", handleResize);
      window.removeEventListener("mousemove", handleMouseMove);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-0 opacity-70"
      style={{ background: "transparent" }}
    />
  );
}
