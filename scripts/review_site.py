#!/usr/bin/env python3
"""Browser checks and screenshots. Requires the optional review dependencies."""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--base-url',default='http://127.0.0.1:8765')
    parser.add_argument('--chrome',default='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    parser.add_argument('--output',default='/tmp/adam-site-review')
    args=parser.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    errors=[];checks=0
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=args.chrome,headless=True)
        context=browser.new_context(java_script_enabled=False,reduced_motion='reduce')
        page=context.new_page()
        page.on('pageerror',lambda err:errors.append(str(err)))
        page.on('response',lambda r:errors.append(f'HTTP {r.status}: {r.url}') if r.status>=400 else None)
        for path in ['','papers.html','news.html','cv.html']:
            for width in (375,768,1440):
                page.set_viewport_size({'width':width,'height':1000})
                page.goto(args.base_url+'/'+path)
                page.evaluate('document.fonts.ready')
                # Scroll each image into view so lazy loading is tested, not mistaken for failure.
                for img in page.locator('img').all():
                    img.scroll_into_view_if_needed()
                    img.evaluate('(i)=>i.decode()')
                page.evaluate('window.scrollTo(0,0)')
                if page.evaluate('document.documentElement.scrollWidth>innerWidth'): errors.append(f'Overflow: {path} at {width}')
                if page.locator('h1').count()!=1: errors.append(f'Heading: {path}')
                if page.locator('[aria-current="page"]').count()!=1: errors.append(f'Active navigation: {path}')
                page.screenshot(path=str(out/f'{path or "home"}-{width}.png'),full_page=True)
                checks+=1
            # Browser zoom shrinks the CSS viewport; exercise equivalent 200% reflow.
            page.set_viewport_size({'width':720,'height':500})
            if page.evaluate('document.documentElement.scrollWidth>innerWidth'): errors.append(f'200% reflow: {path}')
            page.reload();page.keyboard.press('Tab')
            if page.locator(':focus').inner_text()!='Skip to content': errors.append(f'Skip link: {path}')
            page.keyboard.press('Enter')
            if page.evaluate('location.hash')!='#main': errors.append(f'Skip target: {path}')
        context.close()
        # Force system-font fallbacks to confirm reflow without downloaded fonts.
        context=browser.new_context(viewport={'width':375,'height':900})
        context.route('**/*.ttf',lambda route:route.abort())
        context.route('**/*.woff2',lambda route:route.abort())
        page=context.new_page()
        for path in ['','papers.html','news.html','cv.html']:
            page.goto(args.base_url+'/'+path)
            if page.evaluate('document.documentElement.scrollWidth>innerWidth'): errors.append(f'Font fallback overflow: {path}')
        browser.close()
    print(json.dumps({'responsive_views':checks,'javascript':'disabled','font_fallback':'checked','keyboard_skip_links':'checked','errors':errors,'screenshots':str(out)},indent=2))
    if errors: raise SystemExit(1)

if __name__=='__main__': main()
