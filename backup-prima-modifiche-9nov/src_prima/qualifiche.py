"""Certificazioni e qualifiche aziendali + Tecnologie e marchi utilizzati.

NIENTE di quanto compare qui è pubblicato finché non viene inserito un elemento con 'pubblicato': True.
Non inserire nulla che non sia documentato: ogni voce deve poter essere verificata (documento, ente, numero).

Modifiche: aggiungi i blocchi alle liste, metti i file in assets/certificazioni/ (loghi e documenti, vedi LEGGIMI.txt),
poi python3 src/build.py. Le sezioni sono già pronte nei componenti di comp.py ma non sono inserite in nessuna pagina
finché non viene deciso dove mostrarle (punto di aggancio previsto: blocco "Chi siamo" della Home).
"""

ATTIVA = False      # interruttore generale delle sezioni Qualifiche e Marchi (False = non vengono mai prodotte)

# ------------------------------------------------------------------ CERTIFICAZIONI E QUALIFICHE
QUALIFICHE = []
# MODELLO:
#   {
#       'nome': 'Nome esatto della certificazione/qualifica',
#       'ente': 'Ente che l'ha rilasciata',
#       'numero': 'N. ...',                    # facoltativo
#       'scadenza': '31/12/2027',              # facoltativo (se c'è, va tenuta aggiornata)
#       'logo': 'nome-file.png',               # facoltativo, in assets/certificazioni/ (con 'logo_alt')
#       'logo_alt': 'Logo di ...',
#       'documento': 'nome-file.pdf',          # facoltativo, in assets/certificazioni/ (copia pubblicabile)
#       'descrizione': 'Che cosa attesta, in una frase.',
#       'pubblicato': True,
#   },

# ------------------------------------------------------------------ TECNOLOGIE E MARCHI UTILIZZATI
MARCHI = []
# MODELLO (i loghi e i riferimenti commerciali si decidono caso per caso):
#   {
#       'nome': 'Nome del produttore',
#       'categoria': 'Moduli fotovoltaici',    # Moduli, Inverter, Accumulo, Climatizzazione, Monitoraggio...
#       'descrizione': 'facoltativa',
#       'url': 'https://...',                  # facoltativo
#       'mostra_logo': False,                  # True SOLO dopo decisione esplicita; senza, compare il nome in testo
#       'logo': 'nome-file.svg', 'logo_alt': 'Logo di ...',
#       'pubblicato': True,
#   },


def qualifiche_pubblicate():
    return [q for q in QUALIFICHE if ATTIVA and q.get('pubblicato') is True and q.get('nome') and q.get('ente')]


def marchi_pubblicati():
    return [m for m in MARCHI if ATTIVA and m.get('pubblicato') is True and m.get('nome')]
