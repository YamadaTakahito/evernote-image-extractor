import os
import shutil
import string
from datetime import datetime, timezone, timedelta
import random

import plum
from PIL.PngImagePlugin import PngInfo
from exif import Image as exifImage

import csv
import glob


def randomname(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


def covert_jpeg(filepath, time, output_path):
    with open(filepath, 'rb') as img_file:
        try:
            org_img = exifImage(img_file)
            org_img.datetime = time.strftime('%Y:%m:%d %H:%M:%S')
            org_img.datetime_original = time.strftime('%Y:%m:%d %H:%M:%S')
            org_img.datetime_digitized = time.strftime('%Y:%m:%d %H:%M:%S')
            with open(output_path, 'wb') as new_image_file:
                new_image_file.write(org_img.get_file())
        except plum.exceptions.UnpackError:
            pass
        except:
            pass



def covert_png(filepath, time, output_path):
    from PIL import Image
    img = Image.open(filepath)

    exif = img.getexif()
    metadata = PngInfo()
    exif.get_ifd(34665)[36867] = time.strftime('%Y:%m:%d %H:%M:%S')
    exif.get_ifd(34665)[36868] = time.strftime('%Y:%m:%d %H:%M:%S')
    exif.update([(36868, time.strftime('%Y:%m:%d %H:%M:%S'))])
    exif.update([(36867, time.strftime('%Y:%m:%d %H:%M:%S'))])
    exif.update([(306, time.strftime('%Y:%m:%d %H:%M:%S'))])
    metadata.add_text("CreationDate", time.strftime('%Y:%m:%d %H:%M:%S'))

    img.save(output_path, exif=exif, metadata=metadata)


csv_files = glob.glob('csv/*.csv')

for csv_file in csv_files:
    folder = csv_file[4:-4]
    os.makedirs(f"output/{folder}", exist_ok=True)
    with open(csv_file) as c_f:
        reader = csv.DictReader(c_f)
        for row in reader:
            print(row["mime"])
            time = datetime.fromtimestamp(int(row["created"]) / 1000, timezone(timedelta(hours=9)))

            filepath = row["filepath"]
            mime = row["mime"]
            filename = row["filepath"].split("/")[-1][:-4]
            if mime == "image/jpeg":
                output_path = f"output/{folder}/{filename}_{randomname(5)}.jpg"
                covert_jpeg(filepath, time, output_path)
            elif mime == "image/webp":
                output_path = f"output/{folder}/{filename}_{randomname(5)}.jpg"
                covert_jpeg(filepath, time, output_path)
            elif mime == "image/png":
                output_path = f"output/{folder}/{filename}_{randomname(5)}.png"
                covert_png(filepath, time, output_path)
            elif mime == "image/gif":
                output_path = f"output/{folder}/{filename}_{randomname(5)}.gif"
                covert_png(filepath, time, output_path)
            elif mime == "video/quicktime":
                output_path = f"output/{folder}/{filename}_{randomname(5)}.mp4"
                shutil.copyfile(filepath, output_path)
            elif mime == "video/mp4":
                output_path = f"output/{folder}/{filename}_{randomname(5)}.mp4"
                shutil.copyfile(filepath, output_path)
            # else:
            #     raise Exception(mime)
