"""Lab 09: Asbury Automotive Group (ABG) five-year pro-forma case.

Uses only Python's standard library and the case inputs supplied for the lab.
All monetary amounts are USD millions; shares are millions.
"""

from copy import deepcopy


YEARS = tuple(range(2026, 2031))
YEAR_LABELS = tuple(f"FY{year}E" for year in YEARS)

# Opening FY2025 case inputs (USD millions unless noted otherwise).
OPENING_2025 = {
    "revenue": 17_999.0,
    "inventory": 2_135.8,
    "ppe": 3_070.4,
    "other_assets": 6_371.6,
    "cash": 40.4,
    "floor_plan": 2_027.0,
    "term_debt": 3_572.0,
    "other_liabilities": 2_127.5,
    "equity": 3_891.7,
    # Model initialization: the lab does not explicitly list an opening revolver.
    "revolver": 0.0,
}

# Supplied case assumptions. Labels identify the basis required by the lab.
REVENUE_GROWTH = 0.018  # [judgment]
GROSS_MARGIN = 0.1705  # [judgment]
SGA_TO_GROSS_PROFIT = (0.665, 0.655, 0.645, 0.645, 0.645)  # [judgment]
DEPRECIATION_TO_OPENING_PPE = 82.4 / 3_070.4  # [history]
NONCASH_IMPAIRMENT = 120.0  # [judgment]
CAPITAL_SPENDING = 250.0  # [guidance]
TAX_RATE = 0.255  # [judgment]
INVENTORY_DAYS = 2_135.8 / (17_999.0 - 3_071.7) * 365.0  # [history]
FLOOR_PLAN_TO_INVENTORY = 2_027.0 / 2_135.8  # [history]
OTHER_WORKING_CAPITAL_TO_REVENUE_CHANGE = 0.008  # [judgment]
MINIMUM_CASH = 25.0  # [history]
REVOLVER_LIMIT = 850.0  # [judgment]
REVOLVER_INTEREST_RATE = 0.06  # [judgment]
TERM_DEBT_REPAYMENT = 150.0  # [judgment]
SHARE_BUYBACK = 150.0  # [judgment]
FLOOR_PLAN_INTEREST_RATE = 0.0467  # [history]
TERM_DEBT_INTEREST_RATE = 0.0544  # [history]
COST_OF_EQUITY = 0.10  # [judgment]
TERMINAL_GROWTH = 0.025  # [judgment]
SHARES_OUTSTANDING = 17.951349  # [fact supplied by lab: June 30, 2026 10-Q]

TOLERANCE = 1e-7


def build_model():
    """Build the five forecast years in the calculation order required by the lab."""
    results = []
    opening = dict(OPENING_2025)

    for index, year in enumerate(YEARS):
        revenue = opening["revenue"] * (1.0 + REVENUE_GROWTH)
        gross_profit = revenue * GROSS_MARGIN
        cost_of_sales = revenue - gross_profit
        sga = gross_profit * SGA_TO_GROSS_PROFIT[index]
        depreciation = opening["ppe"] * DEPRECIATION_TO_OPENING_PPE
        impairment = NONCASH_IMPAIRMENT
        operating_income = gross_profit - sga - depreciation - impairment

        floor_plan_interest = opening["floor_plan"] * FLOOR_PLAN_INTEREST_RATE
        term_debt_interest = opening["term_debt"] * TERM_DEBT_INTEREST_RATE
        revolver_interest = opening["revolver"] * REVOLVER_INTEREST_RATE
        interest = floor_plan_interest + term_debt_interest + revolver_interest
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * TAX_RATE
        net_income = pretax_income - tax

        inventory = cost_of_sales * INVENTORY_DAYS / 365.0
        floor_plan = inventory * FLOOR_PLAN_TO_INVENTORY
        ppe = opening["ppe"] + CAPITAL_SPENDING - depreciation
        change_other_working_capital = (
            OTHER_WORKING_CAPITAL_TO_REVENUE_CHANGE
            * (revenue - opening["revenue"])
        )
        other_assets = (
            opening["other_assets"]
            + change_other_working_capital
            - impairment
        )
        term_debt = opening["term_debt"] - TERM_DEBT_REPAYMENT
        other_liabilities = opening["other_liabilities"]
        equity = opening["equity"] + net_income - SHARE_BUYBACK

        change_inventory = inventory - opening["inventory"]
        change_floor_plan = floor_plan - opening["floor_plan"]
        fcfe = (
            net_income
            + depreciation
            + impairment
            - CAPITAL_SPENDING
            - change_inventory
            - change_other_working_capital
            + change_floor_plan
            - TERM_DEBT_REPAYMENT
        )

        cash_before_revolver = opening["cash"] + fcfe - SHARE_BUYBACK
        revolver = opening["revolver"]
        revolver_movement = 0.0

        if cash_before_revolver < MINIMUM_CASH:
            draw_needed = MINIMUM_CASH - cash_before_revolver
            draw = min(draw_needed, REVOLVER_LIMIT - revolver)
            revolver += draw
            revolver_movement = draw
        elif cash_before_revolver > MINIMUM_CASH and revolver > 0.0:
            repayment = min(cash_before_revolver - MINIMUM_CASH, revolver)
            revolver -= repayment
            revolver_movement = -repayment

        cash = cash_before_revolver + revolver_movement

        operating_cash_flow = (
            net_income
            + depreciation
            + impairment
            - change_inventory
            - change_other_working_capital
            + change_floor_plan
        )
        investing_cash_flow = -CAPITAL_SPENDING
        financing_cash_flow = (
            -TERM_DEBT_REPAYMENT - SHARE_BUYBACK + revolver_movement
        )
        change_cash = (
            operating_cash_flow + investing_cash_flow + financing_cash_flow
        )

        result = {
            "year": year,
            "revenue": revenue,
            "gross_profit": gross_profit,
            "cost_of_sales": cost_of_sales,
            "sga": sga,
            "depreciation": depreciation,
            "impairment": impairment,
            "operating_income": operating_income,
            "floor_plan_interest": floor_plan_interest,
            "term_debt_interest": term_debt_interest,
            "revolver_interest": revolver_interest,
            "interest": interest,
            "pretax_income": pretax_income,
            "tax": tax,
            "net_income": net_income,
            "inventory": inventory,
            "floor_plan": floor_plan,
            "ppe": ppe,
            "other_assets": other_assets,
            "cash": cash,
            "term_debt": term_debt,
            "other_liabilities": other_liabilities,
            "equity": equity,
            "revolver": revolver,
            "change_inventory": change_inventory,
            "change_other_working_capital": change_other_working_capital,
            "change_floor_plan": change_floor_plan,
            "fcfe": fcfe,
            "cash_before_revolver": cash_before_revolver,
            "revolver_movement": revolver_movement,
            "operating_cash_flow": operating_cash_flow,
            "investing_cash_flow": investing_cash_flow,
            "financing_cash_flow": financing_cash_flow,
            "change_cash": change_cash,
            "opening_cash": opening["cash"],
        }
        results.append(result)

        opening = {
            "revenue": revenue,
            "inventory": inventory,
            "ppe": ppe,
            "other_assets": other_assets,
            "cash": cash,
            "floor_plan": floor_plan,
            "term_debt": term_debt,
            "other_liabilities": other_liabilities,
            "equity": equity,
            "revolver": revolver,
        }

    return results


def balance_sheet_gap(result):
    """Recompute the balance-sheet gap directly from individual balances."""
    assets = (
        result["cash"]
        + result["inventory"]
        + result["ppe"]
        + result["other_assets"]
    )
    liabilities_and_equity = (
        result["floor_plan"]
        + result["term_debt"]
        + result["revolver"]
        + result["other_liabilities"]
        + result["equity"]
    )
    return assets - liabilities_and_equity


def assert_balanced(results, tolerance=TOLERANCE):
    """Reject any year with a balance, cash, or revolver failure."""
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
        if not (-tolerance <= result["revolver"] <= REVOLVER_LIMIT + tolerance):
            raise ValueError(
                f"{label} revolver-limit check failed: "
                f"revolver = {result['revolver']:.1f}, "
                f"allowed range = 0.0-{REVOLVER_LIMIT:.1f}"
            )


def value_model(results):
    """Value equity only after all required model checks pass."""
    assert_balanced(results)
    pv_forecast_fcfe = sum(
        result["fcfe"] / (1.0 + COST_OF_EQUITY) ** period
        for period, result in enumerate(results, start=1)
    )
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
    """Return a year-across table with one decimal for statement values."""
    label_width = 32
    value_width = 12
    lines = [title, "-" * (label_width + value_width * len(results))]
    header = "Line item".ljust(label_width)
    header += "".join(f"FY{r['year']}E".rjust(value_width) for r in results)
    lines.append(header)
    for label, key in rows:
        line = label.ljust(label_width)
        line += "".join(f"{result[key]:,.1f}".rjust(value_width) for result in results)
        lines.append(line)
    return "\n".join(lines)


def print_model(results, valuation):
    print("ASBURY AUTOMOTIVE GROUP (ABG) FIVE-YEAR PRO-FORMA CASE")
    print("USD millions except per-share data; shares in millions")
    print("Opening revolver = 0.0 (model initialization; not explicitly listed by the lab)\n")

    income_rows = (
        ("Revenue", "revenue"),
        ("Cost of sales", "cost_of_sales"),
        ("Gross profit", "gross_profit"),
        ("SG&A", "sga"),
        ("Depreciation", "depreciation"),
        ("Noncash impairment", "impairment"),
        ("Operating income", "operating_income"),
        ("Floor plan interest", "floor_plan_interest"),
        ("Term debt interest", "term_debt_interest"),
        ("Revolver interest", "revolver_interest"),
        ("Total interest", "interest"),
        ("Pretax income", "pretax_income"),
        ("Tax", "tax"),
        ("Net income", "net_income"),
    )
    balance_rows = (
        ("Cash", "cash"),
        ("Inventory", "inventory"),
        ("PP&E", "ppe"),
        ("Other assets", "other_assets"),
        ("Floor plan", "floor_plan"),
        ("Term debt", "term_debt"),
        ("Revolver", "revolver"),
        ("Other liabilities", "other_liabilities"),
        ("Equity", "equity"),
    )
    cash_flow_rows = (
        ("Operating cash flow", "operating_cash_flow"),
        ("Investing cash flow", "investing_cash_flow"),
        ("Financing cash flow", "financing_cash_flow"),
        ("Change in cash", "change_cash"),
        ("Opening cash", "opening_cash"),
        ("Ending cash", "cash"),
        ("FCFE before revolver/buyback", "fcfe"),
        ("Revolver movement", "revolver_movement"),
        ("Share buyback", "buyback_display"),
    )

    for result in results:
        result["buyback_display"] = -SHARE_BUYBACK

    print(format_table("INCOME STATEMENT", income_rows, results))
    print()
    print(format_table("BALANCE SHEET", balance_rows, results))
    print()
    print(format_table("CASH FLOW STATEMENT", cash_flow_rows, results))
    print()

    print("REQUIRED CHECKS")
    print("-" * 52)
    for result in results:
        gap = balance_sheet_gap(result)
        cash_result = "PASS" if result["cash"] >= MINIMUM_CASH else "FAIL"
        print(
            f"FY{result['year']}E: balance-sheet gap = {gap:.1f}; "
            f"cash minimum = {cash_result} "
            f"({result['cash']:.1f} >= {MINIMUM_CASH:.1f})"
        )

    print("\nVALUATION")
    print("-" * 52)
    print(f"PV of forecast FCFE:     ${valuation['pv_forecast_fcfe']:,.2f}")
    print(f"Terminal value:          ${valuation['terminal_value']:,.2f}")
    print(f"PV of terminal value:    ${valuation['pv_terminal_value']:,.2f}")
    print(f"Equity value:            ${valuation['equity_value']:,.2f}")
    print(f"Terminal value share:     {valuation['terminal_value_share']:.2%}")
    print(f"Value per share:         ${valuation['value_per_share']:,.2f}")


def run_intentional_failure_test(results):
    """Break a copy of FY2026E cash and confirm valuation is blocked."""
    broken_results = deepcopy(results)
    broken_results[0]["cash"] = 40.4
    try:
        value_model(broken_results)
    except ValueError as error:
        print("\nINTENTIONAL FAILURE TEST")
        print("-" * 52)
        print("Set FY2026E cash to 40.4 on a separate copy.")
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
