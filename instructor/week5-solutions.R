# Run from repository root: Rscript instructor/week5-solutions.R
# Reference computations; remote access requires the actual service guide.
suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
})
root <- normalizePath(getwd())
out <- file.path(root, "output", "instructor-week5")
dir.create(out, recursive = TRUE, showWarnings = FALSE)

# Day 21: validate portable inputs; a local test cannot verify SSH/desktop access.
stopifnot(file.exists("data/seedlings.csv"), file.exists("report.Rmd"))

# Day 22: the supplied representation demonstration.
dna <- readLines("data/dna.txt")
bases <- strsplit(dna, split = "")[[1]]
print(table(bases))
stopifnot(length(dna) == 1, nchar(dna) == 40, length(bases) == 40,
          identical(as.integer(table(bases)), c(11L, 9L, 9L, 11L)))
pixels <- as.matrix(read.csv("data/pixels.csv"))
stopifnot(identical(dim(pixels), c(8L, 8L)),
          sum(pixels > 100) == 24, mean(pixels > 100) == 0.375,
          sum(pixels > 50) == 24, sum(pixels > 220) == 0)
png(file.path(out, "pixel-demonstration.png"), width = 500, height = 500)
plot.new()
rasterImage(as.raster(pixels / 255), 0, 0, 1, 1)
invisible(dev.off())

# Day 23: available measurements and an explicitly directed Welch comparison.
duckweed <- read_csv("data/duckweed.csv", show_col_types = FALSE)
summary_table <- duckweed |>
  group_by(treatment) |>
  summarise(n_started = n(), n_available = sum(!is.na(biomass_mg)),
            n_missing = sum(is.na(biomass_mg)),
            mean_mg = mean(biomass_mg, na.rm = TRUE),
            sd_mg = sd(biomass_mg, na.rm = TRUE), .groups = "drop")
available <- duckweed |> filter(!is.na(biomass_mg))
nutrient <- available |> filter(treatment == "nutrient")
control <- available |> filter(treatment == "control")
comparison <- t.test(nutrient$biomass_mg, control$biomass_mg)
difference_mg <- mean(nutrient$biomass_mg) - mean(control$biomass_mg)
stopifnot(nrow(duckweed) == 20, anyDuplicated(duckweed$flask_id) == 0,
          nrow(nutrient) == 9, nrow(control) == 10,
          is.na(duckweed$biomass_mg[duckweed$flask_id == "F17"]))
print(summary_table)
print(difference_mg)
print(comparison)
write_csv(summary_table, file.path(out, "duckweed-summary.csv"))

# An instructor-only complete report, with all required code in the source.
source_file <- file.path(out, "duckweed-report.Rmd")
writeLines(c(
  '---', 'title: "Duckweed biomass: worked teaching example"',
  'output: html_document', '---', '',
  '# Question and design', '',
  'These simulated teaching data describe 20 separate flasks of duckweed.',
  'Ten flasks were randomly assigned additional nutrients and ten were controls.',
  'Dry biomass was measured after seven days. The independent unit is the flask.',
  'F17 was spilled before weighing and has no biomass measurement.', '',
  '# Methods', '',
  'We summarised available measurements and compared nutrient minus control',
  'mean biomass with an independent Welch two-sample t-test. Flasks are treated',
  'as independent. With these small samples, normal-approximation results remain',
  'conditional on the distributional assumptions and quality of the design.', '',
  '```{r setup, include=FALSE}',
  'library(readr)', 'library(dplyr)', 'library(ggplot2)', '```', '',
  '```{r data}',
  'duckweed <- read_csv("data/duckweed.csv", show_col_types = FALSE)',
  'available <- duckweed |> filter(!is.na(biomass_mg))',
  'group_summary <- duckweed |> group_by(treatment) |>',
  '  summarise(n_available = sum(!is.na(biomass_mg)),',
  '            n_missing = sum(is.na(biomass_mg)),',
  '            mean_mg = mean(biomass_mg, na.rm = TRUE),',
  '            sd_mg = sd(biomass_mg, na.rm = TRUE), .groups = "drop")',
  'nutrient <- available |> filter(treatment == "nutrient")',
  'control <- available |> filter(treatment == "control")',
  'comparison <- t.test(nutrient$biomass_mg, control$biomass_mg)',
  'difference_mg <- mean(nutrient$biomass_mg) - mean(control$biomass_mg)', '```', '',
  '# Results', '', '```{r summary}',
  'knitr::kable(group_summary, digits = 2)', '```', '',
  '```{r figure, fig.cap="Each point is an independent flask. One nutrient flask has unavailable biomass following a spill and is not plotted."}',
  'ggplot(available, aes(treatment, biomass_mg)) +',
  '  geom_point(position = position_jitter(width = 0.08, height = 0, seed = 23)) +',
  '  labs(x = "Nutrient allocation", y = "Dry biomass after seven days (mg)") +',
  '  theme_minimal()', '```', '',
  'The estimated nutrient-minus-control mean difference was',
  '`r round(difference_mg, 2)` mg (95% confidence interval',
  '`r round(comparison$conf.int[1], 2)` to `r round(comparison$conf.int[2], 2)` mg;',
  'Welch p = `r signif(comparison$p.value, 3)`).', '',
  '# Interpretation', '',
  'The nutrient flasks had greater mean observed biomass. Individual values',
  'overlap, and the interval represents uncertainty in a mean difference, not',
  'spread of individual flask values. The p-value is interpreted under an',
  'equal-means model and its assumptions, not as a probability of that model.',
  'F17 could not contribute to the estimate; generalisation is conditional on',
  'the loss not distorting the available comparison. This small simulated study',
  'does not establish an effect for all nutrient formulations or growth conditions.'
), source_file)
rmarkdown::render(source_file, output_dir = out, knit_root_dir = root,
                  envir = new.env(parent = globalenv()), quiet = TRUE)

# Day 25: the repaired growth calculation.
seedlings <- read_csv("data/seedlings.csv", show_col_types = FALSE) |>
  mutate(growth_mm = final_mm - initial_mm)
stopifnot(abs(seedlings$growth_mm[seedlings$plant_id == "P01"] - 18.6) < 1e-10)
cat("Week 5 reference computations and report passed. Artifacts:", out, "\n")
