import os
import json


class ResolutionSelector:
    """
    Selects a resolution from a JSON config and ensures it aligns to a multiple (e.g., 64).
    """

    try:
        p = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(p, 'resolutions.json')

        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                RESOLUTIONS = json.load(f)
        else:
            # Fallback if file is missing
            RESOLUTIONS = {"Error: Config Missing": [512, 512]}
    except Exception as e:
        RESOLUTIONS = {f"Error: {str(e)}": [512, 512]}

    @classmethod
    def INPUT_TYPES(s):
        # We convert the keys of our loaded dictionary into a list for the dropdown
        resolution_list = list(s.RESOLUTIONS.keys())

        return {
            "required": {
                "preset": (resolution_list,),
                # Defaulting to 64 is safe for SD1.5, SDXL, and SD3
                "round_to_multiple": ("INT", {"default": 64, "min": 8, "max": 128, "step": 8}),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "get_resolution"
    CATEGORY = "Utils"

    def get_resolution(self, preset, round_to_multiple):
        # If the preset isn't found for some reason, default to 1024
        dims = self.RESOLUTIONS.get(preset, [1024, 1024])
        w, h = dims[0], dims[1]

        # Rounding Logic
        # Formula: round(value / multiple) * multiple
        w = round(w / round_to_multiple) * round_to_multiple
        h = round(h / round_to_multiple) * round_to_multiple

        return (int(w), int(h))