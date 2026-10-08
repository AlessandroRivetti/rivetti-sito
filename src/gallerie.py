import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MIN_FOTO_GALLERIA = 1
MAX_FOTO_GALLERIA = 6
STRICT = True
MACROAREE = {'privati': 'Privati', 'imprese': 'Imprese', 'pa': 'Pubblica Amministrazione'}
SEZIONE_ID = 'galleria-lavori'
TITOLO = 'Alcuni dei nostri lavori'
TESTO = 'Una selezione di interventi realizzati da Rivetti Impianti.'

DIR = os.path.join(ROOT, 'assets', 'gallerie')
BASE = 'assets/gallerie/'


class ErroreGalleria(Exception):
    pass


FOTO = {
    'privati': [
        {
            'file': 'RESIDENZIALE.png',
            'alt': 'Installazione impianto fotovoltaico residenziale',
            'titolo': 'Impianto Residenziale',
            'descrizione': 'Intervento di installazione residenziale.',
            'reale': True,
            'pubblicato': True,
        },
    ],
    'imprese': [
        {
            'file': 'INDUSTRIALE.png',
            'alt': 'Installazione impianto fotovoltaico industriale',
            'titolo': 'Impianto Industriale',
            'descrizione': 'Intervento di installazione industriale.',
            'reale': True,
            'pubblicato': True,
        },
    ],
    'pa': [
        {
            'file': 'PA.png',
            'alt': 'Installazione impianto per la Pubblica Amministrazione',
            'titolo': 'Intervento Pubblica Amministrazione',
            'descrizione': 'Intervento presso struttura pubblica.',
            'reale': True,
            'pubblicato': True,
        },
    ]
}


def _percorso(area, rel):
    return os.path.join(DIR, area, rel)


def errori(area, f, i):
    sid = f'{area}[{i}] «{f.get("file") or "?"}»'
    e = []
    if not str(f.get('file') or '').strip():
        e.append(f'{sid}: file mancante')
    elif not re.fullmatch(r'[A-Za-z0-9._-]+\.(jpe?g|png)', f['file'], re.I):
        e.append(f'{sid}: nome file non valido')
    elif STRICT and not os.path.isfile(_percorso(area, f['file'])):
        e.append(f'{sid}: file non trovato in assets/gallerie/{area}/{f["file"]}')
    if not str(f.get('alt') or '').strip():
        e.append(f'{sid}: testo alternativo («alt») obbligatorio')
    if f.get('reale') is not True:
        e.append(f'{sid}: serve la conferma "reale": True')
    return e


def pubblicate(area):
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
    return pubblicate(area)[:MAX_FOTO_GALLERIA] if attiva(area) else []


def riservati(f):
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
            a.append(f'Galleria lavori {nome}: {n} foto pubblicate, ne servono almeno {MIN_FOTO_GALLERIA}')
    return a