install:
	# Install the dependencies to execute the project.
	pip install -r requirements.txt

test:
	# Execute the tests for the project classes.
	python3 -B -m pytest --disable-warnings tests/*
	# Coverage tests.
	python3 -B -m pytest --disable-warnings --cov=api --cov=commondata --cov=mongodb tests/  #--cov-report=html