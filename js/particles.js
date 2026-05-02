// 3D Particle Sphere implementation
document.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('bg-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let width, height;
  let particles = [];
  
  // Using black and red but they will be rendered with low opacity for a "light/transparent" look
  const colors = ['#000000', '#B22222', '#D32F2F', '#111111'];
  
  class Particle {
    constructor(radius) {
      // Random position on a sphere surface
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(Math.random() * 2 - 1);
      
      this.baseX = radius * Math.sin(phi) * Math.cos(theta);
      this.baseY = radius * Math.sin(phi) * Math.sin(theta);
      this.baseZ = radius * Math.cos(phi);
      
      this.color = colors[Math.floor(Math.random() * colors.length)];
      this.size = Math.random() * 2 + 1;
    }
  }

  function init() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
    particles = [];
    
    // Increase particle count for a fuller, larger sphere
    const particleCount = window.innerWidth < 768 ? 400 : 800;
    
    // Dynamic radius to fit the screen
    const radius = Math.min(width, height) * 0.45;
    
    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle(radius));
    }
  }

  let mouseX = 0;
  let mouseY = 0;
  let targetRotationX = 0;
  let targetRotationY = 0;
  let currentRotationX = 0;
  let currentRotationY = 0;

  window.addEventListener('mousemove', (e) => {
    // Calculate rotation based on mouse position relative to center
    mouseX = (e.clientX - width / 2) * 0.0005;
    mouseY = (e.clientY - height / 2) * 0.0005;
  });

  window.addEventListener('resize', init);

  function animate() {
    ctx.clearRect(0, 0, width, height);

    // Smooth rotation interpolation
    targetRotationY = mouseX * 2;
    targetRotationX = mouseY * 2;
    
    // Auto rotation if mouse is still
    currentRotationX += (targetRotationX - currentRotationX) * 0.05 + 0.001;
    currentRotationY += (targetRotationY - currentRotationY) * 0.05 + 0.002;

    const cx = width / 2;
    const cy = height / 2;

    particles.forEach(p => {
      // Rotate around X axis
      let y1 = p.baseY * Math.cos(currentRotationX) - p.baseZ * Math.sin(currentRotationX);
      let z1 = p.baseY * Math.sin(currentRotationX) + p.baseZ * Math.cos(currentRotationX);

      // Rotate around Y axis
      let x2 = p.baseX * Math.cos(currentRotationY) + z1 * Math.sin(currentRotationY);
      let z2 = -p.baseX * Math.sin(currentRotationY) + z1 * Math.cos(currentRotationY);

      // Simple perspective projection
      const perspective = 1200; // Increased perspective to flatten the huge sphere slightly
      const scale = perspective / (perspective + z2);
      
      const px = cx + x2 * scale;
      const py = cy + y1 * scale;

      // Only draw if it's "in front" of the camera
      if (z2 > -perspective) {
        ctx.beginPath();
        ctx.arc(px, py, p.size * scale, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        
        // Very subtle opacity for a light/transparent look
        ctx.globalAlpha = Math.max(0.02, Math.min(0.25, scale * 0.3));
        ctx.fill();
        ctx.globalAlpha = 1;
      }
    });

    requestAnimationFrame(animate);
  }

  init();
  animate();
});
