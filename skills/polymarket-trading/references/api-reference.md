# Polymarket API Reference

## Authentication

**Read-only access:** Public, no auth required
**Trading access:** Requires approved API keys (apply via docs.polymarket.com)

## Gamma API — Market Discovery

Base URL: `https://gamma-api.polymarket.com`

### Get Active Events
```
GET /events?closed=false&limit=100&order=volume
```

Response includes:
- `id` — Event ID
- `slug` — URL-friendly name
- `title` — Human-readable title
- `markets` — Array of market objects
- `startDate`, `endDate` — Event timing

### Get Specific Event
```
GET /events/{event_id}
```

### Get Markets
```
GET /markets?closed=false
```

### Filter by Category
```
GET /events?tag=crypto
GET /events?tag=politics
GET /events?tag=sports
```

## CLOB API — Trading

Base URL: `https://clob.polymarket.com`

### Get Price
```
GET /price?token_id={TOKEN_ID}
```

Response:
```json
{
  "price": "0.55",
  "token_id": "..."
}
```

### Get Midpoint
```
GET /midpoint?token_id={TOKEN_ID}
```

### Get Orderbook
```
GET /book?token_id={TOKEN_ID}
```

Response:
```json
{
  "bids": [[price, size], ...],
  "asks": [[price, size], ...],
  "timestamp": 1706900000
}
```

### Place Order (Authenticated)
```
POST /order
Authorization: Bearer {API_KEY}

{
  "token_id": "...",
  "side": "buy",  // or "sell"
  "size": 100,
  "price": "0.54",
  "type": "limit"  // or "market"
}
```

### Cancel Order
```
DELETE /order/{order_id}
Authorization: Bearer {API_KEY}
```

### Get Order Status
```
GET /order/{order_id}
Authorization: Bearer {API_KEY}
```

## Data API — Portfolio

Base URL: `https://data-api.polymarket.com`

### Get Positions
```
GET /positions?user={WALLET_ADDRESS}
GET /positions?user={WALLET_ADDRESS}&market={CONDITION_ID}
```

### Get Trade History
```
GET /trades?user={WALLET_ADDRESS}&limit=50
```

### Get Activity
```
GET /activity?user={WALLET_ADDRESS}
```

## WebSocket — Real-Time

URL: `wss://ws-subscriptions-clob.polymarket.com/ws/`

### Subscribe to Price Updates
```json
{
  "type": "subscribe",
  "channel": "price",
  "token_id": "..."
}
```

### Subscribe to Orderbook
```json
{
  "type": "subscribe", 
  "channel": "book",
  "token_id": "..."
}
```

## Common Token IDs

To find token IDs:
1. Get market from Gamma API
2. Extract `tokens` array from market object
3. Each token has `token_id` (YES outcome) and complement (NO outcome)

## Rate Limits

- Gamma API: 100 req/min
- CLOB API: 300 req/min (read), 60 req/min (write)
- Data API: 100 req/min

## Error Handling

| Code | Meaning |
|------|---------|
| 400 | Bad request (check params) |
| 401 | Unauthorized (need API key) |
| 429 | Rate limited |
| 500 | Server error (retry) |

## Example: Full Market Scan

```python
import requests

GAMMA = "https://gamma-api.polymarket.com"
CLOB = "https://clob.polymarket.com"

# 1. Get active events
events = requests.get(f"{GAMMA}/events?closed=false&limit=20").json()

for event in events:
    for market in event.get('markets', []):
        token_id = market['tokens'][0]['token_id']
        
        # 2. Get current price
        price = requests.get(f"{CLOB}/price?token_id={token_id}").json()
        
        # 3. Get orderbook depth
        book = requests.get(f"{CLOB}/book?token_id={token_id}").json()
        
        print(f"{market['question']}: {price['price']} (depth: {len(book['bids'])} bids)")
```
