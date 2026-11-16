#!/usr/bin/env python3
"""Meaningful local editorial boundary tests, using isolated temporary storage."""
import base64
import copy
import http.client
import json
import re
import shutil
import subprocess
import tempfile
import threading
import unittest
from pathlib import Path
from editorial import demonstration, validate_article, markdown, article_html
from serve import make_server, ROOT
import build

class EditorialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory(prefix='glioniq-editorial-')
        cls.server=make_server(0,cls.tmp.name); cls.port=cls.server.server_port
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        conn=http.client.HTTPConnection('127.0.0.1',cls.port);conn.request('GET','/admin/');response=conn.getresponse();response.read();cls.cookie=response.getheader('Set-Cookie').split(';')[0];conn.close()
    @classmethod
    def tearDownClass(cls): cls.server.shutdown();cls.server.server_close();cls.tmp.cleanup()
    def call(self,method,path,data=None,session=True,origin=True,host=None,raw=None):
        conn=http.client.HTTPConnection('127.0.0.1',self.port)
        headers={'Content-Type':'application/json'}
        if session: headers['Cookie']=self.cookie
        if origin: headers['Origin']=f'http://127.0.0.1:{self.port}'
        if host: headers['Host']=host
        conn.request(method,path,raw if raw is not None else json.dumps(data) if data is not None else None,headers)
        response=conn.getresponse(); result=(response.status,response.read(),dict(response.getheaders()));conn.close();return result
    def test_01_draft_edit_review_conflict_history(self):
        a=demonstration('blog');a['slug']='test-lifecycle'
        status,body,_=self.call('POST','/api/drafts',a);self.assertEqual(status,200)
        a=json.loads(body)['article'];self.assertEqual(a['revision'],1)
        a['title']='Changed locally';a['status']='review'
        status,body,_=self.call('POST','/api/drafts',a);self.assertEqual(status,200)
        self.assertEqual(json.loads(body)['article']['revision'],2)
        self.assertEqual(self.call('POST','/api/drafts',a)[0],409)
        restored=json.loads(self.call('GET','/api/drafts/test-lifecycle')[1]);self.assertEqual(restored['title'],'Changed locally');self.assertEqual(restored['status'],'review')
        self.assertTrue(json.loads(self.call('GET','/api/history')[1])['history'])
    def test_02_no_anonymous_or_cross_origin_writes(self):
        a=demonstration('blog')
        self.assertEqual(self.call('POST','/api/drafts',a,session=False)[0],403)
        self.assertEqual(self.call('POST','/api/drafts',a,origin=False)[0],403)
        self.assertEqual(self.call('POST','/api/drafts',a,host='attacker.example')[0],403)
        self.assertEqual(self.call('GET','/api/drafts',session=False)[0],401)
        self.assertEqual(self.call('POST','/api/publish',a)[0],404)
        a['status']='published';self.assertEqual(self.call('POST','/api/drafts',a)[0],400)
    def test_03_private_files_and_path_traversal(self):
        for path in ('/.git/config','/.local-cms/drafts/test-lifecycle.json','/content/about-us.md','/cms/editor.html','/assets/../content/about-us.md','/assets/%2e%2e/content/about-us.md'):
            self.assertEqual(self.call('GET',path)[0],404,path)
    def test_04_safe_rendering_and_validation(self):
        a=demonstration('science');a['title']='<script>alert(1)</script>';a['body']='<script>alert(1)</script>\n\n## Safe **heading**\n\nAn *idea* and [source](https://example.com).'
        html=article_html(a,True);self.assertNotIn('<script>',html);self.assertIn('&lt;script&gt;',html);self.assertIn('<strong>heading</strong>',html)
        for url in ('javascript:alert','data:text/html,x','//attacker.example','https://x/"onerror=alert','/a/../b'):
            a['body']=f'[unsafe]({url})'
            with self.assertRaises(ValueError,msg=url): validate_article(a)
        a=demonstration('blog');a['slug']='../../about-us'
        with self.assertRaises(ValueError):validate_article(a)
        a=demonstration('blog');a['references']=[{'title':'Invented by test only','url':'javascript:alert'}]
        with self.assertRaises(ValueError):validate_article(a)
    def test_05_upload_restrictions_and_pdf_download(self):
        for name,blob in [('x.svg',b'<svg/>'),('x.html',b'<script/>'),('x.png',b'not-an-image')]:
            self.assertEqual(self.call('POST','/api/upload',{'name':name,'data':base64.b64encode(blob).decode()})[0],400)
        blob=b'%PDF-1.7\n%local test fixture\n%%EOF';status,body,_=self.call('POST','/api/upload',{'name':'fixture.pdf','data':base64.b64encode(blob).decode()});self.assertEqual(status,200)
        url=json.loads(body)['url'];self.assertEqual(self.call('GET',url,session=False)[0],401)
        code,data,headers=self.call('GET',url);self.assertEqual(data,blob);self.assertIn('attachment;',headers['Content-Disposition']);self.assertEqual(headers['X-Content-Type-Options'],'nosniff')
        image=(ROOT/'favicon-32x32.png').read_bytes()
        status,body,_=self.call('POST','/api/upload',{'name':'local-fixture.png','data':base64.b64encode(image).decode()});self.assertEqual(status,200)
        image_url=json.loads(body)['url'];self.assertEqual(self.call('GET',image_url)[1],image)
        article=demonstration('blog');article['featured_image']=image_url;article['featured_caption']='Local fixture caption';article['body']=f'![Local image]({image_url} "Image caption")'
        code,body,_=self.call('POST','/api/preview',article);self.assertEqual(code,200);self.assertIn(b'<figcaption>Image caption</figcaption>',body)
        article['status']='published';article['publication_date']='2026-11-16'
        with self.assertRaises(ValueError):validate_article(article,True)
        big=b'%PDF-'+b'0'*(5*1024*1024)
        self.assertEqual(self.call('POST','/api/upload',{'name':'large.pdf','data':base64.b64encode(big).decode()})[0],413)
    def test_06_preview_templates(self):
        for destination in ('blog','science'):
            a=demonstration(destination);code,body,headers=self.call('POST','/api/preview',a);self.assertEqual(code,200);self.assertIn(b'LOCAL PREVIEW',body);self.assertIn(b'GlionIQ',body);self.assertIn("script-src 'self'",headers['Content-Security-Policy'])
    def test_07_build_index_and_unpublish_in_isolated_copy(self):
        with tempfile.TemporaryDirectory(prefix='glioniq-build-') as folder:
            dest=Path(folder);shutil.copytree(ROOT/'content',dest/'content');(dest/'assets').mkdir()
            a=demonstration('science');a['slug']='fixture-only';a['status']='published';a['publication_date']='2026-11-16'
            source=dest/'content/editorial/fixture.json';source.write_text(json.dumps(a));old_root=build.ROOT
            try:
                build.ROOT=dest;build.build()
                self.assertTrue((dest/'science/fixture-only/index.html').is_file());self.assertIn('/science/fixture-only/',(dest/'assets/search-index.json').read_text());self.assertIn('Your next story',(dest/'science/index.html').read_text())
                a['status']='draft';source.write_text(json.dumps(a));build.build()
                self.assertFalse((dest/'science/fixture-only/index.html').exists());self.assertNotIn('/science/fixture-only/',(dest/'assets/search-index.json').read_text())
                self.assertEqual((dest/'about-us/index.html').read_bytes(),(ROOT/'about-us/index.html').read_bytes())
            finally:build.ROOT=old_root
    def test_08_hero_and_protected_assets(self):
        original=subprocess.check_output(['git','show','903d901:index.html'],cwd=ROOT).decode();now=(ROOT/'index.html').read_text()
        pattern=r'<section class="corporate-hero">.*?</section>'
        self.assertEqual(re.search(pattern,original,re.S)[0],re.search(pattern,now,re.S)[0])
        css=subprocess.check_output(['git','show','903d901:assets/site.css'],cwd=ROOT).decode();self.assertTrue((ROOT/'assets/site.css').read_text().startswith(css))
        for name in ('CNAME','content/about-us.md','public/images/development/trampolina.webp','public/images/development/dr-quiz.webp','public/images/development/neuropath.webp'):
            self.assertEqual((ROOT/name).read_bytes(),subprocess.check_output(['git','show','903d901:'+name],cwd=ROOT))

if __name__=='__main__':unittest.main(verbosity=2)
