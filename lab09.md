# Lab 09 — Asbury Automotive Group Five-Year Pro Forma

## Model description

`proforma.py` builds linked income statements, balance sheets, and cash-flow statements for Asbury Automotive Group for 2026–2030. It uses only the case data supplied for the lab and Python's standard library.

From the course folder, run:

```bash
python3 proforma.py
```

The verified output from the correct model is saved in `abg_results.txt`.

All monetary amounts are USD millions. Shares are in millions. The model initializes the opening revolver at **0.0** because the case does not explicitly provide an opening revolver balance. This is a model initialization, not an additional company fact.

## Supplied assumptions

| Assumption | Case input | Label |
|---|---:|---|
| Revenue growth | 1.8% annually | judgment |
| Gross margin | 17.05% | judgment |
| SG&A / gross profit, 2026–2030 | 66.5%, 65.5%, 64.5%, 64.5%, 64.5% | judgment |
| Depreciation / opening PP&E | 82.4 / 3,070.4 | history |
| Noncash impairment | $120 annually | judgment |
| Capital spending | $250 annually | guidance |
| Tax rate | 25.5% | judgment |
| Inventory days | 2,135.8 / (17,999.0 − 3,071.7) × 365 | history |
| Floor plan / inventory | 2,027.0 / 2,135.8 | history |
| Other working-capital investment | 0.8% of annual revenue change | judgment |
| Minimum cash | $25 | history |
| Revolver limit | $850 | judgment |
| Revolver interest rate | 6.0% | judgment |
| Term-debt repayment | $150 annually | judgment |
| Share buyback | $150 annually | judgment |
| Floor-plan interest rate | 4.67% | history |
| Term-debt interest rate | 5.44% | history |
| Cost of equity | 10.0% | judgment |
| Terminal growth | 2.5% | judgment |
| Shares outstanding | 17.951349 | fact supplied by lab, attributed to June 30, 2026 10-Q |

The supplied share count remains fixed throughout the case even though the model includes annual share-buyback cash flows.

## Results from the correct model

| Line | FY2026E | FY2030E |
|---|---:|---:|
| Revenue | $18,323.0 | $19,678.3 |
| Operating income | $844.2 | $971.4 |
| Net income | $413.6 | $527.5 |
| FCFE | $211.4 | $342.3 |
| Ending cash | $101.8 | $719.8 |
| Assets − liabilities − equity | $0.0 | $0.0 |

All five forecast years pass the balance-sheet, minimum-cash, and revolver-limit checks. The revolver remains at zero because internally generated cash keeps ending cash above the $25 minimum.

### Valuation result

- Present value of forecast FCFE: **$1,059.87**
- Present value of terminal value: **$4,177.46**
- Equity value: **$5,237.34**
- Value per share: **$291.75**
- Terminal value share of equity value: **79.76%**

The terminal cash flow adds back the 2030 term-debt repayment before applying perpetual growth because a fixed $150 annual repayment cannot continue forever once the debt is extinguished.

## Intentional failure test

The failure test copied the correct results, changed FY2026E cash from $101.8 to $40.4, and then attempted valuation. The model stopped before valuation and reported:

```text
FY2026E balance-sheet check failed: gap = -61.4
```

The original results were not changed. The final delivered model remains correct.

## Explanation notes for me to review and put in my own words

### Revenue growth judgment

The case assumes revenue grows 1.8% each year. This is a restrained, steady-growth assumption rather than a forecast of acquisitions or unusually strong vehicle demand. Because revenue drives cost of sales, inventory, floor-plan borrowing, and working-capital investment, changing this assumption affects all three statements.

### Gross-margin judgment

The 17.05% gross margin converts revenue into gross profit. Holding the margin constant assumes the mix and profitability of vehicle sales, parts and service, and finance and insurance remain broadly stable. A small margin change matters because gross profit funds SG&A, depreciation, impairment, interest, and taxes.

### SG&A / gross-profit judgment

SG&A declines from 66.5% of gross profit in 2026 to 64.5% in 2028 and remains there. This assumes operating efficiency improves during the first three forecast years. The model does not assume further efficiency after 2028. A lower ratio increases operating income and cash available to equity.

### Why cash is calculated last

Cash is the result of operating, investing, and financing decisions. The model first calculates earnings, working capital, fixed assets, debt repayment, and FCFE. It then determines whether the resulting cash is above the $25 minimum. Only after that calculation can the model decide whether to draw or repay the revolver. Calculating cash earlier would ignore financing needed to maintain minimum liquidity.

Cash is not used as an unexplained balance-sheet plug. The model calculates it from opening cash, FCFE, buybacks, and revolver movements and then independently checks whether the balance sheet balances.

### Meaning of the −61.4 gap

Correct FY2026E cash is $101.8. Replacing it with $40.4 removes $61.4 of assets without changing any liability or equity balance:

\[
40.4-101.8=-61.4
\]

Therefore, assets are $61.4 lower than liabilities plus equity. The negative gap identifies the broken cash link and prevents the incorrect model from being valued.

### Floor-plan financing in this case

Floor-plan borrowing finances vehicle inventory. The model sets ending floor plan as a historical percentage of ending inventory, so floor-plan debt rises when inventory rises. Floor-plan interest is calculated using the opening floor-plan balance.

Following the course case instructions, the change in floor plan is included in operating cash flow and FCFE. An increase in floor-plan borrowing is a source of cash that helps finance higher inventory; a decrease is a use of cash. The ending floor-plan balance also appears as a balance-sheet liability.

## My reflection

**Complete this section myself. Do not treat the prompts below as completed work.**
- What part of linking the three statements was hardest for me?
I think that one of the main difficulties linking the three statements for me was understanding the order of the parts for each of the statements, and what goes where. Also, I had to think about why changing the cash ends up breaking the model. Adding a test at the end to see if the model catches this helped me understand that better. 
- Which assumption has the strongest effect on value, and why?
I think cost of equity, because it affects present value and terminal value which impact valuation.
- Why is a 79.76% terminal-value share important when interpreting the result?
This means that approximately 80% of the estimated equity value depends on cash flows after 2030 rather than the five detailed forecast years. This makes the $291.75 estimate a lot more sensitive, since it's only 20% based on the 5 year cash flow.
- What would I change after reviewing the model?
After reviewing the model, I would add a sensitivity analysis for the cost of equity and terminal growth rate. Because 79.76% of the equity value comes from the terminal value, small changes in these assumptions could significantly change the estimated value per share. I would use a valuation range instead of relying only on the $291.75 estimate. In a more realistic model, I would also allow share repurchases to reduce the number of shares outstanding, although this assignment requires the share count to remain fixed.
 
