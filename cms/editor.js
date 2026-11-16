'use strict';
const form=document.querySelector('#article-form'), statusLine=document.querySelector('#editor-status');
let revision=0, currentSlug='', dirty=false, attachments=[];
const say=message=>{statusLine.textContent=message;};
const field=name=>form.elements.namedItem(name);
form.addEventListener('input',()=>{dirty=true;});
window.addEventListener('beforeunload',event=>{if(dirty){event.preventDefault();event.returnValue='';}});
async function api(path,body){
  const response=await fetch(path,body===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
  if(!response.ok){let error;try{error=(await response.json()).error;}catch(_){error='Request failed.';}throw new Error(error);}
  return response;
}
function article(){
  const a=Object.fromEntries(new FormData(form));
  a.tags=a.tags.split(',').map(s=>s.trim()).filter(Boolean);a.status='draft';a.revision=a.slug===currentSlug?revision:0;
  a.references=[...document.querySelectorAll('.reference-row')].map(row=>Object.fromEntries([...row.querySelectorAll('input')].map(input=>[input.dataset.field,input.value.trim()])));
  a.attachments=attachments; return a;
}
function reference(ref={}){
 const box=document.createElement('fieldset');box.className='reference-row';const legend=document.createElement('legend');legend.textContent='Research reference';box.append(legend);
 for(const [key,title] of Object.entries({title:'Study title',authors:'Authors',publisher:'Journal or publisher',year:'Year',url:'Source URL',doi:'DOI',pdf:'Uploaded PDF path (optional)'})){
  const label=document.createElement('label');label.textContent=title;const input=document.createElement('input');input.dataset.field=key;input.value=ref[key]||'';input.maxLength=1000;label.append(input);box.append(label);
 }
 const remove=document.createElement('button');remove.type='button';remove.textContent='Remove reference';remove.onclick=()=>{box.remove();dirty=true;};box.append(remove);document.querySelector('#reference-list').append(box);
}
document.querySelector('#add-reference').onclick=()=>{reference();dirty=true;};
function renderAttachments(){
 const area=document.querySelector('#attachment-list');area.replaceChildren();
 attachments.forEach((attachment,index)=>{const row=document.createElement('div');row.className='media-item';const label=document.createElement('label');label.textContent='PDF attachment title';const input=document.createElement('input');input.value=attachment.title;input.oninput=()=>{attachment.title=input.value;dirty=true;};label.append(input);const remove=document.createElement('button');remove.type='button';remove.textContent='Remove attachment';remove.onclick=()=>{attachments.splice(index,1);renderAttachments();dirty=true;};row.append(label,remove);area.append(row);});
}
async function refresh(){
 const data=await (await api('/api/drafts')).json();const list=document.querySelector('#draft-list');list.replaceChildren();
 data.drafts.forEach(draft=>{const button=document.createElement('button');button.className='draft-button';button.type='button';button.textContent=draft.title;const small=document.createElement('small');small.textContent=`${draft.destination} · ${draft.status} · version ${draft.revision}`;button.append(small);button.onclick=()=>loadDraft(draft.slug);list.append(button);});
 const history=await (await api('/api/history')).json();const h=document.querySelector('#history-list');h.replaceChildren();history.history.forEach(name=>{const li=document.createElement('li');li.textContent=name;h.append(li);});
}
function fill(a){
 form.reset();document.querySelector('#reference-list').replaceChildren();
 for(const [key,value] of Object.entries(a)){const control=field(key);if(control)control.value=key==='tags'?value.join(', '):value;}
 (a.references||[]).forEach(reference);attachments=a.attachments||[];renderAttachments();revision=a.revision||0;currentSlug=a.slug||'';dirty=false;document.querySelector('#preview-section').hidden=true;
}
async function loadDraft(slug){
 if(dirty&&!confirm('Discard unsaved edits and open this draft?'))return;
 try{const a=await(await api('/api/drafts/'+encodeURIComponent(slug))).json();fill(a);say(`Opened local ${a.status}: ${a.title}. Version ${a.revision}.`);}catch(error){say(error.message);}
}
document.querySelector('#new-article').onclick=()=>{if(dirty&&!confirm('Discard unsaved edits and start a new article?'))return;fill({tags:[]});say('New local article.');field('title').focus();};
field('title').addEventListener('input',()=>{if(!currentSlug)field('slug').value=field('title').value.toLowerCase().normalize('NFKD').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,90);});
async function save(state){
 if(!form.reportValidity())return;
 const buttons=[...document.querySelectorAll('.editor-actions button')];buttons.forEach(b=>b.disabled=true);
 try{const a=article();a.status=state;const data=await(await api('/api/drafts',a)).json();revision=data.article.revision;currentSlug=data.article.slug;dirty=false;say(`${state==='review'?'Marked for owner review':'Draft saved'} locally · version ${revision}. Nothing published.`);await refresh();}catch(error){say(error.message);}finally{buttons.forEach(b=>b.disabled=false);}
}
form.onsubmit=event=>{event.preventDefault();save('draft');};document.querySelector('#review-article').onclick=()=>save('review');
document.querySelector('#preview-article').onclick=async()=>{if(!form.reportValidity())return;try{const response=await api('/api/preview',article());document.querySelector('#article-preview').srcdoc=await response.text();document.querySelector('#preview-section').hidden=false;say('Preview ready. This article has not been published.');document.querySelector('#preview-section').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});}catch(error){say(error.message);}};
document.querySelector('#export-article').onclick=()=>{if(!form.reportValidity())return;const a=article();delete a.revision;const url=URL.createObjectURL(new Blob([JSON.stringify(a,null,2)+'\n'],{type:'application/json'}));const link=document.createElement('a');link.href=url;link.download=a.slug+'.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);say('Draft exported for backup. No publication performed.');};
const body=field('body');
function insert(text){body.setRangeText(text,body.selectionStart,body.selectionEnd,'end');body.focus();dirty=true;}
document.querySelectorAll('[data-format]').forEach(button=>button.onclick=()=>{const selection=body.value.slice(body.selectionStart,body.selectionEnd)||'Your text';const formats={heading:'\n\n## '+selection+'\n\n',bold:'**'+selection+'**',italic:'*'+selection+'*',link:'['+selection+'](https://example.com)',list:'\n\n- '+selection+'\n\n'};insert(formats[button.dataset.format]);});
body.addEventListener('paste',event=>{
 const html=event.clipboardData.getData('text/html');if(!html)return;
 const doc=new DOMParser().parseFromString(html,'text/html');
 function convert(node){if(node.nodeType===Node.TEXT_NODE)return node.textContent;if(node.nodeType!==Node.ELEMENT_NODE)return '';const tag=node.tagName.toLowerCase();if(['script','style','iframe','object','img'].includes(tag))return '';const text=[...node.childNodes].map(convert).join('');if(/^h[1-6]$/.test(tag))return '\n\n'+'#'.repeat(Math.max(2,Number(tag[1])))+' '+text.trim()+'\n\n';if(['p','div','section'].includes(tag))return '\n\n'+text+'\n\n';if(['strong','b'].includes(tag))return '**'+text+'**';if(['em','i'].includes(tag))return '*'+text+'*';if(tag==='br')return '\n';if(tag==='li')return '\n- '+text;if(tag==='a'){const url=node.getAttribute('href')||'';return /^https?:\/\/[^\s<>"']+$/.test(url)?'['+text+']('+url+')':text;}return text;}
 event.preventDefault();insert([...doc.body.childNodes].map(convert).join('').replace(/\n{3,}/g,'\n\n').trim());say('Formatted text pasted as clean Markdown. Upload images separately.');
});
document.querySelector('#media-upload').onchange=async event=>{
 const file=event.target.files[0];if(!file)return;if(file.size>5*1024*1024){say('Files must be 5 MB or smaller.');return;}
 try{const buffer=await file.arrayBuffer();let binary='';new Uint8Array(buffer).forEach(byte=>{binary+=String.fromCharCode(byte);});const media=await(await api('/api/upload',{name:file.name,data:btoa(binary)})).json();const item=document.createElement('div');item.className='media-item';const name=document.createElement('p');name.textContent=media.name+' · '+media.url;item.append(name);
 if(media.url.endsWith('.pdf')){attachments.push({title:file.name,url:media.url});renderAttachments();}else{
 const add=document.createElement('button');add.type='button';add.textContent='Insert image with caption';add.onclick=()=>insert('\n\n![Describe the image]('+media.url+' "Write your caption")\n\n');
 const featured=document.createElement('button');featured.type='button';featured.textContent='Use as featured image';featured.onclick=()=>{field('featured_image').value=media.url;dirty=true;};item.append(add,featured);}
 document.querySelector('#uploaded-media').append(item);dirty=true;say('Media saved locally. It has not been published.');}catch(error){say(error.message);}finally{event.target.value='';}
};
refresh().catch(error=>say(error.message));
