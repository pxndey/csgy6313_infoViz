import pandas as pd
import glob
import os

def clean_race(filepath):
    """Take raw FastF1 CSV, return cleaned dataframe with race metadata."""
    df = pd.read_csv(filepath)
    df = df.drop(columns=['Unnamed: 0'], errors='ignore')

    # parse lap time
    df['LapTime'] = pd.to_timedelta(df['LapTime']).dt.total_seconds()

    # filters: is accurate, green flag conditions, no pit laps
    df = df[df['IsAccurate'] == True]
    df = df[df['TrackStatus'] == 1]
    df = df[df['PitInTime'].isna() & df['PitOutTime'].isna()]

    # tag with race identity from filename
    fname = os.path.basename(filepath).replace('.csv', '')
    parts = fname.split('_')
    df['Season'] = parts[0]      # e.g. "season25"
    df['Race'] = parts[1]        # e.g. "Monaco"

    # keep only the important columns
    keep = ['Season', 'Race', 'Driver', 'Team', 'LapNumber', 'Stint',
            'TyreLife', 'Compound', 'FreshTyre', 'LapTime', 'Position']
    df = df[keep]

    return df

# loop every CSV in your scrape folder
csv_files = glob.glob('data/*.csv')   # fix this path
print(f"Found {len(csv_files)} race files")

cleaned = []
for fp in csv_files:
    try:
        cdf = clean_race(fp)
        cleaned.append(cdf)
        print(f"  {os.path.basename(fp)}: {len(cdf)} clean laps")
    except Exception as e:
        print(f"  FAILED {os.path.basename(fp)}: {e}")

master = pd.concat(cleaned, ignore_index=True)
print(f"\nMaster dataframe: {master.shape}")
print(master.head())

master.to_csv('clean.csv', index=False)