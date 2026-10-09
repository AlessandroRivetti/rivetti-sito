#!/usr/bin/env python3
"""
Rende il sito autonomo da Google Fonts e jsDelivr.

Cosa fa (una volta sola, da eseguire sul TUO computer con internet, nella cartella del sito):
  1. scarica in locale i font Sora e Inter (WOFF2, licenza SIL OFL);
  2. crea fonts.css con le regole @font-face;
  3. aggiorna tutte le pagine del sito (index, privati, imprese, pubblica-amministrazione, contatti, realizzazioni, 404,
     recensione, privacy, cookie, note-legali):
     toglie i riferimenti a fonts.googleapis.com e cdn.jsdelivr.net e aggiorna
     i paragrafi di Privacy e Cookie Policy che elencano questi servizi.
  Prima di modificare qualsiasi cosa, salva una copia dei file in _backup_prima_dello_script/.
  Se anche un solo download fallisce, NON modifica nulla.

Uso:   python3 scarica-risorse-locali.py
"""
import os, re, shutil, sys, urllib.request

BASE = os.environ.get('RI_CDN', 'https://cdn.jsdelivr.net/npm')   # (solo per i test)
ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = ['index.html', 'privati.html', 'imprese.html', 'pubblica-amministrazione.html', 'contatti.html', 'realizzazioni.html', '404.html',
         'recensione.html', 'privacy.html', 'cookie.html', 'note-legali.html']
JS_FILES = []      # nessuno script con riferimenti a jsDelivr

FONTS = {'sora': ('Sora', [300, 400, 600, 700]), 'inter': ('Inter', [400, 500, 600])}
FILES = []      # (url, percorso locale, firma iniziale attesa)
for fid, (fam, weights) in FONTS.items():
    for w in weights:
        FILES.append((f'{BASE}/@fontsource/{fid}@5/files/{fid}-latin-{w}-normal.woff2', f'assets/fonts/{fid}-latin-{w}.woff2', b'wOF2'))
    FILES.append((f'{BASE}/@fontsource/{fid}@5/LICENSE', f'assets/fonts/LICENSE-{fid}.txt', None))
LATIN = 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD'

EXT_PRIVACY_LOCAL = '''@@EXT_PRIVACY_LOCAL@@'''
EXT_COOKIE_LOCAL = '''@@EXT_COOKIE_LOCAL@@'''

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'rivetti-site-setup'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def main():
    print('1/4  Download delle risorse…')
    data = {}
    for url, path, magic in FILES:
        try:
            b = fetch(url)
        except Exception as e:
            sys.exit(f'ERRORE: impossibile scaricare {url}\n({e})\nNessun file è stato modificato.')
        if len(b) < 200 or (magic and not b.startswith(magic)):
            sys.exit(f'ERRORE: il file scaricato da {url} non è valido.\nNessun file è stato modificato.')
        data[path] = b
        print('     ok', path, f'({len(b)//1024} KB)')

    print('2/4  Copia di sicurezza in _backup_prima_dello_script/ …')
    bk = os.path.join(ROOT, '_backup_prima_dello_script')
    os.makedirs(bk, exist_ok=True)
    for p in PAGES:
        src = os.path.join(ROOT, p)
        if os.path.exists(src) and not os.path.exists(os.path.join(bk, p)):
            shutil.copy2(src, os.path.join(bk, p))

    print('3/4  Scrittura dei file locali…')
    for path, b in data.items():
        full = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, 'wb').write(b)
    css = '/* Font ospitati sul sito (Sora e Inter, licenza SIL OFL 1.1 — vedi assets/fonts/LICENSE-*.txt) */\n'
    for fid, (fam, weights) in FONTS.items():
        for w in weights:
            css += (f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};font-display:swap;"
                    f"src:url(assets/fonts/{fid}-latin-{w}.woff2) format('woff2');unicode-range:{LATIN}}}\n")
    open(os.path.join(ROOT, 'fonts.css'), 'w', encoding='utf-8').write(css)

    print('4/4  Aggiornamento delle pagine…')
    for p in PAGES:
        full = os.path.join(ROOT, p)
        if not os.path.exists(full):
            continue
        h = open(full, encoding='utf-8').read()
        h = h.replace('<link rel="preconnect" href="https://fonts.googleapis.com">\n', '')
        pre = '/' if p == '404.html' else ''          # la 404 usa percorsi dalla radice
        h = re.sub(r'<link href="https://fonts\.googleapis\.com/css2\?[^"]*" rel="stylesheet">',
                   f'<link rel="stylesheet" href="{pre}fonts.css">', h)
        if 'pagine.css' in h and 'rel="preload"' not in h:       # pagine del sito (non legali): precarica i due font principali
            h = h.replace(f'<link rel="stylesheet" href="{pre}fonts.css">',
                f'<link rel="preload" href="{pre}assets/fonts/sora-latin-700.woff2" as="font" type="font/woff2" crossorigin>\n'
                f'<link rel="preload" href="{pre}assets/fonts/inter-latin-400.woff2" as="font" type="font/woff2" crossorigin>\n'
                f'<link rel="stylesheet" href="{pre}fonts.css">', 1)
        h = re.sub(r'<!--EXT:privacy-->.*?<!--/EXT-->', lambda m: '<!--EXT:privacy-->\n' + EXT_PRIVACY_LOCAL + '\n<!--/EXT-->', h, flags=re.S)
        h = re.sub(r'<!--EXT:cookie-->.*?<!--/EXT-->', lambda m: '<!--EXT:cookie-->\n' + EXT_COOKIE_LOCAL + '\n<!--/EXT-->', h, flags=re.S)
        open(full, 'w', encoding='utf-8').write(h)
        left = re.findall(r'https://(?:fonts\.googleapis\.com|fonts\.gstatic\.com|cdn\.jsdelivr\.net)[^"\']*', h)
        print('    ', p, '— riferimenti esterni residui:', len(left))
    for j in JS_FILES:
        full = os.path.join(ROOT, j)
        if os.path.exists(full):
            shutil.copy2(full, os.path.join(bk, j)) if not os.path.exists(os.path.join(bk, j)) else None
            js = open(full, encoding='utf-8').read()
            js = js.replace('https://cdn.jsdelivr.net/npm/globe.gl@2.34.4/dist/globe.gl.min.js', 'assets/vendor/globe.gl.min.js')
            js = js.replace('https://cdn.jsdelivr.net/npm/three-globe@2.31.0/example/img/', 'assets/vendor/')
            open(full, 'w', encoding='utf-8').write(js)
            print('    ', j, '— riferimenti esterni residui:', len(re.findall(r'https://cdn\.jsdelivr\.net', js)))
    print('\nFatto. Apri index.html e controlla che font e globo siano come prima.')
    print('Per tornare indietro: copia i file da _backup_prima_dello_script/ nella cartella del sito.')

if __name__ == '__main__':
    main()
