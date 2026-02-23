.PHONY: build clean

build:
	python3 site/build.py

clean:
	rm -rf site/output/
