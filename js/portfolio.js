import { initCursor } from './cursor.js';

document.addEventListener('DOMContentLoaded', () => {
  initCursor();

  // Reveal
  const obs = new IntersectionObserver(entries => { 
    entries.forEach(e => { 
      if(e.isIntersecting){ e.target.classList.add('visible'); obs.unobserve(e.target); } 
    }); 
  }, {threshold:0.08});
  document.querySelectorAll('.reveal').forEach(el => obs.observe(el));

  // Filters
  const filterMap = {
    paloalto: ['g-paloalto'],
    monterey: ['g-monterey'],
    orangecounty: ['g-orangecounty'],
    bim:      ['g-bim']
  };
  const allGroups = ['g-paloalto','g-monterey','g-orangecounty','g-bim','g-expertise'];
  const extraEls = document.querySelectorAll('.expertise-grid, .geo-grid, .spacer, .category-label:not([id])');

  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const f = btn.dataset.filter;

      if(f === 'all'){
        allGroups.forEach(id => { const el = document.getElementById(id); if(el){ el.style.display=''; el.nextElementSibling && (el.nextElementSibling.style.display=''); } });
        extraEls.forEach(el => el.style.display='');
        document.getElementById('fc').textContent='Showing CS Revit Labs (15 tools) + 15 projects';
      } else {
        // Hide all groups first
        allGroups.forEach(id => {
          const el = document.getElementById(id);
          if(el){
            el.style.display='none';
            let sib = el.nextElementSibling;
            while(sib && !sib.id){ sib.style.display='none'; sib=sib.nextElementSibling; }
          }
        });
        extraEls.forEach(el => el.style.display='none');

        // Show selected
        const toShow = f === 'bim' ? ['g-bim'] : filterMap[f]||[];
        toShow.forEach(id => {
          const el = document.getElementById(id);
          if(el){
            el.style.display='';
            let sib = el.nextElementSibling;
            while(sib && !sib.id){ sib.style.display=''; sib=sib.nextElementSibling; }
          }
        });
        const counts = {paloalto:'1 project', monterey:'13 projects', orangecounty:'1 project', bim:'CS Revit Labs (15 tools)'};
        document.getElementById('fc').textContent = 'Showing ' + counts[f];
      }
    });
  });

  // Auto Horizontal Scroll for Galleries
  const galleries = document.querySelectorAll('.doc-gallery');
  const galleryObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      entry.target.isIntersectingVisible = entry.isIntersecting;
    });
  }, { rootMargin: '50px' });

  galleries.forEach(gallery => {
    let isDown = false;
    let isHovered = false;
    let scrollSpeed = 0.6; // pixels per frame
    gallery.isIntersectingVisible = false;
    galleryObserver.observe(gallery);

    gallery.addEventListener('mouseenter', () => isHovered = true);
    gallery.addEventListener('mouseleave', () => {
      isHovered = false;
      isDown = false;
    });
    
    gallery.addEventListener('mousedown', () => isDown = true);
    gallery.addEventListener('mouseup', () => isDown = false);
    gallery.addEventListener('touchstart', () => isDown = true);
    gallery.addEventListener('touchend', () => isDown = false);

    function autoScroll() {
      if (!isHovered && !isDown && gallery.isIntersectingVisible) {
        gallery.scrollLeft += scrollSpeed;
        if (gallery.scrollLeft >= (gallery.scrollWidth - gallery.clientWidth - 1)) {
          scrollSpeed = -0.6;
        } else if (gallery.scrollLeft <= 0) {
          scrollSpeed = 0.6;
        }
      }
      requestAnimationFrame(autoScroll);
    }
    
    requestAnimationFrame(autoScroll);
  });

  // Lightbox Functionality (Pan & Zoom)
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  const lightboxClose = document.querySelector('.lightbox-close');

  if (lightbox && lightboxImg) {
    let scale = 1;
    let pointX = 0;
    let pointY = 0;
    let start = { x: 0, y: 0 };
    let panning = false;

    function setTransform() {
      // translateZ(0) forces hardware acceleration for crispness during zoom
      lightboxImg.style.transform = `translate(${pointX}px, ${pointY}px) scale(${scale}) translateZ(0)`;
    }

    function resetTransform() {
      scale = 1;
      pointX = 0;
      pointY = 0;
      setTransform();
      lightboxImg.style.cursor = 'zoom-in';
    }

    // Open lightbox
    document.querySelectorAll('.doc-img, .project-cover, .labs-tool-img, .labs-tool-img-container, .labs-tool-video-area').forEach(element => {
      element.addEventListener('click', (e) => {
        e.stopPropagation();
        let img = element;
        if (element.tagName.toLowerCase() !== 'img') {
          img = element.querySelector('img');
        }
        if (!img || !img.src) return;
        
        resetTransform();
        lightboxImg.src = img.src;
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
      });
    });

    // Close lightbox
    const closeLightbox = () => {
      lightbox.classList.remove('active');
      document.body.style.overflow = '';
      setTimeout(() => { lightboxImg.src = ''; resetTransform(); }, 300);
    };

    lightboxClose.addEventListener('click', closeLightbox);
    
    // Zoom with scroll wheel
    lightbox.addEventListener('wheel', (e) => {
      e.preventDefault();
      const xs = (e.clientX - pointX) / scale;
      const ys = (e.clientY - pointY) / scale;
      const delta = (e.wheelDelta ? e.wheelDelta : -e.deltaY);
      
      (delta > 0) ? (scale *= 1.2) : (scale /= 1.2);
      
      // Limits (zoom out up to 0.8x, zoom in up to 5x)
      scale = Math.min(Math.max(0.8, scale), 5);
      
      pointX = e.clientX - xs * scale;
      pointY = e.clientY - ys * scale;

      // Snap back to center if scale is ~1
      if (scale <= 1.05 && scale >= 0.95) {
        scale = 1;
        pointX = 0;
        pointY = 0;
      }

      lightboxImg.style.cursor = scale > 1 ? 'grab' : 'zoom-in';
      setTransform();
    }, { passive: false });

    // Panning (Mouse)
    lightboxImg.onmousedown = function(e) {
      e.preventDefault();
      if(scale <= 1) return;
      start = { x: e.clientX - pointX, y: e.clientY - pointY };
      panning = true;
      lightboxImg.style.cursor = 'grabbing';
    };

    lightboxImg.onmouseup = function(e) {
      panning = false;
      lightboxImg.style.cursor = scale > 1 ? 'grab' : 'zoom-in';
    };

    lightboxImg.onmouseleave = function(e) {
      panning = false;
      lightboxImg.style.cursor = scale > 1 ? 'grab' : 'zoom-in';
    };

    lightboxImg.onmousemove = function(e) {
      e.preventDefault();
      if (!panning || scale <= 1) return;
      pointX = (e.clientX - start.x);
      pointY = (e.clientY - start.y);
      setTransform();
    };

    // Panning (Touch)
    let initialPinchDistance = null;

    lightboxImg.addEventListener('touchstart', (e) => {
      if(e.touches.length === 1) {
        if(scale <= 1) return;
        start = { x: e.touches[0].clientX - pointX, y: e.touches[0].clientY - pointY };
        panning = true;
      } else if (e.touches.length === 2) {
        panning = false;
        initialPinchDistance = Math.hypot(
          e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY
        );
      }
    }, {passive: false});

    lightboxImg.addEventListener('touchmove', (e) => {
      e.preventDefault(); // Prevent page scroll
      if (e.touches.length === 1 && panning && scale > 1) {
        pointX = (e.touches[0].clientX - start.x);
        pointY = (e.touches[0].clientY - start.y);
        setTransform();
      } else if (e.touches.length === 2 && initialPinchDistance) {
        const currentDistance = Math.hypot(
          e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY
        );
        
        // Calculate center of pinch
        const cx = (e.touches[0].clientX + e.touches[1].clientX) / 2;
        const cy = (e.touches[0].clientY + e.touches[1].clientY) / 2;

        const xs = (cx - pointX) / scale;
        const ys = (cy - pointY) / scale;

        // Apply scale change
        const scaleChange = currentDistance / initialPinchDistance;
        scale *= scaleChange;
        scale = Math.min(Math.max(0.8, scale), 5);

        pointX = cx - xs * scale;
        pointY = cy - ys * scale;
        
        if (scale <= 1.05 && scale >= 0.95) {
          scale = 1;
          pointX = 0;
          pointY = 0;
        }

        setTransform();
        initialPinchDistance = currentDistance; // Update for continuous pinch
      }
    }, {passive: false});

    lightboxImg.addEventListener('touchend', (e) => {
      panning = false;
      initialPinchDistance = null;
    });

    // Close on background click
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) {
        closeLightbox();
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && lightbox.classList.contains('active')) {
        closeLightbox();
      }
    });
  }
});
