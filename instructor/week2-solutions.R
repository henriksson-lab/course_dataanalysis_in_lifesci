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

# Expanded days6–10: dependency, units, inspection, derived tables and reports.
initial_single_mm <- 20
final_single_mm <- 37
stored_growth_mm <- final_single_mm - initial_single_mm
final_single_mm <- 39
stopifnot(stored_growth_mm == 17)
stored_growth_mm <- final_single_mm - initial_single_mm
stopifnot(stored_growth_mm == 19,
          identical(c(34,37,40) - c(20,22,19), c(14,15,21)),
          abs(mean(c(17,18,15)/10) - mean(c(17,18,15))/10) < 1e-12)
solutions <- read_csv("data/solutions.csv", show_col_types = FALSE) |>
  mutate(amount_mol = mass_g / molar_mass_g_mol,
         final_volume_l = final_volume_ml / 1000,
         concentration_mmol_l = 1000 * amount_mol / final_volume_l)
stopifnot(nrow(solutions) == 6, anyDuplicated(solutions$solution_id) == 0,
          !anyNA(solutions), length(unique(solutions$solute)) == 2,
          isTRUE(all.equal(solutions$concentration_mmol_l,c(50,100,150,50,100,150))),
          abs(1000*(0.2922/58.44)/.1 - 50) < 1e-10,
          abs(1000*(0.9008/180.16)/.1 - 50) < 1e-10,
          abs(1000*(2*.2922/58.44)/.1 - 100) < 1e-10,
          abs(1000*(.2922/58.44)/.2 - 25) < 1e-10)
transfer <- read_csv("data/seedlings-transfer.csv", show_col_types = FALSE) |>
  mutate(growth_mm = final_mm - initial_mm)
stopifnot(nrow(transfer) == 18, ncol(transfer) == 5,
          anyDuplicated(transfer$plant_id) == 0, !anyNA(transfer),
          all(table(transfer$treatment) == 9),
          abs(transfer$growth_mm[transfer$plant_id=="T01"] - 15) < 1e-10,
          transfer$treatment[transfer$plant_id=="T18"] == "treated",
          abs(transfer$initial_mm[transfer$plant_id=="T18"] - 21.6) < 1e-10,
          abs(transfer$final_mm[transfer$plant_id=="T18"] - 43) < 1e-10)
stopifnot(is.na(mean(c(10,NA,20))), mean(c(10,NA,20),na.rm=TRUE)==15,
          mean(c(10,0,20))==10)
transfer_growth <- transfer |> select(plant_id,treatment,growth_mm)
transfer_treated <- transfer_growth |> filter(treatment=="treated")
stopifnot(nrow(transfer_treated)==9)
write_csv(transfer_growth,file.path(out,"transfer-growth.csv"))
write_csv(transfer_treated,file.path(out,"transfer-treated.csv"))
transfer_plot <- ggplot(transfer,aes(treatment,growth_mm)) +
  geom_point(position=position_jitter(width=.08,height=0,seed=8)) +
  labs(x="Allocation",y="Seven-day growth (mm)") + theme_minimal()
ggsave(file.path(out,"transfer-growth.png"),transfer_plot,width=6,height=4)
transfer_size <- ggplot(transfer,aes(initial_mm,final_mm)) + geom_point() +
  labs(x="Initial length (mm)",y="Final length (mm)") + theme_minimal()
ggsave(file.path(out,"transfer-size.png"),transfer_size,width=6,height=4)
dilutions <- read_csv("data/dilutions.csv",show_col_types=FALSE) |>
  mutate(stock_volume_ml = target_mmol_l * final_volume_ml / stock_mmol_l,
         possible_by_dilution = target_mmol_l <= stock_mmol_l)
stopifnot(isTRUE(all.equal(dilutions$stock_volume_ml,c(2.5,5,10,100))),
          identical(dilutions$possible_by_dilution,c(TRUE,TRUE,TRUE,FALSE)))
supported <- dilutions |> filter(possible_by_dilution)
stopifnot(nrow(supported)==3,all(supported$stock_volume_ml <= supported$final_volume_ml))
write_csv(dilutions,file.path(out,"dilution-check.csv"))
dilution_plot <- ggplot(supported,aes(final_volume_ml,stock_volume_ml)) +
  geom_point() + labs(x="Final total volume (mL)",y="Required stock volume (mL)") +
  theme_minimal()
ggsave(file.path(out,"dilution-plot.png"),dilution_plot,width=6,height=4)
write_csv(solutions,file.path(out,"solution-concentrations.csv"))

# Complete reference source for the fresh-session transfer report.
transfer_source <- c(
 '---','title: "Eighteen seedlings: a transfer report"','output: html_document','---','',
 '# Question and design','',
 'How does seven-day growth vary among these simulated seedlings?',
 'Eighteen independent potted plants were randomly allocated control or treatment,',
 'nine per group. Each row contains initial and final length for the same plant.',
 'Lengths and derived growth are millimetres. This report is descriptive.', '',
 '# Methods','',
 'We checked identifiers, groups, types and missingness, and calculated final',
 'minus initial length. Raw measurements remain in their original CSV.', '',
 '```{r import}', 'library(readr)','library(dplyr)','library(ggplot2)',
 'transfer <- read_csv("data/seedlings-transfer.csv",show_col_types=FALSE)',
 'dim(transfer)', 'length(unique(transfer$plant_id))','table(transfer$treatment)',
 'sum(is.na(transfer$initial_mm))','sum(is.na(transfer$final_mm))',
 'transfer <- transfer |> mutate(growth_mm=final_mm-initial_mm)', '```', '',
 '# Results','', 'The input contains `r nrow(transfer)` plants.', '',
 '```{r plot, fig.cap="Each point is an independent plant; horizontal jitter only separates overlaps."}',
 'ggplot(transfer,aes(treatment,growth_mm)) +',
 ' geom_point(position=position_jitter(width=.08,height=0,seed=8)) +',
 ' labs(x="Allocation",y="Seven-day growth (mm)") + theme_minimal()', '```', '',
 '# Interpretation','',
 'Growth varies among plants within both groups, with overlap between groups.',
 'The figure describes this sample; it does not establish that every treated',
 'plant grows more, nor quantify uncertainty in a population mean difference.'
)
transfer_source_path <- file.path(out,"transfer-report.Rmd")
writeLines(transfer_source,transfer_source_path)
rmarkdown::render(transfer_source_path,output_dir=out,knit_root_dir=root,
                  envir=new.env(parent=globalenv()),quiet=TRUE)
solution_source <- c(
 '---','title: "Laboratory brief: supplied solution calculations"','output: html_document','---','',
 '# Question','',
 'What amount concentrations follow from the supplied numerical inputs?',
 'These six simulated cases are calculated preparations, not independently',
 'treated biological samples. A mole is a chemical amount unit and molar mass',
 'is grams per mole. All constants and the calculation relationship are supplied.', '',
 '# Methods','',
 'Amount in mol is mass in g divided by molar mass in g/mol. Final mL are',
 'divided by 1000 to give litres; amount per litre is multiplied by 1000 for mmol/L.', '',
 '```{r calculate}', 'library(readr)','library(dplyr)','library(ggplot2)',
 'solutions <- read_csv("data/solutions.csv",show_col_types=FALSE) |>',
 ' mutate(concentration_mmol_l=1000*(mass_g/molar_mass_g_mol)/(final_volume_ml/1000))',
 'knitr::kable(solutions,digits=3)', '```', '',
 '# Results','',
 '```{r plot, fig.cap="Calculated values from the supplied rule; points are preparation cases, not independent treatment evidence."}',
 'ggplot(solutions,aes(mass_g,concentration_mmol_l,colour=solute)) +',
 ' geom_point() + labs(x="Supplied mass (g)",y="Calculated concentration (mmol/L)") +',
 ' theme_minimal()', '```', '',
 '# Interpretation','',
 'Each solute has concentrations of 50, 100 and 150 mmol/L. Different masses',
 'can yield the same amount concentration because molar masses differ. The',
 'relationship is supplied by the calculation, not discovered from a biological',
 'experiment. Measurement and preparation uncertainty are not quantified here.'
)
solution_source_path <- file.path(out,"laboratory-brief.Rmd")
writeLines(solution_source,solution_source_path)
rmarkdown::render(solution_source_path,output_dir=out,knit_root_dir=root,
                  envir=new.env(parent=globalenv()),quiet=TRUE)
cat("Expanded weeks1–2 numerical checks, transfer figures, and both new report examples passed.\n")

# Check the failure mechanisms demonstrated in the day9 recovery workshop.
duplicate_source <- c('```{r repeated_label}', '1 + 1', '```', '',
                      '```{r repeated_label}', '2 + 2', '```')
duplicate_error <- tryCatch(
  knitr::knit(text=duplicate_source,quiet=TRUE,envir=new.env(parent=globalenv())),
  error=identity)
stopifnot(inherits(duplicate_error,"error"),
          grepl("Duplicate chunk label",conditionMessage(duplicate_error)))
missing_input_error <- tryCatch(
  read_csv("data/this-input-is-deliberately-absent.csv",show_col_types=FALSE),
  error=identity)
stopifnot(inherits(missing_input_error,"error"))
missing_object_error <- tryCatch(
  eval(quote(mean(not_created_growth_mm)),envir=new.env(parent=baseenv())),
  error=identity)
stopifnot(inherits(missing_object_error,"error"),
          grepl("not_created_growth_mm",conditionMessage(missing_object_error)))
cat("Expected duplicate-label, missing-input and missing-object failures verified.\n")
