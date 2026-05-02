document.addEventListener('DOMContentLoaded', () => {
  // Intersection Observer for silky smooth reveal animations
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    root: null,
    rootMargin: '0px',
    threshold: 0.15
  });

  const revealElements = document.querySelectorAll('.reveal');
  revealElements.forEach(el => revealObserver.observe(el));

  // Dynamic Navigation Background
  try {
    const nav = document.querySelector('nav');
    if (nav) {
      window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
          nav.style.background = 'rgba(255, 255, 255, 0.9)';
          nav.style.boxShadow = '0 4px 20px rgba(0,0,0,0.05)';
          nav.style.padding = '1rem 3rem';
        } else {
          nav.style.background = 'rgba(255, 255, 255, 0.5)';
          nav.style.boxShadow = 'none';
          nav.style.padding = '1.5rem 3rem';
        }
      });
    }
  } catch (err) {
    console.error("Nav scroll binding error:", err);
  }
});
