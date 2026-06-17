from src.keys import KEY, MOD
from src.keystroke import tap_key


class Key:
    """A single key tap, with zero or more modifiers held during the tap."""

    def __init__(self, name, modifiers):
        if name not in KEY:
            raise KeyError(
                f"Unknown key {name!r}. Known keys: {', '.join(sorted(KEY))}"
            )
        flags = 0
        for modifier in modifiers:
            if modifier not in MOD:
                raise KeyError(
                    f"Unknown modifier {modifier!r}. "
                    f"Known modifiers: {', '.join(sorted(MOD))}"
                )
            flags |= MOD[modifier]
        self.name = name
        self.modifiers = modifiers
        self.keycode = KEY[name]
        self.flags = flags

    def perform(self):
        tap_key(self.keycode, self.flags)

    def __repr__(self):
        parts = [repr(self.name), *(repr(m) for m in self.modifiers)]
        return f"key({', '.join(parts)})"


class Call:
    """A deferred call to a Python function."""

    def __init__(self, func, args, kwargs):
        if not callable(func):
            raise TypeError(f"call() expects a function, got {func!r}")
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def perform(self):
        self.func(*self.args, **self.kwargs)

    def __repr__(self):
        name = getattr(self.func, "__name__", repr(self.func))
        return f"call({name})"


def key(name, *modifiers):
    """Build a key tap. The key name comes first; modifiers follow it."""
    return Key(name, modifiers)


def call(func, *args, **kwargs):
    """Build a deferred function call, optionally with arguments."""
    return Call(func, args, kwargs)


def _as_action(action):
    """Coerce one binding entry into something with a .perform() method."""
    if isinstance(action, (Key, Call)):
        return action
    if callable(action):
        return Call(action, (), {})
    raise TypeError(
        f"Invalid action {action!r}. Use key(...), call(...), or a function."
    )


def perform(binding):
    """
    Run a binding: a single action or a list/tuple of actions, in order.

    Each action runs in a try/except so that a buggy function or key does not
    take down the whole remap loop.
    """
    actions = binding if isinstance(binding, (list, tuple)) else [binding]
    for action in actions:
        try:
            _as_action(action).perform()
        except Exception as error:  # keep the daemon alive on a bad action
            print(f"  Action {action!r} failed: {error}")
