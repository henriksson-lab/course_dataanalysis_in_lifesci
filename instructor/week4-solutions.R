# Run from the course repository root: Rscript instructor/week4-solutions.R
# Instructor-only reference calculations; synthetic data, not real evidence.
suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(ggplot2)
})
build_figures <- "--figures" %in% commandArgs(trailingOnly = TRUE)
out <- if (build_figures) "week4/figures" else file.path(tempdir(), "introcomputing-week4")
dir.create(out, recursive = TRUE, showWarnings = FALSE)

# Days 16-17: one growth value per independent plant, treated minus control.
seedlings <- read_csv("data/seedlings.csv", show_col_types = FALSE) |>
  mutate(growth_mm = final_mm - initial_mm)
stopifnot(nrow(seedlings) == 24, anyDuplicated(seedlings$plant_id) == 0,
          !anyNA(seedlings))
group_summary <- seedlings |>
  group_by(treatment) |>
  summarise(n = n(), mean_mm = mean(growth_mm),
            sd_mm = sd(growth_mm), .groups = "drop")
treated <- seedlings |> filter(treatment == "treated") |> pull(growth_mm)
control <- seedlings |> filter(treatment == "control") |> pull(growth_mm)
comparison <- t.test(treated, control, var.equal = FALSE,
                     alternative = "two.sided", conf.level = 0.95)
observed_difference <- mean(treated) - mean(control)
growth_plot <- ggplot(seedlings, aes(treatment, growth_mm)) +
  geom_point(position = position_jitter(width = 0.08, height = 0, seed = 16)) +
  labs(x = "Treatment group", y = "Growth over the study period (mm)") +
  theme_minimal()
ggsave(file.path(out, "day16-growth.png"), growth_plot, width = 6, height = 4)
print(group_summary)
print(observed_difference)
print(comparison)
stopifnot(abs(observed_difference - 6.2166666667) < 1e-7,
          comparison$conf.int[1] > 0,
          abs(comparison$p.value - 0.0015167) < 1e-5)

# Day 18: rows preserve plant identities; no sorting of individual columns.
paired <- read_csv("data/paired.csv", show_col_types = FALSE) |>
  mutate(change_umol_m2_s = after_umol_m2_s - before_umol_m2_s)
stopifnot(nrow(paired) == 10, anyDuplicated(paired$plant_id) == 0,
          !anyNA(paired))
paired_comparison <- t.test(paired$after_umol_m2_s, paired$before_umol_m2_s,
                            paired = TRUE, alternative = "two.sided")
change_comparison <- t.test(paired$change_umol_m2_s, mu = 0)
stopifnot(isTRUE(all.equal(paired_comparison$p.value, change_comparison$p.value)),
          abs(mean(paired$change_umol_m2_s) - 1.983) < 1e-10)
change_plot <- ggplot(paired, aes(plant_id, change_umol_m2_s)) +
  geom_hline(yintercept = 0, linetype = "dashed") + geom_point(size = 2) +
  labs(x = "Plant identifier", y = "After - before (umol m^-2 s^-1)") +
  theme_minimal()
ggsave(file.path(out, "day18-changes.png"), change_plot, width = 6, height = 4)
print(paired_comparison)

# Day 19: fit response = absorbance; invert for supported point estimates.
standards <- read_csv("data/calibration.csv", show_col_types = FALSE)
calibration_fit <- lm(absorbance ~ concentration_mg_l, data = standards)
intercept <- coef(calibration_fit)[1]
slope <- coef(calibration_fit)[2]
standards <- standards |>
  mutate(fitted_absorbance = fitted(calibration_fit), residual = residuals(calibration_fit))
unknowns <- read_csv("data/unknowns.csv", show_col_types = FALSE) |>
  mutate(within_range = absorbance >= min(standards$absorbance) &
                        absorbance <= max(standards$absorbance),
         concentration_mg_l = if_else(within_range,
                                      (absorbance - intercept) / slope, NA_real_))
stopifnot(identical(unknowns$within_range, c(TRUE, TRUE, FALSE)),
          is.na(unknowns$concentration_mg_l[3]),
          abs(unknowns$concentration_mg_l[1] - 4.1677675) < 1e-5)
if (!build_figures) write_csv(unknowns, file.path(out, "day19-unknowns.csv"))
calibration_plot <- ggplot(standards, aes(concentration_mg_l, absorbance)) +
  geom_point(size = 2) +
  geom_abline(intercept = intercept, slope = slope, colour = "steelblue") +
  labs(x = "Known concentration (mg/L)", y = "Absorbance") + theme_minimal()
residual_plot <- ggplot(standards, aes(concentration_mg_l, residual)) +
  geom_hline(yintercept = 0, linetype = "dashed") + geom_point(size = 2) +
  labs(x = "Known concentration (mg/L)", y = "Residual absorbance") + theme_minimal()
ggsave(file.path(out, "day19-calibration.png"), calibration_plot, width = 6, height = 4)
ggsave(file.path(out, "day19-residuals.png"), residual_plot, width = 6, height = 4)
print(coef(calibration_fit))
print(unknowns)

# Day 19 transfer: a new in-range diluted measurement, not extrapolated U3.
diluted_absorbance <- 0.520
dilution_factor <- 10.00 / 1.00
stopifnot(diluted_absorbance >= min(standards$absorbance),
          diluted_absorbance <= max(standards$absorbance))
diluted_mg_l <- unname((diluted_absorbance - intercept) / slope)
original_mg_l <- diluted_mg_l * dilution_factor
stopifnot(abs(diluted_mg_l - 7.404227212) < 1e-6,
          abs(original_mg_l - 74.04227212) < 1e-5,
          is.na(unknowns$concentration_mg_l[unknowns$sample_id == "U3"]))
print(c(diluted_mg_l = diluted_mg_l, original_mg_l = original_mg_l))

# Day 20: observational association, not causal manipulation.
leaves <- read_csv("data/leaf-mass.csv", show_col_types = FALSE)
leaf_fit <- lm(dry_mass_mg ~ leaf_area_cm2, data = leaves)
leaves <- leaves |>
  mutate(fitted_mass_mg = fitted(leaf_fit), residual_mg = residuals(leaf_fit))
without_a18 <- leaves |> filter(plant_id != "A18")
sensitivity_fit <- lm(dry_mass_mg ~ leaf_area_cm2, data = without_a18)
leaf_plot <- ggplot(leaves, aes(leaf_area_cm2, dry_mass_mg)) +
  geom_point(size = 2) +
  geom_abline(intercept = coef(leaf_fit)[1], slope = coef(leaf_fit)[2],
              colour = "steelblue") +
  labs(x = "Leaf area (cm^2)", y = "Leaf dry mass (mg)") + theme_minimal()
leaf_residual_plot <- ggplot(leaves, aes(leaf_area_cm2, residual_mg)) +
  geom_hline(yintercept = 0, linetype = "dashed") + geom_point(size = 2) +
  labs(x = "Leaf area (cm^2)", y = "Observed - fitted mass (mg)") + theme_minimal()
ggsave(file.path(out, "day20-leaf-line.png"), leaf_plot, width = 6, height = 4)
ggsave(file.path(out, "day20-residuals.png"), leaf_residual_plot, width = 6, height = 4)
print(coef(leaf_fit))
print(coef(sensitivity_fit))
print(coef(leaf_fit)[1] + coef(leaf_fit)[2] * 8)
stopifnot(nrow(leaves) == 18, anyDuplicated(leaves$plant_id) == 0,
          abs(unname(coef(leaf_fit)[2]) - 4.110117) < 1e-5)
cat("Week 4 reference computations and figure generation passed. Outputs:", out, "\n")

# Expanded days16–20: independent transfer, output interpretation, and checks.
root <- normalizePath(getwd())
extended_out <- file.path(root,'output','instructor-week4')
dir.create(extended_out, recursive = TRUE, showWarnings = FALSE)
transfer <- read_csv('data/seedlings-transfer.csv', show_col_types = FALSE) |>
  mutate(growth_mm = final_mm - initial_mm)
new_treated <- transfer |> filter(treatment == 'treated') |> pull(growth_mm)
new_control <- transfer |> filter(treatment == 'control') |> pull(growth_mm)
transfer_test <- t.test(new_treated,new_control)
reverse_test <- t.test(control,treated)
ci90 <- t.test(treated,control,conf.level = .90)$conf.int
ci99 <- t.test(treated,control,conf.level = .99)$conf.int
stopifnot(length(new_treated) == 9, length(new_control) == 9,
          abs(mean(new_treated)-mean(new_control)-4.2111111111) < 1e-8,
          abs(transfer_test$conf.int[1]-1.9484407) < 1e-5,
          abs(transfer_test$conf.int[2]-6.4737815) < 1e-5,
          abs(transfer_test$p.value-.0012397) < 1e-6,
          isTRUE(all.equal(as.numeric(reverse_test$conf.int),as.numeric(-rev(comparison$conf.int)))),
          abs(reverse_test$p.value-comparison$p.value) < 1e-12,
          diff(ci90) < diff(comparison$conf.int),
          diff(ci99) > diff(comparison$conf.int))
# Compare initial size and growth without pretending this is an adjusted model.
print(transfer |> group_by(treatment) |>
        summarise(n = n(), initial_mean_mm = mean(initial_mm),
                  final_mean_mm = mean(final_mm), growth_mean_mm = mean(growth_mm),
                  growth_sd_mm = sd(growth_mm), .groups = 'drop'))
wrong_sorted_change <- sort(paired$after_umol_m2_s)-sort(paired$before_umol_m2_s)
stopifnot(abs(mean(wrong_sorted_change)-mean(paired$change_umol_m2_s)) < 1e-12,
          abs(sd(wrong_sorted_change)-sd(paired$change_umol_m2_s)) > .4)
small_before <- c(5,8,6)
small_after <- c(7,9,9)
small_changes <- small_after-small_before
small_test <- t.test(small_after,small_before,paired = TRUE)
stopifnot(identical(small_changes,c(2,1,3)), mean(small_changes) == 2,
          sd(small_changes) == 1,
          abs(small_test$conf.int[1]+.4841377) < 1e-6,
          abs(small_test$conf.int[2]-4.4841377) < 1e-6)
stopifnot(max(abs((standards$absorbance-fitted(calibration_fit)) - residuals(calibration_fit))) < 1e-12)
rounded_estimate <- (.310-round(intercept,2))/round(slope,2)
stopifnot(abs(rounded_estimate-4.5) < 1e-10,
          abs(rounded_estimate-unknowns$concentration_mg_l[1]) > .3)
transfer_standards <- read_csv('data/calibration-transfer.csv',show_col_types = FALSE)
transfer_fit <- lm(absorbance~concentration_mg_l,data = transfer_standards)
transfer_unknowns <- read_csv('data/unknowns-transfer.csv',show_col_types = FALSE) |>
  mutate(in_range = absorbance >= min(transfer_standards$absorbance) &
                      absorbance <= max(transfer_standards$absorbance),
         concentration_mg_l = if_else(in_range,
           (absorbance-coef(transfer_fit)[1])/coef(transfer_fit)[2], NA_real_))
stopifnot(abs(coef(transfer_fit)[1]-.021619047619) < 1e-10,
          abs(coef(transfer_fit)[2]-.100085714286) < 1e-10,
          identical(transfer_unknowns$in_range,c(TRUE,FALSE)),
          abs(transfer_unknowns$concentration_mg_l[1]-2.48168236749) < 1e-7,
          is.na(transfer_unknowns$concentration_mg_l[2]),
          abs(coef(transfer_fit)[1]+coef(transfer_fit)[2]*transfer_unknowns$concentration_mg_l[1]-.270) < 1e-12)
write_csv(transfer_unknowns,file.path(extended_out,'day19-transfer-unknowns.csv'))
leaves <- leaves |> mutate(leaf_area_mm2 = leaf_area_cm2*100)
unit_fit <- lm(dry_mass_mg~leaf_area_mm2,data = leaves)
stopifnot(max(abs(fitted(leaf_fit)-fitted(unit_fit))) < 1e-10,
          abs(coef(unit_fit)[2]*100-coef(leaf_fit)[2]) < 1e-10)
size_fit <- lm(final_mm~initial_mm,data = transfer)
stopifnot(nrow(transfer) == 18, all(is.finite(coef(size_fit))),
          max(abs(transfer$final_mm-fitted(size_fit)-residuals(size_fit))) < 1e-10)
print(transfer_test);print(small_test);print(coef(transfer_fit));print(transfer_unknowns)
print(coef(size_fit))

# Instructor-only report writer. Students need no custom functions to do tasks.
write_expanded_report <- function(name,title,intro,code,conclusion) {
  source <- file.path(extended_out,paste0(name,'.Rmd'))
  writeLines(c('---',paste0('title: "',title,'"'),'output: html_document','---','',
               '## Question and study','',intro,'','## Reproducible analysis','',
               '```{r analysis}',deparse(substitute(code),width.cutoff = 85),'```','',
               '## Interpretation and limitations','',conclusion),source)
  rmarkdown::render(source,output_dir = extended_out,knit_root_dir = root,
                    envir = new.env(parent = globalenv()),quiet = TRUE)
}
write_expanded_report('transfer-comparison','Transfer seedlings: independent comparison',
 'Eighteen independently potted plants were randomly allocated control or treatment, nine per group. Lengths in mm were measured seven days apart. These are simulated teaching data.',
 {
  library(readr);library(dplyr);library(ggplot2)
  transfer <- read_csv('data/seedlings-transfer.csv',show_col_types = FALSE) |>
    mutate(growth_mm = final_mm-initial_mm)
  anyDuplicated(transfer$plant_id);transfer |> count(treatment);sum(is.na(transfer$growth_mm))
  transfer_summary <- transfer |> group_by(treatment) |>
    summarise(n = n(),mean_mm = mean(growth_mm),sd_mm = sd(growth_mm),.groups = 'drop')
  knitr::kable(transfer_summary,digits = 2)
  ggplot(transfer,aes(treatment,growth_mm)) +
    geom_point(position = position_jitter(width = .08,height = 0,seed = 16)) +
    labs(x = 'Allocation',y = 'Seven-day growth (mm)') + theme_minimal()
  new_treated <- transfer |> filter(treatment == 'treated') |> pull(growth_mm)
  new_control <- transfer |> filter(treatment == 'control') |> pull(growth_mm)
  mean(new_treated)-mean(new_control)
  transfer_test <- t.test(new_treated,new_control)
  transfer_test
 },
 'Treated mean growth is about 17.87 mm versus 13.66 mm for controls. The estimated treated-minus-control difference is 4.21 mm (95% interval 1.95–6.47 mm; Welch p about.00124). The interval concerns a mean difference, not individual plant spread. Generalisation depends on the design, model assumptions and these simulated conditions.')
write_expanded_report('paired-transfer','Three illustrative pairs: changes and limits',
 'Three independently sampled plants have supplied before rates 5,8,6 and after rates 7,9,9 in micromoles CO2 per square metre per second. Fixed before/after order and tiny n limit interpretation. These are illustrative values.',
 {
  library(ggplot2)
  demo <- data.frame(plant_id = c('D1','D2','D3'),
                     before_umol_m2_s = c(5,8,6),after_umol_m2_s = c(7,9,9))
  demo$change <- demo$after_umol_m2_s-demo$before_umol_m2_s
  knitr::kable(demo)
  mean(demo$change);sd(demo$change)
  ggplot(demo,aes(plant_id,change)) + geom_hline(yintercept = 0,linetype = 'dashed') +
    geom_point(size = 2) + labs(x = 'Plant ID',y = 'After minus before (umol CO2 m^-2 s^-1)') + theme_minimal()
  t.test(demo$after_umol_m2_s,demo$before_umol_m2_s,paired = TRUE)
 },
 'The changes are2,1,3, with mean 2 and SD 1 in the stated rate units. The approximate 95% mean-change interval is−0.48 to4.48. Its inclusion of zero does not prove equality. Three pairs are very limited evidence, and changing light in a fixed time order does not isolate light from all order effects.')
write_expanded_report('transfer-calibration','A second calibration with range checks',
 'Six prepared standards from 0–5 mg/L have measured absorbance. A straight line is used as a local approximation. Two unknown readings are supplied; no chemical mechanism or optical-law recall is required.',
 {
  library(readr);library(dplyr);library(ggplot2)
  standards <- read_csv('data/calibration-transfer.csv',show_col_types = FALSE)
  fit <- lm(absorbance~concentration_mg_l,data = standards)
  coef(fit)
  ggplot(standards,aes(concentration_mg_l,absorbance)) + geom_point() +
    geom_abline(intercept = coef(fit)[1],slope = coef(fit)[2]) +
    labs(x = 'Known concentration (mg/L)',y = 'Absorbance') + theme_minimal()
  standards <- mutate(standards,residual = residuals(fit))
  ggplot(standards,aes(concentration_mg_l,residual)) + geom_hline(yintercept = 0,linetype = 'dashed') +
    geom_point() + labs(x = 'Known concentration (mg/L)',y = 'Residual absorbance') + theme_minimal()
  unknowns <- read_csv('data/unknowns-transfer.csv',show_col_types = FALSE) |>
    mutate(in_range = absorbance >= min(standards$absorbance) & absorbance <= max(standards$absorbance),
           concentration_mg_l = if_else(in_range,(absorbance-coef(fit)[1])/coef(fit)[2],NA_real_))
  knitr::kable(unknowns,digits = 3)
 },
 'The new slope is about 0.10009 per mg/L and intercept about 0.02162. X1 is within range and estimates about 2.48 mg/L. X2 is outside range, so its estimate is retained as unavailable with that reason. A new supported measurement and recorded volumes would be needed for dilution correction. Full uncertainty propagation is not included.')
write_expanded_report('transfer-association','Starting and final size: descriptive association',
 'Eighteen simulated independent plants have initial and final lengths in mm and randomised allocation labels. This report explores the observational association between starting and final size, not an intervention changing initial length.',
 {
  library(readr);library(dplyr);library(ggplot2)
  transfer <- read_csv('data/seedlings-transfer.csv',show_col_types = FALSE)
  fit <- lm(final_mm~initial_mm,data = transfer)
  coef(fit);range(transfer$initial_mm)
  ggplot(transfer,aes(initial_mm,final_mm,colour = treatment)) + geom_point() +
    geom_abline(intercept = coef(fit)[1],slope = coef(fit)[2],colour = 'black') +
    labs(x = 'Initial length (mm)',y = 'Final length (mm)',colour = 'Allocation') + theme_minimal()
  transfer <- mutate(transfer,residual_mm = residuals(fit))
  ggplot(transfer,aes(initial_mm,residual_mm,colour = treatment)) +
    geom_hline(yintercept = 0,linetype = 'dashed') + geom_point() +
    labs(x = 'Initial length (mm)',y = 'Observed minus fitted final length (mm)') + theme_minimal()
 },
 'The simple combined line describes association in this sample. Allocation and other plant differences can contribute to the pattern. It neither adjusts for these factors nor establishes causation; the mean growth comparison answers a separate question. Predictions should remain within the measured starting-length range.')
cat('Expanded week4 computations and four independently renderable worked reports passed. Outputs:',extended_out,'\n')
