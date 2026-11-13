import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_SYMBOLS, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL

class PortfolioQuotesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            symbols = [s.strip().upper() for s in user_input[CONF_SYMBOLS].split(",") if s.strip()]
            if not symbols:
                errors["base"] = "no_symbols"
            else:
                await self.async_set_unique_id(",".join(sorted(symbols)))
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title="Portfolio Quotes",
                    data={
                        CONF_SYMBOLS: symbols,
                        CONF_SCAN_INTERVAL: user_input.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_SYMBOLS, default="SPCX,STM,GSIT,^IXIC"): str,
                vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(vol.Coerce(int), vol.Range(min=1, max=60)),
            }),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return PortfolioQuotesOptionsFlow(config_entry)

class PortfolioQuotesOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            symbols = [s.strip().upper() for s in user_input[CONF_SYMBOLS].split(",") if s.strip()]
            return self.async_create_entry(
                title="",
                data={
                    CONF_SYMBOLS: symbols,
                    CONF_SCAN_INTERVAL: user_input.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
                },
            )

        current = self.config_entry.options or self.config_entry.data
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_SYMBOLS, default=",".join(current.get(CONF_SYMBOLS, []))): str,
                vol.Optional(CONF_SCAN_INTERVAL, default=current.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)): vol.All(vol.Coerce(int), vol.Range(min=1, max=60)),
            }),
        )
