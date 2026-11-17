/* Small progressive enhancements; platform navigation works without JS. */
function searchEntries(entries, query) {
  const terms = query.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  if (!terms.length) return [];
  return entries.filter(entry => terms.every(term => `${entry.title} ${entry.description} ${entry.text}`.toLocaleLowerCase().includes(term)))
    .sort((a, b) => Number(b.title.toLocaleLowerCase().includes(terms.join(' '))) - Number(a.title.toLocaleLowerCase().includes(terms.join(' '))));
}
// A monotonic clock: frames render elapsed time; they never count time themselves.
const BREATHING_PATTERNS = Object.freeze({
  'square-focus': [['Inhale',4],['Hold',4],['Exhale',4],['Hold',4]],
  'sleep-calm': [['Inhale',4],['Hold',2],['Exhale',6]],
  'neural-wave': [['Inhale',4],['Exhale',6]],
});
function breathingSnapshot(method, elapsedMs) {
  const phases = BREATHING_PATTERNS[method];
  if (!phases) throw new Error('Unknown breathing pattern');
  const seconds = Math.max(0, elapsedMs) / 1000;
  const duration = phases.reduce((total, phase) => total + phase[1], 0);
  let within = seconds % duration, index = 0;
  while (index < phases.length - 1 && within >= phases[index][1]) within -= phases[index++][1];
  const [phase, length] = phases[index], progress = within / length;
  const eased = (1 - Math.cos(Math.PI * progress)) / 2;
  const expansion = phase === 'Inhale' ? eased : phase === 'Exhale' ? 1 - eased : index === 1 ? 1 : 0;
  return {phase, index, progress, expansion, remaining:Math.ceil(length-within),
    cycle:Math.floor(seconds/duration)+1, routeProgress:(index+progress)/phases.length, elapsedMs:Math.max(0,elapsedMs)};
}
class BreathingClock {
  constructor(method) { if (!BREATHING_PATTERNS[method]) throw new Error('Unknown breathing pattern'); this.method=method; this.reset(); }
  reset() { this.elapsed=0; this.startedAt=0; this.running=false; this.started=false; }
  start(now) { this.reset(); this.started=true; this.running=true; this.startedAt=now; }
  value(now) { return this.elapsed + (this.running ? Math.max(0,now-this.startedAt) : 0); }
  pause(now) { this.elapsed=this.value(now); this.running=false; }
  resume(now) { if (this.started && !this.running) { this.startedAt=now; this.running=true; } }
  snapshot(now) { return breathingSnapshot(this.method,this.value(now)); }
}
function renderBreathingOrb(orb, snapshot, reduced=false) {
  const breath = snapshot.expansion;
  // Tiny continuous arm movement during holds; the sphere stays at the phase size.
  const life = Math.sin(snapshot.elapsedMs/1500)*.002;
  orb.toggleAttribute('data-active',true);
  orb.style.setProperty('--orb-scale',reduced ? '1' : String(.94+.12*breath));
  orb.style.setProperty('--orb-light',reduced ? '1' : String(.96+.16*breath));
  orb.style.setProperty('--arm-shift',reduced ? '0px' : (breath*3)+'px');
  orb.style.setProperty('--arm-scale',reduced ? '1' : String(.98+.065*breath+life));
}
function renderBreathingScene(scene, snapshot, reduced=false) {
  renderBreathingOrb(scene.querySelector('.living-orb'),snapshot,reduced);
  scene.dataset.phase=String(snapshot.index);
  scene.querySelector('.frame-trace').style.strokeDashoffset=String(1-snapshot.routeProgress);
}
function initializeLivingOrbs(scope=document) {
  const orbs = [...scope.querySelectorAll('.living-orb')], visible = new Set();
  const sync = () => orbs.forEach(orb => orb.toggleAttribute('data-dormant',document.hidden || !visible.has(orb)));
  const observer = new IntersectionObserver(items => { items.forEach(item => item.isIntersecting ? visible.add(item.target) : visible.delete(item.target)); sync(); });
  orbs.forEach(orb => { orb.toggleAttribute('data-dormant',true); observer.observe(orb); });
  document.addEventListener('visibilitychange',sync);
  // bfcache restores reconnect observers; no animation is left running off-page.
  const hide=()=>{observer.disconnect();visible.clear();sync();};
  const show=()=>{orbs.forEach(orb=>observer.observe(orb));sync();};
  window.addEventListener('pagehide',hide);window.addEventListener('pageshow',show);
  return ()=>{hide();document.removeEventListener('visibilitychange',sync);window.removeEventListener('pagehide',hide);window.removeEventListener('pageshow',show);};
}
if (typeof module !== 'undefined') module.exports = { searchEntries, BREATHING_PATTERNS, breathingSnapshot, BreathingClock, renderBreathingOrb };
if (typeof document !== 'undefined') {
  initializeLivingOrbs();
  const navigation = document.querySelector('#navigation');
  const mobile = window.matchMedia('(max-width: 850px)');
  const syncNavigation = () => { if (navigation) navigation.open = !mobile.matches; };
  syncNavigation(); mobile.addEventListener('change', syncNavigation);
  navigation?.addEventListener('keydown', event => {
    if (event.key === 'Escape' && mobile.matches) { navigation.open = false; navigation.querySelector('summary').focus(); }
  });
  navigation?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => { if (mobile.matches) navigation.open = false; }));
  const form = document.querySelector('#site-search');
  if (form) {
    const field = document.querySelector('#query');
    const status = document.querySelector('#search-status');
    const results = document.querySelector('#search-results');
    let entries, requestNumber = 0;
    async function runSearch() {
      const ownRequest = ++requestNumber;
      const query = field.value.trim().slice(0, 120);
      results.replaceChildren();
      if (!query) { status.textContent = 'Discover our platforms, laboratories and scientific insights.'; return; }
      status.textContent = 'Searching…';
      try {
        if (!entries) {
          const response = await fetch('/assets/search-index.json', {cache:'no-cache'});
          if (!response.ok) throw new Error('Search index unavailable');
          entries = await response.json();
        }
        if (ownRequest !== requestNumber) return;
        const matches = searchEntries(entries, query);
        status.textContent = matches.length ? `${matches.length} ${matches.length === 1 ? 'result' : 'results'} for “${query}”` : `No results for “${query}”. Try a platform name, memory or learning.`;
        matches.forEach(entry => {
          const article = document.createElement('article'); article.className = 'search-result';
          const title = document.createElement('h2'); const link = document.createElement('a');
          link.href = entry.url; link.textContent = entry.title; title.append(link);
          const description = document.createElement('p'); description.textContent = entry.description;
          article.append(title, description); results.append(article);
        });
      } catch (_) {
        if (ownRequest === requestNumber) status.textContent = 'Search is temporarily unavailable. Please try Search again, or browse the navigation above.';
      }
    }
    form.addEventListener('submit', event => {
      event.preventDefault();
      const url = new URL(location.href); const query = field.value.trim().slice(0, 120);
      query ? url.searchParams.set('q', query) : url.searchParams.delete('q');
      history.replaceState(null, '', url); runSearch();
    });
    field.value = (new URLSearchParams(location.search).get('q') || '').slice(0, 120);
    runSearch();
  }
}

function initializeBreathingActivity(root) {
  const clock=new BreathingClock(root.dataset.breathing), scene=root.querySelector('.breathing-scene');
  const start=root.querySelector('[data-action="start"]'),pause=root.querySelector('[data-action="pause"]'),restart=root.querySelector('[data-action="restart"]');
  const phase=root.querySelector('.current-phase'),counter=root.querySelector('[data-countdown]'),cycle=root.querySelector('[data-cycle]'),note=root.querySelector('.session-note');
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  let frame=0, lastPaint=-Infinity;
  const write=(element,value)=>{ if(element.textContent!==String(value)) element.textContent=String(value); };
  function paint(now) {
    const snapshot=clock.snapshot(now);
    renderBreathingScene(scene,snapshot,reduced.matches);
    write(phase,clock.started ? snapshot.phase : 'Ready when you are');
    write(counter,snapshot.remaining);write(cycle,snapshot.cycle);
    root.querySelectorAll('.exercise-steps li').forEach((step,i)=>step.toggleAttribute('data-current',clock.started&&i===snapshot.index));
  }
  function tick(now) {
    if(!clock.running) return;
    if(now-lastPaint>=33){paint(now);lastPaint=now;}
    frame=requestAnimationFrame(tick);
  }
  function controls() {
    root.dataset.state=clock.running?'running':clock.started?'paused':'ready';
    start.disabled=clock.running;write(start,clock.running?'Running':clock.started?'Resume':'Start');
    pause.disabled=!clock.running;restart.disabled=!clock.started;
  }
  function run(restartCycle=false) {
    cancelAnimationFrame(frame);
    const now=performance.now();
    if(restartCycle||!clock.started)clock.start(now);else clock.resume(now);
    paint(now);controls();write(note,'Follow the rhythm. Pause whenever you need.');
    lastPaint=now;frame=requestAnimationFrame(tick);pause.focus({preventScroll:true});
  }
  function stop(reason='Paused. Resume whenever you feel ready.',focus=false) {
    if(!clock.running)return;
    clock.pause(performance.now());cancelAnimationFrame(frame);paint(performance.now());controls();write(note,reason);
    if(focus)start.focus({preventScroll:true});
  }
  start.addEventListener('click',()=>run());
  pause.addEventListener('click',()=>stop(undefined,true));
  restart.addEventListener('click',()=>run(true));
  root.querySelector('.exit-activity').addEventListener('click',()=>{stop();clock.reset();paint(performance.now());controls();scene.querySelector('.living-orb').removeAttribute('data-active');write(note,'Start when you feel ready. Follow a comfortable pace.');});
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop('Paused while the page was hidden. Resume when ready.');});
  const observer=new IntersectionObserver(entries=>{if(!entries[0].isIntersecting)stop('Paused while the guide was out of view. Resume when ready.');},{threshold:0});
  observer.observe(root.querySelector('.breathing-workspace'));
  window.addEventListener('pagehide',()=>{stop('Paused after leaving the activity. Resume when ready.');observer.disconnect();});
  window.addEventListener('pageshow',()=>observer.observe(root.querySelector('.breathing-workspace')));
  reduced.addEventListener('change',()=>{if(clock.started)paint(performance.now());});
  controls();
}
if(typeof document!=='undefined')document.querySelectorAll('[data-breathing]').forEach(initializeBreathingActivity);

function initializeCentralTree(tree) {
  const svg=tree.querySelector('.tree-wires'),nodes=[...tree.querySelectorAll('.tree-branch>.activity-card')];
  function connect() {
    const bounds=tree.getBoundingClientRect();
    svg.setAttribute('viewBox',`0 0 ${bounds.width} ${bounds.height}`);
    const points=nodes.map(node=>{const r=node.getBoundingClientRect();return {x:r.left+r.width/2-bounds.left,y:r.top-bounds.top,left:r.left-bounds.left};});
    const narrow=matchMedia('(max-width:650px)').matches;
    svg.replaceChildren(...points.map(point=>{
      const path=document.createElementNS('http://www.w3.org/2000/svg','path');
      const d=narrow?`M${bounds.width/2} 0H1V${point.y+32}H${point.left}`:
        point.y<40?`M${bounds.width/2} 0V7H${point.x}V${point.y}`:
        `M${bounds.width/2} 0H1V${point.y-14}H${point.x}V${point.y}`;
      path.setAttribute('d',d);return path;
    }));
    tree.toggleAttribute('data-connected',true);
  }
  const observer=new ResizeObserver(connect);observer.observe(tree);connect();
  const hide=()=>observer.disconnect(),show=()=>observer.observe(tree);
  window.addEventListener('pagehide',hide);window.addEventListener('pageshow',show);
  return ()=>{hide();window.removeEventListener('pagehide',hide);window.removeEventListener('pageshow',show);};
}
if(typeof document!=='undefined')document.querySelectorAll('.neural-tree').forEach(initializeCentralTree);

function initializeHomepageExplorer() {
  const container=document.querySelector('.home-page .laboratory-explorer');
  if(!container)return;
  const grid=container.querySelector('.platform-grid'),host=document.createElement('div');
  const status=document.createElement('p');status.className='explorer-load-status';status.setAttribute('role','status');
  host.className='inline-exploration';host.hidden=true;container.append(status,host);
  const allowed=['trampolina','dr-quiz','neuropath','neurobreath'];
  let sequence=0,request=null,dispose=[],lastKey=null;
  const clear=()=>{dispose.forEach(fn=>fn());dispose=[];host.replaceChildren();};
  const selected=()=>{const key=new URLSearchParams(location.search).get('laboratory');return allowed.includes(key)?key:null;};
  async function show(key,{push=false,focus=false}={}) {
    const current=++sequence;request?.abort();request=null;
    if(!key){
      clear();host.hidden=true;grid.hidden=false;status.textContent='';delete container.dataset.explorer;
      if(push){const url=new URL(location.href);url.searchParams.delete('laboratory');url.hash='laboratories';history.pushState(null,'',url);}
      if(focus&&lastKey)grid.querySelector('[data-platform="'+lastKey+'"] .laboratory-toggle').focus({preventScroll:true});
      return;
    }
    status.textContent='Opening laboratories…';request=new AbortController();
    try {
      const response=await fetch('/laboratories/'+key+'/explore/',{signal:request.signal});
      if(!response.ok)throw Error('Explorer unavailable');
      const documentCopy=new DOMParser().parseFromString(await response.text(),'text/html');
      const tree=documentCopy.querySelector('[data-central-tree="'+key+'"]');
      if(!tree)throw Error('Explorer unavailable');
      if(current!==sequence)return;
      clear();
      const title=tree.querySelector('h1'),heading=document.createElement('h3');
      heading.textContent=title.textContent;heading.tabIndex=-1;title.replaceWith(heading);
      tree.querySelectorAll('[data-close-explorer]').forEach(link=>link.addEventListener('click',event=>{
        if(event.button||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
        event.preventDefault();show(null,{push:true,focus:true});
      }));
      grid.hidden=true;host.hidden=false;host.append(tree);container.dataset.explorer=key;lastKey=key;
      dispose.push(initializeCentralTree(tree.querySelector('.neural-tree')),initializeLivingOrbs(tree));
      status.textContent='';
      if(push){const url=new URL(location.href);url.searchParams.set('laboratory',key);url.hash='laboratories';history.pushState(null,'',url);}
      if(focus){heading.focus({preventScroll:true});container.scrollIntoView({block:'start',behavior:'instant'});}
    } catch(error) {
      if(current!==sequence||error.name==='AbortError')return;
      status.replaceChildren(document.createTextNode('The explorer could not open here. '));
      const link=document.createElement('a');link.href='/laboratories/'+key+'/explore/';link.textContent='Open the laboratory page';status.append(link);
    }
  }
  grid.querySelectorAll('.laboratory-toggle').forEach(link=>link.addEventListener('click',event=>{
    if(event.button||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
    const key=link.closest('[data-platform]').dataset.platform;
    if(allowed.includes(key)){event.preventDefault();show(key,{push:true,focus:true});}
  }));
  window.addEventListener('popstate',()=>show(selected(),{focus:true}));
  show(selected());
}
if(typeof document!=='undefined')initializeHomepageExplorer();
