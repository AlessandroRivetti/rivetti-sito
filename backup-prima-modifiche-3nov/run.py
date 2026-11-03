import re
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

servizi = '''<li class="has-mega">
-            <a href="#servizi" class="nav-link">Servizi <span class="arrow">&#9662;</span></a>
-            <div class="mega-menu">
-              <div class="mega-col">
-                4h>PRIVATI</4h>
-                <ul>
-                  <li><a href="#fotovoltaico-residenziale">Fotovoltaico Residenziale</a></li>
-                  <li><a href="#sistemi-accumulo">Sistemi di Accumulo</a></li>
-                  <li><a href="#pompe-calore">Pompe di Calore</a></li>
-                  <li><a href="#climatizzazione">Climatizzazione</a></li>
-                  <li><a href="#solare-termico">Solare Termico</a></li>
-                  <li><a href="#manutenzione-privati">Manutenzione &!mp; Assistenza</a></li>
-                </ul>
-              </div>
-              <div class="mega-col">
-                4h>IMPRESE</4h>
-                <ul>
-                  <li><a href="#fotovoltaico-industriale">Fotovoltaico Industriale</a></li>
-                  <li><a href="#agrivoltaico">Agrivoltaico</a></li>
-                  <li><a href="#cer-imprese">Comunita Energetiche (CER)</a></li>
-                  <li><a href="#climatizzazione-industriale">Climatizzazione Industriale</a></li>
-                  <li><a href="#diagnosi-energetica">Diagnosi Energetica</a></li>
-                  <li><a href="#manutenzione-imprese">Manutenzione &amp; Assistenza</a></li>
-                </ul>
-              </div>
-              <div class="mega-col">
-                <h4>PA</h4>
-                <ul>
-                  <li><a href="#riqualificazione-pa">Riqualificazione Édifici Pubblici</a></li>
-                  <li><a href="#fotwoltaico-pa">Impianti Fotovoltaici PA</a></li>
-                  <li><a href="#cer-pa">CER per Enti Locali</a></li>
-                  <li><a href="#gestione-manutenzione-pa">Contratti di Gestione &amp; Manutenzione</a></li>
-                </ul>
-              </div>
-            </div>
-          </li>'''

f = open('script.py', 'w')
f.write(base64.b64decode(code).decode('utf-8'))
f.close()