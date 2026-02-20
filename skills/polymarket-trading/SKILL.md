---
name: polymarket-trading
description: Trade on Polymarket prediction markets. Use for scanning markets, analyzing odds, placing trades, and managing positions. Covers crypto, politics, sports, AI, and current events. Strategies include arbitrage, momentum, and AI consensus trading.
---

# Polymarket Trading

Autonomous prediction market trading on Polymarket.

## Quick Start

1. **Scan markets** → Find opportunities
2. **Analyze odds** → Compare to your assessment
3. **Place trades** → Execute via API or browser
4. **Monitor positions** → Track P&L and exits

## API Endpoints

| API | URL | Purpose |
|-----|-----|---------|
| Gamma | `https://gamma-api.polymarket.com` | Market discovery |
| CLOB | `https://clob.polymarket.com` | Prices, orderbooks, trading |
| Data | `https://data-api.polymarket.com` | Positions, history |
| WebSocket | `wss://ws-subscriptions-clob.polymarket.com` | Real-time updates |

## Core Workflows

### Scan for Opportunities

```bash
# Get active markets
curl "https://gamma-api.polymarket.com/events?closed=false&limit=50"

# Get specific market price
curl "https://clob.polymarket.com/price?token_id=<TOKEN_ID>"

# Get orderbook depth
curl "https://clob.polymarket.com/book?token_id=<TOKEN_ID>"
```

### Analyze a Market

1. Fetch current YES/NO prices from CLOB
2. Compare to your probability assessment
3. Check liquidity depth (can you get in/out?)
4. Look for edge: your assessment vs market price

**Edge calculation:** If you think YES is 70% likely but market prices it at 55¢, you have +15% edge.

### Trading Strategies

See `references/strategies.md` for detailed playbooks:
- **Arbitrage** — Buy YES+NO when sum < $1.00
- **Momentum** — Follow price trends with volume confirmation
- **Contrarian** — Fade extreme moves (>20% in 24h)
- **Event-driven** — Position before known catalysts

### Execution

**Via Browser (manual):**
1. Navigate to market on polymarket.com
2. Connect wallet / login
3. Place limit or market order

**Via API (programmatic):**
Requires approved API keys. See `references/api-reference.md`.

## Risk Management

- **Position sizing:** Max 5% of bankroll per market
- **Correlation:** Don't stack similar bets
- **Liquidity:** Ensure exit path before entry
- **Time decay:** Markets can stay wrong longer than you can stay solvent

## Market Categories

| Category | Volatility | Edge Source |
|----------|-----------|-------------|
| Crypto prices | High | Technical analysis, on-chain data |
| Politics | Medium | Polling, news flow |
| AI/Tech | Medium | Industry knowledge |
| Sports | Low | Stats, models |
| Current events | Variable | Information speed |

## Position Monitoring

Track via Data API:
```bash
curl "https://data-api.polymarket.com/positions?user=<WALLET_ADDRESS>"
```

## When to Trade

**Good setups:**
- Clear edge (>10% vs market)
- Sufficient liquidity
- Known catalyst timing
- Asymmetric risk/reward

**Avoid:**
- Low liquidity markets
- Ambiguous resolution criteria
- Markets near expiry with unclear outcome
