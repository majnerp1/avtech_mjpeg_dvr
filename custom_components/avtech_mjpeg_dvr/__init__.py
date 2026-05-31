"""Inicializace integrace AV-TECH MJPEG DVR přes Config Flow."""
import logging

_LOGGER = logging.getLogger(__name__)
DOMAIN = "avtech_mjpeg_dvr"
PLATFORMS = ["camera"]

async def async_setup_entry(hass, entry):
    """Nastavení integrace z grafického rozhraní."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass, entry):
    """Odebrání integrace ze systému."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
