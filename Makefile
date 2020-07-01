install:
	# Install the dependencies to execute the project.
	pip install -r requirements.txt

test:
	# Execute the tests for the project classes.
	python3 -B -m pytest --disable-warnings tests/*
	# Coverage tests.
	## --cov-report=html
	python3 -B -m pytest --disable-warnings --cov=mongodb \
    	--cov=postgresql --cov=commondata --cov=main_ops --cov=api tests/