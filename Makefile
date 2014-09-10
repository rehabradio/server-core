# The name of the project is used throughout the makefile to provide
# project-specific docker containers.
PROJNAME = rehabradio


help:
	@echo "build - Build container"
	@echo "run - Run container"

build:
	docker build -t="rehabstudio/$(PROJNAME)" .

run: build
	docker run -t -i -v "$(CURDIR)/app:/app" -p 0.0.0.0:8000:8000 rehabstudio/$(PROJNAME)
