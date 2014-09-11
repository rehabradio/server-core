# The name of the project is used throughout the makefile to provide
# project-specific docker containers.
PROJNAME = rehabradio


help:
	@echo "build - Build container"
	@echo "start - Run container and start database server"
	@echo "run - Run container and start database and web server"
	@echo "test - Run container and run test suite"

build:
	cd docker; docker build -t="rehabstudio/$(PROJNAME)" .

start: build
	docker run --rm -t -i -v "$(CURDIR)/app:/app" -p 0.0.0.0:8000:8000 rehabstudio/$(PROJNAME)

run: build
	docker run --rm -t -i -v "$(CURDIR)/app:/app" -p 0.0.0.0:8000:8000 rehabstudio/$(PROJNAME) make -C /app run

test: build
	docker run --rm -t -i -v "$(CURDIR)/app:/app" -p 0.0.0.0:8000:8000 rehabstudio/$(PROJNAME) make -C /app test
