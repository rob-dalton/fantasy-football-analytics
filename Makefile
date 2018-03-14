TESTS=$(wildcard tests/*.py)

.PHONY: test
test:	
	@- $(foreach TEST,$(TESTS), \
			echo === Running test: $(TEST); \
			python -m unittest $(TEST); \
		)

test_scraper:
	python -m unittest tests/roster_scraper.py
