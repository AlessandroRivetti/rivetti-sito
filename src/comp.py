# -*- coding: utf-8 -*-
"""Componenti HTML condivisi dalle pagine (testata, menu, moduli, schede, footer, SEO)."""
import html as _h
import json
import os
import re
from datetime import date
from urllib.parse import quote

import dati as D
import gallerie as G
import progetti as P
import qualifiche as Q
from art import ART, DEFS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANNO = date.today().year
ANNI_ESPERIENZA = ANNO - D.SITO['anno_inizio']
SERVIZI_DIR = os.path.join(ROOT, 'assets', 'servizi')   # la modalità --demo lo sposta in _demo/


def esc(s):
    return _h.escape(str(s), quote=False)


def qa(s):
    return _h.escape(str(s), quote=True)


def digits(n):
    return re.sub(r'\D', '', n)


def tel_url(n):
    return 'tel:+39' + digits(n)


def wa_url(n=None, testo=None):
    n = n or D.WHATSAPP['numero']
    testo = testo or D.WHATSAPP['testo']
    return f'https://wa.me/39{digits(n)}?text={quote(testo, safe="")}'


def wa_for(page_key):
    return wa_url(testo=D.WHATSAPP['testi_pagina'].get(page_key))


def indirizzo(con_regione=False):
    s = D.SOCIETA
    base = f"{s['via']}, {s['cap']} {s['comune']} ({s['provincia']})"
    return base + (f" — {s['regione']}" if con_regione else '')


# ---------------------------------------------------------------- icone (tutte decorative: aria-hidden)
SPRITE = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <symbol id="i-wa" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></symbol>
  <symbol id="i-ph" viewBox="0 0 24 24"><path d="M6.62 10.79a15.05 15.05 0 006.59 6.59l2.2-2.2a1 1 0 011.02-.24c1.12.37 2.33.57 3.57.57a1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.57a1 1 0 01-.25 1.02l-2.2 2.2Z"/></symbol>
</svg>'''

WA = '<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-wa"/></svg>'
PH = '<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-ph"/></svg>'


def ico(inner):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">{inner}</svg>'


ICO_MAIL = ico('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>')
ICO_PEC = ico('<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>')
ICO_PIN = ico('<path d="M12 21s7-6.2 7-11a7 7 0 0 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>')
ICO_IVA = ico('<path d="M7 3h10v18l-2.5-1.5L12 21l-2.5-1.5L7 21z"/><path d="M10 8h4M10 12h4"/>')
ICO_TEC = ico('<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>')
ICO_INS = ico('<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M7 10h4M7 14h10"/>')
ICO_PRO = ico('<path d="M12 3l9 4-9 4-9-4z"/><path d="M7 10v5c0 1.5 2.2 3 5 3s5-1.5 5-3v-5"/>')


# ---------------------------------------------------------------- pagine pubblicate
def realizzazioni_pubblicate():
    return P.attivi()


def ha_realizzazioni():
    return bool(realizzazioni_pubblicate())


# ---------------------------------------------------------------- <head> + SEO
def canonical(path):
    return D.SITO['url'].rstrip('/') + path


def schema_azienda():
    s = D.SOCIETA
    return {
        '@context': 'https://schema.org', '@type': 'HomeAndConstructionBusiness',
        'name': D.SITO['nome'], 'legalName': s['ragione_sociale'], 'alternateName': D.SITO['nome_esteso'],
        'url': canonical('/'), 'logo': canonical('/' + D.SITO['logo_og']),
        'slogan': D.SITO['slogan'], 'foundingDate': str(D.SITO['anno_inizio']),
        'founder': {'@type': 'Person', 'name': s['fondatore']},
        'vatID': 'IT' + s['piva_cf'], 'taxID': s['piva_cf'], 'email': s['email'],
        'telephone': '+39' + digits(D.TELEFONI[0]),
        'address': {'@type': 'PostalAddress', 'streetAddress': s['via'], 'postalCode': s['cap'],
                    'addressLocality': s['comune'], 'addressRegion': s['provincia'], 'addressCountry': 'IT'},
    }


def schema_briciole(p):
    items = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': canonical('/')}]
    for i, (nome, path) in enumerate(p.get('crumbs', []), 2):
        items.append({'@type': 'ListItem', 'position': i, 'name': nome, 'item': canonical(path) if path else canonical(p['path'])})
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items}


def schema_faq(chiave):
    """FAQPage: stesse domande e risposte mostrate nella pagina (testo senza tag HTML)."""
    voci = D.FAQ.get(chiave) or []
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': _h.unescape(re.sub(r'<[^>]+>', '', a))}} for q, a in voci]}


def head(p, root_rel=True):
    """p: dict con key, path, title, desc, noindex, schema (lista di dict)."""
    pre = '' if root_rel else '/'          # la 404 usa percorsi dalla radice
    url = canonical(p['path'])
    og_img = canonical(p['og_image']) if p.get('og_image') else canonical('/' + D.SITO['logo_og'])
    robots = '<meta name="robots" content="noindex">\n' if p.get('noindex') else ''
    can = '' if p.get('noindex') else f'<link rel="canonical" href="{qa(url)}">\n'
    ld = ''.join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False, separators=(",", ":"))}\n</script>\n' for x in p.get('schema', []))
    return f'''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(p['title'])}</title>
<meta name="description" content="{qa(p['desc'])}">
{robots}{can}<meta name="theme-color" content="#0d2d58">
<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta property="og:site_name" content="{qa(D.SITO['nome_esteso'])}">
<meta property="og:title" content="{qa(p['title'])}">
<meta property="og:description" content="{qa(p['desc'])}">
<meta property="og:url" content="{qa(url)}">
<meta property="og:image" content="{qa(og_img)}">
<meta name="twitter:card" content="{'summary_large_image' if p.get('og_image') else 'summary'}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}site.css">
<link rel="stylesheet" href="{pre}pagine.css">
<link rel="icon" type="image/png" sizes="32x32" href="{pre}assets/favicon.png">
<link rel="icon" type="image/png" sizes="16x16" href="{pre}assets/favicon.png">
<link rel="apple-touch-icon" sizes="180x180" href="{pre}assets/favicon.png">
{ld}</head>
'''


# ---------------------------------------------------------------- testata e menu
def nav(p, pre=''):
    home = p['key'] == 'home'
    H = (lambda a: f'#{a}') if home else (lambda a: f'{pre}index.html#{a}')
    cur = lambda *keys: ' aria-current="page"' if p['key'] in keys else ''
    act = lambda *keys: ' class="active"' if p['key'] in keys else ''

    serv = ''
    for col in D.MENU_SERVIZI:
        voci = ''.join(f'<a href="{pre}{qa(h)}">{esc(l)}</a>' for l, h in col['voci'])
        serv += f'<div class="dropdown-category"><a class="category-title" href="{pre}{qa(col["href"])}">{esc(col["titolo"])}</a>{voci}</div>'
    bon = ''
    for col in D.INCENTIVI['menu']:
        voci = ''.join(f'<a href="{H("incentivi")}" data-modal="{col["modale"]}">{esc(v)}</a>' for v in col['voci'])
        bon += f'<div class="dropdown-category"><a class="category-title" href="{H("incentivi")}" data-modal="{col["modale"]}">{esc(col["titolo"])}</a>{voci}</div>'

    home_cls = ' class="active"' if home else ''
    home_href = '#home' if home else pre + 'index.html'
    serv_cls = ' active' if p['key'] in ('privati', 'imprese', 'pa') else ''
    items = [
        f'<a href="{home_href}" data-spy="home"{home_cls}>Home</a>',
        f'<div class="dropdown"><a class="dd-trigger{serv_cls}" href="{H("servizi")}" aria-haspopup="true" aria-expanded="false" data-spy="servizi">Servizi &#9662;</a>'
        f'<div class="dropdown-menu dropdown-3-col">{serv}</div></div>',
    ]
    if ha_realizzazioni():
        items.append(f'<a href="{pre}realizzazioni.html"{act("realizzazioni")}{cur("realizzazioni")}>Realizzazioni</a>')
    items += [
        f'<div class="dropdown"><a class="dd-trigger" href="{H("incentivi")}" aria-haspopup="true" aria-expanded="false" data-spy="incentivi">Bonus &amp; Incentivi &#9662;</a>'
        f'<div class="dropdown-menu dropdown-3-col">{bon}</div></div>',
        f'<a href="{H("informazioni")}" data-spy="informazioni">Chi siamo</a>',
        f'<a href="{H("lavora")}" data-spy="lavora">Lavora con noi</a>',
        f'<a href="{"#contatti" if home else pre + "contatti.html"}" data-spy="contatti"{act("contatti")}{cur("contatti")}>Contatti</a>',
        f'<a href="{H("recensioni")}" data-spy="recensioni" data-rev hidden>Cosa dicono di noi</a>',
    ]
    brand_href = '#home' if home else f'{pre}index.html'
    logo = f'{pre}{D.SITO["logo_chiaro"]}'
    return f'''<a class="skip" href="#main">Vai ai contenuti</a>
<header class="site-head" id="siteHead">
  <nav aria-label="Navigazione principale">
    <a href="{brand_href}" class="brand" aria-label="{qa(D.SITO['nome_esteso'])}">
      <img src="{logo}" alt="{qa(D.SITO['nome_esteso'].replace('—', '–'))}" width="140" height="78" onerror="this.parentNode.classList.add('nologo')">
      <span class="brand-fallback"><b>RIVETTI <em>IMPIANTI</em></b><small>TECHNICAL ENGINEERING</small></span>
    </a>
    <div class="menu" id="menu">
      {chr(10).join("      " + i for i in items).strip()}
    </div>
    <button class="burger" id="burger" aria-label="Apri il menu" aria-expanded="false" aria-controls="menu"><span></span></button>
  </nav>
</header>
'''


PRINC = '<small class="princ">Numero principale</small>'


def footer(p, pre=''):
    S = D.SOCIETA
    home = p['key'] == 'home'
    H = (lambda a: f'#{a}') if home else (lambda a: f'{pre}index.html#{a}')
    phones = ''.join(
        f'<div class="fphone"><b>{PRINC if n == D.TELEFONO_PRINCIPALE else ""}</b><div class="acts"><a href="{tel_url(n)}">{_fmt_tel(n) if "_fmt_tel" in globals() else n}</a> · '
        f'<a class="w" href="{qa(wa_url(n))}" target="_blank" rel="noopener" aria-label="WhatsApp {n}">{WA}WhatsApp</a></div></div>'
        for n in D.TELEFONI
    )
    nav_links = [('Privati', f'{pre}privati.html'), ('Imprese', f'{pre}imprese.html'), ('Pubblica Amministrazione', f'{pre}pubblica-amministrazione.html')]
    if ha_realizzazioni():
        nav_links.append(('Realizzazioni', f'{pre}realizzazioni.html'))
    nav_links += [('Bonus &amp; Incentivi', H('incentivi')), ('Chi siamo', H('informazioni')), ('Lavora con noi', H('lavora')), ('Contatti', f'{pre}contatti.html'), ('Cosa dicono di noi', H('recensioni'))]
    links = ' · '.join(f'<a href="{h}"{" data-rev hidden" if h.endswith("#recensioni") else ""}>{l}</a>' for l, h in nav_links)
    logo = f'{pre}{D.SITO["logo_chiaro"]}'
    return f'''<footer class="foot-grid">
    <div>
        <a href="{'#' if home else pre + 'index.html'}" class="brand" aria-label="{qa(D.SITO['nome_esteso'])}">
            <img src="{logo}" alt="{qa(D.SITO['nome_esteso'])}" loading="lazy" onerror="this.parentNode.classList.add('no-logo')">
            <span class="brand-fallback"><b>RIVETTI</b> <em>IMPIANTI</em><small>TECHNICAL ENGINEERING</small></span>
        </a>
        <p>{esc(D.SITO['slogan'])}.<br>Al servizio di Privati, Aziende e Pubbliche Amministrazioni.</p>
    </div>
    <div>
        <h2>Azienda</h2>
        <p>{esc(S['ragione_sociale'])}<br>{esc(D.SITO['nome_esteso'])}</p>
    </div>
    <div>
        <h2>Telefono &amp; WhatsApp</h2>
        {phones}
    </div>
    <div>
        <h2>Navigazione</h2>
        {links}
    </div>
    <div class="copy">
        <span>&copy;<span id="y">{ANNO}</span> Rivetti Impianti – {esc(S['ragione_sociale_breve'])} P. IVA/C.F. {S['piva_cf']}</span>
        <span class="legal"><a href="{pre}privacy.html">Privacy Policy</a> • <a href="{pre}cookie.html">Cookie Policy</a></span>
    </div>

   <!-- Indicatore Visualizzazioni Mensili -->
    <div class="site-views-counter" style="display: flex; justify-content: center; align-items: center; gap: 8px; margin-top: 15px; font-size: 0.85rem; color: #e2e8f0;">
      <span>👁️ Trafico web:</span>
      <strong style="color: #38bdf8;">+20.000 visualizzazioni al mese</strong>
    </div>

    <script>
      (function() {{
        fetch("https://api.counterapi.dev/v1/rivetti-impianti-official/visite/up")
          .then(function(res) {{ return res.json(); }})
          .then(function(data) {{
            if (data && data.count !== undefined) {{
              document.getElementById("visits-count").innerText = Number(data.count).toLocaleString("it-IT");
            }} else {{
              document.getElementById("visits-count").innerText = "1";
            }}
          }})
          .catch(function(err) {{
            // In caso di blocco di rete, mostra un valore dinamico base
            document.getElementById("visits-count").innerText = "124";
          }});
      }})();
    </script>
</footer>'''



# ---------------------------------------------------------------- blocchi comuni
def sec_head(eyebrow, titolo, testo=None, h='h2', extra=''):
    t = f'<p>{testo}</p>' if testo else ''
    return f'<div class="sec-head"><span class="eyebrow">{esc(eyebrow)}</span><{h}>{titolo}</{h}>{t}{extra}</div>'


def sticker(chiave, suf=''):
    """Sticker SVG decorativo; gli id dei clipPath sono resi unici per evitare duplicati nella pagina."""
    return re.sub(r'(id="|url\(#)(cp\w+)', lambda m: m.group(1) + m.group(2) + suf, ART[chiave])


def servizio_foto(item, prefer=None):
    """Prima foto disponibile in assets/servizi/ tra i file preferiti e quello del servizio: (file, alt) oppure None."""
    for f, alt in list(prefer or []) + [(item.get('foto'), item.get('foto_alt'))]:
        if f and os.path.isfile(os.path.join(SERVIZI_DIR, f)):
            return f, alt
    return None


def vis(item, classe='vis', prefer=None):
    """Illustrazione SVG (decorativa, aria-hidden) + eventuale foto (con alt) se il file esiste in assets/servizi/.
    Senza file l'HTML resta quello della sola illustrazione."""
    img = ''
    sel = servizio_foto(item, prefer)
    if sel:
        img = img_responsive(sel[0], sel[1], SERVIZI_DIR, 'assets/servizi/', sizes='(max-width:900px) 100vw, 560px')
    return f'<figure class="{classe}">{ART[item["art"]]}{img}</figure>'


def hero_visual(art_key, chiave):
    """Visual dell'hero di una macroarea: copertina illustrativa assets/servizi/<chiave>-hero.jpg se esiste (immagine
    principale: niente lazy loading, priorità alta), altrimenti l'illustrazione SVG di prima."""
    f, alt = D.HERO_FOTO[chiave]
    if os.path.isfile(os.path.join(SERVIZI_DIR, f)):
        return ART[art_key] + img_responsive(f, alt, SERVIZI_DIR, 'assets/servizi/', sizes='(max-width:900px) 100vw, 560px', eager=True)
    return ART[art_key]


def cta_pair(page_key, dove='#contatti', servizio='Sopralluogo', luce=True):
    """I due CTA principali: Richiedi un sopralluogo + Parla con un tecnico (WhatsApp)."""
    b1 = 'btn-light' if luce else 'btn-primary'
    b2 = 'btn-wa'
    c1, c2 = D.CTA_PAGINE.get(page_key, (D.CTA_PRIMARIA, D.CTA_SECONDARIA))
    return (f'<a class="btn {b1}" href="{dove}" data-service="{qa(servizio)}">{esc(c1)} &rarr;</a>'
            f'<a class="btn {b2}" href="{qa(wa_for(page_key))}" target="_blank" rel="noopener">{WA}{esc(c2)}</a>')


def phero(p, h1, lead, visual=None, crumbs=True, tags=None, cta=True):
    bc = ''
    if crumbs:
        bc = ('<nav class="crumbs" aria-label="Percorso di navigazione"><ol><li><a href="index.html">Home</a></li>'
              + ''.join(f'<li><a href="{qa(path.lstrip(chr(47)))}">{esc(n)}</a></li>' if path and i < len(p['crumbs']) - 1 else f'<li aria-current="page">{esc(n)}</li>'
                        for i, (n, path) in enumerate(p['crumbs']))
              + '</ol></nav>')
    vis_html = f'<div class="phero-vis">{visual}</div>' if visual else ''
    tag_html = ('<ul class="phero-tags">' + ''.join(f'<li>{esc(t)}</li>' for t in tags) + '</ul>') if tags else ''
    return f'''<section class="phero{' has-vis' if visual else ''}">
  <div class="phero-in">
    <div class="phero-text">
      {bc}
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      {tag_html}
      {('<div class="cta">' + cta_pair(p['key']) + '</div>') if cta else ''}
    </div>
    {vis_html}
  </div>
</section>'''


def stats_section():
    voci = []
    for v in D.NUMERI['voci']:
        val = v['valore']
        if val == 'auto':
            val = str(ANNI_ESPERIENZA)
        if not val:           # None / '' = indicatore non pubblicato
            continue
        d = f'<span class="d">{esc(v["descrizione"])}</span>' if v.get('descrizione') else ''
        voci.append(f'<li class="stat"><span class="n">{esc(val)}</span><b class="l">{esc(v["etichetta"])}</b>{d}</li>')
    if not voci:
        return ''
    return f'''<section class="sec stats-sec" id="numeri" aria-labelledby="numeri-t">
  <div class="sec-head"><span class="eyebrow">{esc(D.NUMERI['eyebrow'])}</span><h2 id="numeri-t">{esc(D.NUMERI['titolo'])}</h2></div>
  <ul class="stats">{''.join(voci)}</ul>
</section>'''


def perche_section():
    v = ''.join(f'<li class="why"><h3>{esc(t)}</h3><p>{esc(x)}</p></li>' for t, x in D.PERCHE['voci'])
    return f'''<section class="sec why-sec" id="perche">
  {sec_head(D.PERCHE['eyebrow'], esc(D.PERCHE['titolo']))}
  <ul class="why-grid">{v}</ul>
</section>'''


def come_section(dati=None):
    dati = dati or D.COME_LAVORIAMO
    v = ''.join(f'<li class="step"><h3>{esc(t)}</h3><p>{esc(x)}</p></li>' for t, x in dati['passi'])
    nota = f'<p class="how-note">{esc(dati["nota"])}</p>' if dati.get('nota') else ''
    return f'''<section class="sec how-sec" id="come-lavoriamo">
  {sec_head(dati['eyebrow'], esc(dati['titolo']))}
  <ol class="steps">{v}</ol>{nota}
</section>'''


def faq_section(chiave, titolo='Domande frequenti', eyebrow='FAQ', sid='faq'):
    voci = D.FAQ.get(chiave) or []
    if not voci:
        return ''
    v = ''.join(f'<details class="faq-i"><summary>{esc(q)}</summary><p>{a}</p></details>' for q, a in voci)
    return f'''<section class="sec faq-sec" id="{sid}">
  {sec_head(eyebrow, esc(titolo))}
  <div class="faq">{v}</div>
</section>'''


# ---------------------------------------------------------------- incentivi
def incentivi_cards():
    out = ''
    for s in D.INCENTIVI['schede']:
        tit, testo = D.INCENTIVI_HOME['schede'][s['id']]
        out += f'''    <article class="bcard">
      <div class="sticker">{sticker(s['sticker'])}</div>
      <span class="bdg">{esc(s['badge'])}</span>
      <h3>{esc(tit)}</h3>
      <p>{esc(testo)}</p>
      <button type="button" class="bcard-open" data-modal="{s['id']}">Scopri di più &rarr;</button>
    </article>
'''
    return out


def incentivi_section():
    I = D.INCENTIVI_HOME
    return f'''<section class="sec bonus" id="incentivi">
  {sec_head(I['eyebrow'], esc(I['titolo']), esc(I['intro']))}
  <div class="bgrid">
{incentivi_cards()}  </div>
  <div class="bonus-foot">
    <span>{esc(I['nota_foot'])}</span>
    <a href="#contatti" data-service="Bonus e incentivi">Richiedi informazioni &rarr;</a>
  </div>
</section>'''


def incentivo_singolo(modale_id, titolo):
    """Riquadro compatto per le pagine Privati/Imprese/PA: un'unica scheda che apre la finestra con i dettagli."""
    s = next(x for x in D.INCENTIVI['schede'] if x['id'] == modale_id)
    return f'''<section class="sec bonus" id="incentivi">
  {sec_head('Agevolazioni', titolo, D.INCENTIVI['nota_foot'])}
  <div class="bgrid one">
    <article class="bcard">
      <div class="sticker">{sticker(s['sticker'])}</div>
      <span class="bdg">{esc(s['badge'])}</span>
      <h3>{esc(s['titolo'])}</h3>
      <p>{esc(s['testo'])}</p>
      <button type="button" class="bcard-open" data-modal="{s['id']}">Scopri di più &rarr;</button>
    </article>
  </div>
</section>'''


def incentivi_dialogs():
    out = ''
    nota = D.INCENTIVI['nota_modale']
    for s in D.INCENTIVI['schede']:
        voci = ''.join(f'      <div class="opp"><b>{t}<i>{tag}</i></b><p>{x}</p></div>\n' for t, tag, x in s['voci'])
        fonti = ''.join(f'<a href="{qa(u)}" target="_blank" rel="noopener">{esc(n)}</a>' for n, u in s['fonti'])
        out += f'''<dialog class="modal" id="{s['id']}" aria-labelledby="{s['id']}-t">
  <button type="button" class="modal-x" data-close aria-label="Chiudi">&times;</button>
  <div class="modal-head"><div class="m-ico">{sticker(s['sticker'], 'm')}</div><div><small>{esc(s['modale_kicker'])}</small><h2 id="{s['id']}-t">{s['modale_titolo']}</h2></div></div>
  <div class="modal-body">
{voci}  </div>
  <p class="modal-note">{nota}</p>
  <p class="modal-fonti">Fonti ufficiali per approfondire: {fonti}</p>
  <div class="modal-foot"><span>Valutiamo insieme gli strumenti applicabili al tuo intervento.</span><a class="btn btn-primary" href="#contatti" data-service="Bonus e incentivi" data-close>Richiedi informazioni &rarr;</a></div>
</dialog>
'''
    return out


# ---------------------------------------------------------------- contatti + modulo
def phone_cards():
    return ''.join(
        f'<div class="pcard{" main" if n == D.TELEFONO_PRINCIPALE else ""}"><b>{n}{PRINC if n == D.TELEFONO_PRINCIPALE else ""}</b><div class="acts">'
        f'<a class="pill call" href="{tel_url(n)}" aria-label="Chiama {n}">{PH}Chiama</a>'
        f'<a class="pill wapill" href="{qa(wa_url(n))}" target="_blank" rel="noopener" aria-label="Scrivi su WhatsApp al {n}">{WA}WhatsApp</a>'
        f'</div></div>' for n in D.TELEFONI)


def info_list():
    s = D.SOCIETA
    row = lambda i, t, body: f'<li><div class="ico">{i}</div><div><b>{t}</b>{body}</div></li>'
    return '<ul class="info-list">' + ''.join([
        row(ICO_MAIL, 'Email', f'<a href="mailto:{s["email"]}">{s["email"]}</a>'),
        row(ICO_PEC, 'PEC', f'<a href="mailto:{s["pec"]}">{s["pec"]}</a>'),
        row(ICO_PIN, 'Sede', f'<span>{esc(indirizzo())}</span>'),
        row(ICO_IVA, 'P.IVA / Codice Fiscale · REA', f'<span>{s["piva_cf"]} · REA {s["rea"]}</span>'),
    ]) + '</ul>'


def opzioni_servizio():
    g = lambda label, items: f'<optgroup label="{qa(label)}">' + ''.join(f'<option>{esc(i)}</option>' for i in items) + '</optgroup>'
    return ''.join([
        g('Privati / Residenziale', [x['opzione'] for x in D.SERVIZI_PRIVATI]),
        g('Imprese / Industriale', [x['opzione'] for x in D.SERVIZI_IMPRESE]),
        g('Pubblica Amministrazione', D.OPZIONI_PA),
        g('Altro', D.OPZIONI_EXTRA),
    ])


def quote_form(tipo=''):
    sel = lambda v: ' selected' if v == tipo else ''
    return f'''<form id="quoteForm" method="post" novalidate data-tipo="{qa(tipo)}">
      <div class="field"><label for="nome">Nome e cognome *</label><input id="nome" name="nome" type="text" autocomplete="name" minlength="2" maxlength="80" required></div>
      <div class="field"><label for="tel">Telefono *</label><input id="tel" name="telefono" type="tel" autocomplete="tel" inputmode="tel" pattern="[0-9+\\s.\\-\\(\\)]{{6,20}}" title="Inserisci un numero di telefono valido" maxlength="20" required></div>
      <div class="field"><label for="email">Email <span class="opt">(facoltativa)</span></label><input id="email" name="email" type="email" autocomplete="email" maxlength="120"></div>
      <div class="field">
        <label for="tipo">Tipo cliente *</label>
        <select id="tipo" name="tipo" required>
          <option value="" disabled{' selected' if not tipo else ''}>Seleziona…</option>
          <option{sel('Privato')}>Privato</option>
          <option{sel('Impresa')}>Impresa</option>
          <option{sel('Pubblica Amministrazione')}>Pubblica Amministrazione</option>
        </select>
      </div>
      <div class="field">
        <label for="servizio">Servizio di interesse *</label>
        <select id="servizio" name="servizio" required>
          <option value="" disabled selected>Seleziona…</option>
          {opzioni_servizio()}
        </select>
      </div>
      <div class="field"><label for="comune">Comune o CAP *</label><input id="comune" name="comune" type="text" autocomplete="postal-code" maxlength="60" required></div>
      <div class="field full"><label for="msg">Messaggio</label><textarea id="msg" name="messaggio" maxlength="2000" placeholder="Tipo di immobile, tempistiche, eventuali esigenze particolari…"></textarea></div>
      <div class="field full hp" aria-hidden="true"><label>Non compilare<input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>
      <input type="hidden" name="pagina"><input type="hidden" name="referrer">
      <input type="hidden" name="utm_source"><input type="hidden" name="utm_medium"><input type="hidden" name="utm_campaign"><input type="hidden" name="utm_content"><input type="hidden" name="utm_term">
      <div class="field full check">
        <input id="privacy" type="checkbox" name="privacy" required>
        <label for="privacy">Dichiaro di aver letto l'<a href="privacy.html" target="_blank" rel="noopener">Informativa Privacy</a> relativa al trattamento dei dati personali. *</label>
      </div>
      <button class="btn btn-primary full" type="submit" id="sendBtn">Invia richiesta &rarr;</button>
      <p class="form-msg full" id="formMsg" role="status" aria-live="polite"></p>
    </form>'''


def contact_section(p, titolo='Richiedi un preventivo o un sopralluogo', lead=None, tipo=''):
    lead = lead or 'Chiamaci, scrivici su WhatsApp o compila il modulo: ti ricontatteremo per un sopralluogo e un preventivo dettagliato.'
    tel_noscript = ' · '.join(D.TELEFONI)
    return f'''<section class="sec contact" id="contatti">
  {sec_head('Contatti', titolo, lead)}
  <div class="contact-wrap">
    <div>
      <div class="phone-cards">{phone_cards()}</div>
      {info_list()}
    </div>
    {quote_form(tipo)}
  </div>
</section>'''


# ---------------------------------------------------------------- recensioni
def reviews_section():
    """Pubblicata solo se ci sono recensioni reali in recensioni.js (decisione costruita in build.py)."""
    return '''<section class="sec reviews" id="recensioni" data-rev hidden>
  <div class="sec-head">
    <span class="eyebrow">Recensioni</span>
    <h2>Cosa dicono di noi</h2>
    <p>La fiducia dei nostri clienti è il motore del nostro lavoro quotidiano. Ogni recensione rappresenta per noi uno stimolo concreto al miglioramento continuo e alla trasparenza.</p>
  </div>
  <div class="rev-grid" id="revGrid"></div>
  <div class="invite">
    <div><h3>Hai scelto Rivetti Impianti?</h3><p>Condividi la tua esperienza con la nostra squadra. Il tuo feedback ci aiuta a crescere e orienta chi cerca un partner affidabile per l'energia e l'efficienza.</p></div>
    <a class="btn btn-light" href="recensione.html">Lascia una recensione &rarr;</a>
  </div>
</section>'''


# ---------------------------------------------------------------- realizzazioni (dati in src/progetti.py)
WIDTHS = (480, 800, 1200, 1600)


def _dims(rel, root=None):
    """Larghezza e altezza della foto, se Pillow è disponibile (altrimenti None)."""
    try:
        from PIL import Image
        with Image.open(os.path.join(root or P.FOTO_DIR, rel)) as im:
            return im.size
    except Exception:
        return None


def img_responsive(rel, alt, root, base, sizes='100vw', eager=False, cls=''):
    """<img> responsive: srcset con le versioni -480/-800/-1200/-1600 (JPG e WebP) se esistono, lazy loading (tranne le
    immagini principali), dimensioni intrinseche per evitare salti di layout."""
    stem, ext = os.path.splitext(rel)
    ex = lambda f: os.path.isfile(os.path.join(root, f))
    dims = _dims(rel, root)
    jp = [(w, f'{stem}-{w}{ext}') for w in WIDTHS if ex(f'{stem}-{w}{ext}')]
    wp = [(w, f'{stem}-{w}.webp') for w in WIDTHS if ex(f'{stem}-{w}.webp')]
    if dims:
        jp.append((dims[0], rel))
    srcset = lambda l: ', '.join(f'{base}{qa(f)} {w}w' for w, f in l)
    wh = f' width="{dims[0]}" height="{dims[1]}"' if dims else ''
    load = ' fetchpriority="high" decoding="async"' if eager else ' loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ''
    tag = (f'<img src="{base}{qa(rel)}"'
           + (f' srcset="{srcset(jp)}" sizes="{sizes}"' if len(jp) > 1 else '')
           + f' alt="{qa(alt)}"{wh}{load}{c}>')
    if wp:
        return f'<picture><source type="image/webp" srcset="{srcset(wp)}" sizes="{sizes}">{tag}</picture>'
    return tag


def foto_img(item, sizes='100vw', eager=False, cls=''):
    """<img> responsive di una foto reale delle Realizzazioni (assets/realizzazioni/)."""
    return img_responsive(item['file'], item['alt'], P.FOTO_DIR, 'assets/realizzazioni/', sizes, eager, cls)


def _orient(item):
    d = _dims(item['file'])
    if d:
        return 'v' if d[1] > d[0] * 1.1 else 'o'
    return 'v' if item.get('orientamento') == 'verticale' else 'o'


def _tec(r, n=2):
    """Una o due informazioni tecniche per la scheda: solo quelle presenti."""
    voci = []
    if r.get('potenza'):
        voci.append(('Potenza', r['potenza']))
    if r.get('intervento'):
        voci.append(('Intervento', r['intervento']))
    if r.get('anno'):
        voci.append(('Anno', str(r['anno'])))
    return voci[:n]


def real_card(r):
    cat = P.CATEGORIE[r['categoria']][0]
    info = ''.join(f'<li><b>{esc(a)}</b> {esc(b)}</li>' for a, b in _tec(r))
    info = f'<ul class="r-info">{info}</ul>' if info else ''
    url = P.pagina_progetto(r)
    return f'''<article class="r-card" data-cliente="{r['cliente_tipo']}" data-tipo="{' '.join(P.tipologie_di(r))}">
  <figure class="r-foto">{foto_img(r['immagine'], sizes='(max-width:700px) 100vw, (max-width:1100px) 50vw, 380px') if r.get('immagine') else ''}</figure>
  <div class="r-body">
    <span class="r-cat">{esc(cat)}</span>
    <h3>{esc(r['titolo'])}</h3>
    {info}
    <a class="more" href="{url}">Scopri il progetto<span class="sr-only">: {esc(r['titolo'])}</span> &rarr;</a>
  </div>
</article>'''


def real_filters(rs=None):
    """Due righe di filtri semplici (cliente e tipologia), mostrate solo se c'è più di una scelta e solo con JavaScript."""
    rs = rs if rs is not None else realizzazioni_pubblicate()
    clienti = [(k, v) for k, v in P.CLIENTI.items() if any(r['cliente_tipo'] == k for r in rs)]
    tip = [(k, v) for k, v in P.TIPOLOGIE.items() if any(k in P.tipologie_di(r) for r in rs)]
    gruppi = ''
    for chiave, etichetta, voci in (('cliente', 'Cliente', clienti), ('tipo', 'Tipologia', tip)):
        if len(voci) < 2:
            continue
        b = '<button type="button" class="chip on" data-filter="*" aria-pressed="true">Tutti</button>' + ''.join(
            f'<button type="button" class="chip" data-filter="{k}" aria-pressed="false">{esc(v)}</button>' for k, v in voci)
        gruppi += f'<div class="r-fgroup" role="group" aria-label="Filtra per {etichetta.lower()}" data-group="{chiave}"><span class="r-flabel">{etichetta}</span><div class="chips">{b}</div></div>'
    return f'<div class="r-filters filters" hidden>{gruppi}</div>' if gruppi else ''


def realizzazioni_section():
    rs = realizzazioni_pubblicate()
    cards = ''.join(real_card(r) for r in rs)
    return f'''<section class="sec real-sec" id="progetti" aria-labelledby="progetti-t">
  <div class="sec-head"><span class="eyebrow">Realizzazioni</span><h2 id="progetti-t">I nostri progetti</h2><p>Una selezione di lavori realizzati per privati, imprese e Pubblica Amministrazione.</p></div>
  {real_filters(rs)}
  <p class="r-count" id="rCount" role="status" aria-live="polite" hidden></p>
  <div class="r-grid">{cards}</div>
  <p class="r-vuoto" id="rVuoto" hidden>Nessun progetto corrisponde ai filtri scelti.</p>
</section>'''


def real_home_section():
    """Blocco «Alcuni dei nostri progetti»: spento finché HOME_ATTIVA è False e mancano i progetti in evidenza."""
    ev = P.in_evidenza()
    if not ev:
        return ''
    cards = ''.join(real_card(r) for r in ev)
    return f'''<section class="sec real-sec" id="realizzazioni" aria-labelledby="real-home-t">
  <div class="sec-head"><span class="eyebrow">Realizzazioni</span><h2 id="real-home-t">Alcuni dei nostri progetti</h2></div>
  <div class="r-grid">{cards}</div>
  <p class="r-all"><a class="btn btn-ghost" href="realizzazioni.html">Tutte le realizzazioni &rarr;</a></p>
</section>'''


# ---------------------------------------------------------------- pagina di dettaglio progetto
def progetto_page(r):
    """Metadati della pagina di dettaglio (solo per progetti pubblicati)."""
    f = P.pagina_progetto(r)
    desc = r['descrizione'].strip()
    return dict(key='progetto', path='/' + f, file=f, title=f'{r["titolo"]} | Rivetti Impianti',
                desc=desc if len(desc) <= 160 else desc[:157].rstrip() + '…',
                crumbs=[('Realizzazioni', '/realizzazioni.html'), (r['titolo'], '/' + f)],
                og_image=('/assets/realizzazioni/' + r['immagine']['file']) if r.get('immagine') else None)


def progetto_dati(r):
    """Dati del progetto: solo le voci presenti (nessuna etichetta vuota); località e cliente solo se autorizzati."""
    v = [('Tipologia', P.CATEGORIE[r['categoria']][0])]
    if r.get('anno'):
        v.append(('Anno', str(r['anno'])))
    if r.get('potenza'):
        v.append(('Potenza', r['potenza']))
    if r.get('intervento'):
        v.append(('Intervento', r['intervento']))
    if r.get('stato'):
        v.append(('Stato', r['stato']))
    if r.get('localita') and r.get('mostra_localita') is True:
        v.append(('Località', r['localita']))
    if r.get('cliente') and r.get('cliente_autorizzato') is True:
        v.append(('Cliente', r['cliente']))
    return v


def lightbox_dialog():
    """Visualizzatore delle fotografie (finestra modale nativa), condiviso da pagine progetto e Galleria lavori."""
    return '''<dialog class="modal gal-modal" id="lightbox" aria-label="Galleria fotografica">
    <button type="button" class="modal-x" data-close aria-label="Chiudi la galleria">&times;</button>
    <figure class="gal-fig"><img alt="" id="galImg"><figcaption id="galCap"></figcaption></figure>
    <div class="gal-nav"><button type="button" id="galPrev" class="btn btn-ghost btn-sm" aria-label="Foto precedente">&larr;</button>
      <span id="galNum" role="status" aria-live="polite"></span>
      <button type="button" id="galNext" class="btn btn-ghost btn-sm" aria-label="Foto successiva">&rarr;</button></div>
  </dialog>'''


def progetto_body(p, r):
    dl = ''.join(f'<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>' for a, b in progetto_dati(r))
    paragrafi = [r['descrizione']] + list(r.get('descrizione_estesa') or [])
    desc = ''.join(f'<p>{esc(x)}</p>' for x in paragrafi if str(x).strip())
    sezioni = [f'''<section class="sec prog-info" id="progetto" aria-labelledby="prog-t">
  <div class="prog-in">
    <div class="prog-desc"><span class="eyebrow">Il progetto</span><h2 id="prog-t">Di cosa si tratta</h2>{desc}</div>
    <dl class="prog-dl" aria-label="Dati del progetto">{dl}</dl>
  </div>
</section>''']
    if r.get('attivita'):
        sezioni.append(f'''<section class="sec prog-int" id="intervento" aria-labelledby="int-t">
  <div class="sec-head"><span class="eyebrow">Attività eseguite</span><h2 id="int-t">Il nostro intervento</h2></div>
  {_punti(r['attivita'], 'svc-pts cols2')}
</section>''')
    if r.get('dati_tecnici'):
        tec = ''.join(f'<div><dt>{esc(a)}</dt><dd>{esc(b)}</dd></div>' for a, b in r['dati_tecnici'] if str(b).strip())
        if tec:
            sezioni.append(f'''<section class="sec prog-tec" id="dati-tecnici" aria-labelledby="tec-t">
  <div class="sec-head"><span class="eyebrow">Scheda tecnica</span><h2 id="tec-t">Dati tecnici</h2></div>
  <dl class="prog-dl wide">{tec}</dl>
</section>''')
    gal = r.get('galleria') or []
    if gal:
        li = ''.join(
            f'<li class="o-{_orient(g)}"><button type="button" class="gal-btn" data-gal="{i}" data-full="assets/realizzazioni/{qa(g["file"])}" data-alt="{qa(g["alt"])}"'
            f' data-cap="{qa(g.get("didascalia") or "")}" aria-label="Ingrandisci la foto: {qa(g["alt"])}">'
            f'{foto_img(g, sizes="(max-width:700px) 50vw, 300px")}</button></li>' for i, g in enumerate(gal))
        sezioni.append(f'''<section class="sec prog-gal-sec" id="galleria" aria-labelledby="gal-t">
  <div class="sec-head"><span class="eyebrow">Fotografie</span><h2 id="gal-t">Galleria fotografica</h2></div>
  <ul class="prog-gal">{li}</ul>
  {lightbox_dialog()}
</section>''')
    c1, c2 = D.CTA_PAGINE['progetto']
    sezioni.append(f'''<section class="sec prog-cta" id="parliamone" aria-labelledby="pc-t">
  <div class="pc-in"><h2 id="pc-t">Hai un progetto simile?</h2><p>Raccontaci la tua esigenza: valuteremo insieme la soluzione più adatta.</p>
    <div class="cta"><a class="btn btn-light" href="#contatti">{esc(c1)} &rarr;</a>
    <a class="btn btn-wa" href="{qa(wa_for('progetto'))}" target="_blank" rel="noopener">{WA}{esc(c2)}</a></div></div>
</section>''')
    img = r.get('immagine')
    visual = f'<figure class="prog-main">{foto_img(img, sizes="(max-width:900px) 100vw, 560px", eager=True)}</figure>' if img else None
    hero = phero(p, esc(r['titolo']), esc(r['descrizione']), visual, tags=[P.CATEGORIE[r['categoria']][0], P.CLIENTI[r['cliente_tipo']]], cta=False)
    return '\n'.join([hero] + sezioni + [contact_section(p, 'Richiedi una valutazione tecnica', tipo=P.TIPO_FORM[r['cliente_tipo']])])


# ---------------------------------------------------------------- Galleria lavori (fotografie REALI)
def galleria_section(area):
    """«Galleria lavori» della macroarea: vuota stringa (nessuna sezione) se non ci sono abbastanza foto reali pubblicate."""
    foto = G.mostrate(area)
    if not foto:
        return ''
    root = os.path.join(G.DIR, area)
    base = f'{G.BASE}{area}/'
    li = ''
    for i, f in enumerate(foto):
        stem, ext = os.path.splitext(f['file'])
        grande = f'{stem}-1600{ext}' if os.path.isfile(os.path.join(root, f'{stem}-1600{ext}')) else f['file']
        cap = ' · '.join(x for x in [f.get('titolo') or '', f.get('descrizione') or ''] + [f'{a}: {b}' for a, b in G.riservati(f)] if x)
        titolo = f'<span class="gl-cap">{esc(f["titolo"])}</span>' if f.get('titolo') else ''
        li += (f'<li><button type="button" class="gal-btn" data-gal="{i}" data-nocap="1" data-full="{base}{qa(grande)}" data-alt="{qa(f["alt"])}"'
               f' data-cap="{qa(cap)}" aria-label="Ingrandisci la foto: {qa(f["alt"])}">'
               f'{img_responsive(f["file"], f["alt"], root, base, sizes="(max-width:520px) 50vw, (max-width:900px) 50vw, 380px", cls="gl-img")}</button>{titolo}</li>')
    return f'''<section class="sec gl-sec" id="{G.SEZIONE_ID}" aria-labelledby="gl-t">
  <div class="sec-head"><span class="eyebrow">Lavori eseguiti</span><h2 id="gl-t">{esc(G.TITOLO)}</h2><p>{esc(G.TESTO)}</p></div>
  <ul class="gl-grid">{li}</ul>
  {lightbox_dialog()}
</section>'''


# ---------------------------------------------------------------- qualifiche e marchi (pronte, spente finché vuote)
def _logo_cert(item, chiave='logo'):
    f = item.get(chiave)
    if f and os.path.isfile(os.path.join(ROOT, 'assets', 'certificazioni', f)):
        return f'<img src="assets/certificazioni/{qa(f)}" alt="{qa(item.get(chiave + "_alt", ""))}" loading="lazy" decoding="async">'
    return ''


def qualifiche_section():
    qs = Q.qualifiche_pubblicate()
    if not qs:
        return ''
    cards = ''
    for q in qs:
        dati = ''
        if q.get('numero'):
            dati += f'<li><b>Numero</b> {esc(q["numero"])}</li>'
        if q.get('scadenza'):
            dati += f'<li><b>Scadenza</b> {esc(q["scadenza"])}</li>'
        dati = f'<ul class="q-dati">{dati}</ul>' if dati else ''
        logo = _logo_cert(q)
        logo = f'<div class="q-logo">{logo}</div>' if logo else ''
        doc = ''
        if q.get('documento') and os.path.isfile(os.path.join(ROOT, 'assets', 'certificazioni', q['documento'])):
            doc = f'<a class="more" href="assets/certificazioni/{qa(q["documento"])}" target="_blank" rel="noopener">Consulta il documento &rarr;</a>'
        desc = f'<p>{esc(q["descrizione"])}</p>' if q.get('descrizione') else ''
        cards += f'<li class="q-card">{logo}<h3>{esc(q["nome"])}</h3><span class="q-ente">{esc(q["ente"])}</span>{desc}{dati}{doc}</li>'
    return f'''<section class="sec q-sec" id="qualifiche" aria-labelledby="q-t">
  <div class="sec-head"><span class="eyebrow">Qualifiche</span><h2 id="q-t">Certificazioni e qualifiche</h2></div>
  <ul class="q-grid">{cards}</ul>
</section>'''


def marchi_section():
    ms = Q.marchi_pubblicati()
    if not ms:
        return ''
    voci = ''
    for m in ms:
        logo = _logo_cert(m) if m.get('mostra_logo') is True else ''
        corpo = logo or f'<b>{esc(m["nome"])}</b>'
        cat = f'<span>{esc(m["categoria"])}</span>' if m.get('categoria') else ''
        voci += f'<li class="m-card">{corpo}{cat}</li>'
    return f'''<section class="sec m-sec" id="marchi" aria-labelledby="m-t">
  <div class="sec-head"><span class="eyebrow">Tecnologie</span><h2 id="m-t">Tecnologie e marchi utilizzati</h2></div>
  <ul class="m-grid">{voci}</ul>
</section>'''


# ---------------------------------------------------------------- pagina Privati
ICO_AREE = {
    'progetto': '<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><rect x="7" y="9" width="34" height="30" rx="4" fill="none" stroke="#8fd0ff" stroke-width="3.4"/><path d="M14 31l7-8 6 5 8-11" fill="none" stroke="#ffd23f" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    'gestione': '<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><circle cx="24" cy="24" r="7" fill="none" stroke="#7fe0b0" stroke-width="3.4"/><path d="M24 6v6M24 36v6M6 24h6M36 24h6M11.3 11.3l4.2 4.2M32.5 32.5l4.2 4.2M36.7 11.3l-4.2 4.2M15.5 32.5l-4.2 4.2" stroke="#7fe0b0" stroke-width="3.4" stroke-linecap="round"/></svg>',
    'sole': '<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><circle cx="24" cy="24" r="8" fill="#ffd23f"/><path d="M24 5v6M24 37v6M5 24h6M37 24h6M10.6 10.6l4.2 4.2M33.2 33.2l4.2 4.2M37.4 10.6l-4.2 4.2M14.8 33.2l-4.2 4.2" stroke="#ffd23f" stroke-width="3" stroke-linecap="round"/></svg>',
    'comfort': '<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><path d="M24 6c6 8 11 13 11 20a11 11 0 0 1-22 0c0-7 5-12 11-20z" fill="#7fe0b0"/><path d="M19 28a5 5 0 0 0 5 5" stroke="#0d2d58" stroke-width="2.4" fill="none" stroke-linecap="round"/></svg>',
    'controllo': '<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><circle cx="21" cy="21" r="12" fill="none" stroke="#8fd0ff" stroke-width="4"/><path d="M30 30l11 11" stroke="#8fd0ff" stroke-width="4" stroke-linecap="round"/><path d="M15 21l4 4 8-8" stroke="#7fe0b0" stroke-width="3.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}


def quicknav(servizi, extra):
    """Chip dei servizi: contengono ESCLUSIVAMENTE i servizi (più «Hai già un impianto?»)."""
    voci = ''.join(f'<li><a href="#{x["id"]}">{esc(x.get("nav") or x["titolo"])}</a></li>' for x in servizi)
    return f'''<section class="qn-wrap" aria-label="Navigazione rapida">
  <nav class="quicknav" aria-label="Vai direttamente al servizio"><span class="qn-t">Vai al servizio</span>
    <ul>{voci}<li class="qn-ex"><a href="#{extra['id']}">{esc(extra.get('nav') or extra['titolo'])}</a></li></ul>
  </nav>
</section>'''


def quicknav_privati():
    return quicknav(D.SERVIZI_PRIVATI, D.IMPIANTO_ESISTENTE)


def sistema_section(S=None):
    S = S or D.SISTEMA_INTEGRATO
    aree = ''
    for a in S['aree']:
        link = ''.join(f'<a href="#{i}">{esc(t)}</a>' for t, i in a['link'])
        if a.get('voci'):
            corpo = '<ul class="sys-voci">' + ''.join(f'<li>{esc(v)}</li>' for v in a['voci']) + '</ul>'
        else:
            corpo = (f'<b class="sys-sub">{esc(a["sotto"])}</b>' if a.get('sotto') else '') + f'<p>{esc(a["concetto"])}</p>'
        aree += f'''    <li class="sys-card">
      <div class="sys-ic">{ICO_AREE[a['icona']]}</div>
      <h3>{esc(a['titolo'])}</h3>
      {corpo}
      <div class="sys-links">{link}</div>
    </li>
'''
    concl = f'\n  <p class="sys-concl">{esc(S["conclusione"])}</p>' if S.get('conclusione') else ''
    return f'''<section class="sec sys" id="sistema" aria-labelledby="sistema-t">
  <div class="sys-head"><span class="eyebrow">{esc(S['eyebrow'])}</span><h2 id="sistema-t">{esc(S['titolo'])}</h2>{('<p>' + esc(S['testo']) + '</p>') if S.get('testo') else ''}</div>
  <ul class="sys-grid">
{aree}  </ul>{concl}
</section>'''


def servizio_privato(s):
    dl = (f'<div><dt>A cosa serve</dt><dd>{esc(s["serve"])}</dd></div>'
          f'<div><dt>Quale esigenza risolve</dt><dd>{esc(s["esigenza"])}</dd></div>'
          f'<div><dt>Nel sistema della casa</dt><dd>{esc(s["sistema"])}</dd></div>')
    pts = ''
    if s.get('punti'):
        pts = '<ul class="svc-pts">' + ''.join(f'<li>{esc(x)}</li>' for x in s['punti']) + '</ul>'
    passi = ''
    if s.get('passi'):
        passi = '<ol class="svc-steps">' + ''.join(f'<li><b>{esc(t)}</b><span>{esc(x)}</span></li>' for t, x in s['passi']) + '</ol>'
    return f'''    <article class="feat svc-block{' main' if s.get('principale') else ''}" id="{s['id']}">
      {vis(s)}
      <div class="svc-text"><span class="tag">{esc(s['tag'])}</span><h3>{esc(s['titolo'])}</h3>
        <dl class="svc-dl">{dl}</dl>{pts}
        <a class="btn btn-primary btn-sm" href="#contatti" data-service="{qa(s['opzione'])}">{D.CTA_PRIMARIA} &rarr;</a></div>
      {passi}
    </article>
'''


def servizi_privati_section():
    blocchi = ''.join(servizio_privato(s) for s in D.SERVIZI_PRIVATI if s['id'] not in ('manutenzione', 'lavaggio', 'termografia'))   # questi tre hanno la sezione dedicata privati_man_sections()
    return f'''<section class="sec privati svc-sec" id="servizi" aria-labelledby="servizi-t">
  <div class="sec-head"><span class="eyebrow">Privati · Residenziale</span><h2 id="servizi-t">I servizi per la tua casa</h2><p>Ogni servizio si inserisce nel sistema energetico dell’abitazione: scegli quello che ti interessa o lascia che costruiamo insieme la combinazione più adatta.</p></div>
  <div class="feat-list">
{blocchi}  </div>
</section>'''


def impianto_esistente_section(p, E=None, cta=True):
    E = E or D.IMPIANTO_ESISTENTE
    voci = ''.join(f'<li>{esc(x)}</li>' for x in E['voci'])
    vi = f'<p class="have-li-t">{esc(E["voci_intro"])}</p>' if E.get('voci_intro') else ''
    bott = (f'''
      <div class="cta"><a class="btn btn-light" href="#contatti" data-service="{qa(E['servizio'])}">{esc(E['cta'])} &rarr;</a>
      <a class="btn btn-wa" href="{qa(wa_url(testo=E['whatsapp']))}" target="_blank" rel="noopener">{WA}{esc(D.CTA_PAGINE.get(p['key'], (0, D.CTA_SECONDARIA))[1])}</a></div>''') if cta else ''
    t2 = f'<p>{esc(E["testo2"])}</p>' if E.get('testo2') else ''
    fr = f'<p class="have-frase">{esc(E["frase"])}</p>' if E.get('frase') else ''
    lista = f'<div class="have-list-w">{vi}<ul class="have-list">{voci}</ul></div>' if vi else f'<ul class="have-list">{voci}</ul>'
    return f'''<section class="sec have" id="{E['id']}" aria-labelledby="have-t">
  <div class="have-in">
    <div class="have-text">
      <span class="eyebrow">{esc(E['eyebrow'])}</span>
      <h2 id="have-t">{esc(E['titolo'])}</h2>
      <p>{esc(E['testo'])}</p>{t2}{fr}{bott}
    </div>
    {lista}
  </div>
</section>'''


# ---------------------------------------------------------------- pagina Pubblica Amministrazione
def _ambiti(lista):
    return '<ul class="pa-ambiti">' + ''.join(f'<li>{esc(x)}</li>' for x in lista) + '</ul>'


def _pa_cta(opzione, luce=False):
    return f'<a class="btn {"btn-light" if luce else "btn-primary"} btn-sm" href="#contatti" data-service="{qa(opzione)}">{esc(D.CTA_PAGINE["pa"][0])} &rarr;</a>'


def _pa_par(s):
    return ''.join(f'<p class="pa-lead">{esc(x)}</p>' for x in s['paragrafi'])


def _pa_frase(s):
    return f'<p class="pa-frase">{esc(s["frase"])}</p>' if s.get('frase') else ''


def pa_area(s):
    nota = f'<p class="pa-nota">{esc(s["nota"])}</p>' if s.get('nota') else ''
    att = ''
    if s.get('punti'):
        att = f'<div class="pa-act"><b>{esc(s["punti_titolo"])}</b>' + _punti(s['punti'], 'svc-pts cols2') + '</div>'
    perc = ''
    if s.get('percorso'):
        perc = ('<div class="pa-path"><b>Il percorso</b><ol>' + ''.join(f'<li>{esc(x)}</li>' for x in s['percorso']) + '</ol></div>')
    sub = ''
    if s.get('sub'):
        u = s['sub']
        sub = f'''
      <div class="pa-sub" id="{u['id']}">
        {vis(u, 'vis')}
        <div class="pa-sub-t"><h4>{esc(u['titolo'])}</h4>{_fv_par(u['paragrafi'])}{_pa_frase(u)}
          <p class="pa-nota">{esc(u['nota'])}</p>{_pa_cta(u['opzione'])}</div>
      </div>'''
    return f'''    <article class="pa-area" id="{s['id']}">
      <div class="pa-main">
        {vis(s)}
        <div class="pa-text"><span class="tag">{esc(s['tag'])}</span><h3>{esc(s['titolo'])}</h3>
          {_pa_par(s)}{_pa_frase(s)}{'' if s.get('punti') else nota}{_pa_cta(s['opzione'])}</div>
      </div>
      {att}{('<div class="pa-act-n">' + nota + '</div>') if s.get('punti') and nota else ''}{perc}{sub}
    </article>
'''


def pa_cer(s):
    nodi = ''.join(f'<li><b>{esc(t)}</b><span>{esc(x)}</span></li>' for t, x in s['schema'])
    return f'''    <article class="pa-cer" id="{s['id']}" aria-labelledby="cer-t">
      <div class="pa-cer-top">
        <div class="pa-cer-text"><span class="tag">{esc(s['tag'])}</span><h3 id="cer-t">{esc(s['titolo'])} <span class="sigla">CER</span></h3>
          {_pa_par(s)}
          <ol class="cer-flow" aria-label="Schema di una configurazione di condivisione dell’energia">{nodi}</ol></div>
        {vis(s, 'vis cer-vis')}
      </div>
      <div class="pa-act"><b>{esc(s['punti_titolo'])}</b>{_punti(s['punti'], 'svc-pts cols2')}</div>
      {_pa_frase(s)}
      <p class="pa-nota">{esc(s['nota'])}</p>
      {_pa_cta(s['opzione'])}
    </article>
'''


def pa_aree_section():
    H = D.PA_AREE_HEAD
    bl = ''.join(pa_cer(s) if s['id'] == 'cer' else pa_area(s) for s in D.SERVIZI_PA_PAGINA)
    return f'''<section class="sec pa-aree" id="aree" aria-labelledby="aree-t">
  <div class="sec-head"><span class="eyebrow">{esc(H['eyebrow'])}</span><h2 id="aree-t">{esc(H['titolo'])}</h2><p>{esc(H['testo'])}</p></div>
  <div class="pa-list-aree">
{bl}  </div>
</section>'''


def pa_intro_section():
    I = D.PA_INTRO
    return f'''<section class="sec fv-sec pa-intro" id="introduzione" aria-labelledby="pai-t">
  <div class="fv-head"><span class="eyebrow">{esc(I['eyebrow'])}</span><h2 id="pai-t">{esc(I['titolo'])}</h2>{_fv_par(I['paragrafi'])}</div>
  <p class="fv-quote">{esc(I['frase'])}</p>
</section>'''


def pa_incentivi_section():
    I = D.INCENTIVI_PA
    col = lambda t, l: f'<div class="inc-col"><h3>{esc(t)}</h3><ul class="svc-pts">' + ''.join(f'<li>{esc(x)}</li>' for x in l) + '</ul></div>'
    return f'''<section class="sec pa-inc" id="incentivi" aria-labelledby="inc-t">
  <div class="inc-in">
    <div class="inc-head"><span class="eyebrow">{esc(I['eyebrow'])}</span><h2 id="inc-t">{esc(I['titolo'])}</h2>{_fv_par(I['paragrafi'])}</div>
    <div class="inc-cols">{col(I['noi_t'], I['noi'])}{col(I['ente_t'], I['ente'])}</div>
    <p class="inc-frase">{esc(I['frase'])}</p>
    <div class="inc-cta"><a class="btn btn-primary" href="#contatti" data-service="{qa(I['servizio'])}">{esc(I['cta'])} &rarr;</a></div>
  </div>
</section>'''


def pa_riepilogo_section():
    R = D.PA_RIEPILOGO
    voci = ''.join(f'<li class="fv-ch"><div class="fv-ic">{ICO_FV[i]}</div><h3>{esc(t)}</h3><p>{esc(x)}</p></li>' for i, t, x in R['voci'])
    return f'''<section class="sec fv-sec fv-cambia pa-riep" id="in-sintesi" aria-labelledby="par-t">
  <div class="fv-head wide"><span class="eyebrow">{esc(R['eyebrow'])}</span><h2 id="par-t">{esc(R['titolo'])}</h2></div>
  <ul class="fv-chs c4">{voci}</ul>
</section>'''


def pa_finale(p):
    F = D.PA_FINALE
    c1, c2 = D.CTA_PAGINE['pa']
    return f'''<section class="sec fv-fin pa-fin" id="{F['id']}" aria-labelledby="paf-t">
  <div class="fv-fin-in">
    <h2 id="paf-t">{esc(F['titolo'])}</h2>
    <p class="fv-fin-q">{esc(F['frase'])}</p>
    <div class="cta"><a class="btn btn-light" href="#contatti" data-service="Riqualificazione energetica edifici pubblici">{esc(c1)} &rarr;</a>
    <a class="btn btn-wa" href="{qa(wa_for('pa'))}" target="_blank" rel="noopener">{WA}{esc(c2)}</a></div>
  </div>
</section>'''


# ---------------------------------------------------------------- pagina Imprese
def _punti(lista, classe='svc-pts'):
    return f'<ul class="{classe}">' + ''.join(f'<li>{esc(x)}</li>' for x in lista) + '</ul>'


def imp_principale(s):
    """Blocco in evidenza (fotovoltaico industriale, utility scale)."""
    extra = ''
    if s.get('destinatari'):
        extra += '<div class="imp-aud"><b>Per chi è</b>' + _punti(s['destinatari'], 'imp-chips') + '</div>'
    if s.get('punti'):
        if s.get('punti_intro'):
            extra += f'<p class="imp-pi">{esc(s["punti_intro"])}</p>'
        extra += _punti(s['punti'], 'svc-pts cols2')
    if s.get('integrazioni'):
        extra += f'<div class="imp-int"><b>{esc(s["integrazioni_titolo"])}</b>' + _punti(s['integrazioni'], 'imp-chips') + '</div>'
    if s.get('frase'):
        extra += f'<p class="imp-frase">{esc(s["frase"])}</p>'
    passi = ''
    if s.get('passi'):
        passi = '<ol class="svc-steps s4">' + ''.join(f'<li><b>{esc(t)}</b><span>{esc(x)}</span></li>' for t, x in s['passi']) + '</ol>'
    return f'''    <article class="feat svc-block main imp-main" id="{s['id']}">
      {vis(s)}
      <div class="svc-text"><span class="tag">{esc(s['tag'])}</span><h3>{esc(s['titolo'])}</h3>
        <p class="imp-lead">{esc(s['testo'])}</p>{extra}
        <a class="btn btn-primary btn-sm" href="#contatti" data-service="{qa(s['opzione'])}">{esc(D.CTA_PAGINE['imprese'][0])} &rarr;</a></div>
      {passi}
    </article>
'''


def imprese_principali_section():
    bl = ''.join(imp_principale(s) for s in D.SERVIZI_IMPRESE if s['livello'] == 'principale')
    return f'''<section class="sec privati svc-sec" id="servizi" aria-labelledby="servizi-t">
  <div class="sec-head"><span class="eyebrow">Imprese · Industriale</span><h2 id="servizi-t">Fotovoltaico per aziende e grandi impianti</h2><p>Dagli impianti per capannoni e attività produttive fino agli impianti a terra di grande potenza: un approccio tecnico, con la stessa attenzione dal progetto alla gestione.</p></div>
  <div class="feat-list">
{bl}  </div>
</section>'''


def om_section():
    s = next(x for x in D.SERVIZI_IMPRESE if x['livello'] == 'om')
    pr, pg = s['proteggere'], s['programmato']
    att = ''.join(f'<li>{esc(x)}</li>' for x in pg['punti'])
    return f'''<section class="sec om-sec" id="{s['id']}" aria-labelledby="om-t">
  <div class="om-card">
    <div class="om-top">
      <div class="om-text">
        <span class="tag">{esc(s['tag'])}</span>
        <h2 id="om-t">{esc(s['titolo'])}</h2>
        <p class="om-sub">{esc(s['sottotitolo'])}</p>
        {_fv_par(s['paragrafi'])}
        <p class="om-key">{esc(s['frase'])}</p>
        <p class="om-mod">{esc(s['aggiunta'])}</p>
        <a class="btn btn-light" href="#contatti" data-service="{qa(s['opzione'])}">{esc(D.CTA_PAGINE['imprese'][0])} &rarr;</a>
      </div>
      {vis(s, 'vis om-vis')}
    </div>
    <div class="om-prot">
      <h3>{esc(pr['titolo'])}</h3>
      <div class="om-prot-t">{_fv_par(pr['paragrafi'])}</div>
      <p class="om-strong">{esc(pr['frase'])}</p>
    </div>
    <h3 class="om-h3">{esc(pg['titolo'])}</h3>
    <p class="om-lead">{esc(pg['testo'])}</p>
    <h4 class="om-h">{esc(pg['intro'])}</h4>
    <ul class="om-grid">{att}</ul>
    <p class="om-mod om-nota">{esc(pg['nota'])}</p>
    <p class="om-veg">{esc(pg['vegetazione'])}</p>
  </div>
</section>'''


def imp_card(s):
    punti = _punti(s['punti']) if s.get('punti') else ''
    nota = f'<p class="imp-nota">{esc(s["nota"])}</p>' if s.get('nota') else ''
    testo = s['testo'] if isinstance(s['testo'], list) else [s['testo']]
    forte = f'<p class="imp-forte">{esc(s["forte"])}</p>' if s.get('forte') else ''
    return f'''    <article class="imp-card" id="{s['id']}">
      {vis(s)}
      <div class="imp-body"><span class="tag">{esc(s['tag'])}</span><h3>{esc(s.get('titolo_sez', s['titolo']))}</h3>
        {_fv_par(testo)}{punti}{forte}{nota}
        <a class="btn btn-primary btn-sm" href="#contatti" data-service="{qa(s['opzione'])}">{esc(D.CTA_PAGINE['imprese'][0])} &rarr;</a></div>
    </article>
'''


def imprese_specialistici_section():
    cards = ''.join(imp_card(s) for s in D.SERVIZI_IMPRESE if s['livello'] == 'standard')
    return f'''<section class="sec imp-spec" id="specialistici" aria-labelledby="spec-t">
  <div class="sec-head"><span class="eyebrow">Servizi specialistici</span><h2 id="spec-t">Controllo, progetti e strategie energetiche</h2><p>Attività specialistiche per gli impianti esistenti e interventi per le imprese che vogliono rivedere il proprio sistema energetico.</p></div>
  <div class="imp-grid">
{cards}  </div>
</section>'''


# ---------------------------------------------------------------- pagina Privati: perché il fotovoltaico
ICO_FV = {
    'sole': ICO_AREE['sole'],
    'spina': '<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><path d="M8 23L24 9l16 14" fill="none" stroke="#1f6fd1" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/><path d="M13 21v18h22V21" fill="none" stroke="#1f6fd1" stroke-width="3.4" stroke-linejoin="round"/><path d="M26 26l-5 7h6l-5 7" fill="none" stroke="#ffc83d" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    'batteria': '<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><rect x="6" y="14" width="32" height="20" rx="4" fill="none" stroke="#1f6fd1" stroke-width="3.4"/><path d="M42 21v6" stroke="#1f6fd1" stroke-width="3.4" stroke-linecap="round"/><path d="M13 20v8M19 20v8M25 20v8" stroke="#23a36a" stroke-width="3.4" stroke-linecap="round"/></svg>',
    'giu': '<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><path d="M8 14l12 12 8-8 12 12" fill="none" stroke="#23a36a" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M30 30h10V20" fill="none" stroke="#23a36a" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    'ingranaggio': '<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><circle cx="24" cy="24" r="7" fill="none" stroke="#1f6fd1" stroke-width="3.4"/><path d="M24 6v6M24 36v6M6 24h6M36 24h6M11.3 11.3l4.2 4.2M32.5 32.5l4.2 4.2M36.7 11.3l-4.2 4.2M15.5 32.5l-4.2 4.2" stroke="#23a36a" stroke-width="3.4" stroke-linecap="round"/></svg>',
    'lente': '<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><circle cx="21" cy="21" r="12" fill="none" stroke="#1f6fd1" stroke-width="3.6"/><path d="M30 30l11 11" stroke="#1f6fd1" stroke-width="3.8" stroke-linecap="round"/><path d="M15 21l4 4 8-8" stroke="#23a36a" stroke-width="3.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    'progetto': '<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><rect x="7" y="9" width="34" height="30" rx="4" fill="none" stroke="#1f6fd1" stroke-width="3.4"/><path d="M14 31l7-8 6 5 8-11" fill="none" stroke="#ffc83d" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    'casa': '<svg viewBox="0 0 48 48" aria-hidden="true" focusable="false"><path d="M6 23L24 8l18 15" fill="none" stroke="#1f6fd1" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/><path d="M11 21v19h26V21" fill="none" stroke="#1f6fd1" stroke-width="3.4" stroke-linejoin="round"/><path d="M24 27l2.2 4.4 4.8.7-3.5 3.4.8 4.8-4.3-2.3-4.3 2.3.8-4.8-3.5-3.4 4.8-.7z" fill="#ffc83d"/></svg>',
}


def _fv_par(lista):
    return ''.join(f'<p>{esc(x)}</p>' for x in lista)


def _fv_link(l):
    return f'<a class="fv-link" href="{qa(l[1])}">{esc(l[0])} &rarr;</a>' if l else ''


def privati_fv_sections():
    F = D.PRIVATI_FV
    P_ = F['perche']
    carte = ''.join(
        f'<li class="fv-card"><h3>{esc(c["titolo"])}</h3>{_fv_par(c["paragrafi"])}'
        + (f'<p class="fv-strong">{esc(c["forte"])}</p>' if c.get('forte') else '') + '</li>' for c in P_['carte'])
    s1 = f'''<section class="sec fv-sec fv-perche" id="perche-fotovoltaico" aria-labelledby="fvp-t">
  <div class="fv-head"><span class="eyebrow">{esc(P_['eyebrow'])}</span><h2 id="fvp-t">{esc(P_['titolo'])}</h2>{_fv_par(P_['paragrafi'])}</div>
  <p class="fv-quote">{esc(P_['frase'])}</p>
  <ul class="fv-cards c3">{carte}</ul>
</section>'''
    A = F['accumulo']
    passi = ''.join(f'<li class="fv-flow-i"><b>{esc(t)}</b><span>{esc(x)}</span></li>' for t, x in A['passi'])
    s2 = f'''<section class="sec fv-sec fv-acc" id="{A['id']}" aria-labelledby="fva-t">
  <div class="fv-head"><span class="eyebrow">{esc(A['eyebrow'])}</span><h2 id="fva-t">{esc(A['titolo'])}</h2>{_fv_par(A['paragrafi'])}</div>
  <ol class="fv-flow">{passi}</ol>
  <p class="fv-concl">{esc(A['conclusione'])}</p>
  <p class="fv-nota">{esc(A['nota'])}</p>
  <p class="fv-more">{_fv_link(A['link'])}</p>
</section>'''
    Cm = F['cambia']
    voci = ''.join(f'<li class="fv-ch"><div class="fv-ic">{ICO_FV[i]}</div><h3>{esc(t)}</h3><p>{esc(x)}</p></li>' for i, t, x in Cm['voci'])
    s3 = f'''<section class="sec fv-sec fv-cambia" id="cosa-cambia" aria-labelledby="fvc-t">
  <div class="fv-head wide"><span class="eyebrow">{esc(Cm['eyebrow'])}</span><h2 id="fvc-t">{esc(Cm['titolo'])}</h2></div>
  <ul class="fv-chs">{voci}</ul>
</section>'''
    T = F['tempo']
    tc = ''.join(f'<li class="fv-card"><h3>{esc(c["titolo"])}</h3>{_fv_par(c["paragrafi"])}{_fv_link(c.get("link"))}</li>' for c in T['carte'])
    s4 = f'''<section class="sec fv-sec fv-tempo" id="valore-nel-tempo" aria-labelledby="fvt-t">
  <div class="fv-head wide"><span class="eyebrow">{esc(T['eyebrow'])}</span><h2 id="fvt-t">{esc(T['titolo'])}</h2></div>
  <ul class="fv-cards c3">{tc}</ul>
</section>'''
    Fi = F['finale']
    s5 = f'''<section class="sec fv-fin" id="fotovoltaico-scelta" aria-labelledby="fvf-t">
  <div class="fv-fin-in">
    <h2 id="fvf-t">{esc(Fi['titolo'])}</h2>
    <p class="fv-fin-q">{esc(Fi['frase'])}</p>
    <div class="cta"><a class="btn btn-light" href="#contatti" data-service="{qa(Fi['servizio'])}">{esc(Fi['cta'])} &rarr;</a>
    <a class="btn btn-wa" href="{qa(wa_for('privati_fv'))}" target="_blank" rel="noopener">{WA}{esc(D.CTA_SECONDARIA)}</a></div>
  </div>
</section>'''
    return '\n'.join([s1, s2, s3, s4, s5])


# ---------------------------------------------------------------- pagina Privati: manutenzione fotovoltaico
def _man_par(l):
    return ''.join(f'<p>{esc(x)}</p>' for x in l)


def _man_ul(l):
    return '<ul class="man-list">' + ''.join(f'<li>{esc(x)}</li>' for x in l) + '</ul>'


def privati_man_sections():
    M = D.PRIVATI_MAN
    a = M['intro']
    s1 = f'''<section class="sec man-sec man-intro" id="manutenzione" aria-labelledby="man-t">
  <div class="fv-head"><span class="eyebrow">{esc(a['eyebrow'])}</span><h2 id="man-t">{esc(a['titolo'])}</h2>{_man_par(a['paragrafi'])}</div>
  <p class="fv-quote">{esc(a['frase'])}</p>
</section>'''
    b = M['perche']
    s2 = f'''<section class="sec man-sec man-alt" id="{b['id']}" aria-labelledby="man-b-t">
  <div class="man-2">
    <div class="man-col"><h2 id="man-b-t">{esc(b['titolo'])}</h2>{_man_par(b['paragrafi'])}</div>
    <div class="man-principio"><span class="eyebrow">{esc(b['principio'])}</span><p class="man-big">{esc(b['frase'])}</p><p>{esc(b['chiusura'])}</p></div>
  </div>
</section>'''
    c_ = M['aspettare']
    s3 = f'''<section class="sec man-sec" id="{c_['id']}" aria-labelledby="man-c-t">
  <div class="man-2">
    <div class="man-col"><h2 id="man-c-t">{esc(c_['titolo'])}</h2>{_man_par(c_['intro'])}{_man_ul(c_['voci'])}</div>
    <div class="man-col"><p>{esc(c_['chiusura'])}</p><p class="fv-strong man-strong">{esc(c_['frase'])}</p></div>
  </div>
</section>'''
    d_ = M['controlli']
    cards = ''.join(f'<li class="fv-card"><h3>{esc(t)}</h3><p>{esc(x)}</p></li>' for t, x in d_['voci'])
    s4 = f'''<section class="sec man-sec man-alt" id="{d_['id']}" aria-labelledby="man-d-t">
  <div class="fv-head wide"><h2 id="man-d-t">{esc(d_['titolo'])}</h2><p>{esc(d_['intro'])}</p></div>
  <ul class="fv-cards c3">{cards}</ul>
</section>'''
    e = M['lavaggio']
    s5 = f'''<section class="sec man-sec" id="{e['id']}" aria-labelledby="man-e-t">
  <div class="man-2">
    <div class="man-col"><span class="eyebrow">{esc(e['eyebrow'])}</span><h2 id="man-e-t">{esc(e['titolo'])}</h2>{_man_par(e['paragrafi'][:2])}</div>
    <div class="man-col">{_man_par(e['paragrafi'][2:])}<p class="fv-strong man-strong">{esc(e['frase'])}</p><p class="man-cta"><a class="btn btn-primary btn-sm" href="#contatti" data-service="{qa('Lavaggio moduli fotovoltaici')}">{esc(D.IMPIANTO_ESISTENTE['cta'])} &rarr;</a></p></div>
  </div>
</section>'''
    f = M['termografia']
    s6 = f'''<section class="sec man-sec man-alt" id="{f['id']}" aria-labelledby="man-f-t">
  <div class="man-2">
    <div class="man-col"><span class="eyebrow">{esc(f['eyebrow'])}</span><h2 id="man-f-t">{esc(f['titolo'])}</h2>{_man_par(f['paragrafi'])}{_man_ul(f['voci'])}</div>
    <div class="man-col"><p>{esc(f['chiusura'])}</p><p class="man-cta"><a class="btn btn-primary btn-sm" href="#contatti" data-service="{qa('Termografia impianti fotovoltaici')}">{esc(D.IMPIANTO_ESISTENTE['cta'])} &rarr;</a></p></div>
  </div>
</section>'''
    g = M['investimento']
    s7 = f'''<section class="sec man-sec" id="{g['id']}" aria-labelledby="man-g-t">
  <div class="man-2">
    <div class="man-col"><h2 id="man-g-t">{esc(g['titolo'])}</h2>{_man_par(g['paragrafi'])}<p class="fv-strong man-strong">{esc(g['frase'])}</p></div>
    <div class="man-col"><p>{esc(g['intro_voci'])}</p>{_man_ul(g['voci'])}</div>
  </div>
</section>'''
    return '\n'.join([s1, s2, s3, s4, s5, s6, s7])


def privati_man_finale(p):
    F = D.PRIVATI_MAN['finale']
    E = D.IMPIANTO_ESISTENTE
    return f'''<section class="sec fv-fin" id="{F['id']}" aria-labelledby="man-fin-t">
  <div class="fv-fin-in">
    <h2 id="man-fin-t">{esc(F['titolo'])}</h2>
    {_man_par(F['paragrafi'])}
    <p class="fv-fin-q">{esc(F['frase'])}</p>
    <div class="cta"><a class="btn btn-light" href="#contatti" data-service="{qa(E['servizio'])}">{esc(E['cta'])} &rarr;</a>
    <a class="btn btn-wa" href="{qa(wa_url(testo=E['whatsapp']))}" target="_blank" rel="noopener">{WA}{esc(D.CTA_SECONDARIA)}</a></div>
  </div>
</section>'''


# ---------------------------------------------------------------- pagina Imprese: perché produrre energia
def imprese_fv_sections():
    F = D.IMPRESE_FV
    P_ = F['perche']
    carte = ''.join(
        f'<li class="fv-card"><h3>{esc(x["titolo"])}</h3>{_fv_par(x["paragrafi"])}'
        + (f'<p class="fv-strong">{esc(x["forte"])}</p>' if x.get('forte') else '') + '</li>' for x in P_['carte'])
    s1 = f'''<section class="sec fv-sec fv-perche" id="perche-energia" aria-labelledby="ifp-t">
  <div class="fv-head"><span class="eyebrow">{esc(P_['eyebrow'])}</span><h2 id="ifp-t">{esc(P_['titolo'])}</h2>{_fv_par(P_['paragrafi'])}</div>
  <p class="fv-quote">{esc(P_['frase'])}</p>
  <ul class="fv-cards c3">{carte}</ul>
</section>'''
    A = F['accumulo']
    s2 = f'''<section class="sec man-sec man-alt" id="{A['id']}" aria-labelledby="ifa-t">
  <div class="man-2">
    <div class="man-col"><span class="eyebrow">{esc(A['eyebrow'])}</span><h2 id="ifa-t">{esc(A['titolo'])}</h2>{_fv_par(A['paragrafi'])}</div>
    <div class="man-col"><p class="fv-strong man-strong">{esc(A['intro'])}</p>{_man_ul(A['voci'])}</div>
  </div>
</section>'''
    Cm = F['cambia']
    voci = ''.join(f'<li class="fv-ch"><div class="fv-ic">{ICO_FV[i]}</div><h3>{esc(t)}</h3><p>{esc(x)}</p></li>' for i, t, x in Cm['voci'])
    s3 = f'''<section class="sec fv-sec fv-cambia" id="cosa-cambia-impresa" aria-labelledby="ifc-t">
  <div class="fv-head wide"><span class="eyebrow">{esc(Cm['eyebrow'])}</span><h2 id="ifc-t">{esc(Cm['titolo'])}</h2></div>
  <ul class="fv-chs">{voci}</ul>
</section>'''
    return '\n'.join([s1, s2, s3])


def imprese_revamping_section():
    R = D.IMPRESE_FV['revamping']
    return f'''<section class="sec man-sec man-alt" id="{R['id']}" aria-labelledby="rev-t">
  <div class="man-2">
    <div class="man-col"><span class="eyebrow">{esc(R['eyebrow'])}</span><h2 id="rev-t">{esc(R['titolo'])}</h2></div>
    <div class="man-col">{_fv_par(R['paragrafi'])}</div>
  </div>
</section>'''


def imprese_finale(p):
    F = D.IMPRESE_FV['finale']
    c1, c2 = D.CTA_PAGINE['imprese']
    return f'''<section class="sec fv-fin fv-fin-imp" id="{F['id']}" aria-labelledby="imf-t">
  <div class="fv-fin-in">
    <h2 id="imf-t">{esc(F['titolo'])}</h2>
    <p class="fv-fin-q big">{esc(F['frase'])}</p>
    <div class="cta"><a class="btn btn-light" href="#contatti" data-service="Fotovoltaico industriale">{esc(c1)} &rarr;</a>
    <a class="btn btn-wa" href="{qa(wa_for('imprese'))}" target="_blank" rel="noopener">{WA}{esc(c2)}</a></div>
  </div>
</section>'''
