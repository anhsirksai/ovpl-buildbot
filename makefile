run:
	./buildbot.py

clean:
	rm  *.pyc
	rm log/*

install: deps
	chmod +x buildbot.py

deps:
	pip install logutils
