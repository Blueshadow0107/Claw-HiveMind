# Polymarket Trading Strategies

## 1. Sum-to-One Arbitrage

**Concept:** When YES + NO prices sum to less than $1.00, buy both for risk-free profit.

**Example:**
- YES price: 48¢
- NO price: 50¢
- Total: 98¢
- Guaranteed profit: 2¢ per share (2% return)

**Execution:**
1. Monitor markets for sum < $0.99 (accounting for fees)
2. Use Fill-or-Kill (FOK) orders for atomic execution
3. Size to 1-5% of available liquidity
4. Add $0.01 premium to ensure fills

**Requirements:**
- Sub-150ms latency for competitive arb
- WebSocket connection for real-time prices
- Sufficient capital for meaningful returns

## 2. Momentum Trading

**Concept:** Follow price trends with volume confirmation.

**Signals:**
- Price breaks key level (round numbers, previous highs/lows)
- Volume spike (2x+ average)
- Orderbook imbalance (3:1 bid/ask ratio)

**Entry:**
- Wait for pullback to broken level
- Confirm with continued volume
- Enter with stop below breakout point

**Exit:**
- Scale out at 20%, 50%, 80% targets
- Trail stop as price advances
- Full exit on volume exhaustion

## 3. Contrarian/Mean Reversion

**Concept:** Fade extreme moves expecting reversion.

**Triggers:**
- >20% price move in 24h without fundamental change
- Extreme sentiment (Twitter/news hysteria)
- Price hits psychological extremes (<10¢ or >90¢)

**Entry:**
- Fade the move after initial exhaustion
- Scale in (25% → 50% → 25%)
- Wider stops (expect volatility)

**Exit:**
- Target 50% retracement of extreme move
- Time-based exit if no reversion in 48-72h

## 4. Event-Driven Trading

**Concept:** Position before known catalysts.

**Catalyst types:**
- Scheduled events (earnings, Fed meetings, elections)
- Expected announcements (product launches, rulings)
- Recurring patterns (monthly data releases)

**Playbook:**
1. Identify catalyst date
2. Assess market's current pricing vs your expectation
3. Enter 24-72h before catalyst
4. Set profit target and stop before event
5. Exit before or immediately after resolution

**Risk:** Binary outcomes can move 50%+ instantly.

## 5. AI Consensus Trading

**Concept:** Query multiple AI models, trade only on consensus.

**Process:**
1. Identify market with unclear odds
2. Query 3+ AI models for probability assessment
3. If consensus emerges (all within 10% of each other):
   - Compare consensus to market price
   - Trade if >15% edge exists
4. If no consensus: skip

**Models to query:**
- Claude
- GPT-4
- Gemini
- Perplexity (with web search)

**Edge:** Aggregated AI assessment often beats individual retail traders.

## 6. Liquidity Provision (Market Making)

**Concept:** Provide bid/ask quotes, earn the spread.

**Setup:**
1. Select high-volume market
2. Place bid at -3% from mid, ask at +3%
3. Manage inventory (don't get too directional)
4. Widen spreads in volatility

**Risks:**
- Adverse selection (informed traders pick you off)
- Inventory risk (stuck with losing position)
- Event risk (binary moves wipe spread profits)

**Capital requirement:** Higher than directional trading.

## Strategy Selection Matrix

| Strategy | Capital Needed | Time Commitment | Edge Source | Risk |
|----------|---------------|-----------------|-------------|------|
| Arbitrage | High | 24/7 automated | Speed | Low |
| Momentum | Medium | Active monitoring | Trend reading | Medium |
| Contrarian | Medium | Daily check | Sentiment analysis | High |
| Event-driven | Low-Medium | Catalyst timing | Information | High |
| AI Consensus | Low | Per-trade | Model aggregation | Medium |
| Market Making | High | 24/7 automated | Spread capture | Medium |

## Starting Recommendations

For a new trader:
1. Start with **Event-driven** (lowest capital, clear catalysts)
2. Add **AI Consensus** (leverages your capabilities)
3. Graduate to **Momentum** as you learn market dynamics
4. Avoid **Arbitrage** and **Market Making** until automated infrastructure exists
