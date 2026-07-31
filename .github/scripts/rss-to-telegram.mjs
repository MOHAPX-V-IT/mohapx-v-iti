/**
 * Публикация записей журнала в Telegram-канал.
 * Берёт rss.xml, отбирает записи, дата которых уже наступила и которые
 * ещё не отправлялись, и постит их с обложкой. Состояние хранится в
 * .github/telegram-state.json и коммитится обратно в репозиторий.
 */
import { readFileSync, writeFileSync, existsSync } from 'node:fs';

const TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const CHAT  = process.env.TELEGRAM_CHAT_ID;
const FORCE = process.env.FORCE_ALL === 'true';
const MAX   = Number(process.env.MAX_PER_RUN || 2);
const STATE = '.github/telegram-state.json';
const FEED  = 'rss.xml';

if (!TOKEN || !CHAT) {
  console.error('Не заданы TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID');
  process.exit(1);
}

const xml = readFileSync(FEED, 'utf8');
const pick = (block, tag) => {
  const m = block.match(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)</${tag}>`));
  return m ? m[1].trim() : '';
};
const unescape = s => s
  .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1')
  .replace(/&lt;/g, '<').replace(/&gt;/g, '>')
  .replace(/&quot;/g, '"').replace(/&#39;/g, "'")
  .replace(/&amp;/g, '&');
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

const items = [...xml.matchAll(/<item>([\s\S]*?)<\/item>/g)].map(m => {
  const b = m[1];
  const enc = b.match(/<enclosure[^>]*url="([^"]+)"/);
  return {
    title: unescape(pick(b, 'title')),
    link: pick(b, 'link'),
    guid: pick(b, 'guid').replace(/^<!\[CDATA\[|\]\]>$/g, ''),
    date: new Date(pick(b, 'pubDate')),
    category: unescape(pick(b, 'category')),
    description: unescape(pick(b, 'description')),
    image: enc ? enc[1] : null,
  };
}).sort((a, b) => a.date - b.date);

const state = existsSync(STATE) ? JSON.parse(readFileSync(STATE, 'utf8')) : { sent: [] };
const sent = new Set(state.sent);
const now = Date.now();

const queue = items
  .filter(i => !sent.has(i.guid))
  .filter(i => FORCE || i.date.getTime() <= now)
  .slice(0, MAX);

if (!queue.length) {
  console.log('Новых записей к публикации нет.');
  process.exit(0);
}

const api = async (method, body) => {
  const r = await fetch(`https://api.telegram.org/bot${TOKEN}/${method}`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
  const j = await r.json();
  if (!j.ok) throw new Error(`${method}: ${j.description}`);
  return j.result;
};

for (const item of queue) {
  let lead = item.description;
  const room = 1024 - item.title.length - item.category.length - item.link.length - 60;
  if (lead.length > room) lead = lead.slice(0, Math.max(room, 0)).replace(/\s+\S*$/, '') + '…';

  const caption =
    `<b>${esc(item.title)}</b>\n\n` +
    `${esc(lead)}\n\n` +
    `<a href="${item.link}">Читать целиком</a>\n\n` +
    `#${item.category}`;

  if (item.image) {
    await api('sendPhoto', { chat_id: CHAT, photo: item.image, caption, parse_mode: 'HTML' });
  } else {
    await api('sendMessage', { chat_id: CHAT, text: caption, parse_mode: 'HTML' });
  }

  sent.add(item.guid);
  console.log('Опубликовано:', item.title);
  await new Promise(r => setTimeout(r, 3000)); // не упираемся в лимиты Telegram
}

writeFileSync(STATE, JSON.stringify({ sent: [...sent] }, null, 2) + '\n');
console.log(`Готово. Отправлено записей: ${queue.length}.`);
