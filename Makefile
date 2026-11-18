.PHONY: render preview downloads check figures

render: downloads
	quarto render
	@touch docs/.nojekyll

preview:
	quarto preview

downloads:
	python3 tools/package_downloads.py

check: downloads
	Rscript instructor/week2-solutions.R
	Rscript instructor/week3-solutions.R
	Rscript instructor/week4-solutions.R
	Rscript instructor/week5-solutions.R
	Rscript tools/check_report.R
	python3 tools/check_course.py

figures:
	Rscript instructor/week2-solutions.R --figures
	Rscript instructor/week3-solutions.R --figures
	Rscript instructor/week4-solutions.R --figures
