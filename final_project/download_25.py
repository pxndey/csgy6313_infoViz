import fastf1 as f1
import pandas as pd
import os

f1.Cache.enable_cache('f1_cache')
os.makedirs('data', exist_ok=True)

years = [2023, 2024, 2025]
for year in years:
    schedule = f1.get_event_schedule(year)
    for i in range(1, schedule.shape[0]):
        weekend = schedule.get_event_by_round(i)
        OUTPUT_FILENAME = f"data/season{year}_{weekend['Location']}.csv"
        
        if os.path.exists(OUTPUT_FILENAME):
            print(f"Skipping {year} {weekend['Location']} — already exists")
            continue

        try:
            race = weekend.get_race()
            race.load(telemetry=False, weather=False, messages=False)
            race.laps.to_csv(OUTPUT_FILENAME)
            print(f"Done: {year} {weekend['Location']}")
        except Exception as e:
            print(f"FAILED: {year} {weekend['Location']} — {e}")
            continue