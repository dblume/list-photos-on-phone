#!/usr/bin/python
# A Windows command line script to find the photos that haven't been
# copied to the local machine yet.

import os
import sys
import time
from optparse import OptionParser
from win32com.shell import shell, shellcon
from collections import defaultdict
import yaml

__author__ = "David Blume"
__copyright__ = "Copyright 2014, David Blume"
__license__ = "http://www.wtfpl.net/"

g_verbose = False


def process_photos(folder, photo_dict, prev_image):
    """
    Adds photos to photo_dict if they are newer than prev_image.
    :param folder: The PIDL of the folder to walk.
    :param photo_dict: A defaultdict of pathname to list of photos.
    :param prev_image: The most recent photo already copied to the local disk.
    """
    for pidl in folder.EnumObjects(0, shellcon.SHCONTF_NONFOLDERS):
        name = folder.GetDisplayNameOf(pidl, shellcon.SHGDN_FORADDRESSBAR)
        dirname = os.path.dirname(name)
        basename, ext = os.path.splitext(os.path.basename(name))
        if ext.endswith("JPG"):
            # Failed Experiment 1: Get creation date
            # SHGetDataFromIDList() does not exist
            # data = shell.SHGetDataFromIDList(folder, pidl,
            #             shellcon.SHGDFIL_FINDDATA)

            # Failed Experiment 2: Get creation date
            # raises pywintypes.com_error: ('The parameter is incorrect.')
            # requires: from win32com.propsys import pscon
            # item = shell.SHCreateItemFromIDList(pidl, shell.IID_IShellItem2)
            # filetime = item.GetFileTime(pscon.PKEY_DateCreated)

            # Failed Experiment 3: Open file to stream
            # raises TypeError: The Python instance can not be a COM object
            # item = shell.SHCreateItemFromIDList(pidl, shell.IID_IShellItem2)
            # Note pythoncom.IID_IStream
            # stream = item.BindToHandler(0, shell.BHID_Stream, ???)

            # Experiment 4: List only the images that are newer.
            if prev_image is None or basename > prev_image:
                photo_dict[dirname].append(name)


def walk_dcim_folder(dcim_pidl, parent, prev_image):
    """
    Iterates all the subfolders of the iPhone's DCIM directory, gathering
    photos that need to be processed in photo_dict.

    :param dcim_pidl: A PIDL for the iPhone's DCIM folder
    :param parent: The parent folder of the PIDL
    :param prev_image: The most recent photo already copied to the local disk
    """
    photo_dict = defaultdict(list)
    dcim_folder = parent.BindToObject(dcim_pidl, None, shell.IID_IShellFolder)
    for pidl in dcim_folder.EnumObjects(0, shellcon.SHCONTF_FOLDERS):
        folder = dcim_folder.BindToObject(pidl, None, shell.IID_IShellFolder)
        process_photos(folder, photo_dict, prev_image)

    for key in photo_dict:
        for item in sorted(photo_dict[key]):
            print item
        print


def get_dcim_folder(device_pidl, parent):
    """
    Tries to find an iPhone by searching the pidl for the path
    "Internal Storage\DCIM".
    :param device_pidl: A candidate Windows PIDL for the iPhone
    :param parent: The parent folder of the PIDL
    """
    device_name = parent.GetDisplayNameOf(device_pidl, shellcon.SHGDN_NORMAL)
    name = None
    pidl = None

    folder = parent.BindToObject(device_pidl, None, shell.IID_IShellFolder)
    for pidl in folder.EnumObjects(0, shellcon.SHCONTF_FOLDERS):
        name = folder.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL)
        if name == "Internal Storage":
            break
    if name != "Internal Storage":
        return None, None, device_name

    folder = folder.BindToObject(pidl, None, shell.IID_IShellFolder)
    for pidl in folder.EnumObjects(0, shellcon.SHCONTF_FOLDERS):
        name = folder.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL)
        if name == "DCIM":
            break
    if name != "DCIM":
        return None, None, device_name

    return pidl, folder, device_name


def get_destination_for_phone(localdir, iphone_name):
    """
    Read a YAML file that maps a phone's name to a local directory.
    :param iphone_name: The iPhone's name
    """
    names = yaml.load(file(os.path.join(localdir, "name-to-path.yaml"), "r"))
    for k in names:
        if k in iphone_name.lower():
            if g_verbose:
                print "Local photo directory: %s" % (names[k], )
            return names[k]
    return None


def get_prev_image(path):
    """
    Return the most recent image already found in the specified directory.
    :param path: The path to search.
    """
    prev_basename = None
    for root, dirs, files in os.walk(path):
        for name in files:
            basename, ext = os.path.splitext(name)
            basename = basename.upper()
            ext = ext.upper()
            if ext == ".JPG":
                if prev_basename is None or prev_basename < basename:
                    prev_basename = basename
            elif ext == ".TXT":
                # Maybe it's a special .jpg.txt file.
                basename, ext = os.path.splitext(basename)
                if ext.upper() == ".JPG":
                    basename = basename[basename.find("IMG_"):]
                    if prev_basename is None or prev_basename < basename:
                        prev_basename = basename
    if g_verbose:
        print "The most recent image already on the computer is", prev_basename
    return prev_basename


def main(all_images):
    start_time = time.time()
    localdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    desktop = shell.SHGetDesktopFolder()

    # Find the iPhone in the Virtual Folder "Computer"
    for pidl in desktop.EnumObjects(0, shellcon.SHCONTF_FOLDERS):
        if desktop.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "Computer":
            folder = desktop.BindToObject(pidl, None, shell.IID_IShellFolder)
            for dpidl in folder:
                # If this is the iPhone, get the PIDL of its DCIM folder.
                dcim_pidl, parent, iphone_name = get_dcim_folder(dpidl, folder)
                if dcim_pidl is not None:
                    if all_images:
                        prev_image = None
                    else:
                        dest = get_destination_for_phone(localdir, iphone_name)
                        prev_image = get_prev_image(dest)
                    walk_dcim_folder(dcim_pidl, parent, prev_image)
                    break
    if g_verbose:
        print "Done. That took %1.2fs." % (time.time() - start_time)


if __name__ == '__main__':
    parser = OptionParser(usage="usage: %prog [options]",
                          version="%prog 0.0")
    parser.add_option("-v", "--verbose", action="store_true")
    parser.add_option("-a", "--all", action="store_true")
    parser.set_defaults(verbose=False, all=False)
    options, args = parser.parse_args()
    g_verbose = options.verbose
    if len(args) > 0:
        parser.error("incorrect number of arguments")
        sys.exit(1)
    main(options.all)
