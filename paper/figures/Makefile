all: pics

# Optionally some PICS could be ignored. By default XXX ones.
# PICS_IGNORE must contain a rule for grep
PICS_IGNORE ?= " "

# For every .svg we must have a pdf
PICS=$(shell find . -iname \*svg \
	| sed -e 's/svg/pdf/g' -e 's/\([^\]\)\([ \t:]\)/\1\\\\\2/g' \
	| grep -v -e $(PICS_IGNORE) )

pics: $(PICS)
	echo $(PICS)

clean:
	for p in *.svg; do rm -f $${p%*.svg}.eps $${p%*.svg}.pdf; done
	-rm -rf *_300dpi.png

.PHONY: ignore-%
ignore-%:
	@grep -q "^$*$$" .gitignore || { \
	  echo "$*" >> .gitignore; echo "Ignore $@"; }

#
# Inkscape rendered figures
#
# alternative calls are for Inkscape v1.0 or later
%.pdf: %.svg ignore-%.pdf
	@echo "Rendering $@"
	@inkscape -z -f "$<" -A "$@" || inkscape --export-filename="$@" "$<" 

%.eps: %.svg ignore-%.eps
	@echo "Rendering $@"
	@inkscape -z -f "$<" -A "$@" || inkscape --export-filename="$@" "$<" 

%_300dpi.png: %.svg ignore-%_300dpi.png
	@echo "Rendering $@"
	@inkscape -z -f "$<" -e "$@" -d 300 || inkscape -d 300 --export-filename="$@" "$<" 

.PHONY: all pics
