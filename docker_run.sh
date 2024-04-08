docker build -t lele-calendar .
docker run \
	-p8080:8080 \
	-v $(pwd)/static/photos:/home/app/static/photos \
	-v $(pwd)/static/diary:/home/app/static/diary \
	lele-calendar:latest
