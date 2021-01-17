install:
	# Install the dependencies to execute the project.
	pip install -r requirements.txt

test:
	# Execute the tests for the project classes.
	python3 -B -m pytest --disable-warnings tests/test_api.py tests/test_commondata.py \
	tests/test_data_analyzer.py tests/test_mongodb.py tests/test_postgredb.py

	# Coverage tests
	# For storing the coverage reports in a HTML: --cov-report=html
	python3 -B -m pytest --disable-warnings --cov=api --cov=commondata --cov=data_analyzer \
		--cov=mongodb --cov=postgredb tests/test_api.py tests/test_commondata.py \
		tests/test_data_analyzer.py tests/test_mongodb.py tests/test_postgredb.py
