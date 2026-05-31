"""Triviální config flow pro testovací pruhovanou kameru."""
import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "avtech_mjpeg_dvr"

class AvtechTrivialConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Triviální grafické nastavení."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Zobrazení jednoduchého formuláře."""
        if user_input is not None:
            return self.async_create_entry(title="AV-TECH Pruhy Test", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required("ip", default="192.168.2.10"): str})
        )
