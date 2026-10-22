# EPU and FDI in India: the six research questions in simple English

This text is written in ASD-STE100 Simplified Technical English (simmi). It is descriptive text: short sentences, one topic for each sentence. The technical content is the same as in the full version.

---

## 1. The important terms

You must know these terms before you read the research questions. Each research question uses them.

- **EPU (Economic Policy Uncertainty):** EPU is an index. It shows how sure or not sure companies are about the decisions that the government will make on tax, spending, interest rates, and rules. For India, the index counts newspaper articles that contain words about the economy, policy, and uncertainty (Bhagat, Ghosh and Rangan).
- **FDI (Foreign Direct Investment):** FDI is money that a company from a different country puts into India. With FDI, the company gets 10% or more of the ownership, and it gets control.
- **FII (Foreign Institutional Investment):** FII is different from FDI. It is money that goes into Indian shares and bonds, and it can go out again in one day. This thesis does not study FII.
- **Gross FDI and net FDI:** Gross FDI is all the FDI money that comes into India. Net FDI is gross FDI minus the money that foreign companies take out. This thesis uses gross FDI, because in FY24 the money taken out was very large.
- **GPR (Geopolitical Risk):** GPR is an index of the risk of wars, terror attacks, and conflicts between countries. It is not the same as EPU.
- **Global EPU:** Global EPU is an average of the EPU indices of many countries. India is one of these countries.
- **WUI and VIX:** WUI (World Uncertainty Index) measures general economic uncertainty. VIX shows how much traders think that US share prices will move in the next 30 days. They are not the same as EPU.
- **Elasticity (β):** An elasticity is a percentage effect. If β is −0.2, a 1% increase in EPU causes a 0.2% decrease in FDI.
- **Shock:** A shock is a sudden change in EPU that persons did not think would occur.

### Three pairs of terms that are not the same

A viva panel will frequently ask about these differences. Thus, it is important that you know them.

- **Long run and long horizon:** The long run is the equilibrium relation between EPU and FDI over many years. A long horizon is a number of months after one shock, for example 24 months. They are two different things.
- **Asymmetry, nonlinearity, and regime change:** Asymmetry means that an increase in EPU and a decrease of the same size have different effects. Nonlinearity means that the effect changes with the level of EPU. Regime change means that the full relation changes at a specified date.
- **Gradual change and structural break:** A gradual change occurs slowly over many years. A structural break is a sudden change at one date, for example the 2008 crisis or COVID in 2020.

### The theory in short

A factory costs much money, and it is not easy to sell again. Thus, when a company is not sure about the rules that will come, it is better to wait. This is the "wait-and-see" effect of real options theory (Bernanke 1983, Dixit and Pindyck 1994).

Hysteresis means that the damage stays. When uncertainty increases, some companies stop their projects or go out of India. When uncertainty decreases again, not all of them go into India again, because entry costs much money a second time (Dixit 1989). Hysteresis is the theory behind the asymmetry in this thesis.

---

## 2. The six research questions

All six questions use monthly data from January 2005 to December 2025 (252 months). The dependent variable is the log of real gross FDI equity inflows from DPIIT.

### RQ1. Is there a long-run relation? (level)

**The question:** Is there a long-run relation between India EPU and FDI that continues when the model includes structural breaks? What is its elasticity (β)?

**The method:**
- Zivot–Andrews and Fourier ADF tests examine each series for a unit root with breaks.
- Bai–Perron tests find the dates of the structural breaks.
- An ARDL bounds test (Pesaran et al. 2001) examines if a long-run relation exists.
- Kripfganz–Schneider critical values make the bounds test accurate for a sample of 252 months.

**The result that the thesis tests (H1):** β is negative and significant. More policy uncertainty causes less FDI over many years.

**Why it is important:** All the other questions use this result as their base.

### RQ2. Do increases and decreases have different effects? (asymmetry)

**The question:** Do increases in EPU and decreases in EPU have different effects on FDI, in the long run and in the short run?

**The method:**
- NARDL (Shin, Yu and Greenwood-Nimmo 2014) divides EPU into two series. EPU⁺ adds all the monthly increases. EPU⁻ adds all the monthly decreases.
- The model then gives two long-run effects: β⁺ for increases and β⁻ for decreases.
- A Wald test examines if "β⁺ = β⁻". The thesis does this test separately for the long run and for the short run.
- A bootstrap gives more accurate p-values for these tests.
- Dynamic multipliers show the path of each effect, month after month.

**The result that the thesis tests (H2):** "|β⁺| > |β⁻|". An increase in EPU causes more damage to FDI than the same decrease in EPU removes. This is the hysteresis prediction.

**Why it is important:** No study gives this result for FDI in India at this time.

### RQ3. When does the effect occur? (horizon)

**The question:** After one sudden increase or one sudden decrease in EPU, how does FDI change in each of the next 36 months? At which month is the difference between the two effects largest?

**The method:**
- Asymmetric local projections (Jordà 2005) use one regression for each month h, from 0 to 36.
- Each regression calculates the change in FDI from the month before the shock to month h.
- Each regression has two shock terms: S⁺ for positive shocks and S⁻ for negative shocks.
- HAC (Newey–West) standard errors adjust for the correlation between months.
- Joint bands give a correct test for all 37 horizons at the same time.
- A Kilian–Vigfusson test compares the response to a +1 standard deviation shock with the response to a −1 standard deviation shock.

**The result that the thesis tests (H3):** The effect is small at month 0. It becomes larger between month 6 and month 24. The reason is that companies make FDI decisions many months before they send the money.

**Why it is important:** RQ1 gives a long-run result. RQ3 gives a long-horizon result. Thus, RQ3 shows the time path that RQ1 cannot show.

### RQ4. Did the relation change over time? (regimes)

**The question:** Did β⁺, β⁻, and the difference between them change between policy periods from 2005 to 2025?

**The method:**
- Bai–Perron tests find the break dates from the data, not from a selection by the researcher.
- A regime-interacted NARDL then gives a different β⁺ and β⁻ for each period.
- Wald tests examine the asymmetry in each period. They also examine if the asymmetry changes between periods.
- A rolling NARDL with an 84-month window gives a graph only. It is not a formal test.

**The result that the thesis tests (H4):** There are two competing predictions. The data will show which prediction is correct.
- Prediction A: After 2014, Indian institutions became stronger. Thus, the asymmetry became smaller.
- Prediction B: After 2018, trade wars and supply-chain changes increased the exposure of India. Thus, the asymmetry became larger.

**Why it is important:** Previous India studies use one β for 20 years. This question lets the β change.

### RQ5. Which uncertainty has the largest effect? (source)

**The question:** Which uncertainty has the largest effect on FDI in India: India EPU, global EPU, or GPR? The thesis calculates each effect with the other two held constant.

**The method:**
- The models from RQ2 and RQ3 also include global EPU and India GPR.
- India is one of the countries in the global EPU index. Thus, the two series contain some of the same information.
- Before the estimation, a regression of India EPU on global EPU removes the global part. The residual is a "pure" domestic EPU.
- WUI and VIX are used only in robustness checks, because they measure different things.

**The result that the thesis tests:** Jardet et al. found that global uncertainty is more important than domestic uncertainty. Canh et al. (2020) found that world uncertainty can increase FDI. The result for India will show which study it agrees with.

**Why it is important:** A viva panel will ask: "Is this effect from India, or from the world?" RQ5 gives the result for that question.

### RQ6. Does the type of FDI change the effect? (composition)

**The question:** Is greenfield FDI more sensitive to EPU than acquisition FDI?

**The terms:** Greenfield FDI makes a new factory or office. Acquisition FDI gets ownership of an Indian company that operates at this time.

**Why the theory gives a prediction:** A new factory is not easy to sell again. Real options theory says that EPU has a larger effect on investment that a company cannot easily sell again (Gulen and Ion 2016).

**The method:** Stacked NARDL or local projections use the two DPIIT route-wise series. A cross-equation test examines if the two effects are different.

**The result that the thesis tests:** Greenfield FDI has a larger effect and a larger asymmetry than acquisition FDI.

**An important condition:** RQ6 is possible only if DPIIT gives the acquisition data for each month from 2005 to 2025. You must make sure that this data is available before you start RQ6.

---

## 3. Which research questions to keep

RQ1 to RQ5 make the strongest core for the thesis. RQ1 gives the base result. RQ2 and RQ3 give the two new results. RQ4 gives the "time-varying" part of the title. RQ5 removes the viva objection that is most possible.

RQ6 gives the best test of the mechanism. But it is an optional addition until you know that the monthly DPIIT data is available. For a master's thesis, RQ1 to RQ4 are sufficient.

---

## 4. One correction to H2

In your text, H2 is "|β⁻| > |β⁺|". But in your definition, EPU⁺ adds the increases in EPU. Thus, "increases cause more damage" is "|β⁺| > |β⁻|". Correct this before your supervisor reads it.

---

## 5. The result of the gap check

The search did not find an India NARDL study of EPU and FDI. Thus, your primary gap is correct.

But one sentence in your gap statement is incorrect. Khan and Qamar (2023) is not the only India EPU–FDI study. Sinha and Ghosh (2021) is a second study, and it is not in your folder. It is linear. It found that the effect of EPU on FDI is larger in the long run than in the short run.

Two India studies use asymmetric methods, but not for FDI:
- Adil and Roy (2024) study total investment in India.
- Simran and Sharma (2024) study the Indian stock market. They found that a decrease in EPU has a larger effect than an increase. This is the opposite direction to your H2.

Your gap statement must refer to these two studies. It must also tell why FDI is different from total investment and from share prices.

The full list of 29 new sources is in [new-literature.md](new-literature.md).

---

## Change log (simmi)

- **Technical nouns kept:** EPU, FDI, FII, GPR, WUI, VIX, NARDL, ARDL, elasticity, regression, residual, shock, horizon, structural break, regime, hysteresis, real options, greenfield, acquisition, Wald test, bootstrap, local projections, unit root, viva, supervisor, and the names of studies and data sources.
- **Words replaced:** "rise" and "fall" → INCREASE and DECREASE. "affect" → HAVE AN EFFECT ON. "explain" → TELL. "buy" → GET OWNERSHIP OF. "reverse" → SELL AGAIN. "expensive" → COSTS MUCH MONEY. "may" → CAN. "however" → BUT. "both" → THE TWO.
- **Sentences split:** Each long sentence from the original reply is now two or three sentences. Each sentence has 25 words or fewer.
