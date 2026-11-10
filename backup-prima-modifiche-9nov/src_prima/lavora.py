# -*- coding: utf-8 -*-
"""Pagina «Lavora con noi» (lavora-con-noi.html): presentazione dei profili cercati e modulo di candidatura con CV.

Invio: lavora.js → FormSubmit (stesso servizio del modulo contatti) → rivettiimpianti@gmail.com. Il CV viaggia come allegato
(max 5 MB, PDF/DOC/DOCX/ODT). Se l'invio automatico non riesce, il modulo ripiega su una email già compilata.
"""
import dati as D
import comp as C

esc, qa = C.esc, C.qa

RUOLI = [
    'Tecnico impiantista fotovoltaico',
    'Installatore / squadra di installazione',
    'Elettricista',
    'Idraulico / termoidraulico',
    'Frigorista / climatizzazione e pompe di calore',
    'Progettista o ingegnere',
    'Responsabile di cantiere / capo squadra',
    'Tecnico manutenzione e O&M',
    'Amministrazione e segreteria',
    'Candidatura spontanea / altro',
]
CV_MAX_MB = 5
CV_ACCEPT = '.pdf,.doc,.docx,.odt'

PROFILI = [
    ('Tecnici', 'Impiantisti e specialisti di fotovoltaico, termoidraulica e manutenzione.', C.ICO_TEC),
    ('Installatori', 'Squadre e singoli installatori per cantieri residenziali, industriali e pubblici.', C.ICO_INS),
    ('Professionisti', 'Progettisti, ingegneri, periti e consulenti tecnici.', C.ICO_PRO),
]


def corpo(p):
    mail = D.SOCIETA['email']
    profili = ''.join(f'<li class="lav-prof"><div class="ico">{ic}</div><div><b>{esc(t)}</b><span>{esc(x)}</span></div></li>' for t, x, ic in PROFILI)
    opz = ''.join(f'<option>{esc(r)}</option>' for r in RUOLI)
    return f'''<section class="phero lav-hero">
  <div class="phero-in"><div class="phero-text">
    <nav class="crumbs" aria-label="Percorso di navigazione"><ol><li><a href="index.html">Home</a></li><li aria-current="page">Lavora con noi</li></ol></nav>
    <h1>Lavora con noi</h1>
    <p class="lead">Cerchiamo persone competenti e affidabili con cui crescere nel fotovoltaico, nella termoidraulica e nella manutenzione degli impianti. Presentati con una breve descrizione e il tuo curriculum.</p>
    <div class="cta"><a class="btn btn-light" href="#candidatura">Invia la tua candidatura &rarr;</a></div>
  </div></div>
</section>
<section class="sec lav-page" id="candidatura">
  {C.sec_head('Candidature', 'Candidati a Rivetti Impianti', 'Valutiamo con attenzione ogni candidatura. Se il tuo profilo è in linea con le nostre esigenze, ti ricontatteremo.')}
  <div class="lav-grid">
    <aside class="lav-side">
      <h3>Chi cerchiamo</h3>
      <ul class="lav-profs">{profili}</ul>
      <p class="lav-note">Puoi candidarti anche per un ruolo non elencato: scegli «Candidatura spontanea» nel modulo.</p>
      <p class="lav-mail">Preferisci scrivere direttamente? <a href="mailto:{qa(mail)}">{esc(mail)}</a></p>
    </aside>
    <form id="jobForm" class="lav-form" method="post" enctype="multipart/form-data" novalidate>
      <div class="field"><label for="j-nome">Nome e cognome *</label><input id="j-nome" name="nome" type="text" autocomplete="name" minlength="2" maxlength="80" required></div>
      <div class="field"><label for="j-email">Email *</label><input id="j-email" name="email" type="email" autocomplete="email" maxlength="120" required></div>
      <div class="field"><label for="j-tel">Telefono *</label><input id="j-tel" name="telefono" type="tel" autocomplete="tel" inputmode="tel" pattern="[0-9+\\s.\\-\\(\\)]{{6,20}}" title="Inserisci un numero di telefono valido" maxlength="20" required></div>
      <div class="field"><label for="j-ruolo">Ruolo o posizione d’interesse *</label>
        <select id="j-ruolo" name="ruolo" required><option value="" disabled selected>Seleziona…</option>{opz}</select></div>
      <div class="field full"><label for="j-msg">Messaggio di presentazione *</label>
        <textarea id="j-msg" name="messaggio" minlength="20" maxlength="3000" required placeholder="Raccontaci le tue competenze, le esperienze e le zone in cui puoi lavorare."></textarea></div>
      <div class="field full"><label for="j-cv">Curriculum (CV) *</label>
        <input id="j-cv" name="attachment" type="file" accept="{CV_ACCEPT}" required data-max-mb="{CV_MAX_MB}">
        <small class="lav-hint">Formati accettati: PDF, DOC, DOCX, ODT — massimo {CV_MAX_MB} MB.</small></div>
      <div class="field full hp" aria-hidden="true"><label>Non compilare<input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>
      <div class="field full check">
        <input id="j-privacy" type="checkbox" name="privacy" required>
        <label for="j-privacy">Dichiaro di aver letto l’<a href="privacy.html" target="_blank" rel="noopener">Informativa Privacy</a> e autorizzo il trattamento dei dati contenuti nella candidatura ai fini della selezione. *</label>
      </div>
      <button class="btn btn-primary full" type="submit" id="jobSend">Invia candidatura &rarr;</button>
      <p class="form-msg full" id="jobMsg" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>'''