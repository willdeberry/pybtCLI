#!/usr/bin/make -f

build/venv/bin/activate:
	mkdir -p docs build
	virtualenv -p python3 build/venv
	sh -c '. $(CURDIR)/build/venv/bin/activate; pip install -r build-requirements.txt; pip install -e .'

rst: build/venv/bin/activate
	sh -c '. $(CURDIR)/build/venv/bin/activate; sphinx-apidoc -o $(CURDIR)/sphinx -e $(CURDIR)/bjarkan'

tag:
	gbp buildpackage --git-tag-only --git-ignore-new

deb:
	gbp buildpackage -uc -us --lintian-opts --verbose --git-ignore-new

installnow: deb
	sudo dpkg -i ../$$( awk '{ print $$1 }' debian/files )

revbump:
	set -e ;\
		VERSION=$$( git tag | awk -F / '$$1=="debian"{print$$2}' | sort --version-sort | tail -1 | awk 'BEGIN{FS=OFS="."}{print $$1,$$2,$$3+1}' ) ;\
		gbp dch -N $$VERSION ;\
		git add debian/changelog ;\
		git diff --cached ;\
		git commit --edit --message "unstable release $$VERSION" ;\

minorbump:
	set -e ;\
		VERSION=$$( git tag | awk -F / '$$1=="debian"{print$$2}' | sort --version-sort | tail -1 | awk 'BEGIN{FS=OFS="."}{print $$1,$$2+1,0}' ) ;\
		gbp dch -N $$VERSION ;\
		git add debian/changelog ;\
		git diff --cached ;\
		git commit --edit --message "unstable release $$VERSION" ;\

majorbump:
	set -e ;\
		VERSION=$$( git tag | awk -F / '$$1=="debian"{print$$2}' | sort --version-sort | tail -1 | awk 'BEGIN{FS=OFS="."}{print $$1+1,0,0}' ) ;\
		gbp dch -N $$VERSION ;\
		git add debian/changelog ;\
		git diff --cached ;\
		git commit --edit --message "unstable release $$VERSION" ;\

release:
	set -e ;\
		VERSION=$$( grep --max-count=1 --only-matching --perl-regexp '(?<=\()[^)]+' debian/changelog ) ;\
		dch -r ignore ;\
		git add debian/changelog ;\
		git diff --cached ;\
		git commit --edit --message "release $$VERSION" ;\

docs: build/venv/bin/activate rst
	mkdir -p build docs
	sh -c '. $(CURDIR)/build/venv/bin/activate; make -C sphinx html'
	cp -r build/html/* docs/.
	ln -s bjarkan.html docs/index.html

clean:
	sh -c '. $(CURDIR)/build/venv/bin/activate; make -C sphinx clean'
	rm -rf \
		$(CURDIR)/sphinx/_autosummary \
		$(CURDIR)/docs \
		$(CURDIR)/sphinx/*.rst \
		$(CURDIR)/build/venv

.PHONY: tag deb installnow revbump minorbump majorbump release rst docs clean

