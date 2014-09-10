help:
	@echo "build-test - Build container in test mode"
	@echo "run-test - Run container for in test mode"

build-base:
	docker build -t="rehabstudio/python-base" .

run-test: build-base
	docker run -P -t -i -v $(CURDIR)/app:/opt/app rehabstudio/python-base
