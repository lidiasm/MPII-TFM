install:
	# Install the dependencies to execute the project.
	pip install -r requirements.txt

test:
	# Execute the tests for the project classes.
	python3 -B -m pytest tests/*
	# Coverage tests.
	python3 -B -m pytest --cov=commondata tests/