"""Index the PDFs already on this machine: copy into repo, verify metadata, write notes."""
import os
import re
import sys
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paperkit as pk
import crossref as cr
import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = r"C:\Users\HP\Documents\Literature-Review"
DST = os.path.join(ROOT, "papers", "Z-existing")
NOTES = os.path.join(ROOT, "notes", "Z-existing")
os.makedirs(DST, exist_ok=True)
os.makedirs(NOTES, exist_ok=True)

# filename -> (search title, known DOI, rq, why, fallback citation)
LIB = {
 "1-s2.0-S1925209924002262-main.pdf": (
   "Macroeconomic impact of FDI inflows: an ARDL approach for the case of India", "10.1080/19186444.2017.1362860", "RQ1",
   "Prior Indian ARDL work on FDI with GDP, exports and the exchange rate, with no uncertainty term. Useful as the local method precedent: it shows ARDL is accepted on Indian FDI data, and its control set is a defensible starting point.", None),
 "201364pap.pdf": (
   "Policy Uncertainty, Irreversibility, and Cross-Border Flows of Capital", "", "theory, RQ6",
   "The mechanism paper for your RQ6 logic: FDI falls before elections while portfolio flows do not, and the effect is stronger where policy reversal is more likely. Direct evidence that irreversibility, not uncertainty alone, drives the result.",
   ("Brandon Julio, Youngsuk Yook", 2013, "Finance and Economics Discussion Series 2013-64, Federal Reserve Board")),
 "2019rwp-144.pdf": (
   "Policy Uncertainty and FDI Flows: The Role of Institutional Quality and Financial Development", "", "RQ1, RQ5",
   "Bilateral OECD panel with election timing as an instrument for policy uncertainty. The cleanest identification in the EPU-FDI literature and the benchmark your India elasticity should be compared with.",
   ("Sangyup Choi, Davide Furceri, Chansik Yoon", 2019, "Yonsei Economic Research Institute Working Paper 2019-144")),
 "2023MZKFQJPEconomicPolicyUncertaintyandFDI.pdf": (
   "Economic Policy Uncertainty and FDI Flows: Evidence from India", "", "RQ1",
   "The incumbent India EPU-FDI study: linear ARDL, 2003-2022, negative long-run effect. Your thesis must state exactly what it adds beyond this paper.",
   ("Mohammad Zain Khan, Furqan Qamar", 2023, "Journal of the Asiatic Society of Mumbai 97(8)")),
 "2025_08_08_Thapa_et_al_Uncertainty_final.pdf": (
   "Policy information uncertainty and foreign institutional investors trading behavior: evidence from India", "10.1007/s11156-025-01448-8", "RQ3, RQ5",
   "Transaction-level evidence that foreign institutional investors withdraw within days of a tax-policy announcement. Useful precisely because FII is fast and reversible: it shows why FDI, the slow and costly flow, needs a different model.", None),
 "6_Akbakay.pdf": (
   "Policy Uncertainty and Foreign Direct Investment: The Moderating Role of Institutional Quality", "10.15388/Ekon.2026.105.1.6", "RQ5",
   "37 developing countries, 2002-2021, system GMM, WUI as the uncertainty measure. Institutional quality weakens the negative EPU effect, which is the empirical basis for your RQ4 prediction A.", None),
 "Asymmetric impact of economic policy uncertainty on cryptocurrency market_ Evidence from NARDL approach - ScienceDirect.pdf": (
   "Asymmetric impact of economic policy uncertainty on cryptocurrency market: Evidence from NARDL approach", "10.1016/j.jeca.2023.e00298", "RQ2",
   "A NARDL template rather than a substantive source: it shows the partial-sum decomposition, long- and short-run asymmetry tests and dynamic multipliers in a published paper. Do not cite it for macro claims.", None),
 "Azam2012_Article_ImpactOfPoliticalRiskAndUncert.pdf": (
   "Impact of Political Risk and Uncertainty on FDI in South Asia", "10.1007/s11300-012-0230-x", "RQ1, RQ5",
   "South Asia ARDL study with hand-built political-risk and macro-policy-uncertainty indices. The closest regional precedent and a source of control variables.", None),
 "EPU_BBD_Mar2016.pdf": (
   "Measuring Economic Policy Uncertainty", "10.1093/qje/qjw024", "all",
   "The EPU index paper, already in your folder. Use it for the construction description, the newspaper-count validation and the known criticisms of the index.", None),
 "IJRPR61698.pdf": (
   "Impact of Economic Policy Uncertainty and Market Volatility on Equity, Exchange Rate and Commodity Markets", "", "RQ5",
   "India EPU transmission to equity, FX and commodity markets. Low-tier outlet, so cite it only as supporting evidence that domestic EPU moves Indian asset prices.",
   ("Dhriti Kumari, Anusha S. Sangondimath", 2026, "International Journal of Research Publication and Reviews 7(4)")),
 "Macroeconomic_Dynamics_of_Foreign_Direct_Investmen.pdf": (
   "Macroeconomic Dynamics of Foreign Direct Investment in India: An Empirical Analysis", "10.17492/pragati.v5i2.14372", "RQ1",
   "India ARDL determinants study with a financial-crisis dummy. Shows how a single break dummy is normally handled, which is the approach your Bai-Perron dates improve on.", None),
 "RBIWPSNO42020A9ED64431A6143E0B5FD7767B715E1F7.pdf": (
   "Macroeconomic Effects of Uncertainty: A Big Data Analysis for India", "", "RQ3",
   "The closest Indian methodological precedent for RQ3: text-mined uncertainty indices plus local projections. Official RBI research, so it is hard for a panel to dismiss.",
   ("Nalin Priyaranjan, Bhanu Pratap", 2020, "RBI Working Paper Series WPS (DEPR) 04/2020")),
 "Rev International Economics - 2022 - Jardet - Foreign direct investment under uncertainty evidence from a large panel of.pdf": (
   "Foreign direct investment under uncertainty: evidence from a large panel of countries", "10.1111/roie.12646", "RQ5",
   "Finds global uncertainty matters more than host-country uncertainty, and that high uncertainty matters disproportionately. The exact claim RQ5 tests for India, and the source of your nonlinearity argument.", None),
 "Uncertainty_Financial_Development_and_FDI_Inflows_.pdf": (
   "Uncertainty, Financial Development and FDI Inflows: France Evidence", "10.20448/journal.518.2021.6.7.13", "RQ1",
   "Single-country ARDL with both EPU and WUI as regressors. Useful for the RQ5 point that EPU and WUI are not interchangeable.", None),
 "Volume+15,+Issue+4-3.pdf": (
   "Economic Policy Uncertainty and Institutional Credibility: Assessing the Role of Central Bank Independence in Maintaining Financial Stability", "10.54560/jracr.v15i4.694", "RQ5",
   "Peripheral: EPU and financial stability, not FDI. Keep it only if you discuss institutional credibility as a conditioning channel.", None),
 "echap03.pdf": (
   "External Sector: Getting FDI Right", "", "data",
   "Official Government of India discussion of gross versus net FDI and the repatriation surge in FY24-FY25. This is the citation for your choice of gross FDI over net FDI.",
   ("Government of India, Ministry of Finance", 2025, "Economic Survey 2024-25, Chapter 3")),
 "economies-13-00147.pdf": (
   "Uncertainty, FDI Inflows, and Financial Market Development: Empirical Evidence", "10.3390/economies13060147", "RQ1",
   "75 emerging markets, PMG estimation, and a positive long-run EPU-FDI coefficient. Important counter-evidence: it stops you claiming the negative sign is universal.", None),
 "jrfm-18-00354.pdf": (
   "Economic Policy Uncertainty and China's FDI Inflows: Moderating Effects of Financial Development and Political Stability", "10.3390/jrfm18070354", "RQ5",
   "Separates global EPU from China's own EPU and reports both reduce inflows. A direct template for the RQ5 horse race.", None),
 "mlpezgarcia,+6971-Article+Text-28364-1-20220331.pdf": (
   "Do Geopolitical Risk Factors and Economic Policy Uncertainties Stimulate Capital Outflows? An Updated Evidence", "10.25115/eea.v40i3.6971", "RQ5",
   "GPR and EPU effects on capital flight from South Africa. Marginal for India but usable to argue GPR and EPU act through different channels.", None),
 "sustainability-14-12609-v4.pdf": (
   "Do Uncertainty and Financial Development Influence the FDI Inflow of a Developing Nation? A Time Series ARDL Approach", "10.3390/su141912609", "RQ1",
   "Pakistan ARDL study with EPU and financial development. A South Asian comparator with a similar sample length.", None),
 "sustainability-15-06131.pdf": (
   "The Effect of Economic Policy Uncertainty on Foreign Direct Investment in the Era of Global Value Chain: Evidence from the Asian Countries", "10.3390/su15076131", "RQ1, RQ5",
   "Asian panel evidence with global value chain participation. Relevant to RQ5 because it separates domestic from global uncertainty exposure.", None),
 "working-paper-1324-macro-financial-impact-economic-policy-uncertainty-latin-america.pdf": (
   "The macro-financial impact of economic policy uncertainty in Latin America", "", "RQ3, RQ5",
   "BIS panel local-projection study for four Latin American economies. A high-quality example of EPU shocks traced month by month, and a model for your RQ3 presentation.",
   ("Ana Aguilar, Rafael Guerra, Carola Mueller, Alexandre Tombini", 2026, "BIS Working Paper 1324")),
 "1004139261.pdf": (
   "Does Financial Stability Withstand Economic Policy Uncertainty? Insights From Linear and Nonlinear Patterns", "10.1002/pa.70098", "RQ2",
   "Documents a nonlinear, even sign-switching, EPU effect. Useful for the nonlinearity-versus-asymmetry distinction, though the outcome is financial stability rather than FDI.", None),
 "2-strr.pdf": (
   "FDI Spillovers in Emerging Markets: Does Economic Policy Uncertainty and Geopolitical Risk Matter?", "10.15388/omee.2025.16.11", "RQ5",
   "BRICS TVP-VAR spillover study that includes India. Evidence that EPU and GPR are transmitted across borders, which underpins the global-EPU regressor in RQ5.", None),
 "10.22034_nasmea.2026.243845.pdf": (
   "Does economic policy uncertainty drive foreign direct investment inflows? Evidence from South Africa", "", "RQ4, RQ5",
   "Time-varying connectedness between EPU and FDI in an emerging market. Supports the RQ4 premise that the relation is not constant across the sample.",
   ("Babatunde Lawrence, Fabian Moodley, Sune Ferreira-Schenk", 2026, "New Applied Studies in Management, Economics & Accounting 9")),
 "10.30586-pek.1942446-5970845.pdf": (
   "Long-run Impacts of Geopolitical Risk and Economic Policy Uncertainty on Foreign Direct Investments in Turkey", "10.30586/pek.1942446", "RQ1, RQ5",
   "Long-run EPU and GPR effects on FDI with structural-change-robust methods. The closest single-country analogue for the RQ1 plus RQ5 combination.", None),
}


def pdf_doi(path):
    try:
        d = pymupdf.open(path)
        txt = "".join(d[i].get_text() for i in range(min(3, d.page_count)))
        d.close()
    except Exception:
        return ""
    m = re.findall(r"10\.\d{4,9}/[^\s<>\"]+", txt)
    for c in m:
        c = c.rstrip(".,;)")
        if "doi.org" not in c and len(c) > 8:
            return c
    return ""


if __name__ == "__main__":
    seen = set()
    for fn, (title, doi, rq, why, manual) in LIB.items():
        src = os.path.join(SRC, fn)
        if not os.path.exists(src):
            import glob
            g = glob.glob(os.path.join(SRC, fn[:12] + "*"))
            if g:
                src = g[0]
            else:
                print("MISSING FILE", fn)
                continue
        it = cr.by_doi(doi) if doi else None
        if it is None:
            pd = pdf_doi(src)
            it = cr.by_doi(pd) if pd else None
        if it is None:
            cand = cr.best(title, "", None)
            if cand and cand["_title_sim"] >= 0.72:
                it = cand
        if it:
            disp = (it.get("title") or [title])[0]
            meta = dict(authors=cr.authors(it), year=cr.year(it), venue=cr.venue(it),
                        doi=it.get("DOI"), cites=it.get("is-referenced-by-count"))
        elif manual:
            meta = dict(authors=manual[0], year=manual[1], venue=manual[2], doi="", cites=None)
            disp = title
        else:
            print("UNRESOLVED", fn)
            continue
        first = (meta["authors"].split(",")[0] or "anon").split()[-1]
        base = f"{meta['year'] or 'nd'}-{pk.slug(first,18)}-{pk.slug(disp,70)}"
        if base in seen:
            continue
        seen.add(base)
        dst = os.path.join(DST, base + ".pdf")
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
        d = pymupdf.open(dst)
        pages = d.page_count
        d.close()
        abstract = pk.pdf_abstract(dst)
        note = f"""# {disp}

**Authors:** {meta['authors']}
**Year:** {meta['year']}
**Outlet:** {meta['venue']}
**DOI:** {meta['doi'] or '—'}
**PDF:** `papers/Z-existing/{os.path.basename(dst)}` ({pages} pages)
**Research questions:** {rq}
**Status:** already in your library before this review.

## Abstract (extracted from the PDF)

> {abstract.strip() or '_No abstract paragraph could be extracted automatically. Read the first page of the PDF._'}

## Why it matters

{why}

## Note

Copied from `C:\\Users\\HP\\Documents\\Literature-Review` so the literature folder is self-contained.
"""
        open(os.path.join(NOTES, base + ".md"), "w", encoding="utf-8").write(note)
        print("OK", base)
