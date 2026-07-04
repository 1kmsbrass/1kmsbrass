#!/usr/bin/env python3
"""
Converts products.csv into individual Hugo content pages under
content/<category>/<slug>/index.md

Run this every time you update products.csv:
    python3 scripts/build_products.py

Each generated page gets:
  - title / description front matter for SEO (<title> and meta description)
  - keywords front matter
  - price, image, category as params for the template to use
"""
import csv
import os
import re

CSV_PATH = "products.csv"
CONTENT_ROOT = "content"

def esc(s: str) -> str:
    """Escape double quotes for safe YAML front matter."""
    return (s or "").replace('"', '\\"')

def main():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    count = 0
    for row in rows:
        category = row["category"].strip()
        slug = row["slug"].strip()
        out_dir = os.path.join(CONTENT_ROOT, category, slug)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "index.md")

        seo_title = f'{row["name_english"].strip()} - {row["name_tamil"].strip()}'
        seo_description = row["description"].strip()
        if len(seo_description) > 155:
            seo_description = seo_description[:152].rsplit(" ", 1)[0] + "..."

        front_matter = f"""---
title: "{esc(seo_title)}"
description: "{esc(seo_description)}"
keywords: [{", ".join('"' + k.strip() + '"' for k in row["keywords"].split(","))}]
nameTamil: "{esc(row['name_tamil'])}"
nameEnglish: "{esc(row['name_english'])}"
price: {row['price'].strip() or 0}
unit: "{esc(row['unit'])}"
imageURL: "{esc(row['imageURL'])}"
category: "{esc(category)}"
type: "product"
---

{row['description'].strip()}
"""
        with open(out_path, "w", encoding="utf-8") as out:
            out.write(front_matter)
        count += 1

    print(f"Generated {count} product pages from {CSV_PATH}")

if __name__ == "__main__":
    main()
