"""Config flow for AV-TECH MJPEG DVR."""
import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN


class AvtechConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Simple config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """User setup step."""
        if user_input is not None:
            return self.async_create_entry(
                title="AV-TECH MJPEG DVR",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("ip", default="192.168.1.10"): str,
                }
            ),
        )