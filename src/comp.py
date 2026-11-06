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
    pre = '' if root_rel else '/'         # la 404 usa percorsi dalla radice
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
        serv += f'<div class="dropdown-category"><span class="category-title">{esc(col["titolo"])}</span>{voci}</div>'
    bon = ''
    for col in D.INCENTIVI['menu']:
        voci = ''.join(f'<a href="{H("incentivi")}" data-modal="{col["modale"]}">{esc(v)}</a>' for v in col['voci'])
        bon += f'<div class="dropdown-category"><a class="category-title" href="{H("incentivi")}" data-modal="{col["modale"]}">{esc(col["titolo"])}</a>{voci}</div>'

    home_cls = ' class="active"' if home else ''
    home_href = '#home' if home else pre + 'index.html'
    serv_cls = ' active' if p['key'] in ('privati', 'imprese', 'pa') else ''
    items = [
        f'<a href="{home_href}" data-spy="home"{home_cls}>Home</a>',
        f'<div class="dropdown"><a class="dd-trigger{serv_cls}" href="javascript:void(0);" aria-haspopup="true" aria-expanded="false" data-spy="servizi">Servizi &#9662;</a><div class="dropdown-menu dropdown-3-col">{serv}</div></div>',
    ]
    items += [
        f'<div class="dropdown"><a class="dd-trigger" href="{H("incentivi")}" aria-haspopup="true" aria-expanded="false" data-spy="incentivi">Bonus &amp; Incentivi &#9662;</a><div class="dropdown-menu dropdown-3-col">{bon}</div></div>',
        f'<a href="{pre}index.html#informazioni" data-spy="informazioni">Chi siamo</a>',
        f'<a href="{pre}lavora-con-noi.html">Lavora con noi</a>',
        f'<a class="nav-offerte{" active" if p["key"] == "offerte" else ""}" href="{pre}offerte.html" data-spy="offerte"{cur("offerte")}>Offerte</a>',
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
    s = D.SOCIETA
    home = p['key'] == 'home'
    H = (lambda a: f'#{a}') if home else (lambda a: f'{pre}index.html#{a}')
    phones = ''.join(
        f'<div class="fphone"><b>{n}{PRINC if n == D.TELEFONO_PRINCIPALE else ""}</b><div class="acts"><a href="{tel_url(n)}" aria-label="Chiama {n}">{PH}Chiama</a>'
        f'<a class="w" href="{qa(wa_url(n))}" target="_blank" rel="noopener" aria-label="WhatsApp {n}">{WA}WhatsApp</a></div></div>'
        for n in D.TELEFONI)
    nav_links = [('Privati', f'{pre}privati.html'), ('Imprese', f'{pre}imprese.html'), ('Pubblica Amministrazione', f'{pre}pubblica-amministrazione.html')]
    if ha_realizzazioni():
        nav_links.append(('Realizzazioni', f'{pre}realizzazioni.html'))
    nav_links += [('Offerte', f'{pre}offerte.html'), ('Bonus &amp; Incentivi', H('incentivi')), ('Chi siamo', H('informazioni')), ('Lavora con noi', f'{pre}lavora-con-noi.html'),
                  ('Contatti', f'{pre}contatti.html'), ('Cosa dicono di noi', H('recensioni'))]
    links = ''.join(f'<a href="{h}"{" data-rev hidden" if h.endswith("#recensioni") else ""}>{l}</a>' for l, h in nav_links)
    logo = f'{pre}{D.SITO["logo_chiaro"]}'
    return f'''<footer>
  <div class="foot-grid">
    <div>
      <a href="{'#home' if home else pre + 'index.html'}" class="brand" aria-label="{qa(D.SITO['nome_esteso'])}">
        <img src="{logo}" alt="{qa(D.SITO['nome_esteso'].replace('—', '–'))}" loading="lazy" onerror="this.parentNode.classList.add('nologo')">
        <span class="brand-fallback"><b>RIVETTI <em>IMPIANTI</em></b><small>TECHNICAL ENGINEERING</small></span>
      </a>
      <p>{esc(D.SITO['slogan'])}.<br>Al servizio di Privati, Aziende e Pubbliche Amministrazioni.</p>
    </div>
    <div>
      <h2>Azienda</h2>
      <p>{esc(s['ragione_sociale'])}<br>{esc(D.SITO['nome_esteso'])}</p>
      <p>{esc(indirizzo())}</p>
      <p>P.IVA / C.F. {s['piva_cf']} · REA {s['rea']}</p>
      <a href="mailto:{s['email']}">{s['email']}</a>
      <a href="mailto:{s['pec']}">PEC: {s['pec']}</a>
    </div>
    <div>
      <h2>Telefono &amp; WhatsApp</h2>
      {phones}
    </div>
    <div>
      <h2>Navigazione</h2>
      {links}
    </div>
  </div>
  <div class="copy">
    <span>© <span id="y">{ANNO}</span> Rivetti Impianti — {esc(s['ragione_sociale_breve'])} · P. IVA/C.F. {s['piva_cf']} · REA {s['rea']} — Tutti i diritti riservati</span>
    <span class="legal"><a href="{pre}privacy.html">Privacy Policy</a> · <a href="{pre}cookie.html">Cookie Policy</a> · <a href="{pre}note-legali.html">Note legali</a></span>
  </div>
</footer>
'''


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
        voci = ''.join(f'     <div class="opp"><b>{t}<i>{tag}</i></b><p>{x}</p></div>\n' for t, tag, x in s['voci'])
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