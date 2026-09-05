"""Prepare and validate the dependency-free public website."""
from pathlib import Path
from html.parser import HTMLParser
import shutil

root = Path(__file__).resolve().parent
class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.modals = [], [], []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs: self.links.append(attrs[key])
        if 'data-modal' in attrs: self.modals.append(attrs['data-modal'])
page = Page()
page.feed((root / 'index.html').read_text())
assert len(page.ids) == len(set(page.ids)), 'Duplicate IDs'
for link in page.links:
    if link.startswith('#'): assert link[1:] in page.ids, f'Missing anchor: {link}'
    elif not link.startswith(('https:', 'mailto:')): assert (root / link).is_file(), f'Missing asset: {link}'
assert set(page.modals) == {'idiscover', 'angen', 'modern', 'otif'}
output = root / 'dist'
output.mkdir(exist_ok=True)
for name in ('index.html', 'styles.css', 'script.js'):
    shutil.copy2(root / name, output / name)
shutil.copytree(root / 'assets', output / 'assets', dirs_exist_ok=True)
print('Static build passed: unique IDs, internal links, local assets, and four project triggers checked.')
