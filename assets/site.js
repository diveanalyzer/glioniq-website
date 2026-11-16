/* Small progressive enhancements; platform navigation works without JS. */
function searchEntries(entries, query) {
  const terms = query.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  if (!terms.length) return [];
  return entries.filter(entry => terms.every(term => `${entry.title} ${entry.description} ${entry.text}`.toLocaleLowerCase().includes(term)))
    .sort((a, b) => Number(b.title.toLocaleLowerCase().includes(terms.join(' '))) - Number(a.title.toLocaleLowerCase().includes(terms.join(' '))));
}
if (typeof module !== 'undefined') module.exports = { searchEntries };
if (typeof document !== 'undefined') {
  const region = document.querySelector('.laboratory-explorer');
  if (region) {
    const cards = [...region.querySelectorAll('.platform-card')];
    const buttons = cards.map(card => card.querySelector('.laboratory-toggle'));
    const trees = [...region.querySelectorAll('[data-tree]')];
    const panel = region.querySelector('#laboratory-panel');
    const title = panel.querySelector('#tree-title');
    const connector = region.querySelector('.neural-connector');
    const reduced = matchMedia('(prefers-reduced-motion: reduce)');
    const narrow = matchMedia('(max-width: 650px)');
    let active = null;
    function connect() {
      if (!active || narrow.matches) { connector.hidden = true; return; }
      connector.hidden = false;
      const r = region.getBoundingClientRect(), c = active.closest('.platform-card').getBoundingClientRect(), p = panel.getBoundingClientRect();
      const left = c.left + c.width / 2 < r.left + r.width / 2;
      const x = (left ? c.left : c.right) - r.left, y = c.top + c.height / 2 - r.top;
      const rail = left ? 3 : r.width - 3, endY = p.top - r.top;
      connector.setAttribute('viewBox', `0 0 ${r.width} ${r.height}`);
      connector.querySelector('path').setAttribute('d', `M${x} ${y}H${rail}V${endY-18}H${r.width/2}V${endY}`);
    }
    function select(button, restoreFocus = false) {
      const previous = active;
      active = button;
      buttons.forEach(item => {
        const open = item === active;
        item.setAttribute('aria-expanded', String(open));
        item.querySelector('.toggle-label').textContent = open ? 'Close Laboratories' : 'Discover Laboratories';
        item.querySelector('.toggle-mark').textContent = open ? '×' : '+';
        item.closest('.platform-card').classList.toggle('is-active', open);
      });
      trees.forEach(tree => { tree.hidden = !active || tree.dataset.tree !== active.closest('.platform-card').dataset.platform; });
      panel.hidden = !active;
      region.classList.toggle('has-active', !!active);
      if (active) {
        title.textContent = active.dataset.name + ' Laboratories';
        if (narrow.matches) {
          // Only explicit activation scrolls. Focus follows the newly revealed content.
          title.focus({preventScroll:true});
          const rect = panel.getBoundingClientRect();
          if (rect.top < 0 || rect.top > innerHeight - 140) panel.scrollIntoView({behavior:reduced.matches?'instant':'smooth',block:'start'});
        }
      } else if (restoreFocus && previous) previous.focus();
      connect();
    }
    buttons.forEach(button => {
      button.hidden = false;
      button.addEventListener('click', () => select(active === button ? null : button));
    });
    panel.querySelector('.tree-close').addEventListener('click', () => select(null, true));
    region.addEventListener('keydown', event => {
      if (event.key === 'Escape' && active) { event.preventDefault(); select(null, true); }
    });
    new ResizeObserver(connect).observe(region);
    narrow.addEventListener('change', connect);
  }
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
