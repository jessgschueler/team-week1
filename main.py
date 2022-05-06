from exif import Image
from PIL import Image
from PIL.ExifTags import TAGS
from csv import DictWriter
import pandas as pd
import os, glob
import numpy as np
import hashlib
import datetime

#function to rename files
def file_rename():
    """Renames all files in the image to ensure no duplicates and make sure all are the same file type
    """
    #use counter to count up + 1 for every image
    count = 10
    #for loop that iterates over each image in images
    for image in os.listdir('images'):
       #rename image file to img_(file number)
       
        os.rename(f'./images/{image}', f'./images/img_{count}.jpg')
        count += 1

def img_filepaths():
    """
    Returns a list of all the file filepaths in our directory variable.
    """
    directory = "./images"
    filepaths = []
    for image in os.listdir(directory):
        i = os.path.join(directory, image)
        if os.path.isfile(i):
            filepaths.append(i)
    return filepaths

def dict_convert():
    """
    Returns a list of dictionaries of all of the metadata for a list of items in our file path from img_filepaths().
    """
    dict_list = []
    image_names = img_filepaths()
    # assign image names as our img_filepaths function
    for image in image_names:
    # Loop through each image in our directory
        try:
            image_file = Image.open(image)
            # assign image_file as the image file being open.
            exifdata = image_file.getexif()
            # assign pillow metadata tags onto id fields
            file_dict = {}
            for tag_id in exifdata:
                # loop through the tag_ids (metadata tags)
                tag = TAGS.get(tag_id, tag_id)
                # acquire the tags and convert them into human readable metadata tags
                data = exifdata.get(tag_id)
                # get the value attributed to the tags in the metadata
                if isinstance(data, bytes):
                # check if our data is readable data
                    data = data.decode()
                # if not readable, decode it.
                file_dict[tag] = data
                # create a dictionary key-value pair with {metadata tag: data from photo}
            name = {'File Path': image}
            file_dict.update(name)
            dict_list.append(file_dict)
            # append the dictionary to our empty list "dict_list"
        except:
        # If the file is not readable by our function, instead of raising a value error. Pass it on through and leave it's dictionary empty.
            pass   
    return dict_list
    # returns our list of dictionaries for each photo.

dict_list = dict_convert()
# assign our dict_list to our function(dict_convert()) output
field_names = ['TileWidth', 'TileLength', 'GPSInfo','ResolutionUnit', 'ExifOffset', 'Make', 'Model', 'Software', 'Orientation', 'DateTime', 'XResolution', 'YResolution', 'HostComputer', 'File Path']
# assign our header column names to the second photo in our directory (The first one is Blank [0])
with open("./data/meta_data.csv", 'w',newline='') as csvfile:
# write to meta_data.csv
    writer = DictWriter(csvfile, fieldnames=field_names, extrasaction='ignore')
    # to the csv assign the fieldnames as 'field_names' and ignore any data that doesnt fit in our columns(field_names)
    writer.writeheader()
    # write the header with "field_names"
    writer.writerows(dict_list)
    # write the rows with our dict_list which was the output of our dict_convert() function.