FROM python:3.10-buster
COPY requirements.txt requirements.txt
COPY google.json google.json
COPY setup.py setup.py
RUN pip install .
COPY uk_election uk_election/
CMD uvicorn uk_election.api.fast:app --host 0.0.0.0 --port $PORT
