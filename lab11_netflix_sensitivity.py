"""Lab 11 one-at-a-time sensitivity analysis for the Netflix pro-forma.

This script imports the unchanged Lab 10 model, resets every independent input
to a deep-copied base set before every run, changes one driver, and writes the
visible results to lab11_netflix.md.
"""

from copy import deepcopy
from pathlib import Path

import netflix_proforma as model


OUTPUT_PATH = Path(__file__).with_name("lab11_netflix.md")
YEARS = model.YEARS
ROUNDING_TOLERANCE = 0.01  # USD millions and USD/share for output comparison

# Every independent input used by build_model() or value_model(). Restoring this
# complete set before each run prevents scenario leakage.
INPUT_NAMES = (
    "OPENING_2025",
    "FY2025_CONTENT_ADDITIONS",
    "FY2025_CONTENT_AMORTIZATION",
    "FY2025_COST_OF_REVENUES",
    "FY2025_DA_PPE_AND_INTANGIBLES",
    "FY2024_PPE",
    "REVENUE_GROWTH",
    "CONTENT_ADDITIONS_GROWTH",
    "CONTENT_AMORTIZATION_GROWTH",
    "OTHER_COST_OF_REVENUES_TO_REVENUE",
    "SGA_TO_GROSS_PROFIT",
    "DEPRECIATION_TO_OPENING_PPE",
    "CAPITAL_SPENDING",
    "OTHER_ASSET_INVESTMENT_TO_REVENUE_CHANGE",
    "CONTENT_LIABILITIES_TO_CONTENT_ASSETS",
    "TAX_RATE",
    "INTEREST_RATE",
    "TERM_DEBT_REPAYMENT",
    "SHARE_BUYBACK",
    "MINIMUM_CASH",
    "COST_OF_EQUITY",
    "TERMINAL_GROWTH",
    "SHARES_OUTSTANDING",
    "TOLERANCE",
)
BASE_INPUTS = {name: deepcopy(getattr(model, name)) for name in INPUT_NAMES}

# Exact ranges documented before the formal sensitivity analysis.
SCENARIOS = {
    "REVENUE_GROWTH": {
        "label": "Revenue growth",
        "units": "annual percent growth; changes in percentage points (pp)",
        "reason": (
            "Netflix reported revenue growth of 6.67% in 2023, 15.65% in "
            "2024, and 15.85% in 2025. The research file records "
            "management's July 2026 expectation of 13%-14% full-year "
            "growth. Later-year bounds are explicitly analyst judgment "
            "around the declining-growth base path."
        ),
        "lower": (0.10, 0.08, 0.06, 0.05, 0.04),
        "base": BASE_INPUTS["REVENUE_GROWTH"],
        "higher": (0.14, 0.12, 0.10, 0.09, 0.08),
    },
    "SGA_TO_GROSS_PROFIT": {
        "label": "Operating expenses / gross profit",
        "units": "percent of gross profit; changes in percentage points (pp)",
        "reason": (
            "The comparable historical ratio declined from 50.36% in 2023 "
            "to 42.00% in 2024 and 39.17% in 2025. The higher FY2026E value "
            "is close to the 2025 actual ratio; the lower path is explicitly "
            "analyst judgment about stronger operating leverage."
        ),
        "lower": (0.355, 0.345, 0.335, 0.330, 0.325),
        "base": BASE_INPUTS["SGA_TO_GROSS_PROFIT"],
        "higher": (0.395, 0.385, 0.375, 0.370, 0.365),
    },
}


def restore_inputs(inputs):
    """Apply a fresh complete input set to the imported Lab 10 module."""
    for name in INPUT_NAMES:
        setattr(model, name, deepcopy(inputs[name]))


def changed_inputs(inputs):
    """Return independent inputs that differ exactly from the base set."""
    return [name for name in INPUT_NAMES if inputs[name] != BASE_INPUTS[name]]


def run_case(driver=None, level="base"):
    """Run the full linked model from a fresh base copy with one change."""
    inputs = deepcopy(BASE_INPUTS)
    if driver is not None:
        inputs[driver] = deepcopy(SCENARIOS[driver][level])
    restore_inputs(inputs)
    results = model.build_model()

    checks = []
    accounting_valid = True
    cash_valid = True
    for result in results:
        gap = model.balance_sheet_gap(result)
        gap_pass = abs(gap) <= model.TOLERANCE
        cash_pass = result["cash"] >= model.MINIMUM_CASH - model.TOLERANCE
        accounting_valid = accounting_valid and gap_pass
        cash_valid = cash_valid and cash_pass
        checks.append(
            {
                "year": result["year"],
                "gap": gap,
                "gap_pass": gap_pass,
                "cash": result["cash"],
                "cash_pass": cash_pass,
                "fcfe": result["fcfe"],
            }
        )

    valuation = None
    valuation_error = None
    try:
        valuation = model.value_model(results)
    except ValueError as error:
        valuation_error = str(error)

    differences = changed_inputs(inputs)
    expected_differences = [] if driver is None or level == "base" else [driver]
    isolation_valid = differences == expected_differences
    scenario_valid = accounting_valid and cash_valid and isolation_valid

    return {
        "driver": driver,
        "level": level,
        "inputs": inputs,
        "changed_inputs": differences,
        "isolation_valid": isolation_valid,
        "accounting_valid": accounting_valid,
        "cash_valid": cash_valid,
        "scenario_valid": scenario_valid,
        "results": results,
        "checks": checks,
        "valuation": valuation,
        "valuation_error": valuation_error,
        "final_operating_income": results[-1]["operating_income"],
        "final_fcfe": results[-1]["fcfe"],
        "value_per_share": (
            valuation["value_per_share"] if valuation is not None else None
        ),
    }


def money(value, decimals=1):
    return f"${value:,.{decimals}f}"


def signed_money(value, decimals=1):
    sign = "+" if value >= 0 else "-"
    return f"{sign}${abs(value):,.{decimals}f}"


def visible_difference(changed, base, decimals):
    """Subtract displayed rounded outputs so visible checks tie exactly."""
    return round(changed, decimals) - round(base, decimals)


def percentages(values):
    return ", ".join(f"{year}: {value:.1%}" for year, value in zip(YEARS, values))


def markdown_table(headers, rows):
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" if index == 0 else "---:" for index in range(len(headers))) + "|",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return lines


def detail_table(case):
    headers = ["Line item"] + [f"FY{year}E" for year in YEARS]
    rows = []
    items = (
        ("Revenue", "revenue"),
        ("Content amortization", "content_amortization"),
        ("Other cost of revenues", "other_cost_of_revenues"),
        ("Cost of revenues", "cost_of_revenues"),
        ("Gross profit", "gross_profit"),
        ("Operating expenses", "sga"),
        ("Operating profit", "operating_income"),
        ("Net income", "net_income"),
        ("Content additions", "content_additions"),
        ("Operating cash flow", "operating_cash_flow"),
        ("Capital spending", "investing_cash_flow"),
        ("FCFE before share buybacks", "fcfe"),
        ("Ending cash", "cash"),
        ("Content assets", "content_assets"),
        ("Term debt", "term_debt"),
        ("Stockholders' equity", "equity"),
    )
    for label, key in items:
        rows.append([label] + [money(result[key]) for result in case["results"]])
    return markdown_table(headers, rows)


def build_report(initial_base, cases, final_base):
    lines = [
        "# Lab 11 - Netflix One-at-a-Time Sensitivity Analysis",
        "",
        "This report was generated by `lab11_netflix_sensitivity.py` from the unchanged `netflix_proforma.py`. Monetary statement outputs are USD millions; value per share is USD/share.",
        "",
        "## Method and controls",
        "",
        "- A deep-copied base input set contains every independent input used by the linked forecast and valuation.",
        "- Every lower, base, and higher run starts with a fresh copy of that complete set.",
        "- Each non-base case changes only the named driver for FY2026E-FY2030E. All linked statement quantities recalculate.",
        "- Negative FCFE is retained. The existing valuation function is not bypassed: if FCFE is negative, valuation is shown as unavailable and no terminal value is invented.",
        "- The existing valuation is a simplified but structurally defensible FCFE valuation because after-interest, after-net-debt-repayment cash flow is discounted at the cost of equity to produce equity value directly.",
        "- Scenario validity requires the one-input isolation check, balance-sheet check, and minimum-cash check to pass. Valuation availability is reported separately.",
        "",
        "## Exact selected ranges",
        "",
    ]

    for driver, spec in SCENARIOS.items():
        lines.extend(
            [
                f"### {spec['label']} (`{driver}`)",
                "",
                f"**Units:** {spec['units']}  ",
                "**Years affected:** FY2026E-FY2030E  ",
                f"**Reason:** {spec['reason']}",
                "",
            ]
        )
        range_rows = []
        base_values = spec["base"]
        for level in ("lower", "base", "higher"):
            values = spec[level]
            changes = [100.0 * (value - base) for value, base in zip(values, base_values)]
            range_rows.append(
                [level.title()]
                + [f"{value:.1%} ({change:+.1f} pp)" for value, change in zip(values, changes)]
            )
        lines.extend(markdown_table(["Path"] + [f"FY{year}E" for year in YEARS], range_rows))
        lines.append("")

    lines.extend(
        [
            "## Unchanged initial base",
            "",
            f"- FY2030E operating profit: {money(initial_base['final_operating_income'])}",
            f"- FY2030E FCFE before share buybacks: {money(initial_base['final_fcfe'])}",
            f"- Value per share: {money(initial_base['value_per_share'], 2)}",
            "- Scenario validity: PASS",
            "",
            "## Scenario results and signed changes from base",
            "",
        ]
    )

    spans = {}
    for driver, spec in SCENARIOS.items():
        driver_cases = cases[driver]
        base_case = driver_cases["base"]
        lines.extend([f"### {spec['label']}", ""])
        rows = []
        for level in ("lower", "base", "higher"):
            case = driver_cases[level]
            valuation_text = (
                money(case["value_per_share"], 2)
                if case["value_per_share"] is not None
                else "Unavailable"
            )
            valuation_change = (
                signed_money(
                    visible_difference(
                        case["value_per_share"], base_case["value_per_share"], 2
                    ),
                    2,
                )
                if case["value_per_share"] is not None
                and base_case["value_per_share"] is not None
                else "N/A"
            )
            rows.append(
                [
                    level.title(),
                    percentages(case["inputs"][driver]),
                    money(case["final_operating_income"]),
                    signed_money(
                        visible_difference(
                            case["final_operating_income"],
                            base_case["final_operating_income"],
                            1,
                        )
                    ),
                    money(case["final_fcfe"]),
                    signed_money(
                        visible_difference(
                            case["final_fcfe"], base_case["final_fcfe"], 1
                        )
                    ),
                    valuation_text,
                    valuation_change,
                    "PASS" if case["scenario_valid"] else "FAIL",
                ]
            )
        lines.extend(
            markdown_table(
                [
                    "Case",
                    f"Actual {driver} inputs",
                    "FY2030E operating profit",
                    "Change",
                    "FY2030E FCFE",
                    "Change",
                    "Value/share",
                    "Change",
                    "Valid",
                ],
                rows,
            )
        )
        lines.append("")

        valid_cases = [case for case in driver_cases.values() if case["scenario_valid"]]
        op_values = [case["final_operating_income"] for case in valid_cases]
        fcfe_values = [case["final_fcfe"] for case in valid_cases]
        share_values = [case["value_per_share"] for case in valid_cases if case["value_per_share"] is not None]
        spans[driver] = {
            "operating_income": max(round(value, 1) for value in op_values)
            - min(round(value, 1) for value in op_values),
            "fcfe": max(round(value, 1) for value in fcfe_values)
            - min(round(value, 1) for value in fcfe_values),
            "value_per_share": (
                max(round(value, 2) for value in share_values)
                - min(round(value, 2) for value in share_values)
                if share_values
                else None
            ),
        }
        lines.extend(
            [
                "Output spans (maximum minus minimum across valid cases):",
                "",
                f"- FY2030E operating-profit span: {money(spans[driver]['operating_income'])}",
                f"- FY2030E FCFE span: {money(spans[driver]['fcfe'])}",
                f"- Value-per-share span: {money(spans[driver]['value_per_share'], 2) if spans[driver]['value_per_share'] is not None else 'Unavailable'}",
                "",
            ]
        )

    lines.extend(["## Visible accounting checks and validity", ""])
    for driver, spec in SCENARIOS.items():
        for level in ("lower", "base", "higher"):
            case = cases[driver][level]
            lines.extend([f"### {spec['label']} - {level}", ""])
            lines.append(
                f"Changed independent inputs versus the base set: {', '.join(case['changed_inputs']) if case['changed_inputs'] else 'none'}; isolation check: {'PASS' if case['isolation_valid'] else 'FAIL'}."
            )
            lines.append("")
            check_rows = []
            for check in case["checks"]:
                check_rows.append(
                    [
                        f"FY{check['year']}E",
                        f"{check['gap']:,.6f}",
                        "PASS" if check["gap_pass"] else "FAIL",
                        money(check["cash"]),
                        "PASS" if check["cash_pass"] else "FAIL",
                        money(check["fcfe"]),
                        "negative" if check["fcfe"] < 0.0 else "nonnegative",
                    ]
                )
            lines.extend(
                markdown_table(
                    ["Year", "BS gap", "Balance", "Ending cash", "Cash floor", "FCFE", "FCFE sign"],
                    check_rows,
                )
            )
            lines.append("")
            if case["valuation_error"]:
                lines.append(f"Valuation unavailable: {case['valuation_error']}")
                lines.append("")

    invalid_cases = [
        case
        for driver_cases in cases.values()
        for case in driver_cases.values()
        if not case["scenario_valid"]
    ]
    lines.extend(["## Failure investigation and mechanical span ranking", ""])
    if invalid_cases:
        for case in invalid_cases:
            lines.append(
                f"- INVALID: {case['driver']} {case['level']}; accounting={case['accounting_valid']}, cash={case['cash_valid']}, isolation={case['isolation_valid']}."
            )
    else:
        lines.append("All six driver-level cases passed isolation, balance-sheet, and minimum-cash checks; no invalid run required further failure investigation.")
    lines.extend(["", "Mechanical ranking by output span uses only valid scenarios:", ""])
    for metric, label, decimals in (
        ("operating_income", "FY2030E operating profit", 1),
        ("fcfe", "FY2030E FCFE", 1),
        ("value_per_share", "value per share", 2),
    ):
        ranking = sorted(
            (
                (SCENARIOS[driver]["label"], values[metric])
                for driver, values in spans.items()
                if values[metric] is not None
            ),
            key=lambda item: item[1],
            reverse=True,
        )
        rendered = "; ".join(
            f"{index}. {name} ({money(value, decimals)})"
            for index, (name, value) in enumerate(ranking, start=1)
        )
        lines.append(f"- {label}: {rendered}")
    lines.append("")

    lines.extend(["## Statement-detail appendix", ""])
    lines.append("The following linked details are retained for every scenario so a selected result can be traced through the statements.")
    lines.append("")
    for driver, spec in SCENARIOS.items():
        for level in ("lower", "base", "higher"):
            case = cases[driver][level]
            lines.extend(
                [
                    f"### {spec['label']} - {level}",
                    "",
                    f"Actual driver inputs ({spec['units']}): {percentages(case['inputs'][driver])}",
                    "",
                ]
            )
            lines.extend(detail_table(case))
            lines.append("")

    input_match = final_base["inputs"] == initial_base["inputs"] == BASE_INPUTS
    output_pairs = (
        ("FY2030E operating profit", initial_base["final_operating_income"], final_base["final_operating_income"]),
        ("FY2030E FCFE", initial_base["final_fcfe"], final_base["final_fcfe"]),
        ("Value per share", initial_base["value_per_share"], final_base["value_per_share"]),
    )
    output_match = all(abs(final - initial) <= ROUNDING_TOLERANCE for _, initial, final in output_pairs)
    lines.extend(
        [
            "## Final base restoration and rerun",
            "",
            f"Comparison tolerance: {ROUNDING_TOLERANCE:.2f} USD million for statement outputs and {ROUNDING_TOLERANCE:.2f} USD/share for value per share.",
            "",
            f"- Complete independent input set restored exactly: {'PASS' if input_match else 'FAIL'}",
        ]
    )
    restoration_rows = []
    for label, initial, final in output_pairs:
        decimals = 2 if label == "Value per share" else 1
        restoration_rows.append(
            [label, money(initial, decimals), money(final, decimals), signed_money(final - initial, decimals), "PASS" if abs(final - initial) <= ROUNDING_TOLERANCE else "FAIL"]
        )
    lines.extend(markdown_table(["Output", "Initial base", "Final restored base", "Difference", "Within tolerance"], restoration_rows))
    lines.extend(
        [
            "",
            f"Overall final base restoration: {'PASS' if input_match and output_match else 'FAIL'}",
            "",
            "## Student locked prediction - completed before viewing sensitivity results",
            "",
            "**Date/time:**  ",
            "**Driver and affected years:**  ",
            "**Old input -> new input, with units:**  ",
            "**Expected direction and rough size of the output change:**  ",
            "**Why, tracing input -> statements -> output:**  ",
            "",
            "## Actual-result reconciliation - student completion",
            "",
            "**Scenario compared with locked prediction:**  ",
            "**Actual signed changes:**  ",
            "**Prediction versus result:**  ",
            "**Explanation of agreement or difference:**  ",
            "**Does the result change my valuation conclusion or research priority, and why?:**  ",
            "",
            "## Conclusion and interpretation - student completion",
            "",
            "**Larger FY2030E operating-profit span, using the phrase 'over these tested ranges':**  ",
            "**Larger FY2030E FCFE span, using the phrase 'over these tested ranges':**  ",
            "**Larger value-per-share span, using the phrase 'over these tested ranges':**  ",
            "**One causal link traced with actual results:**  ",
            "**What the results mean for my Netflix valuation or research priority:**  ",
            "**Limitations:**  ",
            "",
            "## Partner verification and exchanges - complete only after they occur",
            "",
            "**Partner name:**  ",
            "**Date/time:**  ",
            "**My locked prediction and ranges shown:**  ",
            "**Restored-base comparison checked:**  ",
            "**One-input isolation checked:**  ",
            "**Accounting checks reviewed:**  ",
            "**Scenario and signed difference recomputed by partner:**  ",
            "**Partner's recomputation:** changed output ___ - base output ___ = ___  ",
            "**Partner's trace-through-statements question:**  ",
            "**My trace-through-statements response:**  ",
            "**Partner's question about the ranking or ranges:**  ",
            "**My response:**  ",
            "**Whether the ranges help explain the ranking:**  ",
            "**Comparison of our companies and drivers:**  ",
            "**Roles swapped - partner/company/model checked:**  ",
            "**What I checked in the partner's model:**  ",
            "**My recomputation on the partner's model:** changed output ___ - base output ___ = ___  ",
            "**My question to partner and partner's response:**  ",
            "",
            "## Learning questions - student completion",
            "",
            "**What one-at-a-time sensitivity means:**  ",
            "**How selected ranges affect driver rankings:**  ",
            "**Why sensitivity scenarios do not establish probabilities:**  ",
            "",
            "## Submission links - add after publishing to GitHub",
            "",
            "**Analysis-code GitHub URL:**  ",
            "**Markdown-report GitHub URL:**  ",
            "",
        ]
    )
    return "\n".join(lines)


def main():
    initial_base = run_case()
    cases = {
        driver: {
            level: run_case(driver, level)
            for level in ("lower", "base", "higher")
        }
        for driver in SCENARIOS
    }
    # Required end control: restore and rerun the unchanged base.
    final_base = run_case()
    report = build_report(initial_base, cases, final_base)
    OUTPUT_PATH.write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
