NAME ?= thy4869

all: build run

images:
	docker images | grep ${NAME}

ps:
	docker ps -a | grep ${NAME}

build:
	docker build -t ${NAME}/app:1.0 .

run:
	docker run --name "ISS_position_and_sighting_data_analysis_project" -d -p 5034:5000

push:
	docker push ${NAME}/app:1.0
