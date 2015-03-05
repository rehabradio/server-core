help:
	@echo "db_start - start postgres server"
	@echo "clean - remove build artifacts"
	@echo "run - run the local development server for testing/debugging purposes"
	@echo "test - run all of the app's tests and print a coverage report"

clean:
	# remove build artifacts from tree
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -empty -type d -delete

run: clean
	# run the development server
	foreman run python manage.py makemigrations
	foreman run python manage.py migrate
	foreman run python manage.py runserver 0.0.0.0:8000

test: clean
	# run tests with a coverage report
	foreman run python manage.py makemigrations
	foreman run python manage.py migrate
	foreman run coverage erase
	foreman run coverage run --source='.' manage.py test apps radio
	foreman run coverage report -m
	foreman run coverage xml
