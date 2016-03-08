all: ldmc.pdf

ldmc.pdf: ldmc.tex ldmc.bib
	pdflatex ldmc.tex
	bibtex ldmc
	pdflatex ldmc.tex
	pdflatex ldmc.tex
