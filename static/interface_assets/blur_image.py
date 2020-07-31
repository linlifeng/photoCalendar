'''
1. image file path
'''
from PIL import Image, ImageFilter, ImageEnhance
from sys import argv
from os import path

try:
	image = Image.open(argv[1])
except IndexError:
	exit(__doc__)

outfile_path = path.splitext(argv[1])[0] + '-blur.jpg'
blurImage = image.filter(ImageFilter.GaussianBlur(radius=20))
enhancer = ImageEnhance.Brightness(blurImage)

blurImage = enhancer.enhance(1.5)

blurImage.save(outfile_path)

