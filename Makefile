init: 
	pip3 install -r requirements.txt

run: 
	python3 game/main.py

doc: 	
	# requires pdoc3
	cd game
	pdoc --html --output-dir ../docs main game display missile platforms player scoreboard settings

clean:
	cd game
	rm -rf __pycache__

.PHONY: init run doc clean
