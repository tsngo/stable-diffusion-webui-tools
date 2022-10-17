import glob
import sys
import os

script_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except:
        print(f"python {__file__} glob_pattern_to_param_files")
        sys.exit(1)
    
    files = glob.glob(path)

    for file in files:
        ext = file.split('.').pop().lower()
        if ext == "txt" or ext == "json":
            pngFile = file.replace(ext, 'png')
            jpgFile = file.replace(ext, 'jpg')
            if not os.path.exists(pngFile) and not os.path.exists(jpgFile):
                print(f"Deleting {file}")
                os.remove(file)
