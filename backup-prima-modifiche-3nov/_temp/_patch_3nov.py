# -*- coding: utf-8 -*-
"""Applica le modifiche del 3 novembre al sito (eseguito una volta sola)."""
import re, os
R = os.path.dirname(os.path.abspath(__file__))
def rd(f): return open(os.path.join(R, f), encoding='utf-8').read()
def wr(f, s): open(os.path.join(R, f), 'w', encoding='utf-8').write(s)
def sub1(s, a, b, tag):
    assert s.count(a) == 1, f'{tag}: pattern trovato {s.count(a)} volte'
    return s.replace(a, b)

# ---------------------------------------------------------------- build.py
b = rd('src/build.py')
# 1) home(): da "    intro = f'''..." (prima occorrenza) fino al return finale dentro home(), riscritto pulito
i0 = b.index("    intro = f'''<section class=\"sec intro\" id=\"servizi\">")
i1 = b.index("# ----------------------------------------------------------------------------- PRIVATI / IMPRESE / PA")
about = '''    about = f\'\'\'<section class="sec about" id="informazioni">
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
</section>\'\'\'

    body = '\\n\\n'.join(x for x in [
        hero, C.stats_section(), intro, C.real_home_section(),
        C.come_section(), C.incentivi_section(), about, C.qualifiche_section(), C.marchi_section(),
        C.reviews_section(), C.faq_section('home', 'Domande frequenti', 'FAQ'),
        C.contact_section(p, 'Parliamo del tuo impianto', 'Descrivici ciò di cui hai bisogno. Puoi chiamarci, scriverci su WhatsApp oppure utilizzare il modulo: raccoglieremo le informazioni necessarie e, quando serve, organizzeremo un sopralluogo.')] if x)
    return p, doc(p, body, scripts=('ri.js', 'recensioni.js', 'site.js'))


'''
intro = '''    intro = f\'\'\'<section class="sec intro" id="servizi">
  {C.sec_head('Cosa facciamo', 'Impianti e servizi tecnici per privati, imprese ed enti pubblici', 'Operiamo nel fotovoltaico, nella termoidraulica, nella climatizzazione e nella manutenzione, su nuovi impianti e su sistemi già esistenti. Ogni intervento viene definito in base alle esigenze del cliente e alle caratteristiche tecniche del progetto.')}
</section>\'\'\'

'''
b = b[:i0] + intro + about + b[i1:]

# 2) PAGINE: lavora-con-noi + pagine servizio
b = sub1(b, "    '404': dict(path='/404.html'",
 "    'lavora-con-noi': dict(path='/lavora-con-noi.html', file='lavora-con-noi.html', crumbs=[('Lavora con noi', '/lavora-con-noi.html')],\n"
 "                           title='Lavora con noi | Rivetti Impianti',\n"
 "                           desc='Candidati a Rivetti Impianti: invia il tuo curriculum per posizioni di tecnico, installatore o professionista nel fotovoltaico e nella termoidraulica.'),\n"
 "    '404': dict(path='/404.html'", 'PAGINE')
b = sub1(b, "def pagina(key):\n    p = dict(PAGINE[key], key=key)",
 "def pagina(key):\n    p = dict(PAGINE[key], key=key)", 'pagina')
b = sub1(b, "    elif 'crumbs' in p:\n        schema = [C.schema_briciole(p)]",
 "    elif 'crumbs' in p:\n        schema = [C.schema_briciole(p)]", 'pagina2')

# 3) import
b = sub1(b, "import dati as D", "import dati as D", 'imp') if "import dati as D" in b and b.count("import dati as D") == 1 else b
if 'servizi_pagine' not in b:
    m = re.search(r'^(import|from) .*\bcomp as C.*$', b, re.M)
    assert m, 'riga import comp non trovata'
    b = b[:m.end()] + '\nimport servizi_pagine as SP\nimport lavora as LAV' + b[m.end():]

# 4) funzioni pagina nuove (prima di pagina_404)
nuove = '''def lavora_con_noi():
    p = pagina('lavora-con-noi')
    return p, doc(p, LAV.corpo(p), scripts=('ri.js', 'lavora.js', 'site.js'))


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


def pagina_404():'''
b = sub1(b, "def pagina_404():", nuove, 'nuove')

# 5) main(): funzioni + errori dati
b = sub1(b, "    funzioni = [home, privati, imprese, pa]\n",
 "    err_sv = SP.errori()\n    if err_sv:\n        sys.exit('\\nBUILD FERMATA (pagine servizio):\\n  ' + '\\n  '.join(err_sv))\n"
 "    funzioni = [home, privati, imprese, pa] + pagine_servizio()\n", 'main1')
b = sub1(b, "    funzioni += [offerte, contatti, pagina_404]", "    funzioni += [lavora_con_noi, offerte, contatti, pagina_404]", 'main2')

# 6) rimuove il vecchio generatore mai invocato
j = b.index("def genera_pagine_singole_servizi")
b = b[:j].rstrip() + '\n'
wr('src/build.py', b)

# ---------------------------------------------------------------- comp.py: incentivi dinamici
c = rd('src/comp.py')
c = sub1(c, "    for s in D.INCENTIVI['schede']:\n        tit, testo = D.INCENTIVI_HOME['schede'][s['id']]\n        out += f'''    <article class=\"bcard\">",
 "    for n, s in enumerate(D.INCENTIVI['schede']):\n        tit, testo = D.INCENTIVI_HOME['schede'][s['id']]\n        out += f'''    <article class=\"bcard rv\" style=\"--i:{n}\">", 'inc1')
c = sub1(c, "    return f'''<section class=\"sec bonus\" id=\"incentivi\">\n  {sec_head(I['eyebrow']",
 "    return f'''<section class=\"sec bonus bonus-live\" id=\"incentivi\">\n  {sec_head(I['eyebrow']", 'inc2')
c = sub1(c, "  <div class=\"bonus-foot\">\n    <span>{esc(I['nota_foot'])}</span>",
 "  <div class=\"bonus-foot rv\" style=\"--i:3\">\n    <span>{esc(I['nota_foot'])}</span>", 'inc3')
wr('src/comp.py', c)

# ---------------------------------------------------------------- CSS
s = rd('site.css')
a = s.index('/* Linea divisoria geometrica')
z = s.index('/* Cornici e box con angoli geometrici')
s = s[:a] + s[z:]
wr('site.css', s)
pc = rd('pagine.css').rstrip() + '\n' + rd('src/_nuovi-stili.css')
wr('pagine.css', pc)

# ---------------------------------------------------------------- JS
r = rd('ri.js')
r = sub1(r, "  /* Ripiego: apre la posta",
"""  /* Invia un modulo con allegato (FormData, multipart): usato dalla pagina «Lavora con noi». Stesso endpoint di send(). */
  async function sendForm(fd) {
    const ctrl = new AbortController(), t = setTimeout(() => ctrl.abort(), 45000);
    try {
      const r = await fetch(FORM_ENDPOINT, { method: 'POST', headers: { 'Accept': 'application/json' }, body: fd, signal: ctrl.signal });
      let j = {}; try { j = await r.json(); } catch (e) {}
      if (!r.ok || j.success === false || j.success === 'false') throw new Error('invio non confermato');
      return true;
    } finally { clearTimeout(t); }
  }
  /* Ripiego: apre la posta""", 'ri1')
r = sub1(r, "return { send, mailto,", "return { send, sendForm, mailto,", 'ri2')
wr('ri.js', r)

j = rd('site.js').rstrip()
assert j.endswith('})();')
j = j[:-len('})();')] + """
  /* Comparsa progressiva degli elementi .rv (sezione Incentivi): solo con JS, senza JS tutto resta visibile. */
  (function () {
    var els = document.querySelectorAll('.rv');
    if (!els.length) return;
    if (!('IntersectionObserver' in window) || (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) return;
    document.documentElement.classList.add('js-reveal');
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (el) { io.observe(el); });
  })();
})();
"""
wr('site.js', j)
print('PATCH OK')
