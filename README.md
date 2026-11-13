# Home Assistant Stock Portfolio Card

Custom Lovelace card for a Grid dashboard.

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

## Install or update the dashboard card in HACS

For a first-time install, open **HACS → ⋮ → Custom repositories**, add
`https://github.com/rwunderlichsr/ha-stock-portfolio-card` as **Dashboard**,
then open **Stock Portfolio Card** and select **Download**.

For an existing HACS dashboard-card install, use **Update information** in
the card's HACS menu, then **Redownload** from the default branch. Reload the
dashboard. If the old column is still visible, hard-refresh the browser.

A repository entry of type **Integration** installs Portfolio Quotes sensors.
For a manually installed card, replace the JavaScript file used by its
dashboard resource, or point that resource to
`/hacsfiles/ha-stock-portfolio-card/stock-portfolio-card.js` after installing
the Dashboard entry through HACS. Keep only one resource for the card.

## Card configuration

Point the existing card at the new sensors (same pattern as before):

```yaml
- type: custom:stock-portfolio-card
  title: My Stocks
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

Existing card YAML still works. Keep each holding’s `shares` and `basis` for
Market Value, gain/loss, and value coloring. The card omits the Avg basis
column even if older YAML contains `show_cost_basis`.

Yahoo Finance may throttle requests. Confirm tickers (especially SPCX) independently.
