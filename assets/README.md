# Assets

- `aleksei-1.jpg` — original portrait extracted losslessly from the previous home page.
- `site.css`, `site.js`, `crown.js` — the home page layout, controls and rotating version of the original crown.
- `enhancements.css`, `enhancements.js` — buildless adaptations of the user-supplied 21st.dev Halftone Wordmark Footer, Tilted Grid Hero, Shiny Button and Background Paths references.
- `project-covers/*.svg` — authored vector illustrations of the six linked open-source projects; not product screenshots or stock photography.
- `github-stats.json` — dated public GitHub snapshot, refreshed by `build/update_github.py` and the GitHub Actions workflow. All visitor requests remain same-origin.
- `vendor/three.*.min.js` — Three.js 0.180.0, downloaded from the public npm distribution through jsDelivr. MIT license in `vendor/three-LICENSE.txt`.

## Reference sources

- Composition: https://www.comblock.ru/
- Extruded geometry: https://threejs.org/docs/#api/en/geometries/ExtrudeGeometry
- Reduced motion: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- Performance: https://web.dev/articles/animations-guide
- Interruptible menu animation: https://developer.mozilla.org/en-US/docs/Web/API/Element/animate
- Native disclosure fallback: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/details

The reference's code, texts and identity have not been copied. The crown path and palette belong to the existing site. The 3D scene makes no external network requests.

## 21st.dev component attribution

- Halftone Wordmark Footer — kedhareswer: https://21st.dev/@kedhareswer/components/halftone-wordmark-footer
- Tilted Grid Hero — ruixen.ui: https://21st.dev/@ruixen.ui/components/tilted-grid-hero
- GitHub Activity Grid — wensity: https://21st.dev/@wensity/components/github-activity-grid

The first four effects were adapted from user-supplied source prompts. The
GitHub grid source was retrieved through the direct 21st.dev connector, and its
single moving tooltip and newest-first reveal were adapted to vanilla JS/CSS.
Its mock-data generator is not used: counts and activity levels come from GitHub.

## Fieldwork redesign

The portfolio is a custom composition, not a downloaded template. Broad catalog
research covered portfolio heroes, navigation, bento cards, spotlights, timelines,
type reveals, buttons, backgrounds, footers, filters, templates and themes.
Selected source bundles retrieved directly from 21st.dev:

- Portfolio Hero — waleedkibhen: https://21st.dev/@waleedkibhen/components/portfolio-hero
- Spotlight — kevingirelli: https://21st.dev/@kevingirelli/components/spotlight
- Filter Grid — ddoemonn: https://21st.dev/@ddoemonn/components/filter-grid
- Scroll animated timeline — ibrandify: https://21st.dev/@ibrandify/components/scroll-timeline
- Magnetic Button — Mohammad Shehadeh / Hirael (MIT): https://21st.dev/@mohammadshehadeh/components/magnetic-button
- Text Reveal — kuratlielia: https://21st.dev/@kuratlielia/components/text-reveal

`portfolio.css` and `portfolio.js` adapt selected interaction ideas to the existing
static architecture. The hero, annotated portrait, case diagrams, copy structure,
colour system and contact panel are authored for Aleksei. No fictional customers,
testimonials or preview statistics are introduced. Existing portrait and crown
are retained; all project detail text remains available in disclosures.
