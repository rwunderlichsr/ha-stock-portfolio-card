from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    symbols = entry.data.get("symbols", [])
    async_add_entities([QuoteSensor(coordinator, symbol) for symbol in symbols])

class QuoteSensor(CoordinatorEntity, SensorEntity):
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "USD"

    def __init__(self, coordinator, symbol):
        super().__init__(coordinator)
        self.symbol = symbol
        self._attr_name = f"Portfolio {symbol}"
        self._attr_unique_id = f"portfolio_{symbol.lower().replace('^', '')}"
        self._attr_icon = "mdi:chart-line"

    @property
    def native_value(self):
        return (self.coordinator.data or {}).get(self.symbol, {}).get("price")

    @property
    def extra_state_attributes(self):
        data = (self.coordinator.data or {}).get(self.symbol, {})
        return {k: v for k, v in data.items() if k != "price" and v is not None}
