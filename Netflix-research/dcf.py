"""Netflix five-year discounted cash flow valuation.

Run:
    python3 dcf.py

The script prints a base-case valuation, WACC calculation, sensitivity table,
reverse DCF, and source notes. Reported figures and analyst assumptions are
identified separately. This is educational analysis, not investment advice.
"""


# -----------------------------------------------------------------------------
# EDITABLE ANALYST ASSUMPTIONS
# -----------------------------------------------------------------------------
MANAGEMENT_2026_FCF_OUTLOOK = 12_500.0  # USD millions
WBD_TERMINATION_FEE = 2_800.0  # USD millions, pre-tax
NORMALIZATION_TAX_RATE = 0.18  # H1 2026 reported effective tax rate
NORMALIZED_2026_FCF = MANAGEMENT_2026_FCF_OUTLOOK - WBD_TERMINATION_FEE * (
    1.0 - NORMALIZATION_TAX_RATE
)
GROWTH_RATES = [0.12, 0.10, 0.08, 0.06, 0.05]  # 2027-2031
WACC = 0.08  # rounded from the bottom-up calculation below
TERMINAL_GROWTH = 0.03
SENSITIVITY_WACCS = [0.07, 0.08, 0.09]
SENSITIVITY_TERMINAL_GROWTH_RATES = [0.02, 0.03, 0.04]
REVERSE_DCF_TARGET_SHARE_PRICE = 78.05  # USD; dated reference in course research
REVERSE_DCF_SHIFT_LOWER_BOUND = -0.05  # -5 percentage points
REVERSE_DCF_SHIFT_UPPER_BOUND = 0.10  # +10 percentage points

# -----------------------------------------------------------------------------
# REPORTED COMPANY DATA - Q2 2026 Form 10-Q
# -----------------------------------------------------------------------------
CASH_AND_INVESTMENTS = 9_131.464  # USD millions; includes restricted cash
DEBT = 14_309.306  # USD millions; carrying amount
DILUTED_SHARES = 4_261.0  # millions; Q2 2026 weighted-average diluted shares

SEC_ARCHIVES = "https://www.sec.gov/Archives/edgar/data/1065280"
FORM_10K = f"{SEC_ARCHIVES}/000106528026000034/nflx-20251231.htm"
FORM_10Q = f"{SEC_ARCHIVES}/000106528026000212/nflx-20260630.htm"
Q2_LETTER = f"{SEC_ARCHIVES}/000106528026000211/ex991_q226.htm"
TREASURY_SOURCE = (
    "https://home.treasury.gov/resource-center/data-chart-center/interest-rates"
)
BETA_SOURCE = "https://pages.stern.nyu.edu/adamodar/New_Home_Page/datafile/Betas.html"
ERP_SOURCE = "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm"
DEFAULT_SPREAD_SOURCE = (
    "https://pages.stern.nyu.edu/adamodar/New_Home_Page/datafile/ratings.html"
)

# -----------------------------------------------------------------------------
# WACC inputs as of 2026-09-09 unless noted otherwise
# -----------------------------------------------------------------------------
RISK_FREE_RATE = 0.0483  # 10-year U.S. Treasury yield, 2026-09-09
EQUITY_RISK_PREMIUM = 0.0414  # Damodaran implied U.S. ERP, 2026-09-01
UNLEVERED_BETA = 0.76  # Damodaran U.S. entertainment beta, corrected for cash
MARGINAL_TAX_RATE = 0.21  # U.S. federal statutory rate used in Netflix's 10-K
REFERENCE_MARKET_EQUITY = REVERSE_DCF_TARGET_SHARE_PRICE * DILUTED_SHARES
EQUITY_WEIGHT = REFERENCE_MARKET_EQUITY / (REFERENCE_MARKET_EQUITY + DEBT)
DEBT_WEIGHT = 1.0 - EQUITY_WEIGHT
MARKET_DEBT_TO_EQUITY = DEBT / REFERENCE_MARKET_EQUITY
RELEVERED_BETA = UNLEVERED_BETA * (
    1.0 + (1.0 - MARGINAL_TAX_RATE) * MARKET_DEBT_TO_EQUITY
)
COST_OF_EQUITY = RISK_FREE_RATE + RELEVERED_BETA * EQUITY_RISK_PREMIUM
DEFAULT_SPREAD = 0.0040  # synthetic AAA spread; 2025 EBIT/interest > 8.5x
PRE_TAX_COST_OF_DEBT = RISK_FREE_RATE + DEFAULT_SPREAD
CALCULATED_WACC = (
    EQUITY_WEIGHT * COST_OF_EQUITY
    + DEBT_WEIGHT * PRE_TAX_COST_OF_DEBT * (1.0 - MARGINAL_TAX_RATE)
)


def validate_inputs():
    if len(GROWTH_RATES) != 5:
        raise SystemExit("Error: provide exactly five annual growth rates.")
    if WACC <= -1.0 or TERMINAL_GROWTH >= WACC:
        raise SystemExit("Error: WACC must exceed terminal growth and -100%.")
    if any(growth <= -1.0 for growth in GROWTH_RATES):
        raise SystemExit("Error: every annual growth rate must exceed -100%.")
    if DILUTED_SHARES <= 0.0:
        raise SystemExit("Error: diluted shares must be positive.")


def calculate_dcf(growth_rates, wacc, terminal_growth):
    """Calculate values in USD millions and value per share in USD."""
    if terminal_growth >= wacc:
        raise ValueError("Terminal growth must be less than WACC.")
    forecast_fcf = []
    fcf = NORMALIZED_2026_FCF
    for growth_rate in growth_rates:
        if growth_rate <= -1.0:
            raise ValueError("Every annual growth rate must exceed -100%.")
        fcf *= 1.0 + growth_rate
        forecast_fcf.append(fcf)
    pv_forecast = sum(
        annual_fcf / (1.0 + wacc) ** year
        for year, annual_fcf in enumerate(forecast_fcf, start=1)
    )
    terminal_value = (
        forecast_fcf[-1]
        * (1.0 + terminal_growth)
        / (wacc - terminal_growth)
    )
    pv_terminal = terminal_value / (1.0 + wacc) ** 5
    enterprise_value = pv_forecast + pv_terminal
    net_debt = DEBT - CASH_AND_INVESTMENTS
    equity_value = enterprise_value - net_debt
    return {
        "forecast_fcf": forecast_fcf,
        "pv_forecast": pv_forecast,
        "pv_terminal": pv_terminal,
        "enterprise_value": enterprise_value,
        "net_debt": net_debt,
        "equity_value": equity_value,
        "value_per_share": equity_value / DILUTED_SHARES,
        "terminal_share": pv_terminal / enterprise_value,
    }


def money(amount):
    return f"${amount:,.2f}"


def print_base_case(result):
    print("NETFLIX FIVE-YEAR DCF — BASE CASE")
    print("Educational analysis; not investment advice")
    print("Units: USD millions except per-share amounts\n")
    print("Reported / management data")
    print("  2025 operating cash flow:                 $10,149.27")
    print("  2025 purchases of property and equipment:   $688.22")
    print("  2025 reported free cash flow:              $9,461.05")
    print(
        "  Management 2026 FCF outlook:             "
        f"~{money(MANAGEMENT_2026_FCF_OUTLOOK)}"
    )
    print(f"  WBD termination fee (pre-tax):            {money(WBD_TERMINATION_FEE)}")
    print(f"  Cash and investments (2026-06-30):        {money(CASH_AND_INVESTMENTS)}")
    print(f"  Debt (2026-06-30):                        {money(DEBT)}")
    print(f"  Q2 weighted-average diluted shares (m):   {DILUTED_SHARES:,.2f}\n")
    print("Analyst assumptions")
    print(f"  Normalized 2026 FCF:                      {money(NORMALIZED_2026_FCF)}")
    print("    Outlook less the after-tax WBD termination-fee benefit.")
    print("    Used as a practical FCFF proxy for this course model.")
    growth_text = ", ".join(f"{growth:.1%}" for growth in GROWTH_RATES)
    print(f"  Annual FCF growth (2027-2031):            {growth_text}")
    print(f"  WACC:                                      {WACC:.1%}")
    print(f"  Perpetual growth:                          {TERMINAL_GROWTH:.1%}\n")
    print("WACC calculation (market-based estimate)")
    print(f"  Relevered beta:                            {RELEVERED_BETA:.2f}")
    print(
        f"  Cost of equity = {RISK_FREE_RATE:.2%} + {RELEVERED_BETA:.2f} x "
        f"{EQUITY_RISK_PREMIUM:.2%} = {COST_OF_EQUITY:.2%}"
    )
    print(f"  Pre-tax cost of debt:                      {PRE_TAX_COST_OF_DEBT:.2%}")
    print(f"  Marginal tax rate:                         {MARGINAL_TAX_RATE:.1%}")
    print(
        "  Market-value weights:                      "
        f"{EQUITY_WEIGHT:.1%} equity / {DEBT_WEIGHT:.1%} debt"
    )
    print(f"  Calculated WACC:                           {CALCULATED_WACC:.2%}")
    print(f"  Rounded WACC used:                         {WACC:.1%}\n")
    print("Forecast and valuation")
    print("  Year      Growth       FCF")
    forecast_rows = zip(GROWTH_RATES, result["forecast_fcf"])
    for year, (growth, fcf) in enumerate(forecast_rows, start=2027):
        print(f"  {year}      {growth:>5.1%}    {money(fcf):>12}")
    valuation_rows = (
        ("PV of explicit FCF", money(result["pv_forecast"])),
        ("PV of terminal value", money(result["pv_terminal"])),
        ("Enterprise value", money(result["enterprise_value"])),
        ("Less net debt", money(result["net_debt"])),
        ("Equity value", money(result["equity_value"])),
        ("ESTIMATED VALUE PER SHARE", money(result["value_per_share"])),
        ("Terminal value / enterprise value", f"{result['terminal_share']:.1%}"),
    )
    print()
    for label, value in valuation_rows:
        print(f"  {label:<40}{value:>14}")


def print_sensitivity():
    print("\nSENSITIVITY — VALUE PER SHARE")
    heading = f"{'Terminal g':<13}" + "".join(
        f"WACC {wacc:.1%}".rjust(14) for wacc in SENSITIVITY_WACCS
    )
    print(heading)
    valid_values = []
    for terminal_growth in SENSITIVITY_TERMINAL_GROWTH_RATES:
        row = f"{terminal_growth:.1%}".ljust(13)
        for wacc in SENSITIVITY_WACCS:
            if terminal_growth >= wacc:
                cell = "invalid"
            else:
                sensitivity_value = calculate_dcf(
                    GROWTH_RATES, wacc, terminal_growth
                )["value_per_share"]
                valid_values.append(sensitivity_value)
                cell = money(sensitivity_value)
            row += cell.rjust(14)
        print(row)
    base_value = calculate_dcf(
        GROWTH_RATES, WACC, TERMINAL_GROWTH
    )["value_per_share"]
    print("  Interpretation:")
    print(
        f"    Base case ({WACC:.1%} WACC, "
        f"{TERMINAL_GROWTH:.1%} terminal growth): {money(base_value)}"
    )
    print(
        f"    Tested valuation range: {money(min(valid_values))} "
        f"to {money(max(valid_values))}"
    )
    print("    A higher WACC lowers value; higher terminal growth raises value.")
    print("    These are scenarios, not predictions or reported company facts.")


def reverse_dcf():
    print("\nREVERSE DCF — UNIFORM SHIFT TO ALL FIVE GROWTH RATES")
    print(f"  Target share price: {money(REVERSE_DCF_TARGET_SHARE_PRICE)}")
    lower = REVERSE_DCF_SHIFT_LOWER_BOUND
    upper = REVERSE_DCF_SHIFT_UPPER_BOUND
    print("  Solved variable:    uniform percentage-point shift to")
    print("                      2027-2031 FCF growth")
    print(f"  Method:             bisection within [{lower:+.1%}, {upper:+.1%}]")
    if lower >= upper:
        print("  No solution: lower bound must be less than upper bound.")
        return
    bracket_rates = (
        base + bound
        for base in GROWTH_RATES
        for bound in (lower, upper)
    )
    if any(growth <= -1.0 for growth in bracket_rates):
        print("  No solution: bracket makes an annual growth rate -100% or lower.")
        return

    def price_gap(shift):
        shifted = [growth + shift for growth in GROWTH_RATES]
        implied_price = calculate_dcf(
            shifted, WACC, TERMINAL_GROWTH
        )["value_per_share"]
        return implied_price - REVERSE_DCF_TARGET_SHARE_PRICE

    lower_gap = price_gap(lower)
    upper_gap = price_gap(upper)
    if lower_gap * upper_gap > 0.0:
        print(f"  No solution in bracket [{lower:+.1%}, {upper:+.1%}].")
        return
    for _ in range(100):
        midpoint = (lower + upper) / 2.0
        midpoint_gap = price_gap(midpoint)
        if abs(midpoint_gap) < 1e-10 or upper - lower < 1e-12:
            break
        if lower_gap * midpoint_gap <= 0.0:
            upper = midpoint
        else:
            lower = midpoint
            lower_gap = midpoint_gap
    shifted_rates = [growth + midpoint for growth in GROWTH_RATES]
    base_fcf_cagr = (
        calculate_dcf(GROWTH_RATES, WACC, TERMINAL_GROWTH)["forecast_fcf"][-1]
        / NORMALIZED_2026_FCF
    ) ** (1.0 / 5.0) - 1.0
    implied_result = calculate_dcf(shifted_rates, WACC, TERMINAL_GROWTH)
    implied_fcf_cagr = (
        implied_result["forecast_fcf"][-1] / NORMALIZED_2026_FCF
    ) ** (1.0 / 5.0) - 1.0
    print(
        f"  Solved shift:       {midpoint:+.2%} "
        f"({midpoint * 100:+.2f} percentage points)"
    )
    base_growth_text = ", ".join(f"{growth:.1%}" for growth in GROWTH_RATES)
    implied_growth_text = ", ".join(
        f"{growth:.1%}" for growth in shifted_rates
    )
    print(f"  Base growth:        {base_growth_text}")
    print(f"  Implied growth:     {implied_growth_text}")
    print(f"  Base five-year CAGR:                         {base_fcf_cagr:.1%}")
    print(f"  Implied five-year CAGR:                      {implied_fcf_cagr:.1%}")
    print(
        "  Implied 2031 FCF:                            "
        f"{money(implied_result['forecast_fcf'][-1])}"
    )
    print(
        "  Model value at solution:                     "
        f"{money(implied_result['value_per_share'])}"
    )
    print("  Held fixed:")
    print(f"    Normalized 2026 FCF {money(NORMALIZED_2026_FCF)}; WACC {WACC:.1%};")
    print(
        f"    terminal growth {TERMINAL_GROWTH:.1%}; cash/investments "
        f"{money(CASH_AND_INVESTMENTS)};"
    )
    print(f"    debt {money(DEBT)}; shares {DILUTED_SHARES:,.2f} million.")
    print("  Interpretation:")
    print("    The target price requires faster FCF growth than the base case.")
    print("    This is an implied market expectation, not a forecast from Netflix.")


def print_sources_and_notes():
    print("\nSOURCES AND INTERPRETATION")
    print("  Facts: Netflix 2025 Form 10-K and Q2 2026 Form 10-Q/shareholder letter.")
    print(f"  10-K: {FORM_10K}")
    print(f"  10-Q: {FORM_10Q}")
    print(f"  Q2 letter: {Q2_LETTER}")
    print(f"  Treasury yields: {TREASURY_SOURCE}")
    print(f"  Industry beta: {BETA_SOURCE}")
    print(f"  Equity risk premium: {ERP_SOURCE}")
    print(f"  Default spread method: {DEFAULT_SPREAD_SOURCE}")
    print("  Assumptions: normalized FCF, forecast growth, WACC, and terminal growth")
    print("  are analyst estimates, not facts reported by Netflix.")
    print("  The $78.05 reverse-DCF target is a dated, editable reference price from")
    print("  the course research; it is not a figure from Netflix's SEC filings.")
    print("  Main limitation: terminal value is a large share of enterprise value;")
    print("  small WACC or perpetual-growth changes materially affect the result.")


def main():
    validate_inputs()
    print_base_case(calculate_dcf(GROWTH_RATES, WACC, TERMINAL_GROWTH))
    print_sensitivity()
    reverse_dcf()
    print_sources_and_notes()


if __name__ == "__main__":
    main()
