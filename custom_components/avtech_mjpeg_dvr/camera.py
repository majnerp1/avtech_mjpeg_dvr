"""AV-TECH testovací kamera (pruhovaný obraz)."""

import logging
from homeassistant.components.camera import Camera

_LOGGER = logging.getLogger(__name__)

DOMAIN = "avtech_mjpeg_dvr"


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup camera platform from config entry."""
    async_add_entities([AvtechOstraCamera(config_entry)])


class AvtechOstraCamera(Camera):
    """Jednoduchá testovací kamera s generovaným obrazem."""

    def __init__(self, config_entry):
        """Inicializace."""
        super().__init__()
        self.config_entry = config_entry

        self._attr_name = "AV-TECH Ostré Pruhy"
        self._attr_unique_id = f"{config_entry.entry_id}_ostra_camera"

    async def async_camera_image(self, width=None, height=None):
        """Vrací statický JPEG obraz (test pattern)."""
        return b"".join(
            [
                b"\xff\xd8\xff\xe0\x00\x10JFIF",
                b"\x00" * 64,
                b"\x11\x22\x33\x44" * 32,
                b"\xaa" * 128,
                b"\xff\xd9",
            ]
        )

    @property
    def supported_features(self):
        """Required property in newer HA versions."""
        return 0