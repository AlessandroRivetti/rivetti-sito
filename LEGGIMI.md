# Sito Rivetti Impianti — guida rapida

Sito statico: nessuna installazione. Carica sull'hosting tutti i file della cartella **tranne** `src/`, `_backup_*`, `_demo/`, `dev/`, `serverless/`, `scarica-risorse-locali.py`, `prepara-foto.py`, `rivetti-impianti-home.html`, `LEGGIMI.md` e i file `LEGGIMI.txt` nelle cartelle `assets/` (restano per te).

## Pagine
`index.html` (Home), `privati.html`, `imprese.html`, `pubblica-amministrazione.html`, `contatti.html`, `recensione.html`, `privacy.html`, `cookie.html`, `note-legali.html`, `404.html`, `sitemap.xml`, `robots.txt`.
Le pagine **Realizzazioni** (`realizzazioni.html` e una pagina `progetto-<nome>.html` per ogni lavoro) esistono **solo se ci sono almeno 3 progetti pubblicati** in `src/progetti.py`: finché non è così non ci sono né pagine, né voce di menu o footer, né blocco in Home, né voci in sitemap.
File condivisi: `site.css` (base e pagine legali), `pagine.css` (pagine del sito), `ri.js` (invio moduli), `site.js` (menu, finestre, filtri, modulo), `recensioni.js` (recensioni approvate).

## Come si modifica il sito
I contenuti stanno in **`src/dati.py`** (dati societari, telefoni, WhatsApp, numeri, servizi, incentivi, FAQ, realizzazioni). Dopo ogni modifica:

    python3 src/build.py

rigenera le pagine e fa i controlli automatici (link, ancore, title/description unici, un solo H1, SVG accessibili, nessun TODO visibile). Le pagine HTML generate **non vanno modificate a mano**. Le pagine legali si rigenerano con `python3 src/legal.py`. Le recensioni restano in `recensioni.js`.

- **Numeri "Risultati che parlano"**: `NUMERI` in `dati.py`. Valore `None` = indicatore non pubblicato. Oggi sono pubblicati solo clienti (1.000+) e anni di esperienza; con i dati reali di lavori ed energia diventano 4. Gli anni di esperienza si calcolano da soli (anno corrente − 2008) a ogni build.
- **Realizzazioni** (`src/progetti.py`): copia il modello commentato in fondo al file, compila i campi e metti `'pubblicato': True` solo quando il lavoro è approvato. Le foto vanno in `assets/realizzazioni/<nome-progetto>/` (istruzioni in `assets/realizzazioni/LEGGIMI.txt`; `python3 prepara-foto.py` crea le versioni leggere). Ogni foto pubblicata deve avere il testo alternativo. Cliente e località compaiono solo se compilati **e** autorizzati (`cliente_autorizzato`, `mostra_localita`). Se un progetto pubblicato è incompleto la build si ferma e dice cosa manca. Il blocco "Alcuni dei nostri progetti" in Home si accende con `HOME_ATTIVA = True` e 3 progetti `in_evidenza`.
- **Alcuni dei nostri lavori** (`src/gallerie.py`): fotografie **reali** di interventi eseguiti, una lista per macroarea (Privati, Imprese, PA) con le foto in `assets/gallerie/<privati|imprese|pa>/`. La sezione «Alcuni dei nostri lavori» compare **solo con almeno 3 foto pubblicate** (`MIN_FOTO_GALLERIA`, al massimo 6 mostrate). Ogni foto vuole `alt`, `'reale': True` e `'pubblicato': True`; titolo e descrizione sono facoltativi e cliente/indirizzo/località/potenza compaiono solo se compilati e autorizzati. Niente immagini IA nella galleria (la build lo impone). Non sostituisce Realizzazioni.
- **Copertine delle macroaree**: `assets/servizi/privati-hero.jpg`, `imprese-hero.jpg`, `pa-hero.jpg` (immagini illustrative, non lavori eseguiti; istruzioni in `assets/servizi/LEGGIMI.txt`). Se un file manca resta l'illustrazione attuale. `python3 prepara-foto.py` crea le versioni leggere anche per gallerie e copertine.
- **Certificazioni e qualifiche, tecnologie e marchi** (`src/qualifiche.py`): strutture pronte ma **spente e vuote**; nulla viene pubblicato senza un elemento con `pubblicato: True` e l'interruttore `ATTIVA`. Non sono ancora collegate a nessuna pagina.
- **Anteprima con dati di prova**: `python3 src/build.py --demo` crea `_demo/` usando `dev/fixture_progetti.py` (dati e immagini SINTETICHE, non reali). `_demo/` e `dev/` non vanno mai pubblicati.
- **Dominio**: `SITO['url']` in `dati.py` (canonical, Open Graph, sitemap). Da confermare (con o senza www).
- **Foto dei servizi**: se il file esiste in `assets/servizi/` (nomi in `dati.py`) sostituisce l'illustrazione.

## Test in locale
    cd cartella-del-sito
    python3 -m http.server 8000
poi apri http://localhost:8000 (la 404 su http://localhost:8000/404.html; sull'hosting va impostata come pagina "non trovato").

## Stato tecnico (cosa fa davvero il sito)
- **Moduli**: POST tramite **FormSubmit** verso rivettiimpianti@gmail.com; se la consegna non è confermata si apre la posta con il messaggio pronto. Antispam: campo invisibile. Il modulo di richiesta invia anche, in automatico, pagina di invio, provenienza (referrer) e parametri UTM se presenti.
- **Font**: Google Fonts. **Globo 3D e immagini della Terra**: jsDelivr (caricati dopo il contenuto e solo se dispositivo, connessione e preferenza "riduci movimento" lo consentono).
- **Cookie / memoria del browser**: nessuno. Nessun Analytics, pixel o marketing.
- **WhatsApp**: link `wa.me`, nessuno script.
Privacy e Cookie Policy (non modificate in Fase 1) descrivono questa configurazione: vedi il report di Fase 1 per i punti da aggiornare.

## Rendere il sito autonomo da Google Fonts e jsDelivr (consigliato)
Sul tuo computer con internet: `python3 scarica-risorse-locali.py` (scarica i font in `assets/`, aggiorna tutte le pagine e i paragrafi di Privacy e Cookie; copia di sicurezza in `_backup_prima_dello_script/`). Se poi rigeneri le pagine con `build.py`, rilancia lo script.

## Sostituire FormSubmit
Vedi `serverless/contatto.js` (funzione per Cloudflare Pages con Resend): imposta `RESEND_API_KEY`, `MAIL_FROM`, `MAIL_TO`, `ALLOWED_ORIGIN` nel pannello dell'hosting, poi cambia `FORM_ENDPOINT` in `ri.js` e aggiorna Privacy e Cookie.

## Prima di pubblicare
1. Primo invio di prova dei moduli: FormSubmit manda una mail di attivazione a rivettiimpianti@gmail.com da confermare.
2. Conferma dominio e "www" in `SITO['url']`, poi `python3 src/build.py`.
3. Pagine legali: falle rivedere da un consulente.
4. Imposta la pagina 404 e, solo dopo aver verificato gli URL indicizzati, gli eventuali redirect 301 (nessun redirect è stato creato).

## Hero della Home (video showreel)
La Hero usa `assets/rivetti-showreel.mp4` (poster: `assets/servizi/pa-hero.jpg`), con pulsante audio. Testi in `src/dati.py` (`HERO_HOME`). Copia il video in `assets/` con quel nome: finché manca, il build stampa una NOTA e la Hero mostra solo il poster. Il globo 3D è stato rimosso.
