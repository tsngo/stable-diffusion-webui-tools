# Stable Difussion Web UI Tools

Various python and nodeJS scripts that are useful with this fork of
["stable-diffusion-webui"](https://github.com/tsngo/stable-diffusion-webui).

Most tools will depend on the JSON parameter file output unless otherwise noted.

## Strip PNG Chunk Info
python ./strip_png_info.py /path/to/file [/path/to/newfile]

Removes the PNG Check Info from a PNG file

## Get PNG Chunk Info
python ./get_png_info.py /path/to/file

Outputs the PNG Chunk Info from a PNG file as JSON