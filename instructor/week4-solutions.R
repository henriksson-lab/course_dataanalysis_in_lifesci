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
  summarise(n = n(), mean_growth_mm = mean(growth_mm),
            sd_growth_mm = sd(growth_mm), .groups = "drop")
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
