all: index.html style.css docs/ cats/ tags/

style.css: generate-style.py
	./$< > $@

index.html: index.py bitdocs.db
	./$< bitdocs.db > $@

tags: generate-tag-indexes.py bitdocs.db
	./$< bitdocs.db

cats: generate-cats.py index.py bitdocs.db
	./$< bitdocs.db

docs: generate-docs.py bitdocs.db
	./$< bitdocs.db

bitdocs.db: load-docs.sh init-db.py
	./$<

bitcoin:
	git clone https://github.com/bitcoin/bitcoin.git

clean:
	rm bitdocs.db
	rm -rf docs/
	rm -rf cats/
	rm -rf tags/
	rm -f index.html
	rm -f style.css
