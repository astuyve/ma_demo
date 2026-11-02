"""Extract Massachusetts age distributions (ACS 2020-2024 5-year, B01001 + B01002)
for county subdivisions (cities/towns), counties, and the state.

Usage: python3 -I scripts/build_data.py raw/acs build/ages.json
"""
import json
import sys

# B01001 age brackets: male E003-E025, female E027-E049 (same 23 brackets).
BRACKETS = [
    (0, 5), (5, 10), (10, 15), (15, 18), (18, 20), (20, 21), (21, 22), (22, 25),
    (25, 30), (30, 35), (35, 40), (40, 45), (45, 50), (50, 55), (55, 60),
    (60, 62), (62, 65), (65, 67), (67, 70), (70, 75), (75, 80), (80, 85), (85, 100),
]

PREFIXES = {"0400000US25": "state", "0500000US25": "county", "0600000US25": "town"}


def kind_of(geo_id):
    for prefix, kind in PREFIXES.items():
        if geo_id.startswith(prefix):
            return kind
    return None


def read_rows(path):
    with open(path) as f:
        header = f.readline().rstrip("\n").split("|")
        for line in f:
            if kind_of(line) is None:
                continue
            yield dict(zip(header, line.rstrip("\n").split("|")))


def main(acs_dir, out_path):
    medians = {}
    for row in read_rows(f"{acs_dir}/b01002.dat"):
        try:
            medians[row["GEO_ID"]] = float(row["B01002_E001"])
        except ValueError:
            medians[row["GEO_ID"]] = None

    out = {"brackets": BRACKETS, "state": None, "counties": {}, "towns": {}}
    for row in read_rows(f"{acs_dir}/b01001.dat"):
        geo_id = row["GEO_ID"]
        total = int(row["B01001_E001"])
        if total <= 0:
            continue
        counts = [
            int(row[f"B01001_E{3 + i:03d}"]) + int(row[f"B01001_E{27 + i:03d}"])
            for i in range(len(BRACKETS))
        ]
        rec = {"pop": total, "median": medians.get(geo_id), "counts": counts}
        kind = kind_of(geo_id)
        key = geo_id.split("US", 1)[1]
        if kind == "state":
            out["state"] = rec
        elif kind == "county":
            out["counties"][key] = rec
        else:
            out["towns"][key] = rec

    with open(out_path, "w") as f:
        json.dump(out, f, separators=(",", ":"))
    print(f"state={out['state'] is not None} counties={len(out['counties'])} towns={len(out['towns'])}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
