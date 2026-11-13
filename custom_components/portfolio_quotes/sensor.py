from datetime import timedelta
import logging
import yfinance as yf
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
_LOGGER = logging.getLogger(__name__)
def fetch(symbols):
    data = {}
    for symbol in symbols:
        try:
            info = yf.Ticker(symbol).info or {}
            price = info.get("regularMarketPrice")
            previous = info.get("regularMarketPreviousClose")
            data[symbol] = {"price": price, "regularMarketChangePercent": (price-previous)/previous*100 if price is not None and previous else None, "regularMarketVolume": info.get("regularMarketVolume")}
        except Exception as exc:
            _LOGGER.warning("Quote failed for %s: %s", symbol, exc)
            data[symbol] = {"price": None, "error": str(exc)}
    return data
async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    opts = discovery_info or config
    symbols = opts.get("symbols", ["SPCX","STM","GSIT","^IXIC"])
    minutes = max(1,int(opts.get("scan_interval_minutes",5)))
    coordinator = DataUpdateCoordinator(hass,_LOGGER,name="Portfolio Quotes",update_method=lambda: hass.async_add_executor_job(fetch,symbols),update_interval=timedelta(minutes=minutes))
    await coordinator.async_refresh()
    async_add_entities([Quote(coordinator,s) for s in symbols])
class Quote(CoordinatorEntity,SensorEntity):
    def __init__(self, coordinator, symbol):
        super().__init__(coordinator)
        self.symbol=symbol
        self._attr_name="Portfolio "+symbol
        self._attr_unique_id="portfolio_"+symbol.lower().replace("^","")
        self.entity_id="sensor.portfolio_"+symbol.lower().replace("^","")
    @property
    def native_value(self):
        return (self.coordinator.data or {}).get(self.symbol,{}).get("price")
    @property
    def extra_state_attributes(self):
        return {k:v for k,v in (self.coordinator.data or {}).get(self.symbol,{}).items() if k!="price"}
