.PHONY: install test test-cov lint serve demo clean check

PYTHON ?= python3
PIP ?= $(PYTHON) -m pip
PYTEST ?= $(PYTHON) -m pytest

install:
	$(PIP) install -e '.[dev]'

test:
	$(PYTEST) -v

test-cov:
	$(PYTEST) --cov=octo_harness --cov-report=term-missing --cov-report=html

lint:
	$(PYTHON) -m py_compile src/octo_harness/*.py src/octo_harness/*/*.py

serve:
	$(PYTHON) -m uvicorn octo_harness.server.app:app --host 0.0.0.0 --port 8000 --reload

demo:
	$(PYTHON) examples/basic_routing.py
	$(PYTHON) examples/grok_chatgpt_fallback.py
	$(PYTHON) examples/cowork_multi_agent.py

check: lint test

clean:
	rm -rf .pytest_cache .coverage htmlcov __pycache__ build dist *.egg-info src/*.egg-info
