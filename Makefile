#!/usr/bin/make -f

build/venv/bin/activate:
	mkdir -p docs build
	virtualenv -p python3 build/venv
	sh -c '. $(CURDIR)/build/venv/bin/activate; pip install -r build-requirements.txt; pip install -e .'

rst: build/venv/bin/activate
	sh -c '. $(CURDIR)/build/venv/bin/activate; sphinx-apidoc -o $(CURDIR)/sphinx -e $(CURDIR)/bjarkan'

docs: build/venv/bin/activate rst
	mkdir -p docs
	sh -c '. $(CURDIR)/build/venv/bin/activate; make -C sphinx html'

clean:
	sh -c '. $(CURDIR)/build/venv/bin/activate; make -C sphinx clean'
	rm -rf \
		$(CURDIR)/sphinx/_autosummary \
		$(CURDIR)/docs \
		$(CURDIR)/sphinx/*.rst \
		$(CURDIR)/build/venv

.PHONY: docs clean rst

