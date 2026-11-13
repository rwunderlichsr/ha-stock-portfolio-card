from datetime import timedelta
import logging
import yfinance as yf
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from .const import DOMAIN, CONF_SYMBOLS, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

def fetch(symbols):
    data = {}
    for symbol in symbols:
        try:
            info = yf.Ticker(symbol).info or {}
            price = info.get("regularMarketPrice")
            previous = info.get("regularMarketPreviousClose")
            change_pct = None
            if price is not None and previous:
                change_pct = (price - previous) / previous * 100
            data[symbol] = {
                "price": price,
                "regularMarketChangePercent": change_pct,
                "regularMarketVolume": info.get("regularMarketVolume"),
                "currency": info.get("currency"),
                "shortName": info.get("shortName") or info.get("longName"),
            }
        except Exception as exc:
            _LOGGER.warning("Quote failed for %s: %s", symbol, exc)
            data[symbol] = {"price": None, "error": str(exc)}
    return data

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform."""
    conf = discovery_info or config
    symbols = conf.get(CONF_SYMBOLS, ["SPCX", "STM", "GSIT", "^IXIC"])
    minutes = max(1, int(conf.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)))

    async def async_update_data():
        return await hass.async_add_executor_job(fetch, symbols)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Portfolio Quotes",
        update_method=async_update_data,
        update_interval=timedelta(minutes=minutes),
    )
    await coordinator.async_refresh()

    async_add_entities([QuoteSensor(coordinator, s) for s in symbols])

class QuoteSensor(CoordinatorEntity, SensorEntity):
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "USD"
    _attr_icon = "mdi:chart-line"

    def __init__(self, coordinator, symbol):
        super().__init__(coordinator)
        self.symbol = symbol
        self._attr_name = f"Portfolio {symbol}"
        self._attr_unique_id = f"portfolio_{symbol.lower().replace('^', '')}"

    @property
    def native_value(self):
        return (self.coordinator.data or {}).get(self.symbol, {}).get("price")

    @property
    def extra_state_attributes(self):
        data = (self.coordinator.data or {}).get(self.symbol, {})
        return {k: v for k, v in data.items() if k != "price" and v is not None}
