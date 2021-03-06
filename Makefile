.PHONY: install
install:
	@python setup.py develop

.PHONY: pep8
pep8:
	@flake8 pychecko --ignore=F401

.PHONY: pychecko_package
pychecko_package:
	@cd etc/pycheco_package; python setup.py install

.PHONY: test
test: pep8 pychecko_package
	@py.test tests -s -vv --cov --cov-config=.coveragerc --doctest-modules pychecko

.PHONY: sdist
sdist: test
	@python setup.py sdist bdist_wheel upload

.PHONY: clean
clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
