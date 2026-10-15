import tobii_research as tr
from pylsl import StreamInfo, StreamOutlet
import time

# 1. Konfigurasi LSL Stream
# kirim 2 data: Gaze X dan Gaze Y
info = StreamInfo('TobiiGaze', 'Gaze', 2, 90, 'float32', 'myuid123')
outlet = StreamOutlet(info)

# 2. Mencari Sistem Tobii
found_trackers = tr.find_all_eyetrackers()
if not found_trackers:
    print("Tracker tidak ditemukan!")
    exit()
my_tracker = found_trackers[0]

# 3. Penambahan Fungsi untuk kirim data ke LSL
def gaze_callback(gaze_data):
    gaze_point = gaze_data['left_gaze_point_on_display_area']
    if gaze_point[0] == gaze_point[0]: # Cek bukan NaN
        # Kirim data [X, Y] ke LSL
        outlet.push_sample([gaze_point[0], gaze_point[1]])
        print(f"Mengirim ke LSL: {gaze_point[0]:.2f}, {gaze_point[1]:.2f}")

# 4. Mulai
my_tracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_callback, as_dictionary=True)

print("Streaming ke LSL dimulai... Tekan Ctrl+C untuk berhenti.")
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    my_tracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_callback)
    print("Streaming berhenti.")
