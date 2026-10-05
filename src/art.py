"""Illustrazioni vettoriali dei servizi e sticker dei bonus (generate qui, incollate in index.html)."""
import math

FONT = 'font-family="Inter,sans-serif"'

DEFS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<linearGradient id="gSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fcaf6"/><stop offset="1" stop-color="#eaf6ff"/></linearGradient>
<linearGradient id="gPanel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2f7fe3"/><stop offset="1" stop-color="#14489a"/></linearGradient>
<linearGradient id="gHill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#93d8a8"/><stop offset="1" stop-color="#5dbb82"/></linearGradient>
<linearGradient id="gTherm" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#2b5cd9"/><stop offset=".25" stop-color="#26b6d8"/><stop offset=".5" stop-color="#5fd07a"/><stop offset=".72" stop-color="#ffd23f"/><stop offset="1" stop-color="#ff3b1f"/></linearGradient>
<linearGradient id="gCone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd23f" stop-opacity=".55"/><stop offset="1" stop-color="#ffd23f" stop-opacity="0"/></linearGradient>
<radialGradient id="gHot"><stop offset="0" stop-color="#fff6b0"/><stop offset=".35" stop-color="#ffb000"/><stop offset=".75" stop-color="#ff3b1f"/><stop offset="1" stop-color="#ff3b1f" stop-opacity="0"/></radialGradient>
<symbol id="mod" viewBox="0 0 60 36"><rect width="60" height="36" rx="2" fill="url(#gPanel)" stroke="#dbe9fb" stroke-width="1.6"/><path d="M15 0V36M30 0V36M45 0V36M0 12H60M0 24H60" stroke="#8fc0f5" stroke-width=".8" opacity=".85"/></symbol>
<symbol id="sun" viewBox="0 0 64 64"><g stroke="#ffc83d" stroke-width="3" stroke-linecap="round"><path d="M32 3v8M32 53v8M3 32h8M53 32h8M11 11l6 6M47 47l6 6M53 11l-6 6M17 47l-6 6"/></g><circle cx="32" cy="32" r="14" fill="#ffd23f"/></symbol>
<symbol id="spark" viewBox="-10 -10 20 20"><path d="M0-10L2-2 10 0 2 2 0 10-2 2-10 0-2-2z" fill="#fff"/></symbol>
<symbol id="drop" viewBox="-7 -8 14 16"><path d="M0-7C4-1 6 2 0 6C-6 2-4-1 0-7z" fill="#4fb3f2"/></symbol>
</defs></svg>'''


def svg(vb, inner):
    return f'<svg viewBox="{vb}" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">{inner}</svg>'


def mod(x, y, w, h):
    return f'<use href="#mod" x="{x}" y="{y}" width="{w}" height="{h}"/>'


def para(x, y, w, h, s, fill="url(#gPanel)", grid=True):
    """Pannello in prospettiva: bordo alto spostato a destra di s."""
    p = f'<polygon points="{x+s},{y} {x+w+s},{y} {x+w},{y+h} {x},{y+h}" fill="{fill}" stroke="#dbe9fb" stroke-width="1"/>'
    if grid:
        p += (f'<path d="M{x+w/2+s/2:.1f} {y}L{x+w/2:.1f} {y+h}M{x+s/2:.1f} {y+h/2:.1f}H{x+w+s/2:.1f}" stroke="#8fc0f5" stroke-width=".8" opacity=".8"/>')
    return p


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def thermal(t):
    stops = [(0, (43, 92, 217)), (.25, (38, 182, 216)), (.5, (95, 208, 122)), (.72, (255, 210, 63)), (.88, (255, 138, 43)), (1, (255, 59, 31))]
    t = max(0, min(1, t))
    for i in range(len(stops) - 1):
        if stops[i][0] <= t <= stops[i + 1][0]:
            u = (t - stops[i][0]) / (stops[i + 1][0] - stops[i][0])
            c = lerp(stops[i][1], stops[i + 1][1], u)
            return '#%02x%02x%02x' % c
    return '#ff3b1f'


# ---------------------------------------------------------------- PRIVATI (400x250)
def fv_domestico():
    tilt = -6.56
    roof = ''.join(mod(i * 55, -30, 51, 28) for i in range(4))
    return svg('0 0 400 250', f'''
<rect width="400" height="250" fill="url(#gSky)"/>
<use href="#sun" x="305" y="10" width="70" height="70"/>
<path d="M0 205Q100 172 210 196T400 188V250H0Z" fill="url(#gHill)"/>
<path d="M0 228Q140 206 260 226T400 216V250H0Z" fill="#46a872"/>
<rect x="70" y="138" width="190" height="84" fill="#fff" stroke="#c7d7ea" stroke-width="2"/>
<polygon points="52,140 278,140 278,98 52,124" fill="#d3dcea" stroke="#b7c6db" stroke-width="2"/>
<g transform="translate(64,122.6) skewY({tilt})">{roof}</g>
<rect x="98" y="174" width="28" height="48" rx="2" fill="#2f7fe3"/>
<rect x="160" y="162" width="56" height="38" rx="2" fill="#cfe8fb" stroke="#9ec3e8" stroke-width="2"/>
<path d="M188 162v38M160 181h56" stroke="#9ec3e8" stroke-width="2"/>
<rect x="290" y="170" width="36" height="56" rx="7" fill="#e7f8ef" stroke="#23a36a" stroke-width="2.5" stroke-dasharray="5 4"/>
<path d="M310 186l-9 15h8l-3 14 11-17h-8z" fill="#23a36a"/>
<path d="M276 118C300 120 308 140 308 168" fill="none" stroke="#23a36a" stroke-width="2" stroke-dasharray="4 4"/>
<rect x="246" y="229" width="124" height="17" rx="8.5" fill="#fff" fill-opacity=".92"/><text x="308" y="241" text-anchor="middle" font-size="11" font-weight="600" {FONT} fill="#17804f">Accumulo opzionale</text>''')


def accumulo():
    stars = ''.join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="#fff"/>' for x, y in [(230, 30), (262, 58), (300, 24), (330, 70), (372, 96), (250, 100), (392, 40)])
    bars = ''.join(f'<rect x="168" y="{y}" width="64" height="18" rx="4" fill="#23a36a"/>' for y in (84, 108, 132, 156))
    return svg('0 0 400 250', f'''
<rect width="400" height="250" fill="url(#gSky)"/>
<rect x="200" width="200" height="250" fill="#16335f"/>{stars}
<path d="M352 28a22 22 0 1 0 14 38a18 18 0 0 1-14-38z" fill="#ffe9a8"/>
<use href="#sun" x="14" y="10" width="60" height="60"/>
<rect y="218" width="400" height="32" fill="#7fc79a" opacity=".55"/>
<g transform="translate(18,150) skewX(-12)">{mod(0,0,84,50)}</g>
<path d="M112 176H142" stroke="#23a36a" stroke-width="5" stroke-linecap="round"/><polygon points="140,167 156,176 140,185" fill="#23a36a"/>
<rect x="186" y="56" width="28" height="14" rx="4" fill="#14539f"/>
<rect x="150" y="68" width="100" height="126" rx="16" fill="#fff" stroke="#1f6fd1" stroke-width="5"/>{bars}
<circle cx="250" cy="74" r="17" fill="#ffc83d" stroke="#fff" stroke-width="3"/><path d="M252 64l-9 12h7l-3 11 11-14h-7z" fill="#0f2a4a"/>
<path d="M258 176H290" stroke="#23a36a" stroke-width="5" stroke-linecap="round"/><polygon points="288,167 304,176 288,185" fill="#23a36a"/>
<rect x="308" y="150" width="72" height="62" fill="#e9f1fb"/>
<polygon points="300,152 344,114 388,152" fill="#b9c7dc"/>
<rect x="320" y="166" width="18" height="18" rx="2" fill="#ffd86b"/><rect x="350" y="166" width="18" height="18" rx="2" fill="#ffd86b"/><rect x="336" y="190" width="16" height="22" rx="2" fill="#2f7fe3"/>
<text x="96" y="242" text-anchor="middle" font-size="12" font-weight="600" {FONT} fill="#14539f">Di giorno</text>
<text x="344" y="242" text-anchor="middle" font-size="12" font-weight="600" {FONT} fill="#dfe9f8">Di sera</text>''')


def termo_clima():
    fins = ''.join(f'<rect x="{46 + i * 15}" y="142" width="12" height="58" rx="4" fill="#ffe3cf" stroke="#f3a06b" stroke-width="1.5"/>' for i in range(8))
    blades = ''.join(f'<path d="M0 0L0-20a20 20 0 0 1 14 6z" fill="#7fb3e8" transform="rotate({a})"/>' for a in (0, 90, 180, 270))
    waves = ''.join(f'<path d="M{x} 88c12 10-12 22 0 32s-12 20 0 30" fill="none" stroke="#62b6ef" stroke-width="3" stroke-linecap="round" opacity=".85"/>' for x in (56, 92, 128, 164))
    return svg('0 0 400 250', f'''
<rect width="400" height="250" fill="#f3f7fc"/>
<rect x="238" width="162" height="250" fill="url(#gSky)"/>
<rect x="228" width="10" height="250" fill="#cdd9e8"/>
<rect y="208" width="228" height="42" fill="#e8dccb"/><rect x="238" y="208" width="162" height="42" fill="#7fc79a"/>
<rect x="34" y="32" width="156" height="42" rx="12" fill="#fff" stroke="#c4d3e6" stroke-width="2"/>
<rect x="46" y="56" width="132" height="6" rx="3" fill="#dde7f3"/><circle cx="172" cy="44" r="4" fill="#23a36a"/>{waves}
<rect x="36" y="196" width="138" height="8" rx="3" fill="#cdd9e8"/>{fins}
<path d="M278 142V58H190" fill="none" stroke="#c98b5e" stroke-width="5" stroke-linejoin="round"/>
<path d="M262 142V90H232" fill="none" stroke="#e0553a" stroke-width="3"/>
<circle cx="278" cy="100" r="8" fill="#e0553a" stroke="#fff" stroke-width="2"/>
<rect x="262" y="142" width="108" height="66" rx="8" fill="#fff" stroke="#b8c9dd" stroke-width="2"/>
<circle cx="316" cy="175" r="25" fill="#e6eef8" stroke="#b8c9dd" stroke-width="2"/>
<g transform="translate(316 175)">{blades}</g><circle cx="316" cy="175" r="4" fill="#14539f"/>''')


def manutenzione():
    return svg('0 0 400 250', f'''
<rect width="400" height="250" fill="#e9f1fa"/>
<rect y="216" width="400" height="34" fill="#cfdcec"/>
<path d="M150 50V14M190 50V14" stroke="#26344a" stroke-width="4"/>
<rect x="112" y="50" width="116" height="126" rx="12" fill="#fff" stroke="#b4c7de" stroke-width="3"/>
<rect x="128" y="66" width="84" height="40" rx="6" fill="#0f2a4a"/>
<polyline points="134,96 146,88 158,92 170,80 184,86 198,74" fill="none" stroke="#46e3a0" stroke-width="2.6" stroke-linejoin="round"/>
<circle cx="136" cy="124" r="5" fill="#23a36a"/><circle cx="152" cy="124" r="5" fill="#23a36a"/><circle cx="168" cy="124" r="5" fill="#ffc83d"/>
<path d="M132 142H208M132 152H208M132 162H208" stroke="#dbe6f2" stroke-width="3" stroke-linecap="round"/>
<rect x="132" y="176" width="12" height="10" fill="#26344a"/><rect x="152" y="176" width="12" height="10" fill="#26344a"/><rect x="172" y="176" width="12" height="10" fill="#26344a"/><rect x="192" y="176" width="12" height="10" fill="#26344a"/>
<path d="M228 72L262 52" stroke="#1f6fd1" stroke-width="2.5"/>
<rect x="262" y="34" width="96" height="30" rx="15" fill="#1f6fd1"/><text x="310" y="54" text-anchor="middle" font-size="14" font-weight="700" {FONT} fill="#fff">Inverter</text>
<g {FONT} font-size="12.5" font-weight="600" fill="#0f2a4a">
<circle cx="276" cy="94" r="9" fill="#23a36a"/><path d="M271 94l4 4 6-8" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><text x="293" y="98">Prestazioni</text>
<circle cx="276" cy="124" r="9" fill="#23a36a"/><path d="M271 124l4 4 6-8" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><text x="293" y="128">Collegamenti</text>
<circle cx="276" cy="154" r="9" fill="#23a36a"/><path d="M271 154l4 4 6-8" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><text x="293" y="158">Sicurezza</text></g>
<rect x="50" y="188" width="14" height="30" fill="#26344a"/><rect x="68" y="188" width="14" height="30" fill="#26344a"/>
<rect x="44" y="120" width="44" height="72" rx="12" fill="#1f6fd1"/><rect x="44" y="148" width="44" height="6" fill="#ffc83d"/>
<path d="M88 134L118 122" stroke="#1f6fd1" stroke-width="12" stroke-linecap="round"/><circle cx="121" cy="121" r="6" fill="#f1c7a0"/>
<circle cx="66" cy="104" r="14" fill="#f1c7a0"/><path d="M44 100a22 20 0 0 1 44 0z" fill="#ffc83d"/><rect x="40" y="98" width="52" height="6" rx="3" fill="#f2b21e"/>
<g transform="translate(100,170) rotate(-40)"><rect x="-3" y="-20" width="6" height="42" rx="3" fill="#8a99ad"/><circle cy="-24" r="9" fill="#8a99ad"/><rect x="-3" y="-36" width="6" height="12" fill="#e9f1fa"/></g>''')


def lavaggio():
    grid = ''.join(f'<path d="M{x} 90V200" stroke="#8fc0f5" stroke-width="1.2"/>' for x in range(90, 340, 50)) + '<path d="M40 127H340M40 163H340" stroke="#8fc0f5" stroke-width="1.2"/>'
    blots = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#7d8a9b" opacity=".5"/>' for x, y, r in [(70, 110, 9), (120, 150, 13), (160, 120, 8), (95, 180, 10), (175, 175, 7)])
    sparks = ''.join(f'<use href="#spark" x="{x-10}" y="{y-10}" width="{s}" height="{s}"/>' for x, y, s in [(250, 120, 20), (300, 150, 26), (220, 170, 16), (330, 108, 16)])
    drops = ''.join(f'<use href="#drop" x="{x-7}" y="{y-8}" width="14" height="16"/>' for x, y in [(186, 168), (206, 176), (228, 158), (170, 190), (250, 184)])
    return svg('0 0 400 250', f'''
<rect width="400" height="250" fill="url(#gSky)"/>
<use href="#sun" x="10" y="8" width="56" height="56"/>
<path d="M0 214Q120 192 240 210T400 204V250H0Z" fill="url(#gHill)"/>
<g transform="matrix(1,0,-0.25,1,50,0)"><rect x="40" y="90" width="300" height="110" fill="url(#gPanel)" stroke="#dbe9fb" stroke-width="3"/>{grid}
<rect x="40" y="90" width="150" height="110" fill="#9aa7b8" opacity=".55"/>{blots}</g>
{sparks}
<path d="M356 28L200 130" stroke="#7b8a9e" stroke-width="6" stroke-linecap="round"/>
<g transform="translate(192,136) rotate(-32)"><rect x="-32" y="-8" width="64" height="15" rx="5" fill="#f0a93a"/><rect x="-30" y="7" width="60" height="7" rx="2" fill="#3a4a63"/></g>
{drops}
<circle cx="150" cy="200" r="7" fill="#fff" fill-opacity=".55" stroke="#bfe4fb" stroke-width="1.5"/><circle cx="162" cy="214" r="10" fill="#fff" fill-opacity=".55" stroke="#bfe4fb" stroke-width="1.5"/><circle cx="270" cy="206" r="6" fill="#fff" fill-opacity=".55" stroke="#bfe4fb" stroke-width="1.5"/>''')


def termografia():
    hot = (3, 1)
    cells = ''
    for r in range(4):
        for c in range(6):
            d = math.hypot(c - hot[0], (r - hot[1]) * 1.1)
            t = 0.12 + 0.88 * math.exp(-(d ** 2) / 1.6)
            if (c, r) == hot:
                t = 1
            cells += f'<rect x="{70 + c * 40}" y="{46 + r * 37.5}" width="38" height="35.5" rx="2" fill="{thermal(t)}"/>'
    hx, hy = 70 + 3 * 40 + 19, 46 + 37.5 + 17.75
    mini = ''.join(f'<rect x="{276 + i * 12}" y="{182 + (i % 2) * 6}" width="12" height="{40 - (i % 2) * 12}" fill="{thermal(0.15 + 0.14 * i)}"/>' for i in range(5))
    return svg('0 0 400 250', f'''
<rect width="400" height="250" fill="#0f2a4a"/>
<rect x="30" y="46" width="12" height="150" rx="3" fill="url(#gTherm)"/>
<text x="50" y="54" font-size="10" font-weight="600" {FONT} fill="#ffb4a8">caldo</text><text x="50" y="196" font-size="10" font-weight="600" {FONT} fill="#9fc4ff">freddo</text>
{cells}<circle cx="{hx}" cy="{hy}" r="26" fill="url(#gHot)" opacity=".85"/>
<circle cx="{hx}" cy="{hy}" r="15" fill="none" stroke="#fff" stroke-width="2"/><path d="M{hx-22} {hy}H{hx-8}M{hx+8} {hy}H{hx+22}M{hx} {hy-22}V{hy-8}M{hx} {hy+8}V{hy+22}" stroke="#fff" stroke-width="2"/>
<rect x="{hx+16}" y="{hy-42}" width="82" height="22" rx="11" fill="#fff"/><text x="{hx+57}" y="{hy-27}" text-anchor="middle" font-size="11.5" font-weight="700" {FONT} fill="#b83227">Punto caldo</text>
<rect x="262" y="168" width="116" height="74" rx="14" fill="#e6edf6" stroke="#9fb3cc" stroke-width="2"/>
<rect x="272" y="178" width="66" height="52" rx="6" fill="#0f2a4a"/>{mini}
<circle cx="356" cy="204" r="14" fill="#26344a" stroke="#9fb3cc" stroke-width="3"/><circle cx="356" cy="204" r="5" fill="#46e3a0"/>''')


# ---------------------------------------------------------------- AZIENDE (640x360)
def solare_termico():
    return svg('0 0 400 250', f'''
<rect width="400" height="250" fill="url(#gSky)"/>
<use href="#sun" x="30" y="16" width="64" height="64"/>
<rect y="214" width="400" height="36" fill="#7fc79a"/>
<polygon points="40,150 200,70 360,150" fill="#d98b6b" stroke="#b86a4b" stroke-width="2"/>
<rect x="64" y="150" width="272" height="66" fill="#fff" stroke="#c4d3e6" stroke-width="2"/>
<rect x="92" y="170" width="34" height="46" rx="3" fill="#cfe3f8" stroke="#9fbbdb" stroke-width="1.6"/>
<polygon points="140,134 296,134 312,92 156,92" fill="#0f3d7a" stroke="#dbe9fb" stroke-width="2"/>
<path d="M165 134L180 92M210 134L222 92M255 134L264 92M150 113H304" stroke="#8fc0f5" stroke-width="1.2" opacity=".8"/>
<rect x="268" y="160" width="46" height="56" rx="10" fill="#e6eef8" stroke="#b4c7de" stroke-width="2.4"/>
<rect x="268" y="186" width="46" height="30" fill="#ff9f5a" opacity=".55"/>
<path d="M291 134V160" stroke="#e0553a" stroke-width="3"/><path d="M279 134V160" stroke="#4fb3f2" stroke-width="3"/>
<use href="#drop" x="330" y="168" width="22" height="26"/>''')


def industriale():
    roof = ''.join(mod(70 + i * 56, 74 - i * 0 + (0), 52, 30) if False else f'<use href="#mod" x="{74 + i * 54}" y="74" width="50" height="30"/>' for i in range(5))
    roof2 = ''.join(f'<use href="#mod" x="{74 + i * 54}" y="108" width="50" height="30"/>' for i in range(5))
    doors = ''.join(f'<rect x="{92 + i * 70}" y="176" width="46" height="40" rx="2" fill="#cfd9e6" stroke="#9fb1c7" stroke-width="2"/><path d="M{92 + i * 70} 188H{138 + i * 70}M{92 + i * 70} 200H{138 + i * 70}" stroke="#9fb1c7" stroke-width="1.5"/>' for i in range(4))
    return svg('0 0 400 250', f'''
<rect width="400" height="250" fill="url(#gSky)"/>
<use href="#sun" x="316" y="10" width="64" height="64"/>
<rect y="214" width="400" height="36" fill="#9aa8ba"/><rect y="222" width="400" height="4" fill="#fff" opacity=".5"/>
<polygon points="48,150 352,150 336,66 64,66" fill="#e3ebf5" stroke="#b4c7de" stroke-width="2"/>
{roof}{roof2}
<rect x="48" y="150" width="304" height="66" fill="#f4f7fb" stroke="#b4c7de" stroke-width="2"/>
{doors}
<rect x="352" y="120" width="22" height="96" fill="#cdd9e8" stroke="#9fb1c7" stroke-width="2"/>''')


def om_fotovoltaico():
    rows = ''.join(f'<use href="#mod" x="{30 + i * 78}" y="{118 + (i % 2) * 0}" width="72" height="42"/>' for i in range(5))
    rows2 = ''.join(f'<use href="#mod" x="{14 + i * 82}" y="{168}" width="76" height="46"/>' for i in range(5))
    return svg('0 0 400 250', f'''
<rect width="400" height="250" fill="url(#gSky)"/>
<use href="#sun" x="20" y="12" width="60" height="60"/>
<path d="M0 118Q120 96 240 112T400 104V250H0Z" fill="url(#gHill)"/>
{rows}{rows2}
<rect x="262" y="40" width="108" height="62" rx="10" fill="#fff" stroke="#b4c7de" stroke-width="2.4"/>
<rect x="272" y="50" width="88" height="30" rx="5" fill="#0f2a4a"/>
<polyline points="278,72 292,64 306,68 322,58 338,62 352,54" fill="none" stroke="#46e3a0" stroke-width="2.4" stroke-linejoin="round"/>
<circle cx="282" cy="92" r="4" fill="#23a36a"/><circle cx="296" cy="92" r="4" fill="#23a36a"/><circle cx="310" cy="92" r="4" fill="#ffc83d"/>
<g {FONT} font-size="13" font-weight="700" fill="#fff"><rect x="150" y="30" width="78" height="28" rx="14" fill="#1f6fd1"/><text x="189" y="49" text-anchor="middle">O&amp;M</text></g>
<path d="M228 44H262" stroke="#1f6fd1" stroke-width="2.4"/>''')


def agrivoltaico():
    legs = ''.join(f'<path d="M{60 + i * 84} 118V196" stroke="#6b7a90" stroke-width="5"/>' for i in range(4))
    pan = ''.join(f'<polygon points="{36 + i * 84},96 {96 + i * 84},84 {104 + i * 84},112 {44 + i * 84},124" fill="url(#gPanel)" stroke="#dbe9fb" stroke-width="1.6"/>' for i in range(4))
    crops = ''.join(f'<path d="M{-20 + r * 18} 250L{150 + r * 40} 200" stroke="#3f9d5e" stroke-width="5" opacity=".75"/>' for r in range(0, 14))
    return svg('0 0 400 250', f'''
<rect width="400" height="250" fill="url(#gSky)"/>
<use href="#sun" x="316" y="8" width="64" height="64"/>
<rect y="196" width="400" height="54" fill="#8fcf9f"/>{crops}
{legs}{pan}
<g transform="translate(300 196)"><rect x="-22" y="-26" width="44" height="22" rx="4" fill="#e0553a"/><rect x="-6" y="-40" width="18" height="16" rx="3" fill="#b7432b"/><circle cx="-12" cy="-2" r="10" fill="#26344a"/><circle cx="16" cy="-4" r="14" fill="#26344a"/></g>''')


def cer():
    def casa(x, y, c):
        return (f'<polygon points="{x},{y} {x + 60},{y} {x + 60},{y + 50} {x},{y + 50}" fill="#fff" stroke="#b4c7de" stroke-width="2"/>'
                f'<polygon points="{x - 6},{y} {x + 30},{y - 28} {x + 66},{y} " fill="{c}" stroke="#b4c7de" stroke-width="1.5"/>'
                f'<use href="#mod" x="{x + 14}" y="{y - 18}" width="26" height="14"/>'
                f'<rect x="{x + 22}" y="{y + 20}" width="16" height="30" fill="#cfe3f8"/>')
    return svg('0 0 400 250', f'''
<rect width="400" height="250" fill="url(#gSky)"/>
<use href="#sun" x="326" y="6" width="56" height="56"/>
<rect y="206" width="400" height="44" fill="#8fcf9f"/>
{casa(34, 150, "#d98b6b")}{casa(170, 130, "#8aa4c4")}{casa(300, 150, "#d98b6b")}
<g fill="none" stroke="#ffc83d" stroke-width="3" stroke-dasharray="7 6" stroke-linecap="round"><path d="M64 128Q120 70 200 82"/><path d="M200 82Q290 70 330 128"/><path d="M200 82V100"/></g>
<circle cx="200" cy="72" r="20" fill="#ffd23f" stroke="#fff" stroke-width="3"/><path d="M203 60l-9 15h7l-3 12 10-16h-7z" fill="#0d2d58"/>''')


def utility_scale():
    rows = ''
    for y, h, w, gap in [(198, 16, 34, 6), (224, 24, 50, 8), (264, 34, 72, 10), (318, 46, 104, 14)]:
        s = h * 0.3
        n = int(700 / (w + gap)) + 2
        off = -(gap + w) * 0.4
        rows += ''.join(para(round(off + i * (w + gap), 1), y, w, h, s) for i in range(n))
    pyl = lambda x, sc: (f'<g transform="translate({x} 190) scale({sc})" stroke="#6b7a90" stroke-width="2.2" fill="none">'
                          '<path d="M-22 0L-6-100M22 0L6-100M-6-100H6M-14-40H14M-18-20H18M-10-70H10M-14-40L14-20M14-40L-14-20"/>'
                          '<path d="M-34-84H34M-26-104H26"/></g>')
    wires = ('<path d="M20 100Q200 130 330 104T640 112" stroke="#6b7a90" stroke-width="1.4" fill="none"/>'
             '<path d="M20 124Q200 152 330 126T640 134" stroke="#6b7a90" stroke-width="1.4" fill="none"/>')
    return svg('0 0 640 360', f'''
<rect width="640" height="360" fill="url(#gSky)"/>
<use href="#sun" x="500" y="20" width="110" height="110"/>
<path d="M0 196Q130 150 270 184T520 172T640 184V360H0Z" fill="#b6e0c4"/>
{pyl(120, 0.9)}{pyl(520, 0.62)}{wires}
<path d="M0 206Q160 190 320 204T640 198V360H0Z" fill="url(#gHill)"/>
{rows}''')


def termografia_az():
    panels = ''
    for r in range(3):
        for c in range(5):
            x, y = 70 + c * 106, 130 + r * 70
            panels += f'<rect x="{x}" y="{y}" width="96" height="60" rx="3" fill="url(#gPanel)" stroke="#dbe9fb" stroke-width="2"/>'
            panels += f'<path d="M{x+24} {y}V{y+60}M{x+48} {y}V{y+60}M{x+72} {y}V{y+60}M{x} {y+20}H{x+96}M{x} {y+40}H{x+96}" stroke="#8fc0f5" stroke-width=".9" opacity=".8"/>'
    hx, hy = 70 + 3 * 106 + 48, 130 + 70 + 30
    lines = ''.join(f'<path d="M0 {y}H640" stroke="#cbe5d3" stroke-width="2"/>' for y in range(30, 360, 44))
    return svg('0 0 640 360', f'''
<rect width="640" height="360" fill="#d9eedf"/>{lines}
{panels}
<circle cx="{hx}" cy="{hy}" r="62" fill="url(#gHot)" opacity=".92"/>
<polygon points="{hx},84 {hx-46},{hy-20} {hx+46},{hy-20}" fill="url(#gCone)"/>
<g stroke="#26344a" stroke-width="4" stroke-linecap="round"><path d="M{hx-16} 66L{hx-44} 52M{hx+16} 66L{hx+44} 52"/></g>
<ellipse cx="{hx-46}" cy="50" rx="22" ry="4.5" fill="#9fb3cc"/><ellipse cx="{hx+46}" cy="50" rx="22" ry="4.5" fill="#9fb3cc"/>
<ellipse cx="{hx}" cy="68" rx="24" ry="10" fill="#26344a"/><circle cx="{hx}" cy="80" r="6" fill="#ffd23f" stroke="#26344a" stroke-width="2"/>
<rect x="{hx+58}" y="{hy-36}" width="112" height="30" rx="15" fill="#fff" stroke="#b83227" stroke-width="2"/>
<text x="{hx+114}" y="{hy-16}" text-anchor="middle" font-size="14" font-weight="700" {FONT} fill="#b83227">Punto caldo</text>''')


def impianti_termici():
    wins = ''.join(f'<rect x="{58 + i * 52}" y="142" width="34" height="42" rx="3" fill="#cfe8fb" stroke="#9ec3e8" stroke-width="2"/>' for i in range(4))
    wins += ''.join(f'<rect x="{x}" y="200" width="34" height="42" rx="3" fill="#cfe8fb" stroke="#9ec3e8" stroke-width="2"/>' for x in (58, 214))
    smoke = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".9"/>' for x, y, r in [(553, 46, 14), (578, 28, 18), (608, 16, 14)])
    return svg('0 0 640 360', f'''
<rect width="640" height="360" fill="url(#gSky)"/>
<rect y="300" width="640" height="60" fill="#b9c7d8"/>
<polygon points="30,122 155,70 280,122" fill="#e7eef7" stroke="#c7d7ea" stroke-width="3"/>
<rect x="40" y="120" width="230" height="180" fill="#fff" stroke="#c7d7ea" stroke-width="3"/>{wins}
<rect x="128" y="232" width="52" height="68" rx="3" fill="#2f7fe3"/>
<path d="M270 262H338" stroke="#e0553a" stroke-width="9"/><path d="M270 284H338" stroke="#2f7fe3" stroke-width="9"/>
<rect x="330" y="170" width="280" height="130" fill="#dce6f2" stroke="#b5c6db" stroke-width="3"/>
<rect x="540" y="62" width="26" height="110" fill="#a9b8cc"/><rect x="540" y="96" width="26" height="14" fill="#e0553a"/>{smoke}
<ellipse cx="392" cy="204" rx="36" ry="10" fill="#eaf1f9"/><rect x="356" y="204" width="72" height="88" fill="#c3d1e3"/><ellipse cx="392" cy="292" rx="36" ry="10" fill="#c3d1e3"/>
<path d="M356 226H428M356 262H428" stroke="#a9b8cc" stroke-width="3"/>
<ellipse cx="478" cy="220" rx="30" ry="9" fill="#eaf1f9"/><rect x="448" y="220" width="60" height="72" fill="#c3d1e3"/><ellipse cx="478" cy="292" rx="30" ry="9" fill="#c3d1e3"/>
<circle cx="392" cy="246" r="15" fill="#fff" stroke="#7a8aa0" stroke-width="3"/><path d="M392 246L401 238" stroke="#e0553a" stroke-width="3" stroke-linecap="round"/>
<path d="M338 262H356M338 284H356" stroke="#7a8aa0" stroke-width="5"/>
<path d="M508 250H540V172" fill="none" stroke="#e0553a" stroke-width="6"/>
<circle cx="560" cy="246" r="24" fill="#ff7a2b"/><path d="M560 228C567 238 574 243 572 253C570 262 552 262 550 251C549 245 554 243 555 236C558 240 560 236 560 228Z" fill="#fff"/>''')


def lavaggio_az():
    roof = ''
    for i in range(6):
        x = 244 + i * 62
        roof += para(x, 98, 56, 36, 12)
        if i < 3:
            roof += f'<polygon points="{x+12},98 {x+68},98 {x+56},134 {x},134" fill="#9aa7b8" opacity=".55"/>'
    sparks = ''.join(f'<use href="#spark" x="{x-10}" y="{y-10}" width="{s}" height="{s}"/>' for x, y, s in [(470, 112, 20), (540, 120, 26), (596, 104, 18)])
    gates = ''.join(f'<rect x="{x}" y="226" width="90" height="74" fill="#9fb3cc"/><path d="M{x} 244H{x+90}M{x} 262H{x+90}M{x} 280H{x+90}" stroke="#8ea3be" stroke-width="2"/>' for x in (266, 386, 506))
    drops = ''.join(f'<use href="#drop" x="{x-7}" y="{y-8}" width="14" height="16"/>' for x, y in [(330, 116), (352, 128), (372, 104), (312, 134), (394, 120)])
    return svg('0 0 640 360', f'''
<rect width="640" height="360" fill="url(#gSky)"/>
<use href="#sun" x="20" y="14" width="80" height="80"/>
<rect y="300" width="640" height="60" fill="#b9c7d8"/>
<rect x="230" y="150" width="390" height="150" fill="#edf2f8" stroke="#c4d2e4" stroke-width="3"/>
<rect x="224" y="138" width="402" height="14" fill="#cfd9e7"/>{gates}{roof}{sparks}
<path d="M150 252L236 124L306 98" fill="none" stroke="#f0a93a" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="236" cy="124" r="7" fill="#26344a"/>
<g transform="translate(312,96) rotate(-24)"><rect x="-22" y="-7" width="44" height="14" rx="5" fill="#3a4a63"/></g>
<path d="M322 92Q350 70 392 100" fill="none" stroke="#4fb3f2" stroke-width="3" stroke-dasharray="2 8" stroke-linecap="round"/>
<path d="M322 98Q356 88 380 112" fill="none" stroke="#4fb3f2" stroke-width="3" stroke-dasharray="2 8" stroke-linecap="round"/>{drops}
<rect x="72" y="250" width="104" height="44" rx="20" fill="#2f7fe3" stroke="#14489a" stroke-width="3"/>
<rect x="32" y="258" width="44" height="36" rx="7" fill="#fff" stroke="#b5c6db" stroke-width="2"/><rect x="40" y="264" width="24" height="14" rx="2" fill="#cfe8fb"/>
<rect x="26" y="290" width="156" height="9" fill="#26344a"/>
<circle cx="60" cy="298" r="14" fill="#26344a"/><circle cx="60" cy="298" r="5" fill="#9fb3cc"/><circle cx="150" cy="298" r="14" fill="#26344a"/><circle cx="150" cy="298" r="5" fill="#9fb3cc"/>''')


# ---------------------------------------------------------------- STICKER (120x120)
def sticker_people():
    return '''<svg viewBox="0 0 120 120" aria-hidden="true" focusable="false"><defs><clipPath id="cpPeople"><circle cx="60" cy="60" r="54"/></clipPath></defs>
<circle cx="60" cy="60" r="57" fill="#dcefff" stroke="#fff" stroke-width="6"/>
<g clip-path="url(#cpPeople)">
<path d="M14 64L60 28l46 36v60H14z" fill="#fff" opacity=".7"/>
<path d="M18 120V96a16 16 0 0 1 32 0v24z" fill="#23a36a"/><circle cx="34" cy="76" r="9" fill="#e8b48a"/><path d="M25 74a9 9 0 0 1 18 0 9 7 0 0 0-18 0z" fill="#5a3a26"/>
<path d="M72 120V98a14 14 0 0 1 28 0v22z" fill="#ffc83d"/><circle cx="86" cy="80" r="8" fill="#f4d2b0"/><path d="M78 78a8 8 0 0 1 16 0z" fill="#2b2b2b"/>
<path d="M38 120V88a22 22 0 0 1 44 0v32z" fill="#1f6fd1"/><circle cx="60" cy="64" r="12" fill="#f1c7a0"/><path d="M48 62a12 12 0 0 1 24 0 12 8 0 0 0-24 0z" fill="#3a2a1c"/>
</g></svg>'''


def sticker_factory():
    return '''<svg viewBox="0 0 120 120" aria-hidden="true" focusable="false"><defs><clipPath id="cpFact"><circle cx="60" cy="60" r="54"/></clipPath></defs>
<circle cx="60" cy="60" r="57" fill="#d5f2e3" stroke="#fff" stroke-width="6"/>
<g clip-path="url(#cpFact)">
<circle cx="82" cy="22" r="9" fill="#fff" opacity=".9"/><circle cx="94" cy="12" r="11" fill="#fff" opacity=".8"/>
<rect x="76" y="28" width="11" height="40" fill="#5b6b82"/><rect x="76" y="36" width="11" height="6" fill="#e0553a"/>
<polygon points="18,102 18,62 40,78 40,62 62,78 62,62 84,78 84,62 102,70 102,102" fill="#fff" stroke="#b7cfc2" stroke-width="2"/>
<rect x="26" y="84" width="12" height="10" fill="#9ec3e8"/><rect x="46" y="84" width="12" height="10" fill="#9ec3e8"/><rect x="66" y="84" width="12" height="10" fill="#9ec3e8"/>
<rect x="84" y="84" width="12" height="18" fill="#2f7fe3"/><rect x="0" y="102" width="120" height="20" fill="#7fc79a"/>
</g></svg>'''


def sticker_palazzo():
    cols = ''.join(f'<rect x="{x}" y="60" width="8" height="30" fill="#fff" stroke="#d3bd86" stroke-width="1.5"/>' for x in (30, 46, 62, 78))
    return f'''<svg viewBox="0 0 120 120" aria-hidden="true" focusable="false"><defs><clipPath id="cpHall"><circle cx="60" cy="60" r="54"/></clipPath></defs>
<circle cx="60" cy="60" r="57" fill="#ffefc4" stroke="#fff" stroke-width="6"/>
<g clip-path="url(#cpHall)">
<path d="M60 30V10" stroke="#8a7a52" stroke-width="2"/><rect x="60" y="10" width="7" height="9" fill="#23a36a"/><rect x="67" y="10" width="7" height="9" fill="#fff" stroke="#e2d6b4" stroke-width=".6"/><rect x="74" y="10" width="7" height="9" fill="#d23a2e"/>
<polygon points="20,54 60,28 100,54" fill="#fff" stroke="#d3bd86" stroke-width="2"/><circle cx="60" cy="45" r="5" fill="#ffd86b"/>
<rect x="24" y="54" width="72" height="6" fill="#f3e6bd" stroke="#d3bd86" stroke-width="1.5"/>{cols}
<rect x="20" y="90" width="80" height="6" fill="#f3e6bd" stroke="#d3bd86" stroke-width="1.5"/><rect x="14" y="96" width="92" height="8" fill="#f3e6bd" stroke="#d3bd86" stroke-width="1.5"/>
</g></svg>'''


def pa_scene():
    """Municipio con impianto fotovoltaico sul tetto, scuola e bandiere (640x360)."""
    cols = ''.join(f'<rect x="{x}" y="196" width="12" height="82" fill="#fff" stroke="#c9d6e6" stroke-width="2"/>' for x in range(236, 420, 34))
    roof = ''.join(para(222 + i * 46, 138, 40, 22, 8) for i in range(5))
    win = ''.join(f'<rect x="{x}" y="{y}" width="14" height="22" rx="2" fill="#9ec3e8" stroke="#fff" stroke-width="2"/>' for x in (70, 102, 456, 488, 520) for y in (218, 250))
    return svg('0 0 640 360', f'''
<rect width="640" height="360" fill="url(#gSky)"/>
<use href="#sun" x="520" y="18" width="96" height="96"/>
<path d="M0 290Q160 262 320 282T640 274V360H0Z" fill="url(#gHill)"/>
<rect x="44" y="200" width="130" height="92" fill="#f4ead0" stroke="#d3bd86" stroke-width="2"/>
<rect x="446" y="200" width="150" height="92" fill="#f4ead0" stroke="#d3bd86" stroke-width="2"/>
{win}
<polygon points="200,196 320,120 440,196" fill="#fff" stroke="#c9d6e6" stroke-width="3"/>
{roof}
<circle cx="320" cy="176" r="9" fill="#ffd86b" stroke="#c9b06a" stroke-width="2"/>
<rect x="210" y="190" width="220" height="10" fill="#f1f5fb" stroke="#c9d6e6" stroke-width="2"/>
{cols}
<rect x="206" y="278" width="228" height="10" fill="#f1f5fb" stroke="#c9d6e6" stroke-width="2"/>
<rect x="196" y="288" width="248" height="12" fill="#e5ecf6" stroke="#c9d6e6" stroke-width="2"/>
<rect x="306" y="232" width="28" height="46" rx="3" fill="#2f7fe3" stroke="#fff" stroke-width="2"/>
<path d="M320 120V70" stroke="#6b7a90" stroke-width="3"/>
<rect x="320" y="70" width="18" height="8" fill="#23a36a"/><rect x="338" y="70" width="18" height="8" fill="#fff" stroke="#dbe3ee" stroke-width="1"/><rect x="356" y="70" width="18" height="8" fill="#d23a2e"/>
<g fill="#23a36a" opacity=".9"><circle cx="24" cy="282" r="16"/><circle cx="616" cy="278" r="18"/><circle cx="178" cy="286" r="12"/></g>''')


# ---------------------------------------------------------------- PUBBLICA AMMINISTRAZIONE (illustrazioni generiche, senza simboli comunali)
def _finestre(x0, y0, cols, rows, dx, dy, w=16, h=20):
    return ''.join(f'<rect x="{x0 + c * dx}" y="{y0 + r * dy}" width="{w}" height="{h}" rx="2" fill="#bcd8f2" stroke="#fff" stroke-width="2"/>'
                   for c in range(cols) for r in range(rows))


def _auto(x, y, col):
    return (f'<g transform="translate({x} {y})"><rect x="0" y="-14" width="44" height="14" rx="5" fill="{col}"/>'
            f'<path d="M9 -14L15 -24H31L37 -14Z" fill="{col}"/><path d="M16 -22H30L34 -15H12Z" fill="#dcebfa"/>'
            f'<circle cx="11" cy="0" r="6" fill="#26344a"/><circle cx="33" cy="0" r="6" fill="#26344a"/></g>')


def pa_edificio():
    pannelli = ''.join(f'<use href="#mod" x="{96 + i * 38}" y="62" width="34" height="20"/>' for i in range(5))
    return svg('0 0 400 250', f'''
<rect width="400" height="250" fill="url(#gSky)"/>
<use href="#sun" x="324" y="10" width="60" height="60"/>
<rect y="212" width="400" height="38" fill="#9fb3c8"/><rect y="220" width="400" height="3" fill="#fff" opacity=".5"/>
<rect x="70" y="86" width="224" height="126" fill="#f3f6fb" stroke="#b4c7de" stroke-width="2.4"/>
<rect x="62" y="80" width="240" height="10" fill="#dfe8f3" stroke="#b4c7de" stroke-width="2"/>
<path d="M90 82L108 66M222 82L240 66" stroke="#9fb1c7" stroke-width="3"/>
{pannelli}
{_finestre(88, 100, 5, 2, 40, 36)}
<rect x="165" y="164" width="34" height="48" rx="2" fill="#cfe3f8" stroke="#9fbbdb" stroke-width="2"/><path d="M182 164V212" stroke="#9fbbdb" stroke-width="2"/>
<g transform="translate(318 162)"><rect width="56" height="50" rx="5" fill="#e7eef7" stroke="#b4c7de" stroke-width="2.4"/><circle cx="28" cy="25" r="17" fill="#fff" stroke="#9fb1c7" stroke-width="2"/><path d="M28 12V38M15 25H41M19 16L37 34M37 16L19 34" stroke="#4fa0e6" stroke-width="3" stroke-linecap="round"/></g>
<path d="M294 190H318" stroke="#4fa0e6" stroke-width="3" stroke-dasharray="5 4"/>''')


def pa_fv():
    file = ''.join(f'<use href="#mod" x="{60 + i * 46}" y="{70 + r * 28}" width="42" height="25"/>' for r in range(3) for i in range(6))
    return svg('0 0 400 250', f'''
<rect width="400" height="250" fill="url(#gSky)"/>
<use href="#sun" x="326" y="8" width="58" height="58"/>
<rect y="214" width="400" height="36" fill="#8fcf9f"/>
<path d="M30 168Q36 96 70 66H330Q364 96 370 168Z" fill="#e6edf6" stroke="#b4c7de" stroke-width="2.4"/>
{file}
<rect x="30" y="168" width="340" height="46" fill="#f3f6fb" stroke="#b4c7de" stroke-width="2.4"/>
{''.join(f'<rect x="{52 + i * 56}" y="180" width="38" height="34" rx="2" fill="#bcd8f2" stroke="#fff" stroke-width="2"/>' for i in range(6))}
<rect x="190" y="186" width="20" height="28" fill="#cfe3f8" stroke="#9fbbdb" stroke-width="2"/>''')


def pa_pensilina():
    tetto = ''.join(f'<use href="#mod" x="{50 + i * 52}" y="62" width="48" height="26"/>' for i in range(6))
    tetto2 = ''.join(f'<use href="#mod" x="{58 + i * 52}" y="90" width="48" height="26"/>' for i in range(6))
    return svg('0 0 400 250', f'''
<rect width="400" height="250" fill="url(#gSky)"/>
<use href="#sun" x="20" y="10" width="58" height="58"/>
<rect y="190" width="400" height="60" fill="#9fb1c7"/>
<path d="M0 218H400M0 238H400" stroke="#fff" stroke-width="2" opacity=".45"/>
<path d="M62 190V226M110 190V226M170 190V226M230 190V226M290 190V226M338 190V226" stroke="#fff" stroke-width="3" opacity=".8"/>
<path d="M60 116V196M338 124V196" stroke="#6b7a90" stroke-width="7"/>
<polygon points="42,118 372,118 354,56 60,56" fill="#e3ebf5" stroke="#b4c7de" stroke-width="2"/>
{tetto}{tetto2}
{_auto(76, 214, '#e0553a')}{_auto(190, 214, '#5b7fa8')}
<g transform="translate(296 144)"><rect width="22" height="48" rx="5" fill="#fff" stroke="#9fb1c7" stroke-width="2.4"/><rect x="5" y="7" width="12" height="9" rx="2" fill="#23a36a"/><path d="M12 22L8 32H12L10 40L16 29H12Z" fill="#ffc83d"/><path d="M22 36Q34 36 34 48" fill="none" stroke="#26344a" stroke-width="3"/></g>''')


def pa_cer():
    def edificio(x, y, w, h, c):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#f3f6fb" stroke="#b4c7de" stroke-width="2.4"/>'
                f'<rect x="{x - 6}" y="{y - 8}" width="{w + 12}" height="10" fill="{c}" stroke="#b4c7de" stroke-width="1.6"/>'
                + _finestre(x + 10, y + 12, max(1, (w - 14) // 26), 2, 26, 30, 14, 18))
    return svg('0 0 400 250', f'''
<rect width="400" height="250" fill="url(#gSky)"/>
<use href="#sun" x="330" y="6" width="54" height="54"/>
<rect y="208" width="400" height="42" fill="#8fcf9f"/>
{edificio(24, 148, 78, 60, "#8aa4c4")}
{edificio(148, 130, 104, 78, "#dfe8f3")}
{edificio(300, 156, 70, 52, "#d98b6b")}
<use href="#mod" x="164" y="108" width="30" height="18"/><use href="#mod" x="198" y="108" width="30" height="18"/>
<use href="#mod" x="38" y="128" width="30" height="18"/><use href="#mod" x="312" y="136" width="30" height="18"/>
<g fill="none" stroke="#ffc83d" stroke-width="3" stroke-dasharray="7 6" stroke-linecap="round"><path d="M62 120Q110 66 190 76"/><path d="M200 76Q290 62 330 128"/><path d="M200 76V92"/></g>
<circle cx="200" cy="64" r="18" fill="#ffd23f" stroke="#fff" stroke-width="3"/><path d="M203 53l-9 14h7l-3 11 10-15h-7z" fill="#0d2d58"/>''')


def pa_hero():
    """Edificio pubblico generico con fotovoltaico in copertura e pensilina con ricarica (640x360)."""
    pannelli = ''.join(f'<use href="#mod" x="{96 + i * 52}" y="86" width="48" height="28"/>' for i in range(6))
    tetto = ''.join(f'<use href="#mod" x="{360 + i * 50}" y="132" width="46" height="26"/>' for i in range(4))
    return svg('0 0 640 360', f'''
<rect width="640" height="360" fill="url(#gSky)"/>
<use href="#sun" x="520" y="14" width="90" height="90"/>
<path d="M0 300Q170 276 340 294T640 286V360H0Z" fill="url(#gHill)"/>
<rect y="302" width="640" height="58" fill="#a9b9cb"/><path d="M0 330H640" stroke="#fff" stroke-width="3" opacity=".45"/>
<rect x="60" y="118" width="300" height="184" fill="#f3f6fb" stroke="#b4c7de" stroke-width="3"/>
<rect x="50" y="108" width="320" height="14" fill="#dfe8f3" stroke="#b4c7de" stroke-width="2.4"/>
<path d="M110 110L128 96M300 110L318 96" stroke="#9fb1c7" stroke-width="3"/>
{pannelli}
{_finestre(84, 140, 7, 3, 40, 42, 22, 26)}
<rect x="196" y="244" width="46" height="58" rx="2" fill="#cfe3f8" stroke="#9fbbdb" stroke-width="2.4"/><path d="M219 244V302" stroke="#9fbbdb" stroke-width="2"/>
<path d="M398 190V306M588 198V306" stroke="#6b7a90" stroke-width="8"/>
<polygon points="380,192 612,192 598,128 394,128" fill="#e3ebf5" stroke="#b4c7de" stroke-width="2.4"/>
{tetto}
{_auto(414, 322, '#e0553a')}{_auto(484, 322, '#5b7fa8')}
<g transform="translate(556 252)"><rect width="22" height="48" rx="5" fill="#fff" stroke="#9fb1c7" stroke-width="2.4"/><rect x="5" y="7" width="12" height="9" rx="2" fill="#23a36a"/><path d="M12 22L8 32H12L10 40L16 29H12Z" fill="#ffc83d"/></g>
<g fill="#23a36a" opacity=".9"><circle cx="30" cy="292" r="17"/><circle cx="626" cy="288" r="16"/></g>''')


ART = {
    'fv': fv_domestico(), 'acc': accumulo(), 'clima': termo_clima(), 'manut': manutenzione(),
    'lav': lavaggio(), 'termo': termografia(), 'solterm': solare_termico(), 'industriale': industriale(), 'om': om_fotovoltaico(), 'agri': agrivoltaico(), 'cer': cer(),
    'utility': utility_scale(), 'termo_az': termografia_az(), 'termici': impianti_termici(), 'lav_az': lavaggio_az(),
    'pa': pa_scene(), 'pa_hero': pa_hero(), 'pa_edificio': pa_edificio(), 'pa_fv': pa_fv(), 'pa_pensilina': pa_pensilina(), 'pa_cer': pa_cer(), 'st_people': sticker_people(), 'st_factory': sticker_factory(), 'st_hall': sticker_palazzo(),
}
