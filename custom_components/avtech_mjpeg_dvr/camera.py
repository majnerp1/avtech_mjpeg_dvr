"""AV-TECH test camera."""
from homeassistant.components.camera import Camera

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up camera platform."""
    async_add_entities([AvtechCamera(entry)])


class AvtechCamera(Camera):
    """Simple striped test camera."""

    def __init__(self, entry):
        super().__init__()
        self._entry = entry
        self._attr_name = "AV-TECH Ostré Pruhy"
        self._attr_unique_id = f"{entry.entry_id}_camera"

    async def async_camera_image(self, width=None, height=None):
        """Return fake JPEG image."""
        return (
            b"\xff\xd8"
            + b"\x00" * 64
            + b"\xaa" * 128
            + b"\x55" * 128
            + b"\xff\xd9"
        )

    @property
    def supported_features(self):
        return 0