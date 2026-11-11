# Pictures REST API

IBM Back-end Application Development Capstone implementation by Dias Nygman, based on the IBM Skills Network starter (Apache 2.0). AI assistance was used for implementation and testing.

## Features
Health and count endpoints; list, retrieve, create, update and delete pictures. Duplicate IDs and missing records are handled explicitly.

## Run
Install Flask and pytest in a Python virtual environment, then run `python app.py`. Run the official test suite with `python -m pytest -v`.

## Validation
All 11 provided tests passed locally on Python 3.12 with Flask 3.1.3. Pictures use an in-memory list and reset when the process restarts.
