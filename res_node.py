# AI Disclosure: Code comments were generated with AI

import os
import json


class ResolutionSelector:
    @classmethod
    def _get_config_path(cls):
        # Helper to find the file
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resolutions.json')

    @classmethod
    def _load_resolutions(cls):
        # Helper to read the file
        path = cls._get_config_path()
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {"Error: Config Missing": [512, 512]}

    @classmethod
    def INPUT_TYPES(s):
        # This runs ONCE at startup to build the menu
        data = s._load_resolutions()
        return {
            "required": {
                "preset": (list(data.keys()),),
                "round_to_multiple": ("INT", {"default": 64, "min": 8, "max": 128, "step": 8}),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "get_resolution"
    CATEGORY = "DLWW/Utils"

    def get_resolution(self, preset, round_to_multiple):
        # RELOAD the file right now (Hot Reload)
        # This ensures we have the latest numbers, even if the server hasn't restarted
        current_data = self._load_resolutions()

        # Get dimensions (fallback to 1024 if key is missing)
        dims = current_data.get(preset, [1024, 1024])
        w, h = dims[0], dims[1]

        # Apply Rounding
        w = round(w / round_to_multiple) * round_to_multiple
        h = round(h / round_to_multiple) * round_to_multiple

        return (int(w), int(h))