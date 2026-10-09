# -*- coding: utf-8 -*-
"""
DATI CENTRALI DEL SITO RIVETTI IMPIANTI
=======================================
Qui si modificano i contenuti ripetuti del sito: dati societari, contatti, servizi,
incentivi, FAQ, numeri, realizzazioni. Dopo ogni modifica si rigenerano le pagine con:

    python3 src/build.py

REGOLE
- Nessun dato inventato: se un valore non è verificato, mettilo a None (o lascia vuota la lista):
  l'elemento corrispondente NON viene pubblicato e il sito resta pulito.
- Le recensioni NON stanno qui: restano in recensioni.js (approvazione manuale).
"""

# ----------------------------------------------------------------------------- SITO
SITO = {
    # Indirizzo pubblico del sito (serve a canonical, Open Graph e sitemap).
    # DA CONFERMARE: dominio definitivo e se si usa "www" oppure no. Si cambia solo qui.
    'url': 'https://www.rivettiimpianti.it',
    'nome': 'Rivetti Impianti',
    'nome_esteso': 'Rivetti Impianti — Technical Engineering',
    'slogan': 'Dal 2008, impianti energetici e servizi tecnici',
    'anno_inizio': 2008,
    'logo_chiaro': 'assets/logo-rivetti-dark.png',   # logo con sfondo trasparente (usato su fondo blu)
    'logo_og': 'assets/logo-rivetti.png',            # immagine di anteprima per i social
}

# ----------------------------------------------------------------------------- SOCIETÀ
SOCIETA = {
    'ragione_sociale': 'RM IMPIANTI DI ALESSANDRO RIVETTI S.A.S.',
    'ragione_sociale_breve': 'RM Impianti di Alessandro Rivetti S.a.s.',
    'piva_cf': '03428210615',
    'rea': 'CE-243308',
    'via': 'Via Landolfo',
    'cap': '81034',
    'comune': 'Mondragone',
    'provincia': 'CE',
    'regione': 'Campania',
    'fondatore': 'Michele Rivetti',
    'email': 'rivettiimpianti@gmail.com',
    'pec': 'rmimpiantisas@pec.it',
}

# ----------------------------------------------------------------------------- CONTATTI
# I numeri sono lasciati esattamente come sono. L'ordine è quello di visualizzazione.
# Il PRIMO è il numero principale: compare sempre per primo (schede, footer, dati strutturati) ed è
# quello usato dai link "Chiama" principali e dal WhatsApp "Parla con un tecnico".
TELEFONI = ['327 878 1998', '353 343 7800', '330 348 700']
TELEFONO_PRINCIPALE = TELEFONI[0]

WHATSAPP = {
    'numero': TELEFONI[0],   # numero principale dei pulsanti "Parla con un tecnico"
    'testo': 'Salve, ho visitato il vostro sito e avrei bisogno di informazioni, grazie.',
    # messaggio precompilato per pagina (se una pagina non è elencata, si usa 'testo')
    'testi_pagina': {
        'privati': 'Salve, ho visitato il vostro sito e vorrei informazioni su un impianto per la mia abitazione, grazie.',
        'imprese': 'Buongiorno, vorrei ricevere una valutazione tecnica per un impianto fotovoltaico o un intervento energetico per la mia attività.',
        'pa': 'Salve, ho visitato il vostro sito e vorrei un confronto tecnico per il nostro ente, grazie.',
        'privati_fv': 'Buongiorno, vorrei ricevere informazioni per valutare un impianto fotovoltaico per la mia abitazione.',
        'progetto': 'Salve, ho visto una vostra realizzazione sul sito e vorrei parlare con l’ufficio tecnico, grazie.',
    },
}

# Caselle future (info@, preventivi@, assistenza@): NON usarle finché non sono confermate.

# ----------------------------------------------------------------------------- CTA
CTA_PRIMARIA = 'Richiedi un sopralluogo'
CTA_SECONDARIA = 'Parla con un tecnico'
# Pagine con CTA dedicate (chiave pagina: (principale, secondaria)); le altre usano quelle sopra.
CTA_PAGINE = {
    'imprese': ('Richiedi una valutazione tecnica', 'Parla con il nostro ufficio tecnico'),
    'pa': ('Richiedi un confronto tecnico', 'Parla con il nostro ufficio tecnico'),
    'progetto': ('Richiedi una valutazione tecnica', 'Parla con il nostro ufficio tecnico'),   # pagine di dettaglio delle realizzazioni
}

# ----------------------------------------------------------------------------- NUMERI
# "valore": testo mostrato in grande. None = indicatore NON pubblicato.
# "auto" (solo per l'esperienza) = anno corrente - anno di inizio attività, calcolato a ogni build.
NUMERI = {
    'eyebrow': 'Rivetti Impianti',
    'titolo': 'Esperienza costruita sul campo',
    'voci': [
        {'id': 'clienti', 'valore': '1.000+', 'etichetta': 'Clienti',
         'descrizione': 'Privati, imprese ed enti che hanno scelto Rivetti Impianti.'},
        # DA COMPLETARE quando avrai il dato verificato (es. '120', con la sua descrizione):
        {'id': 'lavori', 'valore': None, 'etichetta': 'Impianti realizzati',
         'descrizione': 'Lavori portati a termine per privati, imprese e Pubblica Amministrazione.'},
        # DA COMPLETARE solo con un dato dimostrabile. Etichette possibili, a seconda del dato:
        #   'Energia rinnovabile prodotta ogni anno'   (se il dato è una produzione annua stimata/misurata)
        #   'Energia prodotta dagli impianti realizzati' (se il dato è cumulato)
        {'id': 'energia', 'valore': None, 'etichetta': 'Energia rinnovabile prodotta ogni anno',
         'descrizione': ''},
        {'id': 'esperienza', 'valore': 'Dal 2008', 'etichetta': 'Esperienza nel settore',
         'descrizione': ''},
    ],
}

# ----------------------------------------------------------------------------- SERVIZI
# art = illustrazione SVG (decorativa); foto = file opzionale in assets/servizi/ (se esiste viene mostrato
# al posto dell'illustrazione, con il testo alternativo indicato); opzione = voce nel modulo di contatto.
SERVIZI_PRIVATI = [
    {'id': 'fotovoltaico', 'titolo': 'Impianti fotovoltaici', 'tag': 'Produzione e autoconsumo', 'principale': True,
     'testo': 'Progettazione e installazione su misura.',
     'serve': 'Produce energia elettrica dalla luce del sole direttamente sulla tua abitazione, per alimentare i consumi di casa.',
     'esigenza': 'Avere un impianto pensato sulle tue abitudini di consumo, sulla copertura e sulle caratteristiche dell’edificio, e non una soluzione standard uguale per tutti.',
     'sistema': 'È il cuore del sistema energetico della casa: può essere abbinato a un sistema di accumulo e alla climatizzazione, per utilizzare al meglio l’energia prodotta.',
     'passi': [
         ('Analisi delle esigenze', 'Partiamo da consumi, abitudini e caratteristiche dell’abitazione.'),
         ('Progettazione', 'Definiamo l’impianto sulla base di quanto emerso dal sopralluogo.'),
         ('Installazione', 'Realizziamo l’impianto secondo il progetto concordato.'),
         ('Configurazione', 'Mettiamo in servizio e configuriamo l’impianto per un funzionamento corretto.'),
         ('Integrazione', 'Quando opportuno, lo coordiniamo con accumulo e altri sistemi energetici.'),
         ('Assistenza', 'Restiamo a disposizione anche dopo la realizzazione.'),
     ],
     'art': 'fv', 'foto': 'fotovoltaico-domestico.jpg', 'foto_alt': 'Impianto fotovoltaico domestico',
     'opzione': 'Fotovoltaico domestico'},
    {'id': 'accumulo', 'titolo': 'Sistemi di accumulo', 'tag': 'Produzione e autoconsumo',
     'testo': "Uso serale dell'energia prodotta.",
     'serve': 'Conserva parte dell’energia prodotta dall’impianto fotovoltaico per renderla disponibile quando serve, ad esempio quando i moduli producono meno.',
     'esigenza': 'Utilizzare in modo più efficace l’energia prodotta dalla tua abitazione, senza dipendere solo dal momento in cui viene generata.',
     'sistema': 'Si collega all’impianto fotovoltaico e fa da “serbatoio” tra ciò che la casa produce e ciò che consuma.',
     'punti': ['Insieme a un nuovo impianto fotovoltaico', 'Come integrazione di un impianto esistente, quando tecnicamente possibile'],
     'art': 'acc', 'foto': 'accumulo.jpg', 'foto_alt': 'Sistema di accumulo',
     'opzione': 'Sistema di accumulo'},
    {'id': 'climatizzazione', 'titolo': 'Climatizzazione e pompe di calore', 'tag': 'Comfort ed efficienza',
     'testo': 'Riscaldamento, pompe di calore, impianti idrosanitari.',
     'serve': 'Raffresca gli ambienti in estate e li riscalda in inverno, anche con pompe di calore: tecnologie che usano l’energia elettrica in modo efficiente.',
     'esigenza': 'Avere comfort tutto l’anno con un impianto correttamente progettato e dimensionato sugli ambienti da servire.',
     'sistema': 'Alimentata a energia elettrica, la climatizzazione può essere integrata con la produzione dell’impianto fotovoltaico.',
     'punti': ['Comfort in estate e in inverno', 'Pompe di calore', 'Corretta progettazione e dimensionamento', 'Integrazione con la produzione fotovoltaica'],
     'art': 'clima', 'foto': 'termoidraulica-climatizzazione.jpg', 'foto_alt': 'Climatizzazione e pompe di calore',
     'opzione': 'Termoidraulica e Climatizzazione'},
    {'id': 'solare-termico', 'titolo': 'Solare termico', 'tag': 'Comfort ed efficienza',
     'testo': 'Acqua calda sanitaria dall’energia solare.',
     'serve': 'Sfrutta l’energia solare per la produzione di acqua calda sanitaria.',
     'esigenza': 'Produrre l’acqua calda di casa anche con una fonte rinnovabile, in funzione della configurazione dell’impianto.',
     'sistema': 'Si affianca all’impianto termico dell’abitazione e, a seconda di come è configurato, può contribuire all’efficienza energetica complessiva. La soluzione adatta si valuta caso per caso.',
     'art': 'solterm', 'foto': 'solare-termico.jpg', 'foto_alt': 'Impianto solare termico',
     'opzione': 'Solare termico'},
    {'id': 'manutenzione', 'titolo': 'Manutenzione impianti fotovoltaici', 'tag': 'Controllo nel tempo',
     'testo': 'Verifiche su inverter, collegamenti e sicurezza.',
     'serve': 'Verifica lo stato dell’impianto e dei suoi componenti e interviene quando serve, per mantenerlo correttamente funzionante.',
     'esigenza': 'Non lasciare l’impianto senza controlli: possiamo seguire anche impianti già installati, non solo quelli nuovi.',
     'sistema': 'È l’attività che mantiene efficiente nel tempo il resto del sistema.',
     'punti': ['Controlli e manutenzione ordinaria e straordinaria', 'Verifica dello stato dei componenti, inverter e collegamenti compresi', 'Individuazione di eventuali anomalie', 'Attività necessarie al corretto funzionamento dell’impianto'],
     'art': 'manut', 'foto': 'manutenzione-inverter.jpg', 'foto_alt': "Manutenzione dell'inverter",
     'opzione': 'Manutenzione ordinaria e straordinaria'},
    {'id': 'lavaggio', 'titolo': 'Lavaggio moduli fotovoltaici', 'tag': 'Controllo nel tempo',
     'testo': 'Pulizia professionale.',
     'serve': 'Rimuove sporco, polvere e depositi dalla superficie dei moduli, come attività di manutenzione dell’impianto.',
     'esigenza': 'Sporco, polvere e depositi possono influire sulle condizioni operative dei moduli: se e quando intervenire dipende dall’impianto e dal contesto in cui si trova.',
     'sistema': 'Rientra nel piano di manutenzione dell’impianto e può essere abbinato a controlli e termografia.',
     'art': 'lav', 'foto': 'lavaggio-pannelli.jpg', 'foto_alt': 'Lavaggio moduli fotovoltaici',
     'opzione': 'Lavaggio moduli fotovoltaici'},
    {'id': 'termografia', 'titolo': 'Termografia impianti fotovoltaici', 'tag': 'Controllo nel tempo',
     'testo': 'Analisi per individuare anomalie e guasti.',
     'serve': 'È un controllo non invasivo: una camera termica mostra le differenze di temperatura su moduli e componenti e permette di individuare eventuali anomalie termiche.',
     'esigenza': 'Avere un’indicazione in più sullo stato dell’impianto, senza smontare nulla, a supporto di manutenzione e verifiche.',
     'sistema': 'È uno strumento di verifica nel controllo nel tempo: l’esito indica dove approfondire con ulteriori controlli.',
     'art': 'termo', 'foto': 'termografia.jpg', 'foto_alt': 'Termografia di un impianto fotovoltaico',
     'opzione': 'Termografia impianti fotovoltaici'},
]

# Pagina Privati: titoli di sezione e blocchi dedicati
PRIVATI_HERO = {
    'h1': 'Energia, comfort ed efficienza per la tua casa',
    'lead': 'Soluzioni integrate per produrre energia, migliorare il comfort e mantenere efficienti gli impianti nel tempo.',
}

SISTEMA_INTEGRATO = {
    'eyebrow': 'Soluzione completa per la casa',
    'titolo': 'Pensiamo al sistema, non al singolo componente',
    'testo': 'Fotovoltaico, accumulo, climatizzazione, solare termico e manutenzione non vanno necessariamente considerati come elementi separati. '
             'Valutiamo la tua abitazione e le tue esigenze per costruire, quando opportuno, una soluzione coordinata.',
    'aree': [
        {'icona': 'sole', 'titolo': 'Produzione e autoconsumo', 'sotto': 'Fotovoltaico e sistemi di accumulo',
         'concetto': 'Produrre energia direttamente dall’abitazione e utilizzare in modo più efficace l’energia prodotta.',
         'link': [('Fotovoltaico', 'fotovoltaico'), ('Accumulo', 'accumulo')]},
        {'icona': 'comfort', 'titolo': 'Comfort ed efficienza', 'sotto': 'Climatizzazione e soluzioni termiche',
         'concetto': 'Gestire riscaldamento, raffrescamento e produzione di acqua calda con tecnologie efficienti e coerenti con il sistema energetico dell’abitazione.',
         'link': [('Climatizzazione', 'climatizzazione'), ('Solare termico', 'solare-termico')]},
        {'icona': 'controllo', 'titolo': 'Controllo nel tempo', 'sotto': 'Manutenzione, lavaggio e termografia',
         'concetto': 'Mantenere l’impianto controllato ed efficiente nel tempo attraverso attività di verifica e manutenzione.',
         'link': [('Manutenzione', 'manutenzione'), ('Lavaggio', 'lavaggio'), ('Termografia', 'termografia')]},
    ],
}

IMPIANTO_ESISTENTE = {
    'id': 'impianto-esistente',
    'eyebrow': 'Per chi ha già un impianto fotovoltaico',
    'titolo': 'Hai già un impianto?',
    'testo': 'Non è necessario che l’impianto sia stato realizzato da Rivetti Impianti. Possiamo valutare anche impianti già esistenti per verificarne lo stato e definire, quando necessario, le attività più appropriate.',
    'voci_intro': 'Possiamo intervenire per:',
    'voci': ['Verifica tecnica', 'Manutenzione', 'Lavaggio moduli', 'Termografia', 'Ricerca di anomalie',
             'Controllo dei principali componenti', 'Valutazione di eventuali interventi di adeguamento',
             'Valutazione di sistemi di accumulo o altre integrazioni, quando tecnicamente possibili'],
    'cta': 'Richiedi una verifica del tuo impianto',
    'servizio': 'Manutenzione ordinaria e straordinaria',
    'whatsapp': 'Buongiorno, possiedo già un impianto fotovoltaico e vorrei ricevere informazioni per una verifica e un eventuale intervento di manutenzione.',
}

SERVIZI_IMPRESE = [
    {'id': 'fotovoltaico-industriale', 'livello': 'principale', 'tag': 'Aziende e attività produttive', 'titolo': 'Fotovoltaico industriale',
     'testo': 'Un impianto industriale deve partire dai consumi dell’azienda, non soltanto dallo spazio disponibile.',
     'frase': 'Dimensionare correttamente significa progettare l’impianto intorno al modo in cui l’azienda utilizza l’energia.',
     'destinatari': ['Aziende', 'Capannoni', 'Attività produttive', 'Strutture commerciali', 'Realtà con consumi energetici significativi'],
     'passi': [
         ('Analisi dei consumi', 'Studiamo come e quando l’attività utilizza energia.'),
         ('Sopralluogo', 'Rileviamo sul posto lo stato dell’edificio e degli impianti.'),
         ('Verifica delle superfici', 'Valutiamo coperture e aree disponibili.'),
         ('Verifica delle caratteristiche elettriche', 'Controlliamo l’impianto elettrico esistente e i punti di connessione.'),
         ('Progettazione', 'Definiamo la soluzione tecnica più adatta.'),
         ('Dimensionamento', 'Calibriamo la potenza sulle esigenze dell’attività.'),
         ('Realizzazione', 'Eseguiamo le lavorazioni nell’ambito delle attività tecniche di nostra competenza e coordiniamo le attività affidate a imprese partner.'),
         ('Configurazione e collaudo', 'Mettiamo in servizio l’impianto e ne verifichiamo il corretto funzionamento.'),
         ('Gestione e manutenzione', 'Programmiamo controlli e interventi per mantenerlo efficiente nel tempo.'),
     ],
     'integrazioni_titolo': 'Quando tecnicamente opportuno, l’impianto può essere integrato con:',
     'integrazioni': ['Sistemi di accumulo', 'Infrastrutture di ricarica', 'Altri sistemi energetici'],
     'art': 'industriale', 'foto': 'fotovoltaico-industriale.jpg', 'foto_alt': 'Impianto fotovoltaico su capannone industriale',
     'opzione': 'Fotovoltaico industriale'},
    {'id': 'utility-scale', 'livello': 'principale', 'tag': 'Impianti a terra e di grande potenza', 'titolo': 'Fotovoltaico Utility Scale',
     'testo': 'Nei grandi impianti, progettazione, esecuzione e gestione devono essere affrontate come parti dello stesso sistema.',
     'punti_intro': 'Rivetti Impianti può intervenire, in funzione della commessa, su:',
     'punti': ['Progettazione', 'Realizzazione', 'Coordinamento delle lavorazioni', 'Componentistica elettrica',
               'Quadri e collegamenti', 'Infrastrutture elettriche', 'Cabine, quando previste', 'Commissioning', 'Manutenzione', 'Attività O&M'],
     'frase': 'Un grande impianto non termina con la messa in esercizio. Da quel momento inizia la fase in cui produzione, disponibilità e manutenzione devono essere controllate nel tempo.',
     'art': 'utility', 'foto': 'utility-scale.jpg', 'foto_alt': 'Parco fotovoltaico Utility Scale',
     'opzione': 'Fotovoltaico Utility Scale'},
    {'id': 'om', 'livello': 'om', 'tag': 'Gestione e manutenzione', 'titolo': 'Operation & Maintenance', 'nav': 'Operation & Maintenance',
     'sottotitolo': 'Produrre energia non basta. Bisogna continuare a produrla bene.',
     'paragrafi': ['Un impianto fotovoltaico lavora ogni giorno e il suo valore dipende anche dalla capacità di mantenere nel tempo condizioni operative adeguate.',
                   'Per questo l’O&M non deve essere considerato un intervento da effettuare soltanto quando compare un guasto.'],
     'frase': 'L’energia che l’impianto non produce è energia che non può essere utilizzata, valorizzata o immessa in rete.',
     'aggiunta': 'Individuare tempestivamente anomalie, degradi o condizioni operative non ottimali permette di programmare gli interventi prima che una criticità possa incidere più a lungo sulla produzione.',
     'proteggere': {
         'titolo': 'Proteggere la produzione significa proteggere l’investimento',
         'paragrafi': ['Su impianti industriali e di grande potenza, anche una condizione apparentemente limitata può interessare una parte della produzione per periodi prolungati se non viene rilevata.',
                       'Monitoraggio, verifiche periodiche e manutenzione permettono di conoscere lo stato dell’impianto nel tempo.'],
         'frase': 'Un impianto che risulta acceso non è necessariamente un impianto che sta producendo come dovrebbe.'},
     'programmato': {
         'titolo': 'Non aspettare il guasto',
         'testo': 'La manutenzione correttiva resta necessaria quando si verifica un problema, ma un servizio O&M efficace deve prevedere anche attività preventive e programmate.',
         'intro': 'Possibili attività:',
         'punti': ['Controlli visivi', 'Verifiche elettriche', 'Controllo inverter', 'Verifica quadri', 'Controllo delle connessioni',
                   'Serraggi, quando previsti', 'Verifiche meccaniche', 'Termografia', 'Lavaggio moduli',
                   'Gestione della vegetazione, dove necessaria', 'Analisi delle anomalie', 'Interventi correttivi'],
         'nota': 'Attività e frequenze vengono definite in funzione della tipologia, della dimensione e delle caratteristiche dell’impianto.',
         'vegetazione': 'Negli impianti a terra, la gestione della vegetazione contribuisce a mantenere accessibilità, condizioni operative e controllo dell’area.'},
     'art': 'om', 'foto': 'om-fotovoltaico.jpg', 'foto_alt': 'Operation & Maintenance di un impianto fotovoltaico',
     'opzione': 'Operation & Maintenance fotovoltaico'},
    {'id': 'lavaggio', 'livello': 'standard', 'tag': 'Manutenzione', 'titolo': 'Lavaggio moduli fotovoltaici', 'nav': 'Lavaggio moduli',
     'titolo_sez': 'La superficie dei moduli fa parte dell’impianto',
     'testo': ['Polvere, depositi e contaminanti possono accumularsi sulla superficie dei moduli e influire sulle condizioni operative dell’impianto.',
               'La necessità del lavaggio deve essere valutata in funzione del sito, delle condizioni ambientali, dell’inclinazione dei moduli e dello stato effettivo dell’impianto.'],
     'forte': 'Il lavaggio non deve essere una routine eseguita senza criterio: deve essere un’attività di manutenzione valutata sulle reali condizioni del campo fotovoltaico.',
     'art': 'lav_az', 'foto': 'lavaggio-azienda.jpg', 'foto_alt': 'Lavaggio moduli fotovoltaici su capannone',
     'opzione': 'Lavaggio moduli fotovoltaici (impresa)'},
    {'id': 'termografia', 'livello': 'standard', 'tag': 'Controllo specialistico', 'titolo': 'Termografia', 'nav': 'Termografia',
     'titolo_sez': 'Vedere ciò che un controllo visivo può non mostrare',
     'testo': ['La termografia consente di analizzare la distribuzione delle temperature e può contribuire all’individuazione di comportamenti anomali su moduli, connessioni, quadri e componenti elettrici.',
               'Integrata in un programma di manutenzione, rappresenta uno strumento utile per approfondire condizioni che potrebbero non essere immediatamente visibili.'],
     'art': 'termo_az', 'foto': 'termografia-azienda.jpg', 'foto_alt': 'Termografia di un campo fotovoltaico',
     'opzione': 'Termografia impianti fotovoltaici (impresa)'},
    {'id': 'agrivoltaico', 'livello': 'standard', 'tag': 'Fotovoltaico e agricoltura', 'titolo': 'Agrivoltaico',
     'testo': ['L’agrivoltaico richiede di progettare produzione energetica e utilizzo agricolo del terreno come elementi dello stesso intervento.',
               'Configurazione, strutture e caratteristiche dell’impianto devono essere valutate in relazione all’attività agricola, al sito e alla normativa applicabile.'],
     'art': 'agri', 'foto': 'agrivoltaico.jpg', 'foto_alt': 'Impianto agrivoltaico',
     'opzione': 'Agrivoltaico'},
    {'id': 'cer', 'livello': 'standard', 'tag': 'Condivisione dell’energia', 'titolo': 'Comunità Energetiche Rinnovabili', 'nav': 'Comunità Energetiche (CER)',
     'testo': ['Le imprese possono valutare la partecipazione a configurazioni di condivisione dell’energia quando sussistono i requisiti previsti.',
               'Rivetti Impianti può supportare gli aspetti tecnici ed energetici legati agli impianti e alla configurazione del progetto.'],
     'art': 'cer', 'foto': 'cer.jpg', 'foto_alt': 'Comunità energetica rinnovabile',
     'opzione': 'Comunità Energetiche Rinnovabili'},
    {'id': 'efficienza', 'livello': 'standard', 'tag': 'Sistema energetico dell’attività', 'titolo': 'Efficienza energetica e impianti tecnologici', 'nav': 'Efficienza energetica',
     'titolo_sez': 'Non guardare soltanto a quanto produci. Guarda anche a come consumi.',
     'testo': ['Un progetto energetico efficace non considera solamente la produzione fotovoltaica, ma anche il modo in cui l’azienda utilizza l’energia.',
               'Analizzare i consumi consente di valutare in modo coordinato fotovoltaico, accumulo, climatizzazione, pompe di calore e altri interventi di efficientamento.'],
     'forte': 'Produrre meglio e consumare meglio sono due parti dello stesso progetto.',
     'art': 'termici', 'foto': 'impianti-termici.jpg', 'foto_alt': 'Impianti termici e tecnologici',
     'opzione': 'Efficienza energetica e impianti tecnologici'},
]

IMPRESE_HERO = {
    'h1': 'Energia e servizi tecnici per imprese e grandi impianti',
    'lead': 'Progettiamo, realizziamo e gestiamo impianti fotovoltaici e sistemi energetici per aziende, attività produttive e operatori del settore, seguendo l’intervento dalla valutazione tecnica alla gestione nel tempo.',
    'tags': ['Nuovi impianti', 'Ampliamenti', 'Revamping', 'Manutenzione', 'Attività specialistiche', 'Impianti di grande potenza'],
}

SISTEMA_IMPRESE = {
    'eyebrow': 'Continuità del servizio',
    'titolo': 'Un unico interlocutore per l’impianto',
    'testo': 'Dalla progettazione alla gestione: un unico riferimento tecnico per seguire l’impianto in tutte le sue fasi, con continuità nel tempo.',
    'aree': [
        {'icona': 'progetto', 'titolo': 'Progettazione e realizzazione', 'concetto': 'Dai consumi e dalle caratteristiche del sito alla progettazione e alla realizzazione dell’impianto.',
         'link': [('Fotovoltaico industriale', 'fotovoltaico-industriale'), ('Utility Scale', 'utility-scale')]},
        {'icona': 'gestione', 'titolo': 'Gestione e manutenzione', 'concetto': 'Dalla messa in esercizio alla manutenzione programmata e agli interventi tecnici.',
         'link': [('Operation & Maintenance', 'om')]},
        {'icona': 'controllo', 'titolo': 'Controllo specialistico', 'concetto': 'Termografia, verifiche elettriche, lavaggio e attività di controllo per conoscere lo stato dell’impianto.',
         'link': [('Termografia', 'termografia'), ('Lavaggio moduli', 'lavaggio')]},
    ],
}

IMPIANTO_ESISTENTE_IMPRESE = {
    'id': 'impianto-esistente',
    'eyebrow': 'Per chi gestisce già un impianto',
    'titolo': 'Hai già un impianto fotovoltaico?',
    'testo': 'Possiamo partire dallo stato attuale dell’impianto per valutarne condizioni operative, necessità di manutenzione e possibili interventi. Non è necessario che l’impianto sia stato realizzato da Rivetti Impianti.',
    'voci_intro': 'Possiamo intervenire per:',
    'voci': ['Verifica tecnica iniziale', 'Manutenzione', 'O&M', 'Termografia', 'Lavaggio', 'Ricerca anomalie', 'Revamping',
             'Valutazione di ampliamenti', 'Integrazione di sistemi di accumulo, quando tecnicamente possibile'],
    'cta': 'Richiedi una valutazione dell’impianto',
    'servizio': 'Operation & Maintenance fotovoltaico',
    'whatsapp': 'Buongiorno, vorrei ricevere una valutazione tecnica per la gestione, manutenzione o verifica di un impianto fotovoltaico esistente.',
}

COME_LAVORIAMO_IMPRESE = {
    'eyebrow': 'Come lavoriamo',
    'titolo': 'Un percorso tecnico, dalla prima analisi alla gestione',
    'passi': [
        ('Analisi preliminare', 'Raccogliamo esigenze, consumi e obiettivi dell’attività o dell’impianto.'),
        ('Sopralluogo e raccolta dati', 'Verifichiamo sul posto struttura, impianti e dati necessari.'),
        ('Progettazione e proposta tecnica', 'Definiamo la soluzione e la proposta tecnica.'),
        ('Realizzazione e collaudo', 'Eseguiamo le lavorazioni nell’ambito delle attività tecniche di nostra competenza, coordiniamo le attività affidate a imprese partner e verifichiamo il funzionamento.'),
        ('Gestione e manutenzione', 'Attività programmate, interventi tecnici e verifiche nel tempo.'),
    ],
    'nota': 'Per gli impianti esistenti il percorso può partire direttamente dalla verifica tecnica.',
}

SERVIZI_PA = {
    'tag': 'I servizi per la PA',
    'titolo': 'Interventi per l’efficienza energetica, il fotovoltaico, le Comunità Energetiche e la gestione degli impianti pubblici.',
    'testo': 'In funzione dell’intervento possono essere valutati incentivi, contributi e strumenti di finanziamento disponibili.',
    'art': 'pa_hero', 'foto': 'pubblica-amministrazione.jpg', 'foto_alt': 'Edificio pubblico con impianto fotovoltaico',
}

# Copertine illustrative delle tre macroarea: assets/servizi/<chiave>-hero.jpg (immagini IA fotorealistiche, NON lavori
# eseguiti: per questo il testo alternativo le descrive come immagini generiche). Se il file manca resta l'illustrazione SVG.
# Hero della Home: video showreel (con pulsante audio). Il file video va in assets/ (vedi LEGGIMI.md).
HERO_HOME = dict(
    video='assets/rivetti-showreel.mp4',
    poster='assets/servizi/pa-hero.jpg',
    tag='Rivetti Impianti &bull; Technical Engineering',
    titolo='Dal 2008 chiudiamo circuiti e stringiamo relazioni. Grazie',
    testo='Progettiamo, realizziamo e manteniamo impianti tecnologici per abitazioni, imprese ed enti pubblici, seguendo ogni intervento dalla valutazione tecnica all&rsquo;assistenza.',
    audio_on='Attiva audio', audio_off='Disattiva audio',
)

HERO_FOTO = {
    'privati': ('privati-hero.jpg', 'Abitazione con impianto fotovoltaico'),
    'imprese': ('imprese-hero.jpg', 'Impianto fotovoltaico su copertura industriale'),
    'pa': ('pa-hero.jpg', 'Edificio pubblico con impianto fotovoltaico'),
}

# ----------------------------------------------------------------------------- PAGINA PUBBLICA AMMINISTRAZIONE
PA_HERO = {
    'h1': 'Soluzioni energetiche per la Pubblica Amministrazione',
    'lead': 'Progettiamo, realizziamo e gestiamo interventi energetici per edifici e strutture pubbliche, dal fotovoltaico alla riqualificazione impiantistica, fino alla manutenzione degli impianti nel tempo.',
}

# Testi della pagina PA: tono istituzionale; nessun numero, percentuale, promessa economica o riferimento geografico.
PA_INTRO = {
    'eyebrow': 'Edifici e strutture pubbliche',
    'titolo': 'Ogni edificio pubblico consuma energia. Il punto è come utilizzarla meglio.',
    'paragrafi': [
        'Scuole, uffici, strutture sportive e altri edifici pubblici presentano esigenze energetiche differenti.',
        'Intervenire in modo efficace significa partire dallo stato reale dell’edificio, dagli impianti presenti e dai consumi, per individuare gli interventi tecnicamente più appropriati.',
    ],
    'frase': 'Riqualificare non significa sostituire un singolo componente: significa migliorare il modo in cui edificio e impianti utilizzano l’energia.',
}

SISTEMA_PA = {
    'eyebrow': 'Approccio coordinato',
    'titolo': 'Un progetto energetico coordinato',
    'testo': None,
    'aree': [
        {'icona': 'progetto', 'titolo': 'Analisi e progettazione',
         'concetto': 'Raccogliamo dati, analizziamo gli impianti esistenti e valutiamo le condizioni tecniche dell’intervento prima di definire la soluzione.',
         'link': [('Riqualificazione energetica', 'riqualificazione')]},
        {'icona': 'sole', 'titolo': 'Realizzazione',
         'concetto': 'Coordiniamo le attività tecniche previste dal progetto, dall’installazione alla configurazione e al collaudo degli impianti.',
         'link': [('Fotovoltaico', 'fotovoltaico-pa'), ('Comunità Energetiche', 'cer')]},
        {'icona': 'gestione', 'titolo': 'Gestione nel tempo',
         'concetto': 'Manutenzione, verifiche e interventi tecnici permettono di continuare a seguire gli impianti anche dopo la messa in esercizio.',
         'link': [('Gestione e manutenzione', 'gestione')]},
    ],
    'conclusione': 'L’obiettivo non è soltanto realizzare un nuovo impianto, ma inserirlo correttamente nel sistema energetico dell’edificio.',
}

PA_AREE_HEAD = {
    'eyebrow': 'Aree di intervento',
    'titolo': 'Gli ambiti di intervento',
    'testo': 'Per ogni intervento si parte da una valutazione tecnica delle caratteristiche dell’Ente e delle strutture interessate.',
}

SERVIZI_PA_PAGINA = [
    {'id': 'riqualificazione', 'nav': 'Riqualificazione energetica', 'tag': 'Edifici pubblici',
     'titolo': 'Riqualificare partendo da come l’edificio utilizza l’energia',
     'paragrafi': ['Prima di definire un intervento è necessario comprendere come l’edificio utilizza energia, quali impianti sono presenti e dove esistono margini di miglioramento.'],
     'punti_titolo': 'Ambiti dell’intervento',
     'punti': ['Climatizzazione', 'Pompe di calore', 'Impianti termici', 'Produzione di acqua calda sanitaria', 'Regolazione e gestione',
               'Fotovoltaico', 'Sistemi di accumulo, quando opportuni', 'Integrazione tra i diversi sistemi'],
     'frase': 'Produrre energia in modo efficiente e utilizzarla in modo efficiente sono due parti dello stesso progetto.',
     'nota': 'Il nostro ambito è quello energetico e impiantistico: eventuali opere edili collegate vanno valutate caso per caso.',
     'art': 'pa_edificio', 'foto': 'pa-riqualificazione.jpg', 'foto_alt': 'Edificio pubblico con impianti energetici',
     'opzione': 'Riqualificazione energetica edifici pubblici'},
    {'id': 'fotovoltaico-pa', 'nav': 'Fotovoltaico', 'tag': 'Fotovoltaico',
     'titolo': 'Produrre energia direttamente sulle strutture pubbliche',
     'paragrafi': ['Coperture, pensiline e altre superfici idonee possono diventare una risorsa per produrre energia direttamente presso gli edifici e le strutture dell’Ente.',
                   'Il progetto deve partire dalla verifica delle superfici, dei consumi, delle caratteristiche elettriche e delle condizioni tecniche e amministrative applicabili.'],
     'frase': 'Una superficie disponibile può diventare una superficie che produce energia.',
     'percorso': ['Sopralluogo', 'Raccolta dati', 'Verifica delle superfici', 'Progettazione', 'Dimensionamento', 'Realizzazione', 'Configurazione e collaudo', 'Manutenzione'],
     'art': 'pa_fv', 'foto': 'pa-fotovoltaico.jpg', 'foto_alt': 'Impianto fotovoltaico su struttura pubblica',
     'opzione': 'Fotovoltaico per edifici e strutture pubbliche',
     'sub': {'id': 'pensiline', 'titolo': 'Parcheggi che possono produrre energia',
             'paragrafi': ['Le aree di parcheggio possono essere valutate per integrare pensiline fotovoltaiche senza rinunciare alla loro funzione principale.',
                           'Quando previsto dal progetto, le pensiline possono essere integrate con sistemi di accumulo e infrastrutture di ricarica per veicoli elettrici.'],
             'frase': 'Una stessa area può offrire copertura, produrre energia e supportare nuovi servizi energetici.',
             'nota': 'Fattibilità tecnica e autorizzativa da verificare caso per caso.',
             'art': 'pa_pensilina', 'foto': 'pa-pensiline.jpg', 'foto_alt': 'Pensilina fotovoltaica in un’area di parcheggio',
             'opzione': 'Pensiline fotovoltaiche e aree di parcheggio'}},
    {'id': 'cer', 'nav': 'Comunità Energetiche', 'tag': 'Comunità Energetiche Rinnovabili',
     'titolo': 'Energia prodotta localmente, condivisa all’interno di una configurazione',
     'paragrafi': ['Le Comunità Energetiche Rinnovabili introducono un modello nel quale produzione e consumo di energia possono essere messi in relazione all’interno di una configurazione regolata.',
                   'Un Ente può valutare il proprio coinvolgimento come produttore, consumatore o soggetto promotore, in funzione della configurazione e dei requisiti applicabili.'],
     'schema': [('Produzione', 'Impianti da fonti rinnovabili'), ('Consumo', 'Utenze dell’Ente e dei soggetti coinvolti'), ('Condivisione', 'Energia condivisa nella configurazione')],
     'punti_titolo': 'Rivetti Impianti può supportare',
     'punti': ['Valutazione tecnica preliminare', 'Analisi dei punti di produzione', 'Analisi dei punti di consumo', 'Progettazione degli impianti',
               'Configurazione energetica', 'Supporto tecnico alla documentazione di propria competenza'],
     'frase': 'Una CER non è semplicemente un impianto fotovoltaico: è un sistema in cui produzione e consumi vengono messi in relazione.',
     'nota': 'Costituzione, partecipazione, incentivi e configurazione devono essere verificati sulla base della normativa vigente e delle caratteristiche del progetto.',
     'art': 'pa_cer', 'foto': 'pa-cer.jpg', 'foto_alt': 'Configurazione di condivisione dell’energia tra edifici',
     'opzione': 'Comunità Energetiche Rinnovabili (supporto tecnico)'},
    {'id': 'gestione', 'nav': 'Gestione e manutenzione', 'tag': 'Dopo la realizzazione',
     'titolo': 'Realizzare l’impianto è una fase. Gestirlo nel tempo è quella successiva.',
     'paragrafi': ['Gli impianti energetici pubblici devono continuare a essere controllati anche dopo la messa in esercizio.',
                   'Manutenzione programmata, verifiche tecniche e interventi correttivi contribuiscono a mantenere sotto controllo stato e funzionamento degli impianti.'],
     'frase': 'Un impianto pubblico non termina con il collaudo.',
     'punti_titolo': 'Attività possibili',
     'punti': ['Manutenzione preventiva', 'Manutenzione correttiva', 'Verifiche elettriche', 'Controllo inverter', 'Controllo quadri', 'Termografia',
               'Lavaggio moduli', 'Ricerca anomalie', 'Verifica dello stato dei componenti', 'Interventi tecnici programmati'],
     'nota': 'Contenuti, frequenze e modalità degli interventi vengono definiti in funzione dell’impianto e delle procedure applicabili all’Ente.',
     'art': 'om', 'foto': 'pa-gestione.jpg', 'foto_alt': 'Controllo tecnico di un impianto fotovoltaico',
     'opzione': 'Gestione e manutenzione impianti per enti pubblici'},
]

INCENTIVI_PA = {
    'eyebrow': 'Incentivi e strumenti',
    'titolo': 'Incentivi e strumenti per gli interventi energetici',
    'paragrafi': ['Per alcuni interventi possono essere disponibili contributi, incentivi, bandi o programmi di finanziamento.',
                  'La disponibilità delle misure, i requisiti e le procedure cambiano in funzione dello strumento e del momento in cui viene sviluppato il progetto.'],
    'noi_t': 'Rivetti Impianti',
    'noi': ['Supporta la definizione degli aspetti tecnici dell’intervento e la documentazione tecnica di propria competenza.'],
    'ente_t': 'Cosa resta all’Ente',
    'ente': ['La scelta dello strumento e la verifica dei requisiti di accesso', 'Le attività amministrative, procedurali e legali, con i soggetti competenti'],
    'frase': 'Lo strumento di finanziamento deve accompagnare un progetto tecnicamente valido, non sostituirlo.',
    'cta': 'Richiedi un confronto tecnico',
    'servizio': 'Supporto tecnico per incentivi e bandi',
}

IMPIANTO_ESISTENTE_PA = {
    'id': 'impianti-esistenti',
    'nav': 'Impianti esistenti',
    'eyebrow': 'Impianti già installati',
    'titolo': 'Partire da ciò che è già installato',
    'testo': 'Non sempre il primo passo è realizzare un nuovo impianto.',
    'testo2': 'Un Ente può avere già sistemi fotovoltaici, termici o altri impianti energetici che richiedono verifiche, manutenzione o aggiornamenti.',
    'frase': 'Conoscere lo stato dell’impianto esistente è il primo passo per decidere come intervenire.',
    'voci_intro': 'Possibili attività',
    'voci': ['Verifica tecnica', 'Manutenzione', 'Ricerca anomalie', 'Termografia', 'Lavaggio', 'Revamping', 'Valutazione di ampliamenti',
             'Integrazione di nuovi sistemi, quando tecnicamente possibile'],
    'cta': 'Richiedi una valutazione tecnica',
    'servizio': 'Gestione e manutenzione impianti per enti pubblici',
    'whatsapp': 'Salve, vorrei richiedere una valutazione tecnica su impianti energetici già installati presso il nostro ente, grazie.',
}

COME_LAVORIAMO_PA = {
    'eyebrow': 'Come lavoriamo',
    'titolo': 'Dal primo confronto alla gestione dell’impianto',
    'passi': [
        ('Analisi preliminare', 'Raccogliamo le informazioni sull’edificio, sugli impianti e sugli obiettivi dell’Ente.'),
        ('Sopralluogo e raccolta dati', 'Verifichiamo le condizioni tecniche necessarie per sviluppare l’intervento.'),
        ('Studio della soluzione', 'Definiamo la configurazione tecnica più coerente con le esigenze del progetto.'),
        ('Progettazione e realizzazione', 'Seguiamo le attività previste nell’ambito delle nostre competenze tecniche.'),
        ('Collaudo e gestione', 'Dopo la realizzazione possiamo continuare a seguire gli impianti con manutenzione e verifiche.'),
    ],
    'nota': 'Modalità operative, affidamento e percorso di realizzazione dipendono dalle caratteristiche dell’intervento e dalle procedure applicabili.',
}

PA_RIEPILOGO = {
    'eyebrow': 'In sintesi',
    'titolo': 'Un intervento energetico deve funzionare nel suo insieme',
    'voci': [('lente', 'ANALIZZA', 'Parti dai consumi e dallo stato reale degli impianti.'),
             ('progetto', 'PROGETTA', 'Definisci gli interventi in modo coordinato.'),
             ('sole', 'PRODUCI', 'Valuta come integrare energia rinnovabile nelle strutture pubbliche.'),
             ('ingranaggio', 'GESTISCI', 'Continua a controllare gli impianti anche dopo la realizzazione.')],
}

PA_FINALE = {
    'id': 'sintesi-pa',
    'titolo': 'Efficienza energetica non significa soltanto installare nuove tecnologie. Significa scegliere dove intervenire, progettare correttamente e continuare a gestire gli impianti nel tempo.',
    'frase': 'Dalla valutazione iniziale alla manutenzione, ogni fase fa parte dello stesso progetto.',
}

OPZIONI_PA = ([x['opzione'] for x in SERVIZI_PA_PAGINA]
              + [SERVIZI_PA_PAGINA[1]['sub']['opzione'], INCENTIVI_PA['servizio']])

# Voci "extra" del modulo di contatto
OPZIONI_EXTRA = ['Bonus e incentivi', 'Sopralluogo', 'Altro']

# ----------------------------------------------------------------------------- MENU "SERVIZI"
# (etichetta, pagina#ancora). Le voci senza ancora puntano all'inizio della pagina.
MENU_SERVIZI = [
    {'titolo': 'Privati', 'href': 'privati.html', 'voci': [
        ('Fotovoltaico Residenziale', 'privati.html#fotovoltaico'),
        ('Sistemi di Accumulo', 'privati.html#accumulo'),
        ('Climatizzazione e Pompe di Calore', 'privati.html#climatizzazione'),
        ('Solare Termico', 'privati.html#solare-termico'),
        ('Manutenzione & Assistenza', 'privati.html#manutenzione'),
        ('Lavaggio Moduli', 'privati.html#lavaggio'),
        ('Termografia', 'privati.html#termografia'),
        ('Hai già un impianto?', 'privati.html#impianto-esistente'),
    ]},
    {'titolo': 'Imprese', 'href': 'imprese.html', 'voci': [
        ('Fotovoltaico Industriale', 'imprese.html#fotovoltaico-industriale'),
        ('Utility Scale', 'imprese.html#utility-scale'),
        ('Operation & Maintenance (O&M)', 'imprese.html#om'),
        ('Lavaggio Moduli', 'imprese.html#lavaggio'),
        ('Termografia', 'imprese.html#termografia'),
        ('Agrivoltaico', 'imprese.html#agrivoltaico'),
        ('Comunità Energetiche Rinnovabili (CER)', 'imprese.html#cer'),
        ('Efficienza Energetica e Impianti', 'imprese.html#efficienza'),
        ('Hai già un impianto?', 'imprese.html#impianto-esistente'),
    ]},
    {'titolo': 'Pubblica Amministrazione', 'href': 'pubblica-amministrazione.html', 'voci': [
        ('Riqualificazione Energetica', 'pubblica-amministrazione.html#riqualificazione'),
        ('Fotovoltaico PA', 'pubblica-amministrazione.html#fotovoltaico-pa'),
        ('Comunità Energetiche', 'pubblica-amministrazione.html#cer'),
        ('Gestione e Manutenzione', 'pubblica-amministrazione.html#gestione'),
        ('Impianti esistenti', 'pubblica-amministrazione.html#impianti-esistenti'),
    ]},
]

# ----------------------------------------------------------------------------- INCENTIVI
INCENTIVI = {
    'intro': 'Quando disponibili e applicabili, valutiamo insieme al cliente gli strumenti di incentivazione e le agevolazioni collegate all’intervento.',
    'nota_foot': 'Disponibilità e condizioni variano nel tempo e dipendono dal singolo intervento: si verificano caso per caso.',
    'nota_modale': ('Informazioni di carattere generale: disponibilità, requisiti e condizioni degli strumenti cambiano nel tempo, '
                    'dipendono dal singolo intervento e vanno verificati caso per caso. Nessun beneficio è automatico o garantito.'),
    'schede': [
        {'id': 'm-priv', 'sticker': 'st_people', 'badge': 'Privati · Residenziale', 'titolo': 'Detrazioni fiscali',
         'testo': 'Detrazioni fiscali e strumenti collegati agli interventi di riqualificazione energetica dell’abitazione.',
         'modale_kicker': 'Privati · Residenziale', 'modale_titolo': 'Strumenti collegati agli interventi per la casa',
         'voci': [
             ('Detrazioni fiscali', 'Edilizia ed energia', 'Agevolazioni fiscali previste per interventi di ristrutturazione e di riqualificazione energetica dell&rsquo;abitazione, che possono riguardare anche fotovoltaico, pompe di calore e climatizzazione. Aliquote, limiti e adempimenti dipendono dalla normativa in vigore.'),
             ('Fotovoltaico e accumulo', 'Detrazione', 'Impianti fotovoltaici e sistemi di accumulo possono rientrare tra gli interventi agevolabili, secondo le condizioni previste dalla normativa applicabile.'),
             ('Conto Termico', 'GSE', 'Contributo gestito dal GSE per alcuni interventi di efficienza energetica e di produzione di energia termica da fonti rinnovabili, quando ne ricorrono i requisiti.'),
         ],
         'fonti': [('Agenzia delle Entrate', 'https://www.agenziaentrate.gov.it'), ('ENEA – Detrazioni fiscali', 'https://detrazionifiscali.enea.it'), ('GSE', 'https://www.gse.it')]},
        {'id': 'm-imp', 'sticker': 'st_factory', 'badge': 'Imprese · Industriale', 'titolo': 'Agevolazioni e finanziamenti',
         'testo': 'Agevolazioni fiscali, bandi e strumenti di finanziamento per investimenti in efficienza energetica e fonti rinnovabili.',
         'modale_kicker': 'Imprese · Industriale', 'modale_titolo': 'Strumenti collegati agli investimenti per l’impresa',
         'voci': [
             ('Agevolazioni fiscali per gli investimenti', 'Imprese', 'Misure fiscali a sostegno degli investimenti in beni strumentali e in impianti per l&rsquo;autoconsumo, quando previste e applicabili all&rsquo;impresa.'),
             ('Conto Termico', 'GSE', 'Incentivo gestito dal GSE per alcuni interventi di efficienza energetica, aperto anche alle imprese quando ne ricorrono i requisiti.'),
             ('Bandi e programmi di finanziamento', 'Transizione energetica', 'Finanziamenti e contributi nazionali e regionali per efficienza energetica e rinnovabili, con aperture e scadenze variabili.'),
         ],
         'fonti': [('GSE', 'https://www.gse.it'), ('Ministero delle Imprese e del Made in Italy', 'https://www.mimit.gov.it'), ('Agenzia delle Entrate', 'https://www.agenziaentrate.gov.it')]},
        {'id': 'm-pa', 'sticker': 'st_hall', 'badge': 'Pubblica Amministrazione', 'titolo': 'Strumenti di finanziamento',
         'testo': 'Incentivi, contributi e programmi di finanziamento per interventi su edifici e impianti pubblici.',
         'modale_kicker': 'Pubblica Amministrazione', 'modale_titolo': 'Strumenti collegati agli interventi per gli Enti pubblici',
         'voci': [
             ('Incentivi e contributi', 'Efficienza energetica', 'Strumenti di sostegno agli interventi di efficienza energetica e di produzione da fonti rinnovabili su edifici e strutture pubbliche, secondo requisiti e condizioni definiti dai singoli strumenti.'),
             ('Bandi e programmi di finanziamento', 'Bandi', 'Programmi di finanziamento nazionali ed europei, con aperture, scadenze e requisiti variabili.'),
             ('Comunit&agrave; Energetiche Rinnovabili', 'CER', 'Configurazioni di condivisione dell&rsquo;energia per le quali possono essere previsti strumenti di sostegno, in funzione della configurazione e della normativa vigente.'),
         ],
         'fonti': [('GSE', 'https://www.gse.it')]},
    ],
    # voci del menu "Bonus & Incentivi": (etichetta, id della finestra che si apre)
    'menu': [
        {'titolo': 'Privati', 'modale': 'm-priv', 'voci': ['Detrazioni fiscali', 'Fotovoltaico e accumulo', 'Conto Termico']},
        {'titolo': 'Imprese', 'modale': 'm-imp', 'voci': ['Agevolazioni fiscali', 'Conto Termico', 'Bandi e finanziamenti']},
        {'titolo': 'Pubblica Amministrazione', 'modale': 'm-pa', 'voci': ['Incentivi e contributi', 'Bandi e programmi di finanziamento', 'Comunità Energetiche Rinnovabili']},
    ],
}

# Testi della sezione incentivi in HOME (le pagine Privati/Imprese/PA usano le schede qui sopra, invariate)
INCENTIVI_HOME = {
    'eyebrow': 'Agevolazioni',
    'titolo': 'Incentivi e strumenti di sostegno',
    'intro': 'Alcuni interventi possono beneficiare di incentivi, detrazioni, contributi o strumenti di finanziamento. Disponibilità, requisiti e condizioni dipendono dalla normativa vigente e dal singolo caso.',
    'nota_foot': 'Disponibilità, requisiti e condizioni cambiano nel tempo e devono essere verificati per il singolo intervento.',
    'schede': {
        'm-priv': ('Detrazioni fiscali', 'Per alcuni interventi sull’abitazione possono essere previste detrazioni e altre agevolazioni, da verificare in base alla normativa applicabile.'),
        'm-imp': ('Agevolazioni e finanziamenti', 'Gli investimenti in efficienza energetica e fonti rinnovabili possono essere interessati da misure fiscali, bandi o strumenti di finanziamento.'),
        'm-pa': ('Incentivi e programmi di finanziamento', 'Per interventi su edifici e impianti pubblici possono essere disponibili contributi, incentivi e programmi di finanziamento con requisiti specifici.'),
    },
}

# ----------------------------------------------------------------------------- PERCHÉ / COME LAVORIAMO
PERCHE = {   # sezione Home "Il nostro approccio" (id HTML: perche)
    'eyebrow': 'Il nostro approccio',
    'titolo': 'Un’organizzazione tecnica che segue l’impianto nel tempo',
    'voci': [
        ('Un riferimento tecnico', 'Seguiamo il progetto dalla valutazione iniziale alla realizzazione, fino alle attività di assistenza e manutenzione.'),
        ('Competenze integrate', 'Fotovoltaico, termoidraulica, climatizzazione e manutenzione vengono valutati in modo coordinato quando il progetto lo richiede.'),
        ('Nuovi impianti e impianti esistenti', 'Interveniamo sia su nuove realizzazioni sia su impianti già in esercizio, con verifiche, manutenzione e possibili integrazioni.'),
        ('Valutazione degli strumenti disponibili', 'Quando applicabili, valutiamo incentivi e agevolazioni collegati all’intervento sulla base dei requisiti previsti.'),
    ],
}

COME_LAVORIAMO = {   # Home
    'eyebrow': 'Come lavoriamo',
    'titolo': 'Un percorso tecnico definito passo dopo passo',
    'passi': [
        ('Primo confronto', 'Raccogliamo le informazioni sull’intervento, sulle esigenze e sugli impianti eventualmente già presenti.'),
        ('Sopralluogo', 'Verifichiamo sul posto le condizioni tecniche necessarie per definire correttamente il lavoro.'),
        ('Proposta tecnica e preventivo', 'Definiamo la soluzione, le attività previste e il relativo preventivo.'),
        ('Realizzazione', 'Eseguiamo le attività tecniche di nostra competenza e coordiniamo, quando necessario, le lavorazioni complementari.'),
        ('Assistenza e manutenzione', 'Continuiamo a seguire l’impianto con verifiche, manutenzione e interventi tecnici.'),
    ],
}

COME_LAVORIAMO_PRIVATI = {
    'eyebrow': 'Come lavoriamo',
    'titolo': 'Dall’analisi delle esigenze all’assistenza nel tempo',
    'passi': [
        ('Analisi delle esigenze', 'Ascoltiamo come vivi la casa e che cosa ti serve: consumi, abitudini, impianti già presenti.'),
        ('Sopralluogo e valutazione tecnica', 'Valutiamo sul posto l’abitazione e le condizioni per l’intervento.'),
        ('Progettazione della soluzione', 'Ricevi una proposta su misura con un preventivo dettagliato.'),
        ('Installazione', 'Realizziamo l’impianto e coordiniamo, quando serve, le attività affidate a imprese partner.'),
        ('Assistenza e manutenzione', 'Verifiche, manutenzione programmata e assistenza nel tempo.'),
    ],
}

# ----------------------------------------------------------------------------- FAQ
# FAQ della pagina Privati: copia INVARIATA delle prime tre domande che la Home aveva prima del nuovo testo
# (la pagina Privati è approvata e non va toccata); la Home ha ora FAQ proprie.
_FAQ_PRIVATI_BASE = [
    ('Come funziona il sopralluogo?',
     'Dopo la tua richiesta ti ricontattiamo per fissare un sopralluogo. Valutiamo sul posto l’immobile o la struttura e le tue esigenze e, in base a quanto rilevato, prepariamo un preventivo dettagliato.'),
    ('Quanto costa un impianto fotovoltaico?',
     'Il costo dipende da potenza, consumi, tipo di copertura, eventuale sistema di accumulo e caratteristiche dell’edificio. Per questo si definisce caso per caso, dopo il sopralluogo, con un preventivo dettagliato.'),
    ('Posso usufruire di bonus e incentivi?',
     'Possono esistere detrazioni fiscali, contributi o bandi collegati all’intervento. Quando sono disponibili e applicabili, li valutiamo insieme a te; requisiti e condizioni dipendono dal singolo caso. Trovi un quadro generale nella sezione Bonus &amp; Incentivi.'),
]
FAQ = {
    'home': [
        ('Come funziona il sopralluogo?',
         'Dopo il primo contatto raccogliamo le informazioni sull’intervento e, quando necessario, fissiamo un sopralluogo. La verifica sul posto ci permette di valutare le condizioni tecniche e preparare una proposta più precisa.'),
        ('Quanto costa un impianto fotovoltaico?',
         'Il costo dipende dalla potenza, dai consumi, dalle caratteristiche dell’edificio, dalla tipologia di installazione e dagli eventuali sistemi integrati. Per questo il preventivo viene definito dopo aver valutato il caso specifico.'),
        ('Posso usufruire di bonus e incentivi?',
         'Dipende dal tipo di intervento e dalla normativa vigente. Quando sono disponibili strumenti applicabili, ne verifichiamo i requisiti e gli aspetti tecnici collegati al progetto. Nessun incentivo può essere considerato automatico prima delle necessarie verifiche.'),
        ('A cosa serve un sistema di accumulo?',
         'Permette di conservare parte dell’energia prodotta dall’impianto fotovoltaico per utilizzarla in momenti diversi da quelli di produzione. La sua utilità va valutata in base ai consumi e alle caratteristiche dell’impianto.'),
        ('Vi occupate anche di manutenzione?',
         'Sì. Interveniamo anche su impianti esistenti con attività di manutenzione, verifiche tecniche, controllo dei componenti, lavaggio dei moduli e termografia, in funzione delle esigenze dell’impianto.'),
    ],
}

# FAQ della pagina Privati: le prime domande della Home (sopralluogo, costo, incentivi) + quelle specifiche.
FAQ['privati'] = [
    _FAQ_PRIVATI_BASE[0], _FAQ_PRIVATI_BASE[1], _FAQ_PRIVATI_BASE[2],
    ('Posso installare un sistema di accumulo su un impianto fotovoltaico esistente?',
     'In molti casi è possibile, ma dipende dalla configurazione dell’impianto (ad esempio inverter, collegamenti e spazi disponibili) e va verificato con un controllo tecnico. Dopo la verifica ti indichiamo se e con quale soluzione si può integrare.'),
    ('Rivetti Impianti effettua anche manutenzione di impianti non realizzati direttamente?',
     'Sì, possiamo occuparci anche di impianti già installati, indipendentemente da chi li ha realizzati. Si parte da una verifica dello stato dell’impianto, per capire quali attività servono.'),
    ('Ogni quanto va effettuato il lavaggio dei pannelli?',
     'Non esiste una frequenza valida per tutti: dipende dall’impianto e dall’ambiente in cui si trova. Durante una verifica valutiamo se, e con quale cadenza, conviene intervenire.'),
    ('A cosa serve una verifica termografica?',
     'A controllare in modo non invasivo, con una camera termica, la distribuzione della temperatura su moduli e componenti, per individuare eventuali anomalie termiche. È un supporto alla manutenzione e alla verifica dell’impianto: l’esito indica dove approfondire con ulteriori controlli.'),
    ('Fotovoltaico e climatizzazione possono essere integrati?',
     'Sì: una climatizzazione a energia elettrica, come una pompa di calore, può utilizzare l’energia prodotta dall’impianto fotovoltaico. Quanto sia conveniente dipende da consumi, abitudini e dimensionamento dei due impianti, che valutiamo insieme in fase di progetto.'),
    ('Realizzate anche impianti solari termici?',
     'Sì, il solare termico fa parte dei servizi per la casa: sfrutta l’energia solare per la produzione di acqua calda sanitaria. La soluzione dipende dalle esigenze, dagli spazi e dall’impianto termico esistente, e si definisce dopo il sopralluogo.'),
]

# ----------------------------------------------------------------------------- REALIZZAZIONI
# I progetti (dati, regole di pubblicazione, modello) stanno in src/progetti.py; qualifiche e marchi in src/qualifiche.py.


FAQ['imprese'] = [
    ('Realizzate impianti fotovoltaici anche su capannoni industriali?',
     'Sì: capannoni e strutture produttive rientrano tra gli ambiti di intervento. Si parte dall’analisi dei consumi e dalla verifica delle superfici disponibili, poi si definiscono progetto e dimensionamento.'),
    ('Seguite anche impianti fotovoltaici di grande potenza?',
     'Sì, siamo strutturati per operare anche su impianti a terra e di grande potenza. Attività coinvolte e modalità di intervento si definiscono in base al progetto, dopo una valutazione tecnica.'),
    ('Effettuate manutenzione su impianti realizzati da altre aziende?',
     'Sì, possiamo valutare la manutenzione anche di impianti realizzati da altri. Si parte da una verifica tecnica iniziale dello stato dell’impianto e dei componenti, per definire le attività necessarie.'),
    ('È possibile affidare a Rivetti Impianti un servizio O&M programmato?',
     'Sì: il servizio di Operation & Maintenance può comprendere attività programmate e interventi tecnici, ed è modulabile in base alla tipologia e alla dimensione dell’impianto. Contenuti e cadenza si concordano dopo la verifica iniziale.'),
    ('Effettuate termografie su impianti fotovoltaici?',
     'Sì. La termografia può contribuire a individuare anomalie termiche su moduli, connessioni, quadri e componenti elettrici, in funzione del tipo di verifica eseguita, e può essere inserita nei programmi di manutenzione preventiva.'),
    ('Effettuate il lavaggio di grandi impianti?',
     'Sì, il lavaggio dei moduli è un’attività di manutenzione che può riguardare anche impianti di grandi dimensioni. Se e con quale frequenza intervenire dipende dalle condizioni dell’impianto e dal contesto.'),
    ('È possibile integrare un sistema di accumulo su un impianto aziendale esistente?',
     'Quando tecnicamente possibile, sì. Dipende dalla configurazione dell’impianto e dai consumi dell’attività e va verificato con un controllo tecnico preliminare.'),
    ('Seguite anche progetti agrivoltaici?',
     'Sì, possiamo seguire gli aspetti tecnici di progetti agrivoltaici, dallo studio preliminare alla progettazione. La fattibilità dipende dal progetto e dalla normativa applicabile, da verificare caso per caso.'),
    ('Un’impresa può partecipare a una Comunità Energetica Rinnovabile?',
     'Un’impresa può valutare la partecipazione a una Comunità Energetica Rinnovabile, previa verifica dei requisiti applicabili. Possiamo supportare gli aspetti tecnici legati agli impianti e alla configurazione energetica; gli aspetti normativi e incentivanti vanno verificati caso per caso.'),
]

FAQ['pa'] = [
    ('Realizzate impianti fotovoltaici per edifici pubblici?',
     'Sì, edifici e strutture pubbliche rientrano tra gli ambiti di intervento. Si parte dal sopralluogo e dall’analisi di superfici e consumi; fattibilità tecnica e amministrativa vanno verificate caso per caso, in funzione delle procedure applicabili all’Ente.'),
    ('È possibile installare fotovoltaico su scuole e strutture sportive?',
     'In linea generale sì, quando la struttura lo consente. Servono una verifica tecnica di coperture e impianto elettrico esistente e le verifiche amministrative e autorizzative richieste dal caso specifico.'),
    ('È possibile realizzare pensiline fotovoltaiche nei parcheggi pubblici?',
     'È un’ipotesi che può essere valutata, quando tecnicamente e amministrativamente realizzabile. Si verificano spazi, strutture, collegamento elettrico e requisiti autorizzativi applicabili all’area.'),
    ('È possibile integrare infrastrutture di ricarica per veicoli elettrici?',
     'Sì, quando il progetto lo prevede: la ricarica può essere integrata con l’impianto fotovoltaico ed eventualmente con un sistema di accumulo, previa verifica tecnica della potenza disponibile e dell’impianto elettrico.'),
    ('Supportate progetti di Comunità Energetiche Rinnovabili?',
     'Sì, per gli aspetti tecnici: valutazione dei punti di produzione e di consumo, progettazione degli impianti e configurazione energetica. Gli aspetti legali e amministrativi restano in capo all’Ente e ai soggetti competenti.'),
    ('Effettuate manutenzione su impianti già esistenti?',
     'Sì, anche su impianti non realizzati da noi. Si parte da una verifica tecnica iniziale dello stato dell’impianto, per definire le attività necessarie.'),
    ('È possibile affidare attività di manutenzione programmata?',
     'Sì, è possibile definire un programma di attività periodiche, come verifiche, controlli elettrici, lavaggio dei moduli e termografia. Le modalità di affidamento seguono le procedure applicabili all’Ente.'),
    ('Supportate la valutazione di incentivi e bandi?',
     'Supportiamo la definizione degli aspetti tecnici dell’intervento e la documentazione tecnica di nostra competenza. Le attività amministrative e legali non rientrano tra i nostri servizi.'),
    ('Gli interventi possono includere sistemi di accumulo?',
     'Sì, l’accumulo può essere valutato insieme all’impianto fotovoltaico, in funzione del profilo dei consumi, degli spazi disponibili e degli obiettivi dell’Ente. È una valutazione tecnica da fare caso per caso.'),
]


# ----------------------------------------------------------------------------- PRIVATI: perché il fotovoltaico
# Testi concettuali: NESSUN esempio economico, kWh di simulazione, percentuale, previsione sui prezzi o promessa di risparmio.
PRIVATI_FV = {
    'perche': {
        'eyebrow': 'Fotovoltaico per la casa',
        'titolo': 'Perché continuare a comprare energia quando puoi produrla?',
        'paragrafi': [
            'Ogni giorno il sole può produrre una parte dell’energia di cui ha bisogno la tua casa.',
            'Un impianto fotovoltaico permette di trasformare una superficie disponibile dell’abitazione in una fonte di energia, riducendo la quantità di elettricità che deve essere acquistata dalla rete.',
            'Più energia riesci a utilizzare direttamente dal tuo impianto, minore è la dipendenza dall’energia acquistata.',
        ],
        'frase': 'Ogni kWh che produci e utilizzi è un kWh che non devi acquistare dalla rete.',
        'carte': [
            {'titolo': 'Perché installarlo oggi',
             'paragrafi': ['Il fotovoltaico produce valore dal momento in cui entra in funzione.',
                           'Rimandare significa continuare ad acquistare dalla rete energia che, in parte, potresti produrre direttamente.'],
             'forte': 'Prima inizi a produrre la tua energia, prima inizi a ridurre quella che acquisti.'},
            {'titolo': 'Più energia tua, meno dipendenza dalla rete',
             'paragrafi': ['Il fotovoltaico può ridurre il fabbisogno di energia acquistata dall’esterno.',
                           'Produrre energia direttamente significa dipendere meno dalla rete per una parte dei propri consumi: è una maggiore indipendenza energetica per la tua casa.']},
            {'titolo': 'Riduci l’esposizione al costo dell’energia',
             'paragrafi': ['Il prezzo dell’energia acquistata dalla rete può variare nel tempo.',
                           'Produrne una parte direttamente significa ridurre la quantità di energia soggetta a queste variazioni.'],
             'forte': 'Una parte dell’energia che utilizzi non devi più comprarla.'},
        ],
    },
    'accumulo': {
        'id': 'fotovoltaico-accumulo',
        'eyebrow': 'Fotovoltaico + accumulo',
        'titolo': 'Usa la tua energia anche quando il sole non produce',
        'paragrafi': [
            'Il fotovoltaico produce soprattutto durante le ore diurne.',
            'Un sistema di accumulo permette di conservare parte dell’energia prodotta e renderla disponibile in momenti diversi, ad esempio la sera o nelle ore in cui i consumi della casa sono più elevati.',
            'L’accumulo aumenta la possibilità di utilizzare direttamente l’energia prodotta dal proprio impianto e può contribuire a ridurre ulteriormente il ricorso alla rete.',
        ],
        'passi': [
            ('Produci', 'Il fotovoltaico trasforma l’energia solare in energia elettrica per la casa.'),
            ('Utilizza', 'L’energia prodotta viene utilizzata direttamente quando i consumi avvengono nello stesso momento.'),
            ('Conserva', 'L’energia disponibile può essere accumulata per essere utilizzata successivamente.'),
        ],
        'conclusione': 'L’obiettivo è semplice: utilizzare quanto più possibile l’energia prodotta dalla propria casa.',
        'nota': 'Capacità e configurazione della batteria devono essere dimensionate in funzione dell’impianto e delle reali abitudini di consumo.',
        'link': ('Scopri i sistemi di accumulo', '#accumulo'),
    },
    'cambia': {
        'eyebrow': 'In sintesi',
        'titolo': 'Cosa cambia con il fotovoltaico?',
        'voci': [
            ('sole', 'Produci', 'Una parte dell’energia direttamente a casa.'),
            ('spina', 'Consumi', 'Utilizzi l’energia prodotta nel momento in cui serve.'),
            ('batteria', 'Accumuli', 'Con una batteria puoi spostare nel tempo una parte dell’energia prodotta.'),
            ('giu', 'Riduci', 'Diminuisci l’energia che devi acquistare dalla rete.'),
            ('casa', 'Valorizzi', 'Migliori l’efficienza energetica e il profilo energetico dell’abitazione.'),
        ],
    },
    'tempo': {
        'eyebrow': 'Nel tempo',
        'titolo': 'Il valore del fotovoltaico per la tua casa',
        'carte': [
            {'titolo': 'Un investimento anche sull’abitazione',
             'paragrafi': ['Un impianto fotovoltaico ben progettato contribuisce a migliorare il profilo energetico dell’abitazione e può aumentarne l’interesse e il valore nel tempo.']},
            {'titolo': 'Un impianto pensato per durare',
             'paragrafi': ['Il fotovoltaico è una tecnologia progettata per operare per molti anni.',
                           'La qualità della progettazione, dell’installazione e della manutenzione incide sul modo in cui l’impianto conserva prestazioni e affidabilità nel tempo.'],
             'link': ('Scopri la manutenzione', '#manutenzione')},
            {'titolo': 'Produrre energia da una fonte rinnovabile',
             'paragrafi': ['Il fotovoltaico utilizza una fonte rinnovabile e permette di produrre energia direttamente nel luogo in cui viene utilizzata.',
                           'Ridurre il ricorso all’energia acquistata dalla rete significa anche aumentare la quota di energia prodotta da una fonte rinnovabile all’interno della propria abitazione.',
                           'È una scelta che unisce interesse economico, efficienza energetica e riduzione dell’impatto ambientale.']},
            {'titolo': 'E l’energia in eccesso?',
             'paragrafi': ['L’energia prodotta e non utilizzata direttamente o attraverso l’accumulo può essere immessa nella rete secondo i meccanismi applicabili.',
                           'In presenza dei requisiti previsti, può inoltre essere valutata la partecipazione a configurazioni di condivisione dell’energia, come le Comunità Energetiche Rinnovabili.']},
            {'titolo': 'Incentivi e detrazioni',
             'paragrafi': ['Quando previsti dalla normativa e in presenza dei requisiti, incentivi e detrazioni possono contribuire a rendere l’investimento ancora più interessante.'],
             'link': ('Bonus e detrazioni per la tua casa', '#incentivi')},
        ],
    },
    'finale': {
        'titolo': 'Il fotovoltaico non è soltanto un modo per ridurre la bolletta. È un investimento sulla tua casa e sull’energia che utilizzerai negli anni.',
        'frase': 'La bolletta la paghi ogni mese. Il fotovoltaico lavora per te ogni giorno.',
        'cta': 'Scopri la soluzione adatta alla tua casa',
        'servizio': 'Fotovoltaico domestico',
    },
}


# ----------------------------------------------------------------------------- PRIVATI: manutenzione fotovoltaico
# Sostituisce, nella pagina Privati, i blocchi-servizio "manutenzione", "lavaggio" e "termografia" (gli id restano come ancore).
PRIVATI_MAN = {
    'intro': {
        'eyebrow': 'Manutenzione fotovoltaico',
        'titolo': 'Il tuo impianto produce ogni giorno. Assicurati che continui a farlo bene.',
        'paragrafi': [
            'Un impianto fotovoltaico è progettato per lavorare per molti anni, ma questo non significa che debba essere semplicemente installato e dimenticato.',
            'Moduli, inverter, connessioni elettriche, protezioni e strutture lavorano ogni giorno e sono continuamente esposti a calore, pioggia, vento, polvere e variazioni di temperatura.',
            'Per questo controllare periodicamente l’impianto significa proteggere nel tempo la produzione di energia e l’investimento fatto sulla propria casa.',
        ],
        'frase': 'Un impianto che sembra funzionare non è necessariamente un impianto che sta producendo come dovrebbe.',
    },
    'perche': {
        'id': 'manutenzione-importanza',
        'titolo': 'Perché la manutenzione è importante?',
        'paragrafi': [
            'Una riduzione della produzione può svilupparsi gradualmente e passare inosservata.',
            'Sporco sui moduli, anomalie elettriche, connessioni deteriorate, problemi all’inverter o difetti localizzati possono incidere sul comportamento dell’impianto senza provocare necessariamente un arresto completo.',
            'La manutenzione permette di controllare lo stato generale del sistema e di individuare eventuali anomalie prima che diventino problemi più importanti.',
        ],
        'principio': 'Il principio è semplice:',
        'frase': 'L’energia che il tuo impianto non produce è energia che potresti dover acquistare dalla rete.',
        'chiusura': 'Per questo mantenere efficiente l’impianto significa continuare a sfruttare nel tempo l’energia che hai scelto di produrre autonomamente.',
    },
    'aspettare': {
        'id': 'manutenzione-non-aspettare',
        'titolo': 'Non aspettare che l’impianto si fermi',
        'intro': ['La manutenzione non serve soltanto quando compare un guasto.', 'Un impianto può continuare a funzionare anche con:'],
        'voci': ['un modulo che lavora in condizioni anomale', 'una stringa con prestazioni inferiori', 'connessioni che iniziano a deteriorarsi',
                 'un inverter che segnala anomalie', 'moduli ricoperti da sporco o depositi', 'componenti che presentano temperature anomale',
                 'una produzione inferiore a quella attesa'],
        'chiusura': 'Molte di queste condizioni possono essere individuate attraverso controlli mirati.',
        'frase': 'Un controllo mirato permette di intervenire tempestivamente quando emergono condizioni anomale, senza attendere un guasto evidente.',
    },
    'controlli': {
        'id': 'manutenzione-controlli',
        'titolo': 'Cosa controlliamo',
        'intro': 'In funzione dell’impianto e delle sue caratteristiche, le attività di manutenzione possono comprendere:',
        'voci': [
            ('Moduli fotovoltaici', 'Controllo visivo dello stato dei pannelli, delle superfici, dei fissaggi e di eventuali anomalie evidenti.'),
            ('Inverter', 'Verifica dello stato operativo, degli eventuali allarmi e dei principali parametri disponibili.'),
            ('Collegamenti elettrici', 'Controllo delle connessioni e degli elementi dell’impianto interessati dalle verifiche previste.'),
            ('Quadri e protezioni', 'Verifica dello stato generale dei componenti elettrici e delle protezioni.'),
            ('Strutture', 'Controllo visivo di fissaggi, supporti e parti accessibili della struttura.'),
            ('Produzione', 'Quando sono disponibili i dati necessari, analisi dell’andamento dell’impianto per individuare eventuali comportamenti anomali.'),
        ],
    },
    'lavaggio': {
        'id': 'lavaggio',
        'eyebrow': 'Lavaggio dei moduli',
        'titolo': 'Anche la superficie dei pannelli conta.',
        'paragrafi': [
            'Polvere, pollini, residui, foglie, deiezioni e altri depositi possono accumularsi nel tempo sulla superficie dei moduli fotovoltaici.',
            'La pioggia non sempre è sufficiente a rimuovere tutti i residui.',
            'Quando necessario, il lavaggio professionale permette di ripristinare migliori condizioni superficiali dei moduli senza utilizzare interventi improvvisati che potrebbero danneggiare pannelli o componenti.',
            'La necessità e la frequenza del lavaggio dipendono dal luogo di installazione, dall’inclinazione dei moduli e dalle condizioni ambientali.',
        ],
        'frase': 'Non esiste una frequenza uguale per tutti gli impianti: va valutata caso per caso.',
    },
    'termografia': {
        'id': 'termografia',
        'eyebrow': 'Termografia',
        'titolo': 'Alcune anomalie non si vedono a occhio nudo.',
        'paragrafi': ['La termografia permette di osservare la distribuzione delle temperature sui componenti dell’impianto e può contribuire a individuare comportamenti termici anomali.',
                      'In funzione del tipo di verifica, può essere utilizzata su:'],
        'voci': ['moduli fotovoltaici', 'connessioni', 'quadri elettrici', 'componenti dell’impianto'],
        'chiusura': 'È uno strumento particolarmente utile nell’ambito della manutenzione preventiva perché permette di approfondire condizioni che una semplice ispezione visiva potrebbe non evidenziare.',
    },
    'investimento': {
        'id': 'manutenzione-investimento',
        'titolo': 'Manutenzione = protezione dell’investimento',
        'paragrafi': ['Hai installato un impianto per produrre energia per molti anni.',
                      'La manutenzione serve a fare in modo che quell’investimento venga seguito anche dopo l’installazione.'],
        'frase': 'Installare il fotovoltaico è il primo passo. Mantenerlo efficiente nel tempo significa proteggere l’investimento che hai fatto.',
        'intro_voci': 'Un controllo periodico può aiutare a:',
        'voci': ['verificare lo stato generale dell’impianto', 'controllare componenti e collegamenti',
                 'mantenere sotto osservazione la produzione', 'ridurre il rischio che una condizione trascurata evolva in un guasto più importante'],
    },
    'finale': {
        'id': 'verifica-impianto',
        'titolo': 'Non aspettare che sia un guasto a dirti che c’è un problema',
        'paragrafi': ['Il tuo impianto lavora ogni giorno.', 'Controllarlo significa sapere come sta lavorando.'],
        'frase': 'Prenderti cura dell’impianto significa continuare a prenderti cura del risparmio che può generare negli anni.',
    },
}


# ----------------------------------------------------------------------------- IMPRESE: perché produrre energia
# Testi concettuali: nessuna simulazione, percentuale standard, ROI, tempo di rientro o promessa economica.
IMPRESE_FV = {
    'perche': {
        'eyebrow': 'Energia per l’impresa',
        'titolo': 'Perché continuare a comprare tutta l’energia che consumi?',
        'paragrafi': [
            'Per molte attività produttive l’energia rappresenta una voce rilevante dei costi operativi.',
            'Un impianto fotovoltaico permette di produrre direttamente una parte dell’energia utilizzata dall’azienda, trasformando coperture, superfici e aree disponibili in una risorsa energetica.',
        ],
        'frase': 'Ogni kWh prodotto e utilizzato direttamente è energia che l’azienda non deve acquistare dalla rete.',
        'carte': [
            {'titolo': 'Ridurre l’esposizione al costo dell’energia',
             'paragrafi': ['Il prezzo dell’energia acquistata dalla rete può variare nel tempo e incidere sui costi operativi dell’azienda.',
                           'Produrne una parte direttamente consente di ridurre la quantità di energia acquistata e quindi l’esposizione alle variazioni del mercato energetico.'],
             'forte': 'Produrre una parte dell’energia che consumi significa avere maggiore controllo su una voce di costo dell’attività.'},
            {'titolo': 'Trasforma una superficie disponibile in una risorsa energetica',
             'paragrafi': ['Coperture industriali, capannoni, pensiline e altre superfici compatibili possono essere utilizzate per produrre energia senza modificare la destinazione principale dell’attività.'],
             'forte': 'Il progetto parte sempre dalla verifica tecnica delle superfici, dei consumi, delle caratteristiche elettriche e delle reali esigenze dell’azienda.'},
            {'titolo': 'Produci dove consumi',
             'paragrafi': ['Molte imprese concentrano una parte importante dei consumi proprio durante le ore diurne, quando l’impianto fotovoltaico produce energia.',
                           'Quando produzione e consumi coincidono, l’energia può essere utilizzata direttamente dall’attività, riducendo il prelievo dalla rete.'],
             'forte': 'L’energia più interessante è spesso quella che produci e utilizzi nello stesso momento.'},
        ],
    },
    'accumulo': {
        'id': 'produzione-accumulo',
        'eyebrow': 'Fotovoltaico + accumulo',
        'titolo': 'Produzione e accumulo possono lavorare insieme',
        'paragrafi': [
            'Quando il profilo energetico dell’azienda lo rende conveniente, un sistema di accumulo può conservare parte dell’energia prodotta dal fotovoltaico e renderla disponibile in momenti diversi.',
            'Potenza e capacità dell’accumulo devono essere definite sulla base dei consumi reali, delle curve di carico e degli obiettivi dell’intervento.',
        ],
        'intro': 'L’accumulo può servire a:',
        'voci': ['aumentare l’utilizzo dell’energia prodotta', 'spostare nel tempo parte dell’energia disponibile',
                 'contribuire alla gestione dei prelievi', 'integrarsi con altre esigenze energetiche dell’attività'],
    },
    'cambia': {
        'eyebrow': 'In sintesi',
        'titolo': 'Cosa cambia per l’impresa?',
        'voci': [
            ('sole', 'Produci', 'Una parte dell’energia direttamente presso la tua attività.'),
            ('spina', 'Utilizzi', 'Sfrutti l’energia prodotta quando coincide con i consumi aziendali.'),
            ('batteria', 'Accumuli', 'Quando opportuno, conservi una parte dell’energia per utilizzarla in momenti diversi.'),
            ('giu', 'Riduci', 'Diminuisci la quantità di energia acquistata dalla rete.'),
            ('ingranaggio', 'Gestisci', 'Porti produzione, consumi e manutenzione all’interno di una strategia energetica coordinata.'),
        ],
    },
    'finale': {
        'id': 'valore-energia',
        'titolo': 'L’energia è un costo dell’attività. Produrre direttamente una parte di quella che utilizzi significa iniziare a gestirlo in modo diverso.',
        'frase': 'Il fotovoltaico genera valore quando produce. L’O&M serve a proteggerlo nel tempo.',
    },
    'revamping': {
        'id': 'revamping',
        'eyebrow': 'Revamping',
        'titolo': 'Quando un impianto esistente può essere migliorato',
        'paragrafi': ['Un impianto già in esercizio può richiedere nel tempo sostituzioni, adeguamenti o interventi di aggiornamento tecnologico.',
                      'Prima di intervenire è necessario verificare lo stato dell’impianto, le caratteristiche dei componenti esistenti e gli obiettivi dell’intervento.'],
    },
}
