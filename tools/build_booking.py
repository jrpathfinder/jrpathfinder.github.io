"""Build the Register and Payment pages (RU + EN) in the same style as the profile.

Fill in CONFIG below, then run:  python3 tools/build_booking.py
"""
import base64, json, os

from build_profiles import CSS, GLYPHS, SCRIPT, ROOT

# ---------------------------------------------------------------------------
# Your details. None shows a placeholder on the page.
CONFIG = {
    # Booking links from Calendly or Cal.com, one event type per format,
    # e.g. 'https://calendly.com/your-name/setup' or 'https://cal.com/your-name/online'
    'booking': {
        'install': 'https://calendly.com/jr-pathfinder/1hr',
        'online': 'https://calendly.com/jr-pathfinder/1hr',
    },
    # SBP QR code saved from your banking app ("QR для приёма переводов"),
    # as an image file in the project folder, e.g. 'sbp-qr.png'
    'sbp_qr': None,
    # Shown instead of the QR until it is added
    'sbp_phone': '+7 903 138-86-49',
}
# ---------------------------------------------------------------------------

FORMATS = {
    'install': {'amount': 3000, 'from': True},
    'online': {'amount': 5000, 'from': False},
}
SUB_AMOUNT = 2000

T = {
    'ru': dict(
        lang='ru', suffix='-ru', other=('', 'en', 'EN'),
        profile='index-ru.html',
        nav=['Профиль', 'Обучение ⟶»', 'Запись', 'Оплата'], nav_label='Разделы',
        theme='Сменить тему',
        register=dict(
            title='Запись — Рустем Глюмов', h1='Запись',
            mark='Формат → время → оплата',
            step_format='Формат', step_time='Время', step_pay='Оплата',
            formats={
                'install': ('Установка', 'Claude Code или Codex на вашем компьютере'),
                'online': ('Обучение онлайн', '2 часа · Zoom или Телемост'),
            },
            sub=('Подписка на месяц', 'Добавляется к любому формату'),
            time_note='Выберите удобный слот. Подтверждение придёт на почту.',
            no_calendar='Календарь появится здесь после подключения Calendly или Cal.com',
            pay_note='Оплата переводом по СБП после записи. Итого:',
            to_pay='К оплате ⟶»',
        ),
        payment=dict(
            title='Оплата — Рустем Глюмов', h1='Оплата', mark='СБП',
            qr_alt='QR-код для оплаты по СБП', by_phone='Перевод по номеру телефона в Райффайзенбанк',
        ),
    ),
    'en': dict(
        lang='en', suffix='', other=('-ru', 'ru', 'RU'),
        profile='index.html',
        nav=['Profile', 'Training (RU) ⟶»', 'Book', 'Payment'], nav_label='Sections',
        theme='Toggle theme',
        register=dict(
            title='Book — Rustem Gliumov', h1='Book a session',
            mark='Format → time → payment',
            step_format='Format', step_time='Time', step_pay='Payment',
            formats={
                'install': ('Setup', 'Claude Code or Codex on your computer'),
                'online': ('Online training', '2 hours · Zoom or Telemost'),
            },
            sub=('Monthly subscription', 'Add to any format'),
            time_note='Pick a slot that suits you. You will get a confirmation by email.',
            no_calendar='The calendar will appear here once Calendly or Cal.com is connected',
            pay_note='Payment by SBP transfer after booking. Total:',
            to_pay='Go to payment ⟶»',
        ),
        payment=dict(
            title='Payment — Rustem Gliumov', h1='Payment', mark='SBP',
            qr_alt='SBP payment QR code', by_phone='Transfer by phone number to Raiffeisenbank',
        ),
    ),
}

EXTRA_CSS = '''
    /* Numbered step heading: ① + highlighted tag */
    .step-head { display: flex; align-items: center; gap: 14px; }
    .step-head .n { font-size: 22px; letter-spacing: 0; }
    .down { width: 16px; height: 72px; margin: 28px 0 0 4px; border-left: 1.5px dashed var(--ink); position: relative; }
    .down::after { content: "▼"; position: absolute; left: -6px; bottom: -10px; font-size: 10px; letter-spacing: 0; }
    .section.flow { margin-top: 28px; }
    .section.first { margin-top: 80px; }

    /* Format choices: dashed cards that turn solid when picked */
    .choices {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-top: 28px;
    }
    .choice {
      position: relative;
      display: flex;
      flex-direction: column;
      gap: 10px;
      padding: 22px 22px 24px;
      border: 1.5px dashed var(--dash);
      cursor: pointer;
    }
    .choice input { position: absolute; opacity: 0; pointer-events: none; }
    .choice.on { border-style: solid; box-shadow: inset 0 0 0 1px var(--ink); }
    .choice:focus-within { outline: 2px solid var(--blue); outline-offset: 3px; }
    .choice .pick { font-size: 18px; letter-spacing: 0; }
    .choice h3 { margin: 0; font-size: 17px; font-weight: 400; text-transform: uppercase; }
    .choice .price {
      align-self: flex-start;
      padding: 3px 10px;
      background: var(--c);
      color: var(--on);
      font-size: 18px;
      font-weight: 500;
      letter-spacing: .08em;
      white-space: nowrap;
    }
    .choice .meta { color: var(--muted); font-size: 14px; letter-spacing: .06em; }
    .c-blue { --c: var(--blue); --on: #ffffff; }
    .c-claude { --c: var(--highlight); --on: #000000; }
    .c-orange { --c: var(--orange); --on: #000000; }

    .lead { margin: 22px 0 0; color: var(--muted); font-size: 15px; }
    .booking { margin-top: 20px; border: 1.5px dashed var(--dash); background: #ffffff; }
    .booking iframe { display: block; width: 100%; height: 720px; border: 0; }
    .booking .empty { padding: 72px 24px; color: var(--muted); font-size: 15px; text-align: center; }

    .total:empty { display: none; }
    .total { display: inline-block; margin: 14px 0 0; padding: 4px 12px; background: var(--highlight); color: #000000; font-size: 26px; font-weight: 500; letter-spacing: .08em; }
    .cta-link {
      display: inline-block;
      margin-top: 32px;
      font-size: 18px;
      text-transform: uppercase;
      text-decoration: underline;
      text-underline-offset: 6px;
    }
    .cta-link:hover { color: var(--blue); }

    /* SBP QR code */
    .qr {
      display: block;
      width: min(280px, 100%);
      aspect-ratio: 1;
      margin: 56px auto 0;
      padding: 16px;
      border: 1.5px dashed var(--dash);
      background: #ffffff;
    }
    .qr img { display: block; width: 100%; height: 100%; object-fit: contain; }

    /* Phone transfer, until the QR is added */
    .by-phone { margin-top: 56px; }
    .by-phone p { margin: 0; font-size: 18px; text-transform: uppercase; }
    .by-phone .phone { display: inline-block; margin-top: 18px; padding: 4px 12px; background: var(--highlight); color: #000000; font-size: 30px; font-weight: 500; letter-spacing: .08em; white-space: nowrap; }

    @media (max-width: 900px) {
      .section.first { margin-top: 56px; }
      .booking iframe { height: 640px; }
    }'''


def page(t, kind, title, body, script):
    other_suffix, other_lang, other_code = t['other']
    nav_cur = {'register': 2, 'payment': 3}[kind]
    links = [t['profile'], 'offer-ru.html', f'register{t["suffix"]}.html', f'payment{t["suffix"]}.html']
    nav = ''
    for i, (href, label) in enumerate(zip(links, t['nav'])):
        cls = ' class="current"' if i == nav_cur else (' class="cta"' if i == 1 else '')
        nav += f'    <a{cls} href="{href}">{label}</a>\n'
    nav += f'    <a class="lang" href="{kind}{other_suffix}.html" hreflang="{other_lang}" lang="{other_lang}">{other_code}</a>\n'
    return f'''<!doctype html>
<html lang="{t['lang']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;1,400&display=swap" rel="stylesheet">
  <style>
{CSS}
{EXTRA_CSS}
  </style>
</head>
<body>
  <nav class="side" aria-label="{t['nav_label']}">
{nav}  </nav>

{GLYPHS}

  <main id="top">
{body}
  </main>

  <button class="theme" type="button" aria-label="{t['theme']}">☀</button>

{SCRIPT}
  <script>
{script}
  </script>
</body>
</html>
'''


def head(n, label, id_):
    return f'''    <div class="step-head" id="{id_}">
      <span class="n" aria-hidden="true">{n}</span>
      <h2 class="tag">{label}</h2>
    </div>'''


def register(t):
    r = t['register']
    s = t['suffix']
    choices = ''
    for key, cls, price in [('install', 'c-blue', 'от 3 000 ₽' if t['lang'] == 'ru' else 'from 3,000 ₽'),
                            ('online', 'c-claude', '5 000 ₽' if t['lang'] == 'ru' else '5,000 ₽')]:
        name, meta = r['formats'][key]
        checked = ' checked' if key == 'online' else ''
        choices += f'''        <label class="choice {cls}">
          <input type="radio" name="format" value="{key}"{checked}>
          <span class="pick" aria-hidden="true">○</span>
          <h3>{name}</h3>
          <span class="price">{price}</span>
          <span class="meta">{meta}</span>
        </label>
'''
    sub_price = '+2 000 ₽' if t['lang'] == 'ru' else '+2,000 ₽'
    choices += f'''        <label class="choice c-orange">
          <input type="checkbox" name="sub" value="1">
          <span class="pick" aria-hidden="true">□</span>
          <h3>{r['sub'][0]}</h3>
          <span class="price">{sub_price}</span>
          <span class="meta">{r['sub'][1]}</span>
        </label>
'''
    body = f'''    <h1 aria-label="{r['h1']}"><span class="scramble" aria-hidden="true">{r['h1']}</span></h1>
    <p class="highlight"><span class="mark">{r['mark']}</span></p>

    <section class="section first">
{head('①', r['step_format'], 'format')}
      <div class="choices">
{choices}      </div>
      <div class="down" aria-hidden="true"></div>
    </section>

    <section class="section flow">
{head('②', r['step_time'], 'time')}
      <p class="lead">{r['time_note']}</p>
      <div class="booking" id="booking"><p class="empty">{r['no_calendar']}</p></div>
      <div class="down" aria-hidden="true"></div>
    </section>

    <section class="section flow">
{head('③', r['step_pay'], 'pay')}
      <p class="lead">{r['pay_note']}</p>
      <span class="total" id="total"></span><br>
      <a class="cta-link" id="to-pay" href="payment{s}.html">{r['to_pay']}</a>
    </section>'''
    script = f'''    (function () {{
      var BOOKING = {json.dumps(CONFIG['booking'])};
      var FORMATS = {json.dumps(FORMATS)}, SUB = {SUB_AMOUNT};
      var LOCALE = '{'ru-RU' if t['lang'] == 'ru' else 'en-US'}', FROM = '{'от ' if t['lang'] == 'ru' else 'from '}';
      var form = document.querySelectorAll('.choice input');
      var shown = null;
      function money(n) {{ return n.toLocaleString(LOCALE) + ' ₽'; }}
      function update() {{
        var f = document.querySelector('input[name=format]:checked').value;
        var sub = document.querySelector('input[name=sub]').checked;
        form.forEach(function (i) {{
          var c = i.closest('.choice');
          c.classList.toggle('on', i.checked);
          c.querySelector('.pick').textContent = i.type === 'radio' ? (i.checked ? '●' : '○') : (i.checked ? '■' : '□');
        }});
        var total = FORMATS[f].amount + (sub ? SUB : 0);
        document.getElementById('total').textContent = (FORMATS[f].from ? FROM : '') + money(total);
        document.getElementById('to-pay').href = 'payment{s}.html?f=' + f + (sub ? '&sub=1' : '');
        if (BOOKING[f] && shown !== f) {{
          shown = f;
          var url = BOOKING[f] + (BOOKING[f].indexOf('?') < 0 ? '?' : '&') + 'embed=true&hide_gdpr_banner=1';
          document.getElementById('booking').innerHTML = '<iframe title="{r['step_time']}" loading="lazy"></iframe>';
          document.querySelector('#booking iframe').src = url;
        }}
      }}
      form.forEach(function (i) {{ i.addEventListener('change', update); }});
      update();
    }})();'''
    return page(t, 'register', r['title'], body, script)


def payment(t):
    p = t['payment']
    qr = CONFIG['sbp_qr']
    if qr:
        ext = os.path.splitext(qr)[1].lstrip('.').lower().replace('jpg', 'jpeg')
        data = base64.b64encode(open(os.path.join(ROOT, qr), 'rb').read()).decode()
        alt = p['qr_alt']
        pay = f'<div class="qr"><img src="data:image/{ext};base64,{data}" alt="{alt}"></div>'
    else:
        phone = CONFIG['sbp_phone']
        pay = (f'<div class="by-phone"><p>{p["by_phone"]}</p>'
               f'<span class="phone">{phone}</span></div>')
    body = f'''    <h1 aria-label="{p['h1']}"><span class="scramble" aria-hidden="true">{p['h1']}</span></h1>
    <p class="highlight"><span class="mark">{p['mark']}</span></p>

    {pay}'''
    return page(t, 'payment', p['title'], body, '')


def main(root=ROOT):
    for t in T.values():
        for kind, build in [('register', register), ('payment', payment)]:
            name = f'{kind}{t["suffix"]}.html'
            open(os.path.join(root, name), 'w').write(build(t))
            print('wrote', name)


if __name__ == '__main__':
    main()
