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

# Singular product-type noun per real collection (excludes 'featured-products',
# which is a curated cross-section, not a type). Used to build keyword-rich
# product titles/descriptions when the product name itself doesn't say the
# type (e.g. "Bunny", "Ruby Sparkle") — Shopify's product_type/tags fields
# came back empty from the scrape, so this collection membership is the only
# type signal available.
COLLECTION_NOUN = {
    'brooches': 'brooch', 'hairclips': 'hair clip', 'crochet-toys': 'crochet toy',
    'collar': 'collar', 'rakhis': 'rakhi',
}


def product_type_noun(handle):
    for key, noun in COLLECTION_NOUN.items():
        if handle in colls.get(key, []):
            return noun
    return 'accessory'

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


SITE_URL = "https://littlepinkllama.com"
DEFAULT_OG_IMAGE = "assets/images/site/logo.png"


def head(title, root, description=None, canonical_path='', og_image=None, og_type='website', schema=None, noindex=False):
    """Page <head>. `canonical_path` is the page's path relative to site root
    (e.g. 'products/llama-brooch.html', '' for homepage) — used for both the
    canonical link and absolute OG/Twitter URLs. `schema` is a dict (or list
    of dicts) of JSON-LD to embed; omit for none. `noindex=True` for pages
    that should stay crawlable but excluded from search results (404)."""
    desc = description or 'Handcrafted brooches, hairclips, crochet toys and rakhis for kids — made with love in Jaipur, India. Order on WhatsApp or Instagram.'
    desc_esc = html.escape(desc)
    canonical_url = f"{SITE_URL}/{canonical_path}" if canonical_path else f"{SITE_URL}/"
    image_path = og_image or DEFAULT_OG_IMAGE
    image_url = f"{SITE_URL}/{image_path}"

    schema_tag = ''
    if schema is not None:
        schema_json = json.dumps(schema, ensure_ascii=False, indent=None)
        # </script> can't appear literally inside a script body
        schema_json = schema_json.replace('</', '<\\/')
        schema_tag = f'<script type="application/ld+json">{schema_json}</script>\n'

    robots_tag = '<meta name="robots" content="noindex, follow">\n' if noindex else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{desc_esc}">
{robots_tag}<link rel="canonical" href="{canonical_url}">
<link rel="icon" type="image/png" href="{root}assets/images/site/favicon.png">
<link rel="stylesheet" href="{root}assets/css/style.css?v=3">
<meta property="og:site_name" content="Little Pink Llama">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{desc_esc}">
<meta property="og:url" content="{canonical_url}">
<meta property="og:image" content="{image_url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{desc_esc}">
<meta name="twitter:image" content="{image_url}">
{schema_tag}</head>
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
    alt = f"{p['title']} — handmade kids accessory by Little Pink Llama"
    return f'''<div class="product-card">
  <a href="{root}products/{h}.html"><img src="{src}" alt="{html.escape(alt)}" loading="lazy"></a>
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
    for i, (img, htext, sub, link) in enumerate(slides):
        heading_tag = 'h1' if i == 0 else 'h2'  # exactly one H1 on the page, first slide carries it
        hero += f'''<div class="slide{' active' if i == 0 else ''}">
  <img src="{img}" alt="{html.escape(htext)} — handmade kids accessory, Little Pink Llama">
  <div class="slide-content">
    <{heading_tag}>{htext}</{heading_tag}>
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

    org_schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Little Pink Llama",
        "url": f"{SITE_URL}/",
        "logo": f"{SITE_URL}/assets/images/site/logo.png",
        "sameAs": [IG, FB],
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": "+91-99998-25527",
            "contactType": "customer service",
        },
    }
    website_schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Little Pink Llama",
        "url": f"{SITE_URL}/",
    }
    home_desc = ('Handcrafted kids accessories made with love in Jaipur — brooches, hair clips, '
                 'crochet toys & collars. Free shipping across India. Order on WhatsApp/Instagram.')
    page = head(
        'Little Pink Llama | Premium Kids Accessories, Handmade India',
        root,
        description=home_desc,
        canonical_path='',
        schema=[org_schema, website_schema],
    ) + header(root, 'home') + '<main>' + hero + shop_coll + latest + bulk + featured + testis + '</main>' + footer(root)
    write('index.html', page)


def build_collections():
    root = '../'
    # (title, on-page intro text, plural noun used in meta description)
    descs = {
        'all': ('Shop All', 'Every handcrafted piece — brooches, hair clips, crochet toys, collars & rakhis.', 'pieces'),
        'brooches': ('Brooches', 'Playful handcrafted brooches for every giggle.', 'brooches'),
        'hairclips': ('Hairclips', 'Adorable clips for your little star.', 'hairclips'),
        'crochet-toys': ('Crochet toys', 'Crochet magic for tiny hearts.', 'crochet toys'),
        'collar': ('Collar', 'Elegant handcrafted collars.', 'collars'),
        'rakhis': ('Rakhis', 'Handmade rakhis full of love.', 'rakhis'),
        'featured-products': ('Featured Products', 'Our most loved picks, handcrafted in Jaipur.', 'picks'),
    }
    lists = dict(colls)
    lists['all'] = list(prods.keys())
    for key, (title, desc, noun) in descs.items():
        handles = [h for h in lists[key] if h in prods]
        body = f'''<main><div class="page-width">
<div class="breadcrumb"><a href="{root}index.html">Home</a> / {title}</div>
<div class="collection-header"><h1>{title}</h1><p>{html.escape(desc)}</p></div>
<div class="product-grid" style="padding:24px 0 40px">{''.join(card(h, root) for h in handles)}</div>
</div></main>'''
        meta_desc = f"{desc} Shop {len(handles)} handmade {noun} for kids from Jaipur, India."
        breadcrumb_schema = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
                {"@type": "ListItem", "position": 2, "name": title, "item": f"{SITE_URL}/collections/{key}.html"},
            ],
        }
        page = head(
            f'{title} | Little Pink Llama',
            root,
            description=meta_desc,
            canonical_path=f'collections/{key}.html',
            schema=breadcrumb_schema,
        ) + header(root, 'shop') + body + footer(root)
        write(f'collections/{key}.html', page)


def clean_desc(bh):
    if not bh:
        return ''
    bh = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', bh, flags=re.S)
    bh = re.sub(r'\s(class|style|data-[\w-]+|dir|role|aria-\w+)="[^"]*"', '', bh)
    bh = re.sub(r'<img[^>]*>', '', bh)
    bh = re.sub(r'<span[^>]*>|</span>', '', bh)
    return bh


def meta_description_from_html(body_html, fallback, limit=155):
    text = re.sub(r'<[^>]+>', ' ', body_html or '')
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    if not text:
        text = fallback
    if len(text) > limit:
        text = text[:limit].rsplit(' ', 1)[0].rstrip(',.;') + '…'
    return text


def build_products():
    root = '../'
    for h, p in prods.items():
        imgs = imgmap.get(h, [])
        title = p['title']
        price_val = p['variants'][0]['price']
        price = rs(price_val)
        variants = [v['title'] for v in p['variants'] if v['title'] != 'Default Title']
        vhtml = ''
        if variants:
            opt = (p.get('options') or [{}])[0].get('name', 'Options')
            chips = ''.join(f'<span>{html.escape(v)}</span>' for v in variants)
            vhtml = f'<div class="variant-list"><h4>{html.escape(opt)}</h4><div class="variant-chips">{chips}</div></div>'
        main_src = f'{root}assets/images/products/{imgs[0]}' if imgs else f'{root}assets/images/site/logo.png'
        main_alt = f"{title} — handmade kids accessory, Little Pink Llama"
        thumbs = ''.join(
            f'<img src="{root}assets/images/products/{im}" data-full="{root}assets/images/products/{im}" alt="{html.escape(title)} — additional photo {i + 1}" class="{"active" if i == 0 else ""}" loading="lazy">'
            for i, im in enumerate(imgs))
        wa = wa_link(f"Hi! I'd like to order the {title} ({price}). Is it available?")
        desc = clean_desc(p.get('body_html', ''))
        body = f'''<main><div class="page-width">
<div class="breadcrumb"><a href="{root}index.html">Home</a> / <a href="{root}collections/all.html">Shop all</a> / {html.escape(title)}</div>
<div class="product-layout">
  <div class="gallery">
    <div class="gallery-main"><img src="{main_src}" alt="{html.escape(main_alt)}"></div>
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
        meta_desc = meta_description_from_html(
            p.get('body_html', ''),
            f"{title} — handmade for kids, {price}. Made in Jaipur. Order on WhatsApp or Instagram — free shipping across India.")
        # Keyword-rich <title>: most products are named "Name - Type" (e.g.
        # "Llama - Brooch"); rewrite to "Name Handmade Type for Kids" so the
        # type/audience keywords lead instead of trailing after a dash. A
        # few products (crochet toys, collar items) have no " - " in their
        # name — fall back to collection-derived product_type_noun().
        if ' - ' in title:
            product_name, _, type_word = title.partition(' - ')
            product_name, type_word = product_name.strip(), type_word.strip()
            seo_title_base = f"{product_name} Handmade {type_word} for Kids"
        else:
            # No " - Type" suffix in the name (crochet toys, some collar
            # items). Capitalize each word ("Small bear" -> "Small Bear"),
            # preserving words that already carry internal capitals (e.g.
            # "K-Pop"). Only append the type noun if the name doesn't
            # already say it ("Guiding Star Hair Clip", "Derpy Tiger Collar").
            product_name = ' '.join(w if any(c.isupper() for c in w[1:]) else w.capitalize() for w in title.split())
            noun = product_type_noun(h)
            if noun.lower() in title.lower():
                seo_title_base = f"{product_name} — Handmade for Kids"
            else:
                seo_title_base = f"{product_name} — Handmade {noun.title()} for Kids"
        # Drop the brand suffix when it would push past ~60 chars (SERP
        # truncation risk) — same rule gen_pages.py's page() applies to
        # long blog titles; the keyword-rich headline matters more than
        # the trailing brand name once it no longer fits.
        seo_title_full = f"{seo_title_base} | Little Pink Llama"
        seo_title = seo_title_base if len(seo_title_full) > 60 else seo_title_full
        schema = {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": title,
            "image": [f"{SITE_URL}/assets/images/products/{im}" for im in imgs] or [f"{SITE_URL}/{DEFAULT_OG_IMAGE}"],
            "description": meta_desc,
            "brand": {"@type": "Brand", "name": "Little Pink Llama"},
            "offers": {
                "@type": "Offer",
                "url": f"{SITE_URL}/products/{h}.html",
                "priceCurrency": "INR",
                "price": str(price_val),
                "availability": "https://schema.org/InStock",
            },
        }
        page = head(
            seo_title,
            root,
            description=meta_desc,
            canonical_path=f'products/{h}.html',
            og_image=f'assets/images/products/{imgs[0]}' if imgs else None,
            og_type='product',
            schema=schema,
        ) + header(root, 'shop') + body + footer(root)
        write(f'products/{h}.html', page)


if __name__ == '__main__':
    build_home()
    build_collections()
    build_products()
    print('DONE')
