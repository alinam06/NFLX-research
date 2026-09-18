# Lab 08 — Netflix Comparable-Company Valuation

**Target company:** Netflix, Inc. (NFLX)  
**Comparison date:** September 10, 2026  
**Week 3 DCF result used:** $60.94 base case; $44.47–$99.23 sensitivity range  
**Price rule:** Use the closing price on September 10, 2026. If that date is not a trading day, use the nearest prior trading day. September 10 was a trading day, so the September 10 close is used for NFLX, DIS, and WBD.

The DCF values above come from the latest dedicated Week 3 file, [Netflix_DCF_Analysis.md](Netflix-research/Netflix_DCF_Analysis.md). The requested September 10 comparison date is applied to all market prices. An older Week 3 follow-up contains a slightly different base case, so it was not silently combined with the latest analysis.

## 1. Peer policy and rejection criteria

### My peer policy

> A peer must be a publicly traded operating company that earns a substantial portion of its revenue from paid video entertainment, streaming subscriptions, or a closely related direct-to-consumer media business. It should have positive annual diluted EPS that was publicly available by my comparison date. Companies with very different revenue models may be qualified or excluded.

### Rejection criteria written before candidate selection

A candidate is excluded if it is not a publicly traded operating company; does not earn a substantial portion of revenue from paid video entertainment, streaming subscriptions, or a closely related direct-to-consumer media business; or its latest annual GAAP diluted EPS publicly available by September 10, 2026 is zero, negative, missing, or cannot be verified. A company with a materially different consolidated revenue model may be qualified or excluded rather than treated as a clean peer. Duplicate tickers and Netflix itself are removed from the peer set. Any unverified required fact is marked **unresolved** rather than estimated.

## 2. Source table

| Company | Ticker | Decision | Business evidence | Important difference from Netflix | Price | Price date | Annual GAAP diluted EPS | Fiscal period | Publication date | Source link | Exact source locator |
|---|---:|---|---|---|---:|---|---:|---|---|---|---|
| Netflix, Inc. | NFLX | Target; excluded from its own peer set | Netflix describes itself as an entertainment service and says revenue is primarily monthly membership fees. | Not applicable—the target is the benchmark. | $76.01 | Sept. 10, 2026 | $2.53 | Year ended Dec. 31, 2025 | Jan. 23, 2026 | [Netflix 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1065280/000106528026000034/nflx-20251231.htm); [price history](https://stockanalysis.com/stocks/nflx/history/) | Form 10-K, **Item 1. Business**, pp. 3–4; **Consolidated Statements of Operations**, p. 39; **Note 3, Earnings Per Share**, p. 49. Price-history row dated Sept. 10, 2026, “Close.” |
| The Walt Disney Company | DIS | **Use** | Disney reports paid Disney+ and Hulu subscriptions and subscription-fee and advertising revenue within its Entertainment direct-to-consumer business. | Disney also has theme parks and resorts, cruises, sports networks, linear television, theatrical distribution, and licensing; its consolidated EPS is not a streaming-only result. | $105.82 | Sept. 10, 2026 | $6.85 | Year ended Sept. 27, 2025 | Nov. 13, 2025 | [Disney 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1744489/000174448925000155/dis-20250927.htm); [SEC filing page](https://www.sec.gov/Archives/edgar/data/1744489/0001744489-25-000155-index.htm); [price history](https://stockanalysis.com/stocks/dis/history/) | Form 10-K, **Item 7, Direct-to-Consumer**, pp. 39–40; **Entertainment DTC Product Descriptions and Key Definitions**, p. 55; **Consolidated Statements of Income**, p. 71, and **Earnings Per Share**, p. 88. SEC filing page, “Filing Date.” Price-history row dated Sept. 10, 2026, “Close.” |
| Warner Bros. Discovery, Inc. | WBD | **Qualify** | WBD’s Streaming segment includes HBO Max, discovery+, and HBO premium pay-TV; the filing reports 131.6 million streaming subscribers and streaming distribution and advertising revenue. | WBD has large Studios and Global Linear Networks businesses; its 2025 results include a $2.945 billion debt-extinguishment gain; and on the comparison date its stock price reflected a pending $31-per-share cash merger agreement with Paramount Skydance. | $28.20 | Sept. 10, 2026 | $0.29 | Year ended Dec. 31, 2025 | Feb. 27, 2026 | [WBD 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1437107/000143710726000020/wbd-20251231.htm); [SEC filing page](https://www.sec.gov/Archives/edgar/data/1437107/0001437107-26-000020-index.html); [Paramount merger 8-K](https://www.sec.gov/Archives/edgar/data/1437107/000143710726000018/disca-20260227.htm); [price history](https://stockanalysis.com/stocks/wbd/history/) | Form 10-K, **Item 1, Our Company—Streaming**, pp. 8–9; **Item 8, Consolidated Statements of Operations**, p. 65; **Note 3, Equity and Earnings Per Share**, pp. 83–84; and **Gain on Extinguishment of Debt** in Item 7. Feb. 27, 2026 Form 8-K, **Item 1.01, Entry into a Material Definitive Agreement**. SEC filing page, “Filing Date.” Price-history row dated Sept. 10, 2026, “Close.” |

No required table field remained unresolved after checking the filings and dated price histories. The closing-price pages are market-data sources, while the business-model and EPS evidence comes from each issuer’s SEC-filed annual report.

## 3. Candidate decisions

**Disney — Use.** Disney is a listed operating company with a substantial paid-video direct-to-consumer business and positive annual GAAP diluted EPS available before the comparison date. Its broader parks, sports, linear-network, studio, and licensing mix makes it less directly comparable than a streaming-only company, but the policy permits use when the relevant DTC business is substantial.

**Warner Bros. Discovery — Qualify.** WBD is a listed operating company with a substantial subscription-streaming business and positive annual GAAP diluted EPS available before the comparison date. It is qualified, not treated as a clean peer, because Studios and Global Linear Networks materially affect consolidated results, the debt-extinguishment gain makes its $0.29 EPS a weak measure of recurring earnings, and its market price was influenced by the pending $31-per-share cash merger agreement with Paramount Skydance.

Neither candidate is ranked. No candidate was excluded, so there is no excluded row beyond Netflix’s required exclusion from its own peer set.

## 4. Hand check

Disney is an admitted peer:

\[
\text{Disney P/E} = \frac{\$105.82}{\$6.85} = 15.448175\text{x}
\]

This matches the calculator’s displayed Disney multiple. The calculation uses annual GAAP diluted EPS and does not add cash or subtract debt.

## 5. Peer-removal prediction and result

**Prediction before running the removal test:** Removing WBD should sharply lower the median-implied Netflix price because WBD’s small positive EPS produces a much higher P/E than Disney’s. With only Disney remaining, the output should become a one-peer reference estimate rather than a range.

**Calculator result:** The full two-peer median implies **$142.55** per Netflix share. Removing WBD leaves a Disney-only estimate of **$39.08**, a change of **−$103.47** calculated from unrounded values. Removing Disney leaves a WBD-only estimate of **$246.02**, a change of **+$103.47**.

Removing WBD eliminates the high-multiple observation and exposes how strongly it pulls the two-peer median upward. The lost information is WBD’s comparatively close exposure to subscription streaming and content production. The remaining Disney result is only a reference estimate, not a peer range, and Disney’s diversified businesses remain a comparability limitation.

## 6. DCF and peer P/E comparison

| Method | Central result | Range | Interpretation |
|---|---:|---:|---|
| Week 3 DCF | $60.94 | $44.47–$99.23 | Base case and WACC/terminal-growth sensitivity from the latest dedicated Week 3 DCF file. |
| Peer P/E | $142.55 median | $39.08–$246.02 | Based on DIS and qualified WBD; the width shows weak peer-set precision. |
| Actual NFLX close on comparison date | $76.01 | Not applicable | Sept. 10, 2026 close under the common trading-date rule. |

The two valuation methods are not averaged. The DCF is an intrinsic equity-value-per-share estimate after its cash/debt bridge. The P/E method is an equity-value-per-share comparison and therefore receives no additional cash or debt bridge.

## 7. Provisional decision

**Provisional decision: watch-defer.** The $76.01 market close is above the $60.94 DCF base case but inside the DCF sensitivity range. The peer median is much higher, yet it comes from only two diversified companies and changes by $103.47 when either observation is removed. That instability does not support initiating solely from the peer result.

The defensible DCF range is **$44.47–$99.23** under the Week 3 sensitivity assumptions. The mechanically calculated peer range is **$39.08–$246.02**, with a **$142.55** median, but its breadth and WBD’s earnings-quality issue are material limitations. There is no combined range because combining or averaging these methods would hide their disagreement.

Evidence that could change the decision includes a reconciled and independently checked Week 3 market-price/date input; evidence that WBD’s 2025 GAAP EPS is representative of recurring earnings; a larger policy-compliant peer set; or materially different evidence about Netflix’s sustainable free-cash-flow growth, margin, WACC, terminal growth, or share count.

## 8. Skeptical-colleague review and AI criticism

The weakest-supported DCF assumption is the terminal-value framework: the latest Week 3 file uses an 8.0% WACC and 3.0% perpetual growth, and terminal value contributes about 80% of enterprise value. Small changes in those assumptions move the DCF materially. The weakest peer assumption is treating WBD’s $0.29 GAAP diluted EPS and $28.20 merger-influenced price as an ordinary stand-alone P/E observation even though 2025 results include a $2.945 billion debt-extinguishment gain and WBD was subject to a pending $31-per-share cash merger agreement.

The company and valuation object are aligned: Netflix is the target, and both methods ultimately estimate equity value per share. The important mismatches are:

- **Date/price mismatch:** the Week 3 DCF file labels approximately $78.05 as a September 8, 2026 reference price. This Lab 08 comparison instead uses the requested September 10 date and its verified $76.01 NFLX close; the DCF itself has not been revalued.
- **Earnings-period mismatch:** NFLX and WBD use years ended December 31, 2025, while Disney uses its fiscal year ended September 27, 2025. Each is the latest annual result public by the comparison date, but the periods are not coterminous.
- **Earnings-definition limitation:** all P/E inputs use reported annual GAAP diluted EPS, as required, but WBD’s denominator contains a material non-operating gain and none of the peers’ consolidated EPS isolates streaming.
- **Transaction-price limitation:** WBD’s September 10 market price reflected a pending $31-per-share cash acquisition agreement, so it was not a clean stand-alone market valuation.
- **Internal Week 3 mismatch:** the latest dedicated DCF reports $60.94 with an 8.0% WACC, while an older follow-up file reports approximately $61.01 with an 8.5% WACC. This report uses the latest dedicated DCF and does not blend the versions.

**AI criticism to evaluate:** WBD satisfies the written screening rule, but its reported $0.29 EPS is not a defensible recurring earnings denominator without further investigation, and its price was merger-influenced; including it mechanically makes the peer conclusion look more precise and more favorable than the evidence supports.

**Question that could change my decision:** After checking WBD’s 2025 income statement and debt-extinguishment disclosure, do I believe its $0.29 GAAP diluted EPS represents recurring earnings well enough to retain WBD as a qualified P/E peer?

**My evaluation after checking the criticism against my sources:**  
[x] Accept  
[ ] Reject  
[ ] Unresolved  

**Reason:** I accept the criticism because WBD's Form 10-K reports a $2.945 billion gain on extinguishment of debt while total pretax income was only $1.639 billion. The gain is non-operating and larger than reported pretax income, so the resulting $0.29 diluted EPS is not a sound representation of recurring operating earnings. In addition, the $28.20 comparison-date price was influenced by a pending $31-per-share cash merger agreement. These facts make WBD's mechanically calculated P/E unusually high and unsuitable as a clean central valuation anchor.

**Answer to the skeptical question:** No. WBD's $0.29 GAAP diluted EPS is the correct reported number required by the assignment, but it does not represent recurring earnings well enough to treat WBD as a clean P/E peer. I retain WBD only as a **qualified sensitivity observation** because it meets the written screening policy; I would not rely on it alone to initiate an investment.

## Calculator command

From the course folder, run:

```bash
python3 lab08_netflix_comparables.py
```

The Lab 07 file remains unchanged. The Lab 08 copy is [lab08_netflix_comparables.py](lab08_netflix_comparables.py).
