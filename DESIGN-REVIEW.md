# Architecture / Fieldnotes — design review

## Audit of the previous version

The previous page had a coherent ink/cobalt palette but largely followed the résumé: long sequential sections, repeated rectangular cards and generic modal case studies. The opening “Complex data. Clear direction.” did not uniquely establish a senior architect or delivery leader. Evidence, employer/client relationship and personal background had similar visual priority. Credential lists were passive. Projects had no permanent links. There were no real personal assets, so the personal story remained abstract.

Desktop/mobile CSS and all source content were audited. Both résumés had already been read in the preceding iteration. Available assets consisted only of the updated résumé PDF; no portraits, activity photos or verified credential badges were supplied. The prior version had not had a completed mobile browser review.

## Creative thesis

**The decisions behind the systems.** An editorial portfolio organised like a small collection of architectural case files, paired with personal fieldnotes. A serif-led visual system gives the site a recognisable rhythm without relying on logos or decorative technology imagery.

- Ivory `#f4f1ea`, charcoal `#282b27`, oxblood `#713a3b`; supporting muted mineral surfaces only for specific stories.
- Locally hosted Instrument Serif (regular/italic) for expressive headings, Inter for evidence and body text.
- Generous margins, thin rules, asymmetric case-study rows, an intentionally reserved portrait space and a dark architecture chapter.
- Meaningful diagrams only: shared platform foundations, three-stage modernisation and the semantic layer.
- Motion confined to state changes, gallery movement and a restrained case-reading indicator; reduced motion respected.

## Narrative

Who and how senior → documented scale → three flagship cases → architectural decisions → portfolio leadership and progression → academic/person story → continuing learning → contact.

Supply-chain delivery analytics is a fourth, deeper archive entry. MDM and Flyway governance appear where they explain modelling and leadership; they do not become empty stand-alone “projects”. Unprovided achievements, community activities and writing have data collections but remain unpublished.

## Mobile choices

Separate menu, shorter three-line hero, compact portrait/current-engagement pairing, stacked case studies, four compact lifecycle controls, two-column career milestones, touch/keyboard-scrollable credentials and in-flow case navigation. The system explainer remains readable without JavaScript. At reduced motion, scrolling becomes immediate. No animation gates content visibility.

## Self-critique and refinements

The first rendered desktop pass confirmed the visual concept but secondary reading sizes were too small. Body and supporting labels were increased, the hero was shortened around “nearly a decade”, and main evidence was kept in a simple editorial strip. The homepage no longer relies on modals, icon walls or the previous generic card system. Photographic spaces remain honest placeholders rather than fabricated scenes.

## Validation and limits

- Five generated pages pass internal link, fragment, asset, one-H1 and unresolved-template checks.
- All local fonts validate as WOFF2. JavaScript syntax passes.
- Desktop rendered screenshot reviewed in Chrome before the final typography pass.
- Native browser review became unavailable while switching into the mobile view. No completed mobile/tablet interaction audit, final visual recheck, Lighthouse score or WCAG certification is claimed.
- Build includes only public assets, pages and metadata; authoring briefs and content source stay out of the deployment archive.
- All pages have canonical/title/description and Person or Article structured metadata. Homepage has an original social card. Case pages use text social metadata because they have no genuine primary images.
- Performance strategy: static HTML, no runtime dependencies, locally hosted small fonts, no external font requests, no autoplay media, small progressive-enhancement script, and lazy loading for future personal photography.

## Evidence boundary

The 1,000+ migration is Talend → AWS/Airflow; Databricks remains ongoing. ~60 is portfolio scope, not a direct-report count. Credential names follow the résumé and are visibly pending verification. Super 30 programme context comes from https://www.super30.org/FAQS.html and https://super30.org/ ; personal cohort selection is not claimed. MWAA, Jenkins and Bitbucket were mentioned as themes in the request but are not attributed to individual projects without more specific evidence.
