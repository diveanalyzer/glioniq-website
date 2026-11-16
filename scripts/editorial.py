"""Validated editorial JSON and deliberately limited, HTML-free Markdown rendering."""
import json
import re
from datetime import date
from html import escape as e
from pathlib import Path
from urllib.parse import urlsplit, unquote

SLUG = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
TEXT_FIELDS = {'title':180,'subtitle':300,'summary':800,'body':100000,'category':100,'author':160,'publication_date':10,'updated_date':10,'featured_image':500,'featured_caption':500,'seo_title':180,'seo_description':300}
MEDIA = re.compile(r'/(?:public/editorial|local-media)/[a-zA-Z0-9_/-]+\.(?:png|jpg|jpeg|webp|pdf)\Z', re.I)


def safe_url(value, media=False):
    if not isinstance(value,str) or not value or len(value)>2000 or re.search(r'[\x00-\x20\\<>"\']',value):
        return False
    if '..' in unquote(value).split('/') or '%' in value:
        return False
    if media:
        return bool(MEDIA.fullmatch(value))
    u=urlsplit(value)
    return (u.scheme in ('https','http') and bool(u.netloc) and not u.username and not u.password) or (value.startswith('/') and not value.startswith('//') and not u.scheme)


def validate_article(source, allow_published=False):
    if not isinstance(source,dict): raise ValueError('Article must be an object.')
    if set(source)-set(TEXT_FIELDS)-{'slug','destination','status','tags','references','attachments','revision'}: raise ValueError('Unknown article field.')
    a={}
    for key,limit in TEXT_FIELDS.items():
        value=source.get(key,'')
        if not isinstance(value,str) or len(value)>limit: raise ValueError(f'{key}: maximum {limit} characters.')
        a[key]=value.strip()
    if not all(a[k] for k in ('title','summary','body','author')): raise ValueError('Title, summary, content and author are required.')
    slug=source.get('slug','')
    if not isinstance(slug,str) or len(slug)>90 or not SLUG.fullmatch(slug): raise ValueError('Use a short slug with lowercase letters, numbers and hyphens.')
    a['slug']=slug
    a['destination']=source.get('destination')
    if a['destination'] not in ('blog','science'): raise ValueError('Choose Blog or Science.')
    a['status']=source.get('status','draft')
    if a['status'] not in (('draft','review','published') if allow_published else ('draft','review')): raise ValueError('Public publishing is disabled in local mode.')
    for key in ('publication_date','updated_date'):
        if a[key]:
            try: date.fromisoformat(a[key])
            except ValueError: raise ValueError(f'{key}: use YYYY-MM-DD.')
    if a['status']=='published' and not a['publication_date']: raise ValueError('Publication date is required.')
    if a['status']=='published' and '/local-media/' in json.dumps(source): raise ValueError('Promote local media to reviewed public editorial assets before publication.')
    tags=source.get('tags',[])
    if not isinstance(tags,list) or len(tags)>20 or any(not isinstance(t,str) or len(t)>60 for t in tags): raise ValueError('Use up to 20 short tags.')
    a['tags']=tags
    if a['featured_image'] and (not safe_url(a['featured_image'],True) or a['featured_image'].lower().endswith('.pdf')): raise ValueError('Choose an uploaded PNG, JPEG or WebP featured image.')
    a['references']=source.get('references',[])
    if not isinstance(a['references'],list) or len(a['references'])>50: raise ValueError('Too many references.')
    for ref in a['references']:
        if not isinstance(ref,dict) or set(ref)-{'title','authors','publisher','year','url','doi','pdf'}: raise ValueError('Invalid reference fields.')
        if any(not isinstance(v,str) or len(v)>1000 for v in ref.values()) or not ref.get('title'): raise ValueError('Each reference needs a title.')
        if ref.get('year') and not re.fullmatch(r'\d{4}',ref['year']): raise ValueError('Reference year must have four digits.')
        if ref.get('url') and not (safe_url(ref['url']) and ref['url'].startswith(('https://','http://'))): raise ValueError('Invalid reference source URL.')
        if ref.get('doi') and not re.fullmatch(r'10\.\d{4,9}/[a-zA-Z0-9._;()/:-]+',ref['doi']): raise ValueError('Enter a DOI such as 10.1234/example.')
        if ref.get('pdf') and not (safe_url(ref['pdf'],True) and ref['pdf'].endswith('.pdf')): raise ValueError('Choose an uploaded PDF.')
    a['attachments']=source.get('attachments',[])
    if not isinstance(a['attachments'],list) or len(a['attachments'])>20: raise ValueError('Too many attachments.')
    for item in a['attachments']:
        if not isinstance(item,dict) or set(item)!={'title','url'} or not isinstance(item['title'],str) or not 0<len(item['title'])<200 or not safe_url(item['url'],True) or not item['url'].endswith('.pdf'): raise ValueError('Attachments must be named uploaded PDFs.')
    # Render validation rejects unsafe destinations even when the draft is not published.
    markdown(a['body'])
    return a


def inline(text):
    tokens=[]
    def link(m):
        image,label,url,caption=m.groups()
        if not safe_url(url,bool(image)): raise ValueError('Unsafe link or image destination in content.')
        if image:
            if url.endswith('.pdf'): raise ValueError('PDFs must be links, not images.')
            html=f'<figure><img src="{e(url)}" alt="{e(label)}" width="960" height="640" loading="lazy">'+(f'<figcaption>{e(caption)}</figcaption>' if caption else '')+'</figure>'
        else: html=f'<a href="{e(url)}" rel="noopener noreferrer">{e(label)}</a>'
        tokens.append(html); return f'\x00{len(tokens)-1}\x00'
    # Reject token delimiters from input; no raw HTML is ever emitted.
    text=text.replace('\x00','')
    text=re.sub(r'(!?)\[([^\]\n]*)\]\(([^\s)]+)(?: "([^"\n]*)")?\)',link,text)
    text=e(text)
    text=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',text)
    text=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<em>\1</em>',text)
    return re.sub(r'\x00(\d+)\x00',lambda m:tokens[int(m[1])],text)


def markdown(body):
    output=[]
    for block in re.split(r'\n\s*\n',body.strip()):
        lines=block.splitlines()
        if not lines: continue
        heading=re.fullmatch(r'(#{1,6}) (.+)',block)
        if heading:
            level=max(2,len(heading[1])); output.append(f'<h{level}>{inline(heading[2])}</h{level}>')
        elif all(re.match(r'^[-*] ',line) for line in lines): output.append('<ul>'+''.join('<li>'+inline(line[2:])+'</li>' for line in lines)+'</ul>')
        elif re.fullmatch(r'!\[.*\]\(.*\)',block): output.append(inline(block))
        else:
            if re.search(r'!\[',block): raise ValueError('Place each image on its own line, separated by blank lines.')
            output.append('<p>'+inline(' '.join(lines))+'</p>')
    return '\n'.join(output)


def article_html(article, preview=False):
    a=validate_article(article,True)
    dest='Blog & Insights' if a['destination']=='blog' else 'Science & Research'
    banner='<aside class="preview-banner">LOCAL PREVIEW · Not published</aside>' if preview else ''
    featured=f'<figure class="article-feature"><img src="{e(a["featured_image"])}" width="960" height="640" alt="{e(a["featured_caption"] or a["title"])}"><figcaption>{e(a["featured_caption"])}</figcaption></figure>' if a['featured_image'] else ''
    refs=''
    for ref in a['references']:
        title=f'<a href="{e(ref["url"])}">{e(ref["title"])}</a>' if ref.get('url') else e(ref['title'])
        meta=' · '.join(e(ref[k]) for k in ('authors','publisher','year') if ref.get(k))
        doi=f' · <a href="https://doi.org/{e(ref["doi"])}">DOI: {e(ref["doi"])}</a>' if ref.get('doi') else ''
        pdf=f' · <a href="{e(ref["pdf"])}" download>PDF attachment</a>' if ref.get('pdf') else ''
        refs+=f'<li>{title}<br><span>{meta}</span>{doi}{pdf}</li>'
    references=f'<section class="article-references"><h2>Research references</h2><ol>{refs}</ol><p>These sources provide context. A reference does not establish the effectiveness of a GlionIQ product.</p></section>' if refs else ''
    attachments=''.join(f'<li><a href="{e(item["url"])}" download>{e(item["title"])}</a></li>' for item in a['attachments'])
    attachment_section=f'<section><h2>Attachments</h2><ul>{attachments}</ul></section>' if attachments else ''
    dates=(f' · <time datetime="{a["publication_date"]}">{a["publication_date"]}</time>' if a['publication_date'] else ' · Publication date pending')+(f' · Updated {a["updated_date"]}' if a['updated_date'] else '')
    return f'''<article class="content-page article-page editorial">{banner}<a class="breadcrumb" href="/{a['destination']}/">← {dest}</a><p class="kicker">{e(a['category'])}</p><h1>{e(a['title'])}</h1><p class="article-subtitle">{e(a['subtitle'])}</p><p class="article-byline">{e(a['author'])}{dates}</p><p class="lead">{e(a['summary'])}</p>{featured}<div class="article-body">{markdown(a['body'])}</div>{references}{attachment_section}<p class="article-tags">{' · '.join(e(t) for t in a['tags'])}</p></article>'''


def load_articles(folder):
    articles=[]; seen=set()
    for path in sorted(Path(folder).glob('*.json')):
        a=validate_article(json.loads(path.read_text()),True)
        if a['status']!='published': continue
        identity=(a['destination'],a['slug'])
        if identity in seen: raise ValueError('Duplicate article route.')
        seen.add(identity); articles.append(a)
    return sorted(articles,key=lambda a:a['publication_date'],reverse=True)


def listing_html(articles,destination):
    title='Blog & Insights' if destination=='blog' else 'Science & Research'
    cards=''.join(f'<article class="search-result"><p class="kicker">{e(a["category"])}</p><h2><a href="/{destination}/{a["slug"]}/">{e(a["title"])}</a></h2><p>{e(a["summary"])}</p><p>{e(a["author"])} · {a["publication_date"]}</p></article>' for a in articles)
    return f'<section class="content-page"><a class="breadcrumb" href="/">← Home</a><h1>{title}</h1>{cards}</section>'


def demonstration(destination):
    return {'slug':'local-template-preview','title':'Your next story begins here','subtitle':'A GlionIQ article template','summary':'This local demonstration shows the reading layout. It is not a published article or a scientific claim.','body':'## Ideas with room to breathe\n\nPaste your article as Markdown, or paste formatted text into the editor. The template keeps **emphasis**, *italics* and headings consistent with GlionIQ.\n\n## A considered reading experience\n\nClear paragraphs, thoughtful images and traceable references help readers follow your ideas.\n\n- Separate evidence from interpretation.\n- Describe uncertainty clearly.\n- Review every source before publication.','author':'Local template demonstration','category':'Template preview','destination':destination,'status':'draft','tags':['Local preview'],'references':[],'attachments':[]}
