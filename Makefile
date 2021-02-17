init:
	poetry update
test:
	poetry run pytest -p no:cacheprovider

flake8:
	poetry run flake8 --max-line-length=120 scrapingant_client_python tests

publish:
	poetry build
	poetry publish
