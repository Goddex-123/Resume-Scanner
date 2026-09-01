.PHONY: install test lint format docker-build docker-run clean

install:
	pip install --upgrade pip
	pip install -r requirements.txt
	python -m nltk.downloader stopwords punkt

test:
	pytest tests/ -v

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=15 --max-line-length=127 --statistics

format:
	black .

docker-build:
	docker build -t resume-scanner .

docker-run:
	docker run -p 8501:8501 resume-scanner

clean:
	python -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]; [p.unlink(missing_ok=True) for p in pathlib.Path('.').rglob('*.py[co]')]; [shutil.rmtree(p, ignore_errors=True) for p in ['.pytest_cache', 'htmlcov']]; [p.unlink(missing_ok=True) for p in pathlib.Path('.').glob('.coverage*')]"
