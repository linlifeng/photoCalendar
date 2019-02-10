#sudo cp $1 image.jpg;
#sudo convert -blur 0x8 image.jpg image-blur.jpg;
#sudo convert image-blur.jpg -fill white -colorize 50%  image-blur-whiten.jpg;
#sudo mv image-blur-whiten.jpg image-blur.jpg;

cp $1 image.jpg;
convert -blur 0x8 image.jpg image-blur.jpg;
convert image-blur.jpg -fill white -colorize 50%  image-blur-whiten.jpg;
mv image-blur-whiten.jpg image-blur.jpg;

#uncomment the following for brightness options. Sometimes the effect is strange.
#sudo convert -modulate  200% image-blur.jpg image-blur-light.jpg;
#sudo mv image-blur-light.jpg image-blur.jpg;
