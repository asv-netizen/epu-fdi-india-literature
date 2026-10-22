import sys, requests, re
sys.path.insert(0, r"C:\Users\HP\Documents\LT-2\tools")
import crossref as cr

def title_query(title, rows=20):
    for i in range(3):
        try:
            r = requests.get("https://api.crossref.org/works",
                             params={"query.title": title, "rows": rows,
                                     "mailto": "lit-review@example.org"},
                             headers=cr.UA, timeout=45)
            if r.status_code == 200:
                return r.json()["message"]["items"]
        except Exception:
            pass
    return []

Q = ["Simultaneous Confidence Intervals for Impulse Responses to Multiple Shocks",
     "Economic Policy Uncertainty in China Since 1949",
     "Determinants of Foreign Direct Investment in Developing Countries Meta-Analysis",
     "On the Sign of the Investment Uncertainty Relationship"]
for t in Q:
    print("=" * 90)
    print(t)
    items = title_query(t)
    tn = cr.norm(t)
    scored = sorted(items, key=lambda it: -cr._sim(tn, cr.norm((it.get("title") or [""])[0])))
    for it in scored[:5]:
        print(f"  {cr._sim(tn, cr.norm((it.get('title') or [''])[0])):.2f} {cr.year(it)} | {(it.get('title') or [''])[0][:80]}")
        print(f"       {cr.authors(it)[:55]} | {cr.venue(it)[:40]} | {it.get('DOI')}")
