import signal
import sys
import time

from src.hidpp import get_all_cids, pressed_set, set_divert


def learn(handle, idx):
    cids = get_all_cids(handle, idx)
    # Divert everything so that status is reported
    for c in cids:
        set_divert(handle, idx, c, True)

    def cleanup(*_):
        for c in cids:
            set_divert(handle, idx, c, False)
        print("\nUndiverted all controls. Terminating.")
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    print("LEARN MODE. Press each button as single / double / hold.")
    print("Note the CID for each gesture. Watch whether a HOLD keeps the same")
    print("CID pressed (-> use GESTURES) or fires a new CID (-> use ON_PRESS).\n")
    prev = set()
    while True:
        data = handle.read(64)
        if data:
            cur = pressed_set(data, idx)
            if cur is not None:
                for c in cur - prev:  # only print new presses
                    print(f"  {time.strftime('%H:%M:%S')}  pressed CID 0x{c:04x}")
                prev = cur
        else:
            time.sleep(0.005)
