# -*- coding: utf-8 -*-
"""Pagine dedicate dei servizi (una per ogni sottovoce del menu «Servizi»).

UNICA FONTE: la lista PAGINE_SERVIZI qui sotto. Da essa derivano la voce di menu, la pagina HTML, la sitemap e i
controlli. Aggiungere una voce = aggiungere un dizionario: la pagina viene generata dal build, senza altri interventi.

Foto reali dei lavori: copia i file (.jpg/.jpeg/.png/.webp) in  assets/lavori/<nome-pagina>/  e rigenera il sito
(python3 src/build.py). Sono mostrate al massimo MAX_FOTO; finché mancano compaiono i riquadri predisposti.
Sfondo dell'hero (facoltativo): assets/servizi/<nome-pagina>-hero.jpg (o .png/.webp); altrimenti gradiente.
"""
import os
import re

import dati as D
import comp as C

esc, qa = C.esc, C.qa
MAX_FOTO = 9
MIN_RIQUADRI = 3
FOTO_DIR = os.path.join(C.ROOT, 'assets', 'lavori')
FOTO_BASE = 'assets/lavori/'
EST = ('.jpg', '.jpeg', '.png', '.webp')

MACRO = {
    'privati': dict(nome='Privati', pagina='privati.html', opz_tipo='Privato'),
    'imprese': dict(nome='Imprese', pagina='imprese.html', opz_tipo='Impresa'),
    'pa': dict(nome='Pubblica Amministrazione', pagina='pubblica-amministrazione.html', opz_tipo='Pubblica Amministrazione'),
}

ICONE = {
    'sole': '<circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1"/>',
    'termico': '<path d="M12 3v12"/><circle cx="12" cy="18" r="3"/><path d="M8 7h4M8 10h3"/><path d="M17 4l1 2 2 1-2 1-1 2-1-2-2-1 2-1z"/>',
    'goccia': '<path d="M12 3c4 5 6 8 6 11a6 6 0 0 1-12 0c0-3 2-6 6-11z"/><path d="M9.5 14.5a2.5 2.5 0 0 0 2.5 2.5"/>',
    'camera': '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
    'chiave': '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
    'grafico': '<path d="M4 19V5M4 19h16"/><path d="M8 15l3-4 3 2 5-6"/>',
    'fabbrica': '<path d="M3 20V10l5 3V10l5 3V6h3v14zM3 20h18"/><path d="M7 17h1M11 17h1M15 17h1"/>',
    'ingranaggio': '<circle cx="12" cy="12" r="3"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1"/>',
    'rete': '<circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="18" r="2.5"/><circle cx="19" cy="18" r="2.5"/><path d="M11 7.2L6 15.8M13 7.2l5 8.6M7.5 18h9"/>',
    'edificio': '<path d="M4 20V9l8-5 8 5v11M2 20h20"/><path d="M8 20v-6h8v6M12 9v.01"/>',
    'scudo': '<path d="M12 3l8 3v6c0 4.5-3.4 7.8-8 9-4.6-1.2-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    'schermo': '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/><path d="M6 12l3-3 3 2 4-4"/>',
}
SPUNTA = '<path d="M5 12.5l4.5 4.5L19 7.5"/>'

PAGINE_SERVIZI = [
    # ------------------------------------------------------------------ PRIVATI
    dict(file='fotovoltaico-residenziale.html', macro='privati', menu='Fotovoltaico Residenziale', icona='sole',
         opzione='Fotovoltaico domestico', h1='Fotovoltaico per la casa',
         title='Fotovoltaico Residenziale | Rivetti Impianti',
         desc='Impianti fotovoltaici residenziali progettati sulla tua abitazione: sopralluogo, progetto, installazione, pratiche e assistenza con Rivetti Impianti.',
         lead='Produrre in casa una parte dell’energia che consumi, con un impianto progettato sulle tue abitudini e sulle caratteristiche dell’edificio.',
         importanza=['Un impianto fotovoltaico trasforma la luce del sole in energia elettrica direttamente sulla copertura dell’abitazione. L’energia prodotta viene usata subito in casa, riducendo la quota da acquistare dalla rete, il cui prezzo può cambiare nel tempo.',
                     'Per questo il dimensionamento fa la differenza: un impianto troppo piccolo non risponde ai consumi, uno troppo grande non viene sfruttato. Partiamo sempre dalle abitudini della famiglia, dalla copertura e dal contesto elettrico, non da una soluzione standard.'],
         esigenze=['Ridurre la dipendenza dal prezzo dell’energia acquistata dalla rete',
                   'Avere un impianto pensato sui consumi reali della famiglia',
                   'Valutare se e come affiancare un sistema di accumulo',
                   'Sapere chi segue pratiche, collaudo e assistenza dopo l’installazione'],
         passi=[('Primo confronto', 'Raccogliamo consumi, abitudini e obiettivi, e ti spieghiamo cosa è realistico aspettarsi.'),
                ('Sopralluogo', 'Verifichiamo copertura, orientamento, ombreggiamenti, quadro elettrico e punto di consegna.'),
                ('Progetto e preventivo', 'Definiamo potenza, componenti e un preventivo chiaro, con le attività comprese.'),
                ('Installazione', 'Realizziamo l’impianto secondo il progetto, curando la sicurezza del cantiere.'),
                ('Collaudo, pratiche e assistenza', 'Mettiamo in servizio l’impianto, seguiamo le pratiche necessarie e restiamo a disposizione nel tempo.')]),
    dict(file='solare-termico.html', macro='privati', menu='Solare Termico', icona='termico',
         opzione='Solare termico', h1='Solare termico per l’acqua calda',
         title='Solare Termico per la Casa | Rivetti Impianti',
         desc='Impianti solare termico per la produzione di acqua calda sanitaria in casa: valutazione, progetto, installazione e integrazione con l’impianto esistente.',
         lead='Usare l’energia del sole per scaldare l’acqua di casa, integrando il sistema con l’impianto termico che hai già.',
         importanza=['Il solare termico non produce elettricità: raccoglie il calore del sole per scaldare l’acqua. È una soluzione pensata per l’acqua calda sanitaria, uno dei consumi che accompagnano la famiglia tutto l’anno.',
                     'Il risultato dipende da come viene collegato all’impianto esistente: caldaia, pompa di calore, accumulo dell’acqua. Per questo la valutazione parte sempre dall’abitazione, dai consumi di acqua calda e dagli spazi disponibili, e non da un prodotto da vendere.'],
         esigenze=['Produrre l’acqua calda anche con una fonte rinnovabile',
                   'Integrare il sistema con caldaia o pompa di calore già presenti',
                   'Capire se la copertura e gli spazi tecnici sono adatti',
                   'Avere un impianto idraulico realizzato a regola d’arte'],
         passi=[('Valutazione iniziale', 'Verifichiamo consumi di acqua calda, impianto termico presente e spazi disponibili.'),
                ('Sopralluogo', 'Controlliamo esposizione della copertura, percorso delle tubazioni e locale tecnico.'),
                ('Progetto', 'Scegliamo configurazione e componenti in funzione dell’impianto esistente.'),
                ('Installazione', 'Posiamo collettori, accumulo e collegamenti idraulici ed elettrici.'),
                ('Messa in servizio', 'Verifichiamo il funzionamento e ti spieghiamo come gestire l’impianto.')]),
    dict(file='lavaggio-moduli.html', macro='privati', menu='Lavaggio Moduli', icona='goccia',
         opzione='Lavaggio moduli fotovoltaici', h1='Lavaggio dei moduli fotovoltaici',
         title='Lavaggio Moduli Fotovoltaici Casa | Rivetti Impianti',
         desc='Pulizia professionale dei moduli fotovoltaici dell’impianto di casa: rimozione di polvere e depositi, in sicurezza, come parte della manutenzione.',
         lead='Una pulizia professionale dei moduli, eseguita in sicurezza e con attrezzature adatte, per mantenere l’impianto nelle migliori condizioni.',
         importanza=['Polvere, pollini, residui e depositi si accumulano sulla superficie dei moduli e possono ridurne la resa. Quanto incidano dipende dalla zona, dall’inclinazione e dalle stagioni: per questo non esiste un calendario uguale per tutti.',
                     'Pulire un impianto in copertura non è un lavoro da improvvisare: serve operare in sicurezza e senza rovinare i moduli. Usiamo acqua e attrezzature adatte e, quando utile, abbiniamo il lavaggio a un controllo visivo dell’impianto.'],
         esigenze=['Rimuovere sporco e depositi in modo sicuro e senza danneggiare i moduli',
                   'Sapere se e quando il lavaggio serve davvero',
                   'Abbinare la pulizia a un controllo dell’impianto',
                   'Evitare di salire in copertura senza le protezioni necessarie'],
         passi=[('Verifica dello stato', 'Valutiamo tipo di sporco, accessibilità della copertura e condizioni dei moduli.'),
                ('Preparazione in sicurezza', 'Predisponiamo le protezioni necessarie per lavorare in quota.'),
                ('Lavaggio', 'Puliamo i moduli con acqua e attrezzature adatte, senza ricorrere a metodi aggressivi.'),
                ('Controllo visivo', 'Osserviamo moduli, cablaggi e fissaggi e segnaliamo eventuali anomalie.'),
                ('Indicazioni', 'Ti diciamo ogni quanto conviene ripetere l’intervento nel tuo caso.')]),
    dict(file='termografia.html', macro='privati', menu='Termografia', icona='camera',
         opzione='Termografia impianti fotovoltaici', h1='Termografia dell’impianto fotovoltaico',
         title='Termografia Impianti Fotovoltaici Casa | Rivetti Impianti',
         desc='Termografia per impianti fotovoltaici residenziali: controllo non invasivo con termocamera per individuare anomalie termiche su moduli e componenti.',
         lead='Un controllo non invasivo con termocamera per far emergere anomalie termiche che a occhio nudo non si vedono.',
         importanza=['Un modulo o un collegamento che non funziona come dovrebbe spesso si scalda in modo anomalo. La termografia permette di vederlo: una termocamera mostra le differenze di temperatura sulla superficie dell’impianto, senza smontare nulla.',
                     'È uno strumento di verifica, non una diagnosi automatica: l’esito indica dove approfondire con controlli elettrici e di manutenzione. Per questo i risultati vengono letti da un tecnico e spiegati in modo semplice.'],
         esigenze=['Avere un’indicazione in più sullo stato dell’impianto',
                   'Individuare anomalie termiche senza interventi invasivi',
                   'Decidere dove concentrare i controlli successivi',
                   'Controllare un impianto già installato, anche non nostro'],
         passi=[('Preparazione', 'Concordiamo il momento adatto, con irraggiamento sufficiente per una lettura attendibile.'),
                ('Rilievo termico', 'Passiamo in rassegna moduli e componenti con la termocamera.'),
                ('Analisi delle immagini', 'Esaminiamo le immagini e individuiamo le zone con comportamento anomalo.'),
                ('Esito', 'Ti consegniamo una sintesi di quanto emerso, in linguaggio chiaro.'),
                ('Interventi successivi', 'Se serve, proponiamo i controlli o la manutenzione per risolvere le anomalie.')]),
    dict(file='manutenzione-assistenza.html', macro='privati', menu='Manutenzione e Assistenza', icona='chiave',
         opzione='Manutenzione ordinaria e straordinaria', h1='Manutenzione e assistenza degli impianti',
         title='Manutenzione e Assistenza Impianti Casa | Rivetti Impianti',
         desc='Manutenzione ordinaria e straordinaria e assistenza tecnica per impianti fotovoltaici e termici della casa, anche già installati da altri.',
         lead='Controlli periodici e interventi tecnici per tenere in ordine gli impianti di casa, anche se non li abbiamo installati noi.',
         importanza=['Un impianto funziona bene se viene seguito nel tempo. Inverter, collegamenti, protezioni e componenti sono soggetti a usura e possono avere anomalie che non danno segnali evidenti finché il problema non si aggrava.',
                     'Un controllo periodico permette di individuare per tempo ciò che non va e di intervenire in modo programmato, invece che a guasto avvenuto. Seguiamo sia impianti nuovi sia impianti già in esercizio.'],
         esigenze=['Avere un riferimento tecnico a cui rivolgersi in caso di problemi',
                   'Controllare lo stato di inverter, collegamenti e protezioni',
                   'Intervenire su impianti già installati da altri',
                   'Programmare le verifiche invece di inseguire i guasti'],
         passi=[('Segnalazione o richiesta', 'Ci racconti cosa succede o cosa vuoi far controllare.'),
                ('Verifica sull’impianto', 'Controlliamo componenti, parametri e collegamenti sul posto.'),
                ('Diagnosi', 'Individuiamo le cause di eventuali anomalie e ti spieghiamo cosa serve.'),
                ('Intervento', 'Eseguiamo le attività di manutenzione ordinaria o straordinaria concordate.'),
                ('Controllo finale', 'Verifichiamo il corretto funzionamento e indichiamo i prossimi controlli.')]),
    dict(file='monitoraggio.html', macro='privati', menu='Monitoraggio', icona='schermo',
         opzione='Altro', h1='Monitoraggio dell’impianto',
         title='Monitoraggio Impianto Fotovoltaico | Rivetti Impianti',
         desc='Monitoraggio dell’impianto fotovoltaico di casa: tieni sotto controllo produzione e consumi e individua per tempo anomalie di funzionamento.',
         lead='Vedere quanto produce e quanto consuma la tua casa, per accorgerti subito se qualcosa non funziona come dovrebbe.',
         importanza=['Senza un sistema di monitoraggio un impianto fotovoltaico è “a scatola chiusa”: se qualcosa smette di funzionare, spesso lo si scopre solo dalla bolletta. Con il monitoraggio produzione e consumi sono visibili in ogni momento, da telefono o computer.',
                     'Non serve a fare previsioni, ma a rendersi conto in fretta delle anomalie e a usare meglio l’energia prodotta. Configuriamo e verifichiamo il monitoraggio anche su impianti già installati, quando i componenti lo consentono.'],
         esigenze=['Controllare produzione e consumi senza andare in copertura',
                   'Accorgersi in fretta di un calo anomalo o di un fermo',
                   'Capire meglio come usare l’energia che l’impianto produce',
                   'Aggiungere il monitoraggio a un impianto già installato'],
         passi=[('Verifica dell’impianto', 'Controlliamo inverter e dispositivi presenti e cosa è possibile monitorare.'),
                ('Scelta della soluzione', 'Proponiamo il sistema di monitoraggio adatto all’impianto e alla rete di casa.'),
                ('Installazione e configurazione', 'Colleghiamo e configuriamo i dispositivi e l’accesso da telefono e computer.'),
                ('Prova e istruzioni', 'Verifichiamo che i dati arrivino correttamente e ti mostriamo come leggerli.'),
                ('Assistenza', 'Restiamo a disposizione per eventuali segnalazioni o aggiornamenti.')]),
    # ------------------------------------------------------------------ IMPRESE
    dict(file='fotovoltaico-industriale.html', macro='imprese', menu='Fotovoltaico Industriale', icona='fabbrica',
         opzione='Fotovoltaico industriale', h1='Fotovoltaico industriale',
         title='Fotovoltaico Industriale per Aziende | Rivetti Impianti',
         desc='Impianti fotovoltaici industriali su tetto o a terra per aziende e attività produttive: analisi dei consumi, progetto, pratiche, installazione e collaudo.',
         lead='Impianti fotovoltaici su coperture e aree aziendali, dimensionati sui consumi dell’attività e realizzati con tempi compatibili con la produzione.',
         importanza=['Per un’azienda l’energia è un costo che incide sull’attività e che può variare nel tempo. Produrre una parte dell’energia consumata, direttamente nel sito produttivo, è una scelta che rende l’impresa meno esposta a questa variabilità.',
                     'Un impianto industriale è un investimento tecnico: contano profilo di consumo, struttura della copertura, connessione alla rete e continuità dell’attività durante i lavori. Per questo il progetto parte dai dati dell’azienda, non da un catalogo.'],
         esigenze=['Dimensionare l’impianto sui consumi reali dell’attività',
                   'Utilizzare in modo utile coperture e aree di pertinenza',
                   'Gestire le pratiche autorizzative e di connessione alla rete',
                   'Realizzare i lavori senza fermare la produzione più del necessario'],
         passi=[('Analisi dei consumi', 'Studiamo bollette e profili di carico per capire quanto e quando l’azienda consuma.'),
                ('Sopralluogo e fattibilità', 'Verifichiamo coperture, strutture, quadri e punto di connessione.'),
                ('Progetto e dimensionamento', 'Definiamo potenza e componenti in funzione di spazi e fabbisogno.'),
                ('Pratiche e installazione', 'Seguiamo le pratiche necessarie e realizziamo l’opera rispettando tempi e sicurezza.'),
                ('Collaudo e assistenza', 'Mettiamo in servizio l’impianto, rilasciamo le dichiarazioni previste e restiamo a disposizione.')]),
    dict(file='operation-maintenance.html', macro='imprese', menu='Operation e Maintenance (O&M)', icona='ingranaggio',
         opzione='Operation & Maintenance fotovoltaico', h1='Operation & Maintenance (O&M)',
         title='Operation e Maintenance O&M Fotovoltaico | Rivetti Impianti',
         desc='Servizi di Operation & Maintenance per impianti fotovoltaici industriali: monitoraggio, manutenzione programmata, interventi su guasto e reportistica.',
         lead='Gestione tecnica continuativa degli impianti: monitoraggio, manutenzione programmata e interventi, con un unico riferimento.',
         importanza=['Un impianto industriale produce valore finché funziona come previsto. Un guasto non individuato in tempo può significare produzione persa per giorni, e un impianto trascurato perde efficienza senza far rumore.',
                     'Il servizio di O&M organizza il controllo nel tempo: monitoraggio dei parametri, manutenzione programmata e intervento in caso di anomalie, con report periodici sullo stato dell’impianto. È una gestione, non una chiamata a emergenza avvenuta.'],
         esigenze=['Avere un unico riferimento tecnico per la gestione dell’impianto',
                   'Individuare per tempo anomalie e cali di produzione',
                   'Programmare le attività di manutenzione preventiva',
                   'Disporre di report sullo stato dell’impianto'],
         passi=[('Presa in carico', 'Raccogliamo documentazione, schemi e storico dell’impianto da gestire.'),
                ('Piano di manutenzione', 'Definiamo attività e frequenze in funzione del tipo di impianto.'),
                ('Monitoraggio', 'Teniamo sotto controllo i parametri di produzione e segnaliamo gli scostamenti.'),
                ('Interventi', 'Eseguiamo manutenzione preventiva e interventi correttivi quando servono.'),
                ('Reportistica', 'Ti consegniamo report periodici su stato, attività svolte e indicazioni.')]),
    dict(file='lavaggio-moduli-imprese.html', macro='imprese', menu='Lavaggio Moduli', icona='goccia',
         opzione='Lavaggio moduli fotovoltaici (impresa)', h1='Lavaggio moduli per impianti industriali',
         title='Lavaggio Moduli Fotovoltaici Industriali | Rivetti Impianti',
         desc='Lavaggio professionale dei moduli di impianti fotovoltaici industriali e a terra: attrezzature dedicate, sicurezza in quota e programmazione degli interventi.',
         lead='Pulizia professionale di grandi superfici fotovoltaiche, programmata in modo da non interferire con l’attività.',
         importanza=['Su coperture industriali e campi a terra lo sporco si accumula in modo diverso a seconda del contesto: polveri di lavorazione, traffico, agricoltura, volatili. Può ridurre la resa dei moduli, e quanto incide va valutato impianto per impianto.',
                     'Lavare molte centinaia di moduli richiede organizzazione, attrezzature adatte e procedure di sicurezza per il lavoro in quota. Pianifichiamo l’intervento con l’azienda, scegliendo tempi e modalità che non intralcino la produzione.'],
         esigenze=['Pulire grandi superfici in modo organizzato e sicuro',
                   'Valutare quando il lavaggio è davvero utile sull’impianto',
                   'Programmare l’intervento senza fermare l’attività',
                   'Inserire il lavaggio nel piano di manutenzione'],
         passi=[('Sopralluogo', 'Verifichiamo accessi, estensione, tipo di sporco e rischi del sito.'),
                ('Piano dell’intervento', 'Concordiamo date, aree e modalità operative con l’azienda.'),
                ('Lavaggio', 'Puliamo i moduli con attrezzature professionali e acqua adatta.'),
                ('Controllo', 'Osserviamo moduli e componenti e segnaliamo eventuali anomalie.'),
                ('Rapporto', 'Documentiamo l’intervento e indichiamo la frequenza consigliata.')]),
    dict(file='termografia-imprese.html', macro='imprese', menu='Termografia', icona='camera',
         opzione='Termografia impianti fotovoltaici (impresa)', h1='Termografia per impianti industriali',
         title='Termografia Impianti Fotovoltaici Industriali | Rivetti Impianti',
         desc='Termografia di impianti fotovoltaici industriali con termocamera: individuazione di anomalie termiche su moduli, stringhe e quadri a supporto della manutenzione.',
         lead='Diagnostica termica su grandi impianti, per individuare moduli e componenti con comportamento anomalo prima che diventino un problema.',
         importanza=['Su un impianto di grandi dimensioni è impossibile ispezionare ogni modulo a vista. La termografia permette di individuare celle calde, moduli o collegamenti con temperatura anomala, che possono indicare un difetto.',
                     'È un controllo non invasivo, a supporto dei piani di manutenzione: indica dove approfondire e consente di programmare gli interventi. I risultati vengono letti da un tecnico e consegnati in un rapporto.'],
         esigenze=['Ispezionare grandi superfici senza fermare l’impianto',
                   'Individuare celle calde e collegamenti anomali',
                   'Dare priorità agli interventi di manutenzione',
                   'Avere un rapporto documentato sullo stato dei moduli'],
         passi=[('Pianificazione', 'Scegliamo condizioni e momento adatti a un rilievo attendibile.'),
                ('Rilievo termico', 'Eseguiamo il rilievo con termocamera su moduli, stringhe e quadri.'),
                ('Analisi', 'Esaminiamo le immagini e classifichiamo le anomalie individuate.'),
                ('Rapporto', 'Consegniamo un rapporto con immagini e indicazioni.'),
                ('Azioni correttive', 'Se richiesto, programmiamo gli interventi per risolvere le anomalie.')]),
    dict(file='comunita-energetiche.html', macro='imprese', menu='Comunità Energetiche Rinnovabili (CER)', icona='rete',
         opzione='Comunità Energetiche Rinnovabili', h1='Comunità Energetiche Rinnovabili (CER)',
         title='Comunità Energetiche Rinnovabili CER | Rivetti Impianti',
         desc='Supporto tecnico per Comunità Energetiche Rinnovabili: studio di fattibilità, progetto dell’impianto, coordinamento dei soggetti e supporto alle pratiche.',
         lead='Condividere energia rinnovabile tra più soggetti dello stesso territorio: supporto tecnico dallo studio di fattibilità alla messa in servizio.',
         importanza=['Una Comunità Energetica Rinnovabile mette in relazione chi produce energia e chi la consuma all’interno di una stessa configurazione. L’energia condivisa può essere valorizzata secondo le regole e gli strumenti di sostegno previsti dalla normativa.',
                     'È un progetto che unisce aspetti tecnici, organizzativi e amministrativi. Il nostro ruolo è l’ambito tecnico e impiantistico: valutare la fattibilità, progettare e realizzare gli impianti e supportare il coordinamento. Condizioni e incentivi vanno verificati caso per caso.'],
         esigenze=['Capire se una CER è fattibile nel proprio contesto',
                   'Dimensionare gli impianti di produzione della comunità',
                   'Coordinare produttori e consumatori coinvolti',
                   'Avere un riferimento tecnico per pratiche e messa in servizio'],
         passi=[('Studio di fattibilità', 'Valutiamo soggetti coinvolti, consumi, siti disponibili e configurazione possibile.'),
                ('Progetto degli impianti', 'Dimensioniamo gli impianti di produzione in funzione della comunità.'),
                ('Coordinamento', 'Supportiamo il confronto tra i soggetti e le attività tecniche necessarie.'),
                ('Pratiche tecniche', 'Seguiamo gli aspetti tecnici delle pratiche di connessione e configurazione.'),
                ('Realizzazione e avvio', 'Realizziamo gli impianti e li mettiamo in servizio.')]),
    # ------------------------------------------------------------------ PUBBLICA AMMINISTRAZIONE
    dict(file='fotovoltaico-pa.html', macro='pa', menu='Fotovoltaico PA', icona='edificio',
         opzione='Fotovoltaico per edifici e strutture pubbliche', h1='Fotovoltaico per la Pubblica Amministrazione',
         title='Fotovoltaico per Enti e Pubblica Amministrazione | Rivetti Impianti',
         desc='Impianti fotovoltaici per scuole, municipi, impianti sportivi e strutture pubbliche: verifica delle superfici, progetto, realizzazione e collaudo.',
         lead='Impianti fotovoltaici su edifici e aree pubbliche, progettati nel rispetto delle condizioni tecniche e amministrative dell’Ente.',
         importanza=['Coperture, pensiline e altre superfici idonee possono diventare una risorsa per produrre energia direttamente dove viene consumata: scuole, uffici comunali, impianti sportivi, strutture di servizio.',
                     'Per un Ente il progetto non è solo tecnico: occorre tenere conto di vincoli, autorizzazioni e procedure. Partiamo dalla verifica di superfici, consumi e condizioni applicabili, per definire un intervento sostenibile e ben documentato.'],
         esigenze=['Utilizzare superfici pubbliche disponibili per produrre energia',
                   'Valutare fattibilità tecnica e condizioni amministrative',
                   'Avere progetto e documentazione tecnica completi',
                   'Contare su un riferimento unico dal progetto al collaudo'],
         passi=[('Sopralluogo e raccolta dati', 'Verifichiamo edifici, superfici, consumi e caratteristiche elettriche.'),
                ('Fattibilità', 'Valutiamo le condizioni tecniche e amministrative dell’intervento.'),
                ('Progettazione', 'Definiamo e dimensioniamo l’impianto, con la documentazione necessaria.'),
                ('Realizzazione', 'Eseguiamo i lavori nel rispetto di sicurezza e tempi concordati con l’Ente.'),
                ('Collaudo e manutenzione', 'Mettiamo in servizio l’impianto e seguiamo l’assistenza nel tempo.')]),
    dict(file='riqualificazione-energetica.html', macro='pa', menu='Riqualificazione Energetica', icona='grafico',
         opzione='Riqualificazione energetica edifici pubblici', h1='Riqualificazione energetica degli edifici pubblici',
         title='Riqualificazione Energetica Edifici Pubblici | Rivetti Impianti',
         desc='Riqualificazione energetica di edifici e strutture pubbliche: analisi dell’uso dell’energia, impianti termici, climatizzazione, pompe di calore e fotovoltaico.',
         lead='Interventi sugli impianti degli edifici pubblici, partendo da come l’edificio utilizza davvero l’energia.',
         importanza=['Prima di intervenire occorre capire come un edificio consuma energia, quali impianti ha e dove esistono margini di miglioramento. Un intervento efficace nasce da questa conoscenza, non da una soluzione scelta in anticipo.',
                     'Il nostro ambito è quello energetico e impiantistico: climatizzazione, pompe di calore, impianti termici, acqua calda sanitaria, regolazione e fotovoltaico. Eventuali opere edili collegate vanno valutate caso per caso con i soggetti competenti.'],
         esigenze=['Capire come l’edificio utilizza energia e dove migliorare',
                   'Coordinare impianti diversi in un progetto unitario',
                   'Migliorare il comfort di chi usa gli spazi',
                   'Avere un riferimento tecnico unico per le attività impiantistiche'],
         passi=[('Analisi dello stato di fatto', 'Raccogliamo dati su edificio, impianti e consumi.'),
                ('Individuazione degli interventi', 'Indichiamo le opere impiantistiche con maggiore margine di miglioramento.'),
                ('Progettazione', 'Definiamo gli interventi e ne coordiniamo l’integrazione.'),
                ('Realizzazione', 'Eseguiamo le attività impiantistiche e coordiniamo le lavorazioni complementari.'),
                ('Verifica e gestione', 'Verifichiamo il funzionamento e seguiamo la gestione nel tempo.')]),
    dict(file='manutenzione-assistenza-pa.html', macro='pa', menu='Manutenzione e Assistenza', icona='scudo',
         opzione='Gestione e manutenzione impianti per enti pubblici', h1='Manutenzione e assistenza per gli Enti',
         title='Manutenzione e Assistenza Impianti Enti Pubblici | Rivetti Impianti',
         desc='Manutenzione programmata e assistenza per impianti di edifici e strutture pubbliche: verifiche periodiche, diagnostica e interventi tecnici.',
         lead='Verifiche periodiche e interventi tecnici per garantire la continuità di servizio degli impianti pubblici.',
         importanza=['Gli impianti di scuole, uffici e strutture pubbliche devono essere sempre disponibili e in sicurezza. Un guasto non programmato può interrompere servizi essenziali e comporta interventi urgenti e costosi.',
                     'Un piano di controlli periodici consente di individuare per tempo le anomalie e di intervenire in modo programmato. Seguiamo impianti energetici e tecnologici, anche già esistenti, con attività documentate.'],
         esigenze=['Garantire la continuità di servizio degli impianti',
                   'Programmare verifiche e manutenzioni periodiche',
                   'Intervenire su impianti già esistenti',
                   'Avere attività tracciate e documentate'],
         passi=[('Censimento degli impianti', 'Raccogliamo documentazione e stato degli impianti da seguire.'),
                ('Piano di manutenzione', 'Definiamo verifiche e frequenze in funzione di tipologia e uso.'),
                ('Verifiche periodiche', 'Eseguiamo controlli e diagnostica secondo il piano.'),
                ('Interventi', 'Interveniamo sulle anomalie con manutenzione ordinaria e straordinaria.'),
                ('Documentazione', 'Registriamo le attività svolte e le indicazioni per l’Ente.')]),
]


# ------------------------------------------------------------------ utilità
def slug(s):
    return s['file'][:-5]


def per_macro(macro):
    return [s for s in PAGINE_SERVIZI if s['macro'] == macro]


def menu():
    """Struttura del menu «Servizi» derivata dalle pagine: [{titolo, pagina, voci:[(etichetta, file)]}]."""
    return [dict(titolo=MACRO[m]['nome'], pagina=MACRO[m]['pagina'], voci=[(s['menu'], s['file']) for s in per_macro(m)]) for m in MACRO]


def foto(s):
    """Foto reali in assets/lavori/<pagina>/ (escluse le versioni ridimensionate -480/-800/-1200/-1600 e i .webp gemelli)."""
    d = os.path.join(FOTO_DIR, slug(s))
    if not os.path.isdir(d):
        return []
    f = [x for x in sorted(os.listdir(d)) if x.lower().endswith(EST) and not re.search(r'-(480|800|1200|1600)\.[a-z]+$', x, re.I)]
    stems = {os.path.splitext(x)[0] for x in f if not x.lower().endswith('.webp')}
    f = [x for x in f if not (x.lower().endswith('.webp') and os.path.splitext(x)[0] in stems)]
    return f[:MAX_FOTO]


def hero_file(s):
    for ext in ('.jpg', '.jpeg', '.png', '.webp'):
        rel = slug(s) + '-hero' + ext
        if os.path.isfile(os.path.join(C.SERVIZI_DIR, rel)):
            return rel
    return None


def errori():
    """Controlli sui dati: ogni voce completa, file e opzione del modulo validi."""
    err = []
    opzioni = set(x['opzione'] for x in D.SERVIZI_PRIVATI + D.SERVIZI_IMPRESE) | set(D.OPZIONI_PA) | set(D.OPZIONI_EXTRA)
    visti = set()
    for s in PAGINE_SERVIZI:
        for k in ('file', 'macro', 'menu', 'icona', 'opzione', 'h1', 'title', 'desc', 'lead', 'importanza', 'esigenze', 'passi'):
            if not s.get(k):
                err.append(f'{s.get("file")}: manca «{k}»')
        if s['file'] in visti:
            err.append(f'{s["file"]}: file duplicato')
        visti.add(s['file'])
        if not re.fullmatch(r'[a-z0-9-]+\.html', s['file']):
            err.append(f'{s["file"]}: nome file non valido')
        if s['macro'] not in MACRO:
            err.append(f'{s["file"]}: macro sconosciuta')
        if s['opzione'] not in opzioni:
            err.append(f'{s["file"]}: l’opzione «{s["opzione"]}» non esiste nel modulo di contatto')
        if s['icona'] not in ICONE:
            err.append(f'{s["file"]}: icona sconosciuta')
        if len(s['desc']) > 170:
            err.append(f'{s["file"]}: description troppo lunga ({len(s["desc"])})')
    return err


# ------------------------------------------------------------------ rendering
def _svg(nome, cls):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICONE[nome]}</svg>'


def _hero(s):
    m = MACRO[s['macro']]
    hf = hero_file(s)
    sfondo = f' style="--sv-img:url(\'assets/servizi/{qa(hf)}\')"' if hf else ''
    cls = 'sv-hero sv-' + s['macro'] + (' has-img' if hf else '')
    bc = ('<nav class="sv-crumbs" aria-label="Percorso di navigazione"><ol><li><a href="index.html">Home</a></li>'
          f'<li><a href="{m["pagina"]}">{esc(m["nome"])}</a></li><li aria-current="page">{esc(s["menu"])}</li></ol></nav>')
    wa = qa(C.wa_for(s['macro']))
    return f'''<section class="{cls}"{sfondo}>
  <div class="sv-hero-in">
    <div class="sv-hero-text">
      {bc}
      <span class="sv-tag">{esc(m['nome'])}</span>
      <h1>{esc(s['h1'])}</h1>
      <p class="sv-lead">{esc(s['lead'])}</p>
      <div class="sv-cta-row"><a class="btn btn-light" href="#contatti" data-service="{qa(s['opzione'])}">Richiedi una consulenza gratuita &rarr;</a>
        <a class="btn btn-ghost" href="{wa}" target="_blank" rel="noopener">{C.WA}Parla con un tecnico</a></div>
    </div>
    <div class="sv-hero-vis" aria-hidden="true">{_svg(s['icona'], 'sv-big')}</div>
  </div>
</section>'''


def _perche(s):
    par = ''.join(f'<p>{esc(t)}</p>' for t in s['importanza'])
    li = ''.join(f'<li><span class="ico">{C.ico(SPUNTA)}</span><span>{esc(x)}</span></li>' for x in s['esigenze'])
    return f'''<section class="sec sv-why" id="importanza">
  <div class="sv-why-in">
    <div class="sv-why-text">
      <span class="eyebrow">Perché è importante</span>
      <h2>{esc(s['h1'])}: cosa significa davvero</h2>
      {par}
    </div>
    <aside class="sv-needs" aria-labelledby="sv-needs-t">
      <h3 id="sv-needs-t">Le esigenze a cui risponde</h3>
      <ul>{li}</ul>
    </aside>
  </div>
</section>'''


def _come(s):
    li = ''.join(f'<li class="sv-step"><span class="sv-n" aria-hidden="true">{i}</span><h3>{esc(t)}</h3><p>{esc(x)}</p></li>'
                 for i, (t, x) in enumerate(s['passi'], 1))
    return f'''<section class="sec sv-how" id="come-interveniamo">
  {C.sec_head('Modalità di intervento', 'Come interveniamo', 'Un percorso definito, con un unico riferimento tecnico dall’inizio alla fine.')}
  <ol class="sv-steps">{li}</ol>
</section>'''


def _foto(s):
    nome = slug(s)
    files = foto(s)
    root = os.path.join(FOTO_DIR, nome)
    base = f'{FOTO_BASE}{nome}/'
    li = ''
    for i, f in enumerate(files):
        alt = f'Intervento di {s["menu"].lower()} eseguito da Rivetti Impianti'
        img = C.img_responsive(f, alt, root, base, sizes='(max-width:700px) 100vw, 360px', cls='sv-img')
        li += (f'<li><button type="button" class="gal-btn sv-ph" data-gal="{nome}" data-nocap="1" data-full="{base}{qa(f)}" '
               f'data-alt="{qa(alt)}" aria-label="Ingrandisci la foto {i + 1}">{img}</button></li>')
    vuoti = max(0, MIN_RIQUADRI - len(files))
    li += ('<li class="sv-empty" aria-hidden="true"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 8h3l2-3h6l2 3h3v11H4z"/>'
           '<circle cx="12" cy="13" r="3.5"/></svg><span>Foto in arrivo</span></li>') * vuoti
    testo = ('Alcune immagini degli interventi realizzati da Rivetti Impianti.' if files
             else 'Le foto dei nostri interventi saranno presto disponibili in questa sezione.')
    head = C.sec_head('Sul campo', 'Foto dei nostri interventi', testo)
    lb = C.lightbox_dialog() if files else ''
    return f'''<section class="sec sv-foto" id="foto-lavori">
  {head}
  <ul class="sv-grid">{li}</ul>
  {lb}
</section>'''


def _altri(s):
    altri = [x for x in per_macro(s['macro']) if x['file'] != s['file']]
    m = MACRO[s['macro']]
    ch = ''.join(f'<li><a href="{x["file"]}">{esc(x["menu"])}</a></li>' for x in altri)
    return f'''<section class="sec sv-altri" aria-labelledby="sv-altri-t">
  <h2 id="sv-altri-t">Altri servizi: {esc(m['nome'])}</h2>
  <ul class="sv-chips">{ch}<li><a class="sv-all" href="{m['pagina']}">Tutti i servizi &rarr;</a></li></ul>
</section>'''


def _cta(s):
    wa = qa(C.wa_for(s['macro']))
    return f'''<section class="sec sv-cta" aria-labelledby="sv-cta-t">
  <div class="sv-cta-in">
    <h2 id="sv-cta-t">Richiedi una consulenza o un preventivo gratuito</h2>
    <p>Raccontaci la tua situazione: un tecnico ti ascolta, valuta il caso e ti propone la soluzione più adatta, senza impegno.</p>
    <div class="sv-cta-row"><a class="btn btn-light" href="#contatti" data-service="{qa(s['opzione'])}">Richiedi una consulenza gratuita &rarr;</a>
      <a class="btn btn-ghost" href="{wa}" target="_blank" rel="noopener">{C.WA}Scrivici su WhatsApp</a></div>
  </div>
</section>'''


def corpo(s, p):
    contatto = C.contact_section(p, 'Parliamo del tuo progetto',
                                 'Chiamaci, scrivici su WhatsApp o compila il modulo: ti ricontatteremo per una consulenza e un preventivo senza impegno.',
                                 tipo=MACRO[s['macro']]['opz_tipo'])
    return '\n'.join(x for x in [_hero(s), _perche(s), _come(s), _foto(s), _cta(s), contatto, _altri(s)] if x)
