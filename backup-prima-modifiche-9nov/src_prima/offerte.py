# -*- coding: utf-8 -*-
"""Pagina Offerte: DATI (prezzi di listino) e componenti.

I PREZZI sono riportati ESATTAMENTE come nell'offerta in corso: per cambiarli si modificano solo i valori qui sotto.
La detrazione fiscale del fotovoltaico è CALCOLATA da questi stessi prezzi (nessun importo scritto a mano):
    detrazione = 50% × (prezzo + IVA), da recuperare in 10 quote annuali di pari importo.
L'aliquota IVA usata nel calcolo è IVA_FV_PERCENTUALE (verificarla con il commercialista).
"""
from decimal import Decimal, ROUND_HALF_UP
import comp as C

esc = C.esc
IVA_FV_PERCENTUALE = Decimal('10')       # IVA applicata a fotovoltaico + accumulo (assunta: aliquota agevolata)
DETRAZIONE_PERCENTUALE = Decimal('50')
DETRAZIONE_ANNI = 10


def euro(x):
    """1234.5 → '€ 1.234,50' (formato italiano, due decimali)."""
    x = Decimal(x).quantize(Decimal('0.01'), ROUND_HALF_UP)
    s = f'{x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    return '€\u00a0' + s


def detrazione(prezzo_imponibile):
    """Restituisce (totale detraibile, quota annua) per un prezzo imponibile."""
    lordo = Decimal(prezzo_imponibile) * (100 + IVA_FV_PERCENTUALE) / 100
    tot = (lordo * DETRAZIONE_PERCENTUALE / 100).quantize(Decimal('0.01'), ROUND_HALF_UP)
    return tot, (tot / DETRAZIONE_ANNI).quantize(Decimal('0.01'), ROUND_HALF_UP)


# ---------------------------------------------------------------------------- DATI (prezzi invariati)
FOTOVOLTAICO = [
    dict(id='fv-3', badge='Un buon inizio!', kwp='3 kWp', acc='5 kWh', titolo='Fotovoltaico 3 kWp + Accumulo da 5 kWh',
         imponibile=5500, prezzo='€ 5.500 + IVA', evidenza=False,
         intro='La soluzione di partenza per iniziare a produrre e a usare la tua energia.'),
    dict(id='fv-6', badge='Più Venduto!', kwp='6 kWp', acc='10 kWh', titolo='Fotovoltaico 6 kWp + Accumulo da 10 kWh',
         imponibile=7900, prezzo='€ 7.900 + IVA', evidenza=True,
         intro='Il giusto equilibrio tra potenza, accumulo e investimento per la famiglia.'),
    dict(id='fv-9', badge='Per una maggiore efficienza', kwp='9 kWp', acc='15 kWh', titolo='Fotovoltaico 9 kWp + Accumulo da 15 kWh',
         imponibile=9500, prezzo='€ 9.500 + IVA', evidenza=False,
         intro='Per chi vuole la massima autonomia e consumi importanti da coprire.'),
]
INCLUSO_FV = ['Progettazione', 'Installazione', 'Collaudo', 'Pratiche di allaccio e GSE']

ALTRE = [
    dict(id='clima', servizio='Termoidraulica e Climatizzazione', icona='snow', badge='Comfort Tutto l’Anno', titolo='Climatizzazione',
         testo='Fornitura, installazione e certificazione di climatizzatori inverter ad alta efficienza energetica (A+++), con riscaldamento e raffrescamento rapido. Tutto incluso.',
         prezzi=[('10.000 BTU', '€ 420,00'), ('13.000 BTU', '€ 440,00'), ('18.000 BTU', '€ 590,00')], nota_prezzo='Tutto IVA inclusa'),
    dict(id='caldaia', servizio='Termoidraulica e Climatizzazione', icona='fire', badge='Risparmio Gas', titolo='Sostituzione Caldaia a Condensazione',
         testo='Sostituzione della vecchia caldaia con un modello a condensazione di ultima generazione.',
         prezzi=[('A partire da', '€ 990,00 + IVA')], nota_prezzo=''),
    dict(id='lavaggio', servizio='Lavaggio moduli fotovoltaici', icona='drop', badge='Manutenzione', titolo='Lavaggio & Check-Up Impianto Fotovoltaico',
         testo='Pulizia professionale dei moduli con acqua demineralizzata, ispezione termografica e verifica dei parametri dell’inverter, per riportare l’impianto alla sua resa migliore.',
         prezzi=[('A partire da', '€ 79,00 + IVA')], nota_prezzo=''),
]
FINANZIAMENTO = 'Possibilità di finanziamento a tasso agevolato'

VANTAGGI = [
    ('Produci la tua energia', 'Ogni kWh prodotto e usato in casa è un kWh in meno da acquistare dalla rete, con un costo che non dipende dalle oscillazioni del mercato.'),
    ('Usala quando serve', 'L’accumulo conserva l’energia del giorno per la sera e la notte: più autonomia, più continuità.'),
    ('Comfort e sicurezza', 'Climatizzatori e caldaie di nuova generazione, installati e certificati da tecnici qualificati, per vivere meglio ogni stagione.'),
    ('Un impianto che dura', 'Pulizia e controlli periodici mantengono alta la resa e proteggono l’investimento nel tempo.'),
]

ICONE = {
    'sun': '<path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1"/><circle cx="12" cy="12" r="4"/>',
    'snow': '<path d="M12 2v20M4.2 7l15.6 10M19.8 7L4.2 17"/><path d="M9.5 3.5L12 6l2.5-2.5M9.5 20.5L12 18l2.5 2.5"/>',
    'fire': '<path d="M12 22c4 0 7-2.7 7-6.6 0-3.3-2.2-5.2-3.6-7C14.5 7.2 14 5 14 3c-3 1.8-5 4.8-5 8-1.6-.8-2-2.3-2-3.5C5 9.8 5 12 5 15.4 5 19.3 8 22 12 22z"/>',
    'drop': '<path d="M12 3c4 5 6 8 6 11a6 6 0 0 1-12 0c0-3 2-6 6-11z"/>',
    'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    'bank': '<path d="M3 10l9-6 9 6M5 10v8M9.500 10v8M14.500 10v8M19 10v8M3 20h18"/>',
}


def ico(n, cls='of-ico'):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICONE[n]}</svg>'


def _fin():
    return f'<p class="of-fin">{ico("bank", "of-fin-ico")}<span>{FINANZIAMENTO}</span></p>'


def _cta(servizio, testo='Aderisci all’Offerta'):
    return f'<a class="btn btn-primary of-cta" href="#contatti" data-service="{servizio}">{testo} &rarr;</a>'


def card_fv(o):
    tot, rata = detrazione(o['imponibile'])
    incl = ''.join(f'<li>{ico("check", "of-ck")}{esc(x)}</li>' for x in INCLUSO_FV)
    return f'''<article class="of-card of-fv{' of-top' if o['evidenza'] else ''}" id="{o['id']}">
  <div class="of-head">{ico('sun', 'of-ico of-ico-sun')}<span class="of-badge">{esc(o['badge'])}</span></div>
  <h3>{esc(o['titolo'])}</h3>
  <p class="of-intro">{esc(o['intro'])}</p>
  <p class="of-desc">Impianto fotovoltaico &laquo;chiavi in mano&raquo;.</p>
  <ul class="of-incl">{incl}</ul>
  <div class="of-price"><span class="of-label">Prezzo</span><b>{esc(o['prezzo'])}</b></div>
  <div class="of-detr">
    <span class="of-detr-t">Detrazione fiscale {DETRAZIONE_PERCENTUALE:.0f}%</span>
    <b>{euro(tot)}</b>
    <small>da detrarre, in {DETRAZIONE_ANNI} quote annuali da {euro(rata)}</small>
  </div>
  {_fin()}
  {_cta('Fotovoltaico domestico')}
</article>'''


def card_altra(o):
    righe = ''.join(f'<li><span>{esc(a)}</span><b>{esc(b)}</b></li>' for a, b in o['prezzi'])
    nota = f'<small class="of-pnota">{esc(o["nota_prezzo"])}</small>' if o['nota_prezzo'] else ''
    return f'''<article class="of-card of-alt" id="{o['id']}">
  <div class="of-head">{ico(o['icona'])}<span class="of-badge">{esc(o['badge'])}</span></div>
  <h3>{esc(o['titolo'])}</h3>
  <p class="of-desc">{esc(o['testo'])}</p>
  <div class="of-price"><span class="of-label">Prezzo</span><ul class="of-plist">{righe}</ul>{nota}</div>
  {_fin()}
  {_cta(o['servizio'])}
</article>'''


def sezioni(p):
    fv = ''.join(card_fv(o) for o in FOTOVOLTAICO)
    alt = ''.join(card_altra(o) for o in ALTRE)
    van = ''.join(f'<li class="fv-card"><h3>{esc(t)}</h3><p>{esc(x)}</p></li>' for t, x in VANTAGGI)
    return f'''<section class="sec of-sec" id="fotovoltaico-accumulo">
  {C.sec_head('Energia dal sole, chiavi in mano', 'Fotovoltaico con accumulo', 'Tre configurazioni complete, dalla progettazione alle pratiche GSE: scegli quella più adatta ai tuoi consumi. Il prezzo è chiaro e la detrazione fiscale già calcolata.')}
  <div class="of-grid">{fv}</div>
  <p class="of-note">Detrazione calcolata al {DETRAZIONE_PERCENTUALE:.0f}% sul prezzo comprensivo di IVA al {IVA_FV_PERCENTUALE:.0f}%, ripartita in {DETRAZIONE_ANNI} quote annuali. È prevista per l&rsquo;abitazione principale e dipende dalla normativa vigente e dai requisiti del singolo intervento: verifichiamo insieme la tua situazione.</p>
</section>

<section class="sec of-sec of-sec2" id="comfort-manutenzione">
  {C.sec_head('Comfort e manutenzione', 'Vivi meglio la tua casa, tutto l&rsquo;anno', 'Climatizzazione, riscaldamento efficiente e un impianto fotovoltaico sempre in forma: soluzioni complete, installate da tecnici qualificati.')}
  <div class="of-grid">{alt}</div>
</section>

<section class="sec of-finband" id="finanziamento">
  <div class="of-finband-in">
    <div>
      <span class="eyebrow">Finanziamento agevolato</span>
      <h2>Investi oggi, distribuisci la spesa nel tempo</h2>
      <p>Per tutte le soluzioni di questa pagina è possibile richiedere un finanziamento a tasso agevolato: avvii subito il tuo impianto e dilazioni l&rsquo;investimento, anche insieme alla detrazione fiscale. Le condizioni dipendono dalla valutazione della società finanziaria.</p>
    </div>
    <a class="btn btn-light" href="#contatti" data-service="Fotovoltaico domestico">Chiedi un preventivo con finanziamento &rarr;</a>
  </div>
</section>

<section class="sec of-why" id="perche-ora">
  {C.sec_head('Perché adesso', 'Efficienza energetica: un investimento che lavora per te', 'Il costo dell&rsquo;energia può cambiare nel tempo. Un impianto efficiente ti rende meno dipendente da questa variabile.')}
  <ul class="fv-cards c4">{van}</ul>
</section>

<section class="sec of-close">
  <h2>Pronto a scegliere la tua offerta?</h2>
  <p>Un tecnico ti ascolta, valuta la tua situazione e ti propone la soluzione giusta. Il primo passo è una telefonata o un messaggio.</p>
  <div class="cta">{C.cta_pair('offerte')}</div>
  <p class="of-legal">Prezzi di listino dell&rsquo;offerta in corso. Disponibilità, condizioni e requisiti degli incentivi e dei finanziamenti vanno verificati per il singolo intervento.</p>
</section>'''
