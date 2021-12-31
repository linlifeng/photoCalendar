docker build -t lele-calendar .
docker run \
	-p5000:5000 \
	-v $(pwd)/static/photos:/home/app/static/photos \
	-v $(pwd)/static/diary:/home/app/static/diary \
	lele-calendar:latest
