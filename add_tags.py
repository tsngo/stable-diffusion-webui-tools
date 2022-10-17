import sys
# requires pywin32 (See requirements.txt. Supports Windows only obviously)
# also recommend FileMeta https://github.com/Dijji/FileMeta to allow tags for PNG
import pythoncom
try:
    from win32com.propsys import propsys
    from win32com.shell import shellcon
except:
    propsys = None
    shellcon = None

import os
import argparse
import glob

script_path = os.path.dirname(os.path.realpath(__file__))

def tag_files(files_glob="", tags=[], remove_tags=[], remove_all_tags=False, filename=""):
    if propsys == None or shellcon == None:
        return

    if files_glob=="":
        files = [filename]
    else:
        files = glob.glob(files_glob)

    for file in files:
        # get property store for a given shell item (here a file)
        try:
            ps = propsys.SHGetPropertyStoreFromParsingName(os.path.realpath(file), None, shellcon.GPS_READWRITE, propsys.IID_IPropertyStore)
        except:
            pythoncom.CoInitialize()
            ps = propsys.SHGetPropertyStoreFromParsingName(os.path.realpath(file), None, shellcon.GPS_READWRITE, propsys.IID_IPropertyStore)
            
        pk = propsys.PSGetPropertyKeyFromName("System.Keywords")

        # read & print existing (or not) property value, System.Keywords type is an array of string
        existingTags = ps.GetValue(pk).GetValue()
        if existingTags == None:
            existingTags = []
        filteredTags = []

        if not remove_all_tags:
            for tag in existingTags:
                if tag in remove_tags:
                    continue
                filteredTags.append(tag)

        # build an array of string type PROPVARIANT
        newValue = propsys.PROPVARIANTType(
            filteredTags + tags, pythoncom.VT_VECTOR | pythoncom.VT_BSTR)

        # write property
        ps.SetValue(pk, newValue)
        ps.Commit()



parser = argparse.ArgumentParser()
parser.add_argument("-f", "--files-glob", type=str, default="", help="glob pattern to files to tag", required=True)
parser.add_argument("-t", "--tags", type=str, default="", help="comma separated list of tags", required=False)
parser.add_argument("-r", "--remove-tags", type=str, default="", help="comma separated list of tags to remove", required=False)
parser.add_argument("-rt", "--remove-all-tags", action="store_true", help="remove all tags", required=False)

if __name__ == "__main__":
    args = parser.parse_args()
    
    if args.tags == "":
        args.tags = []
    else:
        args.tags = args.tags.split(',')

    if args.remove_tags == "":
        args.remove_tags = []
    else:
        args.remove_tags = args.remove_tags.split(',')
    
    tag_files(**args.__dict__)