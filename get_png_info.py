import argparse
import json
import sys
from PIL import Image
import os

script_path = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", type=str, help="file to get PNG chunks info", required=True)
parser.add_argument("-o", "--output-format", default="json_pretty", choices=["json", "object", "json_pretty"], help="format of output", required=False)

def get_png_info(filename, output_format='object'):
    image = Image.open(filename)
    existing_info = image.info or {}
    indent = 0
    if output_format == "json_pretty":
        indent = 4
    if output_format == "json" or output_format == "json_pretty":
        existing_info = json.dumps(existing_info, indent=indent)
    return existing_info

if __name__ == "__main__":
    args = parser.parse_args()
    args.filename = os.path.realpath(args.filename)

    existing_info = get_png_info(**args.__dict__)
    print(existing_info)


