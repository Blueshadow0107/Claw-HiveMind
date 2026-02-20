#!/usr/bin/env python3
"""
Polymarket Market Scanner
Scans for trading opportunities based on configurable criteria.
"""

import requests
import json
import sys
from datetime import datetime

GAMMA_URL = "https://gamma-api.polymarket.com"
CLOB_URL = "https://clob.polymarket.com"

def get_active_events(limit=50, category=None):
    """Fetch active events from Gamma API."""
    params = {
        "closed": "false",
        "limit": limit,
        "order": "volume",
        "ascending": "false"
    }
    if category:
        params["tag"] = category
    
    resp = requests.get(f"{GAMMA_URL}/events", params=params)
    return resp.json() if resp.ok else []

def get_price(token_id):
    """Get current price for a token."""
    try:
        resp = requests.get(f"{CLOB_URL}/price", params={"token_id": token_id})
        if resp.ok:
            return float(resp.json().get("price", 0))
    except:
        pass
    return None

def get_orderbook(token_id):
    """Get orderbook depth."""
    try:
        resp = requests.get(f"{CLOB_URL}/book", params={"token_id": token_id})
        if resp.ok:
            book = resp.json()
            bid_depth = sum(float(b[1]) for b in book.get("bids", [])[:5])
            ask_depth = sum(float(a[1]) for a in book.get("asks", [])[:5])
            return {"bid_depth": bid_depth, "ask_depth": ask_depth}
    except:
        pass
    return {"bid_depth": 0, "ask_depth": 0}

def scan_arbitrage():
    """Find markets where YES + NO < $1.00."""
    print("\n=== ARBITRAGE OPPORTUNITIES ===\n")
    events = get_active_events(limit=100)
    
    for event in events:
        for market in event.get("markets", []):
            tokens = market.get("tokens", [])
            if len(tokens) >= 2:
                yes_price = get_price(tokens[0].get("token_id"))
                no_price = get_price(tokens[1].get("token_id"))
                
                if yes_price and no_price:
                    total = yes_price + no_price
                    if total < 0.99:  # Potential arb
                        profit = (1 - total) * 100
                        print(f"[ARB] {market.get('question', 'Unknown')[:60]}")
                        print(f"      YES: {yes_price:.2f} + NO: {no_price:.2f} = {total:.2f}")
                        print(f"      Potential profit: {profit:.1f}%\n")

def scan_extremes(threshold_low=0.10, threshold_high=0.90):
    """Find markets at extreme prices (potential mean reversion)."""
    print(f"\n=== EXTREME PRICES (<{threshold_low} or >{threshold_high}) ===\n")
    events = get_active_events(limit=100)
    
    for event in events:
        for market in event.get("markets", []):
            tokens = market.get("tokens", [])
            if tokens:
                price = get_price(tokens[0].get("token_id"))
                if price and (price < threshold_low or price > threshold_high):
                    direction = "LOW" if price < threshold_low else "HIGH"
                    print(f"[{direction}] {market.get('question', 'Unknown')[:60]}")
                    print(f"      Price: {price:.2f}\n")

def scan_crypto():
    """Scan crypto-specific markets."""
    print("\n=== CRYPTO MARKETS ===\n")
    events = get_active_events(limit=30, category="crypto")
    
    for event in events:
        print(f"\n{event.get('title', 'Unknown Event')}")
        for market in event.get("markets", []):
            tokens = market.get("tokens", [])
            if tokens:
                price = get_price(tokens[0].get("token_id"))
                book = get_orderbook(tokens[0].get("token_id"))
                if price:
                    print(f"  → {market.get('question', 'Unknown')[:50]}")
                    print(f"    YES: {price:.2f} | Liquidity: ${book['bid_depth']:.0f}/${book['ask_depth']:.0f}")

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    print(f"Polymarket Scanner - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    if mode in ["all", "arb"]:
        scan_arbitrage()
    
    if mode in ["all", "extremes"]:
        scan_extremes()
    
    if mode in ["all", "crypto"]:
        scan_crypto()

if __name__ == "__main__":
    main()
