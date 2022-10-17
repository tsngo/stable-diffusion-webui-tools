import sys
# requires pywin32 (See requirements.txt. Supports Windows only obviously)
# also recommend FileMeta https://github.com/Dijji/FileMeta to allow tags for PNG
import pythoncom
from win32com.propsys import propsys
from win32com.shell import shellcon
import os

script_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    try:
        filename = os.path.realpath(sys.argv[1])
        tags = sys.argv[2].split(',')
        if len(sys.argv) == 4:
            remove_tags = sys.argv[3].split(',')
    except:
        print(f"python {__file__} /path/to/file csv_of_tags [cvs_tags_to_remove]")
        sys.exit(1)
    
    # get PROPERTYKEY for "System.Keywords"
    pk = propsys.PSGetPropertyKeyFromName("System.Keywords")

    # get property store for a given shell item (here a file)
    ps = propsys.SHGetPropertyStoreFromParsingName(
        filename, None, shellcon.GPS_READWRITE, propsys.IID_IPropertyStore)

    # read & print existing (or not) property value, System.Keywords type is an array of string
    existingTags = ps.GetValue(pk).GetValue()
    if existingTags==None:
        existingTags=[]
    filteredTags = []

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
