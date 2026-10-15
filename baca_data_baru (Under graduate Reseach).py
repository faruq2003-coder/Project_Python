import pyxdf
import pandas as pd

xdf_path = r"C:\Users\Victus\Pictures\Tugas Akhir\data Responden\Eytracking Collecting\Data Eye Tracking\SAM.xdf"

streams, header = pyxdf.load_xdf(xdf_path)

gaze = [s for s in streams 
        if s['info']['name'][0] == 'TobiiStreamEngine_gaze'][0]

channel_names = [
    ch['label'][0]
    for ch in gaze['info']['desc'][0]['channels'][0]['channel']
]

df = pd.DataFrame(gaze['time_series'], columns=channel_names)
df['timestamp'] = gaze['time_stamps']

df.to_csv("gaze_valid_SAM.csv", index=False)

print("✅ Berhasil mengekstrak data gaze")
print(df.head())
