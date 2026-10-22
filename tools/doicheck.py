import sys
sys.path.insert(0, r"C:\Users\HP\Documents\LT-2\tools")
import crossref as cr

CANDS = [
 "10.1257/aer.99.3.710",
 "10.3386/w25363",
 "10.1111/j.1467-9701.2009.01161.x",
 "10.2307/2006905",
 "10.32479/ijeep.14360",
 "10.1016/j.econmod.2021.02.014",
]
for d in CANDS:
    it = cr.by_doi(d)
    if it:
        print(f"OK  {d}")
        print(f"    {(it.get('title') or [''])[0][:90]}")
        print(f"    {cr.authors(it)[:60]} | {cr.year(it)} | {cr.venue(it)[:45]}")
    else:
        print("MISS", d)
