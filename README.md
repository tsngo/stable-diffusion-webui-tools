# Stable Difussion Web UI Tools

Various python and nodeJS scripts that are useful with this fork of
[stable-diffusion-webui](https://github.com/tsngo/stable-diffusion-webui).

Most tools are standalong but some depend on specific features in the forked version of stable-diffusion-webui.

# Installation
pip install -r requirements.txt

# Usage

## Strip PNG Chunk Info
python strip_png_info.py /path/to/file [/path/to/newfile]

Removes the PNG Check Info from a PNG file

## Get PNG Chunk Info
python get_png_info.py /path/to/file

Outputs the PNG Chunk Info from a PNG file as JSON

## Add Tags to file (Windows only)
python add_tags.py /path/to/file csv_of_tags [cvs_tags_to_remove]

Uncomment pywin32 in requirements.txt and rerun installation steps. Adds list of tags and removes list of tags for a file that supports tags. Recommend using [FileMeta](https://github.com/Dijji/FileMeta/releases) to allow PNG file tags.

## Remove orphaned param files
python remove_orphan_params.py glob_pattern_to_param_files

Deletes param files that orphaned (don't have a png or jpg image of the same filename). Example of glob patterns: */*.json or */*.txt


