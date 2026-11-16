/* Small progressive enhancements; navigation and lab disclosures work without JS. */
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
    const disclosures = cards.map(card => card.querySelector('details'));
    const reduced = matchMedia('(prefers-reduced-motion: reduce)');
    const hover = matchMedia('(hover: hover) and (pointer: fine)');
    let enterTimer, leaveTimer, active = null, movingUntil = 0;
    const cancel = () => { clearTimeout(enterTimer); clearTimeout(leaveTimer); };
    function select(detail, restoreFocus = false) {
      cancel();
      if (active === detail) return;
      const previous = active;
      const positions = cards.map(card => card.getBoundingClientRect());
      active = detail;
      disclosures.forEach(item => {
        item.open = item === detail;
        item.querySelector('summary').setAttribute('aria-expanded', String(item.open));
        item.closest('.platform-card').classList.toggle('is-active', item.open);
      });
      region.classList.toggle('has-active', !!detail);
      if (!reduced.matches && matchMedia('(min-width: 851px)').matches) {
        movingUntil = performance.now() + 520;
        cards.forEach((card, index) => {
          const next = card.getBoundingClientRect(), old = positions[index];
          card.animate([{transform:`translate(${old.x-next.x}px,${old.y-next.y}px)`},{transform:'translate(0,0)'}], {duration:500,easing:'cubic-bezier(.2,.7,.2,1)'});
        });
      }
      if (restoreFocus && previous) previous.querySelector('summary').focus({preventScroll:true});
    }
    disclosures.forEach(detail => {
      const card = detail.closest('.platform-card'), summary = detail.querySelector('summary');
      summary.setAttribute('aria-expanded', 'false');
      summary.addEventListener('click', event => { event.preventDefault(); select(active===detail ? null : detail); });
      detail.querySelector('.tree-close').addEventListener('click', () => select(null, true));
      card.addEventListener('click', event => {
        if (!event.target.closest('a,button,summary,details')) select(active===detail ? null : detail);
      });
      const considerHover = event => {
        if (!hover.matches || event.pointerType === 'touch' || performance.now() < movingUntil || active === detail) return;
        clearTimeout(enterTimer); clearTimeout(leaveTimer);
        enterTimer = setTimeout(() => select(detail), 300);
      };
      card.addEventListener('pointerenter', considerHover);
      card.addEventListener('pointermove', event => {
        // Movement after a layout transition starts a fresh intentional dwell.
        if (performance.now() >= movingUntil && !enterTimer) considerHover(event);
      });
      card.addEventListener('pointerleave', () => { clearTimeout(enterTimer); enterTimer = null; });
      detail.addEventListener('toggle', () => {
        // Native disclosures remain the no-JavaScript fallback.
        if (detail.open && active !== detail) select(detail);
      });
    });
    region.addEventListener('pointerenter', () => clearTimeout(leaveTimer));
    region.addEventListener('pointerleave', () => {
      clearTimeout(enterTimer); enterTimer = null;
      if (hover.matches) leaveTimer = setTimeout(() => {
        if (!region.contains(document.activeElement)) select(null);
      }, 500);
    });
    region.addEventListener('keydown', event => {
      if (event.key === 'Escape' && active) { event.preventDefault(); select(null, true); }
    });
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
      if (!query) { status.textContent = 'Enter a topic to search.'; return; }
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
