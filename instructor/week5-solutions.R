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

# Day 21: how big is your data? Worked estimates checked against R.
# Sizes use 1 MB = 1e6 bytes. Object sizes are from object.size() (R >= 4.0).
x <- rnorm(1e6)
stopifnot(as.numeric(object.size(x)) == 8000048,
          format(object.size(x), units = "MB", standard = "SI") == "8 MB")
rm(x)
seedlings_raw <- read_csv("data/seedlings.csv", show_col_types = FALSE)
stopifnot(file.size("data/seedlings.csv") == 592, nrow(seedlings_raw) == 24,
          as.numeric(object.size(seedlings_raw)) > 2000)  # bookkeeping dominates
set.seed(21)
n <- 100000
big <- data.frame(matrix(round(rnorm(n * 10, mean = 20, sd = 4), 1), ncol = 10))
big_csv <- file.path(out, "big-measurements.csv")
write_csv(big, big_csv)
size_rounded <- c(file = file.size(big_csv) / 1e6, object = as.numeric(object.size(big)) / 1e6)
big_back <- read_csv(big_csv, show_col_types = FALSE)
big$sample_id <- sprintf("S%06d", 1:n)
write_csv(big, big_csv)
size_ids <- c(file = file.size(big_csv) / 1e6, object = as.numeric(object.size(big)) / 1e6,
              ids = as.numeric(object.size(big$sample_id)) / 1e6)
set.seed(21)
full_csv <- file.path(out, "unrounded-numbers.csv")
write_csv(data.frame(x = rnorm(1e6, 20, 4)), full_csv)
size_full <- file.size(full_csv) / 1e6
print(round(rbind(size_rounded, size_ids = size_ids[1:2]), 2))
stopifnot(round(size_rounded[["file"]], 2) == 4.79, round(size_rounded[["object"]], 2) == 8.00,
          round(as.numeric(object.size(big_back)) / 1e6, 1) == 8.0,
          round(size_ids[["file"]], 2) == 5.59, round(size_ids[["object"]], 1) == 14.4,
          round(size_ids[["ids"]], 1) == 6.4, round(size_full, 1) == 18.6,
          as.numeric(object.size(rep(c("treated", "control"), length.out = n))) < 1e6)
unlink(full_csv)
dna <- readLines("data/dna.txt")
bases <- strsplit(dna, split = "")[[1]]
print(table(bases))
stopifnot(length(dna) == 1, nchar(dna) == 40, file.size("data/dna.txt") == 41,
          length(bases) == 40, identical(as.integer(table(bases)), c(11L, 9L, 9L, 11L)),
          object.size(bases) > object.size(dna))
pixels <- as.matrix(read_csv("data/pixels.csv", show_col_types = FALSE))
stopifnot(identical(dim(pixels), c(8L, 8L)), typeof(pixels) == "double",
          sum(pixels > 100) == 24, mean(pixels > 100) == 0.375)
png(file.path(out, "pixel-demonstration.png"), width = 500, height = 500)
plot.new()
rasterImage(as.raster(pixels / 255), 0, 0, 1, 1)
invisible(dev.off())
estimates <- c(table_1e6_x10_MB = 1e6 * 10 * 8 / 1e6,       # 80 MB
               table_2e6_x5_MB = 2e6 * 5 * 8 / 1e6,         # 80 MB (topic quiz/practical)
               table_5e5_x20_MB = 5e5 * 20 * 8 / 1e6,       # 80 MB (topic quiz)
               genome_text_GB = 3.1e9 / 1e9,                # 3.1 GB
               genome_letters_R_GB = 3.1e9 * 8 / 1e9,       # 24.8 GB, "about 25 GB"
               image_pixels = 2048 * 2048,                  # 4,194,304
               image_file_MB = 2048 * 2048 / 1e6,           # 4.2 MB
               image_R_MB = 2048 * 2048 * 8 / 1e6,          # 33.6 MB
               images_100_R_GB = 100 * 2048 * 2048 * 8 / 1e9, # 3.4 GB
               single_cell_GB = 30000 * 100000 * 8 / 1e9)   # 24 GB
print(estimates)
stopifnot(estimates[["table_1e6_x10_MB"]] == 80, estimates[["single_cell_GB"]] == 24,
          round(estimates[["image_R_MB"]], 1) == 33.6, round(estimates[["image_file_MB"]], 1) == 4.2,
          round(estimates[["images_100_R_GB"]], 1) == 3.4, estimates[["image_pixels"]] == 4194304)
writeLines(c("Day 21 worked estimates (1 MB = 1e6 bytes):",
             sprintf("%s: %s", names(estimates), sapply(estimates, format, big.mark = ",", scientific = FALSE, digits = 7)),
             sprintf("100,000 x 10 rounded: CSV %.2f MB, object %.2f MB", size_rounded[1], size_rounded[2]),
             sprintf("with unique IDs: CSV %.2f MB, object %.2f MB (IDs %.2f MB)",
                     size_ids[1], size_ids[2], size_ids[3]),
             sprintf("1e6 unrounded numbers: CSV %.2f MB, object 8.00 MB", size_full)),
           file.path(out, "data-size.txt"))
rm(big, big_back)

# Day 22: validate portable inputs; a local test cannot verify SSH/desktop access.
stopifnot(file.exists("data/seedlings.csv"), file.exists("report.Rmd"))

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

# Expanded day 22: content/version checks in disposable local transfer fixtures.
# This never claims SSH, desktop or real remote access was tested.
audit_dir <- file.path(out, "transfer-rehearsal")
dir.create(audit_dir, recursive = TRUE, showWarnings = FALSE)
source_dir <- file.path(audit_dir, "source")
received_dir <- file.path(audit_dir, "received")
dir.create(source_dir, showWarnings = FALSE)
dir.create(received_dir, showWarnings = FALSE)
file.copy("data/algae.csv", file.path(source_dir, "algae.csv"), overwrite = TRUE)
file.copy(file.path(source_dir, "algae.csv"), file.path(received_dir, "algae.csv"),
          overwrite = TRUE)
source_lines <- readLines(file.path(source_dir, "algae.csv"))
received_lines <- readLines(file.path(received_dir, "algae.csv"))
stopifnot(identical(source_lines, received_lines))
writeLines("version 1", file.path(source_dir, "receipt.txt"))
writeLines("version 2", file.path(received_dir, "receipt.txt"))
stopifnot(file.info(file.path(source_dir, "receipt.txt"))$size ==
          file.info(file.path(received_dir, "receipt.txt"))$size,
          !identical(readLines(file.path(source_dir, "receipt.txt")),
                     readLines(file.path(received_dir, "receipt.txt"))))
writeLines(c("Local rehearsal only: no SSH or desktop service was tested.",
             "Two equal-size receipts differ in contents; filenames and size alone are insufficient.",
             "The received algae CSV has been checked against the source text."),
           file.path(audit_dir, "audit.txt"))

# Expanded days 23–25: genuinely fresh transfer data, primary and diagnostic.
algae <- read_csv("data/algae.csv", show_col_types = FALSE)
algae_summary <- algae |>
  group_by(treatment) |>
  summarise(n_enrolled = n(), n_available = sum(!is.na(biomass_mg)),
            n_missing = sum(is.na(biomass_mg)), mean_mg = mean(biomass_mg, na.rm = TRUE),
            sd_mg = sd(biomass_mg, na.rm = TRUE), .groups = "drop")
algae_reference <- algae |> filter(treatment == "reference") |> pull(biomass_mg)
algae_supplement <- algae |> filter(treatment == "supplement") |> pull(biomass_mg)
algae_difference <- mean(algae_supplement, na.rm = TRUE) - mean(algae_reference)
stopifnot(nrow(algae) == 24, anyDuplicated(algae$culture_id) == 0,
          sum(!is.na(algae_reference)) == 12, sum(!is.na(algae_supplement)) == 11,
          sum(is.na(algae$biomass_mg)) == 1,
          is.na(algae$biomass_mg[algae$culture_id == "A19"]),
          abs(mean(algae_reference) - 28.2) < 1e-10,
          abs(mean(algae_supplement, na.rm = TRUE) - 33.91818181818) < 1e-9,
          abs(algae_difference - 5.71818181818) < 1e-9,
          max(algae_reference) == 41.7, max(algae_supplement, na.rm = TRUE) == 39)
# Counterfactual zero is checked only to demonstrate an incorrect missing-value rule.
incorrect_zero_mean <- sum(algae_supplement, na.rm = TRUE) / length(algae_supplement)
stopifnot(abs(incorrect_zero_mean - 31.09166666667) < 1e-9)
# Optional inference reuses, and does not expand, the taught Welch method.
algae_test <- t.test(algae_supplement, algae_reference)
print(algae_summary)
print(algae_test)
write_csv(algae_summary, file.path(out, "algae-transfer-summary.csv"))
algae_plot <- ggplot(filter(algae, !is.na(biomass_mg)), aes(treatment, biomass_mg)) +
  geom_point(position = position_jitter(width = .08, height = 0, seed = 23)) +
  labs(x = "Culture allocation", y = "Dry biomass after seven days (mg)",
       caption = "Each point is one independent culture; A19 spilled and is not plotted.") +
  theme_minimal()
ggsave(file.path(out, "algae-transfer.png"), algae_plot, width = 6, height = 4)

algae_source <- file.path(out, "algae-brief.Rmd")
writeLines(c(
  '---', 'title: "Algae biomass: a short reproducible transfer memo"',
  'output: html_document', '---', '',
  '# Question and design', '',
  'These simulated data describe 24 independently grown cultures, twelve randomly',
  'allocated reference and twelve supplement conditions. Dry biomass was measured',
  'once after seven days. A19 spilled before weighing; biomass is unavailable.',
  'The culture is the independent unit, not each of its cells.', '',
  '```{r input}',
  'library(readr)', 'library(dplyr)', 'library(ggplot2)',
  'algae <- read_csv("data/algae.csv", show_col_types = FALSE)',
  'anyDuplicated(algae$culture_id)',
  'group_summary <- algae |> group_by(treatment) |>',
  '  summarise(n_enrolled = n(), n_available = sum(!is.na(biomass_mg)),',
  '            n_missing = sum(is.na(biomass_mg)),',
  '            mean_mg = mean(biomass_mg, na.rm = TRUE),',
  '            sd_mg = sd(biomass_mg, na.rm = TRUE), .groups = "drop")',
  'reference <- algae |> filter(treatment == "reference") |> pull(biomass_mg)',
  'supplement <- algae |> filter(treatment == "supplement") |> pull(biomass_mg)',
  'difference_mg <- mean(supplement, na.rm = TRUE) - mean(reference, na.rm = TRUE)',
  '```', '',
  '# Results', '',
  'There are `r nrow(algae)` culture records and',
  '`r sum(!is.na(algae$biomass_mg))` available biomass measurements.', '',
  '```{r summary}', 'knitr::kable(group_summary, digits = 2)', '```', '',
  '```{r observations, fig.cap="Independent cultures; A19 has unavailable biomass after a spill and is not plotted."}',
  'ggplot(filter(algae, !is.na(biomass_mg)), aes(treatment, biomass_mg)) +',
  '  geom_point(position = position_jitter(width = .08, height = 0, seed = 23)) +',
  '  labs(x = "Culture allocation", y = "Dry biomass after seven days (mg)") +',
  '  theme_minimal()', '```', '',
  'The observed supplement-minus-reference mean difference is',
  '`r round(difference_mg, 2)` mg. The reference culture A11 has the largest',
  'individual measurement, despite the greater supplement mean.', '',
  '# Interpretation and limitations', '',
  'Supplement cultures had greater mean observed biomass, with overlap among',
  'individual measurements. SD describes culture-to-culture spread; it is not',
  'uncertainty in an effect. The descriptive memo adds no inferential claim.',
  'One supplement result is unavailable, so the comparison is conditional on',
  'the available observations and how the loss relates to the outcome.',
  'A small simulated experiment cannot establish a response for all growing conditions.'
), algae_source)
rmarkdown::render(algae_source, output_dir = out, knit_root_dir = root,
                  envir = new.env(parent = globalenv()), quiet = TRUE)

# Day 24: portable extraction and a controlled missing-input failure.
portable <- file.path(out, "portable-algae")
dir.create(file.path(portable, "data"), recursive = TRUE, showWarnings = FALSE)
dir.create(file.path(portable, "output"), showWarnings = FALSE)
file.copy(algae_source, file.path(portable, "algae-brief.Rmd"), overwrite = TRUE)
file.copy("introcomputing.Rproj", file.path(portable, "introcomputing.Rproj"), overwrite = TRUE)
file.copy("data/algae.csv", file.path(portable, "data/algae.csv"), overwrite = TRUE)
file.copy("data/README.md", file.path(portable, "data/README.md"), overwrite = TRUE)
writeLines(c("Simulated independent-culture data; no original measurements.",
             "Render algae-brief.Rmd from this project root.",
             "R packages: readr,dplyr,ggplot2,rmarkdown,knitr."),
           file.path(portable, "README.txt"))
portable_source <- file.path(portable, "algae-brief.Rmd")
rmarkdown::render(portable_source, quiet = TRUE, envir = new.env(parent = globalenv()))
stopifnot(file.exists(file.path(portable, "algae-brief.html")))
file.rename(file.path(portable, "data/algae.csv"), file.path(portable, "data/algae-temporarily-missing.csv"))
missing_error <- tryCatch({
  rmarkdown::render(portable_source, quiet = TRUE, envir = new.env(parent = globalenv()))
  NULL
}, error = function(error) conditionMessage(error))
file.rename(file.path(portable, "data/algae-temporarily-missing.csv"), file.path(portable, "data/algae.csv"))
stopifnot(is.character(missing_error), length(missing_error) == 1,
          grepl("algae.csv", missing_error, fixed = TRUE))
rmarkdown::render(portable_source, quiet = TRUE, envir = new.env(parent = globalenv()))
false_source <- file.path(portable, "diagnostic-false-prose.Rmd")
writeLines(c(readLines(portable_source), '', '# Intentionally false diagnostic sentence',
             'All 24 cultures had a measured biomass outcome.'), false_source)
rmarkdown::render(false_source, quiet = TRUE, envir = new.env(parent = globalenv()))
stopifnot(file.exists(file.path(portable, "diagnostic-false-prose.html")))
writeLines(c("Case 1: copied input renamed; expected rendering failure observed.",
             paste("Observed error:", missing_error),
             "Case 1 repair: restored exact name; successful fresh render.",
             "Case 2: intentionally false prose still renders; contradiction requires scientific review."),
           file.path(out, "reproduction-cases.txt"))
# Keep intentionally false diagnostics outside the final portable package.
unlink(c(false_source, sub("\\.Rmd$", ".html", false_source)))

# Day 25: preserve the primary data and label sensitivity to one recorded high value.
algae_without_a11 <- filter(algae, culture_id != "A11")
diagnostic_ref <- filter(algae_without_a11, treatment == "reference")$biomass_mg
diagnostic_supplement <- filter(algae_without_a11, treatment == "supplement")$biomass_mg
diagnostic_difference <- mean(diagnostic_supplement, na.rm = TRUE) - mean(diagnostic_ref)
stopifnot(nrow(algae_without_a11) == 23,
          sum(!is.na(algae_without_a11$biomass_mg)) == 22,
          abs(mean(diagnostic_ref) - 26.97272727273) < 1e-9,
          abs(diagnostic_difference - 6.94545454545) < 1e-9,
          mean(diagnostic_supplement, na.rm = TRUE) == mean(algae_supplement, na.rm = TRUE),
          nrow(algae) == 24,
          is.na(algae$biomass_mg[algae$culture_id == "A19"]))
write_csv(data.frame(
  analysis = c("primary_all_available", "diagnostic_a11_omitted_without_error_evidence"),
  n_reference = c(12, 11), n_supplement = c(11, 11),
  observed_difference_mg = c(algae_difference, diagnostic_difference)),
  file.path(out, "primary-and-diagnostic.csv"))

# Package the final tested source and actual inputs, then render its extracted copy.
archive_path <- file.path(out, "algae-share.zip")
local({
  original_directory <- setwd(out)
  on.exit(setwd(original_directory))
  if (file.exists(archive_path)) unlink(archive_path)
  status <- utils::zip(archive_path, files = "portable-algae", flags = "-r9Xq")
  stopifnot(status == 0)
})
extracted <- tempfile("algae-recipient-")
dir.create(extracted)
unzip(archive_path, exdir = extracted)
recipient_source <- file.path(extracted, "portable-algae/algae-brief.Rmd")
rmarkdown::render(recipient_source, quiet = TRUE, envir = new.env(parent = globalenv()))
stopifnot(file.exists(sub("\\.Rmd$", ".html", recipient_source)))
cat("Expanded week 5 data-size, transfer, fresh-culture reports, controlled failure, sensitivity and extracted-project checks passed.\n")

cat("Week 5 reference computations and report passed. Artifacts:", out, "\n")
