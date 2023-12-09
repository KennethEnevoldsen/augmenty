install:
	@echo "--- 🚀 Installing project ---"
	pip install -e ".[dev, docs, tests,tutorials,all,da]" 

static-type-check:
	@echo "--- 🔍 Running static type check ---"
	pyright src/
	pyright tests/

lint:
	@echo "--- 🧹 Running linters ---"
	pyproject-parser check pyproject.toml 		# check pyproject.toml
	ruff format .  								# running ruff formatting (.ipynb, .py)
	ruff **/*.py --fix  						# running ruff linting (.py)

test:
	@echo "--- 🧪 Running tests ---"
	pytest tests/

pr:
	@echo "--- 🚀 Running PR checks ---"
	make lint
	make static-type-check
	make test
	@echo "Ready to make a PR"

build-docs:
	@echo "--- 📚 Building docs ---"
	sphinx-build -b html docs docs/_build/html

view-docs:
	@echo "--- 👀 Viewing docs ---"
	open docs/_build/html/index.html
	
update-from-template:
	@echo "--- 🔄 Updating from template ---"
	@echo "This will update the project from the template, make sure to resolve any .rej files"
	cruft update --skip-apply-ask
	
