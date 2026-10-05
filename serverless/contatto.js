/* =========================================================================
   Endpoint per i moduli del sito (preventivo e recensione) — sostituisce FormSubmit.
   Pronto per Cloudflare Pages Functions: copia questo file in  functions/api/contatto.js
   (per Vercel / Netlify basta un piccolo adattatore: la logica sta in handle()).

   Variabili d'ambiente da impostare nel pannello del provider (MAI nel sito):
     RESEND_API_KEY   chiave API del servizio email Resend (resend.com)
     MAIL_FROM        mittente su dominio verificato, es. "Sito Rivetti <sito@rivettiimpianti.it>"
     MAIL_TO          rivettiimpianti@gmail.com
     ALLOWED_ORIGIN   https://www.rivettiimpianti.it   (accetta richieste solo da qui)

   Poi in ri.js cambia:  const FORM_ENDPOINT = '/api/contatto';
   ========================================================================= */

const MAX = { nome: 80, telefono: 20, email: 120, servizio: 120, messaggio: 2000, tipo: 60, recensione: 1200 };
const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clean = (v, max) => String(v == null ? '' : v).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, '').trim().slice(0, max);
const json = (obj, status) => new Response(JSON.stringify(obj), { status, headers: { 'Content-Type': 'application/json' } });
const fail = (message, status) => json({ success: false, message }, status || 400);

export async function handle(request, env, fetchImpl) {
  fetchImpl = fetchImpl || fetch;
  if (!env.RESEND_API_KEY || !env.MAIL_FROM || !env.MAIL_TO) return fail('Servizio non configurato.', 500);
  const origin = request.headers.get('Origin') || '';
  if (env.ALLOWED_ORIGIN && origin !== env.ALLOWED_ORIGIN) return fail('Richiesta non consentita.', 403);
  if (!(request.headers.get('Content-Type') || '').includes('application/json')) return fail('Formato non valido.', 415);

  let b;
  try { b = await request.json(); } catch (e) { return fail('Dati non validi.'); }
  if (!b || typeof b !== 'object' || Array.isArray(b)) return fail('Dati non validi.');
  if (b._honey) return json({ success: true }, 200);                 // antispam: i robot compilano il campo nascosto; fingiamo di accettare

  const isReview = 'Recensione' in b;
  const f = {};
  f.nome = clean(b.Nome, MAX.nome);
  if (f.nome.length < 2) return fail('Inserisci il nome.');
  let rows;
  if (isReview) {
    const stelle = parseInt(String(b.Stelle), 10);
    f.tipo = clean(b['Tipo cliente'], MAX.tipo);
    f.testo = clean(b.Recensione, MAX.recensione);
    if (!(stelle >= 1 && stelle <= 5)) return fail('Voto non valido.');
    if (f.testo.split(/\s+/).filter(Boolean).length < 5) return fail('La recensione deve contenere almeno 5 parole.');
    if (!/^S[iì]/.test(clean(b['Consenso alla pubblicazione di nome e recensione'], 60))) return fail('Serve il consenso alla pubblicazione.');
    rows = [['Voto', stelle + ' su 5'], ['Nome', f.nome], ['Tipo cliente', f.tipo], ['Recensione', f.testo],
            ['Consenso alla pubblicazione', clean(b['Consenso alla pubblicazione di nome e recensione'], 60)]];
  } else {
    f.telefono = clean(b.Telefono, MAX.telefono); f.email = clean(b.Email, MAX.email);
    f.servizio = clean(b.Servizio, MAX.servizio); f.messaggio = clean(b.Messaggio, MAX.messaggio);
    if (!/^[0-9+()\s.\-]{6,20}$/.test(f.telefono)) return fail('Telefono non valido.');
    if (!/^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]{2,}$/.test(f.email)) return fail('Email non valida.');
    if (!f.servizio) return fail('Seleziona il servizio.');
    rows = [['Nome', f.nome], ['Telefono', f.telefono], ['Email', f.email], ['Servizio', f.servizio], ['Messaggio', f.messaggio],
            ['Presa visione Informativa Privacy', clean(b['Presa visione Informativa Privacy'], 60)]];
  }
  const subject = (isReview ? 'Nuova recensione da approvare — ' + clean(b.Stelle, 6) + ' — ' : 'Richiesta preventivo dal sito — ' + f.servizio + ' — ').replace(/[\r\n]/g, ' ') + f.nome;
  const html = '<table cellpadding="6" style="font-family:sans-serif">' + rows.map(([k, v]) => `<tr><td><b>${esc(k)}</b></td><td>${esc(v).replace(/\n/g, '<br>')}</td></tr>`).join('') + '</table>';

  const body = { from: env.MAIL_FROM, to: [env.MAIL_TO], subject, html };
  if (!isReview) body.reply_to = f.email;                           // "Rispondi" va direttamente al cliente
  let r;
  try {
    r = await fetchImpl('https://api.resend.com/emails', {
      method: 'POST', headers: { 'Authorization': 'Bearer ' + env.RESEND_API_KEY, 'Content-Type': 'application/json' }, body: JSON.stringify(body)
    });
  } catch (e) { return fail('Invio non riuscito, riprova.', 502); }
  if (!r.ok) return fail('Invio non riuscito, riprova.', 502);
  return json({ success: true }, 200);
}

/* Cloudflare Pages Functions */
export const onRequestPost = ({ request, env }) => handle(request, env);
export const onRequest = () => fail('Metodo non consentito.', 405);   // eventuale GET o altri metodi
