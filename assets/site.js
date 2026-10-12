/* Theme, language and keyboard-accessible navigation. No scroll hijacking. */
(() => {
  const root = document.documentElement;
  const menuButton = document.getElementById('menuBtn');
  const menu = document.getElementById('siteMenu');
  const langButton = document.getElementById('langBtn');
  const themeButton = document.getElementById('themeBtn');
  const themeMeta = document.querySelector('meta[name="theme-color"]');
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  let menuOpen = !menu.hidden;
  let menuAnimation;
  let themeTimer;
  const settleDisclosures = [];
  const save = (key,value) => { try { localStorage.setItem(key,value); } catch {} };

  const updateLabels = () => {
    const en = root.lang === 'en';
    document.getElementById('langA').textContent = root.lang.toUpperCase();
    langButton.setAttribute('aria-label',en ? 'Переключить на русский' : 'Switch to English');
    const light = root.dataset.theme === 'light';
    themeButton.setAttribute('aria-label',en ? `Switch to ${light ? 'dark' : 'light'} theme` : `Включить ${light ? 'тёмную' : 'светлую'} тему`);
    themeButton.setAttribute('aria-pressed',String(light));
    themeMeta.content = light ? '#F4F2EE' : '#09090C';
    document.getElementById('nav').setAttribute('aria-label',en ? 'Main navigation' : 'Основная навигация');
    menuButton.setAttribute('aria-label',menuOpen ? (en ? 'Close menu' : 'Закрыть меню') : (en ? 'Open menu' : 'Открыть меню'));
    const portrait = document.querySelector('.portrait img');
    if (portrait) portrait.alt = en ? 'Aleksei Maryshev' : 'Алексей Марышев';
    document.title = root.querySelector('body').dataset.page === 'calculator'
      ? (en ? 'AI solution payback calculator — MOHAPX-V-IT' : 'Калькулятор окупаемости AI-решения — MOHAPX-V-IT')
      : (en ? 'MOHAPX-V-IT — Aleksei Maryshev, AI Forward Deployed Engineer' : 'MOHAPX-V-IT — Алексей Марышев, AI Forward Deployed Engineer');
    if (typeof window.__onLang === 'function') window.__onLang();
  };
  themeButton.addEventListener('click',() => {
    clearTimeout(themeTimer);
    root.classList.toggle('theme-changing',!reducedMotion.matches);
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    save('mvi-theme',root.dataset.theme);
    updateLabels();
    themeTimer = setTimeout(() => root.classList.remove('theme-changing'),320);
  });
  langButton.addEventListener('click',() => {
    root.lang = root.lang === 'ru' ? 'en' : 'ru';
    save('mvi-lang',root.lang);
    updateLabels();
  });

  const setMenu = (open,returnFocus = false) => {
    if (open === menuOpen) return;
    menuOpen = open;
    const visible = !menu.hidden;
    const current = visible ? getComputedStyle(menu) : null;
    const from = current ? {opacity:current.opacity,transform:current.transform} : {opacity:0,transform:'translateY(-10px)'};
    if (menuAnimation) menuAnimation.cancel();
    menu.hidden = false;
    menu.inert = !open;
    menuButton.setAttribute('aria-expanded',String(open));
    menuButton.setAttribute('aria-label',open ? (root.lang === 'en' ? 'Close menu' : 'Закрыть меню') : (root.lang === 'en' ? 'Open menu' : 'Открыть меню'));
    if (returnFocus) menuButton.focus();
    if (reducedMotion.matches || !menu.animate) {
      menu.hidden = !open;
      return;
    }
    menuAnimation = menu.animate([from,{opacity:open ? 1 : 0,transform:open ? 'translateY(0)' : 'translateY(-8px)'}],{
      duration:open ? 300 : 180,easing:'cubic-bezier(.16,1,.3,1)',fill:'both'
    });
    const active = menuAnimation;
    active.finished.then(() => {
      if (menuAnimation !== active) return;
      menu.hidden = !menuOpen;
      active.cancel();
      menuAnimation = null;
    }).catch(() => {}); // Cancellation is normal when the visitor reverses direction.
  };
  menuButton.addEventListener('click',() => setMenu(!menuOpen));
  menu.querySelectorAll('a').forEach(link => link.addEventListener('click',() => setMenu(false)));
  document.addEventListener('keydown',event => {
    if (event.key === 'Escape' && menuOpen) setMenu(false,true);
  });
  document.addEventListener('click',event => {
    if (menuOpen && !event.target.closest('.site-header')) setMenu(false);
  });
  document.addEventListener('focusin',event => {
    if (menuOpen && !event.target.closest('.site-header')) setMenu(false);
  });

  // Native details remain usable without JS. A grid tracks natural content
  // size across language changes and resizing, and reverses without height jumps.
  if (CSS.supports('grid-template-rows','0fr')) {
    document.querySelectorAll('details.project,.faq details').forEach(detail => {
      const summary = detail.querySelector('summary');
      if (!summary) return;
      const panel = document.createElement('div');
      const content = document.createElement('div');
      panel.className = 'disclosure-panel';
      content.className = 'disclosure-content';
      while (summary.nextSibling) content.append(summary.nextSibling);
      panel.append(content);
      detail.append(panel);
      let expanded = detail.open;
      let closeTimer;
      detail.dataset.expanded = String(expanded);
      summary.setAttribute('aria-expanded',String(expanded));
      content.inert = !expanded;
      const settle = () => {
        clearTimeout(closeTimer);
        closeTimer = undefined;
        detail.open = expanded;
      };
      settleDisclosures.push(settle);
      summary.addEventListener('click',event => {
        event.preventDefault();
        expanded = !expanded;
        clearTimeout(closeTimer);
        closeTimer = undefined;
        if (expanded && !detail.open) {
          detail.open = true;
          panel.getBoundingClientRect(); // Establish the collapsed grid before its transition.
        }
        detail.dataset.expanded = String(expanded);
        summary.setAttribute('aria-expanded',String(expanded));
        content.inert = !expanded;
        if (reducedMotion.matches) settle();
        else if (!expanded) closeTimer = setTimeout(settle,290);
      });
      panel.addEventListener('transitionend',event => {
        if (event.target === panel && event.propertyName === 'grid-template-rows' && !expanded) settle();
      });
      // Browser find-in-page and external code may open native details directly.
      detail.addEventListener('toggle',() => {
        if (detail.open !== expanded && !closeTimer) {
          expanded = detail.open;
          detail.dataset.expanded = String(expanded);
          summary.setAttribute('aria-expanded',String(expanded));
          content.inert = !expanded;
        }
      });
    });
  }
  reducedMotion.addEventListener('change',() => {
    if (!reducedMotion.matches) return;
    if (menuAnimation) { menuAnimation.cancel(); menuAnimation = null; }
    menu.hidden = !menuOpen;
    root.classList.remove('theme-changing');
    settleDisclosures.forEach(settle => settle());
  });
  updateLabels();
})();
