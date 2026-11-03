/* Pagina «Lavora con noi»: invio della candidatura con CV allegato (multipart) a rivettiimpianti@gmail.com tramite FormSubmit. */
(function () {
  'use strict';
  var form = document.getElementById('jobForm');
  if (!form || !window.RI) return;
  var msg = document.getElementById('jobMsg'), btn = document.getElementById('jobSend'), cv = form.elements.attachment;
  var MAX = (parseFloat(cv.getAttribute('data-max-mb')) || 5) * 1024 * 1024;
  var OK = /\.(pdf|docx?|odt)$/i;

  function setMsg(t, cls) { msg.textContent = t; msg.className = 'form-msg full ' + (cls || ''); }
  function cvErr() {
    var f = cv.files && cv.files[0];
    if (!f) return 'Allega il tuo curriculum.';
    if (!OK.test(f.name)) return 'Formato non valido: usa PDF, DOC, DOCX o ODT.';
    if (f.size > MAX) return 'Il file supera i ' + (MAX / 1048576) + ' MB: allega un CV più leggero.';
    return '';
  }
  cv.addEventListener('change', function () {
    var e = cvErr();
    cv.setCustomValidity(e && cv.files.length ? e : '');
    setMsg(e && cv.files.length ? e : '', e && cv.files.length ? 'err' : '');
  });

  form.addEventListener('submit', async function (ev) {
    ev.preventDefault();
    if (form._honey.value) return;                                  // antispam
    var e = cvErr(); cv.setCustomValidity(e);
    if (!form.checkValidity()) { form.reportValidity(); setMsg(e || 'Compila correttamente i campi obbligatori.', 'err'); return; }
    var v = function (k) { return String(form.elements[k].value || '').trim(); };
    var ctx = RI.context();
    var fd = new FormData();
    fd.append('Nome e cognome', v('nome'));
    fd.append('Email', v('email'));
    fd.append('Telefono', v('telefono'));
    fd.append('Ruolo di interesse', v('ruolo'));
    fd.append('Messaggio', v('messaggio'));
    fd.append('Presa visione Informativa Privacy', 'Sì — ' + RI.now());
    fd.append('Pagina di invio', ctx.pagina);
    fd.append('attachment', cv.files[0]);
    fd.append('_subject', 'Candidatura dal sito — ' + v('ruolo') + ' — ' + v('nome'));
    fd.append('_template', 'table');
    fd.append('_captcha', 'false');
    fd.append('_replyto', v('email'));
    btn.disabled = true; setMsg('Invio in corso…');
    try {
      await RI.sendForm(fd);
      form.reset(); setMsg('Grazie! Candidatura inviata: la esamineremo e ti ricontatteremo se il profilo è in linea con le nostre esigenze.', 'ok');
    } catch (err) {
      setMsg('Invio automatico non riuscito: si apre la tua posta. Allega il CV alla email e invia.', 'err');
      RI.mailto('Candidatura dal sito — ' + v('ruolo') + ' — ' + v('nome'),
        'Nome: ' + v('nome') + '\nEmail: ' + v('email') + '\nTelefono: ' + v('telefono') + '\nRuolo: ' + v('ruolo') + '\n\n' + v('messaggio') + '\n\n(ricordati di allegare il CV)');
    } finally { btn.disabled = false; }
  });
})();
