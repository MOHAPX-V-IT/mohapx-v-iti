/* Progressive enhancement for MOHAPX Fieldwork.
   21st.dev: Spotlight / Filter Grid / Magnetic Button / Scroll Timeline.
   All content and native disclosures work without JavaScript. */
(() => {
  'use strict';
  const root = document.documentElement;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const motionAllowed = () => !reduced.matches && root.dataset.effectsPaused !== 'true';
  const language = () => root.lang === 'en';
  const cards = [...document.querySelectorAll('#selectedCases > .case-card')];
  const filters = [...document.querySelectorAll('[data-filter]')];
  let active = 'all';
  const filterBar = document.querySelector('.project-filters');
  const grid = document.getElementById('selectedCases');
  const filterStatus = document.getElementById('filterStatus');
  const announceFilter = () => {
    const count = cards.filter(card => !card.hidden).length;
    filterStatus.textContent = language() ? `${count} selected projects shown` : `Показано избранных проектов: ${count}`;
    filterBar.setAttribute('aria-label',language() ? 'Filter selected projects' : 'Фильтр избранных проектов');
  };
  const choose = id => {
    active = id;
    filters.forEach(button => button.setAttribute('aria-pressed',String(button.dataset.filter === id)));
    cards.forEach(card => {
      const show = id === 'all' || card.dataset.category === id;
      card.hidden = !show;
      if (show && motionAllowed() && card.animate) card.animate([{opacity:.3,transform:'translateY(10px)'},{opacity:1,transform:'translateY(0)'}],{duration:300,easing:'cubic-bezier(.22,1,.36,1)'});
    });
    grid.dataset.filter = id;
    announceFilter();
  };
  if (filterBar) {
    filterBar.hidden = false;
    filters.forEach((button,index) => {
      const count = cards.filter(card => button.dataset.filter === 'all' || card.dataset.category === button.dataset.filter).length;
      button.querySelector('.filter-count').textContent = count;
      button.addEventListener('click',() => choose(button.dataset.filter));
      button.addEventListener('keydown',event => {
        let next;
        if(event.key === 'ArrowRight') next = (index+1)%filters.length;
        else if(event.key === 'ArrowLeft') next = (index+filters.length-1)%filters.length;
        else if(event.key === 'Home') next = 0;
        else if(event.key === 'End') next = filters.length-1;
        if(next === undefined)return;
        event.preventDefault();filters[next].focus();choose(filters[next].dataset.filter);
      });
    });
    announceFilter();
  }

  document.querySelectorAll('.spotlight').forEach(card => {
    let frame = 0;
    card.addEventListener('pointermove',event => {
      if(event.pointerType === 'touch' || !motionAllowed())return;
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        const bounds = card.getBoundingClientRect();
        card.style.setProperty('--spotlight-x',`${event.clientX-bounds.left}px`);
        card.style.setProperty('--spotlight-y',`${event.clientY-bounds.top}px`);
      });
    });
    card.addEventListener('pointerleave',() => cancelAnimationFrame(frame));
  });

  // MIT · Mohammad Shehadeh / Hirael magnetic-button reference.
  document.querySelectorAll('.magnetic').forEach(button => {
    const reset = () => { button.style.setProperty('--magnetic-x','0px');button.style.setProperty('--magnetic-y','0px'); };
    button.addEventListener('pointermove',event => {
      if(event.pointerType === 'touch' || !motionAllowed()){reset();return;}
      const rect = button.getBoundingClientRect();
      button.style.setProperty('--magnetic-x',`${Math.max(-5,Math.min(5,(event.clientX-rect.left-rect.width/2)*.07))}px`);
      button.style.setProperty('--magnetic-y',`${Math.max(-4,Math.min(4,(event.clientY-rect.top-rect.height/2)*.1))}px`);
    });
    button.addEventListener('pointerleave',reset);button.addEventListener('blur',reset);
    new MutationObserver(() => {if(!motionAllowed())reset();}).observe(root,{attributes:true,attributeFilter:['data-effects-paused']});
  });

  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if(!entry.isIntersecting)return;
      entry.target.classList.add('is-revealed');revealObserver.unobserve(entry.target);
    });
  },{threshold:.12});
  document.querySelectorAll('.section-heading h2,.about-layout h2,.process-intro h2,.hero-copy h1').forEach(element => {
    element.dataset.reveal = '';revealObserver.observe(element);
  });

  const timeline = document.querySelector('.process-timeline');
  const milestones = [...document.querySelectorAll('.timeline-step')];
  const navLinks = [...document.querySelectorAll('.desktop-links a')];
  let scrollFrame = 0;
  const updateScroll = () => {
    scrollFrame = 0;
    const max = document.documentElement.scrollHeight-innerHeight;
    root.style.setProperty('--read-progress',String(max > 0 ? Math.max(0,Math.min(1,scrollY/max)) : 0));
    if(timeline){
      const rect = timeline.getBoundingClientRect();
      const progress = Math.max(0,Math.min(1,(innerHeight*.6-rect.top)/Math.max(1,rect.height)));
      timeline.style.setProperty('--timeline-progress',String(progress));
      milestones.forEach(item => item.classList.toggle('is-active',item.getBoundingClientRect().top<innerHeight*.6));
    }
    let current = null;
    navLinks.forEach(link => {
      const section = document.querySelector(link.getAttribute('href'));
      if(section && section.getBoundingClientRect().top<innerHeight*.5) current=link;
    });
    navLinks.forEach(link => { if(link === current)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current'); });
  };
  const scheduleScroll = () => {if(!scrollFrame)scrollFrame=requestAnimationFrame(updateScroll);};
  window.addEventListener('scroll',scheduleScroll,{passive:true});window.addEventListener('resize',scheduleScroll);
  document.addEventListener('toggle',scheduleScroll,true);
  const revealAnchor = hash => {
    let id;
    try { id = decodeURIComponent(hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if(!target)return;
    let parent = target.parentElement;
    while(parent){ if(parent.tagName === 'DETAILS')parent.open = true;parent = parent.parentElement; }
  };
  document.addEventListener('click',event => {
    const link = event.target.closest('a[href^="#"]');
    if(link)revealAnchor(link.getAttribute('href'));
  });
  window.addEventListener('hashchange',() => revealAnchor(location.hash));
  if(location.hash)revealAnchor(location.hash);
  updateScroll();
  new MutationObserver(() => {
    const portrait = document.querySelector('.hero-portrait img');
    if(portrait)portrait.alt = language() ? 'Aleksei Maryshev' : 'Алексей Марышев';
    announceFilter();scheduleScroll();
  }).observe(root,{attributes:true,attributeFilter:['lang']});
})();
