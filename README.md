# asmaa.dev

The personal site of Asmaa Abdul-Amin — software engineer building AI-native systems for
financial intelligence, quantitative research, knowledge management, and workflow automation.

- **Live:** <https://asmaa.dev> (custom domain via `CNAME`, served by GitHub Pages from the
  root of `main`)
- **Flagship product:** [BLKPVNTHR.OS](https://os.blkpvnthr.com) — opens in Guest mode, no sign-up.

---

## There is no build step

This is a plain static site: HTML, CSS, and a little vanilla JavaScript. No framework, no
bundler, no preprocessor, no CI build. What is committed is exactly what the browser receives.

- **CSS:** hand-written, in `css/`. `css/styles.css` is the base; `css/os.css` holds the
  design system used by the current pages and must load **after** `styles.css`.
  [Bootstrap 5.3](https://getbootstrap.com/) is pulled from a CDN for the grid, modal and a
  few utilities. (There is no Tailwind here.)
- **JS:** `js/site.js` — mobile nav toggle, active-nav highlighting, and the `©` year.
  Page-specific behaviour (e.g. the gallery filter and modal) is inline in the page that
  needs it.
- **Fonts / icons / images:** all local, under `fonts/` and `assets/`.

## Pages

| Path | What it is |
| --- | --- |
| `index.html` | Home. |
| `blkpvnthr-os/index.html` | The BLKPVNTHR.OS product page. |
| `case-studies.html` | Case studies. |
| `images.html` | Project gallery — a filterable card grid whose image sets are driven by `assets/images/images.json`. |
| `projects.html` | A `noindex` redirect stub kept only so old links do not 404. |
| `robots.txt`, `sitemap.xml` | SEO. `projects.html` is deliberately absent from the sitemap. |

## Partials workflow

Because there is no build step and no server-side includes, the site header/nav and the
footer are **duplicated verbatim into every page**. The duplication is intentional; drift is
not.

The canonical copies live in:

- `includes/partials/nav.html`
- `includes/partials/footer.html`

Each page wraps its copy in sentinel comments (`<!-- @partial:nav start -->` …
`<!-- @partial:nav end -->`). To change the nav or footer, edit the file in
`includes/partials/` and then re-stamp every page:

```bash
python3 tools/sync_partials.py          # rewrite the pages in place
python3 tools/sync_partials.py --check  # exit 1 if any page has drifted
```

`tools/sync_partials.py` is Python 3 stdlib only — no dependencies to install.

## Product imagery

The screenshots under `assets/images/os/` (`ai-brain`, `research-division`, `trading-engine`,
`integrations`, plus the `og-` social image) and `assets/blkpvnthr-os-main.gif` were captured
from the live BLKPVNTHR.OS app at <https://os.blkpvnthr.com>. They show the product's own
demo/seed state — **no number in any screenshot represents real finances or a track record.**
BLKPVNTHR.OS is paper-only; nothing on this site is investment advice.

## Preview locally

No install, no toolchain:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

Serve from the repo root so that the root-absolute paths (`/css/…`, `/assets/…`,
`/js/site.js`) resolve exactly as they do in production.

## Deploy

Push to `main`. GitHub Pages serves the repo root at <https://asmaa.dev>.

---

© 2026 Asmaa Abdul-Amin. Source released under the MIT License.
