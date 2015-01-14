VENV_PREFIX = foreman run /opt/venv/bin/

help:
	@echo "db_start - start postgres server"
	@echo "clean - remove build artifacts"
	@echo "run - run the local development server for testing/debugging purposes"
	@echo "test - run all of the app's tests and print a coverage report"

db_start:
	# Start the database server
	/etc/init.d/postgresql start

clean:
	# remove build artifacts from tree
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -empty -type d -delete
	@-rm -R htmlcov
	@-rm .coverage
	@-rm coverage.xml
	@-rm nosetests.xml

run: clean db_start
	# run the development server
	$(VENV_PREFIX)python manage.py makemigrations
	$(VENV_PREFIX)python manage.py migrate
	$(VENV_PREFIX)python manage.py runserver 0.0.0.0:8000

test: clean db_start
	# run tests with a coverage report
	$(VENV_PREFIX)python manage.py makemigrations
	$(VENV_PREFIX)python manage.py migrate
	$(VENV_PREFIX)coverage erase
	$(VENV_PREFIX)coverage run --source='.' manage.py test apps radio
	$(VENV_PREFIX)coverage report -m
	$(VENV_PREFIX)coverage xml
