#!/usr/bin/env python3
"""Build the static site from public content. Python standard library only."""
import argparse
from collections import defaultdict
from datetime import datetime
from html import escape as e
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://adamdhines.github.io'
SOCIALS = {'Google Scholar':'https://scholar.google.com/citations?user=rH2jg5UAAAAJ&hl=en', 'GitHub':'https://github.com/adamdhines', 'LinkedIn':'https://www.linkedin.com/in/adamdhines/', 'ORCID':'https://orcid.org/0000-0002-0259-3642'}
PAPERS = json.loads((ROOT/'data/publications.json').read_text())
NEWS = json.loads((ROOT/'data/news.json').read_text())
CAREER = json.loads((ROOT/'data/career.json').read_text())
PAGES = {'index.html':('About','Adam Hines | Robotics & Event-Based Vision','Adam Hines is a QUT roboticist working on vision-based positioning for Roo-ver, Australia’s first lunar rover, event-based vision, and open-source tools.'), 'papers.html':('Publications','Publications | Adam Hines','Research publications by Adam Hines on event-based vision, robotic localisation, neuromorphic computing, and neuroscience.'), 'cv.html':('CV','CV & Experience | Adam Hines','Adam Hines’s research experience, education, open-source software, teaching, and academic service. Download his public academic CV.'), 'news.html':('News','Research & EventCV News | Adam Hines','Updates from Adam Hines: EventCV releases, event-based vision research, publications, appointments, and outreach.')}

def links(items):
    return ''.join(f'<a href="{e(url,quote=True)}">{e(label)}</a>' for label,url in items.items())

def page(filename, body):
    label,title,description=PAGES[filename]
    url=BASE+('/' if filename=='index.html' else '/'+filename)
    nav=''.join(f'<a href="{("/" if name=="index.html" else "/"+name)}"'+(' aria-current="page"' if name==filename else '')+f'>{info[0]}</a>' for name,info in PAGES.items())
    structured={'@context':'https://schema.org','@graph':[{'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/','name':'Adam Hines','alternateName':'Adam D Hines'}]}
    if filename=='index.html':
        structured['@graph'] += [{'@type':'ProfilePage','@id':BASE+'/#profile','url':url,'name':title,'dateModified':CAREER['updated'],'mainEntity':{'@id':BASE+'/#adam-hines'}},{'@type':'Person','@id':BASE+'/#adam-hines','name':'Adam Hines','alternateName':['Adam D Hines','Dr Adam D Hines'],'url':BASE+'/','image':BASE+'/static/images/portrait.webp','jobTitle':'Research Fellow','worksFor':{'@type':'Organization','name':'Queensland University of Technology','url':'https://www.qut.edu.au/'},'knowsAbout':['Robotics','Event-based vision','Robotic localisation','Open-source software'],'sameAs':list(SOCIALS.values())}]
    else:
        structured['@graph'] += [{'@type':'WebPage','url':url,'name':title,'description':description,'about':{'@id':BASE+'/#adam-hines'}}]
    return f'''<!DOCTYPE html>
<html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(description,quote=True)}"><link rel="canonical" href="{url}">
<meta name="robots" content="index, follow"><meta name="google-site-verification" content="4FxfVyL6UTuTgW_XYHHlLDI7P4y3i41wxtjFa8Fd5rs">
<meta name="theme-color" content="#f7f6f0"><link rel="icon" type="image/png" href="/static/images/favicon.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="Adam Hines"><meta property="og:title" content="{e(title,quote=True)}"><meta property="og:description" content="{e(description,quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/static/images/social.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Adam Hines — Robotics and event-based vision">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title,quote=True)}"><meta name="twitter:description" content="{e(description,quote=True)}"><meta name="twitter:image" content="{BASE}/static/images/social.jpg">
<link rel="preload" href="/static/fonts/source-sans-3-regular.ttf" as="font" type="font/ttf" crossorigin><link rel="stylesheet" href="/static/css/site.css">
<script type="application/ld+json">{json.dumps(structured,ensure_ascii=False)}</script></head>
<body><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><nav class="nav wrap" aria-label="Main navigation"><a class="brand" href="/" aria-label="Adam Hines — home"><span class="brand-mark" aria-hidden="true">{('<i></i>'*9)}</span>Adam Hines<span aria-hidden="true">.</span></a><div class="nav-links">{nav}</div></nav></header>
<main id="main">{body}</main>
<footer class="site-footer"><div class="wrap"><div class="footer-top"><div><h2>Let’s talk vision.</h2><a href="mailto:adam.hines@qut.edu.au">adam.hines@qut.edu.au</a></div><nav class="footer-socials" aria-label="Professional profiles">{links(SOCIALS)}</nav></div><div class="footer-bottom"><span>© {CAREER['updated'][:4]} Adam D Hines</span><span>Robotics &amp; event-based vision · Brisbane, Australia</span></div></div></footer></body></html>'''

def date_text(n):
    return (n['month']+' ' if n['month'] else '')+str(n['year'])

def news_link(n):
    return f'<br><a href="{e(n["url"],quote=True)}">{e(n.get("link_label","Read more"))} ↗</a>' if n.get('url') else ''

def home():
    work = [
        ('eventcv', 'EventCV', 'Open-source Python and Rust tools for event-based computer vision.', 'https://eventcv.net/', 'eventcv-paper'),
        ('megaevent', 'MegaEvent', 'Multi-viewpoint place recognition with event cameras.', '/papers.html#megaevent', 'megaevent'),
        ('eventgem', 'EventGeM', 'Global-to-local feature matching for event-based place recognition.', '/papers.html#eventgem', 'eventgem'),
        ('lens', 'LENS', 'Energy-efficient robot localisation on embedded neuromorphic hardware.', '/papers.html#lens', 'lens'),
    ]
    items = []
    for id, label, description, url, paper_id in work:
        paper = next(p for p in PAPERS if p['id'] == paper_id)
        items.append(f'<li id="{id}"><a class="work-image" href="{url}" tabindex="-1" aria-hidden="true"><img src="{paper["image"]}" width="200" height="150" alt="" loading="lazy"></a><div><h3><a href="{url}">{label} <span aria-hidden="true">↗</span></a></h3><p>{description}</p></div></li>')
    latest = ''.join(
        f'<li><span class="date">{date_text(n)}</span><div><p>{e(n["text"])}</p>{news_link(n).removeprefix("<br>")}</div></li>'
        for n in NEWS[:2]
    )
    return (ROOT/'templates/home.html').read_text().replace('{{WORK}}', ''.join(items)).replace('{{LATEST}}', latest)

def author_text(text):
    # Preserve complete author lists and emphasise Adam's name.
    for variant in ('Adam D. Hines','Adam D Hines'):
        if variant in text:
            before,after=text.split(variant,1)
            return e(before)+'<strong>'+variant+'</strong>'+e(after)
    return e(text)

def heading(kicker,title,description):
    return f'<header class="page-heading wrap"><span class="eyebrow">{e(kicker)}</span><h1>{e(title)}</h1><p class="lead">{e(description)}</p>'

def publications():
    years=sorted({p['year'] for p in PAPERS},reverse=True)
    body=heading('Research','Publications.','Work on event-based vision, robotic localisation, and efficient perception, alongside earlier research in neuroscience.')
    body+='<nav class="year-nav" aria-label="Publication years">'+''.join(f'<a href="#year-{y}">{y}</a>' for y in years)+'</nav></header><div class="wrap">'
    for y in years:
        body+=f'<section class="year-section" id="year-{y}" aria-labelledby="heading-{y}"><h2 class="year-heading" id="heading-{y}">{y}</h2><div>'
        for p in (p for p in PAPERS if p['year']==y):
            if p['image']:
                alt = p.get('image_alt', 'Figure from ' + p['title'])
                image = f'<a class="paper-image" href="{p["image"]}" aria-label="View figure: {e(p["title"],quote=True)}"><img src="{p["image"]}" width="200" height="150" alt="{e(alt,quote=True)}" loading="lazy"></a>'
            else:
                image = f'<div class="paper-image figure-placeholder" aria-hidden="true"><span>{"Commentary" if p["id"]=="anaesthesia" else "Preprint"}</span></div>'
            badge=f'<span class="badge">{p["status"]}</span>' if p['status']!='Published' else ''
            body+=f'<article class="paper {"" if image else "no-image"}" id="{p["id"]}">{image}<div><p class="meta">{badge}{e(p["venue"])}</p><h3>{e(p["title"])}</h3><p>{author_text(p["authors"])}</p><div class="resource-links">{links(p["links"])}</div></div></article>'
        body+='</div></section>'
    body+='<aside class="reviewing"><h2>Academic service</h2><p>Associate Editor, IROS Conference Paper Review Board (2026). Reviewer for:</p><ul>'+''.join(f'<li>{x}</li>' for x in ['Science Robotics','IEEE Transactions on Robotics','ICRA','ICCV and ECCV','IEEE Robotics and Automation Letters','PLoS ONE','Anesthesiology'])+'</ul></aside></div>'
    return body

def news():
    years=sorted({n['year'] for n in NEWS},reverse=True)
    body=heading('From the lab & beyond','News.','Research, software releases, new chapters, and a few things along the way.')
    body+='<nav class="year-nav" aria-label="News years">'+''.join(f'<a href="#year-{y}">{y}</a>' for y in years)+'</nav></header><div class="wrap">'
    for y in years:
        body+=f'<section class="year-section" id="year-{y}" aria-labelledby="heading-{y}"><h2 class="year-heading" id="heading-{y}">{y}</h2><div>'
        months=defaultdict(list)
        for n in NEWS:
            if n['year']==y: months[n['month']].append(n)
        for month,items in months.items():
            body+=f'<div class="timeline-month"><h3>{e(month or str(y))}</h3><ul>'
            for n in items: body+=f'<li>{e(n["text"])}{news_link(n)}</li>'
            body+='</ul></div>'
        body+='</div></section>'
    return body+'</div>'

def career_items(key):
    return ''.join(f'<article class="career-item"><span class="date">{e(c["date"])}</span><h3>{e(c["title"])}</h3><p>{e(c["organisation"])}</p>'+ (f'<p>{e(c["detail"])}</p>' if c['detail'] else '')+'</article>' for c in CAREER[key])

def cv():
    return heading('Experience & contributions','Curriculum vitae.','Research Fellow at the QUT Centre for Robotics, working on vision-based positioning for Roo-ver, Australia’s first lunar rover, and event-based vision.')+'''<div class="actions"><a class="button" href="/static/CV.pdf" download="Adam-Hines-CV.pdf">Download CV <span aria-hidden="true">↓</span></a><a class="text-link" href="/static/CV.pdf">Open PDF ↗</a></div></header><div class="wrap cv-layout"><div><section class="cv-block"><h2>Research experience</h2>'''+career_items('appointments')+'</section><section class="cv-block"><h2>Education</h2>'+career_items('education')+'''</section></div><div class="cv-card"><span class="eyebrow">Open-source software</span><h2>Building tools others can use.</h2><h3>EventCV</h3><p>Python and Rust tools for event-camera data, representations, feature detection, motion estimation, simulation, and visualisation.</p><div class="actions"><a class="text-link" href="https://eventcv.net/">Explore EventCV ↗</a></div><hr><h3>Event-LAB</h3><p>A common evaluation framework for neuromorphic localisation methods and datasets.</p><div class="actions"><a class="text-link" href="/papers.html#eventlab">Read the paper →</a></div><hr><h3>Teaching &amp; service</h3><p>Engineering capstone supervision, visiting PhD co-supervision, research community leadership, and IROS associate editorship.</p><div class="actions"><a class="text-link" href="/static/CV.pdf">Full experience in the CV →</a></div></div></div><section class="wrap pdf-section" aria-label="PDF curriculum vitae"><h2>Full CV</h2><p><a href="/static/CV.pdf">Open the PDF directly</a> if the preview is unavailable.</p><iframe class="pdf-frame" src="/static/CV.pdf" title="Adam Hines public academic CV" loading="lazy"></iframe></section>'''

def public_cv():
    def listing(key): return '<ul>'+''.join(f'<li>{e(t)}</li>' for t in CAREER[key])+'</ul>'
    sections=''
    # Deliberate page breaks keep the public CV predictable and easy to review.
    sections+='<section class="sheet"><header><p class="kicker">CURRICULUM VITAE · OCTOBER 2026</p><h1>Dr Adam D Hines</h1><p class="role">Research Fellow · QUT Centre for Robotics</p><p><a href="mailto:adam.hines@qut.edu.au">adam.hines@qut.edu.au</a> · <a href="https://adamdhines.github.io/">adamdhines.github.io</a></p><nav>'+links(SOCIALS)+'</nav></header><h2>Research profile</h2><p>'+e(CAREER['summary'])+'</p><h2>Professional experience</h2>'+career_items('appointments')+'<h2>Education</h2>'+career_items('education')+'</section>'
    sections+='<section class="sheet"><h2>Open-source software</h2><h3>EventCV</h3><p>Developer of an open-source event-based computer vision library with a Python interface and Rust core. Work spans recording formats and live cameras, event representations, feature detection, motion estimation, simulation, reconstruction, visualisation, documentation, and developer tooling.</p><p><a href="https://eventcv.net/">eventcv.net</a> · <a href="https://docs.eventcv.net/en/latest/">Documentation</a> · <a href="https://github.com/EventLAB-Team/eventcv">Source code</a></p><h3>Event-LAB</h3><p>Co-author of a framework for standardised evaluation of neuromorphic localisation methods, accepted to ICRA 2026.</p><p><a href="https://arxiv.org/abs/2509.14516">Paper and evaluation framework</a></p><h2>Teaching & supervision</h2>'+listing('teaching')+'<h2>Research funding</h2>'+listing('funding')+'<h2>Honours & awards</h2>'+listing('awards')+'</section>'
    sections+='<section class="sheet"><h2>Leadership, outreach & service</h2>'+listing('service')+'<h2>Presentations & public communication</h2>'+listing('communication')+'<h2>Research collaborations</h2>'+listing('collaborations')+'</section>'
    # Paginate the full bibliography without truncating newly added records.
    for start in range(0, len(PAPERS), 7):
        sections+='<section class="sheet"><h2>Publications'+(' · continued' if start else '')+'</h2>'
        for p in PAPERS[start:start+7]:
            link=p['links'].get('DOI') or next(iter(p['links'].values()))
            sections+=f'<article class="citation"><h3>{e(p["title"])}</h3><p>{author_text(p["authors"])}</p><p>{p["year"]} · {e(p["venue"])} · {p["status"]}</p><p><a href="{e(link,quote=True)}">{e(link.removeprefix("https://"))}</a></p></article>'
        sections+='</section>'
    return '<!DOCTYPE html><html lang="en-AU"><head><meta charset="utf-8"><title>Adam Hines — Public academic CV</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/static/css/cv-print.css"></head><body>'+sections+'</body></html>'

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--check',action='store_true'); args=parser.parse_args()
    outputs={name:page(name,body()) for name,body in [('index.html',home),('papers.html',publications),('news.html',news),('cv.html',cv)]}
    outputs['static/cv-public.html']=public_cv()
    outputs['sitemap.xml']='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{BASE}{"/" if name=="index.html" else "/"+name}</loc><lastmod>{CAREER["updated"]}</lastmod></url>\n' for name in PAGES)+'</urlset>\n'
    stale=[]
    for name,text in outputs.items():
        path=ROOT/name
        if args.check:
            if not path.exists() or path.read_text()!=text: stale.append(name)
        else: path.write_text(text)
    if stale: raise SystemExit('Rebuild required: '+', '.join(stale))
    print('Static outputs '+('are up to date.' if args.check else 'rebuilt.'))

if __name__=='__main__': main()
