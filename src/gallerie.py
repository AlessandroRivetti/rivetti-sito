"""Dati e regole di pubblicazione della «GALLERIA LAVORI» (fotografie REALI di interventi eseguiti).

Come si usa
-----------
1. Metti le fotografie vere in assets/gallerie/privati/, assets/gallerie/imprese/ o assets/gallerie/pa/.
2. Aggiungi una voce alla lista della macroarea in FOTO (modello in fondo).
3. Imposta 'pubblicato': True e 'reale': True solo per fotografie vere di lavori effettivamente eseguiti.
4. Facoltativo, dal computer: python3 prepara-foto.py  (crea le versioni leggere JPG/WebP).
5. Rigenera il sito: python3 src/build.py

Regole (applicate da build.py, non dall'HTML):
- la sezione «Alcuni dei nostri lavori» compare SOLO se la macroarea ha almeno MIN_FOTO_GALLERIA fotografie pubblicate;
  sotto soglia non esiste né la sezione né segnaposto o foto di prova. NON c'è nessun chip tra i pulsanti dei servizi;
- una foto è «pubblicata» solo con 'pubblicato' esattamente True; se è pubblicata ma incompleta (file mancante,
  testo alternativo «alt» assente, manca la conferma 'reale': True) la build SI FERMA con un messaggio chiaro;
- le immagini generate con IA NON possono stare nella galleria: servono 'reale': True e non deve esserci 'ia': True;
- cliente, indirizzo, località e potenza non compaiono mai a meno che siano compilati E autorizzati
  ('mostra_localita': True, 'mostra_potenza': True, 'cliente_autorizzato': True, 'mostra_indirizzo': True);
- si mostrano al massimo MAX_FOTO_GALLERIA fotografie per macroarea, in ordine di 'ordine'.
La galleria NON sostituisce la pagina Realizzazioni (progetti con scheda tecnica completa): vedi progetti.py.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------- impostazioni
MIN_FOTO_GALLERIA = 3     # sotto questa soglia la galleria di quella macroarea non esiste (nessuna sezione)
MAX_FOTO_GALLERIA = 6     # foto mostrate al massimo per macroarea (nessun «Vedi tutti» per ora)
STRICT = True             # controlla che i file esistano; solo la modalità --demo usa dati di prova
MACROAREE = {'privati': 'Privati', 'imprese': 'Imprese', 'pa': 'Pubblica Amministrazione'}
SEZIONE_ID = 'galleria-lavori'
TITOLO = 'Alcuni dei nostri lavori'
TESTO = 'Una selezione di interventi realizzati da Rivetti Impianti.'

DIR = os.path.join(ROOT, 'assets', 'gallerie')   # la modalità --demo lo sposta in _demo/
BASE = 'assets/gallerie/'                          # percorso usato nell'HTML


class ErroreGalleria(Exception):
    pass


# ---------------------------------------------------------------------------- DATI
# Una lista per macroarea. Il campo 'file' è il nome del file dentro assets/gallerie/<macroarea>/.
FOTO = {'privati': [], 'imprese': [], 'pa': []}

# MODELLO (copia, compila e aggiungi nella lista della macroarea; i campi facoltativi si possono togliere):
#
#   {
#       'file': 'impianto-fotovoltaico-01.jpg',                       # in assets/gallerie/privati/
#       'alt': 'Impianto fotovoltaico installato su copertura residenziale',   # OBBLIGATORIO: descrive ciò che si vede
#       'titolo': 'Impianto fotovoltaico residenziale',               # facoltativo (mostrato sotto la miniatura e nel visualizzatore)
#       'descrizione': 'Breve descrizione.',                          # facoltativa (solo nel visualizzatore)
#       'categoria': 'Fotovoltaico',                                  # facoltativa (servizio)
#       'ordine': 10,                                                 # facoltativo: numeri bassi prima
#       'reale': True,                                                # OBBLIGATORIO: conferma che è una foto vera di un lavoro eseguito
#       'pubblicato': True,                                           # True = visibile; qualsiasi altro valore = invisibile
#       # --- dati riservati: compaiono SOLO se compilati E autorizzati ---
#       'localita': 'Comune (PR)', 'mostra_localita': True,
#       'potenza': '6 kWp', 'mostra_potenza': True,
#       'cliente': 'Nome', 'cliente_autorizzato': True,
#       'indirizzo': 'Via ...', 'mostra_indirizzo': True,
#   },


def _percorso(area, rel):
    return os.path.join(DIR, area, rel)


def errori(area, f, i):
    sid = f'{area}[{i}] «{f.get("file") or "?"}»'
    e = []
    if not str(f.get('file') or '').strip():
        e.append(f'{sid}: file mancante')
    elif not re.fullmatch(r'[A-Za-z0-9._-]+\.(jpe?g|png)', f['file'], re.I):
        e.append(f'{sid}: nome file non valido (solo lettere, numeri, punto, trattino; estensione jpg/png)')
    elif re.search(r'-(480|800|1200|1600)\.', f['file']):
        e.append(f'{sid}: indica il file originale, non una versione leggera (-480, -800, -1200, -1600)')
    elif STRICT and not os.path.isfile(_percorso(area, f['file'])):
        e.append(f'{sid}: file non trovato in assets/gallerie/{area}/{f["file"]}')
    if not str(f.get('alt') or '').strip():
        e.append(f'{sid}: testo alternativo («alt») obbligatorio')
    if f.get('reale') is not True:
        e.append(f'{sid}: serve la conferma "reale": True (nella galleria ci sono solo fotografie vere di lavori eseguiti)')
    if f.get('ia'):
        e.append(f'{sid}: le immagini generate con IA non possono comparire nella Galleria lavori')
    if f.get('ordine') is not None and not isinstance(f['ordine'], (int, float)):
        e.append(f'{sid}: «ordine» deve essere un numero')
    return e


def pubblicate(area):
    """Foto pubblicate (pubblicato esattamente True) e valide, in ordine. Se una è incompleta la build si ferma."""
    out, viste, err = [], set(), []
    for i, f in enumerate(FOTO.get(area, [])):
        if f.get('pubblicato') is not True:
            continue
        e = errori(area, f, i)
        if f.get('file') in viste:
            e.append(f'{area}[{i}]: file duplicato «{f.get("file")}»')
        viste.add(f.get('file'))
        err += e
        out.append((f.get('ordine') if f.get('ordine') is not None else 10**6, i, f))
    if err:
        raise ErroreGalleria('; '.join(err))
    return [f for _, _, f in sorted(out, key=lambda t: (t[0], t[1]))]


def attiva(area):
    return len(pubblicate(area)) >= MIN_FOTO_GALLERIA


def mostrate(area):
    """Foto mostrate nella galleria: nessuna se sotto soglia, altrimenti al massimo MAX_FOTO_GALLERIA."""
    return pubblicate(area)[:MAX_FOTO_GALLERIA] if attiva(area) else []


def riservati(f):
    """Etichette riservate mostrabili: solo se compilate E autorizzate."""
    v = []
    if f.get('localita') and f.get('mostra_localita') is True:
        v.append(('Località', f['localita']))
    if f.get('indirizzo') and f.get('mostra_indirizzo') is True:
        v.append(('Indirizzo', f['indirizzo']))
    if f.get('potenza') and f.get('mostra_potenza') is True:
        v.append(('Potenza', f['potenza']))
    if f.get('cliente') and f.get('cliente_autorizzato') is True:
        v.append(('Cliente', f['cliente']))
    return v


def avvisi():
    a = []
    for area, nome in MACROAREE.items():
        n = len(pubblicate(area))
        if 0 < n < MIN_FOTO_GALLERIA:
            a.append(f'Galleria lavori {nome}: {n} foto pubblicate, ne servono almeno {MIN_FOTO_GALLERIA}: la sezione resta NON pubblicata.')
        if n > MAX_FOTO_GALLERIA:
            a.append(f'Galleria lavori {nome}: {n} foto pubblicate, ne vengono mostrate {MAX_FOTO_GALLERIA}.')
    return a
