# GlionIQ editorial workspace and future activation

Status: local preparation works; production authentication, shared roles and publishing are NOT ACTIVE and NOT VERIFIED. This is a local companion editor, not an installed Decap login. No credentials, hosted admin, deployment workflow or remote branch rules were configured.

## Use the local workspace

Run `python3 -B scripts/serve.py --port 8787`, then open `http://127.0.0.1:8787/admin/` directly. The server refuses non-loopback binding and unexpected Host headers. A fresh browser session receives an in-memory, HttpOnly, SameSite=Strict local session cookie. This boundary trusts the signed-in workstation user; it is not a multi-user identity service. Do not tunnel, reverse-proxy or expose it to a LAN.

1. Choose New article; enter title, author, summary and destination.
2. Paste Markdown or formatted text. Supported formatting: headings, paragraphs, bold, italic, links, unordered lists, uploaded images and captions. Rich paste drops embedded images, scripts and styles. Tables, footnotes and arbitrary HTML are not supported.
3. Upload PNG/JPEG/WebP or PDF, maximum 5 MB each. Use images as featured artwork or insert with a caption. PDF uploads become downloadable attachments; their paths can also be attached to structured references. Upload only legally usable material.
4. Add reference title, authors, journal/publisher, year, source URL or DOI, and an optional uploaded PDF. No references are pre-populated or invented.
5. Preview the branded article; save a draft or mark it for owner review. Reopen it from the sidebar to edit.
6. Export draft JSON for backup if desired. Publication is disabled; there is no publish API or credentials.

Drafts are stored in `.local-cms/drafts/*.json`, uploads in `.local-cms/media/`, and previous draft revisions in `.local-cms/history/`. These are deliberately ignored by Git and inaccessible through public static routes. Local drafts are NOT automatically Git-backed, synced or remotely backed up. The version list shows snapshots; restoration currently requires copying a chosen snapshot back to the draft after preserving the latest version. Export and a backup of `.local-cms/` are recommended before moving machines. No delete operation is provided.

A revision check prevents one browser tab from silently overwriting another tab's newer save. An edit after review returns to draft when saved as a draft. Local review status is preparation, not authenticated owner approval.

## Decap assessment, checked 2026-11-16

Decap is compatible with Git-backed static content. Its GitHub backend needs server-side OAuth support; a static GitHub Pages `/admin/` alone cannot perform a secret-bearing token exchange. The standard GitHub backend grants the user's existing repository authority and expects push access. Editorial workflow stores drafts on branches/PRs and publication merges them; workflow labels do not by themselves prevent editors from merging.

The current upstream latest release resolved to `decap-cms@3.17.3`. The October 26 security advisory reports an SVG/file-preview stored-XSS fix in 3.17.3. Any future installation must pin a reviewed release at least that new, re-check current advisories, vendor or integrity-pin browser assets, and prohibit active document uploads. No Decap CDN script is loaded by this project.

Primary sources:

- [GitHub backend and authentication](https://decapcms.org/docs/github-backend/)
- [Editorial workflow and Git operations](https://decapcms.org/docs/editorial-workflows/)
- [Supported local Decap proxy](https://decapcms.org/docs/decap-proxy/)
- [Latest verified release](https://github.com/decaporg/decap-cms/releases/tag/decap-cms@3.17.3)
- [SVG/file-preview security advisory](https://github.com/decaporg/decap-cms/security/advisories/GHSA-qf66-gqh8-qvrh)

We used the small loopback companion instead of activating Decap's remote Git backend or an unauthenticated proxy. The inactive `decap-config.example.yml` describes the matching content model, not a working production installation.

## Future owner-approved activation

None of these external changes were performed in this task.

1. Select a trusted OAuth service (owner-operated HTTPS service or a reviewed managed provider). Register the GitHub OAuth callback exactly. Keep client secrets server-side, validate state/nonces and callback origins, use secure sessions, restrict allowed origins and repository access, rotate credentials and audit revocation. Never paste a PAT into the editor.
2. Review GitHub plan support for the repository's protection/ruleset requirements. Protect the publication branch against direct pushes, force pushes, deletion and bypass; require owner review and successful content/security/build checks. Restrict merges to the owner/release identity. Editors must not have admin or bypass authority. Test all rules using separate real Owner and Editor accounts before enabling publishing.
3. Preferred lower-privilege editorial arrangement: a separate content repository or a mediated GitHub App with a content-only API and draft-branch writes. Editors create/edit permitted drafts and upload validated media; only the owner can approve a publication request. A server authorizes assignment, media writes and the transition to published. Standard Decap GitHub OAuth alone cannot enforce assigned-draft permissions. If using normal repository collaborators, they may access all repository drafts; that narrower role requirement remains unmet. Do not claim it works.
4. For an initial protected-PR workflow, use Decap `editorial_workflow`; a draft creates a PR. Require owner CODEOWNERS review on content/media and all build/workflow policy files. Only owner merges, with a server/GitHub rule that cannot be bypassed by the Editor. Do not use `pull_request_target` to execute untrusted code. Checks must validate schemas, media extension/magic/size, links, reference URLs, rendering and approved-asset/story hashes. A production upload service should decode/re-encode raster images and scan PDFs; local magic-byte checks are not malware scanning.
5. The owner reviews the preview, sets `status: published` and publication date on an approved change, then merges. The protected release workflow builds Python templates and packages ONLY public output. `scripts/package_site.py` demonstrates this allowlist. It excludes `/admin`, `cms`, `.local-cms`, source content, scripts, reports and Git metadata. Do not deploy the repository root or the local server.
6. Configure an authenticated editorial preview on separate infrastructure, or keep previews local. Do not expose confidential drafts in public Pages artifacts. Use a dedicated admin origin with CSP, security headers, HTTPS, no third-party scripts and a strictly validated API. GitHub Pages cannot supply the needed auth/API itself.
7. Owner unpublish changes status to draft in a protected PR, rebuilds and releases. The generator removes retired generated article pages from its route manifest and search. The local temporary build test covers removal. Reverting a content commit and rebuilding is the Git history rollback path; never reset/force-push shared history. Media stays retained until an owner-approved reference audit allows deletion.
8. Test Owner create/edit/review/approve/publish/unpublish/references/media/history, Editor permitted draft edits/upload/submit, denied Editor merge/direct push/publish/other-owner edits, signed-out API denial, OAuth failure/revocation, CSRF, upload attacks, build failure and rollback. Authentication, permission enforcement and full publication remain NOT VERIFIED until those tests pass with owner authorization.

The future user flow is Login → New article → Edit → Preview → Submit → Owner approve/publish → protected Git update → generated static release. The local editor currently covers preparation through preview and local review state only.

## Content and template contract

Approved source files belong in `content/editorial/*.json`: structured metadata, `body` as Markdown, `references` as objects and `attachments` as named PDF URLs. The validator is `scripts/editorial.py`. Only `status: published` is built. Local `/local-media/` paths must be promoted to reviewed `/public/editorial/` files before an approved publication build. Article destinations are restricted to `blog` and `science`; slugs cannot target About Us, Home or laboratory routes. The approved story remains in `content/about-us.md`, outside the CMS model.

Templates share the official header, footer, fonts, navy/gold/blue style, reading width, image/caption treatment and reference list. Dates, SEO metadata and search text come from validated content. Drafts are never added to the public index. `content/articles.json` was the previous empty placeholder model; the new editorial folder is the active article source. No existing approved articles were migrated or removed because that collection was empty.

## Tested local security boundaries

The local API requires the session cookie plus exact same-origin Origin on writes, rejects unexpected Host values and refuses unknown/private filesystem paths. It caps request and upload sizes, restricts media types, checks file signatures, uses random media names, serves PDFs as attachments with nosniff, rejects unsafe URL schemes and escapes raw HTML. Article previews also run in an iframe without script permission. There is no publish endpoint. These measures protect the local demonstration; they do not substitute for production authentication, RBAC, auditing or malware scanning.

Local HTTP cookies omit Secure because the server runs only at loopback HTTP; future HTTPS sessions must use Secure. Restarting the server invalidates in-memory sessions. Open `/admin/` again after a restart. The local server is intended for a single trusted workstation user, not mutually untrusted users on the same computer.
