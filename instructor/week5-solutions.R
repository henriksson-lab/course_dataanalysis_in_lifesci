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

# Day 23 organic-laboratory alternative: descriptive, one outcome per run.
organic <- read_csv("data/organic-recovery.csv", show_col_types = FALSE) |>
  mutate(yield_percent = 100 * isolated_mass_g / theoretical_mass_g)
organic_summary <- organic |>
  group_by(protocol) |>
  summarise(n = n(), mean_yield_percent = mean(yield_percent),
            sd_percentage_points = sd(yield_percent), .groups = "drop")
standard_yield <- organic |> filter(protocol == "standard") |> pull(yield_percent)
modified_yield <- organic |> filter(protocol == "modified") |> pull(yield_percent)
organic_difference_pp <- mean(modified_yield) - mean(standard_yield)
stopifnot(nrow(organic) == 12, anyDuplicated(organic$run_id) == 0,
          !anyNA(organic), all(organic$theoretical_mass_g > 0),
          all(organic$yield_percent >= 0 & organic$yield_percent <= 100),
          length(standard_yield) == 6, length(modified_yield) == 6,
          abs(organic$yield_percent[organic$run_id == "Y01"] - 62) < 1e-10,
          abs(mean(standard_yield) - 68.6666666667) < 1e-8,
          abs(mean(modified_yield) - 77) < 1e-10,
          abs(sd(standard_yield) - 4.320493799) < 1e-8,
          abs(sd(modified_yield) - 3.741657387) < 1e-8,
          abs(organic_difference_pp - 8.3333333333) < 1e-8)
print(organic_summary)
print(organic_difference_pp)
write_csv(organic_summary, file.path(out, "organic-summary.csv"))
organic_plot <- ggplot(organic, aes(protocol, yield_percent)) +
  geom_point(position = position_jitter(width = 0.08, height = 0, seed = 23)) +
  labs(x = "Protocol label", y = "Isolated product yield (%)") + theme_minimal()
ggsave(file.path(out, "organic-yields.png"), organic_plot, width = 6, height = 4)

# Complete alternative report: no confidence interval or test is required.
organic_source <- file.path(out, "organic-study.Rmd")
writeLines(c(
  '---', 'title: "Product yield: a descriptive teaching study"',
  'output: html_document', '---', '',
  '# Question and context', '',
  'How does percentage product yield vary among runs and between protocol labels?',
  'These simulated data describe 12 independently performed synthesis runs, six',
  'randomly assigned each protocol. Theoretical mass is the supplied maximum',
  'product mass for each run. Isolated mass is collected dry product, assumed',
  'pure only for this simplified exercise. No reaction equation is needed.', '',
  '# Methods and checks', '',
  'Yield (%) = 100 times isolated mass (g) divided by theoretical mass (g).',
  'Because starting scales differ, yields are compared instead of raw masses.',
  'The independent unit is the synthesis run, not a repeat weighing.', '',
  '```{r setup, include=FALSE}',
  'library(readr)', 'library(dplyr)', 'library(ggplot2)', '```', '',
  '```{r import}',
  'organic <- read_csv("data/organic-recovery.csv", show_col_types = FALSE)',
  'nrow(organic)', 'anyDuplicated(organic$run_id)',
  'organic |> count(protocol)', 'sum(is.na(organic))',
  'all(organic$theoretical_mass_g > 0)',
  'organic <- organic |>',
  '  mutate(yield_percent = 100 * isolated_mass_g / theoretical_mass_g)',
  'group_summary <- organic |> group_by(protocol) |>',
  '  summarise(n = n(), mean_yield_percent = mean(yield_percent),',
  '            sd_percentage_points = sd(yield_percent), .groups = "drop")',
  'modified_mean <- group_summary$mean_yield_percent[group_summary$protocol == "modified"]',
  'standard_mean <- group_summary$mean_yield_percent[group_summary$protocol == "standard"]',
  'difference_pp <- modified_mean - standard_mean', '```', '',
  'There were `r nrow(organic)` unique runs and no missing measurements.', '',
  '# Results', '', '```{r table}',
  'knitr::kable(group_summary, digits = 2,',
  '  caption = "Means in percent; SD in percentage points.")', '```', '',
  '```{r figure, fig.cap="Each point is one independent synthesis run. Horizontal displacement only separates overlapping points."}',
  'ggplot(organic, aes(protocol, yield_percent)) +',
  '  geom_point(position = position_jitter(width = 0.08, height = 0, seed = 23)) +',
  '  labs(x = "Protocol label", y = "Isolated product yield (%)") + theme_minimal()',
  '```', '',
  'The observed modified-minus-standard mean difference was',
  '`r round(difference_pp, 2)` percentage points. The groups overlap.', '',
  '# Interpretation and limitations', '',
  'The modified protocol had a higher observed mean yield in these simulated',
  'runs. SD describes variation among runs, not uncertainty in a protocol effect.',
  'This is a descriptive comparison without a hypothesis test or confidence',
  'interval. The simplified purity assumption is not a purity measurement.',
  'Yield alone does not establish purity, safety, sustainability, or general',
  'superiority, and these teaching data are not evidence for a real process.'
), organic_source)
rmarkdown::render(organic_source, output_dir = out, knit_root_dir = root,
                  envir = new.env(parent = globalenv()), quiet = TRUE)

# Day 25: the repaired growth calculation.
seedlings <- read_csv("data/seedlings.csv", show_col_types = FALSE) |>
  mutate(growth_mm = final_mm - initial_mm)
stopifnot(abs(seedlings$growth_mm[seedlings$plant_id == "P01"] - 18.6) < 1e-10)
cat("Week 5 reference computations and report passed. Artifacts:", out, "\n")
