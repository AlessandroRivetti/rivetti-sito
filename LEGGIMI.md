# Sito Rivetti Impianti — guida rapida

Sito statico: basta caricare tutti i file (index.html, recensione.html, privacy.html, cookie.html, site.css, ri.js, recensioni.js e la cartella assets/) su qualsiasi hosting. Nessuna installazione.

## Da fare prima della pubblicazione
1. **Attivare i moduli (una volta sola).** Preventivo, recensioni e candidature usano FormSubmit verso rivettiimpianti@gmail.com. Al primo invio di prova arriva una mail di attivazione a quell'indirizzo: clicca il link di conferma. Senza conferma i moduli aprono il programma di posta come ripiego.
2. **Numeri di telefono**: modificabili in un solo punto, l'array `PHONES` in `index.html` (footer, contatti e link Chiama/WhatsApp si aggiornano insieme).
3. **Timeline**: i traguardi (2008, 2010, 2015, 2020, 2026) sono quelli da te indicati; si modificano nella sezione `#storia` di `index.html`.
4. **Privacy e Cookie**: sono testi base, da far controllare prima della pubblicazione.

## Recensioni (approvazione manuale)
1. Il cliente compila `recensione.html`: la recensione arriva per email a rivettiimpianti@gmail.com con voto, nome, tipo di cliente e testo.
2. Tu la leggi. Se la approvi, copia una voce in `recensioni.js` (l'esempio è nel file) e ricarica il file sul sito.
3. Per rimuoverne una, cancella la sua voce da `recensioni.js`.
Sul sito compare solo ciò che è in `recensioni.js`.

## Foto reali (facoltative)
Metti in `assets/servizi/` foto con questi nomi e sostituiranno le illustrazioni: fotovoltaico-domestico.jpg, accumulo.jpg, termoidraulica-climatizzazione.jpg, manutenzione-inverter.jpg, lavaggio-pannelli.jpg, termografia.jpg, utility-scale.jpg, termografia-azienda.jpg, impianti-termici.jpg, lavaggio-azienda.jpg, pubblica-amministrazione.jpg.
