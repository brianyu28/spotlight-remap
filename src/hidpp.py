"""
HID++ helper functions for working with Logitech devices over HID++ protocol.
"""

import sys
import time

import hid

from src.constants import DEV, REPROG, SW, VID


def get_logitech_device_handle():
    """
    Find the Logitech vendor-defined HID interface and open it, returning its
    device handle. We identify by vendor ID + a vendor-defined usage page (>= 0xff00).

    Opening raw HID on macOS needs elevated rights (run with sudo) and Input
    Monitoring permission.
    """
    for device in hid.enumerate(VID):
        if device["usage_page"] >= 0xFF00:  # vendor-defined page = HID++ here
            handle = hid.device()
            handle.open_path(device["path"])
            handle.set_nonblocking(1)  # read() returns [] when idle
            return handle
    sys.exit(
        "No vendor (0xff..) HID interface found. Check that this program was "
        "run with sudo and that the remote is paired and active."
    )


def request_hidpp(handle, feat_idx, func_idx, params=(), timeout=1.0):
    """
    Send one HID++ long (0x11) request and return the matching response.

    The function byte packs the function index (high nibble) and our software
    ID (low nibble). We then read until we see a report whose featureIndex and
    function|softwareID echo ours -- ignoring async events and other traffic
    in between -- or until we time out.
    """

    swfunc = (func_idx << 4) | SW
    buf = [0x11, DEV, feat_idx, swfunc] + list(params)
    buf += [0] * (20 - len(buf))  # long reports are 20 bytes
    handle.write(buf)
    end = time.time() + timeout
    while time.time() < end:
        data = handle.read(64)
        if not data:
            time.sleep(0.005)
            continue
        if len(data) >= 4 and data[2] == feat_idx and data[3] == swfunc:
            return data
    raise TimeoutError("no HID++ response")


def get_reprogrammable_controls_index(handle):
    """
    Ask the root feature (always at index 0, function 0) to translate the
    Reprogrammable-Controls feature ID into this device's feature index.
    """
    idx = request_hidpp(handle, 0x00, 0x00, [REPROG >> 8, REPROG & 0xFF, 0])[4]
    if idx == 0:  # 0 means "feature not present"
        sys.exit("No Reprogrammable Controls (0x1b04) on this device.")
    return idx


def get_all_cids(handle, idx):
    """
    Enumerate every control. Function 0 returns the count; function 1
    returns the info (including the CID) for control number i.
    """
    count = request_hidpp(handle, idx, 0x00)[4]
    cids = []
    for i in range(count):
        info = request_hidpp(handle, idx, 0x01, [i])
        cids.append((info[4] << 8) | info[5])  # CID is bytes 4-5 of the reply
    return cids


def set_divert(handle, idx, cid, on):
    """
    Turn diversion on/off for one CID using setCidReporting (function 3).

    The flags byte uses paired bits: 0x01 = the divert state, 0x02 = "the
    divert bit in this message is valid, apply it". So 0x03 means "divert =
    on", 0x02 means "divert = off". We don't wait for a reply because some
    firmware doesn't echo this set; callers can read state back if needed.
    """
    swfunc = (0x03 << 4) | SW
    flags = 0x03 if on else 0x02
    buf = [0x11, DEV, idx, swfunc, cid >> 8, cid & 0xFF, flags] + [0] * 13
    handle.write(buf)
    time.sleep(0.03)
    while handle.read(64):  # drain any echo / pending events
        pass


def pressed_set(data, idx):
    """
    Parse a divertedButtonsEvent into the set of currently-pressed CIDs.
    Returns None if this report isn't such an event. The event is recognized
    by featureIndex == our reprog index and function|softwareID == 0x00 (a
    device-originated event uses software ID 0). The payload is up to four
    2-byte CIDs starting at byte 4; zeros are empty slots.
    """
    if len(data) < 12 or data[2] != idx or data[3] != 0x00:
        return None
    cids = set()
    for i in range(4, 12, 2):
        c = (data[i] << 8) | data[i + 1]
        if c:
            cids.add(c)
    return cids
