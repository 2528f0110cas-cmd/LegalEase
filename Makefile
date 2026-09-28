install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

backend:
	python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

frontend:
	python -m streamlit run frontend/app.py

test:
	python -m pytest -q
