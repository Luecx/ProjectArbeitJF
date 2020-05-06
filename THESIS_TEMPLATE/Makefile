# Kleines Makefile zum Erzeugen eines
# PDF-Dokumentes aus einer Latex-Datei.

DOKUMENT = Preambel_main

all: $(DOKUMENT).pdf

$(DOKUMENT).pdf: $(DOKUMENT).tex
	pdflatex $(DOKUMENT).tex
	Biber $(DOKUMENT)
	pdflatex $(DOKUMENT).tex
	pdflatex $(DOKUMENT).tex
	open $(DOKUMENT).pdf	
#======================================================================
#	aufraeumen
#======================================================================
clean:
	@echo '---------------------------------------------------'
	@echo 'loesche erstellten Dateien'
	@echo '---------------------------------------------------'
	@rm -f *.aux # LaTeX Zwischendateien
	@rm -f *.log
	@rm -f *.toc
	@rm -f *.out
	@rm -f *.dvi
	@rm -f *.blg
	@rm -f *.bbl
	@rm -f *.acn
	@rm -f *.bcf
	@rm -f *.ist
	@rm -f *.syg1
	@rm -f *.syg2
	@rm -f *.run.*
	@rm -f $(DOKUMENT).ps  # Postscript-Dokument
#	@rm -f $(DOKUMENT).pdf # PDF-Dokument
	@rm -f $(DOKUMENT).tpt # Thumbnails von ThumbPDF
	@rm -f *.gxg # Log-Datei von GlossTeX
	@rm -f *.gxs # Indexdatei von GlossTeX
	@rm -f $(DOKUMENT).ilg # Log-Datei von Makeindex
	@rm -f $(DOKUMENT).glx # das fertige Glossar
	@rm -f $(DOKUMENT).brf # backref
	@rm -f *.lof # List of figures
	@rm -f *.lot # List of tables
#	@rm -f *.lo? # List of <any> and Log-Dateien löschen 
#			(z.B. loa -> List of Algorithms)
# ENDE
