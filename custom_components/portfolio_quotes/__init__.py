from homeassistant.helpers import discovery
async def async_setup(hass, config):
    await discovery.async_load_platform(hass, "sensor", "portfolio_quotes", config.get("portfolio_quotes", {}), config)
    return True
