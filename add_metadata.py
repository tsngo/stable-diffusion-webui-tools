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


def add_ratings(files_glob):
    files = glob.glob(files_glob)
    scoreTotal = {}
    for file in files:
        with open(file, 'r', encoding='utf8') as f:
            scores = json.load(f)
            for score in scores:
                if score['image_id'] in scoreTotal:
                    scoreTotal[score['image_id']].append(score['mean_score_prediction'])
                else:
                    scoreTotal[score['image_id']] = [score['mean_score_prediction']]
    
    for image_id in scoreTotal:
        avg = sum(scoreTotal[image_id]) / len(scoreTotal[image_id])
        scoreTotal[image_id] = avg

    return scoreTotal

def add_metadata(files_glob, param_name="parameters", tags_type="both", seed=True, hash=True, filename="", filename_parser=None, prefix_attr="sdwu", force=False):
    if files_glob == "":
        files = [filename]
    else:
        files = glob.glob(files_glob)

    parsers = [];
    print(filename_parser)
    with open(filename_parser, "r", encoding="utf8") as sp:
        parsers = json.load(sp)

    tag_exif = tags_type in ["both", "exif"]
    tag_windows = tags_type in ["both", "windows"]
    if tag_windows:
        import pythoncom
        from win32com.propsys import propsys
        from win32com.shell import shellcon

    display = __name__ == "__main__"
    for file in progressBar(files, prefix='Progress:', suffix='Complete', length=50, display=display):
        scores = add_ratings('./predictions*.json')
        file = os.path.realpath(file)
        basename = os.path.basename(file).replace('.png', '')
        exif_info = get_exif(file)
        params = {}
        
        # if not force and tag_exif and f"{prefix_attr}_seed" in exif_info:
        #     # skip if seed is found
        #     continue

        if param_name in exif_info:
            params = parse_generation_parameters(exif_info[param_name])

        seed = None
        if "Seed" in params:
            seed = params["Seed"]
        elif "seed" in params:
            seed = params["seed"]
        elif len(parsers) > 0:
            for idx, parser in enumerate(parsers):
                if not "seed" in parser:
                    continue
                sp = parser["seed"]
                parts = file.split(sp["delimiter"])
                if len(parts) > sp["position"] and parts[sp["position"]].isnumeric():
                    seed = parts[sp["position"]]
                    break

        md5sum = md5(json.dumps(params).encode('utf-8')).hexdigest()
        tags = []
        if seed:
            tags.append(f"seed_{seed}")
        if hash:
            tags.append(f"hash_{md5sum}")
        if (basename in scores):
            base = round(scores[basename], 1)
            decimal = int(str(base).split('.').pop())
            base_str = str(base).split('.')[0]
            s = f"score_{base_str}.0"
            if decimal >= 5:
                s = f"score_{base_str}.5"
            tags.append(s)
        if ('CFG scale' in params):
            tags.append(f"cfg_scale_{params['CFG scale']}")
        if ('Sampler' in params):
            tags.append(f"sampler_{params['Sampler']}")
        print(tags)

        if tag_windows:
            tag_files(filename=file, tags=tags, remove_all_tags=True)
            
        # if tag_exif:
        #     exif = {}
        #     exif[f"{prefix_attr}_seed"] = seed
        #     exif[f"{prefix_attr}_hash"] = md5sum
        #     add_exif(filename=file, params=exif)

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--files-glob", type=str, default="", help="glob pattern to files", required=True)
parser.add_argument("-p", "--param-name", type=str, default="parameters", help="name of generation parameters attribute from EXIF", required=False)
parser.add_argument("-t", "--tags-type", type=str, default="both", choices=["windows", "exif", "both"], help="whether to tag using windows file tags, in the image EXIF or both", required=False)
parser.add_argument("-pa", "--prefix-attr", type=str, default="sdwu", help="name of hash attribute from EXIF", required=False)
parser.add_argument("--force", action="store_true", default=False, help="force rewrite of EXIF", required=False)
parser.add_argument("-fp", "--filename-parser", type=str, default="", help="a JSON file containing array of parser definitions", required=False)

if __name__ == "__main__":
    args = parser.parse_args()
    add_metadata(**args.__dict__)
