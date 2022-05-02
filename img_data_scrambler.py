#!./venv/bin/python3

import exif
import random
import os
import argparse
import os


images_dir = "./images"


def cmdline_args():
    """
    Gets the command line args. Sets the images directory by the -d option
    of the command line.

    Raises:
        AssertionError: when the -d is not a valid dir
    """
    global images_dir
    parser = argparse.ArgumentParser(description="Scramble images, introducing some ingestion challenges")
    parser.add_argument("-d", "--images-dir", default=images_dir, type=str, required=False, help="images directory")
    args, _ = parser.parse_known_args()
    assert os.path.isdir(args.images_dir), f"-d option is not a valid direcotry: {args.images_dir}"
    images_dir = args.images_dir


def scrambler(dir_path):
    """
    Introduces metadata anomalies and duplicates into a collection of images.

    Args:
        dir_path (str): path to directory of images
    """
    # get the images dir from the command line
    cmdline_args()
    image_count = 0
    for (_, _, file_names) in os.walk(dir_path):
        for file in file_names:
            print(f"found: {file}")
            image_count += 1
            path = os.path.join(dir_path, file)

            with open(path, 'rb') as file_img:
                img = exif.Image(file_img)

            if img.has_exif:
                # resize 5% of the images to be tiny
                rand_resizer = random.randint(1, 20)
                if rand_resizer <= 1:
                    img.image_width = 10
                    img.image_height = 10

                # flip 5% of the images upside down
                rand_flipper = random.randint(1, 20)
                if rand_flipper <= 1:  
                    img.orientation = 3

                # delete 5% of the datetime data
                rand_del_datetime = random.randint(1, 20)
                if rand_del_datetime <= 1:
                    img.delete('datetime')

                # change extension to 'gif' on 5% of images
                rand_gif = random.randint(1, 20)
                if rand_gif <= 1:
                    base = os.path.splitext(path)[0]
                    os.rename(path, base + '.gif')

                # save the changes to the image metadata
                with open(path, 'wb') as modified_img:
                    modified_img.write(img.get_file())

                # duplicate 5% of the images 
                rand_dupper = random.randint(1, 20)
                if rand_dupper <= 1:
                    without_ext = os.path.splitext(path)[0]
                    ext = os.path.splitext(path)[1]
                    dup_path = without_ext + "2" + ext
                    with open(dup_path, 'wb') as modified_img:
                        modified_img.write(img.get_file())
    # print done
    print(f"processed {image_count} images")
    print("done")


if __name__ == "__main__":
    scrambler(images_dir)

