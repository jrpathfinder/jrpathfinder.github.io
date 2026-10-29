"""Rebuild index.html (EN) and index-ru.html (RU) in the offer-ru.html style.

Run from anywhere:  python3 tools/build_profiles.py
CSS, GLYPHS and SCRIPT are shared with build_booking.py.
"""
import base64, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

T = {
  'en': dict(
    file='index.html', lang='en',
    title='Rustem Gliumov',
    desc='Rustem Gliumov, Senior Software Engineer. 20 years in software: banking, fintech, e-commerce and AI platforms.',
    nav_label='Sections', nav=['Profile', 'About', 'Experience'],
    offer='Training (RU) ⟶»', book=('register.html', 'Book'),
    other_lang=('index-ru.html', 'ru', 'RU'),
    first='Rustem', last='Gliumov',
    about_label='About',
    about='20 years building enterprise systems for banking, fintech and e-commerce. Lately I build AI platforms on LLMs, RAG and semantic search.',
    exp_label='Experience',
    exp_note='20 years in software, from Java services to AI platforms.',
    exp=[
      ('2026 — now', 'AI Platform Architect &amp; Founder', 'RAG, semantic search, LLM integration'),
      ('2023 — 2026', 'Lead Software Engineer', 'Bank DOM.RF · 10M+ transactions a day, 99.99% uptime'),
      ('2022 — 2023', 'Senior Java Developer / Tech Lead', 'EPAM · B2B e-commerce for TVH, Belgium'),
      ('2018 — 2022', 'Senior Java Developer', 'Sber, Innotech · brokerage and credit services'),
      ('2006 — 2018', 'Java Developer', 'PSB, Accenture, Tatneft IT, Exigen and more'),
    ],
    contacts='Contacts', theme='Toggle theme',
  ),
  'ru': dict(
    file='index-ru.html', lang='ru',
    title='Рустем Глюмов',
    desc='Рустем Глюмов, Senior Software Engineer. 20 лет в разработке: банки, финтех, e-commerce и AI-платформы.',
    nav_label='Разделы', nav=['Профиль', 'Обо мне', 'Опыт'],
    offer='Обучение ⟶»', book=('register-ru.html', 'Запись'),
    other_lang=('index.html', 'en', 'EN'),
    first='Рустем', last='Глюмов',
    about_label='Обо мне',
    about='20 лет разрабатываю корпоративные системы для банков, финтеха и e-commerce. Последние годы строю AI-платформы на LLM, RAG и семантическом поиске.',
    exp_label='Опыт',
    exp_note='20 лет в разработке — от Java-сервисов до AI-платформ.',
    exp=[
      ('2026 — сейчас', 'AI Platform Architect &amp; Founder', 'RAG, семантический поиск, интеграция LLM'),
      ('2023 — 2026', 'Lead Software Engineer', 'Банк ДОМ.РФ · 10M+ транзакций в день, 99,99% доступности'),
      ('2022 — 2023', 'Senior Java Developer / Tech Lead', 'EPAM · B2B e-commerce для TVH, Бельгия'),
      ('2018 — 2022', 'Senior Java Developer', 'Сбер, Иннотех · брокерские и кредитные сервисы'),
      ('2006 — 2018', 'Java Developer', 'ПСБ, Accenture, Татнефть, Exigen и др.'),
    ],
    contacts='Контакты', theme='Сменить тему',
  ),
}

CSS = '''    :root {
      --bg: #ffffff;
      --ink: #000000;
      --muted: #6b6b6b;
      --highlight: #cc7c5e;
      --blue: #2f62d0;
      --orange: #ff5a36;
      --yellow: #cc7c5e;
      --dash: #000000;
    }
    @media (prefers-color-scheme: dark) {
      :root:not([data-theme="light"]) {
        --bg: #000000;
        --ink: #ffffff;
        --muted: #a3a3a3;
        --blue: #7aa2ff;
        --dash: #ffffff;
      }
    }
    :root[data-theme="dark"] {
      --bg: #000000;
      --ink: #ffffff;
      --muted: #a3a3a3;
      --blue: #7aa2ff;
      --dash: #ffffff;
    }

    * { box-sizing: border-box; }
    html, body { margin: 0; }
    body {
      background: var(--bg);
      color: var(--ink);
      font-family: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, monospace;
      letter-spacing: .14em;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
      min-height: 100vh;
      overflow-x: hidden;
    }
    a { color: inherit; }

    /* Left navigation */
    .side {
      position: fixed;
      top: 24px;
      left: 20px;
      z-index: 2;
      display: flex;
      flex-direction: column;
      gap: 18px;
      font-size: 15px;
      text-transform: uppercase;
    }
    .side a { text-decoration: none; }
    .side a:hover { text-decoration: underline; text-underline-offset: 5px; }
    .side .current { color: var(--blue); }
    .side .current::before {
      content: "";
      display: inline-block;
      width: 10px;
      height: 10px;
      margin-right: 14px;
      border-radius: 50%;
      background: var(--blue);
      vertical-align: 1px;
    }
    .side .cta, .side .lang { text-decoration: underline; text-underline-offset: 5px; }

    /* Floating math symbols */
    .glyphs { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
    .glyphs span {
      position: absolute;
      font-size: 18px;
      letter-spacing: 0;
      animation: drift 9s ease-in-out infinite alternate;
    }
    .glyphs .p { color: var(--blue); }
    .glyphs .o { color: var(--orange); }
    .glyphs .y { color: var(--yellow); }
    @keyframes drift {
      from { transform: translate(0, 0); }
      to { transform: translate(6px, -10px); }
    }
    @media (prefers-reduced-motion: reduce) {
      .glyphs span { animation: none; }
    }

    main {
      position: relative;
      z-index: 1;
      max-width: 1400px;
      margin: 0 auto;
      padding: 96px 60px 120px 340px;
      text-align: center;
    }

    /* Hero */
    .photo {
      display: block;
      width: 96px;
      height: 96px;
      margin: 0 auto 36px;
      border: 1px dashed var(--dash);
      background: #ffffff;
    }
    h1 {
      margin: 0;
      font-weight: 400;
      font-size: clamp(26px, 4.4vw, 56px);
      letter-spacing: .22em;
      line-height: 1.15;
      text-transform: uppercase;
    }
    .mark {
      display: inline;
      padding: 4px 10px;
      background: var(--highlight);
      color: #000000;
      font-size: clamp(14px, 1.8vw, 19px);
      line-height: 2;
      text-transform: uppercase;
      -webkit-box-decoration-break: clone;
      box-decoration-break: clone;
    }
    .highlight { margin: 48px 0 0; }
    /* Section heading: highlighted tag + gray note, like "Prizes" on yandex.com/cup/ml */
    .section { max-width: 820px; margin: 120px auto 0; text-align: left; }
    .tag {
      display: inline-block;
      margin: 0;
      padding: 4px 10px;
      background: var(--highlight);
      color: #000000;
      font-size: 18px;
      font-weight: 400;
      text-transform: uppercase;
    }
    .note { margin: 18px 0 0 30%; color: var(--muted); font-size: 16px; }
    .about {
      margin: 40px 0 0;
      font-size: clamp(16px, 1.9vw, 22px);
      line-height: 1.6;
      text-transform: uppercase;
    }

    /* Experience: zigzag steps joined by dashed arrows */
    .scheme { --shift: 45%; --r: 10px; margin-top: 56px; }
    .step { width: calc(100% - var(--shift)); }
    .step.right { margin-left: var(--shift); }
    .step .num { display: block; font-size: 18px; letter-spacing: 0; }
    .step .years {
      display: inline-block;
      margin-top: 10px;
      font-size: 20px;
      font-style: italic;
      letter-spacing: .08em;
      text-decoration: underline;
      text-underline-offset: 6px;
    }
    .step .role { margin: 14px 0 0 1.4em; font-size: 17px; text-transform: uppercase; }
    .step .what { margin: 6px 0 0 1.4em; color: var(--muted); font-size: 14px; letter-spacing: .06em; }
    .link { position: relative; width: var(--shift); height: 84px; margin: 24px 0 18px 8px; }
    .link::before, .link::after { content: ""; position: absolute; border: 0 dashed var(--ink); }
    .link::before {
      left: 0;
      top: 0;
      width: calc(100% - var(--r));
      height: 50%;
      border-left-width: 1.5px;
      border-bottom-width: 1.5px;
      border-bottom-left-radius: var(--r);
    }
    .link::after {
      right: 0;
      top: calc(50% - 1.5px);
      width: var(--r);
      height: 50%;
      border-top-width: 1.5px;
      border-right-width: 1.5px;
      border-top-right-radius: var(--r);
    }
    .link .head { position: absolute; right: -4.5px; bottom: -9px; font-size: 10px; letter-spacing: 0; line-height: 1; }
    .link.rev { transform: scaleX(-1); }

    .links {
      display: flex;
      justify-content: flex-start;
      margin-top: 32px;
      flex-wrap: wrap;
      gap: 12px 36px;
      font-size: 16px;
      text-transform: uppercase;
    }
    .links a { text-underline-offset: 6px; }
    .links a:hover { color: var(--blue); }

    /* Theme toggle, bottom-left dashed square */
    .theme {
      position: fixed;
      left: 2px;
      bottom: 2px;
      z-index: 2;
      width: 64px;
      height: 64px;
      border: 1px dashed var(--dash);
      background: var(--bg);
      color: var(--ink);
      font: inherit;
      font-size: 26px;
      letter-spacing: 0;
      cursor: pointer;
    }

    @media (max-width: 900px) {
      .side {
        position: static;
        flex-direction: row;
        flex-wrap: wrap;
        gap: 12px 20px;
        padding: 20px 16px 0;
        font-size: 13px;
      }
      main { padding: 56px 16px 120px; }
      h1 { font-size: clamp(24px, 8vw, 40px); letter-spacing: .16em; }
      .section { margin-top: 80px; }
      .note { margin-left: 0; }
      .scheme { --shift: 22%; }
      .link { height: 60px; }
      .theme { width: 48px; height: 48px; font-size: 20px; }
    }'''

GLYPHS = '''  <div class="glyphs" aria-hidden="true">
    <span class="p" style="top:4%;left:68%">ℕ</span>
    <span class="y" style="top:12%;left:15%">ℕ</span>
    <span class="o" style="top:26%;left:52%">∀</span>
    <span class="o" style="top:42%;left:44%">¬</span>
    <span class="y" style="top:22%;left:90%">¬</span>
    <span class="o" style="top:47%;left:76%">∞</span>
    <span class="p" style="top:49%;left:88%">∅</span>
    <span class="p" style="top:68%;left:29%">∞</span>
    <span class="y" style="top:69%;left:41%">∅</span>
    <span class="o" style="top:67%;left:58%">∩</span>
    <span class="y" style="top:87%;left:10%">∩</span>
    <span class="p" style="top:83%;left:34%">≢</span>
    <span class="o" style="top:84%;left:84%">√</span>
    <span class="y" style="top:95%;left:15%">ℕ</span>
  </div>'''

SCRIPT = '''  <script>
    (function () {
      var root = document.documentElement;
      var btn = document.querySelector('.theme');
      function isDark() {
        var t = root.getAttribute('data-theme');
        if (t) return t === 'dark';
        return window.matchMedia('(prefers-color-scheme: dark)').matches;
      }
      function sync() { btn.textContent = isDark() ? '☾' : '☀'; }
      try {
        var saved = localStorage.getItem('theme');
        if (saved) root.setAttribute('data-theme', saved);
      } catch (e) {}
      sync();
      btn.addEventListener('click', function () {
        var next = isDark() ? 'light' : 'dark';
        root.setAttribute('data-theme', next);
        try { localStorage.setItem('theme', next); } catch (e) {}
        sync();
      });
    })();

    // Name decode, like yandex.ru/cup/ml: letters flicker through symbols, then settle one by one
    (function () {
      var el = document.querySelector('.scramble');
      if (!el || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      var target = el.textContent;
      var noise = '!#_/Y<>*░▒▓█';
      var start = performance.now();
      var settle = Array.prototype.map.call(target, function (ch) {
        return /\\s/.test(ch) ? 0 : 250 + Math.random() * 1150;
      });
      function frame(now) {
        var t = now - start, out = '', done = true;
        for (var i = 0; i < target.length; i++) {
          if (t >= settle[i]) out += target[i];
          else { out += noise[Math.floor(Math.random() * noise.length)]; done = false; }
        }
        el.textContent = out;
        if (!done) setTimeout(function () { requestAnimationFrame(frame); }, 50);
      }
      requestAnimationFrame(frame);
    })();
  </script>'''

def main(root=ROOT):
    # Dithered portrait (192px for sharp 2x screens), embedded so each page stays a single file
    photo = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(root, 'rustem-photo.png'), 'rb').read()).decode()
    for t in T.values():
        href, hl, code = t['other_lang']
        steps = ''
        for i, (years, role, what) in enumerate(t['exp']):
            if i:
                rev = ' rev' if i % 2 == 0 else ''
                steps += f'      <div class="link{rev}" aria-hidden="true"><span class="head">▼</span></div>\n'
            right = ' right' if i % 2 else ''
            steps += f'''      <div class="step{right}">
            <span class="num" aria-hidden="true">{chr(0x2460 + i)}</span>
            <span class="years">{years}</span>
            <p class="role">{role}</p>
            <p class="what">{what}</p>
          </div>
    '''
        html = f'''<!doctype html>
    <html lang="{t['lang']}">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>{t['title']}</title>
      <meta name="description" content="{t['desc']}">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <!-- JetBrains Mono ≈ the spaced monospace of yandex.ru/cup, same as offer-ru.html -->
      <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;1,400&display=swap" rel="stylesheet">
      <style>
    {CSS}
      </style>
    </head>
    <body>
      <nav class="side" aria-label="{t['nav_label']}">
        <a class="current" href="#top">{t['nav'][0]}</a>
        <a href="#about">{t['nav'][1]}</a>
        <a href="#experience">{t['nav'][2]}</a>
        <a href="{t['book'][0]}">{t['book'][1]}</a>
    <a class="cta" href="offer-ru.html">{t['offer']}</a>
        <a class="lang" href="{href}" hreflang="{hl}" lang="{hl}">{code}</a>
      </nav>

    {GLYPHS}

      <main id="top">
        <img class="photo" src="{photo}" alt="{t['first']} {t['last']}" width="96" height="96">
        <h1 aria-label="{t['first']} {t['last']}"><span class="scramble" aria-hidden="true">{t['first']} {t['last']}</span></h1>

        <p class="highlight"><span class="mark">Senior Software Engineer</span></p>

        <section class="section" id="about">
          <h2 class="tag">{t['about_label']}</h2>
          <p class="about">{t['about']}</p>
        </section>

        <section class="section" id="experience">
          <h2 class="tag">{t['exp_label']}</h2>
          <p class="note">{t['exp_note']}</p>
          <div class="scheme">
    {steps}      </div>
        </section>

        <section class="section">
          <h2 class="tag">{t['contacts']}</h2>
          <nav class="links" aria-label="{t['contacts']}">
            <a href="https://www.linkedin.com/in/rgliumov/">LinkedIn</a>
            <a href="https://github.com/jrpathfinder">GitHub</a>
          </nav>
        </section>
      </main>

      <button class="theme" type="button" aria-label="{t['theme']}">☀</button>

    {SCRIPT}
    </body>
    </html>
    '''
        open(os.path.join(root, t['file']), 'w').write(html)
        print('wrote', t['file'])


if __name__ == '__main__':
    main()
