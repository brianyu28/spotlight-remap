import sys

from src.hidpp import (
    detect_device_index,
    get_logitech_device_handle,
    get_reprogrammable_controls_index,
)
from src.learn import learn
from src.remap import remap
from src.restore import restore


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "remap"
    handle = get_logitech_device_handle()
    if cmd == "device":
        detect_device_index(handle)
        return
    idx = get_reprogrammable_controls_index(handle)
    if cmd == "learn":
        learn(handle, idx)
    elif cmd == "restore":
        restore(handle, idx)
    else:
        remap(handle, idx)


if __name__ == "__main__":
    main()
