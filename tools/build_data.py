"""Generate small, synthetic teaching datasets using only the Python stdlib."""

from pathlib import Path
import csv
import random

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)


def write(name, fields, rows):
    with (DATA / name).open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(fields)
        writer.writerows(rows)


rng = random.Random(431)
seedlings = []
for index in range(24):
    group = "control" if index < 12 else "treated"
    initial = round(rng.uniform(18, 26), 1)
    growth = round(rng.gauss(17 if group == "control" else 23, 4), 1)
    seedlings.append([f"P{index + 1:02d}", group, initial, round(initial + growth, 1)])
fields = ["plant_id", "treatment", "initial_mm", "final_mm"]
write("seedlings.csv", fields, seedlings)
messy = [row.copy() for row in seedlings]
messy[2][1] = "Control"
messy[5][3] = ""
messy[14][1] = "treated "
messy[17][2] = f"{messy[17][2]} mm"
messy[20][3] = round(messy[20][3] / 10, 2)
messy.append(messy[0].copy())
write("seedlings-messy.csv", fields, messy)

write("calibration.csv", ["standard_id", "concentration_mg_l", "absorbance"], [
    [f"S{i + 1}", concentration, absorbance]
    for i, (concentration, absorbance) in enumerate(zip(
        [0, 2, 4, 6, 8, 10], [0.041, 0.164, 0.307, 0.422, 0.563, 0.687]
    ))
])
write("unknowns.csv", ["sample_id", "absorbance"], [
    ["U1", 0.310], ["U2", 0.520], ["U3", 0.900]
])

paired = []
for index in range(10):
    before = round(rng.uniform(4.5, 9.0), 2)
    after = round(before + rng.gauss(1.2, 1.0), 2)
    paired.append([f"L{index + 1:02d}", before, after])
write("paired.csv", ["plant_id", "before_umol_m2_s", "after_umol_m2_s"], paired)

leaf = []
for index in range(18):
    area = round(3 + index * 0.7 + rng.uniform(-0.25, 0.25), 2)
    mass = round(8 + 4.2 * area + rng.gauss(0, 5), 2)
    leaf.append([f"A{index + 1:02d}", area, mass])
write("leaf-mass.csv", ["plant_id", "leaf_area_cm2", "dry_mass_mg"], leaf)

duckweed = []
for index in range(20):
    group = "control" if index < 10 else "nutrient"
    biomass = round(rng.gauss(35 if group == "control" else 41, 5), 1)
    duckweed.append([f"F{index + 1:02d}", group, "" if index == 16 else biomass])
write("duckweed.csv", ["flask_id", "treatment", "biomass_mg"], duckweed)

(DATA / "dna.txt").write_text("ACGTACGTTTAGCCGATATACCGGTTAAACGTACGCGTAT\n")
write("pixels.csv", [f"x{i + 1}" for i in range(8)], [
    [210 if (row - 3.5) ** 2 + (col - 3.5) ** 2 < 7 else 25 for col in range(8)]
    for row in range(8)
])
print("Generated eight CSV datasets and a DNA text file in data/.")
