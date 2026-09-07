#!/usr/bin/env python3
"""Compute the default Miaoshou public-collect-box draft price."""

from __future__ import annotations

import argparse
from decimal import Decimal, ROUND_CEILING

DEFAULT_MULTIPLIER = Decimal("6.85")


def draft_price(cost: Decimal, multiplier: Decimal = DEFAULT_MULTIPLIER) -> Decimal:
    """Round cost * multiplier upward to a price ending in .9."""
    if cost <= 0:
        raise ValueError("cost must be greater than zero")
    if multiplier <= 0:
        raise ValueError("multiplier must be greater than zero")
    whole = (cost * multiplier - Decimal("0.9")).to_integral_value(rounding=ROUND_CEILING)
    return whole + Decimal("0.9")


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate the default public-collect-box draft price")
    parser.add_argument("cost", type=Decimal, help="source cost")
    parser.add_argument("--multiplier", type=Decimal, default=DEFAULT_MULTIPLIER)
    args = parser.parse_args()
    try:
        price = draft_price(args.cost, args.multiplier)
    except ValueError as exc:
        parser.error(str(exc))
    print(f"cost={args.cost} multiplier={args.multiplier} price={price:.1f} stock=500")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
