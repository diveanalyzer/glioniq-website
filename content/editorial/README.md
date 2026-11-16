# Editorial source

Future owner-approved articles use validated JSON files with Markdown in `body`.
The shared validator and renderer are in `scripts/editorial.py`. Only entries
with `status: published` are built into Blog/Science pages and search.
No articles are published in this development phase. Local drafts live in
`.local-cms/`, excluded from Git and from the preview server's public surface.
See `cms/SETUP.md` for the approval, content history and activation plan.
