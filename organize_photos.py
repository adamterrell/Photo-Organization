import os
import re
import shutil
import time
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
import argparse

parser = argparse.ArgumentParser(description='Append the date to your photos!.')
parser.add_argument("-d", '--directory')
parser.add_argument("-m", '--move')
args= parser.parse_args()

def create_dir(dir):
    try:
        os.makedirs(dir, exist_ok=True)
    except OSError as error:
        print (error)

def create_folders(dir):
    for filename in os.listdir(dir):
        info = os.stat(dir + filename)
        folder = time.strftime("%Y%m", time.gmtime(info.st_mtime))
        create_dir(dir + folder)
        shutil.move(dir + filename, dir + folder + "/" + filename)

def get_minimum_creation_time(exif_data):
    #this function converts the exif date to something human readable
    mtime = '?'
    if 36867 in exif_data and exif_data[36867] < mtime: # 36867 = DateTimeOriginal
        mtime = exif_data[36867]
    elif 306 in exif_data and exif_data[306] < mtime: # 306 = DateTime
        mtime = exif_data[306]
    elif 36868 in exif_data and exif_data[36868] < mtime: # 36868 = DateTimeDigitized
        mtime = exif_data[36868]
    if mtime != '?':
        return time.strftime("%Y%m%d_%H%M%S", time.strptime(mtime, "%Y:%m:%d %H:%M:%S"))

#@TODO change the function name.
def androidphoto_p (filename):
    #this function checks the first 3 letters of the filename
    firstthree = filename[0:3]
    if(firstthree == 'IMG') or (firstthree == 'PXL'):
        return True

def valid_date_p(date):
    try:
        time.strptime(date, "%Y%m%d_%H%M%S")
        return True
    except Exception as e:
        pass
    
def rename_picture2(fullFileName):
    #try to open the image.  If it doesn't open print out the error and move on
    try:
        #print("Opening %s"%fullFileName)
        img = Image.open(fullFileName)
    except Exception as e:
        print(f"Skipping {fullFileName} due to exception: {e}")
        return
    filepath = Path(fullFileName)
    filename = filepath.name
    name = filepath.stem
    date_from_name = name[0:15]
    try:
        date_taken = get_minimum_creation_time(img._getexif())
    except Exception as e:
        date_taken = ""
        print(f"{fullFileName} Does not have a date taken metadata")
    if valid_date_p(date_from_name):
        img.close()
        return 
    #If the picture was taken with andriod   
    if androidphoto_p(filename):
        new_file_name = filename[4::]
        img.close()
        print("This is an Andriod Photo Removing the prefix")
        rename_if_exists_move(fullFileName, filepath.with_name(new_file_name))
        return
    #This renames the photo to append the date taken to the name.
    #If the file exists it will move the file to a folder called duplicate
    #in the root.
    if date_taken:
        img.close()
        new_file_name = date_taken + " - " + filename
        print(f"Renaming {fullFileName} to {new_file_name}")
        rename_if_exists_move(fullFileName, filepath.with_name(new_file_name))
        return
    #This is the catch all. If there isn't a date in the metadata it just uses the date modified.
    #not ideal. modified times in windows are unreliable. Linux 
    else:
        img.close()
        mod_date = time.strftime("%Y%m%d_%H%M%S", time.gmtime(os.path.getmtime(fullFileName)))
        try: rename_if_exists_move(fullFileName, filepath.with_name(date_taken + " - " + filename))
        except Exception as e:
            print(f"Error {e} happened renaming {fullFileName}")
            return

#This function takes a filepath and a filepath with the renamed file.
# If there is already a file with that same name it moves it into a duplicate folder.
def rename_if_exists_move(original_filepath, new_name):
    parsed_file_path = os.path.split(original_filepath)
    dirname = parsed_file_path[0]
    filename = parsed_file_path[-1]
    try: os.rename(original_filepath, new_name)
    except Exception as e:
        print('File already exists moving to duplicate folder')
        newdirname = (dirname + '/' + 'duplicate/')
        create_dir(newdirname)
        shutil.move(original_filepath, (os.path.join(newdirname, filename)))
  
def rename_all_pictures(rootdir):
    print('Starting')
    for root, dirs, files in os.walk(rootdir):
        for name in files:
                rename_picture2(os.path.join(root, name))
    print('All Done')
    
def move_pictures(rootdir):
    for root, dirs, files in os.walk(rootdir):
        for name in files:
            parsed_file_path = os.path.split(os.path.join(root, name))
            date_from_name = name[0:15]
            try:
                foldername = time.strftime("%Y%m", time.strptime(date_from_name, "%Y%m%d_%H%M%S"))
                create_dir(os.path.join(rootdir, foldername))
                shutil.move(os.path.join(root, name), os.path.join(rootdir, foldername, name))
            except Exception as e:
                print("Skipping '%s' due to exception: %s"%(name, e))
                continue

rename_all_pictures(args.directory)
if args.move:
    move_pictures(args.directory)