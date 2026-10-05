# Adam Hines — personal research website

A static GitHub Pages site about robotics, event-based vision, and open-source software. No JavaScript framework, package manager, or server-side runtime is needed to publish it.

## Preview and update

```sh
python3 scripts/build.py
python3 scripts/check_site.py
python3 -m http.server 8765 --bind 127.0.0.1
```

Open http://127.0.0.1:8765/. Commit the generated HTML alongside its sources; GitHub Pages serves the files directly. Keep the existing Pages deployment configuration. Do not publish temporary review output.

- `templates/home.html`: homepage copy and layout.
- `data/publications.json`: full bibliography; stable `id` values preserve incoming links. `status` distinguishes Published, Accepted, and Preprint. Preserve full author lists and existing PDF paths.
- `data/news.json`: archive in reverse chronological order. Use an empty `month` when only a year is known. `date` stores a verified precise date when available; never infer an event date from a crawl date.
- `data/career.json`: public career content and the last substantive update date. Updating `updated` changes the sitemap's `lastmod` values; do not change it for routine rebuilds.
- `scripts/build.py`: shared navigation, metadata, page layouts, and public CV generation. Generated outputs are the four root HTML pages, `static/cv-public.html`, and the sitemap.
- `static/css/site.css` and `static/css/cv-print.css`: website and print styles.

After editing content, run the build and checks. The builder uses only Python's standard library (Python 3.9+). Local links use root-relative URLs because this is a user site hosted at the domain root.

## Regenerate the public CV

The private Word document is deliberately not included or loaded by the build. All committed career content is already sanitised. Update only public facts in the data files; never copy a private CV into this repository.

With the preview server running, install the optional review dependencies into an isolated environment, then run:

```sh
python -m pip install -r scripts/requirements-review.txt
python scripts/render_cv.py
python scripts/review_site.py
```

These commands default to local Google Chrome on macOS. Supply `--chrome /path/to/chrome` on another platform and `--base-url` for a different preview port. Screenshots go to `/tmp/adam-site-review` by default. The renderer strips browser metadata and writes `static/CV.pdf`. Review all five pages after changes; adjust deliberate print page breaks if the content grows.

Public CV policy: retain professional email, qualifications, appointments, awarded grants, publications, teaching, and service. Omit phone numbers, referees, numerical grades, unpublished proposals, volatile publication metrics, and private metadata. Do not add private data to HTML comments, filenames, links, structured data, or PDF attachments. The generated print HTML is public too; its `noindex` avoids a redundant search result, not access to its contents.

## Search Console after deployment

The homepage was reported as indexed before this redesign; name-query visibility is the main objective. This repository does not have authenticated Search Console access.

1. Inspect `/`, `/papers.html`, `/cv.html`, and `/news.html`. Check HTTP success, indexing eligibility, the rendered content, and Google's selected canonical.
2. Confirm `/sitemap.xml` is submitted and fetched successfully. It contains the four canonical page URLs; preserve the existing verification token.
3. Request indexing for the changed pages once after deployment.
4. Validate homepage structured data with Google's Rich Results Test. No special search appearance or ranking is guaranteed.
5. Record a 28-day performance baseline for “Adam Hines”, “Adam D Hines”, “Adam Hines robotics”, “Adam Hines event-based vision”, and “Adam Hines EventCV”. Compare clicks, impressions, and average position after approximately four and eight weeks, using comparable date ranges and the same filters.
6. Review backlinks from QUT, ORCID, Google Scholar, LinkedIn, GitHub, and EventCV. GitHub and LinkedIn already expose personal-website references; verify their destinations. Other profile editors were not accessed. Add or correct the canonical website link where missing; do not create duplicate profiles or repetitive keyword text.

Guidance: [canonicals](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls), [sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap), [profile pages](https://developers.google.com/search/docs/appearance/structured-data/profile-page), [site names](https://developers.google.com/search/docs/appearance/site-names).

## Content provenance — October 2026 refresh

- Preserved all seven original publication records and 48 original news entries, with spelling corrections and an expanded LENS announcement. Added seven publications and ten news entries (14 publications and 58 news entries in total).
- Current role, career details, teaching, grants, and service come from the owner-supplied 2026 CV. The 2026 QUT appointment and IROS role use year-only dates. EMCR wording preserves committee membership from 2024 without claiming co-chairship started then.
- The homepage has three sections: an introduction highlighting vision-based positioning for Roo-ver, four equally weighted illustrated work entries, and two recent updates. EventCV has no separate feature section. The opening image is Adam’s portrait; Roo-ver remains prominent in the introductory text.
- Google Scholar returned HTTP 429 during the follow-up refresh. Two missing September 2026 preprints were independently verified against arXiv: [The EventCV Library for Event-Based Robotic Vision](https://arxiv.org/abs/2609.21330) and [Multi-viewpoint Geo-localization with Event Cameras (MegaEvent)](https://arxiv.org/abs/2609.21219). Both were submitted on 18 September 2026 and remain labelled as preprints. Direct arXiv links are used because DOI registration was marked pending. This is not a claim that every entry in the inaccessible Scholar profile was reconciled.
- [Event-LAB](https://arxiv.org/abs/2509.14516): full author list and ICRA 2026 acceptance confirmed; the March 2026 revision records acceptance. No publisher DOI was invented.
- [EventGeM](https://arxiv.org/abs/2603.05807), [insect vision model](https://arxiv.org/abs/2602.06405), and [Pixi](https://arxiv.org/abs/2511.04827): titles, authors, dates, and preprint status checked against arXiv.
- [VPRTempo](https://arxiv.org/abs/2309.10225): restored Peter G. Stratton to the author list, matching the CV and arXiv.
- Honeybee preprint: title, initials, year, and Research Square DOI transcribed from the supplied CV. The DOI could not be independently retrieved during this update; no unverified release date or extra resource links were added.
- [EventCV](https://eventcv.net/), its [documentation](https://docs.eventcv.net/en/latest/), and local project source support the software descriptions. The website reports version 1.0.8 released on 20 September 2026; the news item records that release rather than a live “latest version” claim.
- LinkedIn only exposed some public material. The existing June 2025 entry links to the [LENS announcement](https://www.linkedin.com/posts/adamdhines_sciencerobotics-neuroscience-robotics-activity-7341238307390935040-2596); this update is not a complete import of LinkedIn activity.

## Attribution and licenses

The previous site was based on [Nerfies](https://nerfies.github.io/), licensed under [Creative Commons Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/). That attribution is retained; the October 2026 redesign replaces the original layout and styles. Previously supplied portraits, research figures, and papers retain their respective rights.

Source Sans 3 and Source Serif 4 are distributed under the SIL Open Font License; their licenses are in `static/fonts/`. EventCV's existing logo and FEAST example image are reused from the owner's EventCV repository, under its Apache-2.0 license, included as `static/images/EventCV-LICENSE.txt`. The FEAST image is resized/compressed; it depicts the project's before/after learning example. It is not a new experimental result.

### Roo-ver and research imagery

Roo-ver is now explicit in the homepage introduction and public CV. The owner confirmed participation; [QUT’s project overview](https://www.qut.edu.au/research/article?id=201913) describes the positioning work and [Thierry Peynot’s public profile](https://au.linkedin.com/in/thierry-peynot) names Adam in the QUT Roo-ver team. Copy describes a contribution to the team, without claiming mission leadership or a completed lunar deployment.

The retained, currently unused Roo-ver prototype photograph comes from [Roo-ver’s official website](https://roover.com.au/) and should carry a visible Roo-ver / ELO₂ consortium credit if used again. Original asset: [hero-1.jpg](https://images.squarespace-cdn.com/content/v1/686db6656852c8458d6e718d/2720ac89-8e40-4b88-8025-3cb9afe737d4/hero-1.jpg). Copyright remains with its owner. The local WebP is resized and compressed, with the complete image composition retained.

Six additional publication thumbnails use actual paper figures: EventCV figure 1, MegaEvent figure 1, EventGeM figure 1, Event-LAB figure 1, the insect vision model figure 3, and Pixi figure 1. Their source URLs and descriptions are recorded in `data/publications.json` as `image_source` and `image_alt`. SVG figures were rendered to raster without changing their content. All figures use consistent white frames and contain-fit scaling; publication thumbnails link to the larger local figure. The honeybee preprint and older commentary have no verified reusable figure, so their desktop rows use a neutral text placeholder. No synthetic scientific figures or results were created.
