# Photo Organization Script
## What is it?
Appends the date ("yyyymmdd_hhmmss - picturename") to all the pictures in a folder.
You also have the option to automatically create and move the pictures into a folder ("yyyymm") if you so choose.

## How it works.
The script first looks to see if the photo already has a valid data at the begining of the filename. If it does the script does nothing.
It then looks to see if the file was taken by an android phone by looking for "IMG" or "PXL". If it finds either it strips them from the name.
It them looks to see if the image metadata of date taken. If it finds one it appends yyyymmdd_hhmmss to the photo name.
If it can't find anything above it uses the modified time.

## Dependencies
the Pillow library is required.
install PIL with pip install PIL
https://pillow.readthedocs.io/en/stable/

## Running the script
Make sure python is installed with PIL:

To just rename pictures:

    python organize_photos.py -directory "path to pictures"
To rename and move:

    python organize_photos.py -directory "path to pictures" -move "true"
