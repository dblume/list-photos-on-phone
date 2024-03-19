[![Code Climate](https://codeclimate.com/github/dblume/list-photos-on-phone/badges/gpa.svg)](https://codeclimate.com/github/dblume/list-photos-on-phone)
[![Issue Count](https://codeclimate.com/github/dblume/list-photos-on-phone/badges/issue_count.svg)](https://codeclimate.com/github/dblume/list-photos-on-phone/issues)
[![License](https://img.shields.io/badge/license-WTFPL_license-blue.svg)](https://raw.githubusercontent.com/dblume/list-photos-on-phone/main/LICENSE.txt)
![python2.x](https://img.shields.io/badge/python-2.x-yellow.svg) [![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)
# list-photos-on-phone

This is a simple Python script to run on a Windows system with an iPhone attached. It iterates the photos on the phone, and lists the ones that haven't been copied to the local disk yet.

### This is a Deprecated Project Now

iPhones don't provide a DCIM folder when connected to Windows computers anymore.

### Getting Started

You need Windows Python and Python for Windows Extensions Pywin32 (218) for this script to work.

It relies on a YAML data file, name-to-path.yaml, that maps from a name in the iPhone's name to the local directory to which you want those photos copied.  For example,

    richard: C:\Users\Richard\Pictures\iPhone
    arline: C:\Users\Arline\Pictures

Run the script from IDLE or an IDE for easier clipboard access to its output, otherwise, from the DOS command line you can redirect to a file like so:

    C:\Python27\python.exe list-photos-on-phone.py > %TEMP%\photos.txt
    notepad %TEMP%\photos.txt

### Why was this needed?

It used to be easier to open a Windows Explorer window and browse a Virtual Folder of the photos on your iPhone. But since iOS 8.1.1, [iOS's DCIM hierarchy has added more opaque subfolders](https://www.facebook.com/photo.php?fbid=10152438909906561&set=a.395891001560.172294.687611560&type=1&theater) making it more difficult to find the photos you want. (And even though you can flatten the view, [you can't drag the photos from that view out](https://www.facebook.com/photo.php?fbid=10152446470656561&set=a.395891001560.172294.687611560&type=1&comment_id=10152467640501561&offset=0&total_comments=3).)

For Windows users who want to manually backup photos, this is a little script that sorts out where the new photos are.

### Why not have it do the copying too?

At the time I wrote this Pywin32 didn't expose all the shell functions I wanted, and I couldn't figure out how to create a stream from the ShellItem. See failed experiments 1, 2, and 3 in the source code.

### Licence

This software uses the [WTFPL](http://www.wtfpl.net/).

