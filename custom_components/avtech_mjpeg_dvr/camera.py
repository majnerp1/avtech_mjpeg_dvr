import logging
import asyncio
from homeassistant.components.camera import Camera

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Nastavení kamery z bezpečného grafického úložiště HA (Config Entry)."""
    config = config_entry.data
    
    ip = config.get("ip")
    port = config.get("port")
    username = config.get("username")
    password = config.get("password")

    async_add_entities([AvtechPureMjpegCamera(ip, port, username, password)])

class AvtechPureMjpegCamera(Camera):
    """Univerzální integrace pro AV-TECH MJPEG DVR přes čisté TCP sockety."""

    def __init__(self, ip, port, username, password):
        """Inicializace."""
        super().__init__()
        self._attr_name = "AV-TECH MJPEG DVR"
        self._ip = ip
        self._port = int(port)
        self._username = username
        self._password = password

    @property
    def name(self):
        return self._attr_name

    async def _get_new_session_id(self):
        """Vytvoří nové přihlášení a vrátí čerstvé Session ID."""
        try:
            reader, writer = await asyncio.open_connection(self._ip, self._port)
            
            in_data = f"GET /Login.cgi?Username={self._username}&Password={self._password} HTTP/1.1\r\n"
            in_data += f"Host: {self._ip}\r\n"
            in_data += "Connection: Keep-Alive\r\n\r\n"
            
            writer.write(in_data.encode('utf-8'))
            await writer.drain()
            
            raw_response = b""
            while True:
                try:
                    chunk = await asyncio.wait_for(reader.read(1024), timeout=1.0)
                    if not chunk:
                        break
                    raw_response += chunk
                except asyncio.TimeoutError:
                    break
                    
            writer.close()
            await writer.wait_closed()
            
            odpoved = raw_response.decode('utf-8', errors='ignore')
            if "Session-ID=" in odpoved:
                start = odpoved.find("Session-ID=") + len("Session-ID=")
                end = odpoved.find(";F", start)
                if end == -1:
                    end = odpoved.find(";", start)
                if end != -1 and end > start:
                    return odpoved[start:end]
            return None
        except Exception:
            return None

    async def _send_setup_commands(self, session_id):
        """Odeslání inicializačních příkazů pro aktivaci videa."""
        for cmd in [f"Setresolution.cgi?Cookie={session_id}&RES=1", f"Setquality.cgi?Cookie={session_id}&QUA=0"]:
            try:
                reader, writer = await asyncio.open_connection(self._ip, self._port)
                in_data = f"GET /{cmd} HTTP/1.1\r\nHost: {self._ip}\r\nConnection: Close\r\n\r\n"
                writer.write(in_data.encode('utf-8'))
                await writer.drain()
                await asyncio.wait_for(reader.read(1024), timeout=1.0)
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass

    async def async_camera_image(self, width: int | None = None, height: int | None = None) -> bytes | None:
        """STATICKÝ SNÍMEK: Rychlé nasátí jednoho snímku pro náhled na ploše."""
        session_id = await self._get_new_session_id()
        if not session_id:
            return None
            
        await self._send_setup_commands(session_id)
        
        try:
            reader, writer = await asyncio.open_connection(self._ip, self._port)
            in_data = f"GET /Getvideo.cgi?Cookie={session_id} HTTP/1.1\r\nHost: {self._ip}\r\nConnection: Close\r\n\r\n"
            writer.write(in_data.encode('utf-8'))
            await writer.drain()
            
            buffer = b""
            while True:
                try:
                    chunk = await asyncio.wait_for(reader.read(4096), timeout=2.0)
                    if not chunk:
                        break
                    buffer += chunk
                    
                    start_idx = buffer.find(b"\xff\xd8")
                    end_idx = buffer.find(b"\xff\xd9")
                    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                        writer.close()
                        await writer.wait_closed()
                        return buffer[start_idx:end_idx + 2]
                except asyncio.TimeoutError:
                    break
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass
        return None

    async def handle_async_mjpeg_stream(self, request):
        """ŽIVÝ STREAM: Přemostění toku z DVR obohacené o MJPEG hlavičky pro HA."""
        session_id = await self._get_new_session_id()
        if not session_id:
            return None
            
        await self._send_setup_commands(session_id)

        from aiohttp import web
        response = web.StreamResponse()
        
        boundary = "mjpeg_boundary_chata"
        response.content_type = f"multipart/x-mixed-replace; boundary={boundary}"
        await response.prepare(request)

        try:
            reader, writer = await asyncio.open_connection(self._ip, self._port)
            in_data = f"GET /Getvideo.cgi?Cookie={session_id} HTTP/1.1\r\nHost: {self._ip}\r\nConnection: Keep-Alive\r\n\r\n"
            writer.write(in_data.encode('utf-8'))
            await writer.drain()

            await response.write(f"\r\n--{boundary}\r\n".encode('utf-8'))

            while True:
                chunk = await reader.read(65536)
                if not chunk:
                    break
                
                if b"\xff\xd8" in chunk:
                    parts = chunk.split(b"\xff\xd8", 1)
                    mjpeg_header = f"\r\nContent-Type: image/jpeg\r\n\r\n".encode('utf-8')
                    chunk = parts + f"\r\n--{boundary}".encode('utf-8') + mjpeg_header + b"\xff\xd8" + parts

                await response.write(chunk)
                
        except Exception as e:
            _LOGGER.debug("AV-TECH Živý stream přerušen: %s", e)
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass

        return response