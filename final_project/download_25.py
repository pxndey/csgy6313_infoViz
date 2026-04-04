import fastf1 as f1
import pandas as pd

f1.Cache.enable_cache('f1_cache')
years = [2023,2024,2025]
for year in years:
    session = f1.get_event_schedule(year)
    for i in range(1,session.shape[0]):
        weekend = session.get_event_by_round(i)
        race = weekend.get_race()
        race.load(telemetry=False, weather=False, messages=False)
        raceLapData = race.laps
    
        OUTPUT_FILENAME = f"data/season{year}_{weekend['Location']}.csv"
        raceLapData.to_csv(OUTPUT_FILENAME)