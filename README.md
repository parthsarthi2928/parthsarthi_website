# Parth Sarthi — Architecture / Fieldnotes

A static, data-driven personal portfolio: homepage plus four permanent case-study routes. No npm installation or runtime framework is needed.

## Edit and build

1. Update `content/portfolio.json` for projects, credentials, milestones and photography.
2. Edit shared markup in `templates/`. `index.html` and `work/*/index.html` are generated; do not edit them directly.
3. Run `python3 build.py`. This creates pages and validates links, anchors, headings, font files and assets.
4. Preview only public output: `python3 -m http.server 8080 --bind 127.0.0.1 --directory dist`.

`styles.css` contains the art direction, responsive layouts, reading-scale refinements, print and reduced-motion rules. `script.js` progressively enhances navigation, lifecycle exploration, credential filtering/gallery controls and reading progress.

## Content model

- `projects`: slug, number, name, category, title, summary, role, status, metric, metricLabel, stack, problem, context, ownership, decisions, execution, outcome, gaps and flow.
- `credentials`: title, label, group, type, and `verificationLinks` (label + URL). Credentials without links show a verification-pending label, not a dead link.
- `photography`: id (`portrait`, `fieldnote` or `super30`), src, alt, width, height, ratio, caption, title, optional story. Use paths under `assets/`. Null src renders the intentional placeholder. A supplied image requires descriptive alt text; fieldnote supports its own story. Optimise before adding (WebP/AVIF when practical); preserve original files outside public assets.
- `achievements`, `community`, `writing`, `testimonials`: optional arrays. Entries use title, description, optional url, and `published: true`. Empty/unapproved collections are not rendered. Publish only real, permissioned content.
- `milestones`: year, title, description.

Use only an `https://` URL or local asset path for content links; do not enter active-code URLs. The generator escapes plain text. Content and templates are trusted authoring inputs, not a public CMS.

## Assets and metadata

Fonts are locally hosted Latin WOFF2 versions of Instrument Serif and Inter. Licence copies accompany them. The social-sharing image is original generated typographic artwork. The supplied updated résumé remains downloadable. Canonicals and sitemap are derived from the configured `origin`.

The public build is an allowlist of site files; it excludes profile briefs, source data and private authoring notes. Sites configuration retains the existing project. Keep private access until ready for external sharing.

See `CONTENT-ASSET-BRIEF.md` for prioritised requests and `DESIGN-REVIEW.md` for the audit, art direction and validation limitations.
