/* Adapted from the four supplied 21st.dev references. No framework/runtime CDN. */
(() => {
  'use strict';
  const root = document.documentElement;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let paused = reduced.matches;
  const toggle = document.getElementById('effectsToggle');
  if (toggle) toggle.hidden = false;
  const applyPause = () => {
    root.dataset.effectsPaused = String(paused || reduced.matches || document.hidden);
    toggle?.setAttribute('aria-pressed', String(paused));
    if (toggle) toggle.innerHTML = paused
      ? '<span class="ru">Продолжить эффекты ↗</span><span class="en">Resume effects ↗</span>'
      : '<span class="ru">Остановить эффекты Ⅱ</span><span class="en">Pause effects Ⅱ</span>';
  };
  toggle?.addEventListener('click', () => { paused = !paused; applyPause(); });
  reduced.addEventListener('change', () => { paused = reduced.matches; applyPause(); });
  document.addEventListener('visibilitychange', applyPause);
  applyPause();

  // Background Paths: two families of cubic curves, with staggered dash travel.
  const paths = document.querySelector('.hero-paths svg');
  if (paths) {
    for (const position of [1, -1]) {
      for (let i = 0; i < 24; i++) {
        const p = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        p.setAttribute('d', `M${-380+i*5*position} ${-189-i*6}C${-380+i*5*position} ${-189-i*6} ${-312+i*5*position} ${216-i*6} ${152-i*5*position} ${343-i*6}C${616-i*5*position} ${470-i*6} ${684-i*5*position} ${875-i*6} ${684-i*5*position} ${875-i*6}`);
        p.setAttribute('stroke', 'currentColor');
        p.setAttribute('stroke-width', String(.5+i*.035));
        p.setAttribute('stroke-opacity', String(.12+i*.014));
        p.style.setProperty('--i', i);
        paths.append(p);
      }
    }
  }

  // Tilted Grid Hero: sixteen facets per image, sharing one cylindrical orbit.
  const band = document.getElementById('tiltedGrid');
  if (band) {
    const images = Array.from(band.querySelectorAll('img')).map(img => img.getAttribute('src'));
    const scene = document.createElement('div');
    scene.className = 'tilted-scene';
    scene.setAttribute('aria-hidden', 'true');
    const style = document.createElement('style');
    let sizeKey = '';
    const layout = () => {
      const { width, height } = band.getBoundingClientRect();
      if (!width || !height) return;
      const key = `${Math.round(width)}:${Math.round(height)}`;
      if (key === sizeKey) return;
      sizeKey = key;
      const bend = 65*Math.PI/180, camera = 1.6, aspect = 16/10;
      const radius = width * (camera-1+Math.cos(bend))/(2*camera*Math.sin(bend));
      const h = Math.min(height*.65, width*.5/aspect);
      const unit = h/radius*180/Math.PI;
      const pitch = (aspect+.09)*unit;
      const limit = bend*180/Math.PI+aspect*unit/2;
      const columns = Math.min(30, Math.max(2, Math.ceil(2*limit/pitch)));
      const sweep = columns*pitch/2;
      const hide = Math.max(0,(sweep-limit)/(2*sweep)*100);
      const turn = angle => `translateZ(${radius}px) rotateY(${angle}deg) translateZ(${-radius}px)`;
      band.style.setProperty('--tile-h', `${h}px`);
      band.style.setProperty('--tile-w', `${h*aspect}px`);
      band.style.setProperty('--camera', `${radius*camera}px`);
      band.style.setProperty('--duration', `${columns*5}s`);
      style.textContent = `@keyframes tile-orbit{from{transform:${turn(-sweep)}}to{transform:${turn(sweep)}}0%,${hide}%,${100-hide}%,100%{visibility:hidden}${hide+.001}%,${100-hide-.001}%{visibility:visible}}`;
      scene.replaceChildren();
      for (let t=0;t<columns;t++) {
        const tile = document.createElement('div');
        tile.className = 'tilted-tile';
        tile.style.setProperty('--delay', `${-t*5}s`);
        const first = columns-1-t;
        for (let k=0;k<16;k++) {
          const strip = document.createElement('div');
          strip.className = 'tilted-slice';
          strip.style.cssText = `left:${h*(aspect-aspect/16)/2}px;width:${h*aspect/16+1}px;transform:${turn((aspect/2-(k+.5)*aspect/16)*unit)}`;
          const img = document.createElement('img');
          img.src = images[first%images.length];
          img.alt = '';
          img.draggable = false;
          img.style.left = `${-k*h*aspect/16}px`;
          strip.append(img); tile.append(strip);
        }
        tile.addEventListener('animationiteration', event => {
          if (event.target !== tile) return;
          const lap = Math.round(event.elapsedTime/(columns*5));
          tile.querySelectorAll('img').forEach(img => { img.src = images[(lap*columns+first)%images.length]; });
        });
        scene.append(tile);
      }
    };
    band.replaceChildren(style, scene);
    new ResizeObserver(layout).observe(band);
    new IntersectionObserver(entries => {
      scene.style.animationPlayState = entries[0].isIntersecting ? '' : 'paused';
      scene.querySelectorAll('.tilted-tile').forEach(tile => { tile.style.animationPlayState = entries[0].isIntersecting ? '' : 'paused'; });
    }).observe(band);
    layout();
  }

  // Last successful snapshot is served locally; private GitHub tokens never reach visitors.
  const section = document.getElementById('github');
  if (section) {
    let snapshot;
    const caption = document.getElementById('calendarCaption');
    const grid = document.getElementById('githubCalendar');
    const card = section.querySelector('.github-calendar');
    const tooltip = document.createElement('div');
    tooltip.className = 'calendar-tooltip';
    tooltip.hidden = true;
    tooltip.setAttribute('aria-hidden', 'true');
    card.append(tooltip);
    const hideTooltip = () => { tooltip.classList.remove('is-visible');tooltip.hidden = true; };
    window.addEventListener('resize', hideTooltip);
    card.addEventListener('pointerleave', hideTooltip);
    card.addEventListener('focusout', hideTooltip);
    card.addEventListener('keydown', event => { if (event.key === 'Escape') hideTooltip(); });
    card.querySelector('.calendar-scroll').addEventListener('scroll', hideTooltip, {passive:true});
    const revealObserver = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) { card.classList.add('is-revealed'); revealObserver.disconnect(); }
    }, {threshold:.2});
    revealObserver.observe(card);
    const locale = () => root.lang === 'en' ? 'en-US' : 'ru-RU';
    const formatDate = date => new Date(`${date}T12:00:00Z`).toLocaleDateString(locale(), {day:'numeric',month:'long',year:'numeric',timeZone:'UTC'});
    const dayLabel = day => root.lang === 'en' ? `${day.count} contributions · ${formatDate(day.date)}` : `Вкладов: ${day.count} · ${formatDate(day.date)}`;
    const render = () => {
      if (!snapshot) return;
      for (const key of ['publicRepos','stars','followers','contributions']) {
        document.querySelector(`[data-github="${key}"]`).textContent = snapshot[key].toLocaleString(locale());
      }
      const from = snapshot.days[0].date, to = snapshot.days.at(-1).date;
      document.getElementById('calendarRange').textContent = `${formatDate(from)} — ${formatDate(to)}`;
      const updated = document.getElementById('githubUpdated');
      updated.textContent = new Date(snapshot.updatedAt).toLocaleString(locale(),{dateStyle:'medium',timeStyle:'short'});
      updated.dateTime = snapshot.updatedAt;
      grid.setAttribute('aria-label', root.lang === 'en' ? 'GitHub contributions, navigate with arrow keys' : 'Вклады в GitHub, навигация стрелками');
      hideTooltip();
      const days = snapshot.days;
      const offset = new Date(`${days[0].date}T12:00:00Z`).getUTCDay();
      const weeks = Math.ceil((offset+days.length)/7);
      grid.replaceChildren();
      for (let i=0;i<offset;i++) { const spacer=document.createElement('span');grid.append(spacer); }
      days.forEach((day,i) => {
        const cell = document.createElement('button');
        cell.type = 'button';
        cell.className = 'calendar-day';
        cell.dataset.level = day.level;
        cell.dataset.index = i;
        cell.style.setProperty('--reveal-delay', `${(days.length-1-i)*.002}s`);
        cell.tabIndex = i === days.length-1 ? 0 : -1;
        cell.setAttribute('aria-label',dayLabel(day));
        cell.title = dayLabel(day);
        const describe = () => {
          caption.textContent = dayLabel(day);
          tooltip.textContent = dayLabel(day);
          tooltip.hidden = false;
          const bounds = card.getBoundingClientRect(), rect = cell.getBoundingClientRect();
          const half = tooltip.offsetWidth/2+12;
          tooltip.style.left = `${Math.max(half,Math.min(bounds.width-half,rect.left-bounds.left+rect.width/2))}px`;
          tooltip.style.top = `${Math.max(42,rect.top-bounds.top-8)}px`;
          tooltip.classList.add('is-visible');
        };
        cell.addEventListener('pointerenter',describe);
        cell.addEventListener('focus',describe);
        cell.addEventListener('click',describe);
        cell.addEventListener('keydown', event => {
          const delta = {ArrowLeft:-7,ArrowRight:7,ArrowUp:-1,ArrowDown:1,Home:-i,End:days.length-i-1}[event.key];
          if (delta === undefined) return;
          event.preventDefault();
          const next = grid.querySelector(`[data-index="${Math.min(days.length-1,Math.max(0,i+delta))}"]`);
          cell.tabIndex=-1;next.tabIndex=0;next.focus();
        });
        grid.append(cell);
      });
      const months = document.getElementById('calendarMonths');
      months.replaceChildren();
      let previous = '';
      days.forEach((day,i) => {
        const month = day.date.slice(0,7);
        if (month === previous) return;
        previous = month;
        const week = Math.floor((i+offset)/7);
        if (week > weeks-3) return;
        const label = document.createElement('span');
        label.textContent = new Date(`${day.date}T12:00:00Z`).toLocaleDateString(locale(),{month:'short',timeZone:'UTC'});
        label.style.left = `${week/weeks*100}%`;
        months.append(label);
      });
      caption.textContent = root.lang === 'en' ? 'Select a day · use arrow keys to explore' : 'Выбери день · для навигации используй стрелки';
    };
    fetch('assets/github-stats.json').then(response => {
      if (!response.ok) throw new Error('Snapshot unavailable');
      return response.json();
    }).then(data => {
      if (data.username !== 'MOHAPX-V-IT' || !Array.isArray(data.days) || !data.days.length) throw new Error('Invalid snapshot');
      snapshot = data;render();
    }).catch(() => {
      caption.innerHTML = '<span class="ru">Статистика временно недоступна. Активность доступна в профиле GitHub.</span><span class="en">Statistics are temporarily unavailable. View activity on GitHub.</span>';
    });
    new MutationObserver(render).observe(root,{attributes:true,attributeFilter:['lang']});
  }

  // Halftone Wordmark Footer: coverage-sampled dots, pointer springs and click wave.
  const footer = document.getElementById('halftoneFooter');
  const canvas = document.getElementById('halftoneCanvas');
  const ctx = canvas?.getContext('2d');
  if (footer && ctx) {
    let dots=[], width=0,height=0,dpr=1,frame=0,visible=false,px=-1e5,py=-1e5;
    let ring={x:0,y:0,time:-1}, previousTime=0;
    let ink=[236,236,241],warm=[242,160,45];
    const colour = css => {
      const probe=document.createElement('span');probe.style.color=css;footer.append(probe);
      const value=getComputedStyle(probe).color;probe.remove();
      return value.match(/[\d.]+/g).slice(0,3).map(Number);
    };
    const layout = () => {
      width=Math.round(footer.clientWidth);height=Math.round(footer.clientHeight);
      dpr=Math.min(devicePixelRatio||1,2);canvas.width=width*dpr;canvas.height=height*dpr;
      const styles=getComputedStyle(root);ink=colour(styles.getPropertyValue('--tx'));warm=colour(styles.getPropertyValue('--acc'));
      const mask=document.createElement('canvas');mask.width=width;mask.height=height;
      const m=mask.getContext('2d',{willReadFrequently:true});
      m.font='800 100px Manrope';
      const size=width*1.025/m.measureText('mohapx').width*100;
      m.font=`800 ${size}px Manrope`;
      const bounds=m.measureText('mohapx');
      m.fillText('mohapx',(width-bounds.width)/2,height+(bounds.actualBoundingBoxAscent||size*.72)*.14);
      const data=m.getImageData(0,0,width,height).data,gap=width<600?4:6;
      dots=[];
      for(let y=gap/2;y<height;y+=gap) for(let x=gap/2;x<width;x+=gap){
        let alpha=0;
        for(let sy=-1;sy<=1;sy++) for(let sx=-1;sx<=1;sx++){
          const ix=Math.max(0,Math.min(width-1,Math.floor(x+sx*gap/3)));
          const iy=Math.max(0,Math.min(height-1,Math.floor(y+sy*gap/3)));
          alpha+=data[(iy*width+ix)*4+3];
        }
        const coverage=alpha/(9*255);
        if(coverage>.06)dots.push({x,y,hx:x,hy:y,vx:0,vy:0,r:Math.sqrt(coverage)*gap*.48});
      }
      footer.classList.add('is-ready');draw(performance.now());wake();
    };
    const draw = now => {
      frame=0;
      const active=root.dataset.effectsPaused!=='true';
      const dt=previousTime?Math.min(2,(now-previousTime)/16.667):1;previousTime=now;
      ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,width,height);
      let moving=false;
      for(const dot of dots){
        if(active){
          const dx=dot.x-px,dy=dot.y-py,d=Math.hypot(dx,dy)+.001;
          if(d<85){const f=(1-d/85)*2.6;dot.vx+=dx/d*f;dot.vy+=dy/d*f;}
          const age=now-ring.time;
          if(ring.time>=0&&age<900){const distance=Math.hypot(dot.hx-ring.x,dot.hy-ring.y)+.001;const band=Math.abs(distance-age*.9);if(band<24){const f=(1-band/24)*3;dot.vx+=(dot.hx-ring.x)/distance*f;dot.vy+=(dot.hy-ring.y)/distance*f;}}
          dot.vx=(dot.vx+(dot.hx-dot.x)*.05*dt)*Math.pow(.84,dt);
          dot.vy=(dot.vy+(dot.hy-dot.y)*.05*dt)*Math.pow(.84,dt);
          dot.x+=dot.vx*dt;dot.y+=dot.vy*dt;
        }else{dot.x=dot.hx;dot.y=dot.hy;dot.vx=dot.vy=0;}
        const heat=Math.min(1,Math.hypot(dot.x-dot.hx,dot.y-dot.hy)/24);
        const rgb=ink.map((v,i)=>Math.round(v+(warm[i]-v)*heat));
        ctx.fillStyle=`rgb(${rgb.join(',')})`;ctx.beginPath();ctx.arc(dot.x,dot.y,dot.r,0,Math.PI*2);ctx.fill();
        if(Math.abs(dot.vx)+Math.abs(dot.vy)>.04||heat>.005)moving=true;
      }
      if(active&&visible&&!document.hidden&&(moving||(ring.time>=0&&now-ring.time<900)))frame=requestAnimationFrame(draw);
    };
    function wake(){if(!frame&&visible&&!document.hidden)frame=requestAnimationFrame(draw);}
    footer.addEventListener('pointermove',event=>{if(event.pointerType==='touch')return;const r=footer.getBoundingClientRect();px=event.clientX-r.left;py=event.clientY-r.top;wake();});
    footer.addEventListener('pointerleave',()=>{px=py=-1e5;wake();});
    footer.addEventListener('click',event=>{if(event.target.closest('a,button'))return;const r=footer.getBoundingClientRect();ring={x:event.clientX-r.left,y:event.clientY-r.top,time:performance.now()};wake();});
    new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(visible)wake();else{cancelAnimationFrame(frame);frame=0;previousTime=0;}}).observe(footer);
    new ResizeObserver(layout).observe(footer);
    new MutationObserver(layout).observe(root,{attributes:true,attributeFilter:['data-theme']});
    new MutationObserver(wake).observe(root,{attributes:true,attributeFilter:['data-effects-paused']});
    document.addEventListener('visibilitychange',()=>{if(document.hidden){cancelAnimationFrame(frame);frame=0;}else wake();});
    document.fonts.ready.then(layout);
  }
})();
