all: main.pdf

main.pdf: main.tex descr-stats-anno.tex descr-stats-regressors.tex
	latexmk -pdf -g $<

clean:
	latexmk -C
	rm -f main.aux main.bbl main.blg main.fb_latexmk main.fls main.log main.out
	$(MAKE) -C figures clean

figures:
	$(MAKE) -C figures


.PHONY: clean
