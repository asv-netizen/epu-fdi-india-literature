# Methodology key

Which paper supports which method, question by question. Use this when you write the methodology chapter and when a viva panel asks "why this estimator?".

---

## RQ1 — Is there a long-run relation? (level)

| Step | Method | Cite | Note |
|---|---|---|---|
| Unit root with breaks | Zivot–Andrews | Zivot & Andrews (1992) | `notes/C-rq1-longrun/` |
| Unit root with smooth breaks | Fourier ADF | Enders & Lee (2012) | `notes/C-rq1-longrun/` |
| Stationarity with smooth breaks | Fourier KPSS-type | Becker, Enders & Lee (2006) | `notes/C-rq1-longrun/` |
| Break dates | Bai–Perron | Bai & Perron (1998, 2003) | `notes/C-rq1-longrun/` |
| Cointegration with a regime shift | Gregory–Hansen | Gregory & Hansen (1996) | fallback if bounds reject |
| Long-run relation | ARDL bounds | Pesaran, Shin & Smith (2001) | `notes/C-rq1-longrun/` |
| ECM form of ARDL | ARDL | Pesaran & Shin (1999) | better for explaining the ECM |
| Small-sample critical values | Kripfganz–Schneider | Kripfganz & Schneider (2020, 2023) | needed at 252 months |
| Second critical-value set | Narayan | Narayan (2005) | independent check |
| System alternative | Johansen | Johansen (1991) | answer "why not Johansen?" |
| Unit root alternatives | PP, ADF-GLS | Phillips & Perron (1988); Elliott, Rothenberg & Stock (1996) | unit-root table |

**The viva question you will get:** *"Why ARDL and not Johansen?"*
Answer: 252 monthly observations, a mixture of I(0) and I(1) regressors, and you want a single-equation elasticity rather than a system. ARDL bounds is valid when regressors are I(0) or I(1) and none is I(2). Say that sentence in that order.

**The other viva question:** *"Your sample is 252. Are the bounds critical values valid?"*
Answer: the standard Pesaran et al. (2001) values are asymptotic and too liberal in small samples. You use the Kripfganz–Schneider (2020) response surfaces, which give accurate small-sample critical values and p-values. Cite the response-surface paper, not just the Stata command.

---

## RQ2 — Do increases and decreases differ? (asymmetry)

| Step | Method | Cite | Note |
|---|---|---|---|
| The decomposition | NARDL | Shin, Yu & Greenwood-Nimmo (2014) | `notes/D-rq2-asymmetry/` |
| The idea behind it | Hidden cointegration | Granger & Yoon (2002) | `notes/D-rq2-asymmetry/` |
| Test `β⁺ = β⁻` | Wald, separately long-run and short-run | Shin et al. (2014) | |
| Inference | Bootstrap p-values | Shin et al. (2014) | |
| Path of each effect | Dynamic multipliers | Shin et al. (2014) | |
| Asymmetry as a hypothesis test | Symmetry test | Kilian & Vigfusson (2011) | also used in RQ3 |
| Extra table | Asymmetric Granger causality | Hatemi-J (2012) | cheap robustness |

**The viva question:** *"Why NARDL rather than a threshold model?"*
Answer: NARDL decomposes the *change* in EPU into positive and negative partial sums and gives you two long-run elasticities from one equation, with a clean Wald test of `β⁺ = β⁻`. A threshold model gives you a nonlinear effect in the *level*, which is your nonlinearity definition, not your asymmetry definition. Say the difference out loud — your text already defines it correctly.

---

## RQ3 — When does the effect arrive? (horizon)

| Step | Method | Cite | Note |
|---|---|---|---|
| Estimator | Local projections | Jordà (2005) | `notes/E-rq3-horizon/` |
| Modern treatment | LP handbook | Jordà & Taylor (2024) | lag choice, inference, LP vs VAR |
| Inference validity | LP under weak assumptions | Montiel Olea & Plagborg-Møller (2021) | supports your HAC choice |
| LP vs VAR | Asymptotic equivalence | Plagborg-Møller & Wolf (2021) | shows RQ3 complements RQ1 |
| Serial correlation | Newey–West HAC | Newey & West (1987) | state your bandwidth rule |
| Joint bands | Simultaneous confidence regions | Jordà (2009), *Review of Economics and Statistics* | tests all 37 horizons together |
| Shock construction | — | Ramey (2016) | survey; defends shock identification |
| Asymmetric shock test | Symmetry test | Kilian & Vigfusson (2011) | +1 SD vs −1 SD |

**The viva question:** *"Why local projections and not a VAR?"*
Answer, in three parts: (1) LP does not impose the VAR's lag structure on the response at long horizons, so bias does not accumulate at h = 36; (2) Montiel Olea & Plagborg-Møller (2021) show LP inference is robust; (3) Plagborg-Møller & Wolf (2021) show LP and VAR estimate the same thing asymptotically, so RQ3 is a complement to RQ1 rather than a competing result. Then say: RQ1 gives the long-run equilibrium, RQ3 gives the time path, and they answer different questions.

**Second question:** *"37 regressions, 37 chances of a false positive."*
Answer: you report joint confidence bands (Jordà, 2009), which cover the whole path at once. Say "simultaneous confidence region", not "37 separate tests".

---

## RQ4 — Did the relation change? (regimes)

| Step | Method | Cite | Note |
|---|---|---|---|
| Break dates from the data | Bai–Perron | Bai & Perron (1998, 2003) | also used in RQ1 |
| Single unknown break | Sup-F | Andrews (1993) | complement to Bai–Perron |
| Regime-interacted NARDL | — | Shin et al. (2014), extended | different β⁺ and β⁻ per period |
| Rolling NARDL (graph only) | 84-month window | Pesaran & Timmermann (2007) | **say "graph, not a test"** |
| Formal stability comparison | Forecast comparison | Giacomini & Rossi (2010) | upgrades the rolling graph |
| The alternative you rejected | Markov switching | Hamilton (1989) | answer "why not Markov switching?" |
| General reference | Instability in forecasting | Rossi (2013) | framing |

**The viva question:** *"Why dated regimes and not Markov switching?"*
Answer: your regimes correspond to *policy periods*, which are dated and interpretable. Markov switching estimates a latent state from the data and gives you no date, so you cannot say "after 2014". If the examiner pushes, offer Hamilton (1989) as a robustness check.

**Second question:** *"84 months is a big window for 252 observations."*
Answer: you are right, and that is why the rolling estimate is a figure and not a test. The formal result is the regime-interacted NARDL with Bai–Perron dates. Pesaran & Timmermann (2007) is your citation for the window choice.

---

## RQ5 — Which uncertainty matters? (source)

| Step | Method | Cite | Note |
|---|---|---|---|
| Global vs domestic uncertainty | Panel FDI | Jardet, Jude & Chinn (2022) | the claim you test |
| Domestic EPU and FDI | Panel with instrument | Choi, Furceri & Yoon (2020/2021) | cleanest identification |
| EPU and FDI cross-country | Panel | Canh et al. (2020) | comparator |
| Asymmetric global EPU on FDI | NARDL | Elroukh, Al-Hasani & Gani (2025) | closest design to yours |
| GPR construction | GPR index | Caldara & Iacoviello (2022) | `notes/B-measurement/` |
| WUI construction | WUI | Ahir, Bloom & Furceri (2022) | robustness only |
| EPU construction | EPU index | Baker, Bloom & Davis (2016) | `notes/B-measurement/` |
| Country EPU construction | China EPU | Huang & Luk (2020) | index-choice precedent |
| De-overlapping India and global EPU | Regression residual | — | your own step; state it clearly |

**The viva question:** *"India is inside the global EPU index. Isn't that double counting?"*
Answer: yes, and that is why you regress India EPU on global EPU before estimation and use the residual as "pure" domestic EPU. Say this before they ask. It is the single most likely objection in the whole thesis and RQ5 exists to answer it.

**Second question:** *"Why not WUI as your main uncertainty measure?"*
Answer: WUI measures general economic uncertainty from country reports; EPU measures *policy* uncertainty from newspaper text. Your theory is about policy rules — tax, spending, rates, regulation — so EPU is the construct. WUI and VIX go in robustness.

---

## RQ6 — Does the type of FDI matter? (composition)

| Step | Method | Cite | Note |
|---|---|---|---|
| Why the modes differ | Firm heterogeneity | Nocke & Yeaple (2007) | `notes/H-rq6-composition/` |
| Real effects of the two modes | Greenfield vs M&A | Ashraf, Herzer & Nunnenkamp (2015) | |
| Macro behaviour of the two modes | Greenfield vs M&A | Calderón, Loayza & Servén (2004) | cyclicality |
| Irreversibility mechanism | Cross-border capital | Julio & Yook (2013) | FDI falls before elections, portfolio does not |
| Costly reversibility | Real options | Abel & Eberly (1996) | theoretical ordering |
| EPU and the mode choice | Entry mode | Kabukçuoğlu Dur, Kandilov & Leblebicioglu | **see gap-statement.md §4** |
| EPU and entry mode, home side | Entry mode | Zhou et al. (2021) | |
| Estimator | Stacked NARDL or LP | Shin et al. (2014); Jordà (2005) | |
| Test | Cross-equation Wald | Shin et al. (2014) | |

**Warning.** RQ6 is no longer a new question. See `gap-statement.md`, section 4. Frame it as an India-specific, monthly, route-level test.

**Condition.** RQ6 is impossible without monthly DPIIT acquisition data for 2005–2025. Check that before you commit to it. See `data-sources.md`.

---

## Theory — the two mechanisms

| Mechanism | Cite | Use it for |
|---|---|---|
| Wait-and-see (option value of delay) | Bernanke (1983) | why EPU reduces FDI at all |
| Irreversibility and investment | Pindyck (1990) | why FDI specifically, not portfolio flows |
| Hysteresis (entry/exit bands) | Dixit (1989) | **why `|β⁺| > |β⁻|`** — the asymmetry prediction |
| Investment and hysteresis | Dixit (1992) | the plain-language version for the viva |
| Partial reversibility | Abel & Eberly (1996) | why greenfield > acquisition in sensitivity |
| Aggregate effect of inaction bands | Bertola & Caballero (1994) | why the aggregate response is nonlinear |
| Uncertainty shocks are contractionary | Bloom (2009) | why the effect builds over months |
| Uncertainty is countercyclical | Bloom (2014) | answer "isn't EPU just a recession dummy?" |
| Policy uncertainty and investment | Gulen & Ion (2016) | irreversibility moderates the effect |
| Investment cycles around elections | Julio & Yook (2012) | timing pattern your LP should find |
| Policy uncertainty in developing countries | Rodrik (1991) | the emerging-market case |
| Removing trade-policy uncertainty | Handley & Limão (2015) | identification logic |
| Uncertainty and firm investment | Bloom, Bond & Van Reenen (2006) | panel evidence |
| The sign is contested | Koetse, de Groot & Florax (2009) | **the counter-argument to H1** |
| The sign is contested, survey | Lensink, Bo & Sterken (2001) | same, easier to summarise |

**Read Koetse et al. (2009) before your viva.** The single most damaging objection to your whole thesis is "the literature does not agree that uncertainty reduces investment". Have an answer ready. Your answer should be: the theory predicts a negative effect for *irreversible* investment, FDI is the most irreversible form, and that is a testable restriction — which is RQ6.
