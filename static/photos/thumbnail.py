from sys import argv
from PIL import Image
import os

filename = argv[1]
thumbname = 'thumb-' + os.path.basename(filename)
image = Image.open(filename)
MAX_SIZE = (1200, 800)
THUMB_SIZE = (200, 200)

# pillow will mess up the photo rotation if this is not down:
for orientation in ExifTags.TAGS.keys():
if ExifTags.TAGS[orientation] == 'Orientation': break
exif = dict(image._getexif().items())

if exif[orientation] == 3:
image = image.rotate(180, expand=True)
elif exif[orientation] == 6:
image = image.rotate(270, expand=True)
elif exif[orientation] == 8:
image = image.rotate(90, expand=True)
# end restoring rotation issue

image.thumbnail(MAX_SIZE)
image.save(filename)
image.thumbnail(THUMB_SIZE)
image.save(thumbname)
