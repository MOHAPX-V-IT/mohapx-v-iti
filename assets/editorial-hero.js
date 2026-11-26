/* Pointer parallax from the supplied Elias reference. No scroll hijacking. */
(() => {
  const hero = document.querySelector('.editorial-hero');
  if (!hero) return;
  const portrait = hero.querySelector('.editorial-portrait');
  const name = hero.querySelector('#heroTitle');
  const outline = document.createElement('div');
  outline.className = 'editorial-name editorial-name-outline';
  outline.setAttribute('aria-hidden', 'true');
  outline.innerHTML = name.innerHTML;
  name.after(outline);
  const alignName = () => hero.style.setProperty('--name-top', `${name.offsetTop}px`);
  new ResizeObserver(alignName).observe(name);
  alignName();
  const allowed = matchMedia('(hover: hover) and (pointer: fine) and (min-width: 1001px)');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let frame = 0;
  const reset = () => {
    cancelAnimationFrame(frame);
    hero.style.setProperty('--hero-dx', '0px');
    hero.style.setProperty('--hero-dy', '0px');
    hero.classList.remove('is-pointing');
  };
  hero.addEventListener('pointermove', event => {
    if (!allowed.matches || reduced.matches || event.pointerType === 'touch') return;
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(() => {
      const rect = hero.getBoundingClientRect();
      const x = ((event.clientX - rect.left) / rect.width - .5) * 16;
      const y = ((event.clientY - rect.top) / rect.height - .5) * 12;
      hero.style.setProperty('--hero-dx', `${x.toFixed(2)}px`);
      hero.style.setProperty('--hero-dy', `${y.toFixed(2)}px`);
      hero.style.setProperty('--name-spot-x', `${event.clientX - rect.left}px`);
      hero.style.setProperty('--name-spot-y', `${event.clientY - rect.top - name.offsetTop}px`);
      const photo = portrait.getBoundingClientRect();
      portrait.style.setProperty('--spot-x', `${event.clientX - photo.left}px`);
      portrait.style.setProperty('--spot-y', `${event.clientY - photo.top}px`);
      hero.classList.add('is-pointing');
    });
  }, { passive: true });
  hero.addEventListener('pointerleave', reset);
  allowed.addEventListener('change', reset);
  reduced.addEventListener('change', reset);
  const updatePhoto = () => { portrait.querySelector('img').alt = document.documentElement.lang === 'en' ? 'Aleksei Maryshev' : 'Алексей Марышев'; };
  new MutationObserver(updatePhoto).observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
  updatePhoto();
})();
