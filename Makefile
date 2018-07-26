index.html: analyze.py apis
	./$< > $@

apis: dumpapis.sh dumpapi.py bitcoin
	mkdir -p $@
	./$<

bitcoin:
	git clone https://github.com/bitcoin/bitcoin.git