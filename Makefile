install:
	# Install the dependencies to execute the project.
	pip install -r requirements.txt

test:
	# Execute the tests for the project classes.
	python3 -B -m pytest --disable-warnings tests/test_data_analyzer.py
	# Coverage tests
	# --cov-report=html
	python3 -B -m pytest --disable-warnings --cov=api --cov=commondata --cov=mongodb \
	--cov=postgredb --cov=main_ops --cov=data_analyzer tests/*