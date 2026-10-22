# Data sources

Every link in this file was fetched and checked during this review. Where a check failed, it says so.

---

## 1. Economic Policy Uncertainty — India

- **Page:** <https://www.policyuncertainty.com/india_monthly.html> — **checked, HTTP 200**
- **File:** `https://www.policyuncertainty.com/media/India_Policy_Uncertainty_Data.xlsx` — **checked, downloads, 16.9 kB**
- **Sheets:** `Indian News-Based Index`, `Old EPU and Forecast Data`
- **Columns:** `Year`, `Month`, `India News-Based Policy Uncertainty Index`
- **Coverage in the file:** 286 monthly rows, **January 2003 – September 2026**
- **Your window is covered:** January 2005 – December 2025 sits inside this range.

### Correction to your text

Your research-questions document attributes the India EPU index to **Bhagat, Ghosh and Rangan**. That is not what the data file is.

The attribution printed on the data itself is:

> "Source: 'Measuring Economic Policy Uncertainty' by Scott Baker, Nicholas Bloom and Steven J. Davis at www.PolicyUncertainty.com. These data can be used freely with attribution to the authors, the paper, and the website."

So the India monthly series you plan to use is the **Baker, Bloom & Davis** newspaper-based index. Bhagat, Ghosh & Rangan (2013) is a separate paper, *Economic Policy Uncertainty and Economic Growth in India* (`notes/B-measurement/`). It is worth citing — it is the Indian academic literature on EPU — but it is **not the source of your dependent-independent data series**. Cite Baker, Bloom & Davis (2016) for the index and cite Bhagat, Ghosh & Rangan (2013) for the Indian application.

Get this right in Chapter 3. Attributing a dataset to the wrong authors is the kind of error a panel does not forget.

### ⚠ A methodological break sits inside your sample

The site states:

> "As of April 2014, we are no longer using Consensus Economics forecaster dispersion data and solely constructing indices based on newspaper articles. This has a limited impact upon our overall country-level series, with the old and the new index having a high correlation. For users interesting in comparing the historical performance of the two series, we will continue to supply forecaster dispersion and overall EPU index data up through April 2014."

**April 2014 falls inside your January 2005 – December 2025 window.** Before that date the index combines newspaper text with forecaster dispersion; after it, newspapers only. The `Old EPU and Forecast Data` sheet is there so you can compare.

Do this before you estimate anything:

1. Report the break in the data section of the thesis.
2. Re-run RQ1 with a dummy for the pre/post-April-2014 construction change.
3. Because RQ4 splits the sample into policy periods anyway, check whether your Bai–Perron break dates land near April 2014. If a break appears there, a referee will say it is a measurement break, not an economic one. Have the answer ready.

---

## 2. Economic Policy Uncertainty — Global

- **Page:** <https://www.policyuncertainty.com/global_monthly.html> — **checked, HTTP 200**
- **File:** `https://www.policyuncertainty.com/media/Global_Policy_Uncertainty_Data.xlsx` — **checked, downloads, 18.4 kB**
- **Columns:** `Year`, `Month`, `GEPU_current`, `GEPU_ppp`
- **Coverage in the file:** 357 monthly rows, **January 1997 – July 2026**
- **Two series.** `GEPU_current` is weighted by current-price GDP; `GEPU_ppp` is weighted by PPP GDP. **Say which one you use and why.** For India, PPP weighting gives emerging markets more influence, which is usually the right choice when the question is about a developing-country host. State it as a decision, not a default.
- **Citation printed on the data:** Davis, Steven J., 2016, "An Index of Global Economic Policy Uncertainty", *Macroeconomic Review*, October.

**Note for RQ5:** India is one of the countries inside this index. The de-overlapping step — regress India EPU on global EPU, use the residual — is not optional. See `methodology-key.md`, RQ5.

---

## 3. Geopolitical Risk

- **Page:** <https://www.matteoiacoviello.com/gpr.htm> — **checked, HTTP 200** (page is large, ~11.8 MB)
- **Cite:** Caldara, D. and Iacoviello, M. (2022), "Measuring Geopolitical Risk", *American Economic Review*, 112(4), 1194–1225.
- **Note:** `notes/B-measurement/2022-caldara-measuring-geopolitical-risk.md`
- Country-level GPR series are available on that page, including India.

---

## 4. World Uncertainty Index

- **Page:** <https://worlduncertaintyindex.com/> — **checked, HTTP 200**
- **Cite:** Ahir, H., Bloom, N. and Furceri, D. (2022), "The World Uncertainty Index", NBER Working Paper 29763.
- **Note:** `notes/B-measurement/`
- **Use it only in robustness checks.** WUI measures general uncertainty from country reports; EPU measures policy uncertainty from newspaper text. See `methodology-key.md`, RQ5.

---

## 5. FDI — DPIIT, Government of India

- **DPIIT:** <https://www.dpiit.gov.in/> — **checked, HTTP 200**
- **Open data portal:** <https://data.gov.in/> — **checked, HTTP 200**
- **Note:** <https://fdi.gov.in/> **could not be reached from this network** (connection error). Check it yourself.

### What you need and the condition attached to it

| Series | Needed for | Status |
|---|---|---|
| Gross FDI equity inflows, monthly | Dependent variable | obtain from DPIIT/DBIE |
| Route-wise FDI, monthly (greenfield vs acquisition) | **RQ6** | **verify before you commit to RQ6** |
| Sector-wise FDI, monthly | optional robustness | |

**Gross vs net.** Your text uses **gross** FDI because repatriation was very large in FY24. The Government of India's own discussion of this is the Economic Survey chapter you already have: `papers/Z-existing/2025-india-external-sector-getting-fdi-right.pdf`. That is your citation for the choice.

**The RQ6 condition.** RQ6 requires monthly acquisition data for 2005–2025. DPIIT publishes FDI by *route* (automatic vs government approval) and by *sector*, but **"greenfield vs acquisition" is not a standard DPIIT monthly breakdown**. Before you write RQ6 into a proposal, obtain the actual series and confirm:

1. It exists monthly, not just annually.
2. It starts in 2005 or earlier.
3. The definition of "acquisition" is stable across the whole sample.

If any of these fail, RQ6 cannot be run as designed. See `gap-statement.md`, section 4, for what you should do instead.

---

## 6. Other series

| Series | Source | Status |
|---|---|---|
| India VIX | NSE of India | check yourself |
| VIX (US) | FRED series `VIXCLS` | **could not be reached from this network** — <https://fred.stlouisfed.org/series/VIXCLS> |
| RBI data | <https://www.rbi.org.in/> | **checked, HTTP 200** |
| Real effective exchange rate, WPI/CPI | RBI DBIE | via rbi.org.in |

---

## 7. Summary of checks performed

| Item | Result |
|---|---|
| policyuncertainty.com India monthly page | 200 |
| India EPU Excel file | downloads, 286 rows, 2003-01 to 2026-09 |
| policyuncertainty.com Global monthly page | 200 |
| Global EPU Excel file | downloads, 357 rows, 1997-01 to 2026-07 |
| matteoiacoviello.com/gpr.htm | 200 |
| worlduncertaintyindex.com | 200 |
| dpiit.gov.in | 200 |
| data.gov.in | 200 |
| rbi.org.in | 200 |
| fdi.gov.in | **connection failed — not verified** |
| fred.stlouisfed.org | **connection failed — not verified** |

Everything marked 200 was fetched and its contents read during this review. Everything marked as failed has not been verified and should be checked from your own network.
