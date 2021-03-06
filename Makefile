# The name of the project is used throughout the makefile to provide
# project-specific docker containers.
PROJNAME = rehabradio


help:
	@echo "build - Build container"
	@echo "start - Start container $(PROJNAME)"
	@echo "resume - Resume container $(PROJNAME)"
	@echo "run - Run container and start database and web server (non-interactive)"
	@echo "test - Run container and run test suite (non-interactive)"

build:
	cd docker; docker build -t="rehabstudio/$(PROJNAME)" .

start: build
	docker run -t -i --workdir="/app" --name="$(PROJNAME)" -v "$(CURDIR)/app:/app" -p 0.0.0.0:8000:8000 rehabstudio/$(PROJNAME)

resume:
	docker start -i $(PROJNAME)

run: build
	docker run --rm -t -v "$(CURDIR)/app:/app" -p 0.0.0.0:8000:8000 rehabstudio/$(PROJNAME) make -C /app run

test: build
	docker run --rm -t -v "$(CURDIR)/app:/app" -p 0.0.0.0:8000:8000 rehabstudio/$(PROJNAME) make -C /app test
