# Validate the student archive as a fresh extracted project, not repository state.
project_parent <- tempfile("introcomputing-project-")
dir.create(project_parent)
unzip("downloads/course-files.zip", exdir = project_parent)
project <- file.path(project_parent, "introcomputing-course")
stopifnot(file.exists(file.path(project, "report.Rmd")),
          file.exists(file.path(project, "data", "seedlings.csv")))
rmarkdown::render(file.path(project, "report.Rmd"), quiet = TRUE,
                  envir = new.env(parent = globalenv()))
stopifnot(file.exists(file.path(project, "report.html")))
cat("Student starter report rendered from a freshly extracted project.\n")
