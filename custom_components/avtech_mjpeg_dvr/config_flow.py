import voluptuous as vol
from homeassistant import config_entries

DOMAIN = "avtech_mjpeg_dvr"

class AvtechDVRConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Grafické nastavení pro AV-TECH MJPEG DVR."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Zobrazení formuláře uživateli v rozhraní HA."""
        errors = {}

        if user_input is not None:
            await self.async_set_unique_id(f"avtech_{user_input['ip']}_{user_input['port']}")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"AV-TECH DVR ({user_input['ip']})", 
                data=user_input
            )

        DATA_SCHEMA = vol.Schema(
            {
                vol.Required("ip", default="192.168.1.20"): str,
                vol.Required("port", default=8888): int,
                vol.Required("username", default="admin"): str,
                vol.Required("password"): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
