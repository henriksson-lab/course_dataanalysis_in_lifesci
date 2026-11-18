# Instructor worked solutions, days 11–15.
# Run from repository root: Rscript instructor/week3-solutions.R
suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
})
root <- normalizePath(getwd())
stopifnot(file.exists("data/seedlings-messy.csv"))
out <- file.path(root, "output", "instructor-week3")
dir.create(out, recursive = TRUE, showWarnings = FALSE)

# Day 11: source records, not implausibility alone, support these repairs.
raw <- read_csv("data/seedlings-messy.csv", show_col_types = FALSE,
                col_types = cols(.default = col_character()), trim_ws = FALSE)
print(unique(raw$treatment))
print(raw |> count(plant_id) |> filter(n > 1))
cleaned <- raw |>
  mutate(treatment = tolower(trimws(treatment)),
         initial_mm = if_else(plant_id == "P18", "18.7", initial_mm),
         final_mm = if_else(plant_id == "P21", "43.8", final_mm)) |>
  distinct() |>
  mutate(initial_mm = parse_double(initial_mm),
         final_mm = parse_double(final_mm),
         growth_mm = final_mm - initial_mm)
stopifnot(nrow(raw) == 25, nrow(cleaned) == 24,
          anyDuplicated(cleaned$plant_id) == 0,
          sum(is.na(cleaned$growth_mm)) == 1,
          is.na(cleaned$final_mm[cleaned$plant_id == "P06"]),
          cleaned$final_mm[cleaned$plant_id == "P21"] == 43.8)
write_csv(cleaned, file.path(out, "seedlings-cleaned.csv"))
writeLines(c(
  "P01 duplicate confirmed in source record: one identical row removed.",
  "Treatment labels standardised after confirming intended labels.",
  "P18 initial length 18.7 mm confirmed; numeric text restored.",
  "P21 final length 43.8 mm confirmed by source record.",
  "P06 final length unavailable; retained as NA, never replaced with zero."
), file.path(out, "cleaning-notes.txt"))
print(mean(cleaned$growth_mm))
print(mean(cleaned$growth_mm, na.rm = TRUE))

# Day 12: hand-workable spread and the effect of a change of units.
toy <- c(12, 14, 16)
stopifnot(mean(toy) == 14, var(toy) == 4, sd(toy) == 2)
close_mm <- c(13, 14, 15)
spread_mm <- c(8, 14, 20)
stopifnot(mean(close_mm) == mean(spread_mm),
          sd(close_mm) == 1, sd(spread_mm) == 6,
          sd(close_mm + 10) == sd(close_mm),
          abs(var(close_mm / 10) - var(close_mm) / 100) < 1e-10)
toy_spread <- data.frame(group = rep(c("SD = 1 mm", "SD = 6 mm"), each = 3),
                         growth_mm = c(close_mm, spread_mm))
variation_plot <- ggplot(toy_spread, aes(group, growth_mm)) +
  geom_hline(yintercept = 14, linetype = "dashed", colour = "darkred") +
  geom_point(size = 3) +
  labs(x = "Toy group", y = "Growth (mm)",
       caption = "Both means are 14 mm. Dashed line: the common mean.") +
  theme_minimal()
ggsave(file.path(out, "variation-examples.png"), variation_plot,
       width = 6, height = 4)

# Day 13: summary rows are groups, not new observations.
seedlings <- read_csv("data/seedlings.csv", show_col_types = FALSE) |>
  mutate(growth_mm = final_mm - initial_mm)
group_summary <- seedlings |>
  group_by(treatment) |>
  summarise(n_plants = n(), n_observed = sum(!is.na(growth_mm)),
            mean_mm = mean(growth_mm, na.rm = TRUE),
            median_mm = median(growth_mm, na.rm = TRUE),
            variance_mm2 = var(growth_mm, na.rm = TRUE),
            sd_mm = sd(growth_mm, na.rm = TRUE), .groups = "drop")
print(group_summary)
write_csv(group_summary, file.path(out, "growth-summary.csv"))
repaired_summary <- cleaned |>
  group_by(treatment) |>
  summarise(n_plants = n(), n_observed = sum(!is.na(growth_mm)),
            mean_mm = mean(growth_mm, na.rm = TRUE), .groups = "drop")
print(repaired_summary)
stopifnot(repaired_summary$n_observed[repaired_summary$treatment == "control"] == 11)
group_plot <- ggplot(seedlings, aes(treatment, growth_mm)) +
  geom_point(position = position_jitter(width = 0.08, height = 0, seed = 13),
             alpha = 0.75) +
  geom_point(data = group_summary, aes(treatment, mean_mm), inherit.aes = FALSE,
             shape = 18, size = 4, colour = "darkred") +
  labs(x = "Treatment", y = "Change in seedling length (mm)",
       caption = "Small dots: individual plants. Red diamonds: group means.") +
  theme_minimal()
ggsave(file.path(out, "growth-summary.png"), group_plot, width = 6, height = 4)

# Day 14: supplied sampling demonstration; no functions students need to author.
population_mm <- seedlings$growth_mm
set.seed(14)
means_4 <- replicate(400, mean(sample(population_mm, size = 4, replace = TRUE)))
means_16 <- replicate(400, mean(sample(population_mm, size = 16, replace = TRUE)))
sampling <- data.frame(mean_mm = c(means_4, means_16),
                       sample_size = rep(c("4 plants", "16 plants"), each = 400))
print(c(individual_sd = sd(population_mm),
        sd_of_means_n4 = sd(means_4), sd_of_means_n16 = sd(means_16)))
sampling_plot <- ggplot(sampling, aes(mean_mm)) +
  geom_histogram(binwidth = 1, colour = "white") +
  facet_wrap(~sample_size, ncol = 1) +
  labs(x = "Mean growth in one simulated sample (mm)",
       y = "Number of simulated samples") + theme_minimal()
ggsave(file.path(out, "sampling-means.png"), sampling_plot, width = 6, height = 5)

# Day 15: complete descriptive report with self-contained imports/calculations.
report <- c(
  '---', 'title: "Descriptive report: seedling growth"', 'output: html_document', '---',
  '', '## Question and design', '',
  'How does recorded growth vary among individual plants and between groups?',
  'These simulated data contain 24 independently potted seedlings, twelve',
  'randomly assigned to each group. Initial and final lengths belong to the same',
  'plant in each row, with measurements seven days apart. The treated group received',
  'a nutrient treatment; its formulation is unspecified.',
  '', '## Methods and data quality', '',
  'The complete supplied file was used. Plant IDs, group labels, column types,',
  'and missing measurements were checked. Growth is final minus initial length.',
  'The report describes the sample; it does not test a treatment hypothesis.',
  '', '```{r import}',
  'library(readr)', 'library(dplyr)', 'library(ggplot2)',
  'seedlings <- read_csv("data/seedlings.csv", show_col_types = FALSE)',
  'anyDuplicated(seedlings$plant_id)', 'seedlings |> count(treatment)',
  'sum(is.na(seedlings$initial_mm))', 'sum(is.na(seedlings$final_mm))',
  'seedlings <- mutate(seedlings, growth_mm = final_mm - initial_mm)', '```',
  '', '## Results', '', '```{r summary}',
  'group_summary <- seedlings |>',
  '  group_by(treatment) |>',
  '  summarise(n_observed = sum(!is.na(growth_mm)),',
  '            mean_mm = mean(growth_mm, na.rm = TRUE),',
  '            median_mm = median(growth_mm, na.rm = TRUE),',
  '            sd_mm = sd(growth_mm, na.rm = TRUE), .groups = "drop")',
  'knitr::kable(group_summary, digits = 2,',
  '             caption = "Growth by treatment. Means, medians, and SD in mm.")', '```',
  '', '```{r figure, fig.cap="Dots are individual plants; red diamonds are group means."}',
  'ggplot(seedlings, aes(treatment, growth_mm)) +',
  '  geom_point(position = position_jitter(width = 0.08, height = 0, seed = 13)) +',
  '  geom_point(data = group_summary, aes(treatment, mean_mm),',
  '             inherit.aes = FALSE, shape = 18, size = 4, colour = "darkred") +',
  '  labs(x = "Treatment", y = "Change in seedling length (mm)") + theme_minimal()',
  '```', '', '## Interpretation', '',
  'The treated mean growth was about 21.5 mm compared with 15.3 mm for controls.',
  'Individual growth values overlap between groups. The treated SD was about',
  '4.87 mm and the control SD about 3.19 mm, describing spread among plants.',
  'SD is not the uncertainty in a mean. This descriptive report has not estimated',
  'uncertainty in the group difference. The observations come from a small',
  'simulated experiment and should not be generalised to every biological setting.'
)
source_path <- file.path(out, "descriptive-report.Rmd")
writeLines(report, source_path)
rmarkdown::render(source_path, output_dir = out, knit_root_dir = root,
                  envir = new.env(parent = globalenv()), quiet = TRUE)

# Organic-laboratory transfer choices for days 12–15. These replace selected
# practice, not the seedling core or an additional required report.
organic <- read_csv("data/organic-recovery.csv", show_col_types = FALSE) |>
  mutate(yield_percent = 100 * isolated_mass_g / theoretical_mass_g)
stopifnot(nrow(organic) == 12, anyDuplicated(organic$run_id) == 0,
          !anyNA(organic), all(organic$theoretical_mass_g > 0),
          all(organic$isolated_mass_g >= 0),
          all(organic$yield_percent <= 100))
standard_runs <- organic |> filter(protocol == "standard")
modified_runs <- organic |> filter(protocol == "modified")
organic_summary <- organic |>
  group_by(protocol) |>
  summarise(n_runs = n(), mean_yield_percent = mean(yield_percent),
            variance_percentage_points2 = var(yield_percent),
            sd_percentage_points = sd(yield_percent), .groups = "drop")
stopifnot(nrow(standard_runs) == 6, nrow(modified_runs) == 6,
          abs(organic$yield_percent[organic$run_id == "Y01"] - 62) < 1e-10,
          abs(mean(standard_runs$yield_percent) - 68.6666666667) < 1e-8,
          abs(var(standard_runs$yield_percent) - 18.6666666667) < 1e-8,
          abs(sd(standard_runs$yield_percent) - 4.32049379894) < 1e-8,
          abs(mean(modified_runs$yield_percent) - 77) < 1e-10,
          abs(sd(modified_runs$yield_percent) - sqrt(14)) < 1e-10)
print(organic_summary)
write_csv(organic_summary, file.path(out, "organic-yield-summary.csv"))
organic_plot <- ggplot(organic, aes(protocol, yield_percent)) +
  geom_point(position = position_jitter(width = 0.08, height = 0, seed = 13)) +
  labs(x = "Protocol", y = "Isolated product yield (%)",
       caption = "Each point is one independent synthesis run. All data are simulated.") +
  theme_minimal()
ggsave(file.path(out, "organic-yield-summary.png"), organic_plot,
       width = 6, height = 4)

# Day 15 alternative: source includes its own input and calculations, preserving
# root-relative paths when students place the .Rmd beside their .Rproj file.
organic_report <- c(
  '---', 'title: "Descriptive report: collected-product yield"',
  'output: html_document', '---', '', '## Question and design', '',
  'How does collected-product yield vary among runs and between protocols?',
  'These simulated data describe twelve independent product-making experiments,',
  'or synthesis runs, randomly assigned to standard or modified protocol, six each.',
  'Theoretical mass is the supplied maximum product mass for the starting',
  'materials. Isolated mass is dry collected product, assumed pure here.',
  'Both are in grams. The different starting scales make percentage yield',
  'more comparable than raw collected grams.', '', '## Methods and checks', '',
  'Yield was calculated as 100 times isolated mass divided by theoretical mass.',
  'We checked identifiers, protocol labels, missing values, and positive',
  'theoretical masses. SD describes variation among independent runs,',
  'not uncertainty in a protocol mean.', '', '```{r import}',
  'library(readr)', 'library(dplyr)', 'library(ggplot2)',
  'organic <- read_csv("data/organic-recovery.csv", show_col_types = FALSE)',
  'anyDuplicated(organic$run_id)', 'organic |> count(protocol)',
  'sum(is.na(organic$theoretical_mass_g))',
  'sum(is.na(organic$isolated_mass_g))',
  'sum(organic$theoretical_mass_g <= 0)',
  'organic <- mutate(organic,',
  '                  yield_percent = 100 * isolated_mass_g / theoretical_mass_g)',
  '```', '', '## Results', '', '```{r summary}',
  'organic_summary <- organic |> group_by(protocol) |>',
  '  summarise(n_runs = n(), mean_yield_percent = mean(yield_percent),',
  '            sd_percentage_points = sd(yield_percent), .groups = "drop")',
  'knitr::kable(organic_summary, digits = 2,',
  '             caption = "Mean yield in percent; SD in percentage points.")',
  '```', '', '```{r figure, fig.cap="Each point represents one independent synthesis run. Values are simulated."}',
  'ggplot(organic, aes(protocol, yield_percent)) +',
  '  geom_point(position = position_jitter(width = 0.08, height = 0, seed = 13)) +',
  '  labs(x = "Protocol", y = "Isolated product yield (%)") + theme_minimal()',
  '```', '', '## Interpretation and limits', '',
  'Mean isolated yield was about 68.67% with the standard protocol and 77.00%',
  'with the modified protocol. Their SDs were about 4.32 and 3.74 percentage',
  'points, respectively. Individual results overlap between protocols.',
  'This descriptive report does not estimate uncertainty in the mean difference.',
  'The comparison concerns a small simulated set and assumes pure dry product.',
  'Yield alone cannot establish greater purity, safety, environmental benefit,',
  'or superiority in other reactions. We have not inferred a reaction mechanism.'
)
organic_source_path <- file.path(out, "organic-report.Rmd")
writeLines(organic_report, organic_source_path)
rmarkdown::render(organic_source_path, output_dir = out, knit_root_dir = root,
                  envir = new.env(parent = globalenv()), quiet = TRUE)
if ("--figures" %in% commandArgs(trailingOnly = TRUE)) {
  file.copy(file.path(out, c("variation-examples.png", "sampling-means.png")),
            file.path("week3", c("variation-examples.png", "sampling-means.png")),
            overwrite = TRUE)
}
cat("Week 3 worked calculations and report rendered successfully. Artifacts:", out, "\n")
