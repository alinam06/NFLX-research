"""Lab 10: Netflix (NFLX) five-year pro-forma model.

The model uses the supplied local Netflix 2023, 2024, and 2025 Forms 10-K.
All monetary amounts are USD millions; shares are millions. Python standard
library only.
"""

from copy import deepcopy


YEARS = tuple(range(2026, 2031))

# FY2025 opening balances from Netflix's 2025 Form 10-K.
OPENING_2025 = {
    "revenue": 45_183.036,
    "content_assets": 32_778.392,
    "ppe": 2_004.350,
    "other_assets": 11_780.570,
    "cash": 9_033.681,
    "content_liabilities": 5_664.330,
    "term_debt": 14_462.836,
    "other_liabilities": 8_854.339,
    "equity": 26_615.488,
}

# Historical FY2025 inputs used to anchor ratios.
FY2025_CONTENT_ADDITIONS = 17_096.617
FY2025_CONTENT_AMORTIZATION = 16_422.166
FY2025_COST_OF_REVENUES = 23_275.329
FY2025_DA_PPE_AND_INTANGIBLES = 333.389
FY2024_PPE = 1_593.756

# Base-case assumptions. Judgment assumptions are deliberately editable.
REVENUE_GROWTH = (0.12, 0.10, 0.08, 0.07, 0.06)  # [judgment]
CONTENT_ADDITIONS_GROWTH = (0.08, 0.07, 0.06, 0.05, 0.04)  # [judgment]
CONTENT_AMORTIZATION_GROWTH = (0.08, 0.07, 0.06, 0.05, 0.04)  # [judgment]
OTHER_COST_OF_REVENUES_TO_REVENUE = (
    FY2025_COST_OF_REVENUES - FY2025_CONTENT_AMORTIZATION
) / OPENING_2025["revenue"]  # [history]
SGA_TO_GROSS_PROFIT = (0.375, 0.365, 0.355, 0.350, 0.345)  # [judgment]
DEPRECIATION_TO_OPENING_PPE = FY2025_DA_PPE_AND_INTANGIBLES / FY2024_PPE  # [history]
CAPITAL_SPENDING = 700.0  # [judgment]
OTHER_ASSET_INVESTMENT_TO_REVENUE_CHANGE = 0.05  # [judgment]
CONTENT_LIABILITIES_TO_CONTENT_ASSETS = (
    OPENING_2025["content_liabilities"] / OPENING_2025["content_assets"]
)  # [history]
TAX_RATE = 0.14  # [judgment]
INTEREST_RATE = 776.510 / (1_784.453 + 13_798.351)  # [history]
TERM_DEBT_REPAYMENT = 1_000.0  # [judgment]
SHARE_BUYBACK = 6_000.0  # [judgment]
MINIMUM_CASH = 5_000.0  # [judgment]
COST_OF_EQUITY = 0.09  # [judgment]
TERMINAL_GROWTH = 0.03  # [judgment]
SHARES_OUTSTANDING = 4_222.162150  # [history: FY2025 Form 10-K]

TOLERANCE = 1e-7


def build_model():
    """Build five linked forecast years using content assets as the key schedule."""
    results = []
    opening = dict(OPENING_2025)
    prior_content_additions = FY2025_CONTENT_ADDITIONS
    prior_content_amortization = FY2025_CONTENT_AMORTIZATION

    for index, year in enumerate(YEARS):
        revenue = opening["revenue"] * (1.0 + REVENUE_GROWTH[index])
        content_additions = prior_content_additions * (
            1.0 + CONTENT_ADDITIONS_GROWTH[index]
        )
        content_amortization = prior_content_amortization * (
            1.0 + CONTENT_AMORTIZATION_GROWTH[index]
        )
        other_cost_of_revenues = revenue * OTHER_COST_OF_REVENUES_TO_REVENUE
        cost_of_revenues = content_amortization + other_cost_of_revenues
        gross_profit = revenue - cost_of_revenues

        sga = gross_profit * SGA_TO_GROSS_PROFIT[index]
        depreciation = opening["ppe"] * DEPRECIATION_TO_OPENING_PPE
        operating_income = gross_profit - sga - depreciation

        interest = opening["term_debt"] * INTEREST_RATE
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * TAX_RATE
        net_income = pretax_income - tax

        content_assets = (
            opening["content_assets"] + content_additions - content_amortization
        )
        content_liabilities = (
            content_assets * CONTENT_LIABILITIES_TO_CONTENT_ASSETS
        )
        ppe = opening["ppe"] + CAPITAL_SPENDING - depreciation
        change_other_assets = (
            OTHER_ASSET_INVESTMENT_TO_REVENUE_CHANGE
            * (revenue - opening["revenue"])
        )
        other_assets = opening["other_assets"] + change_other_assets
        term_debt = opening["term_debt"] - TERM_DEBT_REPAYMENT
        other_liabilities = opening["other_liabilities"]
        equity = opening["equity"] + net_income - SHARE_BUYBACK

        change_content_liabilities = (
            content_liabilities - opening["content_liabilities"]
        )
        operating_cash_flow = (
            net_income
            + depreciation
            + content_amortization
            - content_additions
            - change_other_assets
            + change_content_liabilities
        )
        investing_cash_flow = -CAPITAL_SPENDING
        fcfe = (
            operating_cash_flow
            + investing_cash_flow
            - TERM_DEBT_REPAYMENT
        )
        financing_cash_flow = -TERM_DEBT_REPAYMENT - SHARE_BUYBACK
        change_cash = operating_cash_flow + investing_cash_flow + financing_cash_flow
        cash = opening["cash"] + change_cash

        result = {
            "year": year,
            "revenue": revenue,
            "content_amortization": content_amortization,
            "other_cost_of_revenues": other_cost_of_revenues,
            "cost_of_revenues": cost_of_revenues,
            "gross_profit": gross_profit,
            "sga": sga,
            "depreciation": depreciation,
            "operating_income": operating_income,
            "interest": interest,
            "pretax_income": pretax_income,
            "tax": tax,
            "net_income": net_income,
            "cash": cash,
            "content_assets": content_assets,
            "ppe": ppe,
            "other_assets": other_assets,
            "content_liabilities": content_liabilities,
            "term_debt": term_debt,
            "other_liabilities": other_liabilities,
            "equity": equity,
            "content_additions": content_additions,
            "change_content_liabilities": change_content_liabilities,
            "change_other_assets": change_other_assets,
            "operating_cash_flow": operating_cash_flow,
            "investing_cash_flow": investing_cash_flow,
            "financing_cash_flow": financing_cash_flow,
            "change_cash": change_cash,
            "opening_cash": opening["cash"],
            "fcfe": fcfe,
            "buyback_display": -SHARE_BUYBACK,
        }
        results.append(result)

        opening = {
            "revenue": revenue,
            "content_assets": content_assets,
            "ppe": ppe,
            "other_assets": other_assets,
            "cash": cash,
            "content_liabilities": content_liabilities,
            "term_debt": term_debt,
            "other_liabilities": other_liabilities,
            "equity": equity,
        }
        prior_content_additions = content_additions
        prior_content_amortization = content_amortization

    return results


def balance_sheet_gap(result):
    """Recompute assets minus liabilities and equity from individual balances."""
    assets = (
        result["cash"]
        + result["content_assets"]
        + result["ppe"]
        + result["other_assets"]
    )
    liabilities_and_equity = (
        result["content_liabilities"]
        + result["term_debt"]
        + result["other_liabilities"]
        + result["equity"]
    )
    return assets - liabilities_and_equity


def assert_balanced(results, tolerance=TOLERANCE):
    """Stop before valuation if any forecast year fails a required check."""
    for result in results:
        label = f"FY{result['year']}E"
        gap = balance_sheet_gap(result)
        if abs(gap) > tolerance:
            raise ValueError(
                f"{label} balance-sheet check failed: gap = {gap:.1f}"
            )
        if result["cash"] < MINIMUM_CASH - tolerance:
            raise ValueError(
                f"{label} cash-minimum check failed: "
                f"cash = {result['cash']:.1f}, minimum = {MINIMUM_CASH:.1f}"
            )


def value_model(results):
    """Discount positive FCFE only after the complete check block passes."""
    assert_balanced(results)
    negative_years = [r["year"] for r in results if r["fcfe"] < 0.0]
    if negative_years:
        labels = ", ".join(f"FY{year}E" for year in negative_years)
        raise ValueError(f"Negative FCFE requires separate treatment: {labels}")

    pv_forecast_fcfe = sum(
        result["fcfe"] / (1.0 + COST_OF_EQUITY) ** period
        for period, result in enumerate(results, start=1)
    )
    # The fixed debt repayment is not assumed to continue forever.
    terminal_fcfe = results[-1]["fcfe"] + TERM_DEBT_REPAYMENT
    terminal_value = (
        terminal_fcfe
        * (1.0 + TERMINAL_GROWTH)
        / (COST_OF_EQUITY - TERMINAL_GROWTH)
    )
    pv_terminal_value = terminal_value / (1.0 + COST_OF_EQUITY) ** len(results)
    equity_value = pv_forecast_fcfe + pv_terminal_value
    value_per_share = equity_value / SHARES_OUTSTANDING
    terminal_value_share = pv_terminal_value / equity_value
    return {
        "pv_forecast_fcfe": pv_forecast_fcfe,
        "terminal_value": terminal_value,
        "pv_terminal_value": pv_terminal_value,
        "equity_value": equity_value,
        "value_per_share": value_per_share,
        "terminal_value_share": terminal_value_share,
    }


def format_table(title, rows, results):
    label_width = 34
    value_width = 13
    lines = [title, "-" * (label_width + value_width * len(results))]
    header = "Line item".ljust(label_width)
    header += "".join(f"FY{r['year']}E".rjust(value_width) for r in results)
    lines.append(header)
    for label, key in rows:
        line = label.ljust(label_width)
        line += "".join(f"{r[key]:,.1f}".rjust(value_width) for r in results)
        lines.append(line)
    return "\n".join(lines)


def print_model(results, valuation):
    print("NETFLIX (NFLX) FIVE-YEAR PRO-FORMA MODEL")
    print("USD millions except per-share data; shares in millions")
    print("Company-specific schedule: content assets, additions, liabilities, and amortization\n")

    income_rows = (
        ("Revenue", "revenue"),
        ("Content amortization", "content_amortization"),
        ("Other cost of revenues", "other_cost_of_revenues"),
        ("Cost of revenues", "cost_of_revenues"),
        ("Gross profit", "gross_profit"),
        ("Operating expenses", "sga"),
        ("Depreciation", "depreciation"),
        ("Operating income", "operating_income"),
        ("Interest", "interest"),
        ("Pretax income", "pretax_income"),
        ("Tax", "tax"),
        ("Net income", "net_income"),
    )
    balance_rows = (
        ("Cash", "cash"),
        ("Content assets, net", "content_assets"),
        ("PP&E, net", "ppe"),
        ("Other assets", "other_assets"),
        ("Content liabilities", "content_liabilities"),
        ("Term debt", "term_debt"),
        ("Other liabilities", "other_liabilities"),
        ("Stockholders' equity", "equity"),
    )
    cash_flow_rows = (
        ("Net income", "net_income"),
        ("Content additions", "content_additions"),
        ("Content amortization", "content_amortization"),
        ("Operating cash flow", "operating_cash_flow"),
        ("Investing cash flow", "investing_cash_flow"),
        ("Financing cash flow", "financing_cash_flow"),
        ("Change in cash", "change_cash"),
        ("Opening cash", "opening_cash"),
        ("Ending cash", "cash"),
        ("FCFE before share buybacks", "fcfe"),
        ("Share buybacks", "buyback_display"),
    )

    print(format_table("INCOME STATEMENT", income_rows, results))
    print()
    print(format_table("BALANCE SHEET", balance_rows, results))
    print()
    print(format_table("CASH FLOW STATEMENT", cash_flow_rows, results))
    print()

    print("REQUIRED CHECKS")
    print("-" * 58)
    for result in results:
        gap = balance_sheet_gap(result)
        displayed_gap = 0.0 if abs(gap) <= TOLERANCE else gap
        cash_result = "PASS" if result["cash"] >= MINIMUM_CASH else "FAIL"
        fcfe_label = "positive" if result["fcfe"] >= 0.0 else "negative FCFE"
        print(
            f"FY{result['year']}E: gap = {displayed_gap:.1f}; "
            f"cash minimum = {cash_result} "
            f"({result['cash']:.1f} >= {MINIMUM_CASH:.1f}); {fcfe_label}"
        )

    print("\nVALUATION")
    print("-" * 58)
    print(f"PV of forecast FCFE:     ${valuation['pv_forecast_fcfe']:,.2f}")
    print(f"Terminal value:          ${valuation['terminal_value']:,.2f}")
    print(f"PV of terminal value:    ${valuation['pv_terminal_value']:,.2f}")
    print(f"Equity value:            ${valuation['equity_value']:,.2f}")
    print(f"Terminal value share:     {valuation['terminal_value_share']:.2%}")
    print(f"Value per share:         ${valuation['value_per_share']:,.2f}")


def run_intentional_failure_test(results):
    """Demonstrate that an unexplained cash edit blocks valuation."""
    broken = deepcopy(results)
    broken[0]["cash"] = OPENING_2025["cash"]
    try:
        value_model(broken)
    except ValueError as error:
        print("\nINTENTIONAL FAILURE TEST")
        print("-" * 58)
        print("Reset FY2026E cash to FY2025 opening cash on a separate copy.")
        print(f"Valuation stopped: {error}")
        return str(error)
    raise AssertionError("Intentional failure test did not stop valuation.")


def main():
    results = build_model()
    assert_balanced(results)
    valuation = value_model(results)
    print_model(results, valuation)
    run_intentional_failure_test(results)


if __name__ == "__main__":
    main()
