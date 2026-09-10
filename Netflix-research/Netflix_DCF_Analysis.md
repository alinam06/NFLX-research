# Netflix DCF Analysis

## Purpose

This report interprets the results produced by `dcf.py`. The model estimates
Netflix's value under a stated set of assumptions and tests how the valuation
changes when those assumptions change.

This is an educational valuation, not investment advice. A DCF produces an
estimate, not a guaranteed or objectively correct share price.

## Base-case result

The model estimates Netflix's equity value at **$259.7 billion**, or **$60.94
per diluted share**.

The base case uses:

- Normalized 2026 free cash flow: **$10.204 billion**
- Annual FCF growth for 2027-2031: **12%, 10%, 8%, 6%, and 5%**
- WACC: **8.0%**
- Terminal growth: **3.0%**
- Cash and investments: **$9.131 billion**
- Debt: **$14.309 billion**
- Weighted-average diluted shares: **4.261 billion**

The model projects 2031 FCF of **$15.111 billion**. The present value of the
five explicit forecast years is **$53.000 billion**, while the present value of
the terminal value is **$211.860 billion**.

## Interpretation of the base case

The base-case value is below the **$78.05 dated reference price** used in the
reverse DCF. Under the model's assumptions, the reference price therefore
reflects stronger expected growth than the base case.

This does not prove that Netflix is overvalued. It means one or more of the
following must be true to support the higher price:

1. Netflix grows FCF faster than the base forecast.
2. Netflix sustains a higher long-run growth rate.
3. Investors require a lower return than the model's 8.0% WACC.
4. Some combination of these outcomes occurs.

## Sensitivity analysis

The sensitivity table holds every input constant except WACC and terminal
growth.

| WACC \ terminal growth | 2% | 3% | 4% |
|---:|---:|---:|---:|
| 7% | $63.16 | $76.68 | $99.23 |
| 8% | $52.25 | **$60.94** | $73.98 |
| 9% | $44.47 | $50.45 | $58.83 |

### Key sensitivity findings

- The tested valuation range is **$44.47 to $99.23 per share**.
- A higher WACC reduces value because future cash flows are discounted more
  heavily.
- A higher terminal-growth rate increases value because it assumes Netflix's
  cash flows grow faster after 2031.
- The base case is the center cell: **8% WACC and 3% terminal growth**.
- The reference price of $78.05 is not supported by the base case. It is close
  to combinations such as a 7% WACC with 3% terminal growth or an 8% WACC with
  4% terminal growth.

The wide range shows that the DCF is highly sensitive to long-term assumptions.
The terminal value represents **80.0% of enterprise value**, so most of the
estimated value comes from cash flows after the explicit five-year forecast.
This makes the terminal-growth and WACC assumptions especially important.

## Reverse DCF

The reverse DCF asks a different question:

> How quickly must Netflix's FCF grow for the model to equal the $78.05 target
> price?

The script uses bisection to solve for one uniform percentage-point shift added
to all five explicit growth rates. It holds normalized FCF, WACC, terminal
growth, cash, debt, and diluted shares fixed.

The solution is a **+5.85 percentage-point shift**:

| Year | Base growth | Implied growth |
|---:|---:|---:|
| 2027 | 12.0% | 17.8% |
| 2028 | 10.0% | 15.8% |
| 2029 | 8.0% | 13.8% |
| 2030 | 6.0% | 11.8% |
| 2031 | 5.0% | 10.8% |

The base forecast produces an **8.2% five-year FCF CAGR**. The reverse DCF
requires approximately **14.0% CAGR** and 2031 FCF of **$19.662 billion** to
reach $78.05 per share.

## Key reverse-DCF takeaway

The $78.05 reference price embeds a more optimistic operating path than the
base case. Netflix would need to maintain double-digit FCF growth through 2031
under the fixed 8.0% WACC and 3.0% terminal-growth assumptions.

That growth may be possible, but it is not guaranteed. The reverse DCF should
be interpreted as the performance required by the target price, not as a
prediction that Netflix will achieve it.

## Reasonableness review

### Starting cash flow

The **$10.204 billion normalized 2026 FCF** is a transparent estimate, but it
is not a figure reported by Netflix. It begins with management's approximately
$12.5 billion FCF outlook and removes the estimated after-tax effect of the
$2.8 billion WBD termination fee.

This is reasonable for scenario analysis because the termination fee is not a
recurring operating cash flow. However, the exact normalization is uncertain
because the timing and final cash-tax effect are not reported separately.

### Explicit growth

The base forecast declines from **12% growth in 2027 to 5% in 2031**, producing
an **8.2% five-year FCF CAGR**. The downward pattern is reasonable for a large,
maturing company because sustaining very high growth generally becomes harder
as the business grows.

The forecast is not conservative in every respect. It still assumes positive
FCF growth in every year despite competition, content costs, foreign-exchange
risk, and possible changes in customer growth or pricing power.

### WACC

The model's calculated WACC is **7.92%**, rounded to **8.0%**. The estimate is
based on market-value capital weights, a 4.83% risk-free rate, a relevered beta
of 0.79, a 4.14% equity-risk premium, a 5.23% pre-tax cost of debt, and a 21%
marginal tax rate.

An 8.0% WACC is defensible for a profitable company with relatively low debt
compared with its market equity value. It should still be treated as an
estimate. A one-percentage-point increase from 8% to 9%, holding terminal
growth at 3%, reduces estimated value from **$60.94 to $50.45 per share**.

### Terminal growth and terminal value

The **3.0% terminal-growth rate** assumes Netflix can grow indefinitely at a
moderate nominal rate. It is below the 8.0% WACC, which is mathematically
required, and it is within a commonly tested long-run range of 2%-4%.

The main concern is that terminal value equals **80.0% of enterprise value**.
That makes the result heavily dependent on assumptions extending beyond 2031.
The sensitivity table confirms this risk: at an 8% WACC, increasing terminal
growth from 2% to 4% raises value from **$52.25 to $73.98**.

### Overall reasonableness

The model is internally consistent and its base assumptions are plausible, but
the output should be treated as a valuation range rather than a precise price.
The **$60.94 base case** is a reasonable central scenario, while the full
**$44.47-$99.23 range** better communicates the uncertainty.

## Conditional call

At the dated **$78.05 reference price**, the base-case value of $60.94 is about
**22% lower**. The appropriate conclusion depends on the operating and market
assumptions an analyst believes Netflix can achieve:

- **Constructive case:** A favorable view is supportable if Netflix can deliver
  roughly **14% five-year FCF CAGR**, or if its long-run risk and growth justify
  a lower WACC or higher terminal-growth combination. These are the conditions
  required to support approximately $78 per share in this model.
- **Neutral case:** A neutral view is reasonable if the analyst sees a balanced
  chance that Netflix outperforms the 8.2% base FCF CAGR but remains uncertain
  whether it can reach the 14% growth implied by the reference price.
- **Cautious case:** A cautious view is appropriate if FCF growth follows the
  base path or falls below it, if WACC rises toward 9%, or if sustainable
  terminal growth is closer to 2%. These conditions produce values below the
  reference price in the sensitivity table.

**Conditional conclusion:** At $78.05, the model does not provide a margin of
safety under the base assumptions. The price becomes supportable only with
stronger FCF growth or more favorable discount-rate and terminal-growth
assumptions. This is a scenario-based research conclusion, not a recommendation
to buy, hold, or sell Netflix shares.

## Overall conclusion

The model's base-case value is **$60.94 per diluted share**. The sensitivity
analysis shows that reasonable changes in WACC and terminal growth create a
wide valuation range. The reverse DCF shows that a $78.05 price requires about
14.0% annual FCF growth over the five-year forecast, compared with 8.2% in the
base case.

The most important conclusion is not one exact price. It is that Netflix's
valuation depends heavily on whether the company can sustain strong FCF growth
and on the return investors require for bearing risk.

## Data and assumption notes

Reported figures are based on Netflix's 2025 Form 10-K and Q2 2026 Form 10-Q
and shareholder letter. Normalized FCF, forecast growth, WACC, and terminal
growth are valuation estimates. Netflix does not report its WACC or guarantee
future growth.

Primary sources:

- [Netflix 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1065280/000106528026000034/nflx-20251231.htm)
- [Netflix Q2 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/1065280/000106528026000212/nflx-20260630.htm)
- [Netflix Q2 2026 shareholder letter](https://www.sec.gov/Archives/edgar/data/1065280/000106528026000211/ex991_q226.htm)
- [U.S. Treasury interest rates](https://home.treasury.gov/resource-center/data-chart-center/interest-rates)
- [Damodaran beta data](https://pages.stern.nyu.edu/adamodar/New_Home_Page/datafile/Betas.html)
- [Damodaran equity-risk-premium data](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm)
