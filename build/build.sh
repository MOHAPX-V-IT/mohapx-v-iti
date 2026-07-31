#!/usr/bin/env bash
# Пересобирает журнал, страницы постов, RSS, обложки и карту сайта из posts.json.
# Запускается из корня репозитория. Файлы index.html и 404.html не трогаются.
set -euo pipefail

mkdir -p site/journal

# index.html — источник стилей и навигации для производных страниц
cp index.html site/index.html
# существующие обложки: covers.py пропустит их и сгенерирует только новые
cp journal/*.jpg site/journal/ 2>/dev/null || true

python3 build/covers.py
python3 build/build_journal.py
python3 build/build_pages.py
python3 build/gen_sitemap.py

# возвращаем пересобранные файлы в корень репозитория
cp site/journal.html            journal.html
cp site/rss.xml                 rss.xml
cp site/sitemap.xml             sitemap.xml
cp site/calculator.html         calculator.html
cp site/journal/post-*.html     journal/
cp site/journal/j*.jpg          journal/ 2>/dev/null || true

rm -rf site posts-telegram.md
echo "build done"
