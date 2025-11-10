DOCTYPE = RTN
DOCNUMBER = 011
DOCNAME = $(DOCTYPE)-$(DOCNUMBER)

tex = $(filter-out $(wildcard *acronyms.tex) , $(wildcard *.tex))

GITVERSION := $(shell git log -1 --date=short --pretty=%h)
GITDATE := $(shell git log -1 --date=short --pretty=%ad)
GITSTATUS := $(shell git status --porcelain)
ifneq "$(GITSTATUS)" ""
        GITDIRTY = -dirty
endif

export TEXMFHOME ?= lsst-texmf/texmf

# ---------- Mermaid setup ----------
MMDC = mmdc
SVG2PDF = inkscape
MMD_DIR = diagrams
FIG_DIR = figures
MMD_SRC = $(wildcard $(MMD_DIR)/*.mmd)
MMD_PDF = $(patsubst $(MMD_DIR)/%.mmd,$(FIG_DIR)/%.pdf,$(MMD_SRC))

# Generate SVG from Mermaid source (already tightly cropped)
$(MMD_DIR)/%.svg: $(MMD_DIR)/%.mmd
	@echo "Generating SVG: $< → $@"
	$(MMDC) -i $< -o $@ -b transparent -t neutral

# Convert SVG → PDF (preserve bounding box)
$(MMD_DIR)/%.pdf: $(MMD_DIR)/%.svg
	@echo " Converting SVG → PDF: $< → $@"
	@if command -v inkscape >/dev/null 2>&1; then \
	  echo "   using Inkscape..."; \
	  inkscape "$<" --export-type=pdf --export-filename="$@"; \
	elif command -v rsvg-convert >/dev/null 2>&1; then \
	  echo "   using rsvg-convert..."; \
	  rsvg-convert -f pdf -o "$@" "$<"; \
	else \
	  echo "Error: neither inkscape nor rsvg-convert found in PATH"; \
	  exit 1; \
	fi

# Add aglossary.tex as a dependancy here if you want a glossary (and remove acronyms.tex)
$(DOCNAME).pdf: $(tex) meta.tex local.bib acronyms.tex authors.tex
	@echo "Building LaTeX document: $(DOCNAME).pdf"
	latexmk -bibtex -xelatex -f $(DOCNAME)
#       makeglossaries $(DOCNAME)
#       xelatex $(SRC)
# For glossary uncomment the 2 lines above

authors.tex:  authors.yaml
	python3 $(TEXMFHOME)/../bin/db2authors.py -m lsstdoc > authors.tex

# Acronym tool allows for selection of acronyms based on tags - you may want more than DM
acronyms.tex: $(tex) myacronyms.txt
	$(TEXMFHOME)/../bin/generateAcronyms.py -t "DM" $(tex)


# If you want a glossary you must manually run generateAcronyms.py  -gu to put the \gls in your files.
aglossary.tex :$(tex) myacronyms.txt
	generateAcronyms.py  -g $(tex)


.PHONY: clean
clean:
	latexmk -c
	rm -f $(DOCNAME).bbl
	rm -f $(DOCNAME).out
	rm -f $(DOCNAME).dvi
	rm -f $(DOCNAME).xdv
	rm -f $(DOCNAME).pdf
	rm -f meta.tex

.FORCE:

meta.tex: Makefile .FORCE
	rm -f $@
	touch $@
	echo '% GENERATED FILE -- edit this in the Makefile' >>$@
	printf '\\newcommand{\\lsstDocType}{$(DOCTYPE)}\n' >>$@
	printf '\\newcommand{\\lsstDocNum}{$(DOCNUMBER)}\n' >>$@
	printf '\\newcommand{\\vcsRevision}{$(GITVERSION)$(GITDIRTY)}\n' >>$@
	printf '\\newcommand{\\vcsDate}{$(GITDATE)}\n' >>$@
