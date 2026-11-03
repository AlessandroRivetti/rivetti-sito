/* =====================================================
   GLOBO 3D della Home — illustrazione grafica sull'energia (concept, non rappresenta progetti)
   Ottimizzato per non pesare su Core Web Vitals e su mobile:
   - il contenuto della pagina e il globo illustrato statico (SVG) sono già visibili: il 3D arriva dopo,
     a pagina caricata e a browser inattivo;
   - NON parte (resta il globo statico) con "riduci movimento", risparmio dati, connessione lenta
     o dispositivo con poca memoria/CPU;
   - si ferma quando l'hero è fuori schermo; sui telefoni usa meno pixel, meno linee e non blocca lo scorrimento.
   Nota tecnica: i dati degli archi vengono impostati UNA sola volta (riassegnarli durante l'animazione
   riavviava il flusso e faceva "bloccare" le linee).
   ===================================================== */
(() => {
  const el = document.getElementById('globe');
  if (!el) return;
  const hero = el.closest('.hero');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const conn = navigator.connection || {};
  const weak = conn.saveData || /(^|-)2g$/.test(conn.effectiveType || '') ||
    (navigator.deviceMemory && navigator.deviceMemory < 4) || (navigator.hardwareConcurrency && navigator.hardwareConcurrency < 4);
  if (reduce.matches || weak) return;                       // resta il globo statico

  const LIB = 'https://cdn.jsdelivr.net/npm/globe.gl@2.34.4/dist/globe.gl.min.js';
  const IMG = 'https://cdn.jsdelivr.net/npm/three-globe@2.31.0/example/img/';

  function init() {
    if (typeof Globe === 'undefined') return;
    const small = innerWidth < 900;
    const host = document.createElement('div');
    host.className = 'globe-canvas';
    el.appendChild(host);

    const plants = [   // sede aziendale + punti puramente decorativi (concept grafico sull'energia, non rappresentano progetti Rivetti)
      {lat:41.12, lng:13.88,  name:'Sede Rivetti Impianti · Mondragone (CE)', hq:true},
      {lat:37.4,  lng:-5.9},
      {lat:31.0,  lng:-6.9},
      {lat:24.8,  lng:55.2},
      {lat:27.0,  lng:71.0},
      {lat:40.0,  lng:96.0},
      {lat:-27.5, lng:140.0},
      {lat:-23.9, lng:-69.1},
      {lat:35.0,  lng:-116.0},
      {lat:-28.4, lng:21.3}
    ];
    const hubs = [     // nodi della rete che ricevono energia
      {lat:51.5,  lng:-0.1},  {lat:52.5,  lng:13.4},  {lat:45.5,  lng:9.2},   {lat:30.0,  lng:31.2},
      {lat:-1.3,  lng:36.8},  {lat:6.5,   lng:3.4},   {lat:-26.2, lng:28.0},  {lat:28.6,  lng:77.2},
      {lat:39.9,  lng:116.4}, {lat:35.7,  lng:139.7}, {lat:1.35,  lng:103.8}, {lat:-33.9, lng:151.2},
      {lat:40.7,  lng:-74.0}, {lat:19.4,  lng:-99.1}, {lat:-23.5, lng:-46.6}, {lat:64.1,  lng:-21.9}
    ];
    const rad = x => x * Math.PI / 180;
    const dist = (a,b) => Math.acos(Math.min(1, Math.sin(rad(a.lat))*Math.sin(rad(b.lat)) + Math.cos(rad(a.lat))*Math.cos(rad(b.lat))*Math.cos(rad(b.lng-a.lng))));

    /* ogni impianto alimenta i nodi più vicini (la sede ne alimenta di più); sui telefoni meno linee */
    const arcs = plants.flatMap((p, pi) =>
      [...hubs].sort((a,b) => dist(p,a) - dist(p,b)).slice(0, p.hq ? (small ? 4 : 6) : (small ? 1 : 3)).map((h, i) => ({
        startLat:p.lat, startLng:p.lng, endLat:h.lat, endLng:h.lng,
        time: 2600 + ((pi * 3 + i) % 5) * 450,
        gap: ((pi * 7 + i * 3) % 10) / 10
      })));

    const solarSVG = `<svg viewBox="0 0 32 28" aria-hidden="true" focusable="false">
      <path d="M6 4h22l-4 14H2z" fill="#1e6fe6" stroke="#9fd0ff" stroke-width="1.3" stroke-linejoin="round"/>
      <path d="M4.7 8.5H26.7M3.3 13.5H25.3M13.3 4L9.3 18M20.7 4L16.7 18" stroke="#cfe8ff" stroke-width=".7" opacity=".9"/>
      <path d="M13 18v5M9.5 24.5h9" stroke="#bcd3ee" stroke-width="1.8" stroke-linecap="round"/></svg>`;

    const world = Globe({animateIn:true})(host)
      .globeImageUrl(IMG + 'earth-blue-marble.jpg')
      .bumpImageUrl(IMG + 'earth-topology.png')
      .backgroundColor('rgba(0,0,0,0)')
      .showAtmosphere(true)
      .atmosphereColor('#5cc8ff')
      .atmosphereAltitude(0.22)

      /* nodi di rete */
      .pointsData(hubs)
      .pointColor(() => '#66c2ff')
      .pointAltitude(0.012)
      .pointRadius(0.4)

      /* marker con moduli blu: solo la sede ha testo e descrizione accessibile, gli altri sono decorativi (nessun testo, link o focus) */
      .htmlElementsData(plants)
      .htmlLat('lat').htmlLng('lng')
      .htmlAltitude(0.012)
      .htmlElement(d => {
        const n = document.createElement('div');
        n.className = 'pv' + (d.hq ? ' hq' : '');
        if (d.hq) { n.title = d.name; n.setAttribute('role', 'img'); n.setAttribute('aria-label', d.name); }
        else n.setAttribute('aria-hidden', 'true');
        n.innerHTML = solarSVG;
        return n;
      })

      /* onde di energia dagli impianti (sui telefoni solo dalla sede) */
      .ringsData(small ? plants.filter(p => p.hq) : plants)
      .ringColor(d => t => `rgba(255,210,63,${(1 - t) * (d.hq ? 1 : .8)})`)
      .ringMaxRadius(d => d.hq ? 6 : 3.6)
      .ringPropagationSpeed(2.2)
      .ringRepeatPeriod(1500)

      /* fili luminosi: dall'impianto (giallo) sfumano verso il blu dei nodi di rete */
      .arcsData(arcs)
      .arcColor(() => ['rgba(255,214,10,.98)', 'rgba(255,190,50,.9)', 'rgba(59,157,255,.95)'])
      .arcStroke(0.45)
      .arcCurveResolution(small ? 24 : 48)
      .arcAltitudeAutoScale(0.42)
      .arcDashLength(0.4)
      .arcDashGap(0.2)
      .arcDashInitialGap('gap')
      .arcDashAnimateTime('time');

    /* i marker sul lato nascosto del globo spariscono (se supportato dalla versione) */
    if (world.htmlElementVisibilityModifier) {
      world.htmlElementVisibilityModifier((node, visible) => { node.style.opacity = visible ? '1' : '0'; });
    }

    /* prestazioni: limita i pixel per non appesantire gli schermi ad alta densità */
    world.renderer().setPixelRatio(Math.min(devicePixelRatio || 1, small ? 1.5 : 2));
    /* sui telefoni un trascinamento verticale sul globo deve far scorrere la pagina, non bloccarla */
    world.renderer().domElement.style.touchAction = 'pan-y';

    const mat = world.globeMaterial();
    mat.color.set('#ffffff');            /* colori naturali della foto satellitare, nessuna tinta */
    mat.emissive.set('#0b2a4d');
    mat.emissiveIntensity = 0.12;
    mat.bumpScale = 4;                   /* rilievo leggero di montagne e oceani */

    const ctrl = world.controls();
    ctrl.autoRotate = true;
    ctrl.autoRotateSpeed = 0.55;
    ctrl.enableZoom = false;
    ctrl.enablePan = false;
    ctrl.enableDamping = true;

    world.pointOfView({lat:36, lng:20, altitude:2.35}, 0);

    const fit = () => world.width(host.clientWidth).height(host.clientHeight);
    fit();
    new ResizeObserver(fit).observe(host);

    /* durante il trascinamento la rotazione automatica si ferma e poi riprende da sola */
    let t;
    host.addEventListener('pointerdown', () => { ctrl.autoRotate = false; clearTimeout(t); });
    addEventListener('pointerup', () => { clearTimeout(t); t = setTimeout(() => { ctrl.autoRotate = !reduce.matches; }, 1800); });

    /* se l'utente attiva "riduci movimento" mentre il globo è acceso, la rotazione si ferma */
    reduce.addEventListener('change', () => { ctrl.autoRotate = !reduce.matches; });

    /* pausa quando l'hero è completamente fuori schermo */
    new IntersectionObserver(([e]) => e.isIntersecting ? world.resumeAnimation() : world.pauseAnimation(), {threshold:0}).observe(el);

    requestAnimationFrame(() => hero.classList.add('globe-on'));   // dissolvenza dal globo statico al 3D
  }

  function load() {
    /* la texture della Terra viene scaricata prima: il 3D compare solo quando è pronto, senza "salti" */
    const tex = new Image();
    tex.onload = () => {
      const s = document.createElement('script');
      s.src = LIB;
      s.onload = () => { try { init(); } catch (e) { /* resta il globo statico */ } };
      document.head.appendChild(s);
    };
    tex.src = IMG + 'earth-blue-marble.jpg';
  }

  const start = () => (window.requestIdleCallback ? requestIdleCallback(load, { timeout: 4000 }) : setTimeout(load, 1500));
  if (document.readyState === 'complete') start(); else addEventListener('load', start);
})();
