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


PAGE_MAP = {'/pages/about-us': 'pages/about-us.html', '/pages/contact': 'pages/contact.html',
            '/pages/faq': 'pages/faq.html', '/pages/shipping-return-policy': 'pages/shipping-policy.html',
            '/pages/return-policy': 'pages/return-policy.html', '/pages/terms-of-service': 'pages/terms-of-service.html',
            '/policies/privacy-policy': 'pages/privacy-policy.html', '/blogs/news': 'blogs/index.html', '/': 'index.html'}


def rewrite_internal_href(href, root):
    """Rewrite a raw Shopify href (absolute path or littlepinkllama.com URL)
    to a site-relative link. Single source of truth — used by both the
    regex-based sanitize() pass and ArticleRebuilder's per-tag rewrite, so
    a link fixed here never regresses in only one of the two code paths."""
    m = re.match(r'https?://littlepinkllama\.com(/[^\s]*)?$', href)
    if m:
        href = m.group(1) or '/'
    if href == '/' or href in PAGE_MAP:
        return root + PAGE_MAP.get(href, 'index.html')
    m = re.match(r'^/collections/([a-z0-9\-]+)$', href)
    if m:
        return f'{root}collections/{m.group(1)}.html'
    m = re.match(r'^/products/([a-z0-9_\-]+)$', href)
    if m:
        return f'{root}products/{m.group(1)}.html'
    m = re.match(r'^/blogs/news/([a-z0-9\-]+)$', href)
    if m:
        return f'{root}blogs/{m.group(1)}.html'
    return href


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
    # rewrite internal links (single source of truth: rewrite_internal_href)
    body = re.sub(r'href="([^"]*)"', lambda m: 'href="%s"' % rewrite_internal_href(m.group(1), root), body)
    # collapse empty wrappers
    for _ in range(6):
        body = re.sub(r'<(div|span|section|article|header|figure|p)>\s*</\1>', '', body)
    body = re.sub(r'\n{3,}', '\n\n', body)
    return body.strip()


def page(path, title, inner, active='', description=None, schema=None):
    # Skip the " | Little Pink Llama" suffix when it would push the <title>
    # tag past ~60 chars (SERP truncation risk) — long blog headlines
    # already carry the keywords that matter most.
    suffixed = title + ' | Little Pink Llama'
    page_title = title if len(suffixed) > 60 else suffixed
    doc = head(
        page_title, ROOT,
        description=description, canonical_path=path, schema=schema,
    ) + header(ROOT, active) + inner + footer(ROOT)
    write(path, doc)


# Leading <h2> banners in the scraped Shopify body that just repeat the page
# title — redundant once content_page() adds a real <h1>.
REDUNDANT_LEADING_HEADINGS = {'about us', 'frequently asked questions'}


def drop_redundant_leading_h2(body_html):
    """Strip a leading banner section whose only content is an <h2> (optionally
    wrapped in <strong>) matching a known page-title heading (see
    REDUNDANT_LEADING_HEADINGS) — the scraped Shopify body often opens with
    <section><div>...<h2>Page Title</h2>...</div></section> purely for
    layout, redundant once content_page() adds a real <h1>. Only removes
    the FIRST such section; leaves everything else untouched."""
    m = re.match(
        r'\s*(?:<(?:section|div)>\s*)*<h2>\s*(?:<strong>)?\s*([^<]*?)\s*(?:</strong>)?\s*</h2>'
        r'(?:\s*</(?:section|div)>\s*)*',
        body_html)
    if m and m.group(1).strip().rstrip('*—-').strip().lower() in REDUNDANT_LEADING_HEADINGS:
        return body_html[m.end():]
    return body_html


def content_page(path, title, body_html, active='', description=None, schema=None, h1=None):
    """`h1` prepends an <h1> when the scraped body doesn't already carry one
    (some Shopify pages open straight into an <h2> section) — every page
    needs exactly one <h1> for on-page SEO. Also drops a leading <h2> that
    just repeats the page title (see drop_redundant_leading_h2)."""
    if h1:
        body_html = drop_redundant_leading_h2(body_html)
    h1_html = f'<h1>{html.escape(h1)}</h1>' if h1 else ''
    inner = '<main><div class="content-page">%s%s</div></main>' % (h1_html, body_html)
    page(path, title, inner, active, description=description, schema=schema)


# ---- About us ----
about = sanitize(load('pages_about-us_main.html'), ROOT)
content_page(
    'pages/about-us.html', 'About us', about, 'about',
    description='Meet Little Pink Llama — handmade kids brooches, hair clips, crochet toys and collars, '
                'lovingly handcrafted in Jaipur, India. Our story, our craft, our promise.',
    h1='About Little Pink Llama',
)

# ---- FAQ: rewrite payment/ordering answers to WhatsApp flow ----
faq = sanitize(load('pages_faq_main.html'), ROOT)
faq = re.sub(
    r'No, we only accept secure online payments through Razorpay[^<]*',
    'We take orders personally over WhatsApp (+91 94600 74404) or Instagram DM. '
    'Message us with the product you love and we will confirm availability, payment and delivery details with you directly. ',
    faq)


def build_faq_schema(faq_html):
    """Extract Q&A pairs (<h3>question</h3>...answer...) into FAQPage JSON-LD."""
    entities = []
    for part in re.split(r'<h3>', faq_html)[1:]:
        m = re.match(r'([^<]*)</h3>(.*)', part, re.S)
        if not m:
            continue
        question = re.sub(r'\s+', ' ', m.group(1)).strip()
        answer_html = re.match(r'(.*?)(?=<h[23]>|$)', m.group(2), re.S).group(1)
        answer_text = re.sub(r'<[^>]+>', ' ', answer_html)
        answer_text = re.sub(r'\s+', ' ', answer_text).strip()
        if question and answer_text:
            entities.append({
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer_text},
            })
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities} if entities else None


content_page(
    'pages/faq.html', 'Frequently Asked Questions', faq,
    description='Answers to common questions about ordering, shipping, returns and product care '
                'at Little Pink Llama — handmade kids accessories from Jaipur, India.',
    h1='Frequently Asked Questions',
    schema=build_faq_schema(faq),
)

# ---- Policies ----
content_page(
    'pages/shipping-policy.html', 'Shipping Policy', sanitize(load('pages_shipping-return-policy_main.html'), ROOT),
    description='Shipping timelines and delivery details for Little Pink Llama orders across India and internationally.',
)
content_page(
    'pages/return-policy.html', 'Return Policy', sanitize(load('pages_return-policy_main.html'), ROOT),
    description='Return, exchange and credit note policy for Little Pink Llama handmade kids accessories.',
)
content_page(
    'pages/terms-of-service.html', 'Terms of Service', sanitize(load('pages_terms-of-service_main.html'), ROOT),
    description='Terms of service for shopping with Little Pink Llama, an India-based handmade kids accessories brand.',
)
content_page(
    'pages/privacy-policy.html', 'Privacy Policy', sanitize(load('policies_privacy-policy_main.html'), ROOT),
    description='How Little Pink Llama collects, uses and protects your personal information.',
)

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
    <p>Phone / WhatsApp: <strong>+91 99998 25527</strong></p>
    <p>Email: <strong>lplkidscouture@gmail.com</strong></p>
    <p>Instagram: <a href="{IG}" target="_blank" rel="noopener">@little_pink_llama_</a></p>
    <p style="margin-top:18px"><a class="btn btn-whatsapp" href="{wa_link('Hi Little Pink Llama! I have a question.')}" target="_blank" rel="noopener">{SVG_WA} Chat on WhatsApp</a></p>
    <p><a class="btn btn-instagram" href="{IG}" target="_blank" rel="noopener">{SVG_IG} DM on Instagram</a></p>
  </div>
</div>
</div></main>'''
page(
    'pages/contact.html', 'Contact', contact_inner, 'contact',
    description='Get in touch with Little Pink Llama on WhatsApp or Instagram — questions, custom orders '
                'and bulk enquiries for our handmade kids accessories, welcome.',
)

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
page(
    'blogs/index.html', 'Blogs',
    f'<main><div class="page-width"><div class="collection-header"><h1>Blogs</h1></div><div class="blog-grid" style="padding:20px 0 40px">{cards}</div></div></main>',
    'blogs',
    description='Handmade kids accessories tips, care guides and stories from Little Pink Llama — '
                'brooches, hair clips and crochet toys crafted in Jaipur, India.',
)

from html.parser import HTMLParser


class ArticleRebuilder(HTMLParser):
    """Re-emit only whitelisted content tags, guaranteed balanced."""
    KEEP = {'p', 'h2', 'h3', 'h4', 'ul', 'ol', 'li', 'strong', 'em', 'b', 'i',
            'blockquote', 'table', 'thead', 'tbody', 'tr', 'td', 'th', 'a'}
    SKIP_TEXT_IN = {'script', 'style', 'button', 'svg', 'form', 'noscript'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.stack = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TEXT_IN:
            self.skip_depth += 1
            return
        if tag in self.KEEP:
            if tag == 'a':
                href = dict(attrs).get('href', '#')
                rewritten = rewrite_internal_href(href, ROOT)
                is_internal = rewritten != href or href.startswith('#')
                target_attrs = '' if is_internal else ' target="_blank" rel="noopener"'
                self.out.append('<a href="%s"%s>' % (html.escape(rewritten, quote=True), target_attrs))
            else:
                self.out.append('<%s>' % tag)
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.SKIP_TEXT_IN:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if tag in self.KEEP and tag in self.stack:
            # close any inner unclosed tags first to stay balanced
            while self.stack:
                top = self.stack.pop()
                self.out.append('</%s>' % top)
                if top == tag:
                    break

    def handle_data(self, data):
        if self.skip_depth == 0:
            self.out.append(html.escape(data))

    def result(self):
        while self.stack:
            self.out.append('</%s>' % self.stack.pop())
        r = ''.join(self.out)
        r = re.sub(r'<(p|li|h2|h3|h4|blockquote)>\s*</\1>', '', r)
        return r


def rebuild_article(raw):
    # start at first real paragraph of the article body
    m = re.search(r'<p[ >]', raw)
    raw = raw[m.start():] if m else raw
    rb = ArticleRebuilder()
    rb.feed(raw)
    return rb.result()


import datetime as _dt

for slug, t, d, ex in posts:
    raw = load('blogs_news_%s_main.html' % slug)
    art = rebuild_article(raw)
    # drop share-widget remnants
    art = re.sub(r'Share\s*(Link\s*)?(Close share\s*)?(Copy link)?', '', art)
    iso_date = _dt.datetime.strptime(d, '%B %d, %Y').date().isoformat()
    inner = f'''<main><div class="blog-post">
<p class="breadcrumb" style="padding:0 0 14px"><a href="{ROOT}blogs/index.html">← All blogs</a></p>
<h1>{html.escape(t)}</h1><time datetime="{iso_date}">{d}</time>
<div class="blog-body">{art}</div>
</div></main>'''
    meta_desc = ex if len(ex) <= 160 else ex[:157].rsplit(' ', 1)[0].rstrip(',.;') + '…'
    blog_schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": t,
        "description": meta_desc,
        "datePublished": iso_date,
        "author": {"@type": "Organization", "name": "Little Pink Llama"},
        "publisher": {
            "@type": "Organization",
            "name": "Little Pink Llama",
            "logo": {"@type": "ImageObject", "url": f"{gen.SITE_URL}/assets/images/site/logo.png"},
        },
        "mainEntityOfPage": f"{gen.SITE_URL}/blogs/{slug}.html",
    }
    page('blogs/%s.html' % slug, t, inner, 'blogs', description=meta_desc, schema=blog_schema)

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
page(
    'pages/sitemap.html', 'Sitemap', sitemap_inner,
    description='Full list of pages, collections and products on the Little Pink Llama website.',
)

print('CONTENT PAGES DONE')
