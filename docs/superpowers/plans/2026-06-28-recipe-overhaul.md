# Recipe Overhaul Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Delete the scraped, flavorless recipe set and replace it with ~50 original, genuinely-delicious meal-prep recipes designed from the `knowledge/cooking/` knowledge base (KB) and verified by KB-grounded adversarial review.

**Architecture:** Recipes are authored as per-category JSON under `data/recipes/`, validated against a shared KB rubric, merged by a new `scripts/build_data.py` into `data/structured_data.json`, and injected into the `const DATA = …;` line in `index.html` (the app's source of truth). `scripts/validate.py` is the integrity gate; the rubric review is the flavor gate.

**Tech Stack:** Static HTML/CSS/JS app (no framework); Python 3 build + validation; JSON data; Basic Memory KB at `knowledge/cooking/` for design principles.

---

## Design & Decisions (read first)

**Why the old recipes are bad:** they were scraped from 만개의레시피 / YouTube, so they are generic and under-built — single salt dump, no acid finish, no umami layering, no browning/texture-contrast, seasonings incoherent with cuisine. The fix is to *design* each recipe from the KB.

**Confirmed scope (from brainstorming):**
- 전면 신규 설계 — discard old dish concepts, author new ones.
- ~50 recipes, 소수정예 (quality over count).
- Verification = KB-based adversarial review (we cannot physically cook).

**Source of truth & data flow (NEW):**
```
data/recipes/<category>.json   (authored, 6 files)
        │  scripts/build_data.py  (merge + stats + default weeklyPlan + aggregated shoppingList)
        ▼
data/structured_data.json      (built artifact, archival)
        │  scripts/build_data.py  (inject minified JSON)
        ▼
index.html  ->  const DATA = {…};   (what the app actually runs; validated by validate.py)
```
This formalizes what is today a hand-edited 220 KB inline line — a deliberate, in-scope improvement.

**Hard constraints (validate.py + app behavior must keep working):**
- Required recipe fields: `name, category, type, ingredients, cookTime, calories, protein, steps, displayCategory`. Also keep (all recipes): `difficulty, source, sourceName, tags, servings, storageInfo`. Add for all: `carbs, fat`.
- `displayCategory` ∈ {korean, western, asian, mediterranean, mexican, quickmeal}.
- `type` ∈ {one-pan, one-pot, sheet-pan, standard}.
- `cookTime`, `protein`, `calories`, `carbs`, `fat` numeric. `protein` in grams.
- Unique `name` (duplicates require a distinct `variant` field — we will keep all names unique, no variants).
- No non-purchasable composite ingredients (e.g. `전분물`); every ingredient line is buyable with an amount.
- `DATA.weeklyPlan` must reference only existing recipe names (validate.py check).
- Typo guard: never emit `키친타올`(→키친타월), `후라이한다`(→프라이한다), `소세지`(→소시지 outside meatKw), `달걸`(→달걀).

**App mode coverage (modes are generated live from `DATA.recipes`, not stored):**
- `balanced`: shuffle all non-side-dish recipes.
- `korean`: needs ≥7 with `displayCategory==='korean'` (target ≥14).
- `highprotein`: needs ≥7 with `protein>=30` (target ≥18).
- `quick`(초간편): needs ≥7 with `cookTime<=20`, clusterable by ingredient overlap (target ≥10, deliberately built in shared-pantry families).
- `isSideDish(r)` excludes side dishes from plans (by name list, by side-tags + `calories<=250`, and by `calories<=200`). `tags` is load-bearing here — keep most recipes mains, and tag true sides precisely or they slip into plans.

**Target distribution (~50):** korean 14 · western 9 · asian 9 · mediterranean 6 · mexican 6 · quickmeal 6.
Cross-cutting targets (a recipe can satisfy several): protein≥30 in ≥18; cookTime≤20 in ≥10 (mostly the quickmeal set + fast others); a coherent 7-day default weeklyPlan from the new set.

**Decision record:** This overhaul (delete scraped set → original KB-grounded recipes + a real build step) is recorded as `knowledge/decisions/0004-recipe-overhaul.md`.

**Safety / reversibility:** Old recipes are preserved in git history and in `data/structured_data.json` until rebuilt; the old `data/recipes_*.json` scraped files are deleted (recoverable from git). `data/ingredients.json` is left untouched (out of scope).

**Branch:** Work on `feat/recipe-overhaul`, branched from `feat/basic-memory-setup` so the KB notes are present for reference.

---

## The Recipe Design Rubric (the core standard)

Every recipe is authored to, and adversarially reviewed against, this rubric. **A recipe passes only if all FLAVOR gates G1–G9, all MEAL-PREP gates M1–M3, and all DATA gates D1–D4 hold.** Each gate links the KB note that justifies it.

**Flavor (G):**
- G1 Seasoning calibrated & layered — explicit salt target ≈0.8–1% of main-component weight; salt applied in layers (season protein, season veg, adjust at end), never one dump. → [[Seasoning and Salting]]
- G2 Acid present, usually finishing — ≥1 acid element; bright acids added late. → [[Acidity and Brightness]], [[Balancing Flavors]]
- G3 Umami layered — ≥2 umami sources, exploiting glutamate×nucleotide synergy where natural (간장+다시마/표고/토마토/멸치/파르미지아노). → [[Umami and Synergy]], [[Umami Boosters]]
- G4 Browning / depth step — a Maillard sear, caramelization, fond+deglaze, or aromatic bloom where the dish allows. → [[Maillard and Caramelization]], [[Building Depth and Layering]]
- G5 Fat as carrier, balanced — right fat for aroma/richness, cut by G2 acid so it never cloys. → [[Fat as Flavor Carrier]]
- G6 Texture contrast — ≥1 textural counterpoint (crisp topping, seared edge, fresh crunch). → [[Texture and Mouthfeel]]
- G7 Aromatic finish — fresh herb / zest / aromatic oil / scallion / toasted seed at the end. → [[Composing a Dish]]
- G8 Grammar coherence — every seasoning fits the dish's cuisine grammar; no incoherent mash. → the matching `[[… Flavor Grammar]]`
- G9 Composition complete — fills slots base+sauce+fat+acid+crunch+aroma. → [[Composing a Dish]]

**Meal-prep (M):**
- M1 Batch & store — scales to `servings` (default 4); `storageInfo` states fridge days (3–5) and what to store separately.
- M2 Reheats/holds — no textures that die on reheat unless the recipe isolates them (crunch/fresh element added at serving, stated in steps + storageInfo).
- M3 Make-ahead technique — e.g. dress grains while warm, keep sauces/crunch separate, choose cuts that stay moist. → [[Marination and Tenderizing]], [[Moist Heat Methods]]

**Data (D):**
- D1 Ingredients all purchasable with amounts; no composites (`전분물` etc.). Use `물전분` written as its parts (e.g. `감자전분 1큰술 + 물 2큰술`) only inside steps, never as an ingredient line.
- D2 Steps specific & technique-cued (heat level, time, visual/temperature cue), 5–9 steps; final step covers portioning/cooling/storage.
- D3 Macros plausible — calories/protein/carbs/fat roughly consistent with ingredients and `servings`; protein grams realistic.
- D4 Schema valid — all required fields; enums respected; unique name; no typo-guard hits.

**Scoring:** reviewer assigns each gate pass/fail with a one-line justification and, for any fail, a concrete fix. Author fixes and re-submits until all gates pass.

---

## Task 0: Branch & safety

**Files:** none (git only)

- [ ] **Step 1: Create the working branch**

Run: `git checkout -b feat/recipe-overhaul`
Expected: `Switched to a new branch 'feat/recipe-overhaul'`

- [ ] **Step 2: Confirm baseline validator passes on the OLD data**

Run: `python3 scripts/validate.py; echo "exit=$?"`
Expected: `exit=0` (establishes the gate works before we change data)

- [ ] **Step 3: Snapshot the current recipe set for reference**

Run: `cp data/structured_data.json /tmp/old_structured_data.json && echo saved`
Expected: `saved` (reviewers may diff against the old set; git also preserves it)

---

## Task 1: Decision record (ADR 0004)

**Files:**
- Create: `knowledge/decisions/0004-recipe-overhaul.md`
- Modify: `knowledge/handoff.md` (add `- decided [[ADR 0004 Recipe Overhaul]]`)

- [ ] **Step 1: Write ADR 0004** following the project ADR template (see `0001-baseline.md`): Context (scraped recipes flavorless), Decision (replace with ~50 original KB-grounded recipes + `build_data.py` build step; `data/recipes/*.json` source of truth), Consequences, Relations (`- supports [[Overview]]`, `- relation [[Cooking Knowledge Index]]`).
- [ ] **Step 2: Add the handoff link** under Relations.
- [ ] **Step 3: Commit**

```bash
git add knowledge/decisions/0004-recipe-overhaul.md knowledge/handoff.md
git commit -m "memory: add ADR 0004 recipe overhaul"
```

---

## Task 2: Lock the rubric & schema as a shared artifact

**Files:**
- Create: `docs/superpowers/recipe-rubric.md` (copy the rubric section above verbatim so generator/reviewer subagents share one source)
- Create: `data/recipes/.gitkeep`

- [ ] **Step 1:** Write `docs/superpowers/recipe-rubric.md` = the "Recipe Design Rubric" + the "Hard constraints" + the recipe JSON field contract (one example recipe object, fully populated incl. `carbs`,`fat`).
- [ ] **Step 2:** Create the `data/recipes/` directory with `.gitkeep`.
- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/recipe-rubric.md data/recipes/.gitkeep
git commit -m "docs: recipe design rubric + schema contract"
```

---

## Task 3: Roster — 50 dish concepts with flavor theses

**Files:**
- Create: `data/recipes/_roster.json` (working file; not consumed by the app)

Design the full 50-recipe roster up front to guarantee coverage and avoid duplication. Each entry: `{name, displayCategory, type, leadProtein, cuisineGrammar, flavorThesis, modeTags}` where `flavorThesis` is one sentence on what makes it delicious (which KB levers it pulls) and `modeTags` ⊆ {highprotein, quick, korean}.

- [ ] **Step 1:** Draft the roster honoring the target distribution and cross-cutting targets (≥14 korean displayCategory, ≥18 protein-heavy, ≥10 quick≤20min built as 2–3 shared-pantry families for the 초간편 clusterer).
- [ ] **Step 2:** Self-check counts with:

Run: `python3 -c "import json,collections as c; d=json.load(open('data/recipes/_roster.json')); print(c.Counter(r['displayCategory'] for r in d)); print('quick',sum('quick' in r['modeTags'] for r in d),'hp',sum('highprotein' in r['modeTags'] for r in d))"`
Expected: displayCategory counts ≈ target; quick ≥10; hp ≥18.

- [ ] **Step 3: Commit**

```bash
git add data/recipes/_roster.json
git commit -m "data: 50-recipe roster with flavor theses"
```

---

## Task 4: Author recipes — one subagent per category (fan-out)

**Files (one per category):**
- Create: `data/recipes/korean.json`, `western.json`, `asian.json`, `mediterranean.json`, `mexican.json`, `quickmeal.json`

Each category subagent receives: the rubric (`docs/superpowers/recipe-rubric.md`), its slice of `_roster.json`, and the relevant KB notes (it reads `knowledge/cooking/**`, especially its `[[… Flavor Grammar]]`, the technique notes its dishes use, and the `principles`/`flavor`/`creativity` hub notes). It authors each recipe to pass G1–G9 / M1–M3 / D1–D4, writing a JSON array of full recipe objects (schema per rubric, including `carbs`,`fat`; `source` = `"원본 레시피 (meal-prep KB 기반 설계)"`, `sourceName` = `"meal-prep KB"`). Korean identifiers stay Korean.

- [ ] **Step 1:** Dispatch 6 category subagents (parallel). Each writes its `data/recipes/<category>.json`.
- [ ] **Step 2: Per-file JSON sanity check**

Run: `for f in data/recipes/{korean,western,asian,mediterranean,mexican,quickmeal}.json; do python3 -c "import json;d=json.load(open('$f'));print('$f',len(d),'recipes')"; done`
Expected: each file parses; total ≈ 50.

- [ ] **Step 3: Commit**

```bash
git add data/recipes/*.json
git commit -m "data: author 50 KB-grounded recipes (pre-review)"
```

---

## Task 5: Adversarial KB review + fix loop (the flavor gate)

**Files:** modify `data/recipes/<category>.json` as fixes land.

Use the pipeline pattern: each recipe → an adversarial reviewer subagent that *tries to prove the dish is flat/boring/incoherent or meal-prep-unsuitable*, scoring all rubric gates with justifications and concrete fixes. Reviewer must default to FAIL when unconvinced. Any failed gate → the authoring side applies the fix → re-review until all gates pass. Reviewers cite KB notes by exact title.

- [ ] **Step 1:** Run the review pipeline over all ~50 recipes; collect per-recipe verdicts.
- [ ] **Step 2:** Apply fixes for every failing gate; re-review changed recipes until 100% pass.
- [ ] **Step 3: Coverage assertion across the whole set**

Run: `python3 -c "import json,glob,collections as c; R=[r for f in glob.glob('data/recipes/[!_]*.json') for r in json.load(open(f))]; print('total',len(R)); print(c.Counter(r['displayCategory'] for r in R)); print('hp',sum(r['protein']>=30 for r in R),'quick',sum(r['cookTime']<=20 for r in R))"`
Expected: total ≈50; korean ≥14; hp ≥18; quick ≥10.

- [ ] **Step 4: Commit**

```bash
git add data/recipes/*.json
git commit -m "data: pass adversarial KB review (all rubric gates green)"
```

---

## Task 6: Build script — merge, stats, weeklyPlan, shoppingList, inject

**Files:**
- Create: `scripts/build_data.py`

`build_data.py` must:
1. Load all `data/recipes/[!_]*.json`, concatenate recipes.
2. Compute `metadata.stats` exactly like the current file (totalRecipes, categoryCounts by displayCategory, averageCookTimeMinutes, averageCalories, onePanOnePotRatio/Count where type∈{one-pan,one-pot}, standardCount).
3. Build a coherent default `weeklyPlan` (7 days × {lunch,dinner} = 14 meals) referencing **14 distinct, unique** existing recipe names spread across categories (not 7 names reused across lunch/dinner — the app dedups by name, so reuse makes the default plan visibly repeat dishes).
4. Build `shoppingList` for **schema parity only** — mark it archival in a comment. The app does NOT read `DATA.shoppingList`; `generateShoppingList()` computes the list live from the active weekly plan + `DATA.recipes`. Aggregate ingredients of the `weeklyPlan` recipes into {meat, vegetable, dairy, grain, sauce, etc} as `[{item, amount}]`, but spend no review effort perfecting it.
5. Write `data/structured_data.json` (pretty).
6. Inject: replace the single `const DATA = …;` line in `index.html` with `      const DATA = <minified-json>;` (preserve indentation; minified, no trailing spaces).

- [ ] **Step 1:** Write `scripts/build_data.py` per the spec above (pure stdlib `json`/`re`).
- [ ] **Step 2: Run the build**

Run: `python3 scripts/build_data.py && echo built`
Expected: `built`; `data/structured_data.json` regenerated; `index.html` DATA line replaced.

- [ ] **Step 3: Confirm the DATA line is still a single valid line**

Run: `python3 -c "import re;h=open('index.html').read();l=[x for x in h.splitlines() if 'const DATA =' in x][0];import json;d=json.loads(re.search(r'const DATA =\s*(.+);\s*$',l).group(1));print('recipes',len(d['recipes']))"`
Expected: `recipes` ≈ 50.

- [ ] **Step 4: Commit**

```bash
git add scripts/build_data.py data/structured_data.json index.html
git commit -m "build: add build_data.py; regenerate DATA from new recipes"
```

---

## Task 7: Delete scraped sources

**Files:**
- Delete: `data/recipes_additional.json`, `data/recipes_global.json`, `data/recipes_highprotein.json`, `data/recipes_korean.json`, `data/recipes_youtube.json`

- [ ] **Step 1: Remove the old scraped files** (git history preserves them)

Run: `git rm data/recipes_additional.json data/recipes_global.json data/recipes_highprotein.json data/recipes_korean.json data/recipes_youtube.json`
Expected: 5 files staged for deletion.

- [ ] **Step 2: Commit**

```bash
git commit -m "data: remove scraped recipe sources (replaced by data/recipes/)"
```

---

## Task 8: Validate (integrity gate) + smoke test the app

**Files:** none (may loop back to Task 5/6 on failure)

- [ ] **Step 1: Run the validator**

Run: `python3 scripts/validate.py; echo "exit=$?"`
Expected: `exit=0`, prints `✓ DATA constant — ~50 recipes parsed`, `✓ Recipe data … weeklyPlan references valid`, `✓ No known typo regressions`.

- [ ] **Step 2: If FAIL** — read each error, fix at the source (`data/recipes/*.json`), re-run `scripts/build_data.py`, re-validate. Do NOT hand-edit `index.html`'s DATA line.

- [ ] **Step 3: Mode-coverage smoke test** (mirror the app's filters)

Run: `python3 -c "import re,json;h=open('index.html').read();d=json.loads(re.search(r'const DATA =\s*(.+);\s*$',[x for x in h.splitlines() if 'const DATA =' in x][0]).group(1));R=d['recipes'];print('korean',sum(r['displayCategory']=='korean' for r in R),'hp',sum(r['protein']>=30 for r in R),'quick',sum(r['cookTime']<=20 for r in R))"`
Expected: korean ≥7, hp ≥7, quick ≥7 (targets ≥14/≥18/≥10).

- [ ] **Step 4 (optional): Visual smoke test** — open `index.html` (or use the `run` skill) and confirm recipes render, search works, each weekly-plan mode produces a full 14-meal plan.

---

## Task 9: Update knowledge base & finalize

**Files:**
- Modify: `knowledge/overview.md` (recipe count/description → ~50 original KB-grounded), `knowledge/handoff.md` (Current State + Next Session)

- [ ] **Step 1:** Update `overview.md` facts (recipe count, "original KB-grounded recipes", build step via `scripts/build_data.py`).
- [ ] **Step 2:** Update `handoff.md` Current State / In Flight / Next Session.
- [ ] **Step 3: Commit**

```bash
git add knowledge/overview.md knowledge/handoff.md
git commit -m "memory: update overview/handoff for recipe overhaul"
```

- [ ] **Step 4: Finish the branch** via superpowers:finishing-a-development-branch (merge to main or open PR — user's choice).

---

## Execution notes
- Tasks 4 and 5 are the heavy creative core; everything else is plumbing/gates.
- The two gates are independent and both mandatory: `scripts/validate.py` (machine integrity) and the rubric review (flavor). A recipe is "done" only when it passes both.
- If a mode-coverage assertion fails after review, add/retune recipes in the short category (usually quickmeal or high-protein) rather than weakening the rubric.
