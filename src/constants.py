# Logitech's USB vendor ID
VID = 0x046D

# HID++ device index.
# 0xff is for a remote paired directly over Bluetooth, assumed here.
# If using a USB receiver, switch this to the slot number (0x01-0x06).
# You can read the correct value off byte 1 of any HID report the device sends.
DEV = 0xFF

# Software ID: an arbitrary tag (1-15) we choose so we can match HID++ replies
# to our own requests. Any nonzero nibble works.
SW = 0x05

# HID++ feature ID for "Reprogrammable Controls V4" -- the feature that lets us
# enumerate and divert controls.
REPROG = 0x1B04

# Timing for software-detected gestures (seconds). Can be adjusted based on preference.
# Presses for at least this number of seconds are a "hold"
HOLD_THRESHOLD = 0.45
# Second press within ths number of seconds is a "double" press
DOUBLE_GAP = 0.30

# CIDs for Spotlight 2 presentation remote buttons and press styles.
# Determined by running in learn mode.
SPOTLIGHT_CIDS = {
    "RIGHT_SHORT": 0x00D9,
    "RIGHT_LONG": 0x00DA,
    "LEFT_SHORT": 0x00DB,
    "LEFT_LONG": 0x00DC,
    "CENTER_SHORT": 0x0050,
    "CENTER_LONG": 0x00D8,
    "ACTION_SHORT": 0x00FB,
    "ACTION_LONG": 0x00FC,
    "ACTION_DOUBLE": 0x01B0,
}
