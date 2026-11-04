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
import servizi_pagine as SP
import lavora as LAV
import offerte as OF
from art import ART, DEFS

ROOT = C.ROOT
esc, qa = C.esc, C.qa

# ----------------------------------------------------------------------------- pagine: metadati SEO
PAGINE = {
    'home': dict(path='/', file='index.html',
                 title='Impianti Fotovoltaici e Termoidraulici | Rivetti Impianti',
                 desc='Dal 2008 progettiamo, realizziamo e manteniamo impianti fotovoltaici, termoidraulici e sistemi energetici per privati, imprese ed enti pubblici.'),
    'privati': dict(path='/privati.html', file='privati.html', crumbs=[('Privati', '/privati.html')],
                    title='Fotovoltaico, Solare Termico e Servizi per Privati | Rivetti Impianti',
                    desc='Impianti fotovoltaici, solare termico, lavaggio moduli, termografia, manutenzione e monitoraggio per la tua casa.'),
    'imprese': dict(path='/imprese.html', file='imprese.html', crumbs=[('Imprese', '/imprese.html')],
                    title='Fotovoltaico Industriale, O&M e CER per Imprese | Rivetti Impianti',
                    desc='Fotovoltaico industriale, O&M, lavaggio moduli, termografia e Comunità Energetiche Rinnovabili (CER) per le aziende.'),
    'pa': dict(path='/pubblica-amministrazione.html', file='pubblica-amministrazione.html', crumbs=[('Pubblica Amministrazione', '/pubblica-amministrazione.html')],
               title='Fotovoltaico e Riqualificazione per la PA | Rivetti Impianti',
               desc='Fotovoltaico PA, riqualificazione energetica, manutenzione e assistenza per la Pubblica Amministrazione.'),
    'realizzazioni': dict(path='/realizzazioni.html', file='realizzazioni.html', crumbs=[('Realizzazioni', '/realizzazioni.html')],
                          title='Realizzazioni | Rivetti Impianti',
                          desc='I lavori realizzati da Rivetti Impianti per privati, imprese e Pubblica Amministrazione: impianti fotovoltaici, termoidraulici e manutenzione.'),
    'offerte': dict(path='/offerte.html', file='offerte.html', crumbs=[('Offerte', '/offerte.html')],
                    title='Offerte Speciali | Rivetti Impianti',
                    desc='Offerte per fotovoltaico con accumulo, climatizzazione, caldaie e manutenzione: prezzi chiari, detrazione fiscale 50% e finanziamento a tasso agevolato.'),
    'contatti': dict(path='/contatti.html', file='contatti.html', crumbs=[('Contatti', '/contatti.html')],
                     title='Contatti e Richiesta di Sopralluogo | Rivetti Impianti',
                     desc='Contatta Rivetti Impianti: telefono, WhatsApp, email e modulo per richiedere un sopralluogo o un preventivo.'),
    'lavora-con-noi': dict(path='/lavora-con-noi.html', file='lavora-con-noi.html', crumbs=[('Lavora con noi', '/lavora-con-noi.html')],
                           title='Lavora con noi | Rivetti Impianti',
                           desc='Candidati a Rivetti Impianti: invia il tuo curriculum per posizioni di tecnico, installatore o professionista nel fotovoltaico e nella termoidraulica.'),
    '404': dict(path='/404.html', file='404.html', title='Pagina non trovata | Rivetti Impianti',
                desc='La pagina richiesta non esiste o è stata spostata.', noindex=True),
}
LEGALI = ['privacy.html', 'cookie.html', 'note-legali.html']          # generate da legal.py
ALTRE = {'recensione.html'}                                          # pagina a parte (noindex)


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


def home():
    hero_html = '''<section class="hero" id="home">
    <div class="hero-content">
        <span class="hero-tag">Soluzioni Energetiche Avanzate</span>
        <h1 class="hero-title">Smetti di subire i costi dell'energia. Inizia a investire nel tuo futuro.</h1>
        <p class="hero-subtitle">Riduci la dipendenza energetica e valorizza il tuo immobile con soluzioni efficienti, affidabili e progettate per durare.</p>
        <a href="#contatti" class="btn btn-primary">Richiedi un sopralluogo &rarr;</a>
        <a href="#contatti" class="btn btn-secondary">Parla con un tecnico</a>
    </div>
</section>'''

    intro = '''<section class="sec intro" id="servizi">
    <div class="sec-head">
        <h2>Cosa facciamo</h2>
        <p>Impianti e servizi tecnici per privati, imprese ed enti pubblici. Operiamo nel fotovoltaico, nella termoidraulica, nella climatizzazione e nella manutenzione, su nuovi impianti e su sistemi già esistenti. Ogni intervento viene definito in base alle esigenze del cliente e alle caratteristiche tecniche del progetto.</p>
    </div>
</section>'''

    about = '''<section class="sec about" id="informazioni">
    <div class="sec-head">
        <span class="eyebrow">Chi siamo</span>
        <h2>Dal 2008 lavoriamo su impianti energetici per privati, imprese ed enti pubblici</h2>
    </div>
    <div class="about-wrap">
        <div class="about-text">
            <p>Rivetti Impianti nasce nel 2008 per iniziativa di Alessandro Rivetti. Nel tempo l'attività si è sviluppata nel fotovoltaico, nel solare termico, nella termoidraulica civile e industriale, nella climatizzazione avanzata e nella manutenzione programmata.</p>
            <p>Il lavoro viene seguito da un team tecnico che coordina le fasi di valutazione, progettazione, realizzazione e manutenzione, coinvolgendo quando necessario collaboratori specializzati.</p>
            <p class="motto">Competenza tecnica, continuità del servizio e attenzione alla sicurezza.</p>
        </div>
        <div class="facts">
            <div class="fact"><span>Anno di fondazione</span><b>2008</b></div>
            <div class="fact"><span>Competenze</span><b>Fotovoltaico, termoidraulica e manutenzione</b></div>
            <div class="fact"><span>Sede</span><b>Via Landolfo, Mondragone (CE)</b></div>
        </div>
    </div>
</section>'''

    body = '\n'.join([
        hero_html,
        intro,
        about,
        '''<section class="sec reviews" id="recensioni">
    <div class="sec-head">
        <h2>Cosa dicono di noi</h2>
        <p>La soddisfazione dei nostri clienti è il nostro traguardo migliore.</p>
    </div>
    <div class="reviews-grid">
        <div class="review-card">
            <div class="review-author">Marco V. (Proprietario di casa)</div>
            <p class="review-text">"Installazione del fotovoltaico impeccabile! L'impianto gira a pieno regime e ho visto una netta miglioria sui consumi domestici. Team professionale, puntuale e disponibilissimo."</p>
        </div>
        <div class="review-card">
            <div class="review-author">Ing. Salvatore R. (Referente Aziendale)</div>
            <p class="review-text">"Ci siamo affidati a Rivetti Impianti per la termoidraulica e il coordinamento impiantistico industriale. Competenza tecnica straordinaria e totale trasparenza nella gestione dei lavori."</p>
        </div>
        <div class="review-card">
            <div class="review-author">Giuseppe M. (Condominio)</div>
            <p class="review-text">"Lavori eseguiti a regola d'arte e grande cortesia. Hanno gestito tutto loro dalla progettazione alla documentazione finale. Consigliatissimi in tutta la Campania!"</p>
        </div>
    </div>
</section>''',
        '''<section class="sec contact" id="contatti">
    <div class="sec-head">
        <h2>Parliamo del tuo impianto</h2>
        <p>Descrivici ciò di cui hai bisogno. Puoi chiamarci, scriverci su WhatsApp oppure utilizzare il modulo di contatto per richiedere informazioni o un sopralluogo gratuito.</p>
    </div>
</section>'''
    ])
    
    p = dict(key='home', path='/', file='index.html', title="Impianti Fotovoltaici e Termoidraulici | Rivetti Impianti", desc="Dal 2008 progettiamo, realizziamo e manteniamo impianti fotovoltaici, termoidraulici e sistemi energetici per privati, imprese ed enti pubblici.")
    return p, doc(p, body)
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


def offerte():
    p = pagina('offerte')
    body = '\n'.join([
        C.phero(p, 'Offerte Speciali', 'Soluzioni complete per la tua casa a condizioni chiare: energia dal sole, comfort tutto l&rsquo;anno e impianti sempre efficienti. Con detrazione fiscale e finanziamento agevolato.',
                tags=['Prezzi chiari', 'Detrazione fiscale 50%', 'Finanziamento agevolato']),
        OF.sezioni(p), C.contact_section(p)])
    return p, doc(p, body)


def contatti():
    p = pagina('contatti')
    body = '\n'.join([
        C.phero(p, 'Parla con Rivetti Impianti', 'Per privati, imprese e Pubbliche Amministrazioni: scegli come contattarci e un tecnico ti risponderà.'),
        C.contact_section(p)])
    return p, doc(p, body)


def lavora_con_noi():
    p = pagina('lavora-con-noi')
    return p, doc(p, LAV.corpo(p), dialoghi=False, scripts=('ri.js', 'lavora.js', 'site.js'))


def pagine_servizio():
    """Una funzione-pagina per ogni voce del menu «Servizi» (dati in src/servizi_pagine.py)."""
    def crea(s):
        def f():
            p = dict(path='/' + s['file'], file=s['file'], key='sv-' + SP.slug(s), title=s['title'], desc=s['desc'],
                     crumbs=[(SP.MACRO[s['macro']]['nome'], '/' + SP.MACRO[s['macro']]['pagina']), (s['menu'], '/' + s['file'])])
            p['schema'] = [C.schema_briciole(p)]
            return p, doc(p, SP.corpo(s, p), scripts=('ri.js', 'site.js'))
        return f
    return [crea(s) for s in SP.PAGINE_SERVIZI]


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
        for f in ['site.css', 'pagine.css', 'ri.js', 'site.js', 'recensioni.js', 'recensione.html'] + LEGALI:
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
    err_sv = SP.errori()
    if err_sv:
        sys.exit('\nBUILD FERMATA (pagine servizio):\n  ' + '\n  '.join(err_sv))
    funzioni = [home, privati, imprese, pa] + pagine_servizio()
    if attivi:
        funzioni.append(realizzazioni)
        funzioni += [(lambda r=r: progetto(r)) for r in attivi]
    funzioni += [lavora_con_noi, offerte, contatti, pagina_404]
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