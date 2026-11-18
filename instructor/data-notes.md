# Data production and intended repair

The student-facing dictionary is `data/README.md`. All data are synthetic.
Generate the canonical CSVs with `python3 tools/build_data.py`.

For `seedlings-messy.csv`, the documented repair is:

- P03: `Control` to `control`.
- P06: keep missing final_mm; do not substitute the canonical dataset's value.
- P15: strip the trailing space from `treated `.
- P18: remove the confirmed ` mm` suffix; parse numeric 18.7.
- P21: correct final_mm to 43.8 using source-record evidence.
- Remove the confirmed identical duplicate P01 record, leaving 24 rows and 24 IDs.

The repaired data have 12 control rows with 11 available growth measurements,
and 12 treated rows with 12 available growth measurements. Do not teach blanket
outlier removal. Later inference lessons use the complete seedlings.csv; make
the switch explicit so their sample sizes do not silently change.

The final duckweed practical has 10 available control measurements and 9
available nutrient measurements. Its teacher solution should retain F17 in the
raw table and exclude only the unavailable measurement from the analysis.

In these synthetic data, allocation is random by design even though files are
sorted by group. In a real practical, a sorted table cannot demonstrate that
allocation was random. Ask students to read the design description.
