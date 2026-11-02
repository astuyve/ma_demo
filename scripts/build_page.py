"""Inline build/ages.json and build/towns.json into the page template.

Usage: python3 -I scripts/build_page.py scripts/template.html build index.html
"""
import sys

template, build_dir, out_path = sys.argv[1:4]
html = open(template).read()
html = html.replace("/*__AGES__*/null", open(f"{build_dir}/ages.json").read())
html = html.replace("/*__TOWNS__*/null", open(f"{build_dir}/towns.json").read())
open(out_path, "w").write(html)
print(f"wrote {out_path} ({len(html) // 1024} KB)")
