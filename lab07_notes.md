# Lab 07 Notes: Comparable-Company Policy and Implied Range

## What P/E means and how it complements DCF

The price-to-earnings ratio (P/E) compares a company's share price with its earnings per share:

**P/E = share price ÷ diluted earnings per share**

It shows how many dollars investors are paying for each dollar of annual earnings. A comparable-company analysis applies peer-company P/E multiples to the target company's EPS to estimate a market-based share price. A discounted cash flow (DCF) analysis instead estimates value from projected cash flows and a discount rate. Using both methods provides two perspectives: P/E reflects how the market prices comparable businesses, while DCF reflects assumptions about the target's own future cash generation.

## Why a lower P/E is not automatically better

A lower P/E may indicate that a stock is inexpensive, but it may also reflect weaker expected growth, greater risk, lower-quality or unusually high earnings, cyclicality, or other company-specific concerns. Differences in accounting and one-time items can also reduce comparability. The multiple must therefore be interpreted with the company's business quality, risks, growth prospects, and the sustainability of its earnings.

## Worked calculation: AutoNation applied to Asbury

AutoNation's P/E is:

**$169.84 ÷ $16.92 = 10.037825×** (displayed to six decimal places)

Applying the full-precision AutoNation multiple to Asbury's FY2024 diluted EPS gives:

**($169.84 ÷ $16.92) × $21.50 = $215.81 per Asbury share** (displayed to cents)

No cash or debt is added or subtracted because P/E compares an equity value per share directly with earnings per share.

## Checked results and peer-removal interpretation

- AutoNation P/E: **10.037825×**
- Group 1 Automotive P/E: **11.450149×**
- Median peer P/E: **10.743987×**
- Asbury implied range: **$215.81–$246.18**
- Asbury at the peer median: **$231.00**
- Removing Group 1 leaves the AutoNation reference estimate: **$215.81**
- Change from the full-peer median estimate: **−$15.18**

Group 1 has the higher P/E multiple. Removing it leaves only AutoNation's lower multiple, so the implied estimate falls. Because only one valid peer remains, that result is a reference estimate rather than a range: a minimum and maximum based on one observation would not provide a meaningful spread.

**Before viewing the program's peer-removal result, make your own prediction about the direction and approximate size of the change.**

## Why this does not prove Asbury is fairly valued

This comparison is a valuation reference, not proof of fair value. It uses only two peers, depends on whether those peers are genuinely comparable, and applies historical FY2024 GAAP diluted EPS. The analysis does not by itself account for differences in growth, risk, earnings quality, capital structure, business mix, or future performance. It should be considered alongside case evidence, DCF analysis, and other relevant information.

## AutoNation peer decision

**My decision (use / qualify / exclude):**

**Use**, provisionally.

**Supporting case evidence:**

The assignment identifies AutoNation as a peer and supplies a December 31, 2024 closing price of $169.84 and FY2024 total GAAP diluted EPS of $16.92. Those consistently dated inputs produce a meaningful P/E of 10.037825×. Based only on the information supplied, AutoNation should remain in the comparison. The available materials do not include further evidence about business mix, growth, risk, or earnings quality, so this decision should be revisited if the case provides such evidence.

## Group 1 Automotive peer decision

**My decision (use / qualify / exclude):**

**Qualify**—include it in the numerical analysis, but interpret its result cautiously.

**Supporting case evidence:**

The assignment describes Group 1 Automotive as a qualified peer and supplies a December 31, 2024 closing price of $421.48 and FY2024 total GAAP diluted EPS of $36.81. Those consistently dated inputs produce a meaningful P/E of 11.450149×. Its multiple is higher than AutoNation's and establishes the $246.18 upper end of the implied range. Removing Group 1 lowers the estimate to AutoNation's $215.81 reference value, showing that the conclusion is sensitive to this peer. Because no further case evidence about operational comparability, growth, risk, or earnings quality was provided, qualification is more defensible than treating Group 1 as an unreserved peer.

## Submission reminder

Review the peer decisions against any additional case evidence available to you, then submit **individual GitHub links** to the completed `lab07_pe_comparison.py` and `lab07_notes.md` files.
