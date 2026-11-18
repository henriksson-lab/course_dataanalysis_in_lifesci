# Instructor worked solutions, days 6–10.
# Run from the repository root: Rscript instructor/week2-solutions.R
# Artifacts go to output/instructor-week2; the script prints their location.
suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
})
root <- normalizePath(getwd())
stopifnot(file.exists("data/seedlings.csv"))
out <- file.path(root, "output", "instructor-week2")
dir.create(out, recursive = TRUE, showWarnings = FALSE)

# Day 6: after the fourth plant and revised first final measurement.
initial_mm <- c(20, 22, 19, 21)
final_mm <- c(38, 40, 34, 39)
growth_mm <- final_mm - initial_mm
length_ratio <- final_mm / initial_mm
print(data.frame(initial_mm, final_mm, growth_mm, length_ratio))
stopifnot(identical(growth_mm, c(18, 18, 15, 18)))
# Growth is an absolute change in mm; ratio has no length unit.

# Day 6 alternative ratio exercise: maximum product mass is supplied.
theoretical_mass_g <- 1.00
isolated_mass_g <- 0.62
yield_percent <- 100 * isolated_mass_g / theoretical_mass_g
stopifnot(yield_percent == 62,
          100 * 0.70 / theoretical_mass_g == 70)
# Collected dry mass is assumed pure here; yield does not establish purity.

# Day 7: an imported observation has a design and units, not just a type.
seedlings <- read_csv("data/seedlings.csv", show_col_types = FALSE)
stopifnot(nrow(seedlings) == 24, ncol(seedlings) == 4,
          !anyNA(seedlings), anyDuplicated(seedlings$plant_id) == 0)
print(str(seedlings))
leaves <- read_csv("data/leaf-mass.csv", show_col_types = FALSE)
stopifnot(nrow(leaves) == 18)
print(head(leaves))

# Day 8: derived change, deliberate selection, two different plot questions.
seedlings <- mutate(seedlings, growth_mm = final_mm - initial_mm)
control_plants <- filter(seedlings, treatment == "control")
growth_table <- select(seedlings, plant_id, treatment, growth_mm)
treated_growth <- seedlings |>
  filter(treatment == "treated") |>
  select(plant_id, growth_mm)
longer_control <- seedlings |>
  filter(treatment == "control") |>
  filter(growth_mm > 15)
stopifnot(nrow(control_plants) == 12, nrow(treated_growth) == 12,
          abs(seedlings$growth_mm[2] - 8) < 1e-10)
print(longer_control)
size_plot <- ggplot(seedlings, aes(initial_mm, final_mm, colour = treatment)) +
  geom_point(size = 2) +
  labs(x = "Initial seedling length (mm)", y = "Final seedling length (mm)",
       colour = "Treatment") + theme_minimal()
growth_plot <- ggplot(seedlings, aes(treatment, growth_mm)) +
  geom_point(position = position_jitter(width = 0.08, height = 0, seed = 8)) +
  labs(x = "Treatment", y = "Change in seedling length (mm)") + theme_minimal()
initial_growth_plot <- ggplot(seedlings, aes(initial_mm, growth_mm)) +
  geom_point() + labs(x = "Initial seedling length (mm)",
                      y = "Change in seedling length (mm)") + theme_minimal()
ggsave(file.path(out, "seedling-size.png"), size_plot, width = 6, height = 4)
ggsave(file.path(out, "seedling-growth.png"), growth_plot, width = 6, height = 4)
ggsave(file.path(out, "initial-growth.png"), initial_growth_plot, width = 6, height = 4)
write_csv(growth_table, file.path(out, "seedling-growth.csv"))
write_csv(treated_growth, file.path(out, "treated-growth.csv"))

# Day 8 alternative transfer: a derived percentage and a plot, not another test.
organic <- read_csv("data/organic-recovery.csv", show_col_types = FALSE)
organic <- mutate(organic,
                  yield_percent = 100 * isolated_mass_g / theoretical_mass_g)
expected_yields <- c(62, 70, 68, 74, 66, 72, 72, 78, 76, 82, 74, 80)
stopifnot(nrow(organic) == 12, anyDuplicated(organic$run_id) == 0,
          !anyNA(organic), all(organic$theoretical_mass_g > 0),
          all(organic$isolated_mass_g >= 0),
          isTRUE(all.equal(organic$yield_percent, expected_yields)),
          organic$yield_percent[organic$run_id == "Y01"] == 62)
print(organic)
organic_plot <- ggplot(organic, aes(protocol, yield_percent)) +
  geom_point(position = position_jitter(width = 0.08, height = 0, seed = 8)) +
  labs(x = "Protocol", y = "Isolated product yield (%)") + theme_minimal()
write_csv(organic, file.path(out, "organic-yields.csv"))
ggsave(file.path(out, "organic-yields.png"), organic_plot, width = 6, height = 4)

# Days 9–10: generate and render a self-contained worked source.
report <- c(
  '---', 'title: "First report: seedling growth"', 'output: html_document', '---',
  '', '## Question and data', '',
  'How did growth vary among plants and between the two supplied groups?',
  'These simulated teaching data describe 24 independently potted seedlings,',
  'with twelve plants randomly assigned to each treatment. Each row is one plant.',
  'Plants received a control or nutrient treatment and were measured seven days apart.',
  'The nutrient formulation is unspecified.',
  '', '## Methods', '',
  'Growth was calculated as final minus initial length in millimetres.',
  'Individual plant measurements are shown rather than a bar of the mean alone.',
  '', '```{r import}',
  'library(readr)', 'library(dplyr)', 'library(ggplot2)',
  'seedlings <- read_csv("data/seedlings.csv", show_col_types = FALSE)',
  'seedlings <- mutate(seedlings, growth_mm = final_mm - initial_mm)',
  '```', '', '## Results', '',
  'There are `r nrow(seedlings)` plant records and',
  '`r sum(is.na(seedlings$growth_mm))` missing growth measurements.',
  '', '```{r figure, fig.cap="Each dot is one independently potted plant."}',
  'ggplot(seedlings, aes(treatment, growth_mm)) +',
  '  geom_point(position = position_jitter(width = 0.08, height = 0, seed = 8)) +',
  '  labs(x = "Treatment", y = "Change in seedling length (mm)") +',
  '  theme_minimal()', '```', '', '## Interpretation', '',
  'Growth varied among plants in both groups. The treated group tended to show',
  'larger growth, but the observations overlap: not every treated plant outgrew',
  'every control plant. This first description does not quantify uncertainty in',
  'a group difference and should not be presented as a universal treatment claim.'
)
source_path <- file.path(out, "first-report.Rmd")
writeLines(report, source_path)
rmarkdown::render(source_path, output_dir = out, knit_root_dir = root,
                  envir = new.env(parent = globalenv()), quiet = TRUE)
leaf_plot <- ggplot(leaves, aes(leaf_area_cm2, dry_mass_mg)) +
  geom_point() + labs(x = "Leaf area (cm²)", y = "Dry mass (mg)") + theme_minimal()
ggsave(file.path(out, "leaf-first-look.png"), leaf_plot, width = 6, height = 4)
if ("--figures" %in% commandArgs(trailingOnly = TRUE)) {
  file.copy(file.path(out, "seedling-growth.png"),
            "week2/seedling-growth.png", overwrite = TRUE)
}
cat("Week 2 worked calculations and report rendered successfully. Artifacts:", out, "\n")
