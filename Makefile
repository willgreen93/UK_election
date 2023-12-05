refresh-virtualenv:
	pip install -r requirements.txt

run_preprocess:
	python -c 'from uk_election.main import preprocess; preprocess()'
