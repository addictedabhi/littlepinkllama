# -*- coding: utf-8 -*-
"""One-time generator: builds the static Little Pink Llama site from scraped Shopify data.

Reads scraped JSON (products.json, coll_*.json, img_map.json) from the scratch dir
given as argv[1]; writes HTML into the repo root. Safe to re-run.
"""
import json, os, re, sys, html

SCRATCH = sys.argv[1]
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WA = "919460074404"
IG = "https://www.instagram.com/little_pink_llama_/"
FB = "https://www.facebook.com/littlepinkllama"

prods = {p['handle']: p for p in json.load(open(os.path.join(SCRATCH, 'products.json'), encoding='utf-8'))['products']}
imgmap = json.load(open(os.path.join(SCRATCH, 'img_map.json'), encoding='utf-8'))
colls = {}
for c in ['brooches', 'hairclips', 'crochet-toys', 'collar', 'rakhis', 'featured-products']:
    colls[c] = [p['handle'] for p in json.load(open(os.path.join(SCRATCH, f'coll_{c}.json'), encoding='utf-8'))['products']]

SVG_WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.5 14.4l-2.1-1c-.3-.1-.5-.1-.7.1l-1 1.2c-.2.2-.4.2-.6.1-.8-.4-2.5-1.5-3.5-3.4-.1-.2-.1-.4.1-.6l.9-1.1c.2-.2.2-.5.1-.7l-1-2.2c-.2-.5-.7-.6-1.1-.4-1 .6-1.8 1.5-1.8 2.6 0 .5.1 1.1.4 1.7 1 2.2 2.8 4 5 5.1.9.4 1.6.7 2.2.7 1.2 0 2.3-.7 2.8-1.8.2-.5 0-1-.7-1.3zM12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3 .8.8-3-.2-.3A8.2 8.2 0 1 1 12 20.2z"/></svg>'
SVG_IG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 1.8c-3.1 0-3.5 0-4.8.1-1.1.1-1.5.2-1.8.3-.5.2-.8.4-1.1.7-.3.3-.5.6-.7 1.1-.1.3-.3.7-.3 1.8-.1 1.3-.1 1.7-.1 4.8s0 3.5.1 4.8c.1 1.1.2 1.5.3 1.8.2.5.4.8.7 1.1.3.3.6.5 1.1.7.3.1.7.3 1.8.3 1.3.1 1.7.1 4.8.1s3.5 0 4.8-.1c1.1-.1 1.5-.2 1.8-.3.5-.2.8-.4 1.1-.7.3-.3.5-.6.7-1.1.1-.3.3-.7.3-1.8.1-1.3.1-1.7.1-4.8s0-3.5-.1-4.8c-.1-1.1-.2-1.5-.3-1.8-.2-.5-.4-.8-.7-1.1-.3-.3-.6-.5-1.1-.7-.3-.1-.7-.3-1.8-.3-1.3-.1-1.7-.1-4.8-.1zm0 3.1a4.9 4.9 0 1 1 0 9.8 4.9 4.9 0 0 1 0-9.8zm0 8.1a3.2 3.2 0 1 0 0-6.4 3.2 3.2 0 0 0 0 6.4zm6.2-8.3a1.1 1.1 0 1 1-2.3 0 1.1 1.1 0 0 1 2.3 0z"/></svg>'
SVG_FB = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.4v7A10 10 0 0 0 22 12z"/></svg>'
SVG_MENU = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18v2H3zm0 5h18v2H3zm0 5h18v2H3z"/></svg>'


def rs(v):
    n = float(v)
    s = '{:,.0f}'.format(n) if n == int(n) else '{:,.2f}'.format(n)
    return 'Rs. ' + s


def wa_link(text):
    from urllib.parse import quote
    return 'https://wa.me/%s?text=%s' % (WA, quote(text))


def head(title, root):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="icon" type="image/png" href="{root}assets/images/site/favicon.png">
<link rel="stylesheet" href="{root}assets/css/style.css?v=3">
</head>
<body>
'''


def header(root, active=''):
    def cls(k):
        return ' class="active"' if k == active else ''
    marquee_item = '<p class="announcement-text">FREE SHIPPING ACROSS INDIA</p><span class="announcement-sep" aria-hidden="true">\U0001F69A</span>' * 6
    return f'''<div class="announcement" aria-label="FREE SHIPPING ACROSS INDIA"><div class="announcement-track">{marquee_item}</div></div>
<header class="site-header">
  <div class="header-inner">
    <a class="logo" href="{root}index.html"><img src="{root}assets/images/site/logo.png" alt="Little Pink Llama"></a>
    <button class="menu-toggle" aria-label="Menu">{SVG_MENU}</button>
    <nav class="nav">
      <a href="{root}index.html"{cls('home')}>Home</a>
      <div class="dropdown">
        <a href="{root}collections/all.html"{cls('shop')}>Shop all</a>
        <div class="dropdown-menu">
          <a href="{root}collections/brooches.html">Brooches</a>
          <a href="{root}collections/hairclips.html">Hairclips</a>
          <a href="{root}collections/crochet-toys.html">Crochet Toys</a>
          <a href="{root}collections/collar.html">Collar</a>
          <a href="{root}collections/rakhis.html">Rakhis</a>
        </div>
      </div>
      <a href="{root}pages/about-us.html"{cls('about')}>About us</a>
      <a href="{root}pages/contact.html"{cls('contact')}>Contact</a>
      <a href="{root}blogs/index.html"{cls('blogs')}>Blogs</a>
    </nav>
    <div class="header-icons">
      <a href="{wa_link('Hi! I would like to know more about Little Pink Llama products.')}" target="_blank" rel="noopener" aria-label="WhatsApp"><span class="icon-wa">{SVG_WA}</span></a>
      <a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram"><span class="icon-ig">{SVG_IG}</span></a>
    </div>
  </div>
</header>
'''


def footer(root):
    return f'''<footer class="site-footer">
  <div class="page-width">
    <div class="footer-grid">
      <div>
        <h4>Little Pink Llama</h4>
        <p>Handcrafted accessories for little dreamers — elegant, comfortable &amp; made with love.</p>
        <ul>
          <li>Phone Number - +91 99998 25527</li>
          <li>Email - lplkidscouture@gmail.com</li>
        </ul>
        <div class="footer-social">
          <a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook">{SVG_FB}</a>
          <a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{SVG_IG}</a>
        </div>
      </div>
      <div>
        <h4>Quick links</h4>
        <ul>
          <li><a href="{root}index.html">Home</a></li>
          <li><a href="{root}pages/about-us.html">About us</a></li>
          <li><a href="{root}pages/contact.html">Contact</a></li>
          <li><a href="{root}pages/faq.html">FAQ</a></li>
        </ul>
      </div>
      <div>
        <h4>Shop</h4>
        <ul>
          <li><a href="{root}collections/all.html">All products</a></li>
          <li><a href="{root}collections/featured-products.html">Featured Products</a></li>
          <li><a href="{root}pages/sitemap.html">Collections</a></li>
          <li><a href="{root}blogs/index.html">Blogs</a></li>
        </ul>
      </div>
      <div>
        <h4>Information</h4>
        <ul>
          <li><a href="{root}pages/shipping-policy.html">Shipping Policy</a></li>
          <li><a href="{root}pages/return-policy.html">Return Policy</a></li>
          <li><a href="{root}pages/terms-of-service.html">Terms of Service</a></li>
          <li><a href="{root}pages/privacy-policy.html">Privacy Policy</a></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="footer-bottom">Copyright © 2025 Little Pink Llama · <a href="{root}pages/sitemap.html">Sitemap</a></div>
</footer>
<a class="float-wa" href="{wa_link('Hi! I would like to order from Little Pink Llama.')}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{SVG_WA}</a>
<script src="{root}assets/js/site.js"></script>
</body>
</html>
'''


def card(h, root):
    p = prods[h]
    img = imgmap.get(h, [])
    src = f'{root}assets/images/products/{img[0]}' if img else f'{root}assets/images/site/logo.png'
    price = rs(p['variants'][0]['price'])
    wa = wa_link(f"Hi! I'd like to order the {p['title']} ({price}). Is it available?")
    return f'''<div class="product-card">
  <a href="{root}products/{h}.html"><img src="{src}" alt="{html.escape(p['title'])}" loading="lazy"></a>
  <div class="card-info">
    <h3><a href="{root}products/{h}.html">{html.escape(p['title'])}</a></h3>
    <span class="price">{price}</span>
    <div class="card-ctas">
      <a class="wa" href="{wa}" target="_blank" rel="noopener">{SVG_WA} WhatsApp</a>
      <a class="ig" href="{IG}" target="_blank" rel="noopener">{SVG_IG} DM us</a>
    </div>
  </div>
</div>'''


def write(path, content):
    full = os.path.join(SITE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(content)
    print('wrote', path)


def build_home():
    root = ''
    slides = [
        ('assets/images/site/website_banner_seamless.jpg', 'Brooches for every giggle', 'Twirl And Cuddle', 'collections/brooches.html'),
        ('assets/images/site/website_banner_seamless_2.jpg', 'Adorable Clips for Your Little Star', 'Handmade hair accessories your little one will love', 'collections/hairclips.html'),
        ('assets/images/site/website_banner_seamless_d6756001-9fcc-45d6-af46-e2035690ad43.jpg', 'Crochet Magic for Tiny Hearts', 'Soft, safe and lovingly handcrafted toys', 'collections/crochet-toys.html'),
    ]
    hero = '<section class="hero">\n'
    for i, (img, h1, sub, link) in enumerate(slides):
        hero += f'''<div class="slide{' active' if i == 0 else ''}">
  <img src="{img}" alt="{html.escape(h1)}">
  <div class="slide-content">
    <h2>{h1}</h2>
    <p>{sub}</p>
    <a class="btn btn-pink" href="{link}">Shop Now</a>
  </div>
</div>\n'''
    hero += '<div class="hero-dots"></div>\n</section>\n'

    cards = [
        (imgmap['llama-brooch'][0], 'Brooches', 'collections/brooches.html'),
        (imgmap['monsoon-muse-hair-clip'][0], 'Hairclips', 'collections/hairclips.html'),
        (imgmap['big-bear'][0], 'Crochet toys', 'collections/crochet-toys.html'),
        (imgmap['ruby-sparkle'][0], 'Collar', 'collections/collar.html'),
    ]
    shop_coll = '<section class="section"><div class="page-width"><h2 class="section-title">Shop by Collection</h2><div class="collections-grid">'
    for img, name, link in cards:
        shop_coll += f'<a class="collection-card" href="{link}"><img src="assets/images/products/{img}" alt="{name}" loading="lazy"><span>{name}</span></a>'
    shop_coll += '</div></div></section>\n'

    latest_handles = ['monsoon-muse-rakhi', 'cloud-rakhi', 'bird-rakhi', 'elephant-with-balloons-rakhi',
                      'candy-cane-hair-clip', 'llama-hair-clip', 'happy-wheels-brooch', 'guiding-star-hair-clip']
    latest = '<section class="section section-alt"><div class="page-width"><h2 class="section-title">Shop the Latest</h2><div class="product-grid">'
    latest += ''.join(card(h, root) for h in latest_handles)
    latest += '</div><p style="text-align:center;margin-top:30px"><a class="btn btn-outline" href="collections/all.html">View All Products</a></p></div></section>\n'

    bulk = f'''<section class="section"><div class="page-width">
<div class="bulk-banner"><img src="assets/images/site/Frame_1000004237_1.png" alt="Bulk orders" loading="lazy">
<div class="bulk-content"><h2>We Accept Bulk Orders</h2>
<p>Birthday return gifts, baby showers, festive hampers &amp; more</p>
<a class="btn btn-whatsapp" href="{wa_link('Hi! I would like to place a bulk order enquiry.')}" target="_blank" rel="noopener">{SVG_WA} Enquire on WhatsApp</a>
</div></div></div></section>\n'''

    featured = '<section class="section"><div class="page-width"><h2 class="section-title">Featured Products</h2><div class="product-grid">'
    featured += ''.join(card(h, root) for h in colls['featured-products'][:8])
    featured += '</div><p style="text-align:center;margin-top:30px"><a class="btn btn-outline" href="collections/featured-products.html">View All Featured</a></p></div></section>\n'

    tst = [
        ("Thank you so much dear for the timely delivery.. she was very happy to see them, specially the note written by you. She was very happy to see the message.. the quality of brooches is really very good.. just loved them.", "Shilpa Lahar Bathla"),
        ("The brooch is so beautifully made! The detailing is exquisite and it feels very premium. My daughter wore it on her dress, and everyone asked where it was from. Can you create 4 giraffe brooches as well? Would need by 25th Sept.", "Richa (Jaipur)"),
        ("Thank you Little Pink Llama, just received the towel and bathrobe set. Love the quality. Need something for a baby shower, do you do hampers??", "Divya Silot"),
    ]
    testis = '<section class="section section-alt"><div class="page-width"><h2 class="section-title">What Parents Are Saying</h2><div class="testimonials-grid">'
    for q, a in tst:
        testis += f'<div class="testimonial"><div class="stars">★★★★★</div><p>{html.escape(q)}</p><cite>- {html.escape(a)}</cite></div>'
    testis += '</div></div></section>\n'

    page = head('Little Pink Llama | Handcrafted Kids Accessories & Toys', root) + header(root, 'home') + '<main>' + hero + shop_coll + latest + bulk + featured + testis + '</main>' + footer(root)
    write('index.html', page)


def build_collections():
    root = '../'
    descs = {
        'all': ('Shop All', 'Every handcrafted piece — brooches, hair clips, crochet toys, collars & rakhis.'),
        'brooches': ('Brooches', 'Playful handcrafted brooches for every giggle.'),
        'hairclips': ('Hairclips', 'Adorable clips for your little star.'),
        'crochet-toys': ('Crochet toys', 'Crochet magic for tiny hearts.'),
        'collar': ('Collar', 'Elegant handcrafted collars.'),
        'rakhis': ('Rakhis', 'Handmade rakhis full of love.'),
        'featured-products': ('Featured Products', 'Our most loved picks, handcrafted in Jaipur.'),
    }
    lists = dict(colls)
    lists['all'] = list(prods.keys())
    for key, (title, desc) in descs.items():
        handles = [h for h in lists[key] if h in prods]
        body = f'''<main><div class="page-width">
<div class="breadcrumb"><a href="{root}index.html">Home</a> / {title}</div>
<div class="collection-header"><h1>{title}</h1><p>{html.escape(desc)}</p></div>
<div class="product-grid" style="padding:24px 0 40px">{''.join(card(h, root) for h in handles)}</div>
</div></main>'''
        page = head(f'{title} | Little Pink Llama', root) + header(root, 'shop') + body + footer(root)
        write(f'collections/{key}.html', page)


def clean_desc(bh):
    if not bh:
        return ''
    bh = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', bh, flags=re.S)
    bh = re.sub(r'\s(class|style|data-[\w-]+|dir|role|aria-\w+)="[^"]*"', '', bh)
    bh = re.sub(r'<img[^>]*>', '', bh)
    bh = re.sub(r'<span[^>]*>|</span>', '', bh)
    return bh


def build_products():
    root = '../'
    for h, p in prods.items():
        imgs = imgmap.get(h, [])
        title = p['title']
        price = rs(p['variants'][0]['price'])
        variants = [v['title'] for v in p['variants'] if v['title'] != 'Default Title']
        vhtml = ''
        if variants:
            opt = (p.get('options') or [{}])[0].get('name', 'Options')
            chips = ''.join(f'<span>{html.escape(v)}</span>' for v in variants)
            vhtml = f'<div class="variant-list"><h4>{html.escape(opt)}</h4><div class="variant-chips">{chips}</div></div>'
        main_src = f'{root}assets/images/products/{imgs[0]}' if imgs else f'{root}assets/images/site/logo.png'
        thumbs = ''.join(
            f'<img src="{root}assets/images/products/{im}" data-full="{root}assets/images/products/{im}" alt="{html.escape(title)} view {i + 1}" class="{"active" if i == 0 else ""}" loading="lazy">'
            for i, im in enumerate(imgs))
        wa = wa_link(f"Hi! I'd like to order the {title} ({price}). Is it available?")
        desc = clean_desc(p.get('body_html', ''))
        body = f'''<main><div class="page-width">
<div class="breadcrumb"><a href="{root}index.html">Home</a> / <a href="{root}collections/all.html">Shop all</a> / {html.escape(title)}</div>
<div class="product-layout">
  <div class="gallery">
    <div class="gallery-main"><img src="{main_src}" alt="{html.escape(title)}"></div>
    <div class="gallery-thumbs">{thumbs}</div>
  </div>
  <div class="product-info">
    <h1>{html.escape(title)}</h1>
    <div class="price">{price}</div>
    <div class="tax-note">Tax included. Free shipping across India.</div>
    {vhtml}
    <div class="order-note">We take orders personally! Message us on WhatsApp or Instagram and we'll confirm availability, colours &amp; delivery for you.</div>
    <div class="product-ctas">
      <a class="btn btn-whatsapp" href="{wa}" target="_blank" rel="noopener">{SVG_WA} Order on WhatsApp</a>
      <a class="btn btn-instagram" href="{IG}" target="_blank" rel="noopener">{SVG_IG} DM on Instagram</a>
    </div>
    <div class="product-desc">{desc}</div>
  </div>
</div>
</div></main>'''
        page = head(f'{title} | Little Pink Llama', root) + header(root, 'shop') + body + footer(root)
        write(f'products/{h}.html', page)


if __name__ == '__main__':
    build_home()
    build_collections()
    build_products()
    print('DONE')
