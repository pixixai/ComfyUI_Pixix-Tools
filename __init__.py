# __init__.py

from .load_text_node import LoadTextFromFolder

NODE_CLASS_MAPPINGS = {
    "LoadTextFromFolderNode": LoadTextFromFolder
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadTextFromFolderNode": "Load Text (from folder)"
}