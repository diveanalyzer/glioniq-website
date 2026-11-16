#!/usr/bin/env python3
"""Loopback-only owner preview. No Git operations, OAuth, role claims or publish API."""
import argparse
import base64
import hashlib
import json
import mimetypes
import re
import secrets
import threading
from datetime import datetime, timezone
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, unquote
from editorial import validate_article, article_html, demonstration
import build

ROOT=Path(__file__).resolve().parents[1]
MAX_REQUEST=8*1024*1024
MAX_UPLOAD=5*1024*1024
CSP="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'self'; form-action 'self'"


def preview_document(article):
    return (re.sub(r'<script[^>]+></script>', '', build.head('Local article preview — GlionIQ','Unpublished local editorial preview.','', '/'))+'<body class="information-page">'+build.header('/','')+'<main id="main">'+article_html(article,True)+'</main>'+build.footer()+'</body></html>').encode()


def make_server(port=8787,storage=None):
    storage=Path(storage) if storage else ROOT/'.local-cms'
    sessions=set(); lock=threading.Lock()
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,fmt,*args):
            # Do not print cookies, bodies, draft titles or tokens.
            if args and isinstance(args[0],str): print(args[0].split('?')[0], flush=True)
        def send(self,code,body=b'',kind='application/json',cookie=None,download=None):
            self.send_response(code); self.send_header('Content-Type',kind); self.send_header('Content-Length',str(len(body)))
            self.send_header('X-Content-Type-Options','nosniff'); self.send_header('Referrer-Policy','no-referrer'); self.send_header('Cache-Control','no-store')
            self.send_header('Content-Security-Policy', CSP if not self.path.startswith('/scripts/') else CSP.replace("script-src 'self'","script-src 'self' 'unsafe-inline'").replace("style-src 'self'","style-src 'self' 'unsafe-inline'"))
            if cookie: self.send_header('Set-Cookie',f'glioniq_local={cookie}; HttpOnly; SameSite=Strict; Path=/')
            if download: self.send_header('Content-Disposition',f'attachment; filename="{download}"')
            self.end_headers()
            if self.command!='HEAD': self.wfile.write(body)
        def json(self,code,value): self.send(code,json.dumps(value,ensure_ascii=False).encode())
        def host_ok(self):
            return self.headers.get('Host') in (f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}') and self.client_address[0]=='127.0.0.1'
        def authenticated(self):
            try: cookie=SimpleCookie(self.headers.get('Cookie','')); token=cookie.get('glioniq_local'); return token is not None and token.value in sessions
            except Exception: return False
        def same_origin(self):
            return self.headers.get('Origin')==f'http://{self.headers.get("Host")}' and self.headers.get('Sec-Fetch-Site','same-origin') not in ('cross-site','same-site')
        def do_HEAD(self): self.do_GET()
        def do_GET(self):
            if not self.host_ok(): return self.json(403,{'error':'Loopback host required.'})
            path=unquote(urlsplit(self.path).path)
            if '..' in path.split('/') or '\\' in path: return self.json(404,{'error':'Invalid path.'})
            if path=='/admin/':
                if self.headers.get('Sec-Fetch-Site') in ('cross-site','same-site'): return self.json(403,{'error':'Open the local editor directly.'})
                token=secrets.token_urlsafe(32); sessions.add(token)
                return self.send(200,(ROOT/'cms/editor.html').read_bytes(),'text/html; charset=utf-8',cookie=token)
            if path in ('/admin/editor.js','/admin/editor.css'):
                target=ROOT/'cms'/Path(path).name
                return self.send(200,target.read_bytes(),mimetypes.guess_type(str(target))[0])
            if path.startswith('/api/'):
                if not self.authenticated(): return self.json(401,{'error':'Open /admin/ in this browser first.'})
                if path=='/api/drafts':
                    drafts=[]
                    for target in sorted((storage/'drafts').glob('*.json')):
                        a=json.loads(target.read_text()); drafts.append({'slug':a['slug'],'title':a['title'],'status':a['status'],'destination':a['destination'],'revision':a['revision']})
                    return self.json(200,{'drafts':drafts})
                m=re.fullmatch(r'/api/drafts/([a-z0-9-]+)',path)
                if m:
                    target=storage/'drafts'/(m[1]+'.json')
                    if target.is_file(): return self.send(200,target.read_bytes())
                    return self.json(404,{'error':'Draft not found.'})
                if path=='/api/history':
                    files=sorted((storage/'history').glob('*.json'),reverse=True)
                    return self.json(200,{'history':[f.name for f in files[:100]]})
                return self.json(404,{'error':'No such endpoint. Public publishing is disabled.'})
            if path.startswith('/preview/'):
                if not self.authenticated(): return self.json(401,{'error':'Open the local editor first.'})
                if path in ('/preview/blog/','/preview/science/'):
                    return self.send(200,preview_document(demonstration(path.split('/')[2])),'text/html; charset=utf-8')
                return self.json(404,{'error':'Preview not found.'})
            if path.startswith('/local-media/'):
                if not self.authenticated(): return self.json(401,{'error':'Local media requires an editor session.'})
                name=path.removeprefix('/local-media/')
                if not re.fullmatch(r'[a-f0-9]{32}\.(png|jpg|webp|pdf)',name): return self.json(404,{'error':'Media not found.'})
                target=storage/'media'/name
                if not target.is_file(): return self.json(404,{'error':'Media not found.'})
                return self.send(200,target.read_bytes(),mimetypes.guess_type(name)[0],download=name if name.endswith('.pdf') else None)
            # Serve an explicit public surface, never arbitrary repository files.
            if path in ('/','/CNAME','/site.webmanifest','/favicon.ico','/apple-touch-icon.png') or re.fullmatch(r'/(?:favicon-\d+x\d+|icon-\d+)\.png',path) or path.startswith(('/assets/','/public/images/','/public/editorial/')) or path=='/scripts/responsive-qa.html' or path=='/scripts/phase2-qa.html':
                target=ROOT/path.lstrip('/')
            elif path.endswith('/') and path.startswith(('/laboratories/','/about-us/','/blog/','/science/','/contact/','/journey/','/search/')): target=ROOT/path.lstrip('/')/'index.html'
            else: return self.json(404,{'error':'Not a public preview route.'})
            if path=='/': target=ROOT/'index.html'
            target=target.resolve()
            if not target.is_relative_to(ROOT) or not target.is_file() or any(p.startswith('.') for p in target.relative_to(ROOT).parts): return self.json(404,{'error':'Not found.'})
            kind=mimetypes.guess_type(str(target))[0] or 'application/octet-stream'
            return self.send(200,target.read_bytes(),kind)
        def do_POST(self):
            if not self.host_ok() or not self.authenticated() or not self.same_origin(): return self.json(403,{'error':'Local editor session and same-origin request required.'})
            if self.headers.get('Content-Type','').split(';')[0]!='application/json': return self.json(415,{'error':'JSON required.'})
            try: size=int(self.headers.get('Content-Length','0'))
            except ValueError: return self.json(400,{'error':'Invalid length.'})
            if not 0<size<=MAX_REQUEST: return self.json(413,{'error':'Request too large.'})
            try:
                source=json.loads(self.rfile.read(size)); path=urlsplit(self.path).path
                if path=='/api/preview':
                    a=validate_article(source)
                    return self.send(200,preview_document(a),'text/html; charset=utf-8')
                if path=='/api/drafts':
                    a=validate_article(source)
                    with lock:
                        folder=storage/'drafts'; folder.mkdir(parents=True,exist_ok=True)
                        target=folder/(a['slug']+'.json')
                        current=json.loads(target.read_text()) if target.exists() else None
                        revision=current['revision'] if current else 0
                        if source.get('revision',0)!=revision: return self.json(409,{'error':'This draft changed in another tab. Reload it before saving.'})
                        if current:
                            history=storage/'history'; history.mkdir(exist_ok=True)
                            (history/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')+'-'+a['slug']+'.json')).write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n')
                        a['revision']=revision+1
                        temp=target.with_suffix('.tmp'); temp.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n'); temp.replace(target)
                    return self.json(200,{'article':a,'message':'Saved locally. Nothing published.'})
                if path=='/api/upload':
                    if not isinstance(source,dict) or set(source)!={'name','data'} or not isinstance(source['name'],str): raise ValueError('Invalid upload.')
                    suffix=Path(source['name']).suffix.lower()
                    if suffix not in ('.png','.jpg','.jpeg','.webp','.pdf'): raise ValueError('Only PNG, JPEG, WebP and PDF files are allowed.')
                    blob=base64.b64decode(source['data'],validate=True)
                    if not 0<len(blob)<=MAX_UPLOAD: return self.json(413,{'error':'Files must be 5 MB or smaller.'})
                    valid=(suffix=='.png' and blob.startswith(b'\x89PNG\r\n\x1a\n')) or (suffix in ('.jpg','.jpeg') and blob.startswith(b'\xff\xd8\xff')) or (suffix=='.webp' and blob[:4]==b'RIFF' and blob[8:12]==b'WEBP') or (suffix=='.pdf' and blob.startswith(b'%PDF-'))
                    if not valid: raise ValueError('File contents do not match the permitted format.')
                    folder=storage/'media'; folder.mkdir(parents=True,exist_ok=True)
                    name=secrets.token_hex(16)+('.jpg' if suffix=='.jpeg' else suffix)
                    (folder/name).write_bytes(blob)
                    return self.json(200,{'url':'/local-media/'+name,'name':source['name']})
                return self.json(404,{'error':'Public publishing is disabled. No such endpoint.'})
            except (ValueError,TypeError,KeyError) as exc: return self.json(400,{'error':str(exc)})
    return ThreadingHTTPServer(('127.0.0.1',port),Handler)


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--port',type=int,default=8787); args=parser.parse_args()
    server=make_server(args.port)
    print(f'Local preview: http://127.0.0.1:{server.server_port}/\nLocal editor: http://127.0.0.1:{server.server_port}/admin/\nLoopback only. Publishing disabled.',flush=True)
    server.serve_forever()
