/* Funzioni comuni (home e pagina recensioni) */
window.RI = (function () {
  /* ---------------------------------------------------------------------------
     INVIO MODULI
     Oggi: FormSubmit inoltra il messaggio a rivettiimpianti@gmail.com.
     Per sostituirlo con un endpoint proprio (vedi LEGGIMI.md e cartella serverless/)
     basta cambiare QUESTA riga, ad es.:  const FORM_ENDPOINT = '/api/contatto';
     --------------------------------------------------------------------------- */
  const FORM_ENDPOINT = 'https://formsubmit.co/ajax/rivettiimpianti@gmail.com';
  const MAIL_TO = 'rivettiimpianti@gmail.com';

  /* Invia i dati in POST (JSON). Lancia un errore se la consegna non è confermata: così nessuna richiesta va persa in silenzio. */
  async function send(payload) {
    const ctrl = new AbortController(), t = setTimeout(() => ctrl.abort(), 15000);
    try {
      const r = await fetch(FORM_ENDPOINT, {
        method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(payload), signal: ctrl.signal
      });
      let j = {}; try { j = await r.json(); } catch (e) {}
      if (!r.ok || j.success === false || j.success === 'false') throw new Error('invio non confermato');
      return true;
    } finally { clearTimeout(t); }
  }
  /* Ripiego: apre la posta del visitatore con il messaggio già pronto. */
  function mailto(subject, body) {
    location.href = 'mailto:' + MAIL_TO + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  }

  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const words = t => String(t || '').trim().split(/\s+/).filter(Boolean).length;
  const stars = n => {
    n = Math.max(0, Math.min(5, Math.round(n)));
    return '<span class="stars" role="img" aria-label="' + n + ' stelle su 5">' + '★'.repeat(n) + '<span class="off">' + '★'.repeat(5 - n) + '</span></span>';
  };
  const now = () => new Date().toISOString();

  /* Dati tecnici della richiesta, raccolti in automatico (nessun cookie, nessuna memoria del browser):
     pagina da cui parte il modulo, pagina di provenienza (referrer) e parametri UTM presenti nell'indirizzo. */
  function context() {
    const q = new URLSearchParams(location.search), o = {};
    ['source', 'medium', 'campaign', 'content', 'term'].forEach(k => {
      const v = (q.get('utm_' + k) || '').trim().slice(0, 100);
      if (v) o['utm_' + k] = v;
    });
    o.pagina = location.href.split(/[?#]/)[0];
    o.referrer = (document.referrer || '').split('#')[0].slice(0, 300);
    return o;
  }
  return { send, mailto, esc, words, stars, now, context, MAIL_TO };
})();
