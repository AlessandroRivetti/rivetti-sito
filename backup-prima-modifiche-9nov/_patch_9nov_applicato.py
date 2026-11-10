# -*- coding: utf-8 -*-
"""Modifiche del 9 novembre (eseguito una volta sola dalla radice del sito)."""
import os, re
R = os.path.dirname(os.path.abspath(__file__))
def rd(f): return open(os.path.join(R, f), encoding='utf-8').read()
def wr(f, s): open(os.path.join(R, f), 'w', encoding='utf-8').write(s)
def sub1(s, a, b, tag):
    assert s.count(a) == 1, f'{tag}: trovato {s.count(a)} volte'
    return s.replace(a, b)

# ------------------------------------------------------------------ dati.py
d = rd('src/dati.py')
i = d.index('HERO_HOME = dict(')
j = d.index('\n)\n', i) + 3
d = d[:i] + '''HERO_HOME = dict(
    video='assets/rivetti-showreel.mp4',
    poster='assets/servizi/pa-hero.png',
    tag='Rivetti Impianti &bull; Technical Engineering',
    titolo_rosso="Smetti di subire i costi dell'energia.",      # in ROSSO
    titolo_verde="Inizia a investire nel tuo futuro.",           # in VERDE
    testo=("Riduci la dipendenza energetica e valorizza il tuo immobile con soluzioni efficienti, affidabili e progettate per durare."
           "<br><br><strong>La fiducia si costruisce con i fatti, non con le promesse.</strong> In Rivetti Impianti crediamo che ogni investimento "
           "debba essere chiaro, sicuro e sostenibile. Per questo offriamo consulenza tecnica, preventivi trasparenti, componenti di qualità e un "
           "servizio di assistenza che continua anche dopo la realizzazione."),
    chiusura="Chiedi subito un preventivo e smetti di preoccuparti della bolletta elettrica, ci pensiamo noi!",
    cta1='Richiedi un preventivo Gratuito', cta2='Parla direttamente con un Tecnico',
    audio_on='Attiva audio', audio_off='Disattiva audio',
)
''' + d[j:]
d = sub1(d, "'intro': 'Alcuni interventi possono beneficiare di incentivi, detrazioni, contributi o strumenti di finanziamento. Disponibilità, requisiti e condizioni dipendono dalla normativa vigente e dal singolo caso.',",
 "'intro': 'Valorizza il tuo investimento con gli strumenti giusti: molti dei nostri interventi possono accedere a detrazioni fiscali, incentivi o formule di sostegno dedicate. Le opportunità variano in base alla normativa vigente e alle caratteristiche specifiche del tuo progetto: ti affianchiamo per orientarti al meglio e valutare tutte le opzioni applicabili al tuo caso.',", 'intro')
d = d.rstrip() + '''


# ----------------------------------------------------------------------------- STORIA AZIENDALE («Chi siamo», #informazioni)
# Testo ufficiale completo. **testo** = grassetto. Una riga = un paragrafo; l'ultimo è il motto.
STORIA_TITOLO = 'Dal 2008 lavoriamo su impianti energetici per privati, imprese ed enti pubblici'
STORIA = [
    "**Rivetti Impianti** — Una storia fatta di energia, coraggio e visione.",
    "Ogni grande storia nasce da una scintilla. La nostra, nel 2008, è diventata una promessa: trasformare il lavoro in valore, le competenze in soluzioni e l'energia in futuro.",
    "Ci sono storie che non nascono negli uffici, né tra le righe di un progetto. Nascono sul campo, dove le mani costruiscono, la fatica insegna, gli imprevisti mettono alla prova e ogni dettaglio fa la differenza. Nascono dalla determinazione di chi non cerca scorciatoie, ma sceglie ogni giorno la strada più difficile: quella fatta di impegno, precisione e responsabilità.",
    "È da questa visione che, nel 2008, **Michele Rivetti** dà vita a Rivetti Impianti.",
    "All'inizio c'è una convinzione semplice, ma destinata a diventare il fondamento di tutto: un lavoro ben fatto non è soltanto un risultato da consegnare. È una promessa da mantenere. Una responsabilità verso chi si affida a noi. Un nome, quello della nostra famiglia e della nostra azienda, da difendere attraverso ogni scelta, ogni installazione, ogni intervento.",
    "Gli anni passano, le sfide cambiano e le tecnologie evolvono. A raccogliere questa preziosa eredità e guidare l'azienda verso nuovi orizzonti è oggi la **seconda generazione**: una continuità familiare che unisce i valori tradizionali del lavoro ben fatto a una visione moderna, tecnica e manageriale, indispensabile per affrontare la transizione energetica e continuare a crescere.",
    "Con costanza, studio e investimenti, Rivetti Impianti amplia le proprie competenze e consolida la propria presenza nel settore energetico, sviluppando soluzioni che spaziano dagli impianti fotovoltaici ai sistemi di accumulo, dalla termoidraulica ai servizi di manutenzione. Ogni nuova sfida diventa un'occasione per crescere. Ogni esperienza aggiunge conoscenza. Ogni progetto rafforza una convinzione: l'eccellenza non si improvvisa, si costruisce giorno dopo giorno.",
    "Ma crescere, per noi, non significa soltanto realizzare impianti più complessi o affrontare progetti più ambiziosi. Significa essere pronti ad assumerci responsabilità maggiori. Significa investire nelle persone, affinare i processi, scegliere soluzioni affidabili e mantenere sempre al centro ciò che conta davvero: la qualità del lavoro, la sicurezza degli interventi e la fiducia dei nostri clienti.",
    "Oggi lavoriamo al fianco di privati, imprese ed enti pubblici, affrontando esigenze diverse con lo stesso approccio: ascoltare, analizzare, progettare e realizzare soluzioni concrete, con attenzione a ogni fase del percorso. Dalla prima valutazione alla messa in opera, fino alla manutenzione, mettiamo in campo competenza tecnica, organizzazione e una visione orientata alla durata nel tempo.",
    "Perché la professionalità non si misura soltanto da ciò che si realizza, ma anche da come lo si realizza. Nella chiarezza delle informazioni, nella trasparenza dei rapporti, nella cura dei dettagli e nella capacità di esserci anche dopo la conclusione di un lavoro.",
    "La fiducia non si chiede. Si conquista. E si conferma ogni giorno.",
    "In un mondo in cui l'energia è diventata una delle grandi sfide del nostro tempo, sentiamo la responsabilità di contribuire a un cambiamento concreto. Crediamo nell'efficienza energetica, nelle fonti rinnovabili e nelle tecnologie capaci di ridurre gli sprechi e valorizzare le risorse. Crediamo in un progresso che non insegua soltanto l'innovazione, ma sappia metterla al servizio delle persone, delle imprese e dell'ambiente.",
    "La sostenibilità, per noi, non è una parola da esibire. È una direzione da seguire. È la scelta di progettare pensando al domani, di lavorare con consapevolezza e di costruire soluzioni che sappiano generare valore nel tempo.",
    "Eppure, dopo ogni traguardo, c'è sempre una nuova sfida. Una tecnologia da conoscere, un'esigenza da comprendere, un progetto da trasformare in realtà. È questa tensione verso il miglioramento a tenerci in movimento. È la stessa determinazione che ci ha accompagnati nel 2008 e che continua a guidarci oggi.",
    "Perché l'energia più importante non è soltanto quella che produciamo o trasformiamo. È quella che mettiamo nel nostro lavoro.",
    "È l'energia delle persone che ogni giorno scelgono di fare la differenza. Della competenza che diventa affidabilità. Della costanza che diventa esperienza. Della passione che si trasforma in qualità. Della fiducia che, progetto dopo progetto, diventa una relazione destinata a durare.",
    "Questa è **Rivetti Impianti**. Una storia nata dal lavoro, cresciuta attraverso le sfide e proiettata verso il futuro. Una realtà che guarda all'innovazione senza rinnegare le proprie radici, che affronta il cambiamento con determinazione e che riconosce in ogni progetto un impegno preciso: fare le cose per bene, con serietà, trasparenza e rispetto per chi ci sceglie.",
    "Dal 2008, continuiamo a costruire il nostro percorso con la stessa convinzione: il futuro non si aspetta. Si progetta. Si realizza. Si alimenta, ogni giorno, con le scelte giuste.",
]
STORIA_MOTTO = "«Nati dal lavoro. Cresciuti con passione. Proiettati verso il futuro.»"


# ----------------------------------------------------------------------------- WIDGET RISPARMIO BOLLETTA
# Importi forniti dal titolare (esempio mensile). Le voci di spesa sono descrittive, senza importi.
BOLLETTA = dict(
    eyebrow='Risparmio in bolletta',
    titolo='Quanto pesa la bolletta, con e senza fotovoltaico',
    lead='Un confronto mensile per capire la differenza che può fare produrre da soli una parte dell’energia che consumi.',
    senza=dict(etichetta='Senza impianto fotovoltaico', importo='156,97', voci=[
        'Tutta l’energia consumata acquistata dalla rete',
        'Trasporto, gestione del contatore e oneri di sistema sull’intero consumo',
        'Imposte e IVA calcolate sull’importo più alto',
    ]),
    con=dict(etichetta='Con impianto fotovoltaico', importo='31,39', voci=[
        'Gran parte dell’energia prodotta e consumata in casa',
        'Acquisti dalla rete ridotti al fabbisogno residuo',
        'Imposte e oneri calcolati su un importo molto più basso',
    ], risparmio='-80%'),
    nota='Esempio indicativo basato sugli importi mensili indicati: il risparmio effettivo dipende da consumi, dimensionamento dell’impianto, quota di autoconsumo e tariffe in vigore, e viene valutato dal nostro tecnico caso per caso.',
    cta='Scrivici su WhatsApp',
)
'''
wr('src/dati.py', d)

# ------------------------------------------------------------------ comp.py
c = rd('src/comp.py')
c = sub1(c, '''f'<a href="{H("informazioni")}" data-spy="informazioni">Chi siamo</a>',''',
            '''f'<a href="{pre}index.html#informazioni">Chi siamo</a>',''', 'nav chi')
c = sub1(c, "('Chi siamo', H('informazioni'))", "('Chi siamo', f'{pre}index.html#informazioni')", 'footer chi')
c = c.rstrip() + '''


# ---------------------------------------------------------------- Chi siamo (storia aziendale, dati in dati.STORIA)
def _storia_html(t):
    return re.sub(r'\\*\\*(.+?)\\*\\*', r'<strong>\\1</strong>', esc(t))


def about_section():
    par = D.STORIA
    corpo = f'<p class="about-lead">{_storia_html(par[0])}</p>' + ''.join(f'<p>{_storia_html(t)}</p>' for t in par[1:])
    return f\'\'\'<section class="sec about" id="informazioni">
  <div class="sec-head">
    <span class="eyebrow">Chi siamo</span>
    <h2>{esc(D.STORIA_TITOLO)}</h2>
  </div>
  <div class="about-wrap">
    <div class="about-text">
      {corpo}
      <p class="motto">{esc(D.STORIA_MOTTO)}</p>
    </div>
    <div class="facts">
      <div class="fact"><span>Anno di fondazione</span><b>{D.SITO['anno_inizio']}</b></div>
      <div class="fact wide"><span>Competenze</span><b>Fotovoltaico, termoidraulica e manutenzione</b></div>
      <div class="fact wide"><span>Sede</span><b>{esc(indirizzo())}</b></div>
      <div class="fact wide"><span>P.IVA</span><b>{D.SOCIETA['piva_cf']}</b></div>
    </div>
  </div>
</section>\'\'\'


# ---------------------------------------------------------------- widget confronto bolletta
def bolletta_widget(compatto=False, sid='risparmio-bolletta'):
    B = D.BOLLETTA
    S, K = B['senza'], B['con']
    voci = lambda L: '' if compatto else '<ul class="bol-voci">' + ''.join(f'<li>{esc(x)}</li>' for x in L) + '</ul>'
    return f\'\'\'<section class="sec bol{' bol-compatto' if compatto else ''}" id="{sid}" aria-labelledby="{sid}-t">
  {sec_head(B['eyebrow'], esc(B['titolo']), esc(B['lead'])).replace('<h2>', f'<h2 id="{sid}-t">', 1)}
  <div class="bol-grid">
    <article class="bol-card bol-senza">
      <span class="bol-tag">{esc(S['etichetta'])}</span>
      <p class="bol-prezzo"><b>{S['importo']} &euro;</b><small>/mese</small></p>
      {voci(S['voci'])}
    </article>
    <div class="bol-freccia" aria-hidden="true"><svg viewBox="0 0 24 24" focusable="false"><path d="M4 12h15M13 6l6 6-6 6"/></svg></div>
    <article class="bol-card bol-con">
      <span class="bol-tag">{esc(K['etichetta'])}</span>
      <p class="bol-prezzo"><b>{K['importo']} &euro;</b><small>/mese</small><span class="bol-badge">{K['risparmio']} di risparmio in bolletta</span></p>
      {voci(K['voci'])}
    </article>
  </div>
  <p class="bol-nota">{esc(B['nota'])}</p>
  <div class="bol-cta"><a class="btn btn-wa" href="{qa(wa_for('privati_fv'))}" target="_blank" rel="noopener">{WA}{esc(B['cta'])}</a>
    <a class="btn btn-ghost" href="#contatti" data-service="Fotovoltaico domestico">Richiedi un preventivo gratuito &rarr;</a></div>
</section>\'\'\'
'''
wr('src/comp.py', c)

# ------------------------------------------------------------------ build.py
b = rd('src/build.py')
a0 = b.index('''      <h1 class="hero-title">{H['titolo']}</h1>''')
a1 = b.index('</section>\'\'\'', a0)
b = b[:a0] + '''      <h1 class="hero-title"><span class="hl hl-rosso">{H['titolo_rosso']}</span> <span class="hl hl-verde">{H['titolo_verde']}</span></h1>
      <p class="hero-subtitle">{H['testo']}</p>
      <p class="hero-chiusura">{H['chiusura']}</p>
      <div class="hero-actions cta"><a class="btn btn-light" href="#contatti" data-service="Sopralluogo">{H['cta1']} &rarr;</a>
        <a class="btn btn-wa" href="{C.qa(C.wa_for('home'))}" target="_blank" rel="noopener">{C.WA}{H['cta2']} &rarr;</a></div>
    </div>
  </div>
''' + b[a1:]
# rimuove «Cosa facciamo» (intro) e il vecchio «about» locale: si usa C.about_section()
i0 = b.index('    intro = f\'\'\'<section class="sec intro" id="servizi">')
i1 = b.index("    body = '\\n\\n'.join(x for x in [", i0)
b = b[:i0] + b[i1:]
b = sub1(b, "hero, C.stats_section(), intro, C.real_home_section(),", "hero, C.stats_section(), C.bolletta_widget(compatto=True, sid='risparmio-home'), C.real_home_section(),", 'body1')
b = sub1(b, "C.incentivi_section(), about,", "C.incentivi_section(), C.about_section(),", 'body2')
b = sub1(b, "        C.privati_fv_sections(),\n", "        C.privati_fv_sections(),\n        C.bolletta_widget(),\n", 'privati')
wr('src/build.py', b)

# ------------------------------------------------------------------ servizi_pagine.py
s = rd('src/servizi_pagine.py')
s = sub1(s, "    return '\\n'.join(x for x in [_hero(s), _perche(s), _come(s), _foto(s), _cta(s), contatto, _altri(s)] if x)",
 "    bol = C.bolletta_widget() if s['file'] == 'fotovoltaico-residenziale.html' else ''\n    return '\\n'.join(x for x in [_hero(s), _perche(s), bol, _come(s), _foto(s), _cta(s), contatto, _altri(s)] if x)", 'sp')
wr('src/servizi_pagine.py', s)

# ------------------------------------------------------------------ CSS
css = rd('pagine.css').rstrip() + '''

/* ===== 9 novembre: titolo Hero rosso/verde, storia, widget bolletta ===== */
.hero-title .hl{display:inline-block;margin:0 0 8px;padding:.04em .42em .08em;border-radius:10px;background:#fff;box-shadow:0 10px 24px -14px rgba(6,30,70,.55)}
.hero-title .hl-rosso{color:red}
.hero-title .hl-verde{color:green}
.hero-chiusura{max-width:520px;margin:-12px 0 26px;font-weight:700;font-size:1.08rem;color:#fff}
@media (max-width:900px){.hero-chiusura{margin:-6px 0 18px;font-size:1rem}}
.about-text .about-lead{font-weight:700;font-size:1.15rem;color:var(--green-d);margin-bottom:6px}
.about-text .motto{background:rgba(35,163,106,.09);border-left:4px solid var(--green);padding:18px 22px;border-radius:0 12px 12px 0;color:var(--green-d);font-weight:700;font-size:1.05rem;margin-top:26px}

.bol{background:linear-gradient(180deg,#fff,var(--paper))}
.bol-grid{display:grid;grid-template-columns:1fr auto 1fr;gap:22px;align-items:stretch;max-width:1040px;margin:0 auto}
.bol-card{border-radius:24px;padding:30px 30px 26px;background:#fff;border:2px solid var(--line);box-shadow:var(--shadow);transition:transform .35s,box-shadow .35s}
.bol-card:hover{transform:translateY(-5px)}
.bol-senza{border-color:#f3b8b3;background:linear-gradient(180deg,#fff,#fff5f4)}
.bol-con{border-color:#9edbbd;background:linear-gradient(180deg,#fff,#effaf4)}
.bol-tag{display:inline-block;padding:5px 14px;border-radius:999px;font:600 .74rem var(--f-display);letter-spacing:.08em;text-transform:uppercase}
.bol-senza .bol-tag{background:#fde4e1;color:#b83227}
.bol-con .bol-tag{background:#d8f3e5;color:var(--green-d)}
.bol-prezzo{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px;margin:16px 0 14px}
.bol-prezzo b{font:700 clamp(2.1rem,4.4vw,3rem) var(--f-display)}
.bol-senza .bol-prezzo b{color:#b83227}
.bol-con .bol-prezzo b{color:var(--green-d)}
.bol-prezzo small{color:var(--ink2);font-size:1rem}
.bol-badge{flex-basis:100%;display:inline-block;width:fit-content;margin-top:6px;padding:6px 14px;border-radius:999px;background:var(--green);color:#fff;font:700 .85rem var(--f-display)}
.bol-voci{list-style:none;display:grid;gap:10px;color:var(--ink2);font-size:.95rem}
.bol-voci li{position:relative;padding-left:22px}
.bol-voci li::before{content:"";position:absolute;left:0;top:.5em;width:9px;height:9px;border-radius:50%}
.bol-senza .bol-voci li::before{background:#e0675d}
.bol-con .bol-voci li::before{background:var(--green)}
.bol-freccia{display:grid;place-items:center;color:var(--blue)}
.bol-freccia svg{width:42px;height:42px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.bol-nota{max-width:780px;margin:24px auto 0;text-align:center;color:var(--ink2);font-size:.86rem}
.bol-cta{display:flex;flex-wrap:wrap;justify-content:center;gap:14px;margin-top:22px}
.bol-compatto .bol-card{padding:24px}
@media (max-width:820px){.bol-grid{grid-template-columns:1fr}.bol-freccia svg{transform:rotate(90deg)}}
@media (prefers-reduced-motion:reduce){.bol-card:hover{transform:none}}
'''
wr('pagine.css', css)
print('PATCH 9 NOV OK')
