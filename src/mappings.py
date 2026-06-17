"""
Custom mappings file.
Edit this file to control what each button does.

ON_PRESS bindings fire immediately when the CID arrives.
GESTURES bindings fire after timing the gesture (single / double / hold).

A binding is either a single action or a list of actions performed in order.

An action is one of:

  key(name, *modifiers)     tap a key
  call(func, *args, **kw)   call a Python function
  a plain function          shorthand for call(func)

The key name always comes first; modifiers ("cmd", "shift", "opt", "ctrl") follow it.

Examples:

  key("right")                                   one keystroke
  key("q", "opt")                                one keystroke with a modifier
  [key("g"), key("a", "shift"), key("return")]   a sequence of keystrokes
  my_func                                        call a Python function
  [my_func, key("return")]                       call a function, then a keystroke
"""

from src.actions import call, key
from src.constants import SPOTLIGHT_CIDS


def example():
    print("Example function!")


ON_PRESS = {
    # Default mappings: right and left buttons map to arrow keys.
    SPOTLIGHT_CIDS["RIGHT_SHORT"]: key("right"),
    SPOTLIGHT_CIDS["LEFT_SHORT"]: key("left"),
    # Custom mappings: map other buttons to keys, with modifiers if you like.
    SPOTLIGHT_CIDS["LEFT_LONG"]: key("left", "shift"),
    SPOTLIGHT_CIDS["RIGHT_LONG"]: key("right", "shift"),
    SPOTLIGHT_CIDS["CENTER_SHORT"]: call(example),
}

GESTURES = {}
