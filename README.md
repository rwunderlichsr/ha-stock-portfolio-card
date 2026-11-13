# Home Assistant Stock Portfolio Card

Custom Lovelace card for a Grid dashboard. The aesthetics are unchanged.

The card reads sensor entities created by the **Portfolio Quotes** component included in this repository.

## Install the component (creates the sensors)

### Option A – Marketplace / HACS (recommended)
1. Settings → Marketplace → Custom repositories
2. Add `https://github.com/rwunderlichsr/ha-stock-portfolio-card` as type **Integration**
3. Install **Portfolio Quotes**
4. Restart Home Assistant

### Option B – Manual
Copy the folder `custom_components/portfolio_quotes` into `/config/custom_components/portfolio_quotes` and restart.

## Configure the sensors

Add this to your `configuration.yaml`:

```yaml
portfolio_quotes:
  symbols:
    - SPCX
    - STM
    - GSIT
    - ^IXIC
  scan_interval_minutes: 5
```

Restart Home Assistant. The sensors will appear in Developer Tools → States:

- `sensor.portfolio_spcx`
- `sensor.portfolio_stm`
- `sensor.portfolio_gsit`
- `sensor.portfolio_ixic`

They update automatically at the interval you set.

## Card configuration

Point the existing card at the new sensors (same pattern as before):

```yaml
- type: custom:stock-portfolio-card
  title: My Stocks
  show_cost_basis: true
  show_gain_loss: false
  stocks:
    - name: SpaceX
      ticker: SPCX
      entity: sensor.portfolio_spcx
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

The card itself is already loaded and does not need to be changed.

Yahoo Finance may throttle requests. Confirm tickers (especially SPCX) independently.
