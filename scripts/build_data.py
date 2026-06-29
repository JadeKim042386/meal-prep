#!/usr/bin/env python3
"""Build the app's DATA from authored per-category recipe files.

Pipeline:
  data/recipes/<category>.json  (authored source of truth, 6 files)
    -> merge + compute metadata.stats
    -> build a default weeklyPlan (14 distinct recipes) + aggregated shoppingList
    -> write data/structured_data.json (archival, pretty)
    -> inject minified JSON into the `const DATA = ...;` line of index.html

Note: `shoppingList` is ARCHIVAL ONLY. The app does not read DATA.shoppingList;
generateShoppingList() in index.html computes it live from the active weekly plan.
We emit it for schema parity with the old file.

Run: python3 scripts/build_data.py
"""
import json
import re
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECIPES_DIR = ROOT / "data" / "recipes"
OUT_JSON = ROOT / "data" / "structured_data.json"
INDEX = ROOT / "index.html"

DISPLAY_ORDER = ["korean", "western", "asian", "mediterranean", "mexican", "quickmeal"]


def load_recipes() -> list:
    recipes = []
    for f in sorted(RECIPES_DIR.glob("[!_]*.json")):
        recipes.extend(json.loads(f.read_text(encoding="utf-8")))
    if not recipes:
        raise SystemExit("No recipes found in data/recipes/*.json")
    return recipes


def build_stats(recipes: list) -> dict:
    n = len(recipes)
    cat_counts = {}
    for r in recipes:
        dc = r["displayCategory"]
        cat_counts[dc] = cat_counts.get(dc, 0) + 1
    one_pan_pot = sum(1 for r in recipes if r.get("type") in ("one-pan", "one-pot"))
    standard = sum(1 for r in recipes if r.get("type") == "standard")
    avg_cook = round(sum(r["cookTime"] for r in recipes) / n, 1)
    avg_cal = round(sum(r["calories"] for r in recipes) / n, 1)
    return {
        "totalRecipes": n,
        "categoryCounts": {k: cat_counts.get(k, 0) for k in DISPLAY_ORDER},
        "averageCookTimeMinutes": avg_cook,
        "averageCalories": avg_cal,
        "onePanOnePotRatio": f"{round(100 * one_pan_pot / n, 1)}%",
        "onePanOnePotCount": one_pan_pot,
        "standardCount": standard,
    }


def build_weekly_plan(recipes: list) -> dict:
    """Meal-prep batch model (1 serving per meal slot): pick just enough
    recipes that their servings cover the 14 weekly meals (~4 for 4-serving
    recipes), then round-robin them across slots so repeats are spread out.
    Cooking one batch of each then covers the week with minimal leftover."""
    by_name = {r["name"]: r for r in recipes}
    by_cat = {k: [] for k in DISPLAY_ORDER}
    for r in recipes:
        by_cat[r["displayCategory"]].append(r["name"])
    # category-spread candidate order
    order = []
    while any(by_cat.values()):
        for k in DISPLAY_ORDER:
            if by_cat[k]:
                order.append(by_cat[k].pop(0))
    TOTAL = 14
    picks, covered = [], 0
    for name in order:
        if covered >= TOTAL:
            break
        picks.append(name)
        covered += by_name[name].get("servings", 1)
    if not picks:
        raise SystemExit("No recipes available to build a weekly plan")
    # servings-capped round-robin: place one meal per recipe each pass while
    # its remaining servings allow it, so repeats spread out and no recipe
    # appears more than `servings` times (unless the pool can't cover 14).
    cap = {n: by_name[n].get("servings", 1) for n in picks}
    order = []
    while len(order) < TOTAL:
        placed = False
        for n in picks:
            if len(order) >= TOTAL:
                break
            if cap[n] > 0:
                order.append(n)
                cap[n] -= 1
                placed = True
        if not placed:
            for n in picks:
                if len(order) >= TOTAL:
                    break
                order.append(n)
    days = ["monday", "tuesday", "wednesday", "thursday",
            "friday", "saturday", "sunday"]
    slots = [(d, m) for d in days for m in ("lunch", "dinner")]
    plan = {}
    for i, (day, meal) in enumerate(slots):
        plan.setdefault(day, {})[meal] = order[i]
    return plan


# --- archival shopping-list aggregation -------------------------------------
BUCKET_KEYWORDS = {
    "meat": ["닭", "소고기", "돼지", "삼겹", "베이컨", "고기", "새우", "연어", "고등어",
             "참치", "두부", "달걀", "계란", "어묵", "오징어", "햄"],
    "vegetable": ["양파", "대파", "쪽파", "마늘", "생강", "버섯", "표고", "느타리", "양배추",
                  "당근", "애호박", "호박", "감자", "고구마", "무", "시금치", "브로콜리",
                  "가지", "파프리카", "고추", "토마토", "양상추", "오이", "콩나물", "부추",
                  "깻잎", "고수", "바질", "민트", "레몬그라스", "olive", "올리브", "콩",
                  "병아리콩", "렌틸", "옥수수", "피망", "셀러리", "라임", "레몬"],
    "dairy": ["우유", "크림", "버터", "치즈", "요거트", "파르미지아노", "코티하", "모짜렐라",
              "생크림", "사워크림"],
    "grain": ["밥", "쌀", "현미", "면", "파스타", "오르조", "쿠스쿠스", "보리", "또띠야",
              "토르티야", "우동", "곤약", "빵", "또띠아", "누룽지"],
    "sauce": ["간장", "고추장", "된장", "굴소스", "피쉬소스", "느억맘", "두반장", "소스",
              "식초", "맛술", "미린", "청주", "와인", "참기름", "들기름", "식용유", "올리브유",
              "설탕", "올리고당", "물엿", "조청", "꿀", "소금", "후추", "고춧가루", "가루",
              "타히니", "수막", "하리사", "커리", "페이스트", "쌈장", "마요네즈", "머스터드",
              "케첩", "발사믹", "액젓", "다시", "다시마", "가쓰오부시", "통깨", "참깨"],
}


def classify(name: str) -> str:
    for bucket, kws in BUCKET_KEYWORDS.items():
        if any(kw in name for kw in kws):
            return bucket
    return "etc"


def split_item(line: str):
    m = re.match(r"^(.+?)\s+([\d/.~][^ ]*.*)$", line.strip())
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return line.strip(), ""


def build_shopping_list(recipes: list, plan: dict) -> dict:
    # Deterministic order (day -> lunch/dinner) so re-runs are byte-stable.
    days = ["monday", "tuesday", "wednesday", "thursday",
            "friday", "saturday", "sunday"]
    used_names = []
    for day in days:
        for meal in ("lunch", "dinner"):
            name = plan[day][meal]
            if name not in used_names:
                used_names.append(name)
    by_name = {r["name"]: r for r in recipes}
    buckets = {k: {} for k in ["meat", "vegetable", "dairy", "grain", "sauce", "etc"]}
    for name in used_names:
        for line in by_name[name]["ingredients"]:
            item, amount = split_item(line)
            b = classify(item)
            if item not in buckets[b]:
                buckets[b][item] = amount
    return {b: [{"item": it, "amount": amt} for it, amt in items.items()]
            for b, items in buckets.items()}


def inject_into_index(data: dict) -> None:
    minified = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    lines = INDEX.read_text(encoding="utf-8").splitlines(keepends=True)
    target_i = next((i for i, ln in enumerate(lines) if "const DATA =" in ln), None)
    if target_i is None:
        raise SystemExit("Could not find 'const DATA =' line in index.html")
    indent = re.match(r"\s*", lines[target_i]).group(0)
    newline = "\n" if lines[target_i].endswith("\n") else ""
    lines[target_i] = f"{indent}const DATA = {minified};{newline}"
    INDEX.write_text("".join(lines), encoding="utf-8")


def main() -> None:
    recipes = load_recipes()
    plan = build_weekly_plan(recipes)
    data = {
        "metadata": {
            "createdAt": datetime.date.today().isoformat(),
            "totalRecipes": len(recipes),
            "stats": build_stats(recipes),
        },
        "recipes": recipes,
        "weeklyPlan": plan,
        "shoppingList": build_shopping_list(recipes, plan),
    }
    OUT_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    inject_into_index(data)
    print(f"✓ Built {len(recipes)} recipes -> data/structured_data.json + index.html")
    print(f"  weeklyPlan: {len({n for d in plan.values() for n in d.values()})} distinct recipes")
    print(f"  stats: {data['metadata']['stats']}")


if __name__ == "__main__":
    main()
