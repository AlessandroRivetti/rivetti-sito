/* =====================================================
   GLOBO 3D FOTOREALISTICO CON LUCE SOLARE E FORME GEOMETRICHE
   ===================================================== */
(() => {
  const el = document.getElementById('globe');
  if (!el) return;
  const hero = el.closest('.hero');

  const LIB = 'https://cdn.jsdelivr.net/npm/globe.gl@2.34.4/dist/globe.gl.min.js';
  const THREE_LIB = 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js';
  const IMG = 'https://cdn.jsdelivr.net/npm/three-globe@2.31.0/example/img/';

  function init() {
    if (typeof Globe === 'undefined') return;
    const small = innerWidth < 900;
    const host = document.createElement('div');
    host.className = 'globe-canvas';
    el.appendChild(host);

    // Punti con moduli fotovoltaici (Sede + Punti nel mondo)
    const plants = [
      {lat:41.12, lng:13.88,  name:'Sede Rivetti Impianti · Mondragone', hq:true},
      {lat:40.41, lng:-3.70,  name:'Impianto Spagna'},
      {lat:31.95, lng:35.91,  name:'Impianto Medio Oriente'},
      {lat:25.20, lng:55.27,  name:'Impianto UAE'},
      {lat:34.05, lng:-118.24,name:'Impianto USA'},
      {lat:-23.55,lng:-46.63, name:'Impianto Sud America'}
    ];

    // Nodi di rete collegati
    const hubs = [
      {lat:51.50, lng:-0.12}, {lat:48.85, lng:2.35},  {lat:41.90, lng:12.49},
      {lat:35.67, lng:139.65},{lat:1.35,  lng:103.81},{lat:37.77, lng:-122.41}
    ];

    const rad = x => x * Math.PI / 180;
    const dist = (a,b) => Math.acos(Math.min(1, Math.sin(rad(a.lat))*Math.sin(rad(b.lat)) + Math.cos(rad(a.lat))*Math.cos(rad(b.lat))*Math.cos(rad(b.lng-a.lng))));

    // Archi di collegamento (Sfumi da Giallo a Blu)
    const arcs = plants.flatMap((p) =>
      [...hubs].sort((a,b) => dist(p,a) - dist(p,b)).slice(0, p.hq ? 5 : 2).map((h, i) => ({
        startLat: p.lat, startLng: p.lng, endLat: h.lat, endLng: h.lng,
        time: 2000 + i * 500
      }))
    );

    // Icona SVG del Pannello Fotovoltaico
    const solarSVG = `<svg viewBox="0 0 32 28" class="pv-icon">
      <path d="M6 4h22l-4 14H2z" fill="#1f6fd1" stroke="#82d830" stroke-width="1.5" stroke-linejoin="round"/>
      <path d="M4.7 8.5H26.7M3.3 13.5H25.3M13.3 4L9.3 18M20.7 4L16.7 18" stroke="#ffffff" stroke-width="0.8" opacity="0.9"/>
      <path d="M13 18v5M9.5 24.5h9" stroke="#1f6fd1" stroke-width="2" stroke-linecap="round"/></svg>`;

    const world = Globe({animateIn:true})(host)
      .globeImageUrl(IMG + 'earth-blue-marble.jpg')
      .bumpImageUrl(IMG + 'earth-topology.png')
      .backgroundColor('rgba(0,0,0,0)')
      .showAtmosphere(true)
      .atmosphereColor('#1aa6d8')
      .atmosphereAltitude(0.25)

      // Punti luminosi
      .pointsData(hubs)
      .pointColor(() => '#ffc83d')
      .pointAltitude(0.02)
      .pointRadius(0.6)

      // Icone dei pannelli fotovoltaici
      .htmlElementsData(plants)
      .htmlLat('lat').htmlLng('lng')
      .htmlAltitude(0.025)
      .htmlElement(d => {
        const n = document.createElement('div');
        n.className = 'pv-marker' + (d.hq ? ' hq' : '');
        n.innerHTML = solarSVG;
        return n;
      })

      // Archi colorati Blu con sfumature e bagliore Giallo
      .arcsData(arcs)
      .arcColor(() => ['#ffc83d', '#1aa6d8', '#1f6fd1'])
      .arcStroke(0.7)
      .arcCurveResolution(64)
      .arcAltitudeAutoScale(0.35)
      .arcDashLength(0.5)
      .arcDashGap(0.15)
      .arcDashAnimateTime('time');

    /* CONFIGURAZIONE LUCE DEL SOLE LATERALE */
    const scene = world.scene();
    if (typeof THREE !== 'undefined') {
      // Rimuovi o riduci la luce ambiente standard
      scene.children.forEach(c => {
        if (c.isAmbientLight) c.intensity = 0.35;
      });

      // Aggiungi un punto di luce Solare intensa e laterale (Da destra)
      const sunLight = new THREE.DirectionalLight(0xfffaed, 2.2);
      sunLight.position.set(400, 100, 200);
      scene.add(sunLight);
    }

    /* PROPRIETÀ MATERIALE E RILIEVI */
    const mat = world.globeMaterial();
    mat.color.set('#ffffff');
    mat.emissive.set('#0a2347');
    mat.emissiveIntensity = 0.1;
    mat.bumpScale = 10;

    /* ROTAZIONE CONTINUA A 360° SENZA BLOCCARSI MAI */
    const ctrl = world.controls();
    ctrl.autoRotate = true;
    ctrl.autoRotateSpeed = 0.8; // Velocità di rotazione costante
    ctrl.enableZoom = false;
    ctrl.enablePan = false;

    // Disabilita lo stop al drag dell'utente
    ctrl.addEventListener('start', () => { ctrl.autoRotate = true; });
    ctrl.addEventListener('end', () => { ctrl.autoRotate = true; });

    world.pointOfView({lat: 25, lng: 10, altitude: small ? 1.9 : 1.65}, 0);

    const fit = () => world.width(host.clientWidth).height(host.clientHeight);
    fit();
    new ResizeObserver(fit).observe(host);

    if (hero) hero.classList.add('globe-on');
  }

  function load() {
    const s1 = document.createElement('script');
    s1.src = THREE_LIB;
    s1.onload = () => {
      const s2 = document.createElement('script');
      s2.src = LIB;
      s2.onload = () => { try { init(); } catch (e) { console.error(e); } };
      document.head.appendChild(s2);
    };
    document.head.appendChild(s1);
  }

  if (document.readyState === 'complete') load(); else addEventListener('load', load);
})();