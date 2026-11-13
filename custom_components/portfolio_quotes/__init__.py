from datetime import timedelta
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .const import DOMAIN, CONF_SYMBOLS, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
import yfinance as yf

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

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    await _async_setup_coordinator(hass, entry)
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def _async_setup_coordinator(hass: HomeAssistant, entry: ConfigEntry):
    data = entry.options or entry.data
    symbols = data.get(CONF_SYMBOLS, [])
    minutes = max(1, int(data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)))

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
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
