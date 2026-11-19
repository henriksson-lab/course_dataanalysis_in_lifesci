.PHONY: render preview downloads check figures lecture-figures

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
	Rscript instructor/transfer-data-checks.R
	Rscript tools/check_report.R
	python3 tools/check_course.py
	python3 tools/check_lectures.py
	python3 tools/check_quizzes.py
	python3 tools/check_expansion.py

figures:
	Rscript instructor/week2-solutions.R --figures
	Rscript instructor/week3-solutions.R --figures
	Rscript instructor/week4-solutions.R --figures

lecture-figures:
	python3 instructor/make-lecture-figures-weeks1-2.py
	python3 instructor/make-lecture-figures-weeks3-4.py
	python3 instructor/make-lecture-figures-week5.py
	python3 instructor/make-lecture-figures-intro.py
	python3 instructor/make-lecture-figures-days-4-5-24.py
	python3 instructor/make-lecture-figures-makeover-a.py
	python3 instructor/make-lecture-figures-makeover-b.py
	python3 instructor/make-lecture-figures-makeover-c.py
