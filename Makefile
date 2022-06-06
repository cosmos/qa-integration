install-deps:
	bash ./deps/prereq.sh

lint: install-deps
	pylint ./python-qa-tools