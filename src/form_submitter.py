import time
import requests
import ntplib
from datetime import datetime, timezone

session = requests.Session()

def submit(url, data):
    try:
        r = session.post(url, data=data, timeout=3)
        r.raise_for_status()
        print("✅ Submitted successfully!")
    except Exception as e:
        print("❌ Error submitting:", e)

def get_ntp_offset():
    """Return offset (ntp_time - local_time) in seconds."""
    client = ntplib.NTPClient()
    response = client.request("pool.ntp.org", version=3)
    ntp_time = response.tx_time
    local_time = time.time()
    return ntp_time - local_time

def run_at_exact_time(target_time_utc, func, *args, early_offset=0.2, **kwargs):
    """
    Run func at target_time_utc (UTC), but send request early by `early_offset` seconds.
    """
    offset = get_ntp_offset()
    print("🔄 NTP offset (s):", offset)

    target_epoch = target_time_utc.timestamp() - early_offset
    while True:
        now = time.time() + offset
        delay = target_epoch - now
        if delay <= 0:
            break
        if delay > 0.05:
            time.sleep(delay - 0.05)  # coarse sleep
        else:
            time.sleep(0.001)        # fine spin

    func(*args, **kwargs)
    print("⏱ Task executed at corrected time:",
          datetime.now(timezone.utc).strftime("%H:%M:%S.%f")[:-3])
