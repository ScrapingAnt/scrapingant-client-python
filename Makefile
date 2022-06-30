init:
	pip3 install -e .[dev,async]

test:
	pytest -p no:cacheprovider

lint:
	flake8 --max-line-length=120 scrapingant_client tests

