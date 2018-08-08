all: index.html style.css cats/

style.css: generate-style.py
	./$< > $@

index.html: generate-index.py apis/ docs/
	./$< > $@

cats: generate-cats.sh generate-index.py
	./$<

docs: generate-docs.sh docdata/
	./$<

apis: dumpapis.sh dumpapi.py bitcoin
	mkdir -p $@
	./$<

docdata: dumpapis.sh dumpdocs.py bitcoin apis/
	mkdir -p $@
	./$<

bitcoin:
	git clone https://github.com/bitcoin/bitcoin.git

clean:
	rm -rf apis/
	rm -rf docs/
	rm -rf docdata/
	rm -rf cats/
	rm -f index.html
	rm -f style.css
