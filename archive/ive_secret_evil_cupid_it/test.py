import time
import requests
import ntplib
from datetime import datetime, timezone, timedelta

# User data
telegram_username = "test_tele_username"
email_address = "test@email.com"
consent = ["Okay"]

yujin_rank = ["2nd"]
gaeul_rank = ["6th"]
rei_rank = ["3rd"]
wonyoung_rank = ["1st"]
liz_rank = ["4th"]
leeseo_rank = ["5th"]

# # real
# real_url = "https://docs.google.com/forms/d/e/1FAIpQLSc_8qz6AN6qajM-m2PCDUNWtE1dcLc6LBoMGUOL_yQeChQCNA/formResponse"
# results_real = {
#     # Telegram username (required)
#     #   Option: any text
#     "entry.1967297339": telegram_username,
#     # Note that IT results are strictly based on fcfs, which means there is a chance of you getting dupes of a certain member/not getting who you want; any resubmission or altering of responses will not be taken into consideration. Please also be sure to rank all members. (required)
#     #   Options: ['Okay']
#     "entry.2069055672": consent,
#     # IT rank: Yujin  (required)
#     #   Options: ['1st', '2nd', '3rd', '4th', '5th', '6th']
#     "entry.1890100439": yujin_rank,
#     # IT rank: Gaeul (required)
#     #   Options: ['1st', '2nd', '3rd', '4th', '5th', '6th']
#     "entry.429171158": gaeul_rank,
#     # IT rank: Rei (required)
#     #   Options: ['1st', '2nd', '3rd', '4th', '5th', '6th']
#     "entry.2044954435": rei_rank,
#     # IT rank: Wonyoung (required)
#     #   Options: ['1st', '2nd', '3rd', '4th', '5th', '6th']
#     "entry.1095196868": wonyoung_rank,
#     # IT rank: Liz (required)
#     #   Options: ['1st', '2nd', '3rd', '4th', '5th', '6th']
#     "entry.1736267461": liz_rank,
#     # IT rank: Leeseo  (required)
#     #   Options: ['1st', '2nd', '3rd', '4th', '5th', '6th']
#     "entry.1554528879": leeseo_rank,
#     # Email Address (required)
#     #   Options: email address
#     "emailAddress": email_address,
# }

# test
test_url = "https://docs.google.com/forms/d/e/1FAIpQLSc62W9NtRU2DZPIFrkRY2lgrZ1K8U0NZrVBWI0CUn4lt24uiQ/formResponse"
results_test = {
    # Telegram username (required)
    #   Option: any text
    "entry.5536349": telegram_username,
    # Note that IT results are strictly based on fcfs, which means there is a chance of you getting dupes of a certain member/not getting who you want; any resubmission or altering of responses will not be taken into consideration. Please also be sure to rank all members. (required)
    #   Options: ['Okay']
    "entry.609433623": consent,
    # IT rank: Yujin (required)
    #   Options: ['1st', '2nd', '3rd', '4th', '5th', '6th']
    "entry.1876345498": yujin_rank,
    # IT rank: Gaeul (required)
    #   Options: ['1st', '2nd', '3rd', '4th', '5th', '6th']
    "entry.2043584535": gaeul_rank,
    # IT rank: Rei (required)
    #   Options: ['1st', '2nd', '3rd', '4th', '5th', '6th']
    "entry.1226703413": rei_rank,
    # IT rank: Wonyoung (required)
    #   Options: ['1st', '2nd', '3rd', '4th', '5th', '6th']
    "entry.230163185": wonyoung_rank,
    # IT rank: Liz (required)
    #   Options: ['1st', '2nd', '3rd', '4th', '5th', '6th']
    "entry.1222652786": liz_rank,
    # IT rank: Leeseo (required)
    #   Options: ['1st', '2nd', '3rd', '4th', '5th', '6th']
    "entry.621643256": leeseo_rank,
    # Email Address (required)
    #   Options: email address
    "emailAddress": email_address,
}


# ---- Networking ----
session = requests.Session()

def submit(url, data):
    try:
        r = session.post(url, data=data, timeout=3)
        r.raise_for_status()
        print("✅ Submitted successfully!")
    except Exception as e:
        print("❌ Error submitting:", e)


# ---- Time sync ----
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




if __name__ == "__main__":

    def my_task():
        submit(test_url, results_test)

    # Target UTC time
    # target = datetime(2025, 9, 3, 12, 3, 0, tzinfo=timezone.utc)
    target = datetime(2025, 9, 3, 22, 9, 0, tzinfo=timezone(timedelta(hours=8)))
    run_at_exact_time(target, my_task, early_offset=0.5)  # 500 ms early

    # def my_task():
    #     submit(real_url, results_real)

    # # Target UTC time
    # target = datetime(2025, 9, 3, 12, 00, 0, tzinfo=timezone.utc)
    # run_at_exact_time(target, my_task, early_offset=0.5)  # 500 ms early