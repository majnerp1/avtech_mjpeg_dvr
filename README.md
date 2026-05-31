# AV-TECH MJPEG DVR pro Home Assistant

Tato vlastní (custom) integrace umožňuje připojení a zobrazení živého MJPEG streamu a statických náhledů z kamerových rekordérů AV-TECH do Home Assistantu přes čisté TCP sockety.

## Hlavní vlastnosti
* **Config Flow:** Plně grafické nastavení přímo v rozhraní Home Assistant (není nutný zápis do `configuration.yaml`).
* **Asynchronní provoz:** Používá neblokující síťovou komunikaci pro plynulý chod HA.
* **Živý MJPEG Stream:** Přemostění nativního videa z DVR včetně správného doplňování HTTP hlaviček.

## Požadavky na nastavení
Při přidávání integrace budete požádáni o zadání následujících údajů:


| Parametr | Výchozí hodnota | Popis |
| :--- | :--- | :--- |
| **IP Adresa** | `192.168.1.20` | Síťová IP adresa vašeho AV-TECH DVR rekordéru. |
| **Port** | `8888` | Síťový port pro komunikaci (ověřte v nastavení DVR). |
| **Uživatelské jméno** | `admin` | Přihlašovací jméno s právy pro zobrazení streamu. |
| **Heslo** | *(prázdné)* | Přihlašovací heslo k uvedenému uživateli. |

## Ruční instalace přes HACS
1. Otevřete rozhraní **HACS** v Home Assistant.
2. Vpravo nahoře klikněte na tři tečky a zvolte **Vlastní repozitáře** (Custom repositories).
3. Vložte URL adresu tohoto repozitáře z vaší lokální Gitea.
4. Zvolte typ **Integrace** a klikněte na **Přidat**.
5. Vyhledejte integraci v HACS, klikněte na **Stáhnout** a následně **restartujte Home Assistant**.

## Aktivace zařízení
Po restartu přejděte do **Nastavení** -> **Zařízení a služby** -> **Přidat integraci** a vyhledejte `AV-TECH MJPEG DVR`. Vyplňte formulář a kamera se automaticky přidá do systému.
