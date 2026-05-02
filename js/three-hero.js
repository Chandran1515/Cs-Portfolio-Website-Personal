export function initThreeHero() {
  const container = document.getElementById('three-canvas-container');
  if (!container || typeof THREE === 'undefined') return;

  const scene = new THREE.Scene();
  // Optional: add subtle fog for depth
  scene.fog = new THREE.FogExp2(0x050505, 0.002);

  const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 15;
  camera.position.y = 5;

  const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(renderer.domElement);

  // Group for all architectural lines
  const group = new THREE.Group();
  scene.add(group);

  // Material for gold/dim wireframes
  const material = new THREE.LineBasicMaterial({
    color: 0xc4973a,
    transparent: true,
    opacity: 0.15
  });

  const materialBright = new THREE.LineBasicMaterial({
    color: 0xe8c97a,
    transparent: true,
    opacity: 0.3
  });

  // Create abstract buildings/grids
  const gridSize = 40;
  const gridDivisions = 40;
  const gridHelper = new THREE.GridHelper(gridSize, gridDivisions, 0xc4973a, 0xffffff);
  gridHelper.material.transparent = true;
  gridHelper.material.opacity = 0.05;
  gridHelper.position.y = -5;
  scene.add(gridHelper);

  // Generate random buildings
  for (let i = 0; i < 50; i++) {
    const w = Math.random() * 2 + 0.5;
    const h = Math.random() * 8 + 2;
    const d = Math.random() * 2 + 0.5;
    const geometry = new THREE.BoxGeometry(w, h, d);
    const edges = new THREE.EdgesGeometry(geometry);
    
    // Mix of bright and dim lines
    const mat = Math.random() > 0.8 ? materialBright : material;
    const line = new THREE.LineSegments(edges, mat);
    
    line.position.x = (Math.random() - 0.5) * 30;
    line.position.z = (Math.random() - 0.5) * 30;
    line.position.y = h / 2 - 5;
    
    group.add(line);
  }

  // Interactivity vars
  let mouseX = 0;
  let mouseY = 0;
  let targetX = 0;
  let targetY = 0;
  const windowHalfX = window.innerWidth / 2;
  const windowHalfY = window.innerHeight / 2;

  document.addEventListener('mousemove', (event) => {
    mouseX = (event.clientX - windowHalfX);
    mouseY = (event.clientY - windowHalfY);
  });

  // Scroll effect on camera
  let scrollY = 0;
  window.addEventListener('scroll', () => {
    scrollY = window.scrollY;
  });

  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });

  const clock = new THREE.Clock();

  function animate() {
    requestAnimationFrame(animate);

    const delta = clock.getDelta();
    
    // Slow rotation
    group.rotation.y += 0.05 * delta;

    // Mouse interactivity (parallax)
    targetX = mouseX * 0.001;
    targetY = mouseY * 0.001;
    
    camera.position.x += (targetX * 5 - camera.position.x) * 0.02;
    camera.position.y += (-targetY * 5 + 5 - camera.position.y) * 0.02;
    
    // Add scroll effect to camera Z and Y
    const targetZ = 15 + scrollY * 0.01;
    camera.position.z += (targetZ - camera.position.z) * 0.05;
    
    camera.lookAt(scene.position);

    renderer.render(scene, camera);
  }

  animate();
}
