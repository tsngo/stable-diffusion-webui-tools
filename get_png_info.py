import json
import sys
from PIL import Image, PngImagePlugin
import os

script_path = os.path.dirname(os.path.realpath(__file__))
try:
    filename = os.path.realpath(sys.argv[1])
except:
    print(
        f"python {__file__} /path/to/file")
    sys.exit(1)

if __name__ == "__main__":
    image = Image.open(filename)
    existing_info = image.info or {}
    print(json.dumps(existing_info))


