import json, re, html, os
from email.utils import format_datetime
from datetime import datetime, timezone

SITE = "https://mohapx-v-it.github.io/mohapx-v-iti"
data = json.load(open('posts.json', encoding='utf-8'))
style = open('site/index.html', encoding='utf-8').read().split('<style>')[1].split('</style>')[0]
STRIP_SHADER = True
import re as _re
style = _re.sub(r'/\* -+ animated shader field.*?@media \(prefers-reduced-motion:reduce\)\{\.bg-fx \.shader\{display:none\}\}\n', '', style, flags=_re.S)
extra = open('site/journal.html', encoding='utf-8').read().split('/* ---------- JOURNAL ---------- */')[1].split('</style>')[0]

MONTHS = ["января","февраля","марта","апреля","мая","июня","июля","августа","сентября","октября","ноября","декабря"]
MONTHS_EN = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
ru_date = lambda i: "%d %s %s" % (int(i.split('-')[2]), MONTHS[int(i.split('-')[1])-1], i.split('-')[0])
en_date = lambda i: "%s %d, %s" % (MONTHS_EN[int(i.split('-')[1])-1], int(i.split('-')[2]), i.split('-')[0])

NBSP_DASH = True
def inline(t):
    t = html.escape(t)
    t = t.replace(' \u2014 ', '\u00A0\u2014 ')
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    return t

def body_html(body):
    body = re.sub(r'\n*#\w+\s*$', '', body.strip())
    return '\n'.join('<p>' + inline(p.strip()).replace('\n','<br>') + '</p>'
                     for p in body.split('\n\n') if p.strip())

def plain(body, limit=260):
    body = re.sub(r'\n*#\w+\s*$', '', body.strip())
    p = re.sub(r'\*\*|`', '', body.split('\n\n')[0]).replace('\n', ' ')
    return (p[:limit].rsplit(' ', 1)[0] + '…') if len(p) > limit else p

RUB = {r['tag']: r for r in data['channel']['rubrics']}

HEAD_GUARD = ("<script>try{var _t=localStorage.getItem('mvi-theme');"
              "if(_t)document.documentElement.setAttribute('data-theme',_t);"
              "var _l=localStorage.getItem('mvi-lang');"
              "if(_l)document.documentElement.setAttribute('lang',_l);}catch(e){}</script>")

FONTS = ''

FAVICON = ("<link rel=\"icon\" href=\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
           "viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%2307070B'/%3E"
           "%3Cpath d='M12 42V18l11 9 9-14 9 14 11-9v24z' fill='%23FF9A1F'/%3E"
           "%3Crect x='12' y='46' width='40' height='5' rx='2.5' fill='%23FF9A1F'/%3E%3C/svg%3E\">")

def nav(prefix, active):
    def a(href, ru, en):
        cur = ' aria-current="true"' if active == href else ''
        return f'    <a href="{prefix}{href}"{cur}><span class="ru">{ru}</span><span class="en">{en}</span></a>'
    return f'''<nav id="nav">
  <a class="brand" href="{prefix}index.html" aria-label="MOHAPX-V-IT">
    <svg class="crown" viewBox="0 0 64 52" aria-hidden="true"><path d="M6 40V14l13 10L32 4l13 20 13-10v26z" fill="currentColor"/><rect x="6" y="45" width="52" height="5" rx="2.5" fill="currentColor"/></svg>
    <span class="wm">MOHAPX<i>-</i>V<i>-</i>IT</span></a>
  <div class="navlinks">
{a("index.html#whoami","кто я","whoami")}
{a("index.html#process","процесс","process")}
{a("index.html#work","проекты","work")}
{a("index.html#path","путь","path")}
{a("journal.html","журнал","journal")}
{a("calculator.html","калькулятор","calculator")}
{a("index.html#contact","контакт","contact")}
  </div>
  <div class="hud">
    <button class="chip" id="langBtn" aria-label="Switch language"><b id="langA">RU</b><span style="opacity:.4">/</span><span id="langB">EN</span></button>
    <button class="chip" id="themeBtn" aria-label="Switch theme"><span id="themeIco">◐</span><span id="themeTx">DARK</span></button>
  </div>
</nav>'''

BASE_JS = """
(function(){
  var root=document.documentElement;
  var themeBtn=document.getElementById('themeBtn'),themeTx=document.getElementById('themeTx'),themeIco=document.getElementById('themeIco');
  function setTheme(t){root.setAttribute('data-theme',t);themeTx.textContent=t==='dark'?'DARK':'LIGHT';
    themeIco.textContent=t==='dark'?'◐':'◑';try{localStorage.setItem('mvi-theme',t);}catch(e){}}
  themeBtn.addEventListener('click',function(){setTheme(root.getAttribute('data-theme')==='dark'?'light':'dark');});

  var langBtn=document.getElementById('langBtn'),langA=document.getElementById('langA'),langB=document.getElementById('langB');
  window.__onLang=null;
  function setLang(l){root.setAttribute('lang',l);langA.textContent=l.toUpperCase();langB.textContent=l==='ru'?'EN':'RU';
    try{localStorage.setItem('mvi-lang',l);}catch(e){}
    var ttl=document.querySelector('[data-title-'+l+']');
    if(ttl) document.title=ttl.getAttribute('data-title-'+l);
    if(window.__onLang) window.__onLang(l);}
  langBtn.addEventListener('click',function(){setLang(root.getAttribute('lang')==='ru'?'en':'ru');});
  try{var sT=localStorage.getItem('mvi-theme');if(sT)setTheme(sT);
      var sL=localStorage.getItem('mvi-lang');if(sL)setLang(sL);}catch(e){}

  var prog=document.getElementById('prog'),nv=document.getElementById('nav');
  function onScroll(){var h=document.documentElement.scrollHeight-window.innerHeight;
    if(prog) prog.style.width=(h>0?(window.scrollY/h)*100:0)+'%';
    if(nv) nv.classList.toggle('stuck',window.scrollY>24);}
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();

  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},
    {threshold:.06,rootMargin:'0px 0px -30px 0px'});
  document.querySelectorAll('.rv, section > *').forEach(function(el){el.classList.add('rv');io.observe(el);});

  var glow=document.getElementById('cursorGlow'),gx=0,gy=0,cx=0,cy=0;
  if(glow && window.matchMedia('(pointer:fine)').matches){
    window.addEventListener('mousemove',function(e){gx=e.clientX;gy=e.clientY;});
    (function loop(){cx+=(gx-cx)*.09;cy+=(gy-cy)*.09;glow.style.left=cx+'px';glow.style.top=cy+'px';requestAnimationFrame(loop);})();
  } else if(glow){ glow.style.display='none'; }
  document.querySelectorAll('.card').forEach(function(c){
    c.addEventListener('mousemove',function(e){var r=c.getBoundingClientRect();
      c.style.setProperty('--mx',((e.clientX-r.left)/r.width*100)+'%');
      c.style.setProperty('--my',((e.clientY-r.top)/r.height*100)+'%');});});
})();
"""

POST_CSS = """
.article{max-width:820px;margin:0 auto;padding-top:140px}
.acover{border-radius:16px;overflow:hidden;border:1px solid var(--line);margin:28px 0 34px;background:#07070B}
.acover img{display:block;width:100%;height:auto}
.atext p{font-size:17.5px;line-height:1.72;color:var(--dim);margin-bottom:20px}
.atext b{color:var(--tx);font-weight:700}
.atext code{font-family:var(--mono);font-size:.88em;color:var(--acc);background:color-mix(in srgb,var(--acc) 10%,transparent);padding:2px 6px;border-radius:5px}
.anav{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:56px}
.anav a{border:1px solid var(--line);border-radius:14px;padding:20px 22px;transition:.3s var(--ease);background:var(--panel)}
.anav a:hover{border-color:var(--acc);transform:translateY(-2px)}
.anav .dir{font-family:var(--mono);font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--acc);display:block;margin-bottom:8px}
.anav .nx{text-align:right}
.anav span.t{font-family:var(--disp);font-weight:700;font-size:16px;line-height:1.3;color:var(--tx)}
@media(max-width:620px){.anav{grid-template-columns:1fr}.anav .nx{text-align:left}.article{padding-top:110px}}
"""

def page(title_ru, title_en, desc_ru, desc_en, canonical, og_image, body, css="", prefix="", extra_js=""):
    return f'''<!DOCTYPE html>
<html lang="ru" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="google-site-verification" content="gfF-3K0brwq0ksgsUm2XDY8JaIDZLYQyMe7ndnqUSBs">
<title>{html.escape(title_ru)}</title>
<meta name="description" content="{html.escape(desc_ru)}">
<meta name="theme-color" content="#07070B">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="MOHAPX-V-IT">
<meta property="og:title" content="{html.escape(title_ru)}">
<meta property="og:description" content="{html.escape(desc_ru)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
{FAVICON}
{FONTS}
<style>{style}
{extra}
{css}</style>
{HEAD_GUARD}
</head>
<body data-title-ru="{html.escape(title_ru)}" data-title-en="{html.escape(title_en)}">
<div class="bg-fx"><div class="vign"></div><div class="floor"></div><div class="scan"></div><div class="noise"></div></div>
<div id="cursorGlow"></div>
<div class="progress" id="prog"></div>
{body}
<footer>
  <span>MOHAPX-V-IT © 2026 <span class="ru">Алексей Марышев</span><span class="en">Aleksei Maryshev</span></span>
  <a href="{prefix}journal.html"><span class="ru">← в журнал</span><span class="en">← to the journal</span></a>
  <a href="#top">↑ <span class="ru">наверх</span><span class="en">back to top</span></a>
</footer>
<script>{BASE_JS}{extra_js}</script>
<!-- Cloudflare Web Analytics: inert until a real site token is set -->
<script>(function(){{var T="__CF_ANALYTICS_TOKEN__";if(!/^[a-f0-9]{{32}}$/.test(T))return;var s=document.createElement("script");s.type="module";s.defer=true;s.src="https://static.cloudflareinsights.com/beacon.min.js";s.setAttribute("data-cf-beacon",JSON.stringify({{token:T}}));document.head.appendChild(s);}})();</script>
</body>
</html>
'''

# ---------------- post pages ----------------
os.makedirs('site/journal', exist_ok=True)
posts = data['posts']
for i, p in enumerate(posts):
    rub = RUB[p['rubric']]
    prev = posts[i-1] if i > 0 else None
    nxt = posts[i+1] if i < len(posts)-1 else None
    def link(q, dirn_ru, dirn_en, cls):
        if not q: return '<span></span>'
        return (f'<a class="{cls}" href="post-{q["n"]:02d}.html"><span class="dir">{dirn_ru}</span>'
                f'<span class="t"><span class="ru">{html.escape(q["title"])}</span>'
                f'<span class="en">{html.escape(q["title_en"])}</span></span></a>')
    body = f'''<a id="top"></a>
{nav("../", "journal.html")}
<main>
<article class="article">
  <div class="jmeta" style="margin-bottom:16px">
    <span class="jrub"><span class="ru">// {rub['tag']}</span><span class="en">// {rub['en'].lower()}</span></span>
    <span class="jdate"><span class="ru">{ru_date(p['date'])}</span><span class="en">{en_date(p['date'])}</span></span>
  </div>
  <h1 style="font-family:var(--disp);font-weight:800;font-size:clamp(28px,4.6vw,48px);line-height:1.12;letter-spacing:-.025em">
    <span class="ru">{html.escape(p['title'])}</span><span class="en">{html.escape(p['title_en'])}</span></h1>
  <div class="acover"><img id="acov" src="j{p['n']:02d}.jpg" data-ru="j{p['n']:02d}.jpg" data-en="j{p['n']:02d}e.jpg" alt="" width="1200" height="630"></div>
  <div class="atext">
    <div class="ru">{body_html(p['body'])}</div>
    <div class="en">{body_html(p['body_en'])}</div>
  </div>

  <div class="anav">
    {link(prev, "← предыдущий", "← previous", "pv")}
    {link(nxt, "следующий →", "next →", "nx")}
  </div>

  <div class="jsub rv" style="margin-top:48px">
    <h2 style="margin-bottom:14px;font-size:clamp(22px,3vw,32px)"><span class="ru">Свежее выходит в Telegram</span><span class="en">New posts land on Telegram first</span></h2>
    <p class="muted" style="margin:0 auto 26px"><span class="ru">Здесь архив, там — раньше и с короткими заметками, которые до сайта не доезжают.</span><span class="en">This is the archive; the channel gets it first, plus short notes that never make it here.</span></p>
    <div class="cta" style="justify-content:center">
      <a class="btn primary" href="https://t.me/MOHAPXVIT" target="_blank" rel="noopener"><span class="ru">Подписаться</span><span class="en">Subscribe</span><span class="arw">↗</span></a>
      <a class="btn ghost" href="../journal.html"><span class="ru">Все записи</span><span class="en">All posts</span><span class="arw">→</span></a>
    </div>
  </div>
</article>
</main>'''
    js = """
(function(){var c=document.getElementById('acov');
 window.__onLang=function(l){ if(c && c.dataset[l]) c.src=c.dataset[l]; };
 var l=document.documentElement.getAttribute('lang'); if(c && c.dataset[l]) c.src=c.dataset[l];})();
"""
    out = page(
        f"{p['title']} — MOHAPX-V-IT", f"{p['title_en']} — MOHAPX-V-IT",
        plain(p['body']), plain(p['body_en']),
        f"{SITE}/journal/post-{p['n']:02d}.html",
        f"{SITE}/journal/j{p['n']:02d}.jpg",
        body, POST_CSS, prefix="../", extra_js=js)
    out = out.replace("url('fonts/", "url('../fonts/")
    open(f"site/journal/post-{p['n']:02d}.html", 'w', encoding='utf-8').write(out)

print("post pages:", len(posts))

# ---------------- RSS ----------------
items = []
for p in reversed(posts):
    dt = datetime.strptime(p['date'], "%Y-%m-%d").replace(hour=10, tzinfo=timezone.utc)
    items.append(f"""    <item>
      <title>{html.escape(p['title'])}</title>
      <link>{SITE}/journal/post-{p['n']:02d}.html</link>
      <guid isPermaLink="true">{SITE}/journal/post-{p['n']:02d}.html</guid>
      <pubDate>{format_datetime(dt)}</pubDate>
      <category>{p['rubric']}</category>
      <description>{html.escape(plain(p['body'], 400))}</description>
      <enclosure url="{SITE}/journal/j{p['n']:02d}.jpg" type="image/jpeg" length="0"/>
    </item>""")

rss = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>MOHAPX-V-IT — журнал</title>
    <link>{SITE}/journal.html</link>
    <atom:link href="{SITE}/rss.xml" rel="self" type="application/rss+xml"/>
    <description>{html.escape(data['channel']['description'])}</description>
    <language>ru</language>
{chr(10).join(items)}
  </channel>
</rss>
'''
open('site/rss.xml', 'w', encoding='utf-8').write(rss)
print("rss.xml written")

# ---------------- calculator ----------------
CALC_CSS = """
.calc{display:grid;grid-template-columns:minmax(0,420px) minmax(0,1fr);gap:26px;margin-top:40px;align-items:start}
@media(max-width:900px){.calc{grid-template-columns:1fr}}
.cform{background:var(--bg2);border:1px solid var(--line);border-radius:18px;padding:26px}
.fld{margin-bottom:18px}
.fld:last-child{margin-bottom:0}
.fld label{display:block;font-size:14.5px;color:var(--tx);margin-bottom:7px}
.fld .hint{display:block;font-family:var(--mono);font-size:11.5px;color:var(--dimmer);margin-top:6px;letter-spacing:.03em}
.fld input{
  width:100%;background:var(--panel);border:1px solid var(--line);border-radius:10px;
  padding:12px 14px;color:var(--tx);font-family:var(--mono);font-size:16px;outline:none;
  transition:.25s var(--ease);-moz-appearance:textfield
}
.fld input:focus{border-color:var(--acc);box-shadow:0 0 0 3px color-mix(in srgb,var(--acc) 14%,transparent)}
.fld input::-webkit-outer-spin-button,.fld input::-webkit-inner-spin-button{-webkit-appearance:none;margin:0}
.cres{background:var(--bg2);border:1px solid var(--line);border-radius:18px;padding:28px;position:sticky;top:88px}
@media(max-width:900px){.cres{position:static}}
.verdict{border-radius:12px;padding:18px 20px;margin-bottom:24px;border-left:3px solid var(--acc);
  background:color-mix(in srgb,var(--acc) 8%,transparent)}
.verdict .vh{font-family:var(--disp);font-weight:800;font-size:20px;line-height:1.25;margin-bottom:8px;color:var(--tx)}
.verdict p{font-size:15px;margin:0}
.verdict.bad{border-left-color:#E0483C;background:color-mix(in srgb,#E0483C 9%,transparent)}
.verdict.warn{border-left-color:#E8A33D;background:color-mix(in srgb,#E8A33D 9%,transparent)}
.rgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:16px;margin-bottom:26px}
.rbox .rv2{font-family:var(--disp);font-weight:800;font-size:clamp(22px,2.7vw,30px);line-height:1.05;color:var(--acc);letter-spacing:-.02em}
.rbox .rl{font-size:13.5px;color:var(--dim);margin-top:7px;line-height:1.45}
.bars{border-top:1px solid var(--line);padding-top:22px}
.bar{margin-bottom:16px}
.bar .bt{display:flex;justify-content:space-between;font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--dim);margin-bottom:7px}
.bar .btr{background:var(--panel);border-radius:7px;height:14px;overflow:hidden;border:1px solid var(--line)}
.bar .bf{height:100%;border-radius:6px;transition:width .7s var(--ease)}
.bar.now .bf{background:linear-gradient(90deg,#6B5340,#9A6A32)}
.bar.after .bf{background:linear-gradient(90deg,var(--acc-deep),var(--acc))}
.faq{margin-top:22px;border-top:1px solid var(--line)}
.faq details{border-bottom:1px solid var(--line);padding:18px 0}
.faq summary{cursor:pointer;font-family:var(--disp);font-weight:700;font-size:17px;color:var(--tx);list-style:none;display:flex;gap:12px;align-items:flex-start}
.faq summary::-webkit-details-marker{display:none}
.faq summary::before{content:'+';color:var(--acc);font-family:var(--mono);flex:none;transition:transform .3s}
.faq details[open] summary::before{content:'−'}
.faq p{margin-top:12px;font-size:16px}
"""

FAQ = [
    (
        'Как рассчитать окупаемость AI-решения?',
        'Оцените текущий объём работы в часах и стоимость часа. Укажите ожидаемое сокращение времени с учётом проверки результата, стоимость разработки и ежемесячной поддержки. Калькулятор сравнит стоимость высвобожденного времени с расходами и покажет срок окупаемости.',
        'How do you estimate an AI solution’s payback?',
        'Estimate current work hours and hourly cost. Enter the expected time reduction including output review, development cost and monthly maintenance. The calculator compares freed capacity with expenses and estimates payback.',
    ),
    (
        'Для каких проектов подходит калькулятор?',
        'Для AI-ассистентов, RAG-поиска и работы с документами, если можно оценить сокращение времени на конкретную задачу. Для проектов, где основной эффект — качество, доступность знаний или снижение риска, одного этого расчёта недостаточно.',
        'Which projects does the calculator suit?',
        'AI assistants, RAG search and document workflows where time reduction can be estimated for a specific task. When the main benefit is quality, knowledge access or reduced risk, this calculation alone is insufficient.',
    ),
    (
        'Что калькулятор не учитывает?',
        'Качество результата, ошибки модели, требования к данным и доступам, изменение процесса и время освоения системы. Высвобожденное время также не означает автоматического сокращения расходов компании.',
        'What does the calculator leave out?',
        'Output quality, model errors, data and access requirements, process changes and adoption time. Freed capacity does not automatically mean lower company spending.',
    ),
    (
        'Как оценить сокращение времени?',
        'Измерьте выполнение одной и той же задачи до и после пилота. Включите время поиска, ожидания ответа, экспертной проверки и исправлений. Используйте наблюдаемое сокращение времени, а не скорость генерации модели.',
        'How do you estimate time reduction?',
        'Measure the same task before and after a pilot. Include search, response time, expert review and corrections. Use observed task time reduction, rather than model generation speed.',
    ),
    (
        'Как оценить стоимость часа сотрудника?',
        'Разделите полные месячные затраты компании на сотрудника на рабочие часы за месяц. Учитывайте оклад, налоги и взносы. Вводные калькулятора — пример расчёта; подставьте фактические значения своей компании.',
        'How do you estimate an employee’s hourly cost?',
        'Divide total monthly company spending on the employee by monthly working hours, including salary, taxes and contributions. Calculator defaults are illustrative; use your company’s actual figures.',
    ),
]

faq_html = "\n".join(f'''    <details{" open" if i==0 else ""}>
      <summary><span><span class="ru">{html.escape(q_ru)}</span><span class="en">{html.escape(q_en)}</span></span></summary>
      <p class="muted"><span class="ru">{html.escape(a_ru)}</span><span class="en">{html.escape(a_en)}</span></p>
    </details>''' for i,(q_ru,a_ru,q_en,a_en) in enumerate(FAQ))

faq_ld = json.dumps({
  "@context":"https://schema.org","@type":"FAQPage",
  "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a,_,_ in FAQ]
}, ensure_ascii=False)

app_ld = json.dumps({
  "@context":"https://schema.org","@type":"WebApplication",
  "name":"Калькулятор окупаемости AI-решения",
  "url":f"{SITE}/calculator.html",
  "applicationCategory":"BusinessApplication",
  "operatingSystem":"Any",
  "offers":{"@type":"Offer","price":"0","priceCurrency":"RUB"},
  "description":"Оценка экономического эффекта AI-решения: экономия времени, расходы на поддержку, срок окупаемости и ROI за первый год.",
  "inLanguage":"ru",
  "author":{"@type":"Person","name":"Алексей Марышев","url":SITE}
}, ensure_ascii=False)

def fld(id_, ru, en, val, hint_ru, hint_en, step="1"):
    return f'''      <div class="fld">
        <label for="{id_}"><span class="ru">{ru}</span><span class="en">{en}</span></label>
        <input type="number" id="{id_}" value="{val}" min="0" step="{step}" inputmode="decimal">
        <span class="hint"><span class="ru">{hint_ru}</span><span class="en">{hint_en}</span></span>
      </div>'''

calc_body = f'''<a id="top"></a>
{nav("", "calculator.html")}
<main>
<section style="padding-top:150px;padding-bottom:20px">
  <div class="eyebrow">$ roi --calc</div>
  <h1 style="font-family:var(--disp);font-weight:800;font-size:clamp(30px,5.2vw,58px);line-height:1.06;letter-spacing:-.03em;margin-bottom:20px">
    <span class="ru">Калькулятор окупаемости AI-решения</span>
    <span class="en">AI solution payback calculator</span>
  </h1>
  <p class="lead">
    <span class="ru">Инструмент предварительной оценки AI-проекта: сколько времени он может освободить, сколько стоит разработка и поддержка, когда вернутся вложения. Подходит для ассистентов, RAG и работы с документами, если эффект можно выразить в сэкономленных часах. Расчёт выполняется в браузере, данные никуда не отправляются.</span>
    <span class="en">A tool for an initial AI project estimate: time it may free up, development and maintenance cost, and payback. It works for assistants, RAG and document workflows when the impact can be expressed as hours saved. Calculations run in your browser and send no data anywhere.</span>
  </p>

  <div class="calc">
    <form class="cform rv" id="cf" onsubmit="return false">
{fld("n","Сколько человек занято задачей","People doing the task","3","человек, которые делают эту работу руками","people doing this work by hand")}
{fld("h","Часов в неделю на одного человека","Hours per week, per person","6","сколько времени уходит на задачу еженедельно","time the task takes each week","0.5")}
{fld("r","Стоимость часа сотрудника, ₽","Hourly cost of an employee, ₽","850","полная стоимость для компании: оклад + налоги ÷ 160 часов","full cost to the company: salary + taxes ÷ 160 hours","10")}
{fld("s","Ожидаемое сокращение времени на задачу, %","Expected reduction in task time, %","70","оценка по пилоту; учитывайте проверку и исправление результата","estimate from a pilot; include review and correction time","5")}
{fld("c","Стоимость разработки и внедрения, ₽","Build and rollout cost, ₽","350000","с запасом 20–30% — на входе её почти всегда занижают","add a 20–30% buffer; it's almost always underestimated","1000")}
{fld("m","Поддержка решения, ₽ в месяц","Maintenance, ₽ per month","8000","хостинг, модели, доработки, дежурство","hosting, models, tweaks, on-call","500")}
    </form>

    <div class="cres rv">
      <div class="verdict" id="verdict">
        <div class="vh" id="vh"></div>
        <p class="muted" id="vp"></p>
      </div>

      <div class="rgrid">
        <div class="rbox"><div class="rv2" id="o1">—</div><div class="rl"><span class="ru">стоимость текущей работы за год</span><span class="en">annual cost of the current work</span></div></div>
        <div class="rbox"><div class="rv2" id="o2">—</div><div class="rl"><span class="ru">чистая экономия за год</span><span class="en">net saving per year</span></div></div>
        <div class="rbox"><div class="rv2" id="o3">—</div><div class="rl"><span class="ru">окупаемость</span><span class="en">payback period</span></div></div>
        <div class="rbox"><div class="rv2" id="o4">—</div><div class="rl"><span class="ru">ROI за первый год</span><span class="en">first-year ROI</span></div></div>
        <div class="rbox"><div class="rv2" id="o5">—</div><div class="rl"><span class="ru">человеко-часов освободится за год</span><span class="en">person-hours freed per year</span></div></div>
      </div>

      <div class="bars">
        <div class="bar now"><div class="bt"><span><span class="ru">сейчас</span><span class="en">today</span></span><span id="b1">—</span></div><div class="btr"><div class="bf" id="bf1" style="width:100%"></div></div></div>
        <div class="bar after"><div class="bt"><span><span class="ru">после внедрения</span><span class="en">after implementation</span></span><span id="b2">—</span></div><div class="btr"><div class="bf" id="bf2" style="width:30%"></div></div></div>
      </div>
    </div>
  </div>
</section>

<section style="padding-top:20px">
  <h2><span class="ru">Как считать эффект AI-решения</span><span class="en">How to estimate an AI solution’s impact</span></h2>
  <p class="muted">
    <span class="ru">Годовая стоимость текущей работы — число сотрудников × часы в неделю × 52 × стоимость часа. Сокращение времени даёт оценку высвобожденного ресурса; из неё вычитаются расходы на поддержку. Срок окупаемости — стоимость разработки, делённая на месячный эффект. ROI первого года учитывает разработку и поддержку.</span>
    <span class="en">Annual cost of the current work is people × hours per week × 52 × hourly cost. Time reduction estimates the value of freed capacity, minus maintenance expenses. Payback is development cost divided by the monthly impact. First-year ROI accounts for development and maintenance.</span>
  </p>
  <p class="muted">
    <span class="ru">Высвобожденные часы не всегда превращаются в сокращение расходов: сотрудники могут использовать их для других задач. Калькулятор оценивает только этот эффект. Качество ответов, экспертную проверку, доступность данных и требования к системе нужно оценивать отдельно.</span>
    <span class="en">Freed hours do not always translate into lower spending: employees may use them for other tasks. The calculator estimates only this effect. Output quality, expert review, data availability and system requirements need a separate assessment.</span>
  </p>

  <h2 style="margin-top:44px"><span class="ru">Частые вопросы</span><span class="en">Frequently asked</span></h2>
  <div class="faq">
{faq_html}
  </div>

  <div class="jsub rv" style="margin-top:50px">
    <div class="eyebrow" style="justify-content:center">$ next</div>
    <h2 style="margin-bottom:14px"><span class="ru">Обсудим задачу и оценку?</span><span class="en">Discuss the problem and the estimate?</span></h2>
    <p class="muted" style="margin:0 auto 28px">
      <span class="ru">Напишите, какой процесс вы оценивали и какие данные доступны. Обсудим, нужен ли здесь AI, как устроить решение и что проверить в пилоте.</span>
      <span class="en">Tell me which process you estimated and what data is available. We can discuss whether AI fits, how to build the solution and what to validate in a pilot.</span>
    </p>
    <div class="cta" style="justify-content:center">
      <a class="btn primary" href="https://t.me/ELITeeiiNHEIT" target="_blank" rel="noopener"><span class="ru">Обсудить расчёт</span><span class="en">Discuss the numbers</span><span class="arw">→</span></a>
      <a class="btn ghost" href="journal.html"><span class="ru">Читать журнал</span><span class="en">Read the journal</span><span class="arw">↗</span></a>
    </div>
  </div>
</section>
</main>
<script type="application/ld+json">{faq_ld}</script>
<script type="application/ld+json">{app_ld}</script>'''

CALC_JS = """
(function(){
  var ids=['n','h','r','s','c','m'], el={};
  ids.forEach(function(i){el[i]=document.getElementById(i);});
  function money(v){
    var l=document.documentElement.getAttribute('lang');
    var s=Math.round(v).toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g,' ');
    return s+(l==='ru'?' \\u20BD':' RUB');
  }
  function num(v){return Math.round(v).toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g,' ');}
  function t(ru,en){return document.documentElement.getAttribute('lang')==='ru'?ru:en;}
  function calc(){
    var n=+el.n.value||0,h=+el.h.value||0,r=+el.r.value||0,
        s=Math.min(+el.s.value||0,100),c=+el.c.value||0,m=+el.m.value||0;
    var hoursYear=n*h*52, costYear=hoursYear*r;
    var savedHours=hoursYear*s/100, savedMoney=savedHours*r;
    var net=savedMoney-m*12;
    var payback = net>0 ? c/(net/12) : Infinity;
    var roi = c>0 ? (net-c)/c*100 : (net>0?Infinity:0);
    document.getElementById('o1').textContent=money(costYear);
    document.getElementById('o2').textContent=net>0?money(net):money(net);
    document.getElementById('o3').textContent = isFinite(payback)
      ? (payback<1? t('меньше месяца','under a month') : num(payback)+' '+t('мес.','mo'))
      : t('никогда','never');
    document.getElementById('o4').textContent = isFinite(roi)? (roi>0?'+':'')+num(roi)+'%' : '—';
    document.getElementById('o5').textContent = num(savedHours)+' '+t('ч','h');

    var after=costYear-savedMoney+m*12;
    var maxv=Math.max(costYear,after,1);
    document.getElementById('bf1').style.width=(costYear/maxv*100)+'%';
    document.getElementById('bf2').style.width=(Math.max(after,0)/maxv*100)+'%';
    document.getElementById('b1').textContent=money(costYear);
    document.getElementById('b2').textContent=money(Math.max(after,0));

    var v=document.getElementById('verdict'), vh=document.getElementById('vh'), vp=document.getElementById('vp');
    v.className='verdict';
    if(net<=0){
      v.classList.add('bad');
      vh.textContent=t('Не окупится','It will not pay off');
      vp.textContent=t('По этим вводным поддержка превышает эффект от высвобожденного времени. Пересмотрите расчёт или оцените другие цели проекта.',
                       'With these inputs, maintenance exceeds the value of freed time. Revisit the estimate or assess the project’s other objectives.');
    } else if(payback<=12){
      vh.textContent=t('Оценка: до года','Estimate: under a year');
      vp.textContent=t('Расчётный срок окупаемости — до года. Следующий шаг: проверить сокращение времени и качество результата на пилоте.',
                       'Estimated payback is within a year. Next, validate time reduction and output quality in a pilot.');
    } else if(payback<=24){
      v.classList.add('warn');
      vh.textContent=t('Оценка: 1–2 года','Estimate: 1–2 years');
      vp.textContent=t('Расчётный срок — от года до двух. Проверьте устойчивость процесса и обоснованность всех вводных.',
                       'Estimated payback is one to two years. Check process stability and the assumptions behind each input.');
    } else {
      v.classList.add('bad');
      vh.textContent=t('Оценка: больше 2 лет','Estimate: over 2 years');
      vp.textContent=t('Окупаемость по экономии времени превышает два года. Сопоставьте этот срок с горизонтом проекта и другими ожидаемыми результатами.',
                       'Payback from time savings exceeds two years. Compare it with the project horizon and other expected outcomes.');
    }
  }
  ids.forEach(function(i){el[i].addEventListener('input',calc);});
  window.__onLang=calc;
  calc();
})();
"""

calc_page = page(
  "Калькулятор окупаемости AI-решения — MOHAPX-V-IT",
  "AI solution payback calculator — MOHAPX-V-IT",
  "Калькулятор экономического эффекта AI-решения: экономия времени, расходы на поддержку, срок окупаемости и ROI. Расчёт в браузере, без регистрации.",
  "An AI solution impact calculator: time saved, maintenance cost, payback period and ROI. Runs in your browser, no sign-up.",
  f"{SITE}/calculator.html", f"{SITE}/journal/j10.jpg",
  calc_body, CALC_CSS, prefix="", extra_js=CALC_JS)
calc_page = calc_page.replace('<meta property="og:type" content="article">', '<meta property="og:type" content="website">')
open('site/calculator.html','w',encoding='utf-8').write(calc_page)
print('calculator.html', round(len(calc_page.encode())/1024,1), 'KB')
