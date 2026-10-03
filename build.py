"""Generate portable static pages from the portfolio content and shared templates."""
import hashlib, json, re, shutil
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'content/portfolio.json').read_text())
CSS_VERSION=hashlib.sha256((ROOT/'styles.css').read_bytes()).hexdigest()[:12]
def esc(value): return escape(str(value), quote=True)
def template(name, values):
    text=(ROOT/'templates'/name).read_text()
    for k,v in values.items(): text=text.replace('{{'+k+'}}',str(v))
    if re.search(r'\{\{\w+\}\}',text): raise ValueError('Unresolved template: '+name)
    return text

def frame(body,title,description,path='',prefix=''):
    canonical=DATA['origin']+'/'+path
    social='<meta name="twitter:card" content="summary">'
    if not path:
        social=f'<meta property="og:image" content="{DATA["origin"]}/assets/social-preview.jpg"><meta property="og:image:width" content="1734"><meta property="og:image:height" content="907"><meta property="og:image:alt" content="Parth Sarthi — Data architecture, platform modernisation and technical leadership"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{DATA["origin"]}/assets/social-preview.jpg">'
    person={'@context':'https://schema.org','@type':'Person','name':DATA['name'],'url':DATA['origin'],'jobTitle':'Solution Architect','email':'mailto:'+DATA['email'],'sameAs':[DATA['linkedin']],'worksFor':{'@type':'Organization','name':'Tata Consultancy Services'},'knowsAbout':['Data architecture','Data engineering','Platform modernisation','Technical leadership']}
    schema=person if not path else {'@context':'https://schema.org','@type':'Article','headline':title,'description':description,'url':canonical,'author':{'@type':'Person','name':DATA['name'],'url':DATA['origin']}}
    return template('base.html',dict(BODY=body,TITLE=esc(title),DESCRIPTION=esc(description),CANONICAL=esc(canonical),ROOT=prefix,CSS_VERSION=CSS_VERSION,SOCIAL=social,SCHEMA=json.dumps(schema).replace('</','<\\/')))

def graphic(project):
    slug=project['slug']
    if slug=='idiscover':
        inner='<div class="platform-map"><div class="domain-stack"><span>Pharmaceutical</span><span>Commercial</span><span>Supply chain</span></div><span class="flow-arrow" aria-hidden="true">→</span><div class="platform-core"><strong>iDiscover</strong><p>INGEST / MODEL / GOVERN</p></div></div><div class="platform-out"><span>Enterprise warehouse</span><span>→</span><span>AnGen / analytics</span></div>'
        kind='platform'; label='A SHARED ENTERPRISE FOUNDATION'
    elif slug=='modernisation':
        inner='<div class="modern-line"><div><span>01</span><strong>Talend</strong><small>Legacy ETL estate</small></div><div><span>02</span><strong>AWS / Airflow</strong><small>1,000+ jobs migrated</small></div><div><span>03</span><strong>Databricks</strong><small>Current evolution · in progress</small></div></div>'
        kind='modern';label='PLATFORM EVOLUTION / THREE CHAPTERS'
    else:
        inner='<div class="semantic-map"><p>COMMERCIAL + MEDICAL DATA</p><div class="semantic-marts">'+''.join(f'<span>{i:02}</span>' for i in range(1,11))+'</div><strong>10+</strong><small>GOVERNED DATA MARTS → TABLEAU</small></div>'
        kind='analytics';label='THE SEMANTIC LAYER / ANGEN'
    return f'<div class="project-graphic graphic-{kind}" role="img" aria-label="{esc(project["summary"])}"><span class="graphic-label">{label}</span>{inner}<span class="graphic-caption">CONCEPTUAL VIEW / {project["number"]}</span></div>'

projects=''
for p in DATA['projects'][:3]:
    projects+=f'<article class="project-feature">{graphic(p)}<div class="project-info"><div class="project-kicker"><span>{p["number"]}</span><span class="eyebrow">{esc(p["category"])}</span></div><h3>{esc(p["title"])}</h3><p>{esc(p["summary"])}</p><p class="project-name">{esc(p["name"])} / TCS · Johnson & Johnson</p><a class="text-link" href="work/{p["slug"]}/">Read the case study <span>↗</span></a></div></article>'
milestones=''.join(f'<article><span class="eyebrow">{esc(year)}</span><h3>{esc(title)}</h3><p>{esc(copy)}</p></article>' for year,title,copy in DATA['milestones'])
credentials=''
for i,c in enumerate(DATA['credentials']):
    links=c.get('verificationLinks') or ([{'label':'Verify credential','url':c['url']}] if c.get('url') else [])
    for verification in links:
        assert urlsplit(verification['url']).scheme == 'https', f'Credential URL must use HTTPS: {c["title"]}'
    if links:
        action='<div class="credential-verifications">'+''.join(
            f'<a href="{esc(item["url"])}" target="_blank" rel="noopener noreferrer">{esc(item["label"])}</a>'
            for item in links
        )+'</div>'
    else:
        action='<span>Verification link pending</span>'
    credentials+=f'<article class="credential-card" data-group="{esc(c["group"])}"><span class="eyebrow">{esc(c["label"])}</span><h3>{esc(c["title"])}</h3><p>{esc(c["type"])}</p><div class="credential-bottom">{action}<span>{i+1:02}</span></div></article>'
body=template('home.html',dict(PROJECTS=projects,MILESTONES=milestones,CREDENTIALS=credentials,SUPER30_IMAGE='__SUPER30_IMAGE__'))
# Curated photography slots can be replaced by editing content only.
for photo in DATA['photography']:
    if photo['src']:
        assert photo['alt'], 'Published photography requires descriptive alt text'
        width,height=photo['width'],photo['height']
        ratio=f'{width} / {height}'
        image=f'<figure class="real-photo"><img src="{esc(photo["src"])}" alt="{esc(photo["alt"])}" width="{width}" height="{height}" loading="{ "eager" if photo["id"]=="portrait" else "lazy"}" style="aspect-ratio:{ratio};object-fit:cover"><figcaption>{esc(photo["caption"])}</figcaption></figure>'
        if photo['id']=='portrait':
            image=image.replace('class="real-photo"','class="real-photo hero-portrait"')
            pattern=r'<div class="portrait-slot">.*?</div></div>'
            body=re.sub(pattern,lambda match:image,body,count=1,flags=re.S)
        elif photo['id']=='super30':
            image=image.replace('class="real-photo"','class="real-photo super30-photo"')
            body=body.replace('__SUPER30_IMAGE__',image,1)
        elif photo['id']=='fieldnote':
            image=image.replace('class="real-photo"','class="real-photo fieldnote-photo"')
            pattern=r'<div class="fieldnote-slot">.*?</div>'
            body=re.sub(pattern,lambda match:image,body,count=1,flags=re.S)
            body=body.replace('There’s more to the story.',esc(photo['title']))
            body=body.replace('A space for a real moment beyond work—and the story that makes it worth sharing.',esc(photo.get('story','')))
            if photo.get('story'):body=re.sub(r'<p class="draft-note">.*?</p>','',body)
# Optional authentic material is rendered only when supplied and approved.
extra=''
for collection in ('achievements','community','writing','testimonials'):
    entries=[x for x in DATA[collection] if x.get('published')]
    if entries:
        extra+=f'<section class="section wrap additional-stories"><span class="eyebrow">{collection.upper()}</span>'
        for item in entries:
            extra+=f'<article><h3>{esc(item["title"])}</h3><p>{esc(item["description"])}</p>'
            if item.get('url'): extra+=f'<a class="text-link" href="{esc(item["url"])}">Read more ↗</a>'
            extra+='</article>'
        extra+='</section>'
body=body.replace('<section class="contact-section"',extra+'<section class="contact-section"')
(ROOT/'index.html').write_text(frame(body,'Parth Sarthi — Data Architecture & Technical Leadership','Data architecture, platform modernisation and delivery leadership. Explore Parth Sarthi’s enterprise platforms, 1,000+ job migration and ~60-person delivery portfolio.'))
for i,p in enumerate(DATA['projects']):
    nxt=DATA['projects'][(i+1)%len(DATA['projects'])]
    vals={k.upper():esc(v) for k,v in p.items() if isinstance(v,str)}
    vals.update(HEADLINE=esc(p['title']),PROBLEM_TITLE='The challenge behind the platform.' if p['slug']!='otif' else 'A delivery date has dependencies.',FLOW=''.join(f'<div class="case-flow-step"><span>{j+1:02}</span><div><strong>{esc(title)}</strong><small>{esc(copy)}</small></div></div>' for j,(title,copy) in enumerate(p['flow'])),DECISIONS=''.join(f'<article><span>{j+1:02}</span><p>{esc(copy)}</p></article>' for j,copy in enumerate(p['decisions'])),STACK=' · '.join(map(esc,p['stack'])),METRIC_LABEL=esc(p['metricLabel']),GAPS=''.join(f'<li>{esc(g)}</li>' for g in p['gaps']),NEXT_SLUG=nxt['slug'],NEXT_NAME=esc(nxt['name']))
    folder=ROOT/'work'/p['slug'];folder.mkdir(parents=True,exist_ok=True)
    (folder/'index.html').write_text(frame(template('case.html',vals),p['name']+' — '+p['title'],p['summary'],'work/'+p['slug']+'/', '../../'))
# Build only an explicit allowlist; never publish briefs or source documents.
OUT=ROOT/'dist';OUT.mkdir(exist_ok=True)
for name in ('index.html','styles.css','script.js'):shutil.copy2(ROOT/name,OUT/name)
for name in ('assets','work'):shutil.copytree(ROOT/name,OUT/name,dirs_exist_ok=True)
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+DATA['origin']+'/sitemap.xml\n')
urls=[DATA['origin']+'/']+[DATA['origin']+'/work/'+p['slug']+'/' for p in DATA['projects']]
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+esc(url)+'</loc></url>' for url in urls)+'</urlset>')
class Page(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.links=[];self.h1=0
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='h1':self.h1+=1
        if 'id' in attrs:self.ids.append(attrs['id'])
        for key in ('src','href'):
            if key in attrs:self.links.append(attrs[key])
pages={}
for file in OUT.rglob('*.html'):
    page=Page();page.feed(file.read_text());pages[file.resolve()]=page
    assert len(page.ids)==len(set(page.ids)),f'Duplicate ids: {file}'
    assert page.h1==1,f'Expected one h1: {file}'
    assert '{{' not in file.read_text(),f'Unresolved template: {file}'
for file,page in pages.items():
    for link in page.links:
        parsed=urlsplit(link)
        if parsed.scheme or parsed.netloc:continue
        dest=(file.parent/unquote(parsed.path)).resolve() if parsed.path else file
        if dest.is_dir():dest=dest/'index.html'
        assert dest.is_relative_to(OUT.resolve()),f'Link outside public output: {link}'
        assert dest.exists(),f'Broken link in {file}: {link}'
        if parsed.fragment and dest in pages:assert parsed.fragment in pages[dest].ids,f'Missing anchor: {link}'
for font in ('instrument-serif','instrument-serif-italic','inter'):
    assert (OUT/'assets/fonts'/f'{font}.woff2').read_bytes()[:4]==b'wOF2',f'Invalid font: {font}'
assert (ROOT/'styles.css').read_text().count('{')==(ROOT/'styles.css').read_text().count('}')
print(f'Built and validated {len(pages)} pages: links, anchors, headings, assets, fonts and template completion.')
