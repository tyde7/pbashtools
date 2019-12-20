#!/usr/bin/env python3
import os, sys, argparse
from bisect import bisect_left

def index(a, x):
    'Locate the leftmost value exactly equal to x'
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    return -1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generating HEIC images from JPG folder. magick command lines is required.")
    parser.add_argument("origin", type=str, help="JPG Folder")
    parser.add_argument("-d","--destination", type=str, default=None, help="HEIC Folder (Default: origin_HEIC)",required=False)
    parser.add_argument("-n", "--no-deletion", action="store_true", help="Do not delete original JPG files.",required=False)
    parser.add_argument("-c","--no-check-magick-binary", action="store_true",help="Do not check if magick binary is usable.", default=False, required=False)
    args = parser.parse_args()
    origin = args.origin
    dest = args.destination if args.destination else origin+"_DCIM"

    rcode = os.system("magick 2>&1 > /dev/null")
    if rcode and not args.no_check_magick_binary:
        print("Magick is not found. Use apt/yum/pacman/brew to install magick. :-)")
        print("If you are using Windows or some other os, just download the binary and add it to path.")
        sys.exit(-1)

    if  args.no_check_magick_binary:
        print("Warning: running without checking magick binary.")

    if not args.no_deletion:
        r=input("Warning: in this mode, this program will delete JPG files after converting.\n And if there is a jpg file which has same name with a HEIC, this file will also be deleted.\nFully aware the risk, please enter y. Else rerun this program with -n option.\n")
        if r.lower() != "y":
            print("User canceled.")
            sys.exit(0)

    if dest in os.listdir("."):
        print("Destination directory {0} is found.".format(dest))
    else:
        result = input("Dest not found. Creating new dir{0}?(y/n)".format(dest)).lower()
        if result == "y":
            os.mkdir(dest)
        elif result == "n":
            print("Canceled by user.")
            sys.exit(0)
        else:
            print("Error input. Quit.")
            sys.exit(-1)

    # Generate new HEIC
    convert_count = 0
    deletion_count = 0
    old = os.listdir(origin)
    new = sorted(os.listdir(dest))
    print("Going to generate HEIC... Please dont write any new HEIC to {0}.".format(dest))
    for of in old:
        if of.endswith("jpg"):
            name = of[:-4]
            if index(new,+name+".HEIC") == -1:
                os.system("magick \"{old}/{name}.jpg\" \"{dst}\{name}.HEIC\"".format(old=origin, dst=dest, name=name))
                convert_count += 1
            if not args.no_deletion:
                os.remove("old/" + new)
                deletion_count += 1

    print("-------Summary-------")
    print("{0} files is converted.".format(convert_count))
    if args.no_deletion:
        print("0 files is deleted as no deletion is enabled.")
    else:
        print("{0} files is deleted.".format(deletion_count))
