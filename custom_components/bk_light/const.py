"""Constants for BK Light ACT1026 integration."""

DOMAIN = "bk_light"

CONF_ADDRESS = "address"
CONF_ROTATION = "rotation"
CONF_BRIGHTNESS = "brightness"

DEFAULT_ROTATION = 0
DEFAULT_BRIGHTNESS = 0.85

DISPLAY_WIDTH = 32
DISPLAY_HEIGHT = 32

MANUFACTURER = "BK Light"
MODEL = "ACT1026"
MODEL_DESCRIPTION = "ACTION 32x32 LED Panel"

UUID_NOTIFY = "0000fff4-0000-1000-8000-00805f9b34fb"
UUID_WRITE = "0000fff3-0000-1000-8000-00805f9b34fb"

HANDSHAKE_FIRST = bytes.fromhex("00")
HANDSHAKE_SECOND = bytes.fromhex("01")

ACK_STAGE_ONE = bytes.fromhex("00")
ACK_STAGE_ONE_ALT = bytes.fromhex("00")
ACK_STAGE_TWO = bytes.fromhex("01")
ACK_STAGE_TWO_ALT = bytes.fromhex("01")
ACK_STAGE_THREE = bytes.fromhex("02")
