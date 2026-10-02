/* Funzioni comuni (home e pagina recensioni) */
window.RI = (function () {

  /* ---------------------------------------------------------------------------
     INVIO MODULI

     I moduli del sito vengono inviati tramite l'endpoint server-side
     /api/contatto, gestito da una Vercel Function.

     La funzione valida i dati ricevuti e inoltra le richieste alla casella
     rivettiimpianti@gmail.com tramite il servizio email configurato lato server.

     Le credenziali email non sono presenti né accessibili nel codice frontend.
     --------------------------------------------------------------------------- */

  const FORM_ENDPOINT = '/api/contatto';
  const MAIL_TO = 'rivettiimpianti@gmail.com';

  /*
   * Invia i dati tramite richiesta POST in formato JSON.
   * Se il server non conferma correttamente la ricezione, viene generato
   * un errore così da evitare che l'utente creda che la richiesta sia stata
   * inviata quando invece non lo è stata.
   */
  async function send(payload) {
    const ctrl = new AbortController();
    const timeout = setTimeout(() => ctrl.abort(), 15000);

    try {
      const response = await fetch(FORM_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(payload),
        signal: ctrl.signal
      });

      let data = {};

      try {
        data = await response.json();
      } catch (e) {
        // La risposta non contiene JSON valido.
      }

      if (
        !response.ok ||
        data.success === false ||
        data.success === 'false'
      ) {
        throw new Error(
          data.message || 'Invio della richiesta non confermato.'
        );
      }

      return true;

    } finally {
      clearTimeout(timeout);
    }
  }

  /*
   * Sistema di emergenza:
   * se previsto dall'interfaccia, apre il programma di posta del visitatore
   * con destinatario, oggetto e messaggio già compilati.
   */
  function mailto(subject, body) {
    location.href =
      'mailto:' +
      MAIL_TO +
      '?subject=' +
      encodeURIComponent(subject) +
      '&body=' +
      encodeURIComponent(body);
  }

  /* Protezione di base per contenuti inseriti dinamicamente nell'HTML. */
  const esc = s =>
    String(s == null ? '' : s).replace(
      /[&<>"']/g,
      c => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;'
      }[c])
    );

  /* Conta il numero di parole di un testo. */
  const words = text =>
    String(text || '')
      .trim()
      .split(/\s+/)
      .filter(Boolean)
      .length;

  /* Genera graficamente la valutazione da 0 a 5 stelle. */
  const stars = n => {
    n = Math.max(0, Math.min(5, Math.round(n)));

    return (
      '<span class="stars" role="img" aria-label="' +
      n +
      ' stelle su 5">' +
      '★'.repeat(n) +
      '<span class="off">' +
      '★'.repeat(5 - n) +
      '</span></span>'
    );
  };

  /* Data e ora corrente in formato ISO. */
  const now = () => new Date().toISOString();

  return {
    send,
    mailto,
    esc,
    words,
    stars,
    now,
    MAIL_TO
  };

})();