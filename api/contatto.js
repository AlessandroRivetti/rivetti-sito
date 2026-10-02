const nodemailer = require('nodemailer');

const MAX = {
  nome: 80,
  telefono: 20,
  email: 120,
  servizio: 120,
  messaggio: 2000,
  tipo: 60,
  recensione: 1200
};

function clean(value, max) {
  return String(value == null ? '' : value)
    .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, '')
    .trim()
    .slice(0, max);
}

function esc(value) {
  return String(value).replace(/[&<>"']/g, char => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }[char]));
}

function response(res, status, data) {
  return res.status(status).json(data);
}

function error(res, message, status = 400) {
  return response(res, status, {
    success: false,
    message
  });
}

module.exports = async function handler(req, res) {

  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return error(res, 'Metodo non consentito.', 405);
  }

  const {
    GMAIL_USER,
    GMAIL_APP_PASSWORD,
    MAIL_TO,
    ALLOWED_ORIGIN
  } = process.env;

  if (!GMAIL_USER || !GMAIL_APP_PASSWORD || !MAIL_TO) {
    console.error('Variabili email mancanti.');
    return error(res, 'Servizio email non configurato.', 500);
  }

  /*
   * Controllo dell'origine.
   * Accettiamo:
   * - www.rivettiimpianti.it
   * - l'eventuale deployment Preview Vercel corrente
   */
  const origin = req.headers.origin || '';

  const allowedOrigins = [
    ALLOWED_ORIGIN,
    'https://rivettiimpianti.it',
    process.env.VERCEL_URL
      ? `https://${process.env.VERCEL_URL}`
      : null
  ].filter(Boolean);

  if (origin && !allowedOrigins.includes(origin)) {
    console.warn('Origine rifiutata:', origin);
    return error(res, 'Richiesta non consentita.', 403);
  }

  let body = req.body;

  if (typeof body === 'string') {
    try {
      body = JSON.parse(body);
    } catch {
      return error(res, 'Dati non validi.');
    }
  }

  if (!body || typeof body !== 'object' || Array.isArray(body)) {
    return error(res, 'Dati non validi.');
  }

  /*
   * Honeypot antispam.
   * Se in futuro aggiungiamo un campo nascosto "_honey",
   * un bot che lo compila viene ignorato.
   */
  if (body._honey) {
    return response(res, 200, { success: true });
  }

  const nome = clean(body.Nome, MAX.nome);

  if (nome.length < 2) {
    return error(res, 'Inserisci un nome valido.');
  }

  const isReview =
    Object.prototype.hasOwnProperty.call(body, 'Recensione');

  let subject;
  let rows;
  let replyTo;

  if (isReview) {

    const stelle = parseInt(String(body.Stelle), 10);
    const tipo = clean(body['Tipo cliente'], MAX.tipo);
    const recensione = clean(body.Recensione, MAX.recensione);

    if (!(stelle >= 1 && stelle <= 5)) {
      return error(res, 'Valutazione non valida.');
    }

    if (
      recensione
        .split(/\s+/)
        .filter(Boolean)
        .length < 5
    ) {
      return error(
        res,
        'La recensione deve contenere almeno 5 parole.'
      );
    }

    const consenso = clean(
      body['Consenso alla pubblicazione di nome e recensione'],
      100
    );

    if (!/^S[iì]/i.test(consenso)) {
      return error(
        res,
        'È necessario il consenso alla pubblicazione.'
      );
    }

    rows = [
      ['Voto', `${stelle} su 5`],
      ['Nome', nome],
      ['Tipo cliente', tipo],
      ['Recensione', recensione],
      ['Consenso alla pubblicazione', consenso],
      [
        'Presa visione Informativa Privacy',
        clean(
          body['Presa visione Informativa Privacy'],
          100
        )
      ]
    ];

    subject =
      `Nuova recensione da approvare — ${stelle}/5 — ${nome}`;

  } else {

    const telefono = clean(body.Telefono, MAX.telefono);
    const email = clean(body.Email, MAX.email);
    const servizio = clean(body.Servizio, MAX.servizio);
    const messaggio = clean(body.Messaggio, MAX.messaggio);

    if (!/^[0-9+()\s.\-]{6,20}$/.test(telefono)) {
      return error(res, 'Numero di telefono non valido.');
    }

    if (!/^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]{2,}$/.test(email)) {
      return error(res, 'Indirizzo email non valido.');
    }

    if (!servizio) {
      return error(res, 'Seleziona il servizio richiesto.');
    }

    const privacy = clean(
      body['Presa visione Informativa Privacy'],
      100
    );

    if (!/^S[iì]/i.test(privacy)) {
      return error(
        res,
        'Conferma la presa visione dell’Informativa Privacy.'
      );
    }

    rows = [
      ['Nome', nome],
      ['Telefono', telefono],
      ['Email', email],
      ['Servizio', servizio],
      ['Messaggio', messaggio],
      ['Presa visione Informativa Privacy', privacy]
    ];

    subject =
      `Richiesta preventivo dal sito — ${servizio} — ${nome}`;

    /*
     * Così quando premi "Rispondi" in Gmail
     * rispondi direttamente al cliente.
     */
    replyTo = email;
  }

  const html = `
    <div style="
      font-family:Arial,Helvetica,sans-serif;
      line-height:1.5;
      color:#222;
    ">
      <h2>${esc(subject)}</h2>

      <table
        cellpadding="9"
        cellspacing="0"
        border="1"
        style="
          border-collapse:collapse;
          border-color:#ddd;
          width:100%;
          max-width:700px;
        "
      >
        ${rows.map(([key, value]) => `
          <tr>
            <td
              style="
                font-weight:bold;
                background:#f7f7f7;
                width:220px;
              "
            >
              ${esc(key)}
            </td>
            <td>
              ${esc(value).replace(/\n/g, '<br>')}
            </td>
          </tr>
        `).join('')}
      </table>

      <p style="
        margin-top:20px;
        font-size:12px;
        color:#777;
      ">
        Messaggio generato automaticamente dal sito
        www.rivettiimpianti.it
      </p>
    </div>
  `;

  /*
   * Collegamento sicuro a Gmail tramite
   * Password per le app.
   */
  const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: GMAIL_USER,
      pass: GMAIL_APP_PASSWORD
    }
  });

  try {

    await transporter.sendMail({
      from: `"Rivetti Impianti - Sito Web" <${GMAIL_USER}>`,
      to: MAIL_TO,
      replyTo: replyTo || GMAIL_USER,
      subject: subject.replace(/[\r\n]/g, ' '),
      html
    });

    return response(res, 200, {
      success: true
    });

  } catch (err) {

    console.error('Errore invio Gmail:', err);

    return error(
      res,
      'Non è stato possibile inviare la richiesta. Riprova.',
      502
    );
  }
};