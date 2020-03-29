all: main.pdf

main.pdf: main.tex
	latexmk -pdf $<

clean:
	latexmk -C
	rm -f main.bbl

.PHONY: clean
