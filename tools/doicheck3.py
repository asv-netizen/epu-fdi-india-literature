import sys
sys.path.insert(0, r"C:\Users\HP\Documents\LT-2\tools")
import crossref as cr

Q = [("Institutional Determinants of Foreign Direct Investment", "benassy"),
     ("Institutional Determinants of Foreign Direct Investment", "quere"),
     ("Determinants of foreign direct investment in developing countries: a meta-analysis", "faeth")]
for t, a in Q:
    print("==", t, "/", a)
    for it in cr.find(t, a, None, rows=8)[:4]:
        print(f"   {it['_title_sim']:.2f} {cr.year(it)} | {(it.get('title') or [''])[0][:75]}")
        print(f"        {cr.authors(it)[:52]} | {cr.venue(it)[:38]} | {it.get('DOI')}")
