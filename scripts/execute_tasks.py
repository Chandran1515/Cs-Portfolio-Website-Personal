import os

base_dir = r"c:\Users\tissu\source\repos\Cs Portfolio Website"
global_css = os.path.join(base_dir, "css", "global.css")
home_css = os.path.join(base_dir, "css", "home.css")
index_html = os.path.join(base_dir, "index.html")
particles_js = os.path.join(base_dir, "js", "particles.js")

# 1. Update global.css for mobile padding, overflow, and img object-fit
with open(global_css, "r", encoding="utf-8") as f:
    g_css = f.read()

# Make sure html/body don't have conflicting overflow rules, we'll append to the end
additional_css = """
/* Phase 1 Fixes */
html, body {
  overflow-x: hidden;
  max-width: 100vw;
}

img {
  object-fit: cover;
}

@media (max-width: 768px) {
  section {
    padding-left: 20px !important;
    padding-right: 20px !important;
  }
}
"""

if "/* Phase 1 Fixes */" not in g_css:
    g_css += additional_css
    with open(global_css, "w", encoding="utf-8") as f:
        f.write(g_css)

# 2. Create particles.js
particles_code = """// 3D Particle Sphere implementation
document.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('bg-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let width, height;
  let particles = [];
  
  // Custom brand colors or monochromatic. User asked for Antigravity style (colorful) 
  // but let's stick to brand colors (Gold, Red, Green) for cohesiveness
  const colors = ['#C4973A', '#E63946', '#2A9D8F', '#1A1A1A'];
  
  class Particle {
    constructor() {
      // Random position on a sphere surface
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(Math.random() * 2 - 1);
      const r = 300; // Sphere radius
      
      this.baseX = r * Math.sin(phi) * Math.cos(theta);
      this.baseY = r * Math.sin(phi) * Math.sin(theta);
      this.baseZ = r * Math.cos(phi);
      
      this.color = colors[Math.floor(Math.random() * colors.length)];
      this.size = Math.random() * 2 + 1;
    }
  }

  function init() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
    particles = [];
    // More particles for larger screens
    const particleCount = window.innerWidth < 768 ? 200 : 500;
    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle());
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
    mouseX = (e.clientX - width / 2) * 0.001;
    mouseY = (e.clientY - height / 2) * 0.001;
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
      const perspective = 800;
      const scale = perspective / (perspective + z2);
      
      const px = cx + x2 * scale;
      const py = cy + y1 * scale;

      // Only draw if it's "in front" of the camera
      if (z2 > -perspective) {
        ctx.beginPath();
        ctx.arc(px, py, p.size * scale, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        
        // Add subtle opacity based on depth
        ctx.globalAlpha = Math.max(0.1, Math.min(1, scale));
        ctx.fill();
        ctx.globalAlpha = 1;
      }
    });

    requestAnimationFrame(animate);
  }

  init();
  animate();
});
"""
with open(particles_js, "w", encoding="utf-8") as f:
    f.write(particles_code)

# 3. Update index.html for Canvas and New Contact Section
with open(index_html, "r", encoding="utf-8") as f:
    i_html = f.read()

# Add canvas and script
if '<canvas id="bg-canvas"></canvas>' not in i_html:
    i_html = i_html.replace('<body>', '<body>\n  <canvas id="bg-canvas"></canvas>')
if '<script src="js/particles.js" defer></script>' not in i_html:
    i_html = i_html.replace('</body>', '  <script src="js/particles.js" defer></script>\n</body>')

# Replace the contact section
old_contact = """  <section id="contact" class="cta-section reveal">
    <h2 class="cta-title">Ready to move your<br>project forward?</h2>
    <div class="hero-actions">
      <a href="mailto:chandran.s.dev@gmail.com" class="btn-primary">Request Quote</a>
      <a href="mailto:chandran.s.dev@gmail.com" class="btn-secondary">Send Plans</a>
    </div>
  </section>"""

new_contact = """  <!-- 8. CONTACT & CONSULTATION (FOCUS MODE LEAD GEN) -->
  <section id="contact" class="cta-section reveal" style="background: var(--surface); padding-top: 5rem; padding-bottom: 5rem;">
    <div class="section-header" style="text-align: center; margin-bottom: 4rem;">
      <h2 class="section-title">Ready to Start?</h2>
      <p class="section-sub">Choose a high-value service below or schedule a direct consultation.</p>
    </div>

    <!-- Service Hooks -->
    <div class="bento-grid" style="margin-bottom: 4rem; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));">
      <div class="bento-card" style="text-align: center;">
        <div class="bento-icon">🔍</div>
        <h3 class="bento-title">Free Consultation</h3>
        <p class="bento-desc">15-minute technical review of your project's BIM requirements.</p>
        <a href="mailto:chandran.s.dev@gmail.com?subject=Free%20Consultation" class="btn-secondary" style="width: 100%; margin-top: 1rem; text-align: center; justify-content: center;">Claim Free Session</a>
      </div>
      <div class="bento-card" style="text-align: center;">
        <div class="bento-icon">🛡️</div>
        <h3 class="bento-title">BIM Audit</h3>
        <p class="bento-desc">A quick check of your Revit models for efficiency and code compliance.</p>
        <a href="mailto:chandran.s.dev@gmail.com?subject=BIM%20Audit" class="btn-secondary" style="width: 100%; margin-top: 1rem; text-align: center; justify-content: center;">Get an Audit</a>
      </div>
      <div class="bento-card" style="text-align: center;">
        <div class="bento-icon">⚙️</div>
        <h3 class="bento-title">Custom Automation</h3>
        <p class="bento-desc">Discuss a specific script or plugin for your firm's workflow.</p>
        <a href="mailto:chandran.s.dev@gmail.com?subject=Custom%20Automation" class="btn-secondary" style="width: 100%; margin-top: 1rem; text-align: center; justify-content: center;">Request a Tool</a>
      </div>
    </div>

    <!-- Scheduling & Deep Links -->
    <div style="background: #ffffff; border: 1px solid var(--border-dim); border-radius: 20px; padding: 4rem 2rem; max-width: 800px; margin: 0 auto; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.03);">
      <h3 style="font-family: var(--font-display); font-size: 2rem; margin-bottom: 1rem;">Let's discuss your project.</h3>
      <p style="color: var(--text-muted); margin-bottom: 2rem;">Available for calls during CA morning hours (PST) to ensure seamless project coordination.</p>
      
      <a href="mailto:chandran.s.dev@gmail.com" class="btn-primary" style="font-size: 0.9rem; padding: 1.2rem 3rem; margin-bottom: 3rem;">Book a Free 15-Min Consultation</a>

      <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 1.5rem; border-top: 1px solid var(--border-dim); padding-top: 3rem;">
        <div style="text-align: left;">
          <div style="font-family: var(--font-mono); font-size: 0.7rem; letter-spacing: 0.1em; color: var(--gold); text-transform: uppercase; margin-bottom: 0.5rem;">Direct Connect</div>
          <a href="mailto:chandran.s.dev@gmail.com" style="display: block; color: var(--text); font-weight: 600; text-decoration: none; margin-bottom: 0.5rem; transition: color 0.2s;">✉️ chandran.s.dev@gmail.com</a>
          <span style="display: block; color: var(--text); font-weight: 600; margin-bottom: 1rem;">📞 +91 79040 53633</span>
          
          <div style="display: flex; gap: 0.5rem;">
            <a href="https://wa.me/917904053633?text=Hi%20Chandran,%20I'd%20like%20to%20discuss%20a%20BIM%20project" target="_blank" class="btn-ghost" style="padding: 0.6rem 1rem; font-size: 0.65rem;">WhatsApp</a>
            <a href="sms:+917904053633" class="btn-ghost" style="padding: 0.6rem 1rem; font-size: 0.65rem;">iMessage / SMS</a>
          </div>
        </div>
      </div>
    </div>
  </section>"""

i_html = i_html.replace(old_contact, new_contact)

with open(index_html, "w", encoding="utf-8") as f:
    f.write(i_html)

# 4. Add Canvas CSS
with open(home_css, "r", encoding="utf-8") as f:
    h_css = f.read()

canvas_css = """
#bg-canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  z-index: -1;
  pointer-events: none;
  opacity: 0.6; /* subtle */
}
"""
if "#bg-canvas" not in h_css:
    h_css += canvas_css
    with open(home_css, "w", encoding="utf-8") as f:
        f.write(h_css)

print("Execution complete.")
