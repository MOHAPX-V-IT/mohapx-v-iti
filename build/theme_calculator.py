"""Apply the current home-page shell to the calculator, never to news pages."""
from pathlib import Path
import re


def restyle_calculator(page, homepage=None):
    if homepage is None:
        homepage = Path('site/index.html').read_text(encoding='utf-8')
    header = Path('build/calculator-header.html').read_text(encoding='utf-8').strip()
    footer_match = re.search(r'<footer class="site-footer">.*?</footer>', homepage, re.S)
    # Home-page canvas effects are intentionally not mounted on the calculator.
    footer = footer_match.group(0) if footer_match else Path('build/calculator-footer.html').read_text(encoding='utf-8').strip()
    header = header.replace('href="#', 'href="index.html#')
    footer = footer.replace('href="#', 'href="index.html#')
    page = page.replace('</head>', '<link rel="stylesheet" href="assets/site.css">\n<link rel="stylesheet" href="assets/calculator.css">\n<script src="assets/site.js" defer></script>\n</head>')
    page, shell_count = re.subn(r'<body[^>]*>.*?<main>', '<body data-page="calculator">\n<a class="skip" href="#main"><span class="ru">К содержанию</span><span class="en">Skip to content</span></a>\n'+header+'\n<main id="main">', page, count=1, flags=re.S)
    if shell_count != 1:
        raise ValueError('Calculator body/navigation boundary was not found')
    page = re.sub(r'<footer>.*?</footer>', footer, page, count=1, flags=re.S)

    # Keep the existing calculations byte-for-byte; the shared legacy shell
    # script is replaced by the new shell's controls, avoiding double listeners.
    pattern = r'<script>\s*\(function\(\)\{.*?\n\(function\(\)\{\n  var ids='
    page, count = re.subn(pattern, '<script>\n(function(){\n  var ids=', page, count=1, flags=re.S)
    if count != 1:
        raise ValueError('Calculator UI/logic script boundary was not found')
    return page
