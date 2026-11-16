/* Small progressive enhancements; platform navigation works without JS. */
function searchEntries(entries, query) {
  const terms = query.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  if (!terms.length) return [];
  return entries.filter(entry => terms.every(term => `${entry.title} ${entry.description} ${entry.text}`.toLocaleLowerCase().includes(term)))
    .sort((a, b) => Number(b.title.toLocaleLowerCase().includes(terms.join(' '))) - Number(a.title.toLocaleLowerCase().includes(terms.join(' '))));
}
if (typeof module !== 'undefined') module.exports = { searchEntries };
if (typeof document !== 'undefined') {
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
