# Recipe Design Rubric & Schema Contract

Shared standard for every recipe authored in the overhaul (see plan `2026-06-28-recipe-overhaul.md`, decision [[ADR 0004 Recipe Overhaul]]). Generators author *to* this; reviewers score *against* it. A recipe is DONE only when it passes every gate **and** `scripts/validate.py` passes.

---

## 1. The Rubric (all gates must pass)

### Flavor gates (G) — grounded in `knowledge/cooking/`
- **G1 Seasoning calibrated & layered** — explicit salt target ≈0.8–1% of main-component weight; salt applied in layers (season protein, season veg, adjust at end), never one dump. → `principles/seasoning-and-salting`
- **G2 Acid present, usually finishing** — ≥1 acid element; bright acids added late for lift. → `flavor/acidity-and-brightness`, `principles/balancing-flavors`
- **G3 Umami layered** — ≥2 umami sources, exploiting glutamate×nucleotide synergy where natural (간장+다시마/표고/토마토/멸치/파르미지아노). → `flavor/umami-and-synergy`, `ingredients/umami-boosters`
- **G4 Browning / depth step** — a Maillard sear, caramelization, fond+deglaze, or aromatic bloom where the dish allows. → `techniques/maillard-caramelization`, `principles/building-depth-and-layering`
- **G5 Fat as carrier, balanced** — right fat for aroma/richness, cut by G2 acid so it never cloys. → `flavor/fat-as-flavor-carrier`
- **G6 Texture contrast** — ≥1 textural counterpoint (crisp topping, seared edge, fresh crunch). → `principles/texture-and-mouthfeel`
- **G7 Aromatic finish** — fresh herb / zest / aromatic oil / scallion / toasted seed at the end. → `creativity/composing-a-dish`
- **G8 Grammar coherence** — every seasoning fits the dish's cuisine grammar; no incoherent mash. → matching `flavor-grammars/<cuisine>`
- **G9 Composition complete** — fills slots base+sauce+fat+acid+crunch+aroma. → `creativity/composing-a-dish`

### Meal-prep gates (M)
- **M1 Batch & store** — scales to `servings` (default 4); `storageInfo` states fridge days (3–5) and what to store separately.
- **M2 Reheats/holds** — no textures that die on reheat unless the recipe isolates them (crunch/fresh element added at serving, stated in steps + storageInfo).
- **M3 Make-ahead technique** — e.g. dress grains while warm, keep sauces/crunch separate, choose cuts that stay moist. → `techniques/marination-tenderizing`, `techniques/moist-heat-methods`
- **M4 Standalone meal** — every recipe is a complete one-dish meal you can eat on its own (protein + carb/veg, e.g. 덮밥/보울/볶음밥/면/시트팬 한 접시). NO side dishes (반찬/밑반찬/나물/곁들임/장아찌/single-component sides). If it would normally be eaten *with* rice, the recipe must include the rice/grain as part of the dish.

### Data gates (D)
- **D1 Purchasable ingredients** — every `ingredients` line is buyable as written, with an amount. No composites (`전분물` etc.); write slurry in *steps* as parts (`감자전분 1큰술 + 물 2큰술`), never as an ingredient line.
- **D2 Specific, technique-cued steps** — each step names heat level / time / a visual or temperature cue; 5–9 steps; final step covers portioning, cooling, storage.
- **D3 Plausible macros** — `calories/protein/carbs/fat` roughly consistent with ingredients ÷ `servings`; `protein` realistic grams per serving.
- **D4 Schema valid** — all required fields present; enums respected; unique `name`; no typo-guard hits.
- **D5 Simple & fast** — `cookTime` ≤ 20 (minutes) AND ≤ 10 ingredient lines total (including seasonings; lean on shared pantry staples). Fast/simple is NOT an excuse for flat — all flavor gates G1–G9 still apply.

**Scoring:** each gate = pass/fail + one-line justification; every fail needs a concrete fix. Reviewers default to FAIL when unconvinced and cite KB notes by exact title.

---

## 2. Hard constraints (validate.py + app behavior)

- **Required fields:** `name, category, type, ingredients, cookTime, calories, protein, steps, displayCategory`. Always also include: `difficulty, source, sourceName, tags, servings, storageInfo, carbs, fat`.
- `displayCategory` ∈ {`korean`,`western`,`asian`,`mediterranean`,`mexican`,`quickmeal`}.
- `type` ∈ {`one-pan`,`one-pot`,`sheet-pan`,`standard`}.
- `cookTime, protein, calories, carbs, fat` numeric. `protein` in grams.
- `name` unique across the whole set (no `variant` fields).
- `source` = `"원본 레시피 (meal-prep KB 기반 설계)"`; `sourceName` = `"meal-prep KB"`.
- `category` = internal grouping; set it equal to `displayCategory` for new recipes.
- **Typo guard — never emit:** `키친타올`(→키친타월), `후라이한다`(→프라이한다), `소세지`(→소시지), `달걸`(→달걀).
- Bodies/steps in Korean (this is a Korean app); identifiers Korean.
- **Every recipe ≤ 20 min cookTime and ≤ 10 ingredient lines (D5).**
- **No side dishes — meals only (M4).** Do not emit `반찬`/`밑반찬`/`나물`/`사이드`/`곁들임` tags.

### Mode coverage (set-level, not per recipe)
The app generates weekly plans live from `DATA.recipes`. Keep:
- `displayCategory==='korean'` ≥14 (korean mode; app filter is `displayCategory==='korean' || category==='korean'`).
- `protein>=30` ≥18 (highprotein mode).
- `cookTime<=20` — now ALL recipes (quick mode pool = whole set). Keep the `quickmeal` displayCategory dishes as a shared-pantry family so the 초간편 ingredient-similarity clusterer can still group them.
- All recipes are mains (M4), so `isSideDish` excludes nothing — the weekly-plan pool is the full set.

---

## 3. Schema contract — fully-populated example

A model recipe that passes every gate (use as the field/shape reference, not as a recipe to ship):

```json
{
  "name": "들기름 간장 버섯 닭다리살 덮밥",
  "category": "korean",
  "displayCategory": "korean",
  "type": "one-pan",
  "ingredients": [
    "닭다리살 600g",
    "표고버섯 6개 (약 150g)",
    "느타리버섯 200g",
    "대파 1대",
    "마늘 5쪽",
    "양파 1/2개",
    "간장 3큰술",
    "굴소스 1큰술",
    "맛술 2큰술",
    "들기름 2큰술",
    "설탕 1작은술",
    "통깨 1큰술",
    "쪽파 3대",
    "현미밥 4공기"
  ],
  "cookTime": 25,
  "difficulty": "쉬움",
  "calories": 520,
  "protein": 34,
  "carbs": 58,
  "fat": 16,
  "steps": [
    "닭다리살 600g은 키친타월로 물기를 제거하고 한입 크기로 썬 뒤 소금 1/2작은술(고기 무게의 약 0.8%)과 후추로 밑간해 10분 둔다.",
    "표고버섯 6개는 도톰하게 저미고 느타리버섯 200g은 손으로 찢는다. 양파 1/2개는 채 썰고, 대파 1대와 마늘 5쪽은 다진다.",
    "간장 3큰술·굴소스 1큰술·맛술 2큰술·설탕 1작은술을 섞어 양념장을 만든다(우마미: 간장+표고+굴소스 다중 레이어).",
    "팬을 센 불에 충분히 달군 뒤 식용유를 두르고 닭다리살을 껍질 쪽부터 펼쳐 넣어 3~4분간 노릇하게 시어한다(Maillard, 뒤집지 말 것).",
    "고기를 한쪽으로 밀고 대파·마늘을 들기름 1큰술에 30초 볶아 향을 낸 뒤(파기름) 버섯과 양파를 넣어 수분이 날아갈 때까지 3분 볶는다.",
    "양념장을 팬 가장자리로 둘러 부어 끓이며 1~2분 졸여 윤기를 낸다.",
    "불을 끄고 들기름 1큰술과 통깨를 둘러 마무리한다(향 마무리).",
    "용기 4개에 현미밥을 담고 덮밥 건더기를 1/4씩 올린다. 쪽파는 따로 담아 먹기 직전 올린다(질감·향 보존). 한 김 식혀 냉장 보관, 3~4일 내 섭취."
  ],
  "source": "원본 레시피 (meal-prep KB 기반 설계)",
  "sourceName": "meal-prep KB",
  "tags": ["원팬", "닭다리살", "고단백", "덮밥", "버섯", "들기름"],
  "servings": 4,
  "storageInfo": "냉장 3~4일. 밥과 건더기 함께 보관 가능, 쪽파·통깨는 먹기 직전 추가 권장."
}
```

Notes on why it passes: G1 salt 0.8% + layered; G2 맛술 + finishing freshness; G3 간장+표고+굴소스 umami stack; G4 껍질 시어 + 파기름; G5 들기름 carrier; G6 쪽파/시어 표면 대비; G7 들기름+통깨+쪽파 finish; G8 한식 양념 문법 일관; G9 base(밥+닭+버섯)+sauce(양념장)+fat(들기름)+acid/brightness(맛술·쪽파)+crunch(통깨/쪽파)+aroma. M1–M3 met; D1–D4 met.
