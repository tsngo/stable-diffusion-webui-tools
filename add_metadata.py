# requires pywin32 (See requirements.txt. Supports Windows only obviously)
# also recommend FileMeta https://github.com/Dijji/FileMeta to allow tags for PNG
import json
import os
import argparse
import glob
from add_exif import add_exif
from add_tags import tag_files
from get_exif import get_exif
from generation_parameters import parse_generation_parameters
from hashlib import md5
script_path = os.path.dirname(os.path.realpath(__file__))
from progesss_bar import progressBar


def add_metadata(files_glob, param_name="parameters", tags_type="both", seed=True, hash=True, filename="", seed_attr="sdwu_seed", hash_attr="sdwu_hash", force=False):
    if files_glob == "":
        files = [filename]
    else:
        files = glob.glob(files_glob)

    tag_exif = tags_type in ["both", "exif"]
    tag_windows = tags_type in ["both", "windows"]
    if tag_windows:
        import pythoncom
        from win32com.propsys import propsys
        from win32com.shell import shellcon

    display = __name__ == "__main__"

    for file in progressBar(files, prefix='Progress:', suffix='Complete', length=50, display=display):
        file = os.path.realpath(file)
        exif_info = get_exif(file)
        params = {}
        
        if not force and tag_exif and seed_attr in exif_info:
            # skip if seed is found
            continue

        if param_name in exif_info:
            params = parse_generation_parameters(exif_info[param_name])

        seed = None
        if "Seed" in params:
            seed = params["Seed"]
        else:
            seed = params["seed"]

        md5sum = md5(json.dumps(params).encode('utf-8')).hexdigest()
        tags = []
        if seed:
            tags.append(seed)
        if hash:
            tags.append(md5sum)

        if tag_windows:
            tag_files(filename=file, tags=tags)
            
        if tag_exif:
            exif = {}
            exif[seed_attr] = seed
            exif[hash_attr] = md5sum
            add_exif(filename=file, params=exif)

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--files-glob", type=str, default="", help="glob pattern to files to tag", required=True)
parser.add_argument("-p", "--param-name", type=str, default="parameters", help="name of generation parameters attribute from EXIF", required=False)
parser.add_argument("-t", "--tags-type", type=str, default="both", choices=["windows", "exif", "both"], help="whether to tag using windows file tags, in the image EXIF or both", required=False)
parser.add_argument("-s", "--seed", action="store_true", default=True, help="add the seed as tag", required=False)
parser.add_argument("-sat", "--seed-attr", type=str, default="sdwu_seed", help="name of seed attribute from EXIF", required=False)
parser.add_argument("-ha", "--hash", action="store_true", default=True, help="add the hash of generation params as tag", required=False)
parser.add_argument("-hat", "--hash-attr", type=str, default="sdwu_hash", help="name of hash attribute from EXIF", required=False)
parser.add_argument("--force", action="store_true", default=False, help="force rewrite of EXIF", required=False)

if __name__ == "__main__":
    args = parser.parse_args()
    
    add_metadata(**args.__dict__)
