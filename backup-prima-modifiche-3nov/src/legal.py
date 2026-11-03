"""Genera privacy.html, cookie.html, note-legali.html (stesso stile del sito)."""
import re

UPD = '2 ottobre 2026'
OWNER_IDS = '''<div class="ids">
<p><strong>RM IMPIANTI DI ALESSANDRO RIVETTI S.A.S.</strong>, operante anche con il segno distintivo commerciale &ldquo;Rivetti Impianti &mdash; Technical Engineering&rdquo;.</p>
<p>Sede: Via Landolfo, 81034 Mondragone (CE)</p>
<p>P. IVA / C.F.: 03428210615 &middot; REA: CE-243308</p>
<p>Email: <a class="l" href="mailto:rivettiimpianti@gmail.com">rivettiimpianti@gmail.com</a></p>
<p>PEC: <a class="l" href="mailto:rmimpiantisas@pec.it">rmimpiantisas@pec.it</a></p>
</div>'''

def page(title, desc, h1, sections, intro, current):
    toc = ''.join(f'<li><a href="#{sid}">{t}</a></li>' for sid, t, _ in sections)
    body = ''.join(f'<h2 id="{sid}">{i}. {t}</h2>\n{b}\n' for i, (sid, t, b) in enumerate(sections, 1))
    links = {
        'privacy': '<a class="l" href="cookie.html">Cookie Policy</a> &middot; <a class="l" href="note-legali.html">Note legali</a>',
        'cookie': '<a class="l" href="privacy.html">Privacy Policy</a> &middot; <a class="l" href="note-legali.html">Note legali</a>',
        'note': '<a class="l" href="privacy.html">Privacy Policy</a> &middot; <a class="l" href="cookie.html">Cookie Policy</a>',
    }[current]
    return f'''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Rivetti Impianti</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="site.css">
<style>body{{background:var(--sky)}}</style>
</head>
<body>
<header class="bar">
  <a href="index.html" aria-label="Rivetti Impianti — home"><span><img src="assets/logo-rivetti-dark.png" alt="Rivetti Impianti – Technical Engineering" onerror="this.parentNode.classList.add('nologo')"><span class="fallback-logo">RIVETTI <em>IMPIANTI</em></span></span></a>
  <a class="back" href="index.html">&larr; Torna al sito</a>
</header>
<main class="legal-wrap"><article>
<h1>{h1}</h1>
<p class="upd">Ultimo aggiornamento: <strong>{UPD}</strong></p>
{intro}
<div class="toc-box"><b>In questa pagina</b><ol class="toc">{toc}</ol></div>
{body}
<p class="upd" style="margin-top:30px">Vedi anche: {links}</p>
</article></main>
{FOOT}
</body>
</html>
'''

FOOT = '''<footer class="sfoot">
  <p><strong>Rivetti Impianti</strong> &mdash; RM Impianti di Alessandro Rivetti S.a.s. &middot; P. IVA/C.F. 03428210615 &middot; REA CE-243308</p>
  <p>Via Landolfo, 81034 Mondragone (CE) &middot; <a href="mailto:rivettiimpianti@gmail.com">rivettiimpianti@gmail.com</a> &middot; PEC <a href="mailto:rmimpiantisas@pec.it">rmimpiantisas@pec.it</a></p>
  <p><a href="privacy.html">Privacy Policy</a> &middot; <a href="cookie.html">Cookie Policy</a> &middot; <a href="note-legali.html">Note legali</a></p>
</footer>'''

# Blocchi che dipendono dalla configurazione tecnica: lo script scarica-risorse-locali.py li sostituisce quando font e librerie diventano locali.
EXT_PRIVACY_EXTERNAL = '''<li><strong>Google Fonts (Google Ireland Limited)</strong>: il browser dell&rsquo;utente scarica i caratteri tipografici direttamente dai server di Google, che riceve l&rsquo;indirizzo IP e i dati tecnici della richiesta.</li>
<li><strong>jsDelivr (rete di distribuzione di contenuti, CDN)</strong>: da essa il browser scarica la libreria grafica del globo 3D e le relative immagini; il fornitore riceve l&rsquo;indirizzo IP e i dati tecnici della richiesta.</li>'''
EXT_PRIVACY_LOCAL = '''<li><strong>Caratteri, librerie e immagini</strong>: sono ospitati direttamente sul sito; per visualizzarli non vengono effettuate connessioni a servizi di terzi.</li>'''
EXT_COOKIE_EXTERNAL = '''<li><strong>Google Fonts (Google Ireland Limited)</strong>: caratteri tipografici scaricati dai server di Google; il fornitore riceve l&rsquo;indirizzo IP e i dati tecnici del browser.</li>
<li><strong>jsDelivr (CDN)</strong>: libreria grafica del globo 3D e relative immagini scaricate dai server del fornitore, che riceve l&rsquo;indirizzo IP e i dati tecnici del browser.</li>'''
EXT_COOKIE_LOCAL = '''<li>Caratteri, librerie e immagini del sito sono ospitati direttamente sul sito: per visualizzarli non vengono effettuate connessioni a servizi di terzi.</li>'''

def ext(name, inner):
    return f'<!--EXT:{name}-->\n{inner}\n<!--/EXT-->'

# ----------------------------------------------------------------- PRIVACY
P = []
P.append(('titolare', 'Titolare del trattamento', f'''<p>Il Titolare del trattamento &egrave;:</p>
{OWNER_IDS}
<p>Di seguito anche il &ldquo;Titolare&rdquo; o &ldquo;Rivetti Impianti&rdquo;.</p>'''))
P.append(('dati', 'Tipologie di dati trattati', '''<p>A seconda delle modalit&agrave; con cui l&rsquo;utente utilizza il sito o entra in contatto con Rivetti Impianti, possono essere trattate le seguenti categorie di dati.</p>
<h3>2.1 Dati di navigazione e dati tecnici</h3>
<p>I sistemi informatici e le procedure software utilizzate per il funzionamento del sito possono acquisire, nel corso del loro normale esercizio, alcune informazioni la cui trasmissione &egrave; implicita nell&rsquo;utilizzo dei protocolli Internet.</p>
<p>Possono rientrare in questa categoria, a titolo esemplificativo:</p>
<ul><li>indirizzo IP;</li><li>tipo di browser e dispositivo;</li><li>sistema operativo;</li><li>data e ora della richiesta;</li><li>pagina di provenienza e pagina richiesta;</li><li>informazioni tecniche relative alla connessione;</li><li>eventuali log necessari alla sicurezza e al corretto funzionamento del sito.</li></ul>
<p>Tali informazioni sono trattate principalmente per consentire il funzionamento e la sicurezza del sito, diagnosticare anomalie, prevenire abusi e, ove necessario, accertare eventuali responsabilit&agrave; in caso di utilizzi illeciti.</p>
<h3>2.2 Richieste di informazioni, preventivi e sopralluoghi</h3>
<p>Quando l&rsquo;utente utilizza il modulo di contatto o comunica con Rivetti Impianti tramite telefono, email o altri canali, possono essere raccolti:</p>
<ul><li>nome e cognome;</li><li>numero di telefono;</li><li>indirizzo email;</li><li>servizio richiesto;</li><li>contenuto del messaggio;</li><li>eventuali ulteriori informazioni volontariamente comunicate dall&rsquo;interessato.</li></ul>
<p>Tali dati vengono utilizzati esclusivamente per gestire la richiesta, fornire informazioni, organizzare eventuali sopralluoghi, elaborare preventivi e svolgere le attivit&agrave; precontrattuali richieste dall&rsquo;interessato.</p>
<p><strong>Base giuridica:</strong> art. 6, par. 1, lett. b), GDPR &mdash; esecuzione di misure precontrattuali adottate su richiesta dell&rsquo;interessato.</p>
<p>Il consenso non &egrave; pertanto necessario per trattare i dati strettamente necessari a rispondere alla richiesta. La casella da spuntare nel modulo serve solo ad attestare la presa visione della presente informativa.</p>
<h3>2.3 Rapporti contrattuali, amministrativi e assistenza</h3>
<p>Qualora alla richiesta segua l&rsquo;instaurazione di un rapporto contrattuale, i dati potranno essere trattati per:</p>
<ul><li>predisposizione ed esecuzione del contratto;</li><li>gestione tecnica e amministrativa della commessa;</li><li>fatturazione e contabilit&agrave;;</li><li>gestione di interventi, manutenzioni e assistenza;</li><li>adempimenti fiscali, civilistici e amministrativi;</li><li>gestione di eventuali garanzie, contestazioni e controversie.</li></ul>
<p><strong>Basi giuridiche:</strong> art. 6, par. 1, lett. b) e c), GDPR e, quando applicabile, art. 6, par. 1, lett. f), GDPR per la tutela dei diritti e degli interessi legittimi del Titolare.</p>
<h3>2.4 Contatti tramite WhatsApp</h3>
<p>Qualora l&rsquo;utente scelga volontariamente di contattare Rivetti Impianti tramite WhatsApp, i dati comunicati saranno utilizzati esclusivamente per gestire la conversazione e la relativa richiesta.</p>
<p>L&rsquo;utilizzo del servizio comporta anche un trattamento di dati da parte del fornitore della piattaforma WhatsApp secondo le condizioni e informative privacy applicabili al relativo servizio. Il sito contiene soltanto un collegamento: nessuna connessione a WhatsApp viene stabilita finch&eacute; l&rsquo;utente non lo seleziona.</p>
<p>L&rsquo;utente &egrave; libero di utilizzare, in alternativa, telefono, email o PEC.</p>
<h3>2.5 Recensioni e testimonianze</h3>
<p>Attraverso l&rsquo;apposita sezione del sito l&rsquo;utente pu&ograve; inviare una recensione indicando, tra l&rsquo;altro:</p>
<ul><li>valutazione espressa;</li><li>nome o nome da visualizzare;</li><li>tipologia di cliente;</li><li>contenuto della recensione.</li></ul>
<p>La recensione viene preventivamente esaminata dallo staff e non &egrave; automaticamente pubblicata.</p>
<p>La pubblicazione sul sito del nome indicato e del contenuto della recensione avviene esclusivamente previo consenso dell&rsquo;interessato, espresso con apposita casella, non preselezionata, presente nel modulo. La data e l&rsquo;ora del consenso sono registrate e inviate al Titolare insieme alla recensione.</p>
<p><strong>Base giuridica:</strong> art. 6, par. 1, lett. a), GDPR &mdash; consenso.</p>
<p>Il consenso pu&ograve; essere revocato in qualsiasi momento scrivendo ai recapiti del Titolare. La revoca non pregiudica la liceit&agrave; del trattamento effettuato prima della revoca.</p>
<p>L&rsquo;interessato &egrave; invitato a non inserire nella recensione dati personali di terzi, informazioni riservate, dati particolari o informazioni non necessarie alla descrizione della propria esperienza.</p>
<p>Poich&eacute; le recensioni pubblicate sono accessibili pubblicamente, esse possono essere indicizzate o memorizzate temporaneamente anche da motori di ricerca o servizi di terzi sui quali il Titolare non esercita un controllo diretto.</p>
<h3>2.6 Candidature e curriculum vitae</h3>
<p>Gli interessati possono trasmettere spontaneamente il proprio curriculum vitae all&rsquo;indirizzo indicato nella sezione &ldquo;Lavora con noi&rdquo;.</p>
<p>I dati vengono trattati esclusivamente per:</p>
<ul><li>esaminare la candidatura;</li><li>valutare la compatibilit&agrave; del profilo con eventuali esigenze presenti o future;</li><li>contattare il candidato;</li><li>gestire eventuali successive fasi di selezione.</li></ul>
<p><strong>Base giuridica:</strong> art. 6, par. 1, lett. b), GDPR e art. 111-bis del D.Lgs. 196/2003.</p>
<p>Per il trattamento dei dati comuni contenuti nei curriculum trasmessi ai fini dell&rsquo;instaurazione di un rapporto di lavoro non &egrave; richiesto uno specifico consenso.</p>'''))
P.append(('sicurezza-diritti', 'Finalit&agrave; di sicurezza e tutela dei diritti', '''<p>I dati potranno inoltre essere trattati nella misura strettamente necessaria per:</p>
<ul><li>prevenire utilizzi abusivi o fraudolenti;</li><li>garantire la sicurezza dei sistemi;</li><li>esercitare o difendere un diritto;</li><li>rispondere a richieste delle Autorit&agrave;;</li><li>adempiere obblighi di legge.</li></ul>'''))
P.append(('conferimento', 'Natura del conferimento', '''<p>Il conferimento dei dati necessari nei moduli &egrave; indispensabile per gestire la richiesta.</p>
<p>Il mancato conferimento pu&ograve; rendere impossibile rispondere, predisporre un preventivo o organizzare un sopralluogo.</p>'''))
P.append(('modalita', 'Modalit&agrave; del trattamento e sicurezza', '''<p>I dati personali sono trattati secondo i principi di liceit&agrave;, correttezza, trasparenza, minimizzazione, esattezza e limitazione della conservazione.</p>
<p>Rivetti Impianti adotta misure tecniche e organizzative ragionevoli e proporzionate volte a proteggere i dati personali. I moduli del sito inviano i dati con richieste di tipo POST (i dati personali non compaiono nell&rsquo;indirizzo della pagina) e sono dotati di un controllo antispam invisibile agli utenti.</p>'''))
P.append(('fornitori', 'Fornitori e servizi tecnici', f'''<p>Per il funzionamento del sito e la gestione delle richieste il Titolare si avvale dei seguenti servizi tecnici, nei limiti di quanto necessario:</p>
<ul>
<li><strong>Servizio di inoltro dei moduli (FormSubmit, formsubmit.co)</strong>: quando l&rsquo;utente invia il modulo preventivi o il modulo recensioni, il contenuto del messaggio transita da questo servizio, che lo inoltra alla casella email del Titolare. Il sito non conserva un archivio proprio dei messaggi inviati.</li>
<li><strong>Posta elettronica e PEC</strong>: le richieste, le recensioni e le candidature ricevute sono gestite nella casella email del Titolare (indirizzo rivettiimpianti@gmail.com, servizio fornito da Google) e nella casella PEC indicata.</li>
<li><strong>Hosting</strong>: il fornitore dello spazio web su cui &egrave; pubblicato il sito pu&ograve; trattare i dati tecnici di navigazione (ad esempio l&rsquo;indirizzo IP) per erogare il servizio.</li>
<li><strong>WhatsApp (Meta Platforms Ireland Limited)</strong>: solo se l&rsquo;utente sceglie di scrivere tramite il relativo collegamento (vedi paragrafo 2.4).</li>
{ext('privacy', EXT_PRIVACY_EXTERNAL)}
</ul>
<p>Il sito non utilizza strumenti di analisi statistica, di pubblicit&agrave; o di profilazione.</p>'''))
P.append(('destinatari', 'Destinatari dei dati', '''<p>I dati possono essere comunicati nei limiti necessari a:</p>
<ul><li>personale e collaboratori autorizzati;</li><li>fornitori IT;</li><li>hosting;</li><li>fornitori email e PEC;</li><li>consulenti amministrativi, fiscali, tecnici e legali;</li><li>professionisti e imprese coinvolti nell&rsquo;esecuzione della prestazione;</li><li>Autorit&agrave; ed enti quando previsto dalla legge.</li></ul>
<p>I dati non vengono venduti a terzi.</p>'''))
P.append(('extra-see', 'Trasferimenti extra SEE', '''<p>Alcuni dei fornitori indicati al paragrafo 6 (ad esempio il servizio di inoltro dei moduli, il fornitore della casella email o WhatsApp) possono avere sede o infrastrutture anche fuori dallo Spazio Economico Europeo. In tal caso i trasferimenti avvengono nel rispetto degli artt. 44 e seguenti del GDPR, sulla base di una decisione di adeguatezza della Commissione europea o di altre garanzie adeguate previste dal Regolamento (ad esempio le clausole contrattuali tipo).</p>'''))
P.append(('conservazione', 'Conservazione dei dati', '''<ul>
<li><strong>Richieste e preventivi:</strong> per un massimo di 24 mesi dall&rsquo;ultimo contatto significativo.</li>
<li><strong>Rapporti contrattuali:</strong> per i termini civilistici e fiscali applicabili, ordinariamente fino a 10 anni.</li>
<li><strong>Curriculum vitae:</strong> di regola per 12 mesi.</li>
<li><strong>Recensioni:</strong> fino a revoca del consenso o rimozione e comunque, di regola, non oltre 5 anni, salvo rinnovo.</li>
<li><strong>Controversie:</strong> per la durata necessaria alla tutela dei diritti.</li>
<li><strong>Log direttamente controllati dal Titolare:</strong> di regola non oltre 30 giorni, salvo esigenze di sicurezza o obblighi di legge. Per i log gestiti dai fornitori (ad esempio l&rsquo;hosting) valgono i tempi da essi applicati.</li>
</ul>'''))
P.append(('decisioni', 'Decisioni automatizzate', '''<p>Il sito non assume decisioni basate unicamente su trattamenti automatizzati aventi effetti giuridici o che incidano in modo analogo significativamente sull&rsquo;interessato e, nella configurazione attuale, non effettua profilazione commerciale.</p>'''))
P.append(('diritti', 'Diritti degli interessati', '''<p>Ai sensi degli artt. 15-22 del GDPR l&rsquo;interessato ha diritto di ottenere:</p>
<ul><li>l&rsquo;accesso ai propri dati;</li><li>la rettifica;</li><li>la cancellazione (&ldquo;diritto all&rsquo;oblio&rdquo;);</li><li>la limitazione del trattamento;</li><li>la portabilit&agrave; dei dati, quando applicabile;</li><li>l&rsquo;opposizione al trattamento;</li></ul>
<p>e di revocare in qualsiasi momento il consenso, dove il trattamento si fondi su di esso, senza pregiudicare la liceit&agrave; del trattamento basato sul consenso prestato prima della revoca.</p>
<p>Per esercitare i diritti &egrave; possibile scrivere a:</p>
<p><a class="l" href="mailto:rivettiimpianti@gmail.com">rivettiimpianti@gmail.com</a><br><a class="l" href="mailto:rmimpiantisas@pec.it">rmimpiantisas@pec.it</a></p>
<p>o inviare una raccomandata A/R alla sede indicata al paragrafo 1.</p>'''))
P.append(('reclamo', 'Reclamo', '''<p>L&rsquo;interessato che ritenga violati i propri diritti ha la possibilit&agrave; di proporre reclamo al Garante per la protezione dei dati personali (<a class="l" href="https://www.garanteprivacy.it" target="_blank" rel="noopener">www.garanteprivacy.it</a>) o di adire l&rsquo;autorit&agrave; giudiziaria.</p>'''))
P.append(('minori', 'Minori', '''<p>I servizi offerti attraverso il sito non sono specificamente rivolti ai minori. Il Titolare non raccoglie intenzionalmente dati di minori; se ne venisse a conoscenza provveder&agrave; a cancellarli.</p>'''))
P.append(('link-esterni', 'Link esterni', '''<p>Il sito pu&ograve; contenere collegamenti a siti e piattaforme di terzi (ad esempio WhatsApp). Tali siti sono disciplinati dalle proprie informative e condizioni, sulle quali il Titolare non esercita alcun controllo.</p>'''))
P.append(('aggiornamenti', 'Aggiornamenti', '''<p>La presente Privacy Policy potr&agrave; essere modificata in caso di evoluzioni normative, tecniche o organizzative. La versione aggiornata sar&agrave; sempre disponibile in questa pagina, con indicazione della data dell&rsquo;ultimo aggiornamento.</p>'''))
privacy = page('Privacy Policy', 'Informativa sul trattamento dei dati personali di Rivetti Impianti ai sensi degli artt. 13 e 14 del GDPR: titolare, finalità, conservazione e diritti.',
  'Informativa sul trattamento dei dati personali', P,
  '''<p>Ai sensi degli artt. 13 e 14 del Regolamento (UE) 2016/679 (&ldquo;GDPR&rdquo;) e della normativa nazionale applicabile.</p>
<p>La presente informativa descrive le modalit&agrave; di trattamento dei dati personali degli utenti che visitano e utilizzano il sito www.rivettiimpianti.it, nonch&eacute; dei soggetti che entrano in contatto con l&rsquo;azienda attraverso i moduli presenti sul sito, posta elettronica, telefono, WhatsApp, candidature, richieste di preventivo o recensioni.</p>''', 'privacy')

# ----------------------------------------------------------------- COOKIE
C = []
C.append(('titolare', 'Titolare del trattamento', f'<p>Il titolare del trattamento &egrave;:</p>\n{OWNER_IDS}'))
C.append(('cosa-sono', 'Cosa sono i cookie', '''<p>I cookie sono brevi file di testo che i siti visitati dall&rsquo;utente inviano al suo dispositivo, dove vengono memorizzati per essere poi ritrasmessi agli stessi siti alla visita successiva. Esistono tecnologie simili (ad esempio il &ldquo;local storage&rdquo; del browser, i pixel di tracciamento o gli identificativi del dispositivo) che hanno funzioni analoghe e a cui si applicano le stesse regole.</p>
<p>I cookie <strong>tecnici</strong> servono a far funzionare il sito o a erogare un servizio richiesto dall&rsquo;utente. Quelli di <strong>profilazione</strong> o di <strong>analisi/marketing</strong> raccolgono informazioni sulle abitudini dell&rsquo;utente e richiedono, di regola, il suo consenso preventivo.</p>'''))
C.append(('configurazione', 'Configurazione attuale del sito', '''<p>Alla data di ultimo aggiornamento, dalle verifiche tecniche effettuate sul codice del sito risulta che:</p>
<ul>
<li>il sito <strong>non imposta cookie propri</strong> e non utilizza il local storage o il session storage del browser;</li>
<li>il sito <strong>non utilizza</strong> strumenti di analisi statistica (ad esempio Google Analytics), pixel di social network, strumenti di marketing o di remarketing, mappe o video incorporati di terzi;</li>
<li>le pagine non richiedono alcun accesso o registrazione.</li>
</ul>
<p>Il fornitore di hosting del sito potrebbe impostare cookie o log tecnici strettamente necessari all&rsquo;erogazione del servizio e alla sicurezza: si tratta di strumenti che non richiedono il consenso dell&rsquo;utente.</p>'''))
C.append(('profilazione', 'Assenza di cookie di profilazione', '''<p>Nella configurazione attuale il sito <strong>non utilizza cookie di profilazione</strong> n&eacute; altri strumenti di tracciamento pubblicitario o di analisi comportamentale, propri o di terze parti.</p>'''))
C.append(('banner', 'Perch&eacute; non viene mostrato un cookie banner', '''<p>L&rsquo;obbligo di raccogliere il consenso mediante banner riguarda l&rsquo;archiviazione di informazioni nel dispositivo dell&rsquo;utente, o l&rsquo;accesso a informazioni gi&agrave; archiviate, effettuati per finalit&agrave; diverse da quelle strettamente tecniche (art. 122 del D.Lgs. 196/2003 e Linee guida del Garante del 10 giugno 2021). Poich&eacute; il sito non utilizza strumenti di questo tipo, non &egrave; necessario mostrare un banner.</p>
<p>Se in futuro venissero aggiunti strumenti soggetti a consenso, il sito mostrer&agrave; un banner con i pulsanti &ldquo;Accetta&rdquo; e &ldquo;Rifiuta&rdquo; di pari evidenza, bloccher&agrave; tali strumenti fino al consenso e questa pagina verr&agrave; aggiornata.</p>'''))
C.append(('dati-tecnici', 'Dati tecnici strettamente necessari', '''<p>Come ogni sito, per funzionare il server riceve alcune informazioni tecniche inviate automaticamente dal browser (ad esempio indirizzo IP, data e ora, pagina richiesta, tipo di browser). Sono trattate per erogare il sito, garantirne la sicurezza e prevenire abusi, come descritto nella <a class="l" href="privacy.html">Privacy Policy</a>.</p>'''))
C.append(('servizi-esterni', 'Servizi esterni utilizzati dal sito', f'''<p>Per visualizzare il sito o per alcune funzioni richieste dall&rsquo;utente vengono utilizzati i seguenti servizi esterni. Essi ricevono almeno l&rsquo;indirizzo IP e i dati tecnici del browser, perch&eacute; ci&ograve; &egrave; inevitabile in ogni connessione.</p>
<ul>
{ext('cookie', EXT_COOKIE_EXTERNAL)}
<li><strong>FormSubmit (formsubmit.co)</strong>: servizio che inoltra i messaggi dei moduli (preventivo e recensione) alla casella email del Titolare; viene contattato soltanto quando l&rsquo;utente invia un modulo.</li>
<li><strong>WhatsApp (Meta Platforms Ireland Limited)</strong>: il sito contiene un semplice collegamento; la connessione al servizio avviene solo se l&rsquo;utente lo seleziona.</li>
</ul>
<p>Per questi servizi non sono stati rilevati, nell&rsquo;uso che ne fa il sito, strumenti di profilazione o di tracciamento pubblicitario. Ciascun fornitore tratta i dati secondo la propria informativa.</p>'''))
C.append(('link-esterni', 'Link esterni', '''<p>Il sito pu&ograve; contenere collegamenti a siti di terzi. Quando l&rsquo;utente li seleziona lascia questo sito e si applicano le politiche sui cookie e sulla privacy di tali siti, sulle quali il Titolare non ha alcun controllo.</p>'''))
C.append(('browser', 'Impostazioni del browser', '''<p>L&rsquo;utente pu&ograve; configurare il proprio browser per accettare, rifiutare o cancellare i cookie, oppure per essere avvisato quando ne viene impostato uno. Le istruzioni sono disponibili nelle pagine di assistenza dei principali browser (Chrome, Firefox, Safari, Edge). La disabilitazione dei cookie tecnici potrebbe compromettere il funzionamento di alcune parti di un sito.</p>'''))
C.append(('trasferimenti', 'Trasferimenti internazionali', '''<p>Alcuni dei servizi esterni indicati possono avere sede o infrastrutture anche fuori dallo Spazio Economico Europeo. I relativi trasferimenti di dati avvengono nel rispetto degli artt. 44 e seguenti del GDPR; per i dettagli si rinvia alla <a class="l" href="privacy.html">Privacy Policy</a>.</p>'''))
C.append(('rinvio', 'Rinvio alla Privacy Policy', '''<p>Per informazioni sul trattamento dei dati personali, sulle finalit&agrave;, sui tempi di conservazione e sull&rsquo;esercizio dei propri diritti si rinvia alla <a class="l" href="privacy.html">Privacy Policy</a>.</p>'''))
C.append(('aggiornamento', 'Aggiornamento della Cookie Policy', '''<p>La presente Cookie Policy pu&ograve; essere modificata in seguito a cambiamenti normativi o tecnici del sito (ad esempio l&rsquo;aggiunta o la rimozione di servizi esterni). La versione vigente &egrave; sempre quella pubblicata in questa pagina, con la data dell&rsquo;ultimo aggiornamento.</p>'''))
cookie = page('Cookie Policy', 'Cookie Policy e tecnologie simili del sito Rivetti Impianti: il sito non utilizza cookie di profilazione né strumenti di analisi.',
  'Cookie Policy e tecnologie simili', C, '<p>Informativa sull&rsquo;uso di cookie e tecnologie simili ai sensi dell&rsquo;art. 122 del D.Lgs. 196/2003 e delle Linee guida del Garante per la protezione dei dati personali.</p>', 'cookie')

# ----------------------------------------------------------------- NOTE LEGALI
N = []
N.append(('titolare', 'Titolare e gestore del sito', f'<p>Il sito www.rivettiimpianti.it &egrave; gestito da:</p>\n{OWNER_IDS}<p>L&rsquo;accesso e l&rsquo;utilizzo del sito comportano l&rsquo;accettazione delle presenti condizioni. Chi non le accetta &egrave; invitato a non utilizzare il sito.</p>'))
N.append(('finalita', 'Finalit&agrave; informative e promozionali', '<p>Il sito ha finalit&agrave; esclusivamente informative e promozionali: presenta l&rsquo;azienda, i servizi offerti e alcune informazioni di carattere generale su energia, impianti e agevolazioni.</p>'))
N.append(('offerta', 'Nessuna offerta al pubblico', '<p>Le informazioni pubblicate sul sito non costituiscono offerta al pubblico ai sensi dell&rsquo;art. 1336 del Codice civile n&eacute; proposta contrattuale vincolante. Un rapporto contrattuale si perfeziona solo con un preventivo o un contratto redatto per iscritto e accettato dalle parti.</p>'))
N.append(('preventivi', 'Richieste di informazioni e preventivi', '<p>Le richieste inviate tramite i moduli del sito o gli altri canali non impegnano n&eacute; l&rsquo;utente n&eacute; Rivetti Impianti. Preventivi e stime richiedono sempre una successiva conferma scritta e, di norma, un sopralluogo tecnico da parte di personale tecnico, che pu&ograve; far variare condizioni, tempi e importi.</p>'))
N.append(('info-tecniche', 'Informazioni tecniche', '<p>Le informazioni tecniche presenti sul sito sono generali e non sostituiscono la progettazione, le verifiche e le valutazioni specifiche per ciascun immobile o impianto. Le caratteristiche effettive di un intervento sono quelle indicate nella documentazione contrattuale e progettuale.</p>'))
N.append(('prestazioni', 'Producibilit&agrave;, risparmio e prestazioni', '''<p>Eventuali valori relativi a produzione fotovoltaica, risparmio in bolletta, autoconsumo, rendimento, ritorno economico e tempi di rientro dell&rsquo;investimento hanno natura di <strong>stime</strong>. Dipendono da fattori variabili (esposizione, ombreggiamenti, condizioni meteorologiche, consumi, tariffe, stato dell&rsquo;impianto) e non costituiscono garanzia di risultato, <strong>salvo specifica garanzia assunta per iscritto nel contratto</strong>.</p>'''))
N.append(('incentivi', 'Bonus, incentivi, detrazioni e bandi', '''<p class="key">Le informazioni relative a incentivi, bonus, detrazioni, contributi GSE, Conto Termico, Comunit&agrave; Energetiche Rinnovabili (CER), bandi, PNRR o altre agevolazioni hanno carattere puramente informativo e sono riferite alla disciplina disponibile al momento della pubblicazione.</p>
<p>La presenza sul sito di informazioni riguardanti un incentivo <strong>non costituisce garanzia</strong>:</p>
<ul><li>dell&rsquo;ammissione della domanda;</li><li>dell&rsquo;ottenimento del contributo;</li><li>dell&rsquo;importo riconosciuto;</li><li>dei tempi di erogazione;</li><li>della permanenza della misura;</li><li>della disponibilit&agrave; delle risorse.</li></ul>
<p>L&rsquo;ammissione e l&rsquo;erogazione restano di competenza esclusiva degli enti e delle amministrazioni competenti. Le informazioni non costituiscono consulenza fiscale, legale o finanziaria: per la propria situazione specifica &egrave; opportuno rivolgersi a un professionista abilitato.</p>'''))
N.append(('normativa', 'Aggiornamento della normativa', '<p>La normativa e le condizioni delle agevolazioni cambiano frequentemente. Rivetti Impianti non garantisce che i contenuti del sito siano sempre aggiornati e invita a verificare con l&rsquo;azienda, prima di ogni decisione, le condizioni in vigore.</p>'))
N.append(('errori', 'Errori materiali e inesattezze', '<p>Pur ponendo la massima cura nella redazione dei contenuti, il sito potrebbe contenere errori materiali o inesattezze. Rivetti Impianti si riserva di correggerli in qualsiasi momento e senza preavviso.</p>'))
N.append(('prezzi', 'Prezzi e condizioni economiche', '<p>Salvo diversa indicazione, il sito non riporta prezzi. Importi, condizioni di pagamento e tempi di esecuzione sono quelli indicati nel preventivo o nel contratto sottoscritto.</p>'))
N.append(('immagini', 'Fotografie, rendering e rappresentazioni grafiche', '<p>Fotografie, illustrazioni, rendering e rappresentazioni grafiche hanno scopo puramente illustrativo e possono non corrispondere esattamente a prodotti, impianti o interventi effettivamente realizzati.</p>'))
N.append(('proprieta', 'Propriet&agrave; intellettuale', '<p>Testi, grafiche, loghi, immagini, illustrazioni, icone, codice sorgente e layout del sito sono di propriet&agrave; di Rivetti Impianti o dei rispettivi titolari e sono protetti dalla normativa sul diritto d&rsquo;autore e sulla propriet&agrave; industriale. &Egrave; vietata la riproduzione, distribuzione o modifica non autorizzata, salvo i casi previsti dalla legge o il consenso scritto del titolare.</p>'))
N.append(('marchi', 'Marchi e segni distintivi di terzi', '<p>Eventuali marchi, nomi e segni distintivi di terzi citati nel sito (ad esempio GSE, WhatsApp) appartengono ai rispettivi titolari e sono utilizzati solo a fini informativi, senza che ci&ograve; implichi affiliazione o sponsorizzazione.</p>'))
N.append(('recensioni', 'Recensioni e contenuti degli utenti', '''<p>Le recensioni inviate dagli utenti sono lette dallo staff e pubblicate solo previa verifica e con il consenso dell&rsquo;autore. Rivetti Impianti si riserva di non pubblicare, modificare o rimuovere contenuti falsi, offensivi, illeciti, lesivi di diritti di terzi o non pertinenti. L&rsquo;utente &egrave; responsabile di quanto scrive e garantisce di averne il diritto. Le modalit&agrave; di trattamento dei dati sono descritte nella <a class="l" href="privacy.html">Privacy Policy</a>.</p>'''))
N.append(('link', 'Collegamenti a siti di terzi', '<p>Il sito pu&ograve; contenere collegamenti a siti o servizi di terzi. Rivetti Impianti non esercita alcun controllo su di essi e non risponde dei loro contenuti, della loro disponibilit&agrave; o del trattamento dei dati da essi effettuato.</p>'))
N.append(('disponibilita', 'Disponibilit&agrave; e sicurezza del sito', '<p>Rivetti Impianti si impegna a mantenere il sito accessibile e sicuro, ma non garantisce l&rsquo;assenza di interruzioni, errori o malfunzionamenti dovuti, ad esempio, a manutenzione, problemi di rete, cause di forza maggiore o attacchi informatici.</p>'))
N.append(('responsabilita', 'Limitazioni di responsabilit&agrave;', '''<p>Nei limiti consentiti dalla legge, Rivetti Impianti non risponde dei danni derivanti dall&rsquo;uso del sito o dall&rsquo;affidamento sulle informazioni in esso contenute, n&eacute; dei danni causati da interruzioni del servizio o da virus e programmi dannosi non riconducibili a sua colpa.</p>
<p>Restano in ogni caso salvi: i diritti dei consumatori; la responsabilit&agrave; per dolo e colpa grave; gli obblighi espressamente assunti tramite contratto; ogni altra responsabilit&agrave; che non possa essere esclusa o limitata ai sensi di legge.</p>'''))
N.append(('consumatori', 'Tutela inderogabile del consumatore', '<p>Nulla nelle presenti Note legali limita i diritti riconosciuti ai consumatori dal Codice del consumo (D.Lgs. 206/2005) e dalle altre norme inderogabili.</p>'))
N.append(('modifiche', 'Modifiche del sito e delle Note legali', '<p>Rivetti Impianti pu&ograve; modificare in qualsiasi momento i contenuti e le funzioni del sito e le presenti Note legali. La versione vigente &egrave; quella pubblicata in questa pagina, con la data dell&rsquo;ultimo aggiornamento.</p>'))
N.append(('legge', 'Legge applicabile', '<p>Le presenti Note legali sono regolate dalla legge italiana. Per le controversie con i consumatori restano ferme le competenze territoriali inderogabili previste dalla legge.</p>'))
N.append(('contatti', 'Contatti', f'<p>Per informazioni o segnalazioni relative al sito:</p>\n{OWNER_IDS}'))
note = page('Note legali', 'Note legali e condizioni di utilizzo del sito Rivetti Impianti: finalità informative, incentivi, stime, proprietà intellettuale e tutela del consumatore.',
  'Note legali e condizioni di utilizzo del sito', N, '', 'note')

if __name__ == '__main__':
    for name, html in (('privacy', privacy), ('cookie', cookie), ('note-legali', note)):
        open(f'/home/claude/{name}.html', 'w', encoding='utf-8').write(html)
        print(name, len(html) // 1024, 'KB')
