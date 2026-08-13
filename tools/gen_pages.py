# -*- coding: utf-8 -*-
"""Generator for content pages: about, contact, FAQ, policies, blogs, sitemap.

Reads the scraped page HTML (``*_main.html``) from the scratch dir given as
argv[1]; sanitizes Shopify markup and wraps it in the shared site layout.
"""
import os, re, sys, html

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen
from gen import head, header, footer, write, wa_link, SVG_WA, SVG_IG, IG

SCRATCH = sys.argv[1]
ROOT = '../'


def load(name):
    return open(os.path.join(SCRATCH, name), encoding='utf-8').read()


def sanitize(body, root):
    """Strip Shopify chrome, keep semantic content, rewrite internal links."""
    body = re.sub(r'<(script|style|noscript|svg|form|button)[^>]*>.*?</\1>', '', body, flags=re.S)
    body = re.sub(r'<(details|summary)[^>]*>|</(details|summary)>', '', body)
    body = re.sub(r'<link[^>]*>', '', body)
    body = re.sub(r'Shopify(\s*\(and any additional service partners you use\))?', 'our service partners', body)
    # drop share widgets and Shopify wrappers but keep inner content
    body = re.sub(r'<[^>]*share[^>]*>.*?</[^>]+>', '', body, flags=re.S | re.I)
    # keep only href on anchors; drop all other attributes everywhere
    body = re.sub(r'<a\s[^>]*href="([^"]*)"[^>]*>', r'<a href="\1">', body)
    for tag in ['div', 'p', 'h1', 'h2', 'h3', 'h4', 'ul', 'ol', 'li', 'strong', 'em', 'span', 'section', 'article', 'header', 'blockquote', 'table', 'tr', 'td', 'th', 'time', 'figure', 'figcaption']:
        body = re.sub(r'<%s\s[^>]*>' % tag, '<%s>' % tag, body)
    # images: keep only littlepinkllama CDN ones? drop — content pages get no imgs (about handled separately)
    body = re.sub(r'<img[^>]*>', '', body)
    # rewrite internal links
    body = body.replace('href="/collections/', 'href="%scollections/' % root)
    body = re.sub(r'href="(%scollections/[a-z0-9\-]+)"' % re.escape(root), r'href="\1.html"', body)
    body = body.replace('href="/products/', 'href="%sproducts/' % root)
    body = re.sub(r'href="(%sproducts/[a-z0-9_\-]+)"' % re.escape(root), r'href="\1.html"', body)
    page_map = {'/pages/about-us': 'pages/about-us.html', '/pages/contact': 'pages/contact.html',
                '/pages/faq': 'pages/faq.html', '/pages/shipping-return-policy': 'pages/shipping-policy.html',
                '/pages/return-policy': 'pages/return-policy.html', '/pages/terms-of-service': 'pages/terms-of-service.html',
                '/policies/privacy-policy': 'pages/privacy-policy.html', '/blogs/news': 'blogs/index.html', '/': 'index.html'}
    for k, v in page_map.items():
        body = body.replace('href="%s"' % k, 'href="%s%s"' % (root, v))
    body = re.sub(r'href="/blogs/news/([a-z0-9\-]+)"', r'href="%sblogs/\1.html"' % root, body)
    body = re.sub(r'href="https?://littlepinkllama\.com/?"', 'href="%sindex.html"' % root, body)
    # collapse empty wrappers
    for _ in range(6):
        body = re.sub(r'<(div|span|section|article|header|figure|p)>\s*</\1>', '', body)
    body = re.sub(r'\n{3,}', '\n\n', body)
    return body.strip()


def page(path, title, inner, active=''):
    doc = head(title + ' | Little Pink Llama', ROOT) + header(ROOT, active) + inner + footer(ROOT)
    write(path, doc)


def content_page(path, title, body_html, active=''):
    inner = '<main><div class="content-page">%s</div></main>' % body_html
    page(path, title, inner, active)


# ---- About us ----
about = sanitize(load('pages_about-us_main.html'), ROOT)
content_page('pages/about-us.html', 'About us', about, 'about')

# ---- FAQ: rewrite payment/ordering answers to WhatsApp flow ----
faq = sanitize(load('pages_faq_main.html'), ROOT)
faq = re.sub(
    r'No, we only accept secure online payments through Razorpay[^<]*',
    'We take orders personally over WhatsApp (+91 94600 74404) or Instagram DM. '
    'Message us with the product you love and we will confirm availability, payment and delivery details with you directly. ',
    faq)
content_page('pages/faq.html', 'Frequently Asked Questions', faq)

# ---- Policies ----
content_page('pages/shipping-policy.html', 'Shipping Policy', sanitize(load('pages_shipping-return-policy_main.html'), ROOT))
content_page('pages/return-policy.html', 'Return Policy', sanitize(load('pages_return-policy_main.html'), ROOT))
content_page('pages/terms-of-service.html', 'Terms of Service', sanitize(load('pages_terms-of-service_main.html'), ROOT))
content_page('pages/privacy-policy.html', 'Privacy Policy', sanitize(load('policies_privacy-policy_main.html'), ROOT))

# ---- Contact ----
contact_inner = f'''<main><div class="content-page">
<h1>Contact</h1>
<div class="contact-grid">
  <form class="contact-form">
    <label for="cf-name">Name</label>
    <input id="cf-name" name="name" type="text" required>
    <label for="cf-email">Email *</label>
    <input id="cf-email" name="email" type="email" required>
    <label for="cf-phone">Phone number</label>
    <input id="cf-phone" name="phone" type="tel">
    <label for="cf-comment">Comment</label>
    <textarea id="cf-comment" name="comment" rows="5"></textarea>
    <p style="margin-top:16px"><button class="btn btn-whatsapp" type="submit">{SVG_WA} Send via WhatsApp</button></p>
  </form>
  <div class="contact-card">
    <h3>Reach us directly</h3>
    <p>Phone / WhatsApp: <strong>+91 94600 74404</strong></p>
    <p>Email: <strong>lplkidscouture@gmail.com</strong></p>
    <p>Instagram: <a href="{IG}" target="_blank" rel="noopener">@little_pink_llama_</a></p>
    <p style="margin-top:18px"><a class="btn btn-whatsapp" href="{wa_link('Hi Little Pink Llama! I have a question.')}" target="_blank" rel="noopener">{SVG_WA} Chat on WhatsApp</a></p>
    <p><a class="btn btn-instagram" href="{IG}" target="_blank" rel="noopener">{SVG_IG} DM on Instagram</a></p>
  </div>
</div>
</div></main>'''
page('pages/contact.html', 'Contact', contact_inner, 'contact')

# ---- Blogs ----
posts = [
    ('hair-clip-care-tips-for-kids', "How to Care for Your Kids' Hair Clips (So They Last for Years)", 'April 5, 2026',
     "A Rs.549 handmade hair clip can last years — if you care for it properly. Here's the complete guide to cleaning, storing, and maintaining your child's hair accessories."),
    ('why-handmade-beats-mass-produced', 'Handmade Accessories Vs Mass Produced: The Little Pink Llama Difference', 'April 4, 2026',
     'Why do parents choose handmade over mass produced? The difference you can see, feel and trust.'),
    ('why-a-brooch-is-more-than-an-accessory-for-your-little-one', 'Why a Brooch is More Than an Accessory for Your Little One', 'February 21, 2026',
     'In a world of fast fashion, a thoughtfully crafted brooch holds a different kind of charm.'),
]
cards = ''.join(
    f'<a class="blog-card" href="{slug}.html"><h3>{html.escape(t)}</h3><time>{d}</time><p>{html.escape(ex)}</p></a>'
    for slug, t, d, ex in posts)
page('blogs/index.html', 'Blogs', f'<main><div class="page-width"><div class="collection-header"><h1>Blogs</h1></div><div class="blog-grid" style="padding:20px 0 40px">{cards}</div></div></main>', 'blogs')

for slug, t, d, ex in posts:
    raw = load('blogs_news_%s_main.html' % slug)
    art = sanitize(raw, ROOT)
    # strip everything before the first heading remnants / share text
    art = re.sub(r'Share\s*Link\s*Close share\s*Copy link', '', art)
    art = re.sub(r'<h1>.*?</h1>', '', art, count=1, flags=re.S)
    inner = f'<main><div class="blog-post"><h1>{html.escape(t)}</h1><time>{d}</time>{art}</div></main>'
    page('blogs/%s.html' % slug, t, inner, 'blogs')

# ---- Sitemap ----
prod_links = ''.join(f'<li><a href="{ROOT}products/{h}.html">{html.escape(p["title"])}</a></li>' for h, p in gen.prods.items())
sitemap_inner = f'''<main><div class="content-page">
<h1>Sitemap</h1>
<h2>Pages</h2>
<ul>
<li><a href="{ROOT}index.html">Home</a></li>
<li><a href="{ROOT}pages/about-us.html">About us</a></li>
<li><a href="{ROOT}pages/contact.html">Contact</a></li>
<li><a href="{ROOT}blogs/index.html">Blogs</a></li>
<li><a href="{ROOT}pages/faq.html">FAQ</a></li>
<li><a href="{ROOT}pages/shipping-policy.html">Shipping Policy</a></li>
<li><a href="{ROOT}pages/return-policy.html">Return Policy</a></li>
<li><a href="{ROOT}pages/terms-of-service.html">Terms of Service</a></li>
<li><a href="{ROOT}pages/privacy-policy.html">Privacy Policy</a></li>
</ul>
<h2>Collections</h2>
<ul>
<li><a href="{ROOT}collections/all.html">Shop All</a></li>
<li><a href="{ROOT}collections/brooches.html">Brooches</a></li>
<li><a href="{ROOT}collections/hairclips.html">Hairclips</a></li>
<li><a href="{ROOT}collections/crochet-toys.html">Crochet toys</a></li>
<li><a href="{ROOT}collections/collar.html">Collar</a></li>
<li><a href="{ROOT}collections/rakhis.html">Rakhis</a></li>
<li><a href="{ROOT}collections/featured-products.html">Featured Products</a></li>
</ul>
<h2>Products</h2>
<ul>{prod_links}</ul>
</div></main>'''
page('pages/sitemap.html', 'Sitemap', sitemap_inner)

print('CONTENT PAGES DONE')
