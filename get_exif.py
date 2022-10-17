import argparse
import json
import sys
from PIL import Image
import os
import piexif

script_path = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", type=str, help="file to get PNG chunks info", required=True)
parser.add_argument("-o", "--output-format", default="json_pretty", choices=["json", "object", "json_pretty"], help="format of output", required=False)


def extract_exif(image):
    if image is None:
        return {}

    if not "exif" in image.info:
        return image.info or {}

    items = image.info

    exif = piexif.load(image.info["exif"])
    exif_comment = (exif or {}).get("Exif", {}).get(
        piexif.ExifIFD.UserComment, b'')
    try:
        exif_comment = piexif.helper.UserComment.load(exif_comment)
    except ValueError:
        exif_comment = exif_comment.decode('utf8', errors="ignore")

    items['exif comment'] = exif_comment
    geninfo = exif_comment

    for field in ['jfif', 'jfif_version', 'jfif_unit', 'jfif_density', 'dpi', 'exif',
                    'loop', 'background', 'timestamp', 'duration']:
        items.pop(field, None)

    return items

def get_exif(filename, output_format='object'):
    image = Image.open(filename)
    
    existing_info = extract_exif(image)

    indent = 0
    if output_format == "json_pretty":
        indent = 4
    if output_format == "json" or output_format == "json_pretty":
        existing_info = json.dumps(existing_info, indent=indent)
    return existing_info

if __name__ == "__main__":
    args = parser.parse_args()
    args.filename = os.path.realpath(args.filename)

    existing_info = get_exif(**args.__dict__)
    print(existing_info)


