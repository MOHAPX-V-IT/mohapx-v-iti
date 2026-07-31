import json
B = "https://mohapx-v-it.github.io/mohapx-v-iti"
d = json.load(open('posts.json', encoding='utf-8'))
last = max(p['date'] for p in d['posts'])
lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
         f'  <url><loc>{B}/</loc><lastmod>{last}</lastmod><changefreq>monthly</changefreq><priority>1.0</priority></url>',
         f'  <url><loc>{B}/calculator.html</loc><lastmod>{last}</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>',
         f'  <url><loc>{B}/journal.html</loc><lastmod>{last}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>']
for p in d['posts']:
    lines.append(f'  <url><loc>{B}/journal/post-{p["n"]:02d}.html</loc><lastmod>{p["date"]}</lastmod>'
                 f'<changefreq>yearly</changefreq><priority>0.6</priority></url>')
lines.append('</urlset>')
open('site/sitemap.xml', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('sitemap:', len(d['posts'])+3, 'urls')
