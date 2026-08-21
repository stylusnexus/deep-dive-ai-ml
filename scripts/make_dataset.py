#!/usr/bin/env python3
"""Generate the messy turbine dataset Block 1 works on.

Deliberately contains the problems real data has: missing values with
different mechanisms, mixed-type columns, duplicates, unit inconsistency,
outliers, a high-cardinality free-text field, an imbalanced target, and
one leaking feature. Nothing here is an accident.

Seeded, so everyone gets the same mess.
"""
import numpy as np, pandas as pd, pathlib

RNG = np.random.default_rng(20260820)
N = 6000
ROOT = pathlib.Path(__file__).resolve().parent.parent

site = RNG.choice(["Ardrossan", "Whitelee", "Clyde", "Beinn an Tuirc"], N, p=[.35, .3, .2, .15])
age = np.clip(RNG.gamma(3.2, 1.5, N), 0.1, 22).round(2)
rotor = np.clip(RNG.normal(14.5, 3.1, N), 0, 28).round(2)
vib = np.clip(RNG.gamma(2.0, 0.14, N) + age * 0.011, 0, None).round(4)
gearbox_c = np.clip(RNG.normal(64, 11, N) + vib * 22, 10, 140).round(1)
hours = (age * 8760 * RNG.uniform(0.72, 0.95, N)).round(0)

# failure risk rises with vibration, temperature and age — with real noise
logit = -4.5 + 5.2 * vib + 0.021 * (gearbox_c - 64) + 0.10 * age
fail = (RNG.uniform(size=N) < 1 / (1 + np.exp(-logit))).astype(int)

df = pd.DataFrame({
    "turbine_id": [f"T{i:05d}" for i in range(N)],
    "site": site,
    "install_date": pd.to_datetime("2026-08-01") - pd.to_timedelta((age * 365).astype(int), unit="D"),
    "age_years": age,
    "rotor_speed_rpm": rotor,
    "vibration_mm_s": vib,
    "gearbox_temp": gearbox_c,
    "operating_hours": hours,
    "last_inspector": RNG.choice(
        ["j.okafor", "J. Okafor", "m_lindqvist", "M Lindqvist", "s.tran", "S. Tran", None], N,
        p=[.19, .12, .18, .11, .2, .12, .08]),
    "failed_within_90d": fail,
})

# --- the mess, each item deliberate ---

# 1. Two sites report gearbox temperature in Fahrenheit. Same column, same units label.
f_mask = np.isin(df["site"], ["Clyde", "Beinn an Tuirc"])
df.loc[f_mask, "gearbox_temp"] = (df.loc[f_mask, "gearbox_temp"] * 9 / 5 + 32).round(1)

# 2. Missing not at random: the worst-vibrating turbines lost their sensor readings
mnar = RNG.uniform(size=N) < (df["vibration_mm_s"] / df["vibration_mm_s"].max()) * 0.30
df.loc[mnar, "vibration_mm_s"] = np.nan

# 3. Missing completely at random elsewhere
df.loc[RNG.uniform(size=N) < 0.06, "rotor_speed_rpm"] = np.nan
df.loc[RNG.uniform(size=N) < 0.04, "operating_hours"] = np.nan

# 4. operating_hours arrives as strings with thousands separators and stray units
oh = df["operating_hours"].map(lambda v: np.nan if pd.isna(v) else f"{int(v):,}")
oh.loc[RNG.choice(N, 140, replace=False)] = oh.loc[RNG.choice(N, 140, replace=False)].map(
    lambda v: f"{v} hrs" if isinstance(v, str) else v)
df["operating_hours"] = oh

# 5. Sensor glitch outliers
df.loc[RNG.choice(N, 22, replace=False), "rotor_speed_rpm"] = 9999.0

# 6. Exact duplicate rows, plus same turbine logged twice under a different id
dupes = df.sample(90, random_state=7)
relogged = df.sample(60, random_state=11).copy()
relogged["turbine_id"] = [f"T9{i:04d}" for i in range(60)]
df = pd.concat([df, dupes, relogged], ignore_index=True)

# 7. The leaking feature: only populated after a failure has been recorded
df["maintenance_ticket_raised"] = np.where(
    df["failed_within_90d"] == 1,
    RNG.choice(["URGENT", "urgent", "Urgent"], len(df)),
    RNG.choice([None, "routine"], len(df), p=[.93, .07]))

df = df.sample(frac=1, random_state=3).reset_index(drop=True)
out = ROOT / "data" / "turbine_readings.csv"
df.to_csv(out, index=False)

print(f"wrote {out.relative_to(ROOT)}  {df.shape[0]} rows x {df.shape[1]} cols")
print(f"  failure rate      : {df['failed_within_90d'].mean():.3%}")
print(f"  exact duplicates  : {df.duplicated().sum()}")
print(f"  vibration missing : {df['vibration_mm_s'].isna().mean():.1%} (not at random)")
print(f"  gearbox_temp      : mixed C/F, range {df['gearbox_temp'].min()}–{df['gearbox_temp'].max()}")
