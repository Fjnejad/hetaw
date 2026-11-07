# hetaw.de

Website of HETAW — decision support for earlier endometriosis recognition at the first visit.

Static site, no build step: `index.html`, `impressum.html`, `datenschutz.html`, `assets/` (CSS, self-hosted fonts, logo).

Hosted on Cloudflare Pages; the `main` branch is deployed automatically. DNS zone at Cloudflare, domain registered at INWX.

## Pages

`index.html` (home), `how-it-works.html`, `for-practices.html`, `for-partners.html`, `about.html`, plus `impressum.html` and `datenschutz.html`.

The five content pages are generated from `tools/build_site.py` (shared header, footer and figures). Edit the script and run `python3 tools/build_site.py .` from the repo root, or edit the HTML directly and stop using the script — don't mix the two.
