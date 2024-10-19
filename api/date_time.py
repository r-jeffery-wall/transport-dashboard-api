from datetime import datetime
from zoneinfo import ZoneInfo

def get_date_time_string():
    date_time = datetime.now(ZoneInfo("Europe/London")) # Replace with your timezone as appropriate.
    return date_time.strftime("%A %-d %B %Y  %-H:%M")


if __name__ == "__main__":
    print(get_date_time_string())
