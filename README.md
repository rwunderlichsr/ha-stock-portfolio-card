# Home Assistant Stock Portfolio Card

Custom Lovelace card for a Grid dashboard, showing price, daily change, volume, optional average cost basis, market value, and optional unrealized gain/loss. No portfolio total.

The card reads sensor entities created by the **Portfolio Quotes** integration (included in this repo). The aesthetics of the card are unchanged.

## Install

### 1. Portfolio Quotes integration (creates the sensors)

**Recommended (HACS):**
1. In HACS → Integrations → three-dot menu → Custom repositories
2. Add `https://github.com/rwunderlichsr/ha-stock-portfolio-card` as type **Integration**
3. Install **Portfolio Quotes**
4. Restart Home Assistant
5. Go to **Settings → Devices & Services → Add Integration**
6. Search for **Portfolio Quotes**
7. Enter your symbols as a comma-separated list (example: `SPCX,STM,GSIT,^IXIC`) and optional scan interval (minutes)
8. The sensors (`sensor.portfolio_spcx`, etc.) will appear and update automatically

**Manual:**
Copy `custom_components/portfolio_quotes` into `/config/custom_components/portfolio_quotes`, restart, then add the integration via the UI as above.

### 2. Stock Portfolio Card (Lovelace)

In HACS → Frontend / Dashboard → Custom repositories, add the same URL as type **Dashboard**.

Install **Stock Portfolio Card** and refresh.

## Card configuration

```yaml
- type: custom:stock-portfolio-card
  title: My Stocks
  show_cost_basis: true
  show_gain_loss: false
  stocks:
    - name: SpaceX
      ticker: SPCX
      entity: sensor.portfolio_spcx
      # shares: 100
      # basis: 120
    - name: STMicroelectronics
      ticker: STM
      entity: sensor.portfolio_stm
    - name: GSI Technology
      ticker: GSIT
      entity: sensor.portfolio_gsit
    - name: NASDAQ Composite
      ticker: ^IXIC
      entity: sensor.portfolio_ixic
```

Entity IDs follow the pattern `sensor.portfolio_<symbol>` (caret removed for indexes).

## Visibility settings

- `show_cost_basis: true/false`
- `show_gain_loss: true/false`

Provide `shares` and `basis` per holding when you want market value and gain/loss. Indexes without holdings show dashes.

Yahoo Finance may throttle or reject some requests. Confirm tickers (especially SPCX) independently.
