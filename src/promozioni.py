import dati as D
from comp import head, nav, footer, esc, qa

def build():
    p = {
        'key': 'promozioni',
        'path': 'promozioni.html',
        'title': 'Promozioni e Offerte Speciali | Rivetti Impianti',
        'desc': 'Scopri tutte le offerte attive per fotovoltaico, accumulo, climatizzazione, caldaie e manutenzione impianti a Rivetti Impianti.'
    }
    
    pre = ''
    
    # Generazione delle card delle promozioni
    cards_html = ""
    for promo in D.PROMOZIONI:
        cards_html += f'''
        <div class="promo-card" style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 30px; display: flex; flex-direction: column; justify-content: space-between; transition: transform 0.2s;">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <span style="font-size: 2rem;">{promo['icona']}</span>
                    <span style="background: rgba(34, 197, 94, 0.15); color: #22c55e; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">{promo['badge']}</span>
                </div>
                <h3 style="color: #fff; font-size: 1.25rem; margin-bottom: 12px;">{promo['titolo']}</h3>
                <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6; margin-bottom: 20px;">{promo['descrizione']}</p>
            </div>
            <div>
                <div style="font-size: 1.2rem; font-weight: 700; color: #38bdf8; margin-bottom: 8px;">{promo['prezzo']}</div>
                <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 20px;">*{promo['note']}</div>
                <a href="contatti.html" style="display: block; text-align: center; background: #22c55e; color: #fff; padding: 10px 20px; border-radius: 6px; font-weight: 600; text-decoration: none; transition: background 0.2s;">Aderisci all'Offerta</a>
            </div>
        </div>
        '''

    content = f'''
    {head(p, pre)}
    <body>
        {nav(p, pre)}
        <main style="max-width: 1200px; margin: 40px auto; padding: 0 20px;">
            <div style="text-align: center; margin-bottom: 50px;">
                <h1 style="color: #22c55e; font-size: 2.5rem; margin-bottom: 15px; font-weight: 800;">Promozioni &amp; Offerte Speciali</h1>
                <p style="color: #cbd5e1; font-size: 1.1rem; max-width: 700px; margin: 0 auto;">Approfitta delle soluzioni tecnologiche certificate di Rivetti Impianti a condizioni vantaggiose per la tua casa o la tua impresa.</p>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 25px;">
                {cards_html}
            </div>
        </main>
        {footer(p, pre)}
    </body>
    </html>
    '''
    
    with open('promozioni.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Promozioni.html generato con successo.")