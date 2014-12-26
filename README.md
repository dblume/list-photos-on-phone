# list-photos-on-phone

This is a simple Python script to run on a Windows system with an iPhone attached. It iterates the photos on the phone, and lists the ones that haven't been copied to the local disk yet.

## Getting Started

You need Windows Python and Python for Windows Extensions Pywin32 (218) for this script to work.

It relies on a YAML data file, name-to-path.py, that maps from a name in the iPhone's name to the local directory to which you want those photos copied.  For example,

    richard: C:\Users\Richard\Pictures\iPhone
    arlene: C:\Users\Arlene\Pictures

Run the script like so:

    C:\Python27\python.exe list-photos-on-phone.py

## Why was this needed?

It used to be relatively easy to open a Windows Explorer window and browse a Virtual Folder of the photos on your iPhone. But since iOS 8.1.1, [Apple's DCIM hierarchy has too many opaque subfolders](https://www.facebook.com/photo.php?fbid=10152438909906561&set=a.395891001560.172294.687611560&type=1&theater).

For Windows users who want to manually backup photos, this is a little script that sorts out where the new photos are.

## Why not have it do the copying too?

At the time I wrote this Pywin32 didn't expose all the shell functions I wanted, and I couldn't figure out how to create a stream from the ShellItem. See failed experiments 1, 2, and 3 in the source code.

## Licence

This software uses the [WTFPL](http://www.wtfpl.net/).

--David Blume
