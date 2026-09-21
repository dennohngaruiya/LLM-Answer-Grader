.PHONY: help test demo html json clean

help:
	@echo "make test   - run the unit tests"
	@echo "make demo   - grade the sample cases and print the markdown report"
	@echo "make html   - write report.html (self-contained, open in a browser)"
	@echo "make json   - write report.json (machine readable)"
	@echo "make clean  - remove generated reports"

test:
	python3 -m unittest discover -s tests -v

demo:
	python3 -m grader evaluate data/sample_outputs.json

html:
	python3 -m grader evaluate data/sample_outputs.json --html report.html
	@echo "wrote report.html"

json:
	python3 -m grader evaluate data/sample_outputs.json --json report.json
	@echo "wrote report.json"

clean:
	rm -f report.html report.json report.md
	find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
