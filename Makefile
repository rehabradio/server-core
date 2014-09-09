help:
	@echo "build-test - Build container in test mode"
	@echo "build-local - Build container for local development"
	@echo "build-deploy - Build container in production mode"
	@echo "run-test - Run container for in test mode"
	@echo "run-local - Run container for local development"
	@echo "run-deploy - Run container for in production mode"

build-base:
	cd ops/base/; docker build -t="rehabstudio/python-base" .

build-test: build-base
	cd ops/test/; docker build -t="rehabstudio/python-test" .

build-local: build-base
	cd ops/local/; docker build -t="rehabstudio/python-local" .

build-deploy: build-base
	cd ops/deploy/; docker build -t="rehabstudio/python-deploy" .

run-test: build-test
	docker run -P -t -i -v $(CURDIR)/app:/opt/app rehabstudio/python-test

run-local: build-local
	docker run -P -t -i -v $(CURDIR)/app:/opt/app rehabstudio/python-local

run-deploy: build-deploy
	docker run -P -t -i -v $(CURDIR)/app:/opt/app rehabstudio/python-deploy