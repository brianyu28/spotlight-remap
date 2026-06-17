import Quartz

# One reusable event source.
# HIDSystemState means the event is built as though it came from the hardware input system.
_event_source = Quartz.CGEventSourceCreate(Quartz.kCGEventSourceStateHIDSystemState)


def tap_key(keycode, flags=0):
    """
    Synthesize a key-down then key-up for `keycode` with optional modifier
    flags, and inject them into the OS input stream.
    """
    down = Quartz.CGEventCreateKeyboardEvent(_event_source, keycode, True)
    up = Quartz.CGEventCreateKeyboardEvent(_event_source, keycode, False)
    Quartz.CGEventSetFlags(down, flags)  # explicitly set (or clear) modifiers
    Quartz.CGEventSetFlags(up, flags)

    # kCGHIDEventTap injects at the lowest point, so every app sees it.
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, down)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, up)
