# Home Assistant Stock Portfolio Card

Custom Lovelace card for a Grid dashboard, showing price, daily change, volume, optional average cost basis, market value, and optional unrealized gain/loss. No portfolio total.

## Install through HACS

Add this URL as a **Dashboard** custom repository:

https://github.com/rwunderlichsr/ha-stock-portfolio-card

Install **Stock Portfolio Card** and refresh Home Assistant.

**Market data is separate:** The card reads Home Assistant sensor entities; it does not itself fetch stock quotes. The bundled `custom_components/portfolio_quotes` integration must be installed manually (not through the Dashboard HACS installation).

## Quote sensors

Copy `custom_components/portfolio_quotes` into `/config/custom_components/portfolio_quotes`. Add to `configuration.yaml`:

```yaml
portfolio_quotes:
  symbols:
    - SPCX
    - STM
    - GSIT
    - ^IXIC
  scan_interval_minutes: 5
```

Restart Home Assistant. Check Developer Tools → States for the resulting entities. Yahoo Finance may reject or throttle requests. **SPCX is not verified as a valid public SpaceX ticker.** Confirm the ticker independently before relying on it.

## Grid card configuration

Add this entry beneath your existing Grid card's `cards:` list:

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

## Visibility settings

In **Edit dashboard → Edit card → Show code editor**, set:

- `show_cost_basis: true` to show average cost basis; `false` to hide it.
- `show_gain_loss: true` to show a separate dollar gain/loss column; `false` to hide it.

Both are independent. Market value stays visible and is green when price is at/above basis, red when below. Provide actual `shares` and `basis` per holding to calculate market value and gains/losses. Indexes without holdings show dashes.

This repository has not yet been tested on a live Home Assistant instance.
