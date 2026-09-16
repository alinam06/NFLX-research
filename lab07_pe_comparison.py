"""Lab 07: comparable-company P/E policy and implied price analysis.

Run:
    python3 lab07_pe_comparison.py

The inputs are frozen case data: December 31, 2024 closing prices paired
with subsequently reported FY2024 total GAAP diluted EPS.
"""

from statistics import median


# -----------------------------------------------------------------------------
# EDITABLE INPUTS
# -----------------------------------------------------------------------------
TARGET = {
    "ticker": "ABG",
    "name": "Asbury Automotive",
    "price": 243.03,
    "diluted_eps": 21.50,
}

PEERS = [
    {
        "ticker": "AN",
        "name": "AutoNation",
        "price": 169.84,
        "diluted_eps": 16.92,
    },
    {
        "ticker": "GPI",
        "name": "Group 1 Automotive",
        "price": 421.48,
        "diluted_eps": 36.81,
    },
]


def is_positive_number(value):
    """Return True only for a usable positive int or float."""
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def clean_ticker(value):
    """Normalize a ticker for comparison and deduplication."""
    return str(value).strip().upper()


def deduplicate_and_exclude_target(peers, target_ticker):
    """Keep the first occurrence of each ticker and remove the target."""
    target_key = clean_ticker(target_ticker)
    seen = set()
    cleaned = []
    for peer in peers:
        ticker = clean_ticker(peer.get("ticker", ""))
        if not ticker or ticker == target_key or ticker in seen:
            continue
        seen.add(ticker)
        peer_copy = dict(peer)
        peer_copy["ticker"] = ticker
        cleaned.append(peer_copy)
    return cleaned


def peer_multiple(peer):
    """Return P/E at full precision, or None when it is not meaningful."""
    price = peer.get("price")
    eps = peer.get("diluted_eps")
    if not is_positive_number(price) or not is_positive_number(eps):
        return None
    return price / eps


def signed_money(amount):
    """Format a dollar change with a true minus sign."""
    sign = "+" if amount >= 0 else "−"
    return f"{sign}${abs(amount):,.2f}"


def print_results():
    peers = deduplicate_and_exclude_target(PEERS, TARGET["ticker"])
    peer_rows = [(peer, peer_multiple(peer)) for peer in peers]
    valid_rows = [(peer, multiple) for peer, multiple in peer_rows if multiple is not None]

    print("LAB 07 — COMPARABLE-COMPANY P/E ANALYSIS")
    print("Frozen case inputs: 2024-12-31 prices and FY2024 GAAP diluted EPS")
    print("P/E uses equity price and EPS; no cash or debt adjustment is made.\n")

    print("Peer P/E multiples")
    if not peer_rows:
        print("  no usable peers")
    for peer, multiple in peer_rows:
        label = f"{peer.get('name', 'Unnamed peer')} ({peer['ticker']})"
        if multiple is None:
            print(f"  {label}: not meaningful")
        else:
            print(f"  {label}: {multiple:.6f}×")

    print("\nAsbury implied share price")
    target_eps = TARGET.get("diluted_eps")
    if not valid_rows:
        print("  no usable peers")
        full_median_price = None
    elif not is_positive_number(target_eps):
        print("  not meaningful")
        full_median_price = None
    else:
        multiples = [multiple for _, multiple in valid_rows]
        minimum_multiple = min(multiples)
        median_multiple = median(multiples)
        maximum_multiple = max(multiples)
        minimum_price = minimum_multiple * target_eps
        full_median_price = median_multiple * target_eps
        maximum_price = maximum_multiple * target_eps

        if len(multiples) == 1:
            print(f"  Reference peer P/E: {median_multiple:.6f}×")
            print(f"  Reference estimate: ${full_median_price:,.2f}")
            print("  Range: not available with one valid peer")
        else:
            print(f"  Minimum peer P/E: {minimum_multiple:.6f}×")
            print(f"  Median peer P/E:  {median_multiple:.6f}×")
            print(f"  Maximum peer P/E: {maximum_multiple:.6f}×")
            print(f"  Implied range: ${minimum_price:,.2f}–${maximum_price:,.2f}")
            print(f"  At peer median: ${full_median_price:,.2f}")

    print("\nPeer-removal analysis")
    if not peer_rows:
        print("  no estimate")
    for removed_peer, _ in peer_rows:
        remaining = [
            multiple
            for peer, multiple in valid_rows
            if peer["ticker"] != removed_peer["ticker"]
        ]
        removed_label = f"{removed_peer.get('name', 'Unnamed peer')} ({removed_peer['ticker']})"
        if not remaining or not is_positive_number(target_eps):
            print(f"  Remove {removed_label}: no estimate")
            continue
        remaining_price = median(remaining) * target_eps
        if full_median_price is None:
            print(f"  Remove {removed_label}: ${remaining_price:,.2f}; change not meaningful")
        else:
            change = remaining_price - full_median_price
            print(
                f"  Remove {removed_label}: ${remaining_price:,.2f}; "
                f"change {signed_money(change)}"
            )


if __name__ == "__main__":
    print_results()
