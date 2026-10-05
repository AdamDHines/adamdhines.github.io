#!/usr/bin/env python3
"""Render the already-sanitised public HTML CV. Never reads the private DOCX."""
import argparse
from pathlib import Path
import tempfile
import fitz
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--base-url',default='http://127.0.0.1:8765')
    parser.add_argument('--chrome',default='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    args=parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='public-cv-') as temp:
        raw=Path(temp)/'cv.pdf'
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path=args.chrome,headless=True)
            page=browser.new_page()
            response=page.goto(args.base_url+'/static/cv-public.html')
            if not response or response.status!=200: raise RuntimeError('Public CV HTML is unavailable')
            page.evaluate('document.fonts.ready')
            page.pdf(path=str(raw),format='A4',print_background=True,prefer_css_page_size=True,display_header_footer=True,header_template='<span></span>',footer_template='<div style="width:100%;font-size:8px;color:#566157;text-align:center">Adam Hines · Public academic CV &nbsp; | &nbsp; <span class="pageNumber"></span> / <span class="totalPages"></span></div>')
            browser.close()
        with fitz.open(raw) as pdf:
            pdf.set_metadata({**{key: '' for key in ('subject', 'keywords', 'creator', 'producer', 'creationDate', 'modDate', 'trapped')}, 'title':'Adam Hines — Public academic CV','author':'Adam Hines'})
            pdf.del_xml_metadata()
            pdf.save(ROOT/'static/CV.pdf',garbage=4,deflate=True)
            print(f'Rendered {len(pdf)} pages to static/CV.pdf; private source never loaded.')

if __name__=='__main__': main()
