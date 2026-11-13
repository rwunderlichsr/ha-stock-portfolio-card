from homeassistant.helpers import discovery
from .const import DOMAIN

async def async_setup(hass, config):
    """Set up the Portfolio Quotes component."""
    conf = config.get(DOMAIN, {})
    if not conf:
        return True
    hass.async_create_task(
        discovery.async_load_platform(hass, "sensor", DOMAIN, conf, config)
    )
    return True
