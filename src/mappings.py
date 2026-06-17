"""
Custom mappings file.
Edit this file to control what each button does.
Each dictionary maps a Spotlight CID to a (keycode, modifier_flags) tuple.

Combine modifiers with |, e.g. MOD["cmd"] | MOD["shift"].

ON_PRESS key mappings fire immediately when the CID arrives.
GESTURES key mappings fire after timing the gesture (single / double / hold).
"""

from src.constants import SPOTLIGHT_CIDS
from src.keys import KEY, MOD

ON_PRESS = {
    # Default mappings: right and left buttons map to arrow keys with no modifiers
    SPOTLIGHT_CIDS["RIGHT_SHORT"]: (KEY["right"], MOD["none"]),
    SPOTLIGHT_CIDS["LEFT_SHORT"]: (KEY["left"], MOD["none"]),
    # Custom mappings, map other buttons to different keys with modifiers.
    # Make changes to any of these to customize behavior.
    SPOTLIGHT_CIDS["LEFT_LONG"]: (KEY["c"], MOD["opt"]),
    SPOTLIGHT_CIDS["ACTION_SHORT"]: (KEY["q"], MOD["opt"]),
    SPOTLIGHT_CIDS["ACTION_DOUBLE"]: (KEY["b"], MOD["opt"]),
}

GESTURES = {}
