from datetime import datetime, timezone, timedelta
from form_submitter import submit, run_at_exact_time

# Pick a form
from forms import ive_test_form as form

def my_task():
    submit(url=form.url, data=form.data)

if __name__ == "__main__":
    # Example: run at 10:09 PM local time (UTC+8)
    target = datetime(2025, 9, 3, 22, 59, 0, tzinfo=timezone(timedelta(hours=8)))
    run_at_exact_time(target, my_task, early_offset=0.5)  # 500 ms early
    # 1.0 will arrive at 19.59.6
    # 0.5 will arrive at 20.00.0
