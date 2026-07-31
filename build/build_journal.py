import json, re, html

data = json.load(open('posts.json', encoding='utf-8'))
src = open('site/index.html', encoding='utf-8').read()
style = src.split('<style>')[1].split('</style>')[0]
STRIP_SHADER = True
import re as _re
style = _re.sub(r'/\* -+ animated shader field.*?@media \(prefers-reduced-motion:reduce\)\{\.bg-fx \.shader\{display:none\}\}\n', '', style, flags=_re.S)

MONTHS = ["января","февраля","марта","апреля","мая","июня",
          "июля","августа","сентября","октября","ноября","декабря"]
MONTHS_EN = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

def ru_date(iso):
    y, m, d = iso.split('-')
    return "%d %s" % (int(d), MONTHS[int(m)-1])

def en_date(iso):
    y, m, d = iso.split('-')
    return "%s %d" % (MONTHS_EN[int(m)-1], int(d))

NBSP_DASH = True
def inline(t):
    t = html.escape(t)
    t = t.replace(' \u2014 ', '\u00A0\u2014 ')
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    return t

def body_html(body):
    body = re.sub(r'\n*#\w+\s*$', '', body.strip())
    out = []
    for para in body.split('\n\n'):
        para = para.strip()
        if not para:
            continue
        out.append('<p>' + inline(para).replace('\n', '<br>') + '</p>')
    return '\n'.join(out)

def first_line(body):
    body = re.sub(r'\n*#\w+\s*$', '', body.strip())
    p = body.split('\n\n')[0]
    p = re.sub(r'\*\*|`', '', p)
    return p

RUB = {r['tag']: r for r in data['channel']['rubrics']}

cards = []
for p in data['posts']:
    rub = RUB[p['rubric']]
    pin_badge = ('<span class="jpin"><span class="ru">закреплено</span>'
                 '<span class="en">pinned</span></span>') if p.get('pinned') else ''
    cards.append(f"""
    <article class="jcard rv" data-rub="{rub['tag']}" id="p{p['n']:02d}">
      <a class="jcover" href="journal/j{p['n']:02d}.jpg" data-ru="journal/j{p['n']:02d}.jpg" data-en="journal/j{p['n']:02d}e.jpg" target="_blank" rel="noopener">
        <img src="journal/j{p['n']:02d}.jpg" data-ru="journal/j{p['n']:02d}.jpg" data-en="journal/j{p['n']:02d}e.jpg" alt="" width="1200" height="630" loading="lazy" decoding="async">
      </a>
      <div class="jbody">
        <div class="jmeta">
          <span class="jrub"><span class="ru">// {rub['tag']}</span><span class="en">// {rub['en'].lower()}</span></span>
          <span class="jdate"><span class="ru">{ru_date(p['date'])}</span><span class="en">{en_date(p['date'])}</span></span>
          {pin_badge}
          <a class="jperm" href="journal/post-{p['n']:02d}.html"><span class="ru">страница ↗</span><span class="en">page ↗</span></a>
        </div>
        <h2 class="jtitle"><a href="journal/post-{p['n']:02d}.html"><span class="ru">{html.escape(p['title'])}</span><span class="en">{html.escape(p['title_en'])}</span></a></h2>
        <div class="jtext" id="t{p['n']:02d}">
          <div class="ru">{body_html(p['body'])}</div>
          <div class="en">{body_html(p['body_en'])}</div>
        </div>
        <button class="jmore" data-t="t{p['n']:02d}">
          <span class="ru">Читать целиком</span><span class="en">Read in full</span>
          <span class="chev">▾</span>
        </button>
      </div>
    </article>""")

filters = ''.join(
    f'<button class="jfil" data-f="{r["tag"]}"><span class="ru">// {r["tag"]}</span>'
    f'<span class="en">// {r["en"].lower()}</span></button>' for r in data['channel']['rubrics'])

extra_css = '''
/* ---------- JOURNAL ---------- */
.jhead{padding-top:150px;padding-bottom:14px}
.jfilters{display:flex;flex-wrap:wrap;gap:9px;margin-top:30px}
.jfil{
  font-family:var(--mono);font-size:12.5px;letter-spacing:.06em;
  border:1px solid var(--line);background:var(--panel);color:var(--dim);
  padding:9px 14px;border-radius:9px;cursor:pointer;transition:.25s var(--ease)
}
.jfil:hover{color:var(--tx);border-color:var(--line-2)}
.jfil.on{background:var(--acc);border-color:var(--acc);color:#0A0A0F;font-weight:700}
.jlist{display:grid;gap:20px;margin-top:38px}
.jcard{
  background:var(--bg2);border:1px solid var(--line);border-radius:18px;
  transition:.4s var(--ease);display:grid;grid-template-columns:388px minmax(0,1fr);gap:4px
}
.jcard:hover{border-color:color-mix(in srgb,var(--acc) 40%,var(--line));box-shadow:var(--shadow)}
.jcover{
  display:block;position:relative;overflow:hidden;background:#07070B;
  align-self:start;margin:26px 0 26px 26px;border:1px solid var(--line);border-radius:12px;
  aspect-ratio:1200/630
}
.jcover img{display:block;width:100%;height:100%;object-fit:cover;transition:transform .8s var(--ease)}
.jcard:hover .jcover img{transform:scale(1.04)}
.jbody{padding:26px 30px 28px}
.jmeta{display:flex;flex-wrap:wrap;align-items:center;gap:14px;font-family:var(--mono);font-size:11.5px;letter-spacing:.12em;text-transform:uppercase}
.jrub{color:var(--acc)}
.jdate{color:var(--dimmer)}
.jpin{border:1px solid var(--line-2);color:var(--dim);padding:3px 8px;border-radius:5px}
.jperm{color:var(--dimmer);margin-left:auto;transition:color .25s}
.jperm:hover{color:var(--acc)}
.jtitle a{transition:color .25s}
.jtitle a:hover{color:var(--acc)}
.jtitle{font-family:var(--disp);font-weight:800;font-size:clamp(20px,2.3vw,28px);line-height:1.2;letter-spacing:-.02em;margin:14px 0 16px}
.jtext{position:relative;max-height:132px;overflow:hidden;transition:max-height .55s var(--ease)}
.jtext::after{content:'';position:absolute;left:0;right:0;bottom:0;height:70px;pointer-events:none;
  background:linear-gradient(to top,var(--bg2),transparent);transition:opacity .4s}
.jtext.open{max-height:5000px}
.jtext.open::after{opacity:0}
.jtext p{font-size:16px;color:var(--dim);margin-bottom:14px}
.jtext p:last-child{margin-bottom:0}
.jtext b{color:var(--tx);font-weight:700}
.jtext code{font-family:var(--mono);font-size:.88em;color:var(--acc);background:color-mix(in srgb,var(--acc) 10%,transparent);padding:2px 6px;border-radius:5px}
.jmore{
  margin-top:18px;font-family:var(--mono);font-size:12.5px;letter-spacing:.08em;text-transform:uppercase;
  background:none;border:1px solid var(--line-2);color:var(--tx);padding:10px 16px;border-radius:9px;
  cursor:pointer;transition:.25s var(--ease);display:inline-flex;align-items:center;gap:9px
}
.jmore:hover{border-color:var(--acc);color:var(--acc)}
.jmore .chev{transition:transform .35s var(--ease)}
.jmore.open .chev{transform:rotate(180deg)}
.jempty{font-family:var(--mono);color:var(--dim);padding:40px 0}
@media(max-width:900px){
  .jcard{grid-template-columns:1fr}
  .jcover{margin:18px 18px 0}
  .jbody{padding:20px 20px 24px}
  .jhead{padding-top:120px}
}
.jsub{
  margin-top:56px;border:1px solid var(--line);border-radius:18px;padding:clamp(26px,4vw,46px);
  background:linear-gradient(140deg,color-mix(in srgb,var(--acc) 9%,transparent),transparent 60%),var(--panel);
  text-align:center
}
'''

nav = '''<nav id="nav">
  <a class="brand" href="index.html" aria-label="MOHAPX-V-IT">
    <svg class="crown" viewBox="0 0 64 52" aria-hidden="true"><path d="M6 40V14l13 10L32 4l13 20 13-10v26z" fill="currentColor"/><rect x="6" y="45" width="52" height="5" rx="2.5" fill="currentColor"/></svg>
    <span class="wm">MOHAPX<i>-</i>V<i>-</i>IT</span></a>
  <div class="navlinks">
    <a href="index.html#whoami"><span class="ru">кто я</span><span class="en">whoami</span></a>
    <a href="index.html#process"><span class="ru">процесс</span><span class="en">process</span></a>
    <a href="index.html#work"><span class="ru">проекты</span><span class="en">work</span></a>
    <a href="index.html#path"><span class="ru">путь</span><span class="en">path</span></a>
    <a href="journal.html" aria-current="true"><span class="ru">журнал</span><span class="en">journal</span></a>
    <a href="calculator.html"><span class="ru">калькулятор</span><span class="en">calculator</span></a>
    <a href="index.html#contact"><span class="ru">контакт</span><span class="en">contact</span></a>
  </div>
  <div class="hud">
    <button class="chip" id="langBtn" aria-label="Switch language"><b id="langA">RU</b><span style="opacity:.4">/</span><span id="langB">EN</span></button>
    <button class="chip" id="themeBtn" aria-label="Switch theme"><span id="themeIco">◐</span><span id="themeTx">DARK</span></button>
  </div>
</nav>'''

page = f'''<!DOCTYPE html>
<html lang="ru" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="google-site-verification" content="gfF-3K0brwq0ksgsUm2XDY8JaIDZLYQyMe7ndnqUSBs">
<title>Журнал — MOHAPX-V-IT</title>
<meta name="description" content="Заметки о внедрении ИИ в бизнес-процессы: кейсы, инструменты и позиция. Без магии и без паники.">
<meta name="theme-color" content="#07070B">
<link rel="canonical" href="https://mohapx-v-it.github.io/mohapx-v-iti/journal.html">
<meta property="og:type" content="website">
<meta property="og:site_name" content="MOHAPX-V-IT">
<meta property="og:title" content="Журнал — MOHAPX-V-IT">
<meta property="og:description" content="Заметки о внедрении ИИ в бизнес-процессы: кейсы, инструменты и позиция.">
<meta property="og:url" content="https://mohapx-v-it.github.io/mohapx-v-iti/journal.html">
<meta property="og:image" content="https://mohapx-v-it.github.io/mohapx-v-iti/journal/j03.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%2307070B'/%3E%3Cpath d='M12 42V18l11 9 9-14 9 14 11-9v24z' fill='%23FF9A1F'/%3E%3Crect x='12' y='46' width='40' height='5' rx='2.5' fill='%23FF9A1F'/%3E%3C/svg%3E">
<link rel="alternate" type="application/rss+xml" title="MOHAPX-V-IT" href="rss.xml">
<style>{style}
{extra_css}</style>
<script>try{{var _t=localStorage.getItem('mvi-theme');if(_t)document.documentElement.setAttribute('data-theme',_t);var _l=localStorage.getItem('mvi-lang');if(_l)document.documentElement.setAttribute('lang',_l);}}catch(e){{}}</script>
</head>
<body>

<div class="bg-fx">
  <div class="vign"></div>
  <div class="floor"></div>
  <div class="scan"></div>
  <div class="noise"></div>
</div>
<div id="cursorGlow"></div>
<div class="progress" id="prog"></div>

{nav}

<main>
<section class="jhead">
  <div class="eyebrow">$ cat ./journal</div>
  <h1 style="font-family:var(--disp);font-weight:800;font-size:clamp(34px,6vw,68px);line-height:1.05;letter-spacing:-.03em;margin-bottom:20px">
    <span class="ru">Журнал</span><span class="en">Journal</span>
  </h1>
  <p class="lead">
    <span class="ru">Заметки о внедрении ИИ в бизнес-процессы: что действительно окупается, что продают под видом работающего и как выглядит работа изнутри. Компании не называю — работаю под NDA. Случаи и цифры настоящие.</span>
    <span class="en">Notes on putting AI into real business processes: what actually pays off, what gets sold as working software, and how the work looks from the inside. I don't name clients — NDA. The cases and numbers are real.</span>
  </p>

  <div class="jfilters">
    <button class="jfil on" data-f="all"><span class="ru">всё</span><span class="en">all</span></button>
    {filters}
  </div>
</section>

<section style="padding-top:0">
  <div class="jlist" id="jlist">{''.join(cards)}
  </div>
  <p class="jempty" id="jempty" style="display:none">// <span class="ru">в этой рубрике пока пусто</span><span class="en">nothing here yet</span></p>

  <div class="jsub rv">
    <div class="eyebrow" style="justify-content:center">$ subscribe</div>
    <h2 style="margin-bottom:16px"><span class="ru">Всё это выходит в Telegram</span><span class="en">All of this goes out on Telegram</span></h2>
    <p class="muted" style="margin:0 auto 30px"><span class="ru">Здесь архив, там — свежее и раньше. Плюс короткие заметки, которые до сайта не доезжают.</span><span class="en">This page is the archive; the channel gets it first, plus short notes that never make it here.</span></p>
    <div class="cta" style="justify-content:center">
      <a class="btn primary" href="https://t.me/MOHAPXVIT" target="_blank" rel="noopener"><span class="ru">Подписаться</span><span class="en">Subscribe</span><span class="arw">↗</span></a>
      <a class="btn ghost" href="https://t.me/ELITeeiiNHEIT" target="_blank" rel="noopener"><span class="ru">Написать напрямую</span><span class="en">Message me</span><span class="arw">→</span></a>
    </div>
  </div>
</section>
</main>

<footer>
  <span>MOHAPX-V-IT © 2026 <span class="ru">Алексей Марышев</span><span class="en">Aleksei Maryshev</span></span>
  <a href="index.html"><span class="ru">← на главную</span><span class="en">← back home</span></a>
  <a href="rss.xml">RSS</a>
  <a href="#top">↑ <span class="ru">наверх</span><span class="en">back to top</span></a>
</footer>

<script>
(function(){{
  var root=document.documentElement;
  var themeBtn=document.getElementById('themeBtn'),themeTx=document.getElementById('themeTx'),themeIco=document.getElementById('themeIco');
  function setTheme(t){{root.setAttribute('data-theme',t);themeTx.textContent=t==='dark'?'DARK':'LIGHT';themeIco.textContent=t==='dark'?'◐':'◑';try{{localStorage.setItem('mvi-theme',t);}}catch(e){{}}}}
  themeBtn.addEventListener('click',function(){{setTheme(root.getAttribute('data-theme')==='dark'?'light':'dark');}});

  var langBtn=document.getElementById('langBtn'),langA=document.getElementById('langA'),langB=document.getElementById('langB');
  function setLang(l){{root.setAttribute('lang',l);langA.textContent=l.toUpperCase();langB.textContent=l==='ru'?'EN':'RU';
    document.title=l==='ru'?'Журнал — MOHAPX-V-IT':'Journal — MOHAPX-V-IT';
    document.querySelectorAll('.jcover, .jcover img').forEach(function(el){{
      var v=el.dataset[l]; if(!v) return;
      if(el.tagName==='IMG') el.src=v; else el.href=v;
    }});
    try{{localStorage.setItem('mvi-lang',l);}}catch(e){{}}
    setTimeout(fitText,60);}}
  langBtn.addEventListener('click',function(){{setLang(root.getAttribute('lang')==='ru'?'en':'ru');}});

  try{{var sT=localStorage.getItem('mvi-theme');if(sT)setTheme(sT);
      var sL=localStorage.getItem('mvi-lang');if(sL)setLang(sL);}}catch(e){{}}

  var prog=document.getElementById('prog'),nav=document.getElementById('nav');
  function onScroll(){{var h=document.documentElement.scrollHeight-window.innerHeight;
    prog.style.width=(h>0?(window.scrollY/h)*100:0)+'%';nav.classList.toggle('stuck',window.scrollY>24);}}
  window.addEventListener('scroll',onScroll,{{passive:true}});onScroll();

  var io=new IntersectionObserver(function(es){{es.forEach(function(e){{
    if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target);}}}});}},
    {{threshold:.06,rootMargin:'0px 0px -30px 0px'}});
  document.querySelectorAll('.rv, section > *').forEach(function(el){{el.classList.add('rv');io.observe(el);}});

  // expand / collapse
  document.querySelectorAll('.jmore').forEach(function(b){{
    b.addEventListener('click',function(){{
      var t=document.getElementById(b.dataset.t);
      var open=t.classList.toggle('open');
      b.classList.toggle('open',open);
      b.querySelectorAll('.ru')[0].textContent = open?'Свернуть':'Читать целиком';
      b.querySelectorAll('.en')[0].textContent = open?'Collapse':'Read in full';
      if(!open) b.closest('.jcard').scrollIntoView({{block:'start',behavior:'smooth'}});
    }});
  }});
  // hide the button when the text already fits
  function fitText(){{
    document.querySelectorAll('.jtext').forEach(function(t){{
      var b=document.querySelector('.jmore[data-t="'+t.id+'"]');
      if(t.classList.contains('open') && b && b.classList.contains('open')) return;
      t.classList.remove('open'); t.style.maxHeight='';
      if(t.scrollHeight<=t.clientHeight+6){{
        if(b) b.style.display='none';
        t.style.maxHeight='none'; t.classList.add('open');
      }} else if(b){{ b.style.display=''; }}
    }});
  }}
  fitText();

  // filters
  var cards=[].slice.call(document.querySelectorAll('.jcard'));
  var empty=document.getElementById('jempty');
  document.querySelectorAll('.jfil').forEach(function(f){{
    f.addEventListener('click',function(){{
      document.querySelectorAll('.jfil').forEach(function(x){{x.classList.remove('on');}});
      f.classList.add('on');
      var v=f.dataset.f, shown=0;
      cards.forEach(function(c){{
        var ok = (v==='all') || c.dataset.rub===v;
        c.style.display = ok?'':'none';
        if(ok) shown++;
      }});
      empty.style.display = shown?'none':'block';
    }});
  }});

  var glow=document.getElementById('cursorGlow'),gx=0,gy=0,cx=0,cy=0;
  if(window.matchMedia('(pointer:fine)').matches){{
    window.addEventListener('mousemove',function(e){{gx=e.clientX;gy=e.clientY;}});
    (function loop(){{cx+=(gx-cx)*.09;cy+=(gy-cy)*.09;glow.style.left=cx+'px';glow.style.top=cy+'px';requestAnimationFrame(loop);}})();
  }} else {{ glow.style.display='none'; }}
}})();
</script>
<!-- Cloudflare Web Analytics: inert until a real site token is set -->
<script>(function(){{var T="__CF_ANALYTICS_TOKEN__";if(!/^[a-f0-9]{{32}}$/.test(T))return;var s=document.createElement("script");s.type="module";s.defer=true;s.src="https://static.cloudflareinsights.com/beacon.min.js";s.setAttribute("data-cf-beacon",JSON.stringify({{token:T}}));document.head.appendChild(s);}})();</script>
</body>
</html>
'''

open('site/journal.html', 'w', encoding='utf-8').write(page)
print('journal.html', round(len(page.encode())/1024, 1), 'KB', '|', len(data['posts']), 'posts')

# ---------- Telegram-ready markdown ----------
md = ["# Контент для канала MOHAPX-V-IT\n",
      "Посты готовы к публикации: копируй текст целиком, обложку бери из папки `site/journal/`.",
      "Telegram понимает **жирный** и `код` при вставке через режим Markdown.\n",
      "---\n",
      "## Настройки канала\n",
      "**Название:** " + data['channel']['name'] + "\n",
      "**Описание (вставить в настройки канала):**\n",
      "```\n" + data['channel']['description'] + "\n```\n",
      "**English description (if you add a second channel):**\n",
      "```\n" + data['channel']['description_en'] + "\n```\n",
      "**Аватар:** корона из шапки сайта — файл `avatar.png` в этой же папке.\n",
      "---\n",
      "## Рубрики\n"]
for r in data['channel']['rubrics']:
    md.append(f"`#{r['tag']}` — {r['about']}")
md.append("\n---\n\n## Календарь\n")
md.append("| № | Дата | Рубрика | Заголовок | Обложка |")
md.append("|---|---|---|---|---|")
for p in data['posts']:
    mark = " (закреп)" if p.get('pinned') else ""
    md.append(f"| {p['n']:02d} | {p['date']} | #{p['rubric']} | {p['title']}{mark} | `journal/j{p['n']:02d}.jpg` |")
md.append("\n---\n")

for p in data['posts']:
    md.append(f"\n## {p['n']:02d} · {p['title']}\n")
    md.append(f"**Дата:** {p['date']} · **Рубрика:** #{p['rubric']} · **Обложка:** `journal/j{p['n']:02d}.jpg` (EN: `journal/j{p['n']:02d}e.jpg`)"
              + (" · **ЗАКРЕПИТЬ**" if p.get('pinned') else "") + "\n")
    md.append("```text")
    md.append(p['body'])
    md.append("```\n")
    md.append(f"<details><summary>English version — {p['title_en']}</summary>\n")
    md.append("```text")
    md.append(p['body_en'])
    md.append("```\n</details>\n")
    md.append("---")

open('posts-telegram.md', 'w', encoding='utf-8').write('\n'.join(md) + '\n')
print('posts-telegram.md written')
