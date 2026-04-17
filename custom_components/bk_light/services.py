"""Services for BK Light ACT1026 integration."""
from __future__ import annotations

import logging
from typing import Final

from bleak import BleakScanner
from PIL import Image, ImageDraw, ImageFont
import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import DISPLAY_HEIGHT, DISPLAY_WIDTH, DOMAIN

_LOGGER = logging.getLogger(__name__)

SERVICE_SCAN_DEVICES: Final = "scan_devices"
SERVICE_DISPLAY_TEXT: Final = "display_text"

SERVICE_SCAN_DEVICES_SCHEMA = vol.Schema({})

SERVICE_DISPLAY_TEXT_SCHEMA = vol.Schema(
    {
        vol.Required("entity_id"): cv.entity_id,
        vol.Required("text"): cv.string,
        vol.Optional("color", default=[255, 0, 0]): vol.All(
            list, vol.Length(min=3, max=3)
        ),
        vol.Optional("background", default=[0, 0, 0]): vol.All(
            list, vol.Length(min=3, max=3)
        ),
        vol.Optional("font_size", default=8): vol.Coerce(int),
    }
)


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for BK Light integration."""

    async def handle_scan_devices(call: ServiceCall) -> None:
        """Handle the scan_devices service call."""
        _LOGGER.info("=" * 60)
        _LOGGER.info("BK Light Device Scanner")
        _LOGGER.info("=" * 60)
        _LOGGER.info("Scanning for BLE devices (15 seconds)...")

        try:
            devices = await BleakScanner.discover(timeout=15.0)

            _LOGGER.info("Scan complete. Found %d BLE devices total.", len(devices))
            _LOGGER.info("-" * 60)

            led_devices = [
                d
                for d in devices
                if d.name
                and (
                    d.name.startswith("LED_BLE_")
                    or d.name.startswith("BK_LIGHT")
                    or d.name.startswith("BJ_LED")
                )
            ]

            if led_devices:
                _LOGGER.info("Found %d BK Light device(s):", len(led_devices))
                _LOGGER.info("-" * 60)
                for device in led_devices:
                    rssi = getattr(device, "rssi", None)
                    signal_strength = (
                        "Excellent" if rssi and rssi > -60 else
                        "Good" if rssi and rssi > -75 else
                        "Fair" if rssi and rssi > -85 else
                        "Weak"
                    )

                    _LOGGER.info("  Device Name:    %s", device.name)
                    _LOGGER.info("  MAC Address:    %s", device.address)
                    if rssi:
                        _LOGGER.info("  Signal (RSSI):  %d dBm (%s)", rssi, signal_strength)
                    _LOGGER.info("  " + "-" * 56)
            else:
                _LOGGER.warning("No BK Light devices found")
                _LOGGER.warning("Expected device names: LED_BLE_*, BK_LIGHT*, BJ_LED*")
                _LOGGER.warning("Troubleshooting:")
                _LOGGER.warning("  1. Make sure the display is powered on")
                _LOGGER.warning("  2. Check the device is within 10 meters")
                _LOGGER.warning("  3. Disconnect from mobile app if connected")
                _LOGGER.warning("  4. Try power cycling the display")

            _LOGGER.info("")
            _LOGGER.info("All BLE devices found:")
            _LOGGER.info("-" * 60)
            for device in sorted(devices, key=lambda d: getattr(d, "rssi", -100), reverse=True):
                name = device.name or "<Unnamed>"
                rssi = getattr(device, "rssi", None)
                rssi_str = f"{rssi} dBm" if rssi else "N/A"
                _LOGGER.info("  %-30s %s  (RSSI: %s)", name[:30], device.address, rssi_str)

            _LOGGER.info("=" * 60)
            _LOGGER.info("Scan complete. Check the information above.")
            _LOGGER.info("=" * 60)

        except Exception as err:
            _LOGGER.error("=" * 60)
            _LOGGER.error("Error scanning for devices: %s", err)
            _LOGGER.error("This may indicate a Bluetooth adapter issue.")
            _LOGGER.error("=" * 60)

    async def handle_display_text(call: ServiceCall) -> None:
        """Handle the display_text service call."""
        entity_id = call.data["entity_id"]
        text = call.data["text"]
        color = tuple(call.data.get("color", [255, 0, 0]))
        background = tuple(call.data.get("background", [0, 0, 0]))
        font_size = call.data.get("font_size", 8)

        object_id = entity_id.split(".", 1)[1]

        if DOMAIN not in hass.data:
            raise ValueError("BK Light domain not initialized")

        matched_device = None

        for _entry_id, device in hass.data[DOMAIN].items():
            if object_id.endswith("display"):
                matched_device = device
                break

        if matched_device is None:
            if len(hass.data[DOMAIN]) == 1:
                matched_device = next(iter(hass.data[DOMAIN].values()))
            else:
                raise ValueError(f"No BK Light device found for entity_id {entity_id}")

        image = Image.new("RGB", (DISPLAY_WIDTH, DISPLAY_HEIGHT), color=background)
        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size
            )
        except Exception:
            font = ImageFont.load_default()

        lines = text.splitlines() or [text]
        bboxes = [draw.textbbox((0, 0), line, font=font) for line in lines]
        line_heights = [bbox[3] - bbox[1] for bbox in bboxes]
        total_height = sum(line_heights)
        y = (DISPLAY_HEIGHT - total_height) // 2

        for line, bbox, line_height in zip(lines, bboxes, line_heights):
            text_width = bbox[2] - bbox[0]
            x = (DISPLAY_WIDTH - text_width) // 2
            draw.text((x, y), line, fill=color, font=font)
            y += line_height

        success = await matched_device.send_image(image)
        if not success:
            raise ValueError("Failed to send text to BK Light display")

    if not hass.services.has_service(DOMAIN, SERVICE_SCAN_DEVICES):
        hass.services.async_register(
            DOMAIN,
            SERVICE_SCAN_DEVICES,
            handle_scan_devices,
            schema=SERVICE_SCAN_DEVICES_SCHEMA,
        )

    if not hass.services.has_service(DOMAIN, SERVICE_DISPLAY_TEXT):
        hass.services.async_register(
            DOMAIN,
            SERVICE_DISPLAY_TEXT,
            handle_display_text,
            schema=SERVICE_DISPLAY_TEXT_SCHEMA,
        )
