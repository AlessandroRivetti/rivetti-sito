/* Funzioni comuni delle pagine del sito: menu, finestre, filtri, moduli.
   Non imposta cookie e non usa localStorage/sessionStorage. */
(() => {
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const page = document.body.dataset.page;
  const ctx = window.RI ? RI.context() : {};

  const y = $('#y'); if (y) y.textContent = new Date().getFullYear();

  /* UTM: se l'indirizzo d'ingresso li contiene, vengono riportati sui link interni, così non si perdono
     passando da una pagina all'altra (nessuna memorizzazione). */
  const utmQ = Object.keys(ctx).filter(k => k.startsWith('utm_')).map(k => k + '=' + encodeURIComponent(ctx[k])).join('&');
  if (utmQ) $$('a[href]').forEach(a => {
    const h = a.getAttribute('href');
    if (!/^\/?[\w\-]+\.html(#.*)?$/.test(h)) return;
    const [p, hash] = h.split('#');
    a.setAttribute('href', p + '?' + utmQ + (hash ? '#' + hash : ''));
  });

  /* ============ MENU ============ */
  const head = $('#siteHead'), burger = $('#burger'), menu = $('#menu');
  const onScroll = () => head.classList.toggle('scrolled', scrollY > 30);
  onScroll(); addEventListener('scroll', onScroll, { passive: true });
  const setMenu = open => {
    menu.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', open);
    burger.setAttribute('aria-label', open ? 'Chiudi il menu' : 'Apri il menu');
  };
  burger.addEventListener('click', () => setMenu(!menu.classList.contains('open')));
  /* tendine: su desktop si aprono al passaggio del mouse o con la tastiera; su tablet/telefono con un tocco */
  const dds = $$('.dropdown'), narrow = matchMedia('(max-width:1320px)');
  dds.forEach(d => $('.dd-trigger', d).addEventListener('click', e => {
    if (!narrow.matches) return;
    e.preventDefault(); e.stopPropagation();
    const open = d.classList.toggle('open'); e.currentTarget.setAttribute('aria-expanded', open);
  }));
  menu.addEventListener('click', e => { if (e.target.closest('a')) { setMenu(false); dds.forEach(d => d.classList.remove('open')); } });
  addEventListener('keydown', e => {
    if (e.key === 'Escape' && menu.classList.contains('open')) { setMenu(false); burger.focus(); }
  });

  /* evidenzia la voce di menu della sezione visibile (solo Home) */
  if (page === 'home' && 'IntersectionObserver' in window) {
    const MAP = { home: 'home', numeri: 'home', servizi: 'servizi', privati: 'servizi', aziende: 'servizi', pa: 'servizi',
      incentivi: 'incentivi', informazioni: 'informazioni', lavora: 'lavora', recensioni: 'recensioni', faq: 'recensioni', contatti: 'contatti' };
    const links = $$('#menu a[data-spy]');
    const spy = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) links.forEach(a => a.classList.toggle('active', a.dataset.spy === MAP[e.target.id]));
    }), { rootMargin: '-40% 0px -55% 0px' });
    Object.keys(MAP).forEach(id => { const s = document.getElementById(id); if (s) spy.observe(s); });
  }

  /* ============ FINESTRE (incentivi) ============ */
  const openDialog = id => {
    const d = document.getElementById(id);
    if (d && d.showModal) { d.showModal(); document.body.classList.add('modal-open'); return true; }
    return false;
  };
  $$('[data-modal]').forEach(b => b.addEventListener('click', e => { if (openDialog(b.dataset.modal)) e.preventDefault(); }));
  $$('[data-open]').forEach(b => b.addEventListener('click', () => openDialog(b.dataset.open)));
  $$('dialog.modal').forEach(d => {
    d.addEventListener('click', e => { if (e.target === d || e.target.closest('[data-close]')) d.close(); });   // sfondo, X o pulsante
    d.addEventListener('close', () => document.body.classList.remove('modal-open'));                            // anche con ESC
  });

  /* ============ FILTRI REALIZZAZIONI ============
     Senza JavaScript tutte le schede restano visibili. Due gruppi (cliente, tipologia): le scelte si combinano. */
  const filters = $('.r-filters');
  if (filters) {
    filters.hidden = false;
    const cards = $$('.r-card'), vuoto = $('#rVuoto'), conta = $('#rCount');
    const sel = { cliente: '*', tipo: '*' };
    const applica = () => {
      let n = 0;
      cards.forEach(c => {
        const ok = (sel.cliente === '*' || c.dataset.cliente === sel.cliente) &&
                   (sel.tipo === '*' || (c.dataset.tipo || '').split(' ').includes(sel.tipo));
        c.hidden = !ok; if (ok) n++;
      });
      if (vuoto) vuoto.hidden = n > 0;
      if (conta) { conta.hidden = false; conta.textContent = n === 1 ? '1 progetto' : n + ' progetti'; }
    };
    filters.addEventListener('click', e => {
      const b = e.target.closest('[data-filter]'); if (!b) return;
      const g = b.closest('[data-group]');
      sel[g.dataset.group] = b.dataset.filter;
      $$('.chip', g).forEach(c => { const on = c === b; c.classList.toggle('on', on); c.setAttribute('aria-pressed', on); });
      applica();
    });
  }

  /* ============ GALLERIA DEL PROGETTO (visualizzatore accessibile da tastiera) ============
     Pulsanti reali, finestra modale nativa (focus intrappolato, ESC chiude), frecce ← → e pulsanti per scorrere. */
  const lb = $('#lightbox');
  if (lb && lb.showModal) {
    const btns = $$('.gal-btn'), img = $('#galImg'), cap = $('#galCap'), num = $('#galNum');
    let i = 0, ultimo = null;
    const mostra = n => {
      i = (n + btns.length) % btns.length;
      const b = btns[i];
      img.src = b.dataset.full; img.alt = b.dataset.alt;
      cap.textContent = b.dataset.cap || (b.dataset.nocap ? '' : b.dataset.alt);   // Galleria lavori: nessun testo se non compilato
      num.textContent = (i + 1) + ' di ' + btns.length;
    };
    btns.forEach(b => b.addEventListener('click', () => { ultimo = b; mostra(+b.dataset.gal); lb.showModal(); document.body.classList.add('modal-open'); }));
    $('#galPrev').addEventListener('click', () => mostra(i - 1));
    $('#galNext').addEventListener('click', () => mostra(i + 1));
    lb.addEventListener('keydown', e => {
      if (e.key === 'ArrowLeft') { e.preventDefault(); mostra(i - 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); mostra(i + 1); }
      if (e.key === 'Tab') {                                   /* il focus resta dentro la finestra: dall'ultimo pulsante si torna al primo */
        const f = $$('button', lb).filter(x => !x.hidden && x.offsetParent !== null), primo = f[0], ultimo2 = f[f.length - 1];
        if (!f.length) return;
        if (e.shiftKey && document.activeElement === primo) { e.preventDefault(); ultimo2.focus(); }
        else if (!e.shiftKey && document.activeElement === ultimo2) { e.preventDefault(); primo.focus(); }
      }
    });
    /* scorrimento con il dito: trascina a sinistra/destra per cambiare foto */
    let x0 = null, y0 = null;
    lb.addEventListener('touchstart', e => { if (e.touches.length === 1) { x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; } }, { passive: true });
    lb.addEventListener('touchend', e => {
      if (x0 === null || btns.length < 2) return;
      const dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
      x0 = y0 = null;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) mostra(i + (dx < 0 ? 1 : -1));
    }, { passive: true });
    lb.addEventListener('close', () => { if (ultimo) ultimo.focus(); });          // il focus torna alla miniatura
    if (btns.length < 2) $$('#galPrev, #galNext', lb).forEach(x => { x.hidden = true; });
  }

  /* ============ RECENSIONI PUBBLICATE (Home) ============
     Le recensioni arrivano via email; quelle approvate si incollano in recensioni.js. */
  /* Senza recensioni reali la sezione, la voce di menu e il link nel footer restano nascosti (attributo [data-rev]). */
  const grid = $('#revGrid');
  if (grid && window.RI) {
    const list = (window.RECENSIONI_APPROVATE || []).filter(r => r && r.testo && r.nome);
    if (list.length) { $$('[data-rev]').forEach(n => { n.hidden = false; });
      grid.innerHTML = list.map(r => `<figure class="rev">${RI.stars(r.stelle || 5)}
      <blockquote>“${RI.esc(r.testo)}”</blockquote>
      <figcaption><b>${RI.esc(r.nome)}</b><span>${RI.esc(r.tipo || 'Cliente')}${r.data ? ' · ' + RI.esc(r.data) : ''}</span></figcaption></figure>`).join(''); }
  }

  /* ============ LAVORA CON NOI ============ */
  const job = $('#jobMail');
  if (job) job.href = 'mailto:' + RI.MAIL_TO + '?subject=' + encodeURIComponent('Candidatura – Lavora con noi') +
    '&body=' + encodeURIComponent('Buongiorno,\nmi chiamo … e mi propongo come (tecnico / installatore / professionista).\nAllego il mio curriculum.\n\nRecapiti: \nZona di residenza: \n\nGrazie.');

  /* ============ PULSANTI "RICHIEDI UN SOPRALLUOGO": preselezionano il servizio ============ */
  $$('[data-service]').forEach(a => a.addEventListener('click', () => {
    const sel = $('#servizio'), v = a.dataset.service;
    if (sel && [...sel.options].some(o => o.value === v)) sel.value = v;
  }));

  /* ============ MODULO DI RICHIESTA ============
     Invio in POST tramite RI.send (vedi ri.js). Se la consegna non è confermata si apre la posta con il
     messaggio già compilato: nessuna richiesta si perde. Pagina di invio, provenienza e UTM sono raccolti
     in automatico nei campi nascosti: il cliente non deve compilare nulla in più. */
  const form = $('#quoteForm');
  if (form && window.RI) {
    const msg = $('#formMsg'), sendBtn = $('#sendBtn');
    const setMsg = (t, cls) => { msg.textContent = t; msg.className = 'form-msg full ' + (cls || ''); };
    const fill = () => Object.keys(ctx).forEach(k => { if (form.elements[k]) form.elements[k].value = ctx[k]; });
    fill();
    form.addEventListener('submit', async e => {
      e.preventDefault();
      if (form._honey.value) return;                                   // antispam: campo invisibile compilato solo dai robot
      if (!form.checkValidity()) { form.reportValidity(); setMsg('Compila correttamente i campi obbligatori.', 'err'); return; }
      const f = new FormData(form), v = k => String(f.get(k) || '').trim();
      const d = { nome: v('nome'), tel: v('telefono'), email: v('email'), tipo: v('tipo'), servizio: v('servizio'), comune: v('comune'), msg: v('messaggio') };
      const tecnici = {};
      if (v('pagina')) tecnici['Pagina di invio'] = v('pagina');
      if (v('referrer')) tecnici['Provenienza (referrer)'] = v('referrer');
      ['source', 'medium', 'campaign', 'content', 'term'].forEach(k => { if (v('utm_' + k)) tecnici['UTM ' + k] = v('utm_' + k); });
      sendBtn.disabled = true; setMsg('Invio in corso…');
      try {
        await RI.send(Object.assign({
          'Nome': d.nome, 'Telefono': d.tel, 'Tipo cliente': d.tipo, 'Comune o CAP': d.comune,
          'Servizio di interesse': d.servizio || 'Non indicato', 'Email': d.email || 'Non indicata', 'Messaggio': d.msg || '—'
        }, tecnici, {
          'Presa visione Informativa Privacy': 'Sì — ' + RI.now(),
          _subject: 'Richiesta dal sito — ' + d.tipo + (d.servizio ? ' — ' + d.servizio : ''), _template: 'table', _captcha: 'false'
        }));
        form.reset(); fill(); setMsg('Grazie! Richiesta inviata: ti ricontatteremo al più presto.', 'ok');
      } catch (err) {
        setMsg('Invio automatico non riuscito: si apre la tua posta per completare la richiesta.', 'err');
        RI.mailto('Richiesta dal sito — ' + d.tipo + (d.servizio ? ' — ' + d.servizio : ''),
          `Nome: ${d.nome}\nTelefono: ${d.tel}\nEmail: ${d.email}\nTipo cliente: ${d.tipo}\nComune o CAP: ${d.comune}\nServizio: ${d.servizio}\n\n${d.msg}\n\n(Pagina: ${v('pagina')})`);
      } finally { sendBtn.disabled = false; }
    });
  }
})();
