import signal
import sys
import time

from src.constants import DOUBLE_GAP, HOLD_THRESHOLD
from src.hidpp import pressed_set, set_divert
from src.keystroke import tap_key
from src.mappings import GESTURES, ON_PRESS

# Whether to print information about each key press or gesture
VERBOSE = False


def remap(handle, idx):
    used_cids = set(ON_PRESS) | set(GESTURES)
    if not used_cids:
        sys.exit("Nothing mapped yet -- edit ON_PRESS / GESTURES first.")
    for cid in used_cids:
        set_divert(handle, idx, cid, True)

    def cleanup(*_):
        for cid in used_cids:
            set_divert(handle, idx, cid, False)
        print("\nUndiverted all controls. Terminating.")
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    print(f"Remapping {len(used_cids)} control(s). Ctrl-C to quit.")

    # Per-CID state machine for the GESTURES buttons.
    gestures = {
        cid: dict(
            down=False,
            t_down=0.0,
            held_fired=False,
            pending_single=False,
            double_candidate=False,
            last_release=0.0,
        )
        for cid in GESTURES
    }

    def fire(cid, gesture):
        binding = GESTURES.get(cid, {}).get(gesture)
        if VERBOSE:
            print(f"  CID 0x{cid:04x} -> {gesture}")
        if binding:
            tap_key(*binding)

    prev = set()
    while True:
        data = handle.read(64)
        now = time.time()

        if data:
            cur = pressed_set(data, idx)
            if cur is not None:
                # Rising edges: CIDs newly pressed since the last event.
                for cid in cur - prev:
                    if cid in ON_PRESS:  # firmware gesture: go
                        if VERBOSE:
                            print(f"  CID 0x{cid:04x} -> on_press")
                        tap_key(*ON_PRESS[cid])
                    if cid in gestures:  # start gesture timing
                        gesture_state = gestures[cid]
                        gesture_state["down"] = True
                        gesture_state["held_fired"] = False
                        gesture_state["double_candidate"] = (
                            gesture_state["pending_single"]
                            and now - gesture_state["last_release"] < DOUBLE_GAP
                        )
                        gesture_state["t_down"] = now
                # Falling edges: CIDs released since the last event.
                for cid in prev - cur:
                    if cid in gestures:
                        gesture_state = gestures[cid]
                        gesture_state["down"] = False
                        if gesture_state["held_fired"]:  # hold already fired
                            gesture_state["pending_single"] = False
                        elif gesture_state["double_candidate"]:  # this was tap #2
                            fire(cid, "double")
                            gesture_state["pending_single"] = False
                            gesture_state["double_candidate"] = False
                        else:  # maybe single; wait to
                            gesture_state["pending_single"] = (
                                True  # see if a 2nd tap comes
                            )
                            gesture_state["last_release"] = now
                prev = cur

        # Timers run every loop, even with no new data.
        for cid, gesture_state in gestures.items():
            # Held past the threshold -> fire hold once.
            if (
                gesture_state["down"]
                and not gesture_state["held_fired"]
                and now - gesture_state["t_down"] >= HOLD_THRESHOLD
            ):
                fire(cid, "hold")
                gesture_state["held_fired"] = True
                gesture_state["pending_single"] = False
            # A tap that waited out the double-click window -> it was a single.
            if (
                gesture_state["pending_single"]
                and now - gesture_state["last_release"] >= DOUBLE_GAP
            ):
                fire(cid, "single")
                gesture_state["pending_single"] = False

        if not data:
            time.sleep(0.005)
