run-debug:
	./buildbot.py --debug

run-release:
	./buildbot.py

#helpers
clean:
	rm  *.pyc
	rm log/*

install: deps
	chmod +x buildbot.py

deps:
	pip2.7 install logutils flask requests plumbum IPy tornado netaddr pymongo sh 

	#install pygit (https://github.com/libgit2/pygit2)
	#install libgit2
	#pip2.7 install cffi
	#pip2.7 pygit2
