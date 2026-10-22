import json, sys
state = json.load(open(r"C:\Users\HP\Documents\LT-2\tools\acquired.json", encoding="utf-8"))
rows = sorted(state.values(), key=lambda v: (v.get("cat") or "", v.get("year") or 0))
for v in rows:
    print(f"{v.get('cat'):22} {str(v.get('year')):6} {(v.get('title') or '')[:88]}")
    print(f"{'':22} {(v.get('authors') or '')[:60]} | pdf={'Y' if v.get('ok') else '-'} abs={'Y' if v.get('has_abstract') else '-'}")
