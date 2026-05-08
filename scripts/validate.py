#!/usr/bin/env python3
"""Validate meal-prep app integrity. Run locally or in CI.

Checks:
1. manifest.json — required PWA fields present
2. sitemap.xml — valid XML
3. index.html — JS parses, DATA constant valid
4. Recipe data — required fields, unique names, valid categories
5. weeklyPlan references existing recipes
6. No non-purchasable composite ingredients (전분물 etc.)
7. Common typo regression guard
8. Service worker syntax (sw.js)

Exits 1 on any error, 0 if only warnings or all OK.
"""
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / 'index.html'
MANIFEST = ROOT / 'manifest.json'
SITEMAP = ROOT / 'sitemap.xml'
SW = ROOT / 'sw.js'

errors: list[str] = []
warnings: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


# --- 1. manifest.json
try:
    mani = json.loads(MANIFEST.read_text(encoding='utf-8'))
    for f in ('name', 'short_name', 'icons', 'start_url', 'display'):
        if f not in mani:
            fail(f"manifest.json missing required field: {f}")
    if not mani.get('icons'):
        fail("manifest.json has empty icons array")
    print(f"✓ manifest.json — name='{mani.get('name','?')[:40]}', icons={len(mani.get('icons',[]))}")
except FileNotFoundError:
    fail("manifest.json not found")
except json.JSONDecodeError as e:
    fail(f"manifest.json invalid JSON: {e}")

# --- 2. sitemap.xml
try:
    ET.fromstring(SITEMAP.read_text(encoding='utf-8'))
    print("✓ sitemap.xml — valid XML")
except FileNotFoundError:
    warn("sitemap.xml not found")
except ET.ParseError as e:
    fail(f"sitemap.xml parse error: {e}")

# --- 3. index.html — extract DATA constant
html = INDEX.read_text(encoding='utf-8')
data_line = next((ln for ln in html.splitlines() if 'const DATA =' in ln), None)
data = None
if not data_line:
    fail("Could not find 'const DATA =' line in index.html")
else:
    m = re.search(r'const DATA =\s*(.+);\s*$', data_line)
    if not m:
        fail("DATA line format unexpected (missing trailing semicolon?)")
    else:
        try:
            data = json.loads(m.group(1))
            print(f"✓ DATA constant — {len(data.get('recipes',[]))} recipes parsed")
        except json.JSONDecodeError as e:
            fail(f"DATA JSON parse error: {e}")

# --- 4. Recipe data integrity
if data:
    REQUIRED = ['name', 'category', 'type', 'ingredients', 'cookTime',
                'calories', 'protein', 'steps', 'displayCategory']
    ALLOWED_DISPLAY = {'korean', 'western', 'asian', 'mediterranean',
                       'mexican', 'quickmeal'}
    names = []
    for i, r in enumerate(data.get('recipes', [])):
        rn = r.get('name', f'#{i}')
        for f in REQUIRED:
            if f not in r:
                fail(f"Recipe '{rn}' missing field: {f}")
        if r.get('displayCategory') not in ALLOWED_DISPLAY:
            fail(f"Recipe '{rn}' invalid displayCategory: "
                 f"{r.get('displayCategory')!r}")
        if not isinstance(r.get('cookTime'), (int, float)):
            fail(f"Recipe '{rn}' cookTime not numeric")
        if not isinstance(r.get('ingredients'), list) or not r.get('ingredients'):
            fail(f"Recipe '{rn}' ingredients missing or not list")
        if not isinstance(r.get('steps'), list) or not r.get('steps'):
            fail(f"Recipe '{rn}' steps missing or not list")

        # Non-purchasable composite ingredients
        for ing in r.get('ingredients', []):
            if re.match(r'^\s*전분물\b', ing):
                fail(f"Recipe '{rn}' has non-purchasable '전분물' "
                     f"as ingredient: {ing}")

        names.append(rn)

    # Duplicate names allowed only for paginated variants:
    # each recipe sharing a name must declare a distinct 'variant' field.
    from collections import defaultdict
    by_name = defaultdict(list)
    for r in data['recipes']:
        by_name[r['name']].append(r)
    for name, group in by_name.items():
        if len(group) <= 1:
            continue
        variants = [r.get('variant') for r in group]
        if any(v is None for v in variants):
            fail(f"Duplicate name {name!r} missing 'variant' field on one or more entries")
        if len(set(variants)) != len(variants):
            fail(f"Duplicate name {name!r} has non-unique variant labels: {variants}")

    # weeklyPlan references
    name_set = set(names)
    for day, plan in data.get('weeklyPlan', {}).items():
        for meal, n in plan.items():
            if n and n not in name_set:
                fail(f"weeklyPlan {day}.{meal} references "
                     f"non-existent recipe: {n!r}")

    print(f"✓ Recipe data — {len(names)} recipes, "
          f"weeklyPlan references valid")

# --- 5. Typo regression guard
TYPO_PATTERNS = [
    (r'키친타올', '키친타올 → 키친타월'),
    (r'후라이한다', '후라이한다 → 프라이한다'),
    (r'\\ub2ec\\uac78', 'unicode-escaped 달걸 → 달걀 (\\ub2ec\\uac40)'),
]
for pat, msg in TYPO_PATTERNS:
    matches = re.findall(pat, html)
    if matches:
        fail(f"Typo regression: {msg} (found {len(matches)})")

# 소세지 special case: allowed only inside meatKw fallback array
sausage_total = len(re.findall(r'\b소세지\b', html))
meat_line = next((ln for ln in html.splitlines()
                  if 'const meatKw' in ln), '')
sausage_in_meatkw = len(re.findall(r'\b소세지\b', meat_line))
if sausage_total - sausage_in_meatkw > 0:
    fail(f"Typo regression: 소세지 → 소시지 "
         f"(found {sausage_total - sausage_in_meatkw} outside meatKw)")

print(f"✓ No known typo regressions")

# --- 6. Service worker
if SW.exists():
    sw_text = SW.read_text(encoding='utf-8')
    for must in ('addEventListener', 'fetch', 'install', 'activate'):
        if must not in sw_text:
            warn(f"sw.js missing expected '{must}' handler")
    print("✓ sw.js — basic shape OK")
else:
    warn("sw.js not found (PWA offline support disabled)")

# --- 7. JS syntax (via node)
try:
    result = subprocess.run(
        ['node', '-e', f'''
const fs = require('fs');
const html = fs.readFileSync({json.dumps(str(INDEX))}, 'utf-8');
const m = html.match(/<script>([\\s\\S]*?)<\\/script>/);
if (!m) {{ console.error('no script tag'); process.exit(1); }}
try {{ new Function(m[1]); console.log('OK'); }}
catch (e) {{ console.error(e.message); process.exit(1); }}
'''],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        fail(f"JS syntax error: {result.stderr.strip() or result.stdout.strip()}")
    else:
        print("✓ index.html JS — syntax OK")

    if SW.exists():
        sw_check = subprocess.run(
            ['node', '-e', f'''
const fs = require('fs');
const text = fs.readFileSync({json.dumps(str(SW))}, 'utf-8');
try {{ new Function(text); console.log('OK'); }}
catch (e) {{ console.error(e.message); process.exit(1); }}
'''],
            capture_output=True, text=True, timeout=15,
        )
        if sw_check.returncode != 0:
            fail(f"sw.js syntax error: {sw_check.stderr.strip()}")
        else:
            print("✓ sw.js — syntax OK")
except FileNotFoundError:
    warn("node not available, skipping JS syntax check")

# --- Output ---
print('=' * 60)
print(f"Errors: {len(errors)}")
for e in errors:
    print(f"  ✗ {e}")
print(f"Warnings: {len(warnings)}")
for w in warnings:
    print(f"  ⚠ {w}")
print('=' * 60)
sys.exit(1 if errors else 0)
