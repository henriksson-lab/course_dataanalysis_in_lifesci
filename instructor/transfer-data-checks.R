# Root integration checks for the additional practice datasets.
# Run from repository root. No instructor artifacts enter the student archives.
suppressPackageStartupMessages({library(readr); library(dplyr)})
transfer <- read_csv("data/seedlings-transfer.csv", show_col_types = FALSE) |>
  mutate(growth_mm = final_mm - initial_mm)
stopifnot(nrow(transfer) == 18, anyDuplicated(transfer$plant_id) == 0,
          all(table(transfer$treatment) == 9), !anyNA(transfer))
print(transfer |> group_by(treatment) |>
        summarise(n = n(), mean_mm = mean(growth_mm), sd_mm = sd(growth_mm), .groups = "drop"))

solutions <- read_csv("data/solutions.csv", show_col_types = FALSE) |>
  mutate(amount_mol = mass_g / molar_mass_g_mol,
         final_volume_l = final_volume_ml / 1000,
         concentration_mmol_l = 1000 * amount_mol / final_volume_l)
stopifnot(nrow(solutions) == 6,
          isTRUE(all.equal(solutions$concentration_mmol_l, rep(c(50, 100, 150), 2))))
print(solutions)
dilutions <- read_csv("data/dilutions.csv", show_col_types = FALSE) |>
  mutate(stock_volume_ml = target_mmol_l * final_volume_ml / stock_mmol_l,
         feasible = stock_volume_ml <= final_volume_ml & target_mmol_l <= stock_mmol_l)
stopifnot(isTRUE(all.equal(dilutions$stock_volume_ml, c(2.5, 5, 10, 100))),
          identical(dilutions$feasible, c(TRUE, TRUE, TRUE, FALSE)))
print(dilutions)

standards <- read_csv("data/calibration-transfer.csv", show_col_types = FALSE)
fit <- lm(absorbance ~ concentration_mg_l, data = standards)
unknowns <- read_csv("data/unknowns-transfer.csv", show_col_types = FALSE) |>
  mutate(in_range = absorbance >= min(standards$absorbance) & absorbance <= max(standards$absorbance),
         concentration_mg_l = if_else(in_range,
           (absorbance - coef(fit)[1]) / coef(fit)[2], NA_real_))
stopifnot(identical(unknowns$in_range, c(TRUE, FALSE)),
          is.na(unknowns$concentration_mg_l[2]))
print(coef(fit)); print(unknowns)

algae <- read_csv("data/algae.csv", show_col_types = FALSE)
stopifnot(nrow(algae) == 24, anyDuplicated(algae$culture_id) == 0,
          all(table(algae$treatment) == 12),
          is.na(algae$biomass_mg[algae$culture_id == "A19"]))
available <- algae |> filter(!is.na(biomass_mg))
reference <- available |> filter(treatment == "reference")
supplement <- available |> filter(treatment == "supplement")
stopifnot(nrow(reference) == 12, nrow(supplement) == 11)
print(algae |> group_by(treatment) |>
        summarise(n_started = n(), n_available = sum(!is.na(biomass_mg)),
                  mean_mg = mean(biomass_mg, na.rm = TRUE),
                  sd_mg = sd(biomass_mg, na.rm = TRUE), .groups = "drop"))
print(t.test(supplement$biomass_mg, reference$biomass_mg))
cat("Additional practice datasets and their numerical anchors verified.\n")
