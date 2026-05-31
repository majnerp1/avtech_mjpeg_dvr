"""Inicializace integrace AV-TECH MJPEG DVR."""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)

DOMAIN = "avtech_mjpeg_dvr"
PLATFORMS: list[str] = ["camera"]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """
    Starý entry point – musí existovat, jinak se integrace někdy nenačte správně.
    U config_flow integrací se většinou jen vrací True.
    """
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Nastavení integrace z UI (config flow)."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Odebrání integrace."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)