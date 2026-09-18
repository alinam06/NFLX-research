"""Lab 08: Netflix comparable-company P/E valuation.

Uses only the Python standard library. Edit the input block below as needed.
"""

from statistics import median


# ------------------------------ EDITABLE INPUTS ------------------------------
COMPARISON_DATE = "2026-09-10"
TRADING_DATE_RULE = (
    "Use the closing price on the comparison date; if it is not a trading day, "
    "use the nearest prior trading day."
)

TARGET = {
    "company": "Netflix, Inc.",
    "ticker": "NFLX",
    "price": 76.01,
    "annual_diluted_eps": 2.53,
}

PEERS = [
    {
        "company": "The Walt Disney Company",
        "ticker": "DIS",
        "decision": "use",
        "price": 105.82,
        "annual_diluted_eps": 6.85,
    },
    {
        "company": "Warner Bros. Discovery, Inc.",
        "ticker": "WBD",
        "decision": "qualify",
        "price": 28.20,
        "annual_diluted_eps": 0.29,
    },
]
# -----------------------------------------------------------------------------


def is_positive_number(value):
    """Return True only for finite, positive numeric inputs."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return number > 0 and number != float("inf")


def clean_ticker(value):
    return str(value).strip().upper()


def deduplicate_and_exclude_target(peers, target_ticker):
    """Keep the first occurrence of each ticker and remove the target."""
    target_ticker = clean_ticker(target_ticker)
    seen = set()
    cleaned = []
    for peer in peers:
        ticker = clean_ticker(peer.get("ticker", ""))
        if not ticker or ticker == target_ticker or ticker in seen:
            continue
        seen.add(ticker)
        cleaned.append(peer)
    return cleaned


def peer_multiple(peer):
    """Return price / annual GAAP diluted EPS, or None if not meaningful."""
    price = peer.get("price")
    eps = peer.get("annual_diluted_eps")
    if not is_positive_number(price) or not is_positive_number(eps):
        return None
    return float(price) / float(eps)


def signed_money(value):
    return f"{value:+.2f}"


def print_results():
    peers = deduplicate_and_exclude_target(PEERS, TARGET["ticker"])
    peer_rows = [(peer, peer_multiple(peer)) for peer in peers]
    valid_rows = [(peer, multiple) for peer, multiple in peer_rows if multiple is not None]

    print("Lab 08 — Netflix Comparable-Company P/E Valuation")
    print(f"Comparison date: {COMPARISON_DATE}")
    print(f"Trading-date rule: {TRADING_DATE_RULE}")
    print()
    print("Peer P/E calculations:")
    for peer, multiple in peer_rows:
        label = f"{peer.get('company', '')} ({clean_ticker(peer.get('ticker', ''))})"
        decision = peer.get("decision", "unresolved")
        if multiple is None:
            print(f"  {label} [{decision}]: not meaningful")
        else:
            print(f"  {label} [{decision}]: {multiple:.6f}x")

    target_eps = TARGET.get("annual_diluted_eps")
    if not is_positive_number(target_eps):
        print()
        print("Netflix annual diluted EPS is zero, negative, or missing.")
        print("P/E cannot support a valuation; no substitute method is used.")
        return

    multiples = [multiple for _, multiple in valid_rows]
    print()
    if not multiples:
        print("Result: no usable peers")
        return

    minimum = min(multiples)
    midpoint = median(multiples)
    maximum = max(multiples)
    target_eps = float(target_eps)
    full_estimate = midpoint * target_eps

    print("Peer multiple summary:")
    print(f"  Minimum: {minimum:.6f}x")
    print(f"  Median:  {midpoint:.6f}x")
    print(f"  Maximum: {maximum:.6f}x")
    print()
    if len(multiples) == 1:
        print(f"Reference estimate (one valid peer): ${full_estimate:.2f}")
        print("No peer range is available with one valid peer.")
    else:
        print("Netflix implied prices:")
        print(f"  Minimum: ${minimum * target_eps:.2f}")
        print(f"  Median:  ${full_estimate:.2f}")
        print(f"  Maximum: ${maximum * target_eps:.2f}")

    print()
    print("Peer-removal sensitivity:")
    for removed_peer, _ in valid_rows:
        removed_ticker = clean_ticker(removed_peer.get("ticker", ""))
        remaining = [
            multiple
            for peer, multiple in valid_rows
            if clean_ticker(peer.get("ticker", "")) != removed_ticker
        ]
        if not remaining:
            print(f"  Remove {removed_ticker}: no estimate")
            continue
        remaining_estimate = median(remaining) * target_eps
        dollar_change = remaining_estimate - full_estimate
        print(
            f"  Remove {removed_ticker}: ${remaining_estimate:.2f} "
            f"({signed_money(dollar_change)} vs. full-peer estimate)"
        )


if __name__ == "__main__":
    print_results()
