# ha-action-32x32-led

Home Assistant integration and setup notes for the ACTION / BK Light 32x32 LED panel.

## Included in this repository

- patched custom integration for `BK Light ACT1026`
- pixel-font based line rendering for 32x32 displays
- fixed row placement using `y_line`
- examples for multi-page automations
- Bluetooth gateway setup guide for Home Assistant

## Features

- BLE connection to the LED panel
- patched image transfer handling
- 3x5 pixel font rendering optimized for 32x32
- horizontal centering for every line
- multi-line display service: `bk_light.display_lines`

## Installation

1. Copy `custom_components/bk_light` into your Home Assistant configuration directory.
2. Restart Home Assistant.
3. Add the integration.
4. Make sure BLE connectivity is stable.
5. For best results, use an ESP32 Bluetooth gateway.

## Services

### `bk_light.scan_devices`

Scans nearby BLE devices and logs possible BK Light panels.

### `bk_light.display_text`

Displays one or more lines starting at a fixed row or centered automatically.

### `bk_light.display_lines`

Displays multiple individually positioned lines.

Example:

```yaml
action: bk_light.display_lines
data:
  entity_id: image.my_led_display
  background: [0, 0, 0]
  lines:
    - text: "18:42"
      y_line: 5
      font_size: 1
      color: [0, 255, 0]
    - text: "14.04.26"
      y_line: 16
      font_size: 1
      color: [0, 255, 0]
```

## Bluetooth gateway

See `BT_GATEWAY_SETUP.md` for the full setup of an ESP32 Bluetooth proxy and the steps required to use BLE devices in Home Assistant.

## Example files

- `examples/test_display_lines.yaml`
- `examples/automation_multi_page.yaml`

## Privacy

This repository contains no private MAC addresses, credentials, or personal entity IDs.
Replace the placeholder entities with your own Home Assistant entities before use.
