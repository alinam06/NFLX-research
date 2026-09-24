# Lab 10 - Netflix Five-Year Pro Forma

**Company:** Netflix, Inc.  
**Ticker:** NFLX  
**Question:** What are five years of Netflix's statements worth, built from assumptions I can defend?

## How to run the model

From the course folder, run:

```bash
python3 netflix_proforma.py
```

The model uses Python's standard library only. It projects 2026-2030, prints an income statement, balance sheet, cash-flow statement, check block, FCFE valuation, and intentional failure test.

The existing ABG `proforma.py` was rerun before this model was built. It still produces five balanced years, a value of $291.75 per share, and a 79.76% terminal-value share. The ABG file was not modified.

## The line that makes Netflix different

**Draft for me to review and put in my own words:** Netflix spends cash to acquire and produce content, capitalizes those costs as content assets, and recognizes content amortization as viewers consume the titles, so content spending affects cash before the related expense is fully recognized.

Netflix has no vehicle inventory or floor-plan borrowing. The company-specific replacement is the linked schedule for content additions, content assets, content liabilities, and content amortization.

## Filing sources

The model uses the three local filings supplied for the lab:

1. [Netflix 2023 Form 10-K](Netflix%2010-K/Netflix%202023%2010-K.pdf), year ended December 31, 2023, accession **0001065280-24-000030**.
2. [Netflix 2024 Form 10-K](Netflix%2010-K/Netflix%202024%2010-K.pdf), year ended December 31, 2024, accession **0001065280-25-000044**.
3. [Netflix 2025 Form 10-K](Netflix%2010-K/nflx-20251231%2010K.pdf), year ended December 31, 2025, accession **0001065280-26-000034**.

Amounts below are converted from the filings' reported units of thousands to USD millions.

## Three-year history

Netflix does not report inventory. `None` is therefore the answer for the requested inventory line. Content assets are shown as the company-specific replacement.

For this model, **operating expenses** are defined as sales and marketing plus technology and development plus general and administrative expenses. This is the closest consistent Netflix equivalent to the video's SG&A line.

| Historical item | 2023 | Source | 2024 | Source | 2025 | Source |
|---|---:|---|---:|---|---:|---|
| Revenue | $33,723.297 | 2023 10-K, Statement of Operations, p. 40 | $39,000.966 | 2024 10-K, Statement of Operations, p. 37 | $45,183.036 | 2025 10-K, Statement of Operations, p. 39 |
| Gross profit | $14,007.929 | 2023 10-K, revenue less cost of revenues, p. 40 | $17,962.502 | 2024 10-K, revenue less cost of revenues, p. 37 | $21,907.707 | 2025 10-K, revenue less cost of revenues, p. 39 |
| Operating expenses | $7,053.926 | 2023 10-K, three operating-expense lines, p. 40 | $7,544.888 | 2024 10-K, three operating-expense lines, p. 37 | $8,581.104 | 2025 10-K, three operating-expense lines, p. 39 |
| Net income | $5,407.990 | 2023 10-K, Statement of Operations, p. 40 | $8,711.631 | 2024 10-K, Statement of Operations, p. 37 | $10,981.201 | 2025 10-K, Statement of Operations, p. 39 |
| Inventory | None | Netflix does not report inventory | None | Netflix does not report inventory | None | Netflix does not report inventory |
| Content assets, net | $31,658.056 | 2023 10-K, Balance Sheet, p. 42 | $32,452.462 | 2024 10-K, Balance Sheet, p. 40 | $32,778.392 | 2025 10-K, Balance Sheet, p. 42 |
| PP&E, net | $1,491.444 | 2023 10-K, Balance Sheet, p. 42 | $1,593.756 | 2024 10-K, Balance Sheet, p. 40 | $2,004.350 | 2025 10-K, Balance Sheet, p. 42 |
| Stockholders' equity | $20,588.313 | 2023 10-K, Balance Sheet, p. 42 | $24,743.567 | 2024 10-K, Balance Sheet, p. 40 | $26,615.488 | 2025 10-K, Balance Sheet, p. 42 |

No history item in this table remains unresolved. Gross profit and operating expenses are calculated classifications rather than separately reported subtotals.

## Two filing numbers for me to verify personally

The lab requires me to open the filings and check two numbers myself. These are deliberately identified for my manual verification:

- [x] **2025 revenue: $45,183,036 million**, 2025 Form 10-K, Consolidated Statements of Operations, p. 39.
- [x] **2025 additions to content assets: $17,096,617 million**, 2025 Form 10-K, Consolidated Statements of Cash Flows, p. 41.

I should check the boxes only after I personally locate and verify the figures in the filing.

## Historical ratios

| Ratio | 2023 | 2024 | 2025 | Calculation and source |
|---|---:|---:|---:|---|
| Gross margin | 41.54% | 46.06% | 48.49% | (Revenue - cost of revenues) / revenue; Statements of Operations |
| Operating expenses / gross profit | 50.36% | 42.00% | 39.17% | (Sales and marketing + technology and development + G&A) / gross profit |
| Inventory days | None | None | None | Netflix does not report inventory |
| Content-asset days | 813.9 | 774.1 | 728.5 | Ending content assets / content amortization x 365 |
| Depreciation / opening PP&E | 25.53% | 22.05% | 20.92% | D&A of PP&E and intangibles / prior-year PP&E |
| Capital spending | $348.552 | $439.538 | $688.220 | Purchases of property and equipment; Statements of Cash Flows |
| Effective tax rate | 12.85% | 12.58% | 13.69% | Income-tax provision / pretax income |
| Reported revenue growth | 6.67% | 15.65% | 15.85% | Current-year revenue / prior-year revenue - 1 |
| Organic or same-store growth | Not disclosed | Not disclosed | Not disclosed | Netflix does not use an ABG-style same-store metric |

Netflix's MD&A explains the reported growth using operating drivers rather than a same-store percentage. The 2023 filing attributes streaming growth primarily to an 8% increase in average paying memberships, partly offset by a 1% decrease in average monthly revenue per paying membership. The 2024 filing attributes growth primarily to average paying memberships and price increases, partly offset by foreign exchange. The 2025 filing attributes growth primarily to memberships, price increases, and advertising, partly offset by foreign exchange.

## Content accounting verified against the filings

The 2025 filing states that Netflix capitalizes licensed-content fees when the license period begins and the title is known, accepted, and available. Produced-content development, direct production, and production-overhead costs are capitalized as incurred.

Netflix amortizes licensed and produced content within cost of revenues over the shorter of the contractual availability window, estimated period of use, or ten years. Amortization is accelerated because viewing is generally heavier near release. The filing states that, on average, more than 90% of a content asset is expected to be amortized within four years of first availability.

The model therefore treats:

- Content additions as an operating cash outflow that increases content assets.
- Content amortization as a noncash expense within cost of revenues that decreases content assets.
- Content liabilities as financing provided by timing differences between content recognition and payment. Changes in the liability remain in operating cash flow, consistent with the filing's cash-flow presentation.

## Opening FY2025 balance sheet used by the model

| Item | USD millions | Source or calculation |
|---|---:|---|
| Cash | $9,033.681 | 2025 10-K |
| Content assets | $32,778.392 | 2025 10-K |
| PP&E | $2,004.350 | 2025 10-K |
| Other assets | $11,780.570 | Total assets less cash, content assets, and PP&E |
| Content liabilities | $5,664.330 | Current plus non-current content liabilities |
| Term debt | $14,462.836 | Short-term plus long-term debt |
| Other liabilities | $8,854.339 | Total liabilities less content liabilities and debt |
| Stockholders' equity | $26,615.488 | 2025 10-K |

The opening balance sheet balances:

\[
\text{Assets} - \text{Liabilities} - \text{Equity} = 0
\]

## Base-case assumption set

These are proposed assumptions for review. 
| Assumption | Value | Label | Reason |
|---|---:|---|---|
| Revenue growth | 12%, 10%, 8%, 7%, 6% | judgment |  Growth declines as Netflix becomes larger, while membership, pricing, and advertising continue to support positive growth. |
| Content-additions growth | 8%, 7%, 6%, 5%, 4% | judgment |  Content spending continues to grow, but more slowly than revenue as Netflix uses its global scale. |
| Content-amortization growth | 8%, 7%, 6%, 5%, 4% | judgment |  Amortization follows the expanding content slate but grows more slowly over time as growth matures. |
| Other cost of revenues / revenue | 15.17% | history | Equal to 2025 other cost of revenues divided by revenue. |
| Operating expenses / gross profit | 37.5%, 36.5%, 35.5%, 35.0%, 34.5% | judgment | Operating expenses gain modest scale, but Netflix continues funding marketing and technology. |
| Depreciation / opening PP&E | 20.92% | history | Equal to 2025 D&A of PP&E and intangibles divided by 2024 PP&E. |
| Capital spending | $700 annually | judgment | This is close to 2025 spending and allows continued investment without assuming another sharp increase. |
| Other-asset investment | 5% of annual revenue increase | judgment |  A portion of growth requires additional working capital and non-content operating assets. |
| Content liabilities / content assets | 17.28% | history | Equal to the FY2025 closing ratio. |
| Tax rate | 14% | judgment |  This is slightly above the recent effective rates of approximately 12.6%-13.7%. |
| Minimum cash | $5,000 | judgment |  Netflix retains a substantial liquidity reserve while still funding content and repurchases. |
| Debt repayment | $1,000 annually | judgment | Netflix gradually reduces debt rather than assuming refinancing or immediate repayment. |
| Share buybacks | $6,000 annually | judgment | This normalizes the 2023-2025 repurchase range rather than repeating the unusually high 2025 amount. |
| Interest rate | 4.98% | history | 2025 interest expense divided by opening short- and long-term debt. |
| Cost of equity | 9% | judgment | The rate is above the risk-free return and reflects equity risk and forecast uncertainty. |
| Terminal growth | 3% | judgment |  Long-run nominal growth is below the cost of equity and below the explicit forecast growth rates. |
| Shares outstanding | 4,222.162150 | history | FY2025 year-end shares from the 2025 10-K; held fixed for this simplified case. |
| Floor plan | None | company-specific | Netflix has no vehicle inventory or floor-plan financing; the content schedule replaces this ABG line. |

## Five-year model results

| Line | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
|---|---:|---:|---:|---:|---:|
| Revenue | $50,605.0 | $55,665.5 | $60,118.7 | $64,327.1 | $68,186.7 |
| Operating income | $15,326.7 | $17,457.5 | $19,395.8 | $21,180.2 | $22,909.6 |
| Net income | $12,561.1 | $14,436.5 | $16,146.3 | $17,723.8 | $19,253.9 |
| Content assets | $33,506.8 | $34,286.2 | $35,112.4 | $35,979.8 | $36,882.0 |
| FCFE before buybacks | $10,406.8 | $12,316.8 | $14,064.7 | $15,656.9 | $17,204.9 |
| Ending cash | $13,440.5 | $19,757.3 | $27,821.9 | $37,478.9 | $48,683.8 |
| Balance-sheet gap | $0.0 | $0.0 | $0.0 | $0.0 | $0.0 |

Cash remains above the $5.0 billion floor in every year. The model does not draw a revolver.

All projected FCFE values are positive. If a revised case produces negative FCFE, the script identifies the affected years and refuses the current terminal-value calculation. A growing-perpetuity terminal value based on negative cash flow is not economically meaningful because it would imply a perpetually negative equity cash flow rather than a claim with positive value.

## Valuation

| Valuation output | Result |
|---|---:|
| PV of forecast FCFE | $53,048.59 million |
| PV of terminal value | $203,114.60 million |
| Equity value | $256,163.18 million |
| Value per share | **$60.67** |
| Terminal value / equity value | 79.29% |

Netflix closed at **$71.36 per share on September 23, 2026**. The model says **$60.67**, while the market says **$71.36**, using the model's fixed 4,222.162150 million-share denominator. The question is whether Netflix can grow faster, produce greater operating efficiency, or justify a lower required return than this base case assumes.

This is an educational valuation comparison, not an investment recommendation.

## Check block and failure test

The script recomputes assets minus liabilities minus equity from the individual balances. Every forecast year reports a zero gap and passes the cash-floor test before valuation.

The intentional failure test changes FY2026E cash only on a separate copy, resetting it to the $9,033.681 million opening balance. Valuation stops with:

```text
FY2026E balance-sheet check failed: gap = -4406.8
```

The negative gap means the edited assets are $4,406.8 million below liabilities plus equity. The correct model remains unchanged.

## My judgment reasons - required before submission

Replace the draft language above with my own reasoning. At minimum, answer:

1. Why do I expect Netflix's revenue growth to decline from 12% to 6%?
I expect growth to decline from 12% to 6% because Netflix is already large, making it harder to maintain the same percentage
growth. Membership growth, pricing, and advertising should still support positive growth.
2. Why should content additions and amortization grow more slowly than revenue?
Content additions and amortization should grow more slowly than revenue because Netflix can distribute content across a larger global customer base. Revenue can
also grow through pricing and advertising without an equal increase in content spending.
3. Why do I expect operating expenses to fall as a percentage of gross profit?
I expect operating expenses to decline relative to gross profit because Netflix can use its existing technology, brand, and administrative
structure to support more revenue.
4. Which judgment would I defend the longest, and what evidence would change it?
I would defend declining revenue growth the longest because it reflects Netflix’s increasing size and maturity. I would change it if future
results showed sustained growth above or below my forecast because of advertising, pricing, membership trends, or customer cancellations.
     
## Partner review - complete only if a partner review occurs

Spoke about it in class.

## My reflection - complete in my own words
Netflix appears financially strong, with growing revenue, improving margins, and positive cash flow. Its global scale
allows revenue to grow faster than some content and operating costs, but the valuation depends heavily on future
assumptions, especially revenue growth and content spending. I learned that Netflix’s value is sensitive to whether it
can continue growing while controlling costs. The 79.29% terminal-value share also shows that most of the estimated
value depends on performance beyond the five-year forecast, making the $60.67 value per share uncertain rather than exact.
