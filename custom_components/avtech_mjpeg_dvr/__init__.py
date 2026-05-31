"""AV-TECH MJPEG DVR integration."""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["camera"]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Initialize integration."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from config flow."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload integration."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)