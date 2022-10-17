import json
import sys
from PIL import Image, PngImagePlugin
import os
import base64
import argparse
from get_exif import get_exif

script_path = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", type=str, help="file to add PNG info", required=True)
parser.add_argument("-p", "--params", type=str, default="", help="JSON string of key value pairs to add to PNG", required=False)
parser.add_argument("-r", "--remove-params", type=str, default="", help="comma separated list of tags to remove", required=False)
parser.add_argument("-rp", "--remove-all-params", action="store_true", help="remove all PNG info", required=False)
parser.add_argument("-o", "--output_filename", type=str, help="PNG file to write to", required=False)

def add_exif(filename, params={}, remove_params=[], remove_all_params=False, output_filename=""):
    filename = os.path.realpath(filename)
    if output_filename == "":
        output_filename = filename
    else:
        output_filename = os.path.realpath(output_filename)

    with Image.open(filename) as image:
        if len(params) > 0:
            existing_info = image.info or {}
            pnginfo = PngImagePlugin.PngInfo()

            if existing_info is not None or remove_all_params:
                for k, v in existing_info.items():
                    if k in params or k in remove_params:
                        continue
                    pnginfo.add_text(k, str(v))

            for k, v in params.items():
                pnginfo.add_text(k, str(v))
        image.save(output_filename, pnginfo=pnginfo)

if __name__ == "__main__":
    args = parser.parse_args()
    if args.params == "":
        args.params = {}
    else:
        args.params = json.loads(args.params)

    if args.remove_params == "":
        args.remove_params = []
    else:
        args.remove_params = args.remove_params.split(',')

    args.output_filename = args.filename
    args.params = json.loads(args.params)

    add_exif(**args.__dict__)



