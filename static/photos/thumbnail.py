from sys import argv
from PIL import Image
import os

filename = argv[1]
thumbname = 'thumb-' + os.path.basename(filename)
image = Image.open(filename)
MAX_SIZE = (1200, 800)
THUMB_SIZE = (200, 200)
image.thumbnail(MAX_SIZE)
image.save(filename)
image.thumbnail(THUMB_SIZE)
image.save(thumbname)
