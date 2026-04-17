# Bluetooth Gateway Setup for Home Assistant

A Bluetooth gateway is recommended when Home Assistant is not physically close to the LED panel or other BLE devices.

## Recommended hardware

- ESP32 DevKit, D1 Mini ESP32, or a similar ESP32 board
- USB cable
- Stable 5V power supply
- Good Wi-Fi coverage

## Goal

The ESP32 runs ESPHome with Bluetooth Proxy enabled.
Home Assistant then uses it as a remote BLE adapter.

## 1. Install ESPHome in Home Assistant

In Home Assistant:
- Settings
- Add-ons
- Install **ESPHome**
- Start the add-on

Also make sure the **Bluetooth** integration is enabled.

## 2. Flash the ESP32

Connect the ESP32 by USB and flash it with ESPHome.

Example configuration:

```yaml
substitutions:
  name: bt-proxy-led-panel

esphome:
  name: ${name}
  name_add_mac_suffix: true

esp32:
  variant: esp32
  framework:
    type: esp-idf

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  ap:
    ssid: "BT-Proxy-Fallback"
    password: !secret wifi_ap_password

captive_portal:

logger:

api:

ota:
  platform: esphome

esp32_ble_tracker:

bluetooth_proxy:
  active: true
```

## 3. Add secrets

In `secrets.yaml`:

```yaml
wifi_ssid: "YOUR_WIFI"
wifi_password: "YOUR_WIFI_PASSWORD"
wifi_ap_password: "YOUR_FALLBACK_PASSWORD"
```

## 4. Add the gateway to Home Assistant

After boot:
- Settings
- Devices & Services
- Add the ESPHome device if needed

Then verify under:
- Settings
- Devices & Services
- Bluetooth

The ESP32 should show up as a Bluetooth proxy / remote adapter.

## 5. Place the gateway correctly

- Place the ESP32 close to the LED panel
- Avoid metal enclosures
- Avoid placing it directly next to the Wi-Fi router
- Test with less than 1 meter distance first

## 6. Use the gateway for BLE devices

Home Assistant can use the same gateway for multiple BLE devices, including:
- the ACTION 32x32 LED panel
- BLE thermometers
- door sensors
- plant sensors
- battery sensors
- beacons

## 7. Troubleshooting

If BLE devices do not show up:
- reboot the ESP32
- move it closer to the device
- make sure the BLE device is not connected to a phone app
- verify the Bluetooth integration is loaded
- keep the ESPHome proxy configuration minimal
