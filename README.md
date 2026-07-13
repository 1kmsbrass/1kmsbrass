# கும்பகோணம் மெட்டல் ஸ்டோர்ஸ் — Hugo Site

## Run locally
1. Install Hugo (extended version): https://gohugo.io/installation/
2. From this folder: `hugo server -D`
3. Open http://localhost:1313

## Edit content
- **Category cards (homepage grid)** → `data/categories.yaml`
- **Featured product chips (scroll strip)** → `data/featured.yaml`
- **Phone / WhatsApp numbers, tagline** → `hugo.toml` under `[params]`
- **Wholesale / Temple items / Products page text** → `content/*/_index.md`
- **Colors, fonts, spacing** → `assets/css/main.css`

## Managing a big catalog with products.csv
1. Add/edit rows in `products.csv` (open in Excel/Google Sheets, export as CSV,
   drop it back in the project root). Columns:
   `slug, name_tamil, name_english, category, price, unit, description, imageURL, keywords`
   - `category` must be `products` or `temple-items` (or `wholesale` if you add
     dealer-only items later) — it decides which folder the page lands in.
   - `slug` becomes the URL: `/temple-items/kalasam-12inch/`
2. Run: `python3 scripts/build_products.py`
   This regenerates `content/<category>/<slug>/index.md` for every row —
   safe to re-run any time, it overwrites existing generated pages.
3. Commit and push. Cloudflare rebuilds automatically.

Each generated page becomes its own real URL with its own `<title>`, meta
description, Open Graph tags, and Product structured data (JSON-LD) — that's
what lets Google index "Brass Kalasam 12 Inch" separately from "Brass Kudam
8 Inch" instead of lumping your whole catalog into one page. The category
list pages (`/temple-items/`, `/products/`) automatically show cards for
every product in that category — no manual linking needed.

Tip: for hundreds of products, add `python3 scripts/build_products.py` as a
pre-build step in Cloudflare (Build command: `python3 scripts/build_products.py && hugo --minify`)
so you only ever touch the CSV, never the generated markdown by hand.

## Add product photos (R2)
Upload your image to Cloudflare R2, get its public URL, then paste it into
the `imageURL:` field for that item in `data/categories.yaml` or
`data/featured.yaml`. Leave `imageURL: ""` to keep showing the emoji.

## Deploy on Cloudflare Pages
1. Push this repo to GitHub.
2. In Cloudflare dashboard → Workers & Pages → Create → Pages → Connect to Git.
3. Build settings:
   - Framework preset: **Hugo**
   - Build command: `hugo --minify`
   - Build output directory: `public`
   - Environment variable: `HUGO_VERSION` = (match your local `hugo version`, e.g. `0.134.0`)
4. Save and deploy. Every push to `main` auto-deploys; PRs get preview URLs.

## Notes
- Icons for dealers/gifts/home cards default to emoji. Only kalasam/temple-specific
  items need real photos — set those via `imageURL` once uploaded to R2.
- `hugo.toml` centralizes your phone/WhatsApp numbers so you never have to
  hunt through templates to update them.
