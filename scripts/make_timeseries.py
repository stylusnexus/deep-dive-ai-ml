#!/usr/bin/env python3
"""Daily sensor readings per turbine — the time-structured companion to the
cross-sectional dataset. Carries trend, weekly seasonality, a regime change,
gaps, and failures that follow a rising-vibration run-up.

Seeded, so everyone gets the same series.
"""
import numpy as np, pandas as pd, pathlib

RNG = np.random.default_rng(20260821)
ROOT = pathlib.Path(__file__).resolve().parent.parent
DAYS, N_TURBINES = 730, 40
start = pd.Timestamp("2024-09-01")

rows = []
for t in range(N_TURBINES):
    tid = f"T{t:03d}"
    base_vib = RNG.uniform(0.18, 0.34)
    drift = RNG.uniform(0.00004, 0.00013)          # slow mechanical degradation
    fail_days = sorted(RNG.choice(range(120, DAYS), size=RNG.integers(1, 4), replace=False))

    for d in range(DAYS):
        date = start + pd.Timedelta(days=d)
        vib = base_vib + drift * d
        vib += 0.030 * np.sin(2 * np.pi * d / 7)   # weekly load pattern
        if d > 400:                                 # sensor recalibrated: a regime change
            vib += 0.05
        # failures are preceded by a rising run-up, which is the learnable signal
        for f in fail_days:
            if 0 < f - d <= 14:
                vib += 0.11 * (1 - (f - d) / 14) ** 2
        vib += RNG.normal(0, 0.022)
        rows.append({
            "turbine_id": tid,
            "date": date,
            "vibration_mm_s": round(max(vib, 0.01), 4),
            "gearbox_temp_c": round(58 + 22 * vib + RNG.normal(0, 2.6), 1),
            "power_output_kw": round(max(RNG.normal(1850, 240) - 900 * max(vib - 0.4, 0), 0), 1),
            "failure": int(d in fail_days),
        })

df = pd.DataFrame(rows)

# real series have gaps — a fortnight of telemetry loss at one site
gap = (df["turbine_id"].isin([f"T{i:03d}" for i in range(0, 6)]) &
       df["date"].between("2025-06-02", "2025-06-15"))
df = df.loc[~gap].reset_index(drop=True)

out = ROOT / "data" / "turbine_daily.csv"
df.to_csv(out, index=False)
print(f"wrote {out.relative_to(ROOT)}  {len(df):,} rows x {df.shape[1]} cols")
print(f"  turbines        : {df['turbine_id'].nunique()}")
print(f"  date range      : {df['date'].min().date()} to {df['date'].max().date()}")
print(f"  failure days    : {df['failure'].sum()} ({df['failure'].mean():.3%} of rows)")
print(f"  regime change   : day 400 (sensor recalibration, +0.05 mm/s)")
print(f"  telemetry gap   : 6 turbines, 2025-06-02 to 06-15")
