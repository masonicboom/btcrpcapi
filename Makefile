all: index.html style.css cats/ tags/

style.css: generate-style.py
	./$< > $@

index.html: generate-index.py apis/ docs/
	./$< > $@

tags: generate-tag-indexes.sh generate-tag-index.py
	mkdir -p $@
	./$<

cats: generate-cats.sh generate-index.py
	./$<

docs: generate-docs.sh docdata/
	./$<

apis: dump-apis.sh dump-api.py bitcoin
	mkdir -p $@
	./$<

docdata: dump-apis.sh dump-docs.py bitcoin apis/
	mkdir -p $@
	./$<

bitcoin:
	git clone https://github.com/bitcoin/bitcoin.git

clean:
	rm -rf apis/
	rm -rf docs/
	rm -rf docdata/
	rm -rf cats/
	rm -rf tags/
	rm -f index.html
	rm -f style.css
