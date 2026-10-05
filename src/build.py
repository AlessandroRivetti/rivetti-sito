# -*- coding: utf-8 -*-
"""
Genera il sito: index, privati, imprese, pubblica-amministrazione, contatti, (realizzazioni), 404, sitemap.xml, robots.txt.

    python3 src/build.py            # genera i file definitivi nella cartella del sito
    python3 src/build.py --demo     # anteprima di Realizzazioni con dati FITTIZI (da dev/, se presente) in _demo/ (NON da pubblicare)

I contenuti si modificano in src/dati.py; il codice delle pagine è in src/comp.py e in questo file.
Ogni build esegue anche i controlli automatici (link, titoli, H1, SVG, TODO): se qualcosa non va, si ferma.
"""
import math
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dati as D
import gallerie as G
import progetti as P
import comp as C
from art import ART, DEFS

ROOT = C.ROOT
esc, qa = C.esc, C.qa

# ----------------------------------------------------------------------------- pagine: metadati SEO
PAGINE = {
    'home': dict(path='/', file='index.html',
                 title='Impianti Fotovoltaici e Termoidraulici | Rivetti Impianti',
                 desc='Dal 2008 progettiamo, realizziamo e manteniamo impianti fotovoltaici, termoidraulici e sistemi energetici per privati, imprese ed enti pubblici.'),
    'privati': dict(path='/privati.html', file='privati.html', crumbs=[('Privati', '/privati.html')],
                    title='Fotovoltaico e Climatizzazione Casa | Rivetti Impianti',
                    desc='Impianti fotovoltaici, sistemi di accumulo, climatizzazione e solare termico per la casa, con manutenzione, lavaggio moduli e termografia per impianti fotovoltaici.'),
    'imprese': dict(path='/imprese.html', file='imprese.html', crumbs=[('Imprese', '/imprese.html')],
                    title='Fotovoltaico Industriale e O&M | Rivetti Impianti',
                    desc='Fotovoltaico industriale e Utility Scale, O&M e manutenzione, termografia, lavaggio moduli, agrivoltaico e CER per aziende e operatori del settore fotovoltaico.'),
    'pa': dict(path='/pubblica-amministrazione.html', file='pubblica-amministrazione.html', crumbs=[('Pubblica Amministrazione', '/pubblica-amministrazione.html')],
               title='Energia per la Pubblica Amministrazione | Rivetti Impianti',
               desc='Riqualificazione energetica di edifici pubblici, fotovoltaico, Comunità Energetiche e manutenzione degli impianti: supporto tecnico per Enti e Pubblica Amministrazione.'),
    'realizzazioni': dict(path='/realizzazioni.html', file='realizzazioni.html', crumbs=[('Realizzazioni', '/realizzazioni.html')],
                          title='Realizzazioni | Rivetti Impianti',
                          desc='I lavori realizzati da Rivetti Impianti per privati, imprese e Pubblica Amministrazione: impianti fotovoltaici, termoidraulici e manutenzione.'),
    'contatti': dict(path='/contatti.html', file='contatti.html', crumbs=[('Contatti', '/contatti.html')],
                     title='Contatti e Richiesta di Sopralluogo | Rivetti Impianti',
                     desc='Contatta Rivetti Impianti: telefono, WhatsApp, email e modulo per richiedere un sopralluogo o un preventivo.'),
    '404': dict(path='/404.html', file='404.html', title='Pagina non trovata | Rivetti Impianti',
                desc='La pagina richiesta non esiste o è stata spostata.', noindex=True),
}
LEGALI = ['privacy.html', 'cookie.html', 'note-legali.html']          # generate da legal.py
ALTRE = {'recensione.html'}                                            # pagina a parte (noindex)


def pagina(key):
    p = dict(PAGINE[key], key=key)
    schema = []
    if key == 'home':
        schema = [C.schema_azienda()]
    elif key == 'contatti':
        schema = [C.schema_azienda(), C.schema_briciole(p)]
    elif key in ('privati', 'imprese', 'pa'):
        schema = [C.schema_briciole(p), C.schema_faq(key)]
    elif 'crumbs' in p:
        schema = [C.schema_briciole(p)]
    p['schema'] = schema
    return p


def doc(p, body, dialoghi=True, pre='', scripts=('ri.js', 'site.js')):
    root_rel = (pre == '')
    sc = ''.join(f'<script src="{pre}{s}" defer></script>\n' for s in scripts)
    return (C.head(p, root_rel=root_rel) +
            f'<body data-page="{p["key"]}">\n{DEFS}\n{C.SPRITE}\n' + C.nav(p, pre) +
            f'<main id="main">\n{body}\n</main>\n' + (C.incentivi_dialogs() if dialoghi else '') +
            C.footer(p, pre) + sc + '</body>\n</html>\n')


# ----------------------------------------------------------------------------- globo: fallback statico
def globe_static():
    """Globo illustrato leggero (SVG inline, nessuna richiesta di rete): resta se il 3D non parte (movimento ridotto,
    connessione lenta, dispositivo debole) e fa da primo fotogramma mentre il 3D si carica."""
    r, cx, cy = 168, 200, 200
    mer = ''.join(f'<ellipse cx="{cx}" cy="{cy}" rx="{r * math.sin(math.radians(a)):.1f}" ry="{r}"/>' for a in (30, 60))
    mer += f'<line x1="{cx}" y1="{cy - r}" x2="{cx}" y2="{cy + r}"/>'
    par = ''.join(f'<line x1="{cx - r}" x2="{cx + r}" y1="{cy - r * math.sin(math.radians(a)):.1f}" y2="{cy - r * math.sin(math.radians(a)):.1f}"/>'
                  for a in (-60, -30, 0, 30, 60))
    hq = (222, 150)
    pts = [(120, 120), (95, 215), (270, 110), (292, 205), (168, 262), (250, 270), (140, 175)]
    arcs = ''.join(
        f'<path d="M{hq[0]} {hq[1]} Q{(hq[0] + x) / 2 + 10:.0f} {min(hq[1], y) - 38:.0f} {x} {y}" stroke="url(#gsA)" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
        for x, y in pts)
    dots = ''.join(f'<circle cx="{x}" cy="{y}" r="5" fill="#66c2ff"/><circle cx="{x}" cy="{y}" r="9" fill="#66c2ff" opacity=".25"/>' for x, y in pts)
    return f'''<svg viewBox="0 0 400 400" role="img" aria-label="Illustrazione di un globo terrestre con flussi di energia; il punto luminoso indica la sede di Rivetti Impianti" focusable="false">
<defs>
<radialGradient id="gsS" cx=".36" cy=".32" r=".85"><stop offset="0" stop-color="#9ad4ff"/><stop offset=".55" stop-color="#2a7bd0"/><stop offset="1" stop-color="#0d3a7a"/></radialGradient>
<radialGradient id="gsG" cx=".5" cy=".5" r=".5"><stop offset=".86" stop-color="#5cc8ff" stop-opacity="0"/><stop offset="1" stop-color="#5cc8ff" stop-opacity=".5"/></radialGradient>
<linearGradient id="gsA" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffd23f"/><stop offset="1" stop-color="#3b9dff"/></linearGradient>
<radialGradient id="gsH"><stop offset="0" stop-color="#fff6b0"/><stop offset=".45" stop-color="#ffd23f"/><stop offset="1" stop-color="#ffd23f" stop-opacity="0"/></radialGradient>
<clipPath id="gsC"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>
</defs>
<circle cx="{cx}" cy="{cy}" r="{r + 24}" fill="url(#gsG)"/>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#gsS)"/>
<g clip-path="url(#gsC)" stroke="#fff" stroke-opacity=".22" stroke-width="1" fill="none">{mer}{par}</g>
<g clip-path="url(#gsC)">{arcs}{dots}</g>
<circle cx="{hq[0]}" cy="{hq[1]}" r="22" fill="url(#gsH)"/><circle cx="{hq[0]}" cy="{hq[1]}" r="6.5" fill="#fff"/>
</svg>'''


# ----------------------------------------------------------------------------- HOME
def home():
    p = pagina('home')
    hero = f'''<section class="hero" id="home">
  <div id="globe" class="globe">
    <div class="globe-static">{globe_static()}</div>
  </div>
  <div class="legend" aria-hidden="true">
    <small>Trascina per ruotare</small>
    <span>Flussi di energia <i class="ln"></i></span>
  </div>
  <div class="hero-content">
    <div class="badge"><i aria-hidden="true"></i> Fotovoltaico · Termoidraulica · Manutenzione</div>
    <h1>Impianti fotovoltaici e termoidraulici <span>dal 2008</span></h1>
    <p class="lead">Progettiamo, realizziamo e manteniamo impianti per abitazioni, imprese ed enti pubblici, seguendo ogni intervento dalla valutazione tecnica all&rsquo;assistenza.</p>
    <div class="cta">{C.cta_pair('home')}</div>
  </div>
</section>'''

    intro = f'''<section class="sec intro" id="servizi">
  {C.sec_head('Cosa facciamo', 'Impianti e servizi tecnici per privati, imprese ed enti pubblici', 'Operiamo nel fotovoltaico, nella termoidraulica, nella climatizzazione e nella manutenzione, su nuovi impianti e su sistemi già esistenti. Ogni intervento viene definito in base alle esigenze del cliente e alle caratteristiche tecniche del progetto.')}
  <div class="paths">
    <a class="path p1" href="privati.html"><div><b>Privati</b><span>Fotovoltaico, accumulo, climatizzazione e manutenzione per la casa</span></div><i aria-hidden="true">&rarr;</i></a>
    <a class="path p2" href="imprese.html"><div><b>Imprese</b><span>Fotovoltaico industriale, Utility Scale, O&amp;M e servizi tecnici</span></div><i aria-hidden="true">&rarr;</i></a>
    <a class="path p3" href="pubblica-amministrazione.html"><div><b>Pubblica Amministrazione</b><span>Efficienza energetica, fotovoltaico, Comunità Energetiche e gestione degli impianti</span></div><i aria-hidden="true">&rarr;</i></a>
  </div>
</section>'''

    chips = lambda items, page: '<ul class="chips-l">' + ''.join(f'<li><a href="{page}#{x["id"]}">{esc(x.get("nav") or x["titolo"])}</a></li>' for x in items) + '</ul>'
    band_priv = f'''<section class="sec privati band" id="privati">
  {C.sec_head('Privati · Residenziale', 'Energia e comfort per la casa', 'Fotovoltaico, accumulo, climatizzazione, solare termico e manutenzione per gestire in modo più efficiente l’energia e gli impianti dell’abitazione.')}
  <article class="feat">
    {C.vis(D.SERVIZI_PRIVATI[0], prefer=[D.HERO_FOTO['privati']])}
    <div><span class="tag">I servizi per la casa</span><h3>Dalla produzione di energia alla manutenzione dell’impianto</h3>{chips(D.SERVIZI_PRIVATI, 'privati.html')}
    <a class="btn btn-primary btn-sm" href="privati.html">Scopri le soluzioni per la tua casa &rarr;</a></div>
  </article>
</section>'''
    band_imp = f'''<section class="sec aziende band" id="aziende">
  {C.sec_head('Imprese · Industriale', 'Impianti e servizi tecnici per le imprese', 'Fotovoltaico industriale, grandi impianti e servizi O&amp;M per aziende, strutture produttive e operatori del settore.')}
  <article class="feat">
    {C.vis(D.SERVIZI_IMPRESE[0], prefer=[D.HERO_FOTO['imprese']])}
    <div><span class="tag">I servizi per le imprese</span><h3>Progettazione, realizzazione e gestione di impianti industriali e di grande potenza</h3>{chips(D.SERVIZI_IMPRESE, 'imprese.html')}
    <a class="btn btn-primary btn-sm" href="imprese.html">Scopri le soluzioni per la tua impresa &rarr;</a></div>
  </article>
</section>'''
    pa = D.SERVIZI_PA
    chips_pa = '<ul class="chips-l">' + ''.join(f'<li><a href="pubblica-amministrazione.html#{x["id"]}">{esc(x.get("nav") or x["titolo"])}</a></li>' for x in D.SERVIZI_PA_PAGINA + [D.IMPIANTO_ESISTENTE_PA]) + '</ul>'
    band_pa = f'''<section class="sec pa band" id="pa">
  {C.sec_head('Pubblica Amministrazione', 'Soluzioni energetiche per enti e strutture pubbliche', 'Riqualificazione energetica, fotovoltaico, Comunità Energetiche e manutenzione degli impianti, con un supporto tecnico definito sulle esigenze dell’intervento.')}
  <article class="feat">
    {C.vis(pa, prefer=[D.HERO_FOTO['pa']])}
    <div><span class="tag">{esc(pa['tag'])}</span><h3>Efficienza energetica, fotovoltaico e gestione degli impianti pubblici</h3>{chips_pa}<p class="band-note">In funzione dell’intervento possono essere valutati anche incentivi, contributi e strumenti di finanziamento applicabili.</p>
    <a class="btn btn-primary btn-sm" href="pubblica-amministrazione.html">Scopri le soluzioni per la Pubblica Amministrazione &rarr;</a></div>
  </article>
</section>'''

    about = f'''<section class="sec about" id="informazioni">
  <div class="sec-head">
    <span class="eyebrow">Chi siamo</span>
    <h2>Dal 2008 lavoriamo su impianti energetici per privati, imprese ed enti pubblici</h2>
  </div>
  <div class="about-wrap">
    <div class="about-text">
      <p>Rivetti Impianti nasce nel 2008 per iniziativa di <strong>{D.SOCIETA['fondatore']}</strong>. Nel tempo l’attività si è sviluppata nel fotovoltaico, nella termoidraulica e nei servizi di manutenzione, seguendo interventi di diversa tipologia e dimensione.</p>
      <p>Il lavoro viene seguito da un team tecnico che coordina le fasi di valutazione, progettazione, realizzazione e manutenzione, coinvolgendo quando necessario imprese partner per le attività complementari.</p>
      <p class="motto">Competenza tecnica, continuità del servizio e attenzione alla sicurezza.</p>
    </div>
    <div class="facts">
      <div class="fact"><span>Anno di fondazione</span><b>{D.SITO['anno_inizio']}</b></div>
      <div class="fact wide"><span>Competenze</span><b>Fotovoltaico, termoidraulica e manutenzione</b></div>
      <div class="fact wide"><span>Sede</span><b>{esc(C.indirizzo())}</b></div>
      <div class="fact wide"><span>P.IVA</span><b>{D.SOCIETA['piva_cf']}</b></div>
    </div>
  </div>
</section>'''

    lavora = f'''<section class="sec lavora" id="lavora">
  <div class="sec-head">
    <span class="eyebrow">Candidature</span>
    <h2>Lavora con noi</h2>
    <p>Valutiamo candidature di tecnici, installatori e professionisti interessati a collaborare con Rivetti Impianti nei settori fotovoltaico, termoidraulico e impiantistico.</p>
  </div>
  <div class="lav-wrap">
    <div class="lav-profiles">
      <div class="lprof"><div class="ico">{C.ICO_TEC}</div><div><b>Tecnici</b><span>Impiantisti e specialisti di fotovoltaico e termoidraulica</span></div></div>
      <div class="lprof"><div class="ico">{C.ICO_INS}</div><div><b>Installatori</b><span>Squadre e singoli installatori, per cantieri residenziali e industriali</span></div></div>
      <div class="lprof"><div class="ico">{C.ICO_PRO}</div><div><b>Professionisti</b><span>Progettisti, ingegneri, periti e consulenti tecnici</span></div></div>
    </div>
    <div>
      <p class="lav-intro">Se vuoi presentarti, inviaci il tuo curriculum e una breve descrizione delle tue competenze ed esperienze. Ti ricontatteremo qualora il profilo sia in linea con le nostre esigenze.</p>
      <div class="lav-cta">
        <a class="btn btn-primary" id="jobMail" href="mailto:{D.SOCIETA['email']}">Invia la tua candidatura &rarr;</a>
      </div>
      <p class="lav-privacy">Prima di inviare il curriculum consulta l'<a href="privacy.html">Informativa Privacy</a>.</p>
      <p class="lav-mail">Candidature a: <a href="mailto:{D.SOCIETA['email']}">{D.SOCIETA['email']}</a></p>
    </div>
  </div>
</section>'''

    body = '\n\n'.join(x for x in [
        hero, C.stats_section(), intro, band_priv, band_imp, band_pa, C.real_home_section(),
        C.perche_section(), C.come_section(), C.incentivi_section(), about, C.qualifiche_section(), C.marchi_section(), lavora,
        C.reviews_section(), C.faq_section('home', 'Domande frequenti', 'FAQ'),
        C.contact_section(p, 'Parliamo del tuo impianto', 'Descrivici ciò di cui hai bisogno. Puoi chiamarci, scriverci su WhatsApp oppure utilizzare il modulo: raccoglieremo le informazioni necessarie e, quando serve, organizzeremo un sopralluogo.')] if x)
    return p, doc(p, body, scripts=('ri.js', 'recensioni.js', 'site.js', 'globe.js'))


# ----------------------------------------------------------------------------- PRIVATI / IMPRESE / PA
def _j(parti):
    """Unisce i blocchi della pagina saltando quelli vuoti (es. la Galleria lavori quando non è pubblicata)."""
    return '\n'.join(x for x in parti if x)


def privati():
    p = pagina('privati')
    H = D.PRIVATI_HERO
    body = _j([
        C.phero(p, H['h1'], H['lead'], C.hero_visual('fv', 'privati')),
        C.quicknav_privati(),
        C.privati_fv_sections(),
        C.sistema_section(),
        C.servizi_privati_section(),
        C.privati_man_sections(),
        C.impianto_esistente_section(p, cta=False),
        C.privati_man_finale(p),
        C.galleria_section('privati'),
        C.incentivo_singolo('m-priv', 'Bonus e detrazioni per la tua casa'),
        C.come_section(D.COME_LAVORIAMO_PRIVATI),
        C.faq_section('privati', 'Domande frequenti sulle soluzioni per la casa', 'FAQ'),
        C.contact_section(p, 'Richiedi un sopralluogo', tipo='Privato')])
    return p, doc(p, body)


def imprese():
    p = pagina('imprese')
    H = D.IMPRESE_HERO
    body = _j([
        C.phero(p, H['h1'], H['lead'], C.hero_visual('utility', 'imprese'), tags=H['tags']),
        C.quicknav(D.SERVIZI_IMPRESE, D.IMPIANTO_ESISTENTE_IMPRESE),
        C.imprese_fv_sections(),
        C.sistema_section(D.SISTEMA_IMPRESE),
        C.imprese_principali_section(),
        C.om_section(),
        C.imprese_specialistici_section(),
        C.impianto_esistente_section(p, D.IMPIANTO_ESISTENTE_IMPRESE),
        C.imprese_revamping_section(),
        C.imprese_finale(p),
        C.galleria_section('imprese'),
        C.incentivo_singolo('m-imp', 'Bandi e agevolazioni per la tua impresa'),
        C.come_section(D.COME_LAVORIAMO_IMPRESE),
        C.faq_section('imprese', 'Domande frequenti per le imprese', 'FAQ'),
        C.contact_section(p, 'Richiedi una valutazione tecnica', tipo='Impresa')])
    return p, doc(p, body)


def pa():
    p = pagina('pa')
    H = D.PA_HERO
    body = _j([
        C.phero(p, H['h1'], H['lead'], C.hero_visual('pa_hero', 'pa')),
        C.quicknav(D.SERVIZI_PA_PAGINA, D.IMPIANTO_ESISTENTE_PA),
        C.pa_intro_section(),
        C.sistema_section(D.SISTEMA_PA),
        C.pa_aree_section(),
        C.impianto_esistente_section(p, D.IMPIANTO_ESISTENTE_PA),
        C.galleria_section('pa'),
        C.pa_incentivi_section(),
        C.come_section(D.COME_LAVORIAMO_PA),
        C.pa_riepilogo_section(),
        C.pa_finale(p),
        C.faq_section('pa', 'Domande frequenti per la Pubblica Amministrazione', 'FAQ'),
        C.contact_section(p, 'Richiedi un confronto tecnico', tipo='Pubblica Amministrazione')])
    return p, doc(p, body)


def contatti():
    p = pagina('contatti')
    body = '\n'.join([
        C.phero(p, 'Parla con Rivetti Impianti', 'Per privati, imprese e Pubbliche Amministrazioni: scegli come contattarci e un tecnico ti risponderà.'),
        C.contact_section(p)])
    return p, doc(p, body)


def pagina_404():
    p = pagina('404')
    body = f'''<section class="phero"><div class="phero-in"><div class="phero-text">
  <h1>Pagina non trovata</h1>
  <p class="lead">La pagina che cerchi non esiste o è stata spostata. Puoi ripartire da qui:</p>
  <div class="cta"><a class="btn btn-light" href="/index.html">Torna alla Home</a><a class="btn btn-outline-light" href="/contatti.html">Contatti</a></div>
</div></div></section>
<section class="sec intro">
  {C.sec_head('Dove vuoi andare?', 'I nostri percorsi')}
  <div class="paths">
    <a class="path p1" href="/privati.html"><div><b>Privati · Residenziale</b><span>Per la tua casa e il tuo condominio</span></div><i aria-hidden="true">&rarr;</i></a>
    <a class="path p2" href="/imprese.html"><div><b>Imprese · Industriale</b><span>Per capannoni, industrie e grandi impianti</span></div><i aria-hidden="true">&rarr;</i></a>
    <a class="path p3" href="/pubblica-amministrazione.html"><div><b>PA · Pubblica Amministrazione</b><span>Per enti e strutture comunali</span></div><i aria-hidden="true">&rarr;</i></a>
  </div>
</section>'''
    return p, doc(p, body, dialoghi=False, pre='/', scripts=('ri.js', 'site.js'))


# ----------------------------------------------------------------------------- sitemap, robots
def sitemap(percorsi, out):
    base = D.SITO['url'].rstrip('/')
    urls = [base + x for x in percorsi] + [f'{base}/{f}' for f in LEGALI if os.path.exists(os.path.join(out, f))]
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    x += ''.join(f'  <url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n'
    return x


def robots():
    return f"User-agent: *\nAllow: /\n\nSitemap: {D.SITO['url'].rstrip('/')}/sitemap.xml\n"


# ----------------------------------------------------------------------------- controlli automatici
def controlla(out, files):
    errori = []
    titoli, descr = {}, {}
    ids_per_file = {}
    for f in files + LEGALI + sorted(ALTRE):
        path = os.path.join(out, f)
        if os.path.exists(path):
            ids_per_file[f] = set(re.findall(r'\sid="([^"]+)"', open(path, encoding='utf-8').read()))
    for f in files:
        h = open(os.path.join(out, f), encoding='utf-8').read()
        if re.findall(r'\{\{|\}\}', re.sub(r'<script type="application/ld\+json">.*?</script>', '', h, flags=re.S)):
            errori.append(f'{f}: segnaposto non sostituito')
        if re.search(r'\bTODO\b|DA COMPLETARE|DA CONFERMARE|lorem ipsum', h):
            errori.append(f'{f}: testo provvisorio visibile (TODO/lorem)')
        if len(re.findall(r'<h1[\s>]', h)) != 1:
            errori.append(f'{f}: deve avere esattamente un H1')
        t = re.search(r'<title>(.*?)</title>', h, re.S).group(1)
        d = re.search(r'<meta name="description" content="(.*?)">', h).group(1)
        if t in titoli:
            errori.append(f'{f}: title duplicato con {titoli[t]}')
        if d in descr:
            errori.append(f'{f}: description duplicata con {descr[d]}')
        titoli[t], descr[d] = f, f
        if len(d) > 170:
            errori.append(f'{f}: description troppo lunga ({len(d)})')
        for tag in re.findall(r'<svg\b[^>]*>', h):
            if 'aria-hidden="true"' not in tag and 'role="img"' not in tag:
                errori.append(f'{f}: SVG senza aria-hidden né role="img": {tag[:80]}')
        ids = re.findall(r'\sid="([^"]+)"', h)
        dup = {i for i in ids if ids.count(i) > 1}
        if dup:
            errori.append(f'{f}: id duplicati {sorted(dup)}')
        # niente salti di livello tra i titoli
        lvl = [int(x) for x in re.findall(r'<h([1-6])[\s>]', h)]
        for a, b in zip(lvl, lvl[1:]):
            if b > a + 1:
                errori.append(f'{f}: salto di livello H{a} → H{b}')
                break
        # link interni
        if f == '404.html':
            continue
        for href in re.findall(r'<a [^>]*href="([^"]+)"', h):
            if re.match(r'(https?:|mailto:|tel:|javascript:)', href):
                continue
            pth, _, frag = href.partition('#')
            target = pth or f
            if pth and not os.path.exists(os.path.join(out, pth)):
                errori.append(f'{f}: link a file inesistente {href}')
                continue
            if frag and frag not in ids_per_file.get(target, set()):
                errori.append(f'{f}: ancora inesistente {href}')
    return errori


# ----------------------------------------------------------------------------- realizzazioni (elenco e dettaglio)
def realizzazioni():
    p = pagina('realizzazioni')
    body = '\n'.join([
        C.phero(p, 'Le nostre realizzazioni', 'Progetti realizzati per privati, imprese e Pubblica Amministrazione: impianti fotovoltaici, termoidraulici e attività di manutenzione.', cta=False),
        C.realizzazioni_section(),
        C.contact_section(p, 'Hai un progetto simile? Parliamone')])
    return p, doc(p, body)


def progetto(r):
    p = C.progetto_page(r)
    p['schema'] = [C.schema_briciole(p)]
    return p, doc(p, C.progetto_body(p, r))


# ----------------------------------------------------------------------------- main
def scrivi(out, funzioni):
    """Scrive le pagine e restituisce l'elenco (metadati, file)."""
    risultati = []
    for fn in funzioni:
        p, html = fn()
        open(os.path.join(out, p['file']), 'w', encoding='utf-8').write(html)
        risultati.append(p)
    return risultati


def carica_demo(out):
    """Dati di PROVA (cartella dev/, fuori dal sito): servono solo per l'anteprima in _demo/."""
    import importlib.util
    f = os.path.join(ROOT, 'dev', 'fixture_progetti.py')
    if not os.path.exists(f):
        sys.exit('Anteprima non disponibile: manca dev/fixture_progetti.py')
    spec = importlib.util.spec_from_file_location('fixture_progetti', f)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    P.FOTO_DIR = os.path.join(out, 'assets', 'realizzazioni')
    C_FOTO = P.FOTO_DIR
    os.makedirs(C_FOTO, exist_ok=True)
    m.crea_foto(C_FOTO)
    P.PROGETTI[:] = m.PROGETTI
    P.HOME_ATTIVA = True
    # gallerie e copertine di PROVA (solo in _demo/): privati sopra soglia, imprese esattamente alla soglia, PA sotto soglia
    gm = importlib.util.module_from_spec(importlib.util.spec_from_file_location('fixture_gallerie', os.path.join(ROOT, 'dev', 'fixture_gallerie.py')))
    gm.__spec__.loader.exec_module(gm)
    G.DIR = os.path.join(out, 'assets', 'gallerie')
    C.SERVIZI_DIR = os.path.join(out, 'assets', 'servizi')
    gm.crea(G.DIR, C.SERVIZI_DIR)
    for k in G.FOTO:
        G.FOTO[k][:] = gm.FOTO[k]


def main():
    demo = '--demo' in sys.argv
    out = ROOT
    if demo:
        out = os.path.join(ROOT, '_demo')
        shutil.rmtree(out, ignore_errors=True)
        os.makedirs(out)
        for f in ['site.css', 'pagine.css', 'ri.js', 'site.js', 'globe.js', 'recensioni.js', 'recensione.html'] + LEGALI:
            if os.path.exists(os.path.join(ROOT, f)):
                shutil.copy(os.path.join(ROOT, f), out)
        shutil.copytree(os.path.join(ROOT, 'assets'), os.path.join(out, 'assets'))
        carica_demo(out)
        # legal.py non viene rieseguito: si usano le copie già generate
    try:
        attivi = P.attivi()
        for area in G.MACROAREE:
            G.pubblicate(area)                      # ferma la build se una foto pubblicata è incompleta o non è una foto reale
    except (P.ErroreProgetto, G.ErroreGalleria) as e:
        sys.exit(f'\nBUILD FERMATA: {e}')
    funzioni = [home, privati, imprese, pa]
    if attivi:
        funzioni.append(realizzazioni)
        funzioni += [(lambda r=r: progetto(r)) for r in attivi]
    funzioni += [contatti, pagina_404]
    # niente file orfani: pagine di dettaglio o elenco di build precedenti che ora non devono esistere
    voluti = {'realizzazioni.html'} if attivi else set()
    voluti |= {P.pagina_progetto(r) for r in attivi}
    for f in os.listdir(out):
        if (f == 'realizzazioni.html' or re.fullmatch(r'progetto-[a-z0-9-]+\.html', f)) and f not in voluti:
            os.remove(os.path.join(out, f))
    pagine = scrivi(out, funzioni)
    files = [p['file'] for p in pagine]
    percorsi = [p['path'] for p in pagine if not p.get('noindex')]
    open(os.path.join(out, 'sitemap.xml'), 'w', encoding='utf-8').write(sitemap(percorsi, out))
    open(os.path.join(out, 'robots.txt'), 'w', encoding='utf-8').write(robots())
    err = controlla(out, files)
    for f in files:
        print(f'{f:32s}{os.path.getsize(os.path.join(out, f)) // 1024:4d} KB')
    for a in P.avvisi() + G.avvisi():
        print('NOTA:', a)
    if err:
        print('\nCONTROLLI FALLITI:')
        for e in err:
            print(' -', e)
        sys.exit(1)
    print('\nControlli automatici superati (link, ancore, titoli, H1, SVG, id, TODO).')
    if demo:
        print('Anteprima con dati FITTIZI creata in _demo/ — NON pubblicare questa cartella.')


if __name__ == '__main__':
    main()
