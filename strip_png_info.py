import sys
from PIL import Image
import os
script_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    try:
        filename = os.path.realpath(sys.argv[1])
        newfilename = os.path.realpath(filename)
        if len(sys.argv) == 3:
            newfilename = os.path.realpath(sys.argv[2])
    except:
        print(f"python {__file__} /path/to/file [/path/to/newfile]")
        sys.exit(1)
    
    with Image.open(filename) as image:
        image.save(newfilename)


