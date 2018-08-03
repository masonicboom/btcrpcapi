all: index.html style.css

style.css: generate-style.py
	./$< > $@

index.html: generate-index.py apis/
	./$< > $@

apis: dumpapis.sh dumpapi.py bitcoin
	mkdir -p $@
	./$<

bitcoin:
	git clone https://github.com/bitcoin/bitcoin.git

clean:
	rm -rf apis/
	rm -rf docs/
	rm -f index.html
	rm -f style.css