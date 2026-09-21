# -*- coding: utf-8 -*-
"""Generator for 404.html.

Its content needs no scraped data, but it imports gen.py for head()/header()/
footer(), and gen.py itself requires a scratch dir at argv[1] (product/image
data) to import at all — so pass one anyway, e.g. the same dir used for the
other generators. Regenerate whenever header/footer change.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen
from gen import head, header, footer, write

inner = '''<main><div class="content-page" style="text-align:center;padding:80px 20px">
<h1>Page not found</h1>
<p>Oops! That page wandered off with the llama.</p>
<p><a class="btn btn-pink" href="index.html">Back to Home</a></p>
</div></main>'''

doc = (
    head(
        'Page not found | Little Pink Llama', '',
        description='This page could not be found. Browse Little Pink Llama\'s handmade kids accessories instead.',
        canonical_path='404.html',
        noindex=True,
    )
    + header('')
    + inner
    + footer('')
)
write('404.html', doc)
print('wrote 404.html')
