#!/usr/bin/env python3
"""Dependency-free structural, content, and local-link checks."""
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlsplit,unquote
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
PAGES=['index.html','papers.html','cv.html','news.html','static/cv-public.html']
class Document(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=[];self.links=[];self.headings=0;self.canonical=[];self.description=[];self.json=[];self.in_json=False;self.active=0;self.missing_alt=0;self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='h1':self.headings+=1
        if a.get('aria-current')=='page':self.active+=1
        if tag=='img' and 'alt' not in a:self.missing_alt+=1
        if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a['href'])
        if tag=='meta' and a.get('name')=='description':self.description.append(a['content'])
        for key in ('href','src'):
            if key in a:self.links.append(a[key])
        self.in_json=tag=='script' and a.get('type')=='application/ld+json'
    def handle_data(self,data):
        if self.in_json:self.json.append(json.loads(data))
    def handle_endtag(self,tag):
        if tag=='script':self.in_json=False

def main():
    subprocess.run([sys.executable,str(ROOT/'scripts/build.py'),'--check'],check=True)
    documents={name:Document((ROOT/name).read_text()) for name in PAGES};errors=[]
    for name,doc in documents.items():
        if len(doc.ids)!=len(set(doc.ids)):errors.append(name+': duplicate IDs')
        if doc.headings!=1 or doc.missing_alt:errors.append(name+': heading or image alternative missing')
        if not name.startswith('static/'):
            expected='https://adamdhines.github.io'+('/' if name=='index.html' else '/'+name)
            if doc.canonical!=[expected] or len(doc.description)!=1 or doc.active!=1 or not doc.json:errors.append(name+': metadata or navigation invalid')
        for link in doc.links:
            u=urlsplit(link)
            if u.scheme or u.netloc:continue
            target=ROOT/unquote(u.path.lstrip('/')) if u.path.startswith('/') else (ROOT/name).parent/unquote(u.path) if u.path else ROOT/name
            if target.is_dir():target=target/'index.html'
            if not target.exists():errors.append(name+': missing '+link);continue
            if u.fragment and target.suffix=='.html':
                parsed=Document(target.read_text())
                if u.fragment not in parsed.ids:errors.append(name+': missing anchor '+link)
    papers=json.loads((ROOT/'data/publications.json').read_text());news=json.loads((ROOT/'data/news.json').read_text())
    original={'lens','threshold','synapses','vprtempo','tracking','cardiac','anaesthesia'}
    if not original.issubset({p['id'] for p in papers}):errors.append('Original publication missing')
    if len(news)<48:errors.append('News archive truncated')
    if len({p['id'] for p in papers})!=len(papers):errors.append('Duplicate publication ID')
    descriptions=[documents[n].description[0] for n in PAGES if not n.startswith('static/')]
    if len(set(descriptions))!=4:errors.append('Duplicate descriptions')
    ET.parse(ROOT/'sitemap.xml')
    print('\n'.join(errors) if errors else f'Passed: {len(PAGES)} documents, local links/anchors, metadata, {len(papers)} publications, {len(news)} news entries.')
    if errors:raise SystemExit(1)

if __name__=='__main__':main()
