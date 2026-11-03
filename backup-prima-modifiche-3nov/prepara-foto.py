#!/usr/bin/env python3
"""Prepara le foto del sito: crea le versioni leggere (-480, -800, -1200, -1600 px di larghezza) in JPG e WebP.

Uso (dal computer, serve Pillow:  pip install pillow):
    python3 prepara-foto.py                       # assets/realizzazioni/, assets/gallerie/ e assets/servizi/ (copertine)
    python3 prepara-foto.py assets/realizzazioni/mio-progetto

Le foto originali NON vengono modificate. Le versioni già esistenti vengono rigenerate solo se l'originale è più recente.
Il sito (build.py) usa in automatico le versioni create, con lo srcset: su telefono si scaricano file molto più piccoli.
Prima di pubblicare togli dalle foto i metadati di posizione: questo script li rimuove dalle versioni create (non dall'originale).
"""
import os
import re
import sys

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit('Serve Pillow: pip install pillow')

LARGHEZZE = (480, 800, 1200, 1600)
VARIANTE = re.compile(r'-(480|800|1200|1600)\.(jpg|jpeg|png|webp)$', re.I)
ROOT = os.path.dirname(os.path.abspath(__file__))


def elabora(cartella):
    n = 0
    for dp, _, fs in os.walk(cartella):
        for f in sorted(fs):
            if not f.lower().endswith(('.jpg', '.jpeg', '.png')) or VARIANTE.search(f):
                continue
            src = os.path.join(dp, f)
            stem = os.path.splitext(src)[0]
            with Image.open(src) as im:
                im = ImageOps.exif_transpose(im).convert('RGB')      # applica la rotazione e scarta i metadati
                for w in LARGHEZZE:
                    if w >= im.width:
                        continue
                    h = round(im.height * w / im.width)
                    r = im.resize((w, h), Image.LANCZOS)
                    for ext, kw in (('jpg', dict(quality=82, optimize=True, progressive=True)), ('webp', dict(quality=80, method=6))):
                        dst = f'{stem}-{w}.{ext}'
                        if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
                            continue
                        r.save(dst, **kw)
                        n += 1
    return n


if __name__ == '__main__':
    cartelle = sys.argv[1:] or [os.path.join(ROOT, 'assets', d) for d in ('realizzazioni', 'gallerie', 'servizi')]
    tot = sum(elabora(c) for c in cartelle)
    print(f'Create {tot} versioni leggere.')
