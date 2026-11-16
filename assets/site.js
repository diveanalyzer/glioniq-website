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
function initializeLivingOrbs() {
  const orbs = [...document.querySelectorAll('.living-orb')], visible = new Set();
  const sync = () => orbs.forEach(orb => orb.toggleAttribute('data-dormant',document.hidden || !visible.has(orb)));
  const observer = new IntersectionObserver(items => { items.forEach(item => item.isIntersecting ? visible.add(item.target) : visible.delete(item.target)); sync(); });
  orbs.forEach(orb => { orb.toggleAttribute('data-dormant',true); observer.observe(orb); });
  document.addEventListener('visibilitychange',sync);
  // bfcache restores reconnect observers; no animation is left running off-page.
  window.addEventListener('pagehide',()=>{observer.disconnect();visible.clear();sync();});
  window.addEventListener('pageshow',()=>{orbs.forEach(orb=>observer.observe(orb));sync();});
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
