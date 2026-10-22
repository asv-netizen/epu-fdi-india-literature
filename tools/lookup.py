import sys
sys.path.insert(0, r"C:\Users\HP\Documents\LT-2\tools")
import crossref as cr

Q = [
 ("Simultaneous Confidence Intervals for Impulse Responses to Multiple Shocks", "jorda"),
 ("Economic Policy Uncertainty in China Since 1949", "davis"),
 ("Determinants of Foreign Direct Investment in Developing Countries: A Meta-Analysis", "faeth"),
 ("Revisiting the Nexus between Economic Policy Uncertainty, Financial Development, and FDI Inflows", ""),
 ("On the Sign of the Investment-Uncertainty Relationship", "caballero"),
]
for title, au in Q:
    print("=" * 90)
    print(title)
    for it in cr.find(title, au, None, rows=12)[:8]:
        print(f"  {it['_title_sim']:.2f} {cr.year(it)} | {(it.get('title') or [''])[0][:78]}")
        print(f"       {cr.authors(it)[:55]} | {cr.venue(it)[:38]} | {it.get('DOI')}")
