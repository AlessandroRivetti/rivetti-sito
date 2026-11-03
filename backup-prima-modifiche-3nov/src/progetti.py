"""Dati e regole di pubblicazione delle REALIZZAZIONI (progetti reali).

Come si usa
-----------
1. Aggiungi un blocco alla lista PROGETTI (modello commentato in fondo).
2. Metti le foto in assets/realizzazioni/<slug>/ (vedi LEGGIMI.txt in quella cartella).
3. Imposta 'pubblicato': True solo quando il progetto è stato approvato.
4. Rigenera il sito: python3 src/build.py

Regole (sono applicate da build.py, non dipendono dall'HTML):
- un progetto con 'pubblicato' diverso da True NON produce nessun output: né pagina, né scheda, né Home,
  né sitemap, né dati strutturati, né link interni; eventuali file di prove precedenti vengono cancellati;
- un progetto pubblicato ma incompleto (titolo, categoria, descrizione, foto principale con testo alternativo...)
  FERMA la build con un messaggio chiaro: non viene mai pubblicato "a metà" né con immagini finte;
- la pagina Realizzazioni, la voce di menu/footer e le pagine di dettaglio compaiono solo quando i progetti
  pubblicati sono almeno MIN_PROGETTI;
- il blocco "Alcuni dei nostri progetti" in Home resta spento finché HOME_ATTIVA è False e non ci sono
  HOME_N progetti con 'in_evidenza': True;
- tutti i dati riservati (cliente, località, importi...) sono facoltativi e non producono etichette vuote.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------- impostazioni
MIN_PROGETTI = 3          # sotto questa soglia Realizzazioni non viene pubblicata (pagina, menu, footer, sitemap)
HOME_ATTIVA = False       # True = mostra "Alcuni dei nostri progetti" in Home (servono HOME_N progetti in evidenza)
HOME_N = 3
STRICT = True             # controlla che le foto esistano; solo la modalità --demo lo disattiva

# ---------------------------------------------------------------------------- vocabolari
# Categoria (etichetta mostrata) -> tipologia usata dai filtri (None = nessun filtro per tipologia)
CATEGORIE = {
    'fotovoltaico-residenziale': ('Fotovoltaico residenziale', 'fotovoltaico'),
    'fotovoltaico-industriale': ('Fotovoltaico industriale', 'fotovoltaico'),
    'utility-scale': ('Utility Scale', 'utility-scale'),
    'om': ('Operation & Maintenance', 'om'),
    'pubblica-amministrazione': ('Pubblica Amministrazione', None),
    'climatizzazione': ('Climatizzazione / impianti termici', 'termoidraulica'),
    'cer': ('Comunità Energetiche / progetti energetici', 'cer'),
    'altri-interventi': ('Altri interventi tecnici', None),
}
# Filtro per tipologia (etichetta); una scheda può averne più di una con il campo facoltativo 'tipologie'
TIPOLOGIE = {
    'fotovoltaico': 'Fotovoltaico', 'utility-scale': 'Utility Scale', 'om': 'O&M',
    'termoidraulica': 'Termoidraulica / climatizzazione', 'cer': 'CER',
}
CLIENTI = {'privati': 'Privati', 'imprese': 'Imprese', 'pa': 'Pubblica Amministrazione'}
TIPO_FORM = {'privati': 'Privato', 'imprese': 'Impresa', 'pa': 'Pubblica Amministrazione'}   # valore del modulo

# ---------------------------------------------------------------------------- DATI
PROGETTI = []

# MODELLO (copia, compila e aggiungi sopra; i campi facoltativi si possono togliere):
#
#   {
#       'id': 'RI-001',                       # codice interno univoco
#       'slug': 'nome-breve-senza-spazi',     # per l'indirizzo: progetto-<slug>.html (minuscole, numeri, trattini)
#       'titolo': 'Titolo del progetto',
#       'categoria': 'fotovoltaico-industriale',   # una chiave di CATEGORIE
#       'cliente_tipo': 'imprese',            # privati | imprese | pa
#       'anno': 2024,                         # facoltativo
#       'potenza': '120 kWp',                 # facoltativo, solo se applicabile e verificata
#       'intervento': 'Nuovo impianto',       # facoltativo: tipologia di intervento (Nuovo impianto, Ampliamento, Revamping...)
#       'stato': 'Completato',                # facoltativo: Completato / In corso...
#       'descrizione': 'Breve descrizione (una o due frasi).',
#       'descrizione_estesa': ['Paragrafo 1', 'Paragrafo 2'],   # facoltativo
#       'attivita': ['Sopralluogo', 'Progettazione', 'Installazione'],   # elenco di "Il nostro intervento"
#       'dati_tecnici': [('Moduli', '300 da 550 W'), ('Inverter', '2')],  # facoltativo (etichetta, valore)
#       'tipologie': ['fotovoltaico', 'om'],  # facoltativo: per i filtri; se manca si ricava dalla categoria
#       'immagine': {'file': 'nome-breve/principale.jpg', 'alt': 'Descrizione reale della foto'},
#       'galleria': [{'file': 'nome-breve/02.jpg', 'alt': 'Descrizione', 'didascalia': 'facoltativa'}],
#       # --- dati riservati: compaiono SOLO se compilati E autorizzati ---
#       'localita': 'Comune (PR)', 'mostra_localita': True,
#       'cliente': 'Nome del cliente', 'cliente_autorizzato': True,
#       'pubblicato': True,                   # True = visibile; qualsiasi altro valore = invisibile ovunque
#       'in_evidenza': False,                 # True = candidato al blocco in Home
#   },


# ---------------------------------------------------------------------------- logica
class ErroreProgetto(Exception):
    pass


FOTO_DIR = os.path.join(ROOT, 'assets', 'realizzazioni')   # la modalità --demo lo sposta in _demo/


def _file_ok(rel):
    return os.path.isfile(os.path.join(FOTO_DIR, rel))


def errori(p):
    """Elenco dei problemi che impediscono di pubblicare un progetto."""
    e = []
    sid = p.get('id') or p.get('slug') or '?'
    for k in ('id', 'slug', 'titolo', 'categoria', 'cliente_tipo', 'descrizione'):
        if not str(p.get(k) or '').strip():
            e.append(f'{sid}: campo obbligatorio mancante «{k}»')
    if p.get('slug') and not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', p['slug']):
        e.append(f'{sid}: slug non valido (solo minuscole, numeri e trattini)')
    if p.get('categoria') and p['categoria'] not in CATEGORIE:
        e.append(f'{sid}: categoria sconosciuta «{p["categoria"]}»')
    if p.get('cliente_tipo') and p['cliente_tipo'] not in CLIENTI:
        e.append(f'{sid}: cliente_tipo deve essere privati, imprese o pa')
    for t in p.get('tipologie', []) or []:
        if t not in TIPOLOGIE:
            e.append(f'{sid}: tipologia sconosciuta «{t}»')
    if p.get('anno') is not None and not (isinstance(p['anno'], int) and 1990 <= p['anno'] <= 2100):
        e.append(f'{sid}: anno non valido')
    imm = p.get('immagine') or {}
    immagini = [('immagine', imm)] + [(f'galleria[{i}]', g) for i, g in enumerate(p.get('galleria') or [])]
    if not imm:
        e.append(f'{sid}: manca la foto principale («immagine»)')
    for nome, g in immagini:
        if not g:
            continue
        if not str(g.get('alt') or '').strip():
            e.append(f'{sid}: {nome} senza testo alternativo («alt»)')
        if not g.get('file'):
            e.append(f'{sid}: {nome} senza file')
        elif STRICT and not _file_ok(g['file']):
            e.append(f'{sid}: {nome} file non trovato in assets/realizzazioni/{g["file"]}')
    return e


def tutti():
    return list(PROGETTI)


def pubblicati():
    """Solo i progetti con pubblicato esattamente True. Se uno è incompleto la build si ferma."""
    out, vistiSlug, vistiId = [], set(), set()
    for p in PROGETTI:
        if p.get('pubblicato') is not True:
            continue
        err = errori(p)
        if p.get('slug') in vistiSlug:
            err.append(f'{p.get("id")}: slug duplicato «{p.get("slug")}»')
        if p.get('id') in vistiId:
            err.append(f'{p.get("id")}: id duplicato')
        if err:
            raise ErroreProgetto('Progetto pubblicato ma non valido:\n - ' + '\n - '.join(err))
        vistiSlug.add(p['slug']); vistiId.add(p['id'])
        out.append(p)
    return out


def attivi():
    """Progetti effettivamente mostrati: tutti i pubblicati se ne esistono almeno MIN_PROGETTI, altrimenti nessuno."""
    pub = pubblicati()
    return pub if len(pub) >= MIN_PROGETTI else []


def in_evidenza():
    ev = [p for p in attivi() if p.get('in_evidenza') is True]
    return ev[:HOME_N] if (HOME_ATTIVA and len(ev) >= HOME_N) else []


def tipologie_di(p):
    t = list(p.get('tipologie') or [])
    base = CATEGORIE[p['categoria']][1]
    if base and base not in t:
        t.insert(0, base)
    return t


def avvisi():
    """Messaggi informativi per chi lancia la build (non bloccanti)."""
    a = []
    n = len(pubblicati())
    if 0 < n < MIN_PROGETTI:
        a.append(f'{n} progetti pubblicati ma la soglia è {MIN_PROGETTI}: la sezione Realizzazioni resta NON pubblicata.')
    if HOME_ATTIVA and attivi() and len([p for p in attivi() if p.get('in_evidenza') is True]) < HOME_N:
        a.append(f'HOME_ATTIVA ma i progetti «in_evidenza» sono meno di {HOME_N}: il blocco in Home resta spento.')
    non_pub = len([p for p in PROGETTI if p.get('pubblicato') is not True])
    if non_pub:
        a.append(f'{non_pub} progetti in bozza (pubblicato diverso da True): nessun output.')
    return a


def pagina_progetto(p):
    return f'progetto-{p["slug"]}.html'
