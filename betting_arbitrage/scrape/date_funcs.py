from datetime import datetime, timedelta


def get_datetime_from_date_str_and_time_str(date_str, time_str):
    str_combined = date_str.strip() + " " + time_str.strip()
    now = datetime.now()
    try:
        datetime_created = datetime.strptime(str_combined, "%a %d %b %H:%M")
    except ValueError:
        names_vs_numbers = {
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4,
            "Saturday": 5,
            "Sunday": 6,
        }
        if "Today" in date_str:
            date_str = date_str.replace("Today", now.strftime("%A"))
            str_combined = str_combined.replace("Today", now.strftime("%A"))
        if "Tomorrow" in date_str:
            tomorrow = now + timedelta(days=1)
            date_str = date_str.replace("Tomorrow", tomorrow.strftime("%A"))
            str_combined = str_combined.replace("Tomorrow", tomorrow.strftime("%A"))

        date_str = date_str.strip()
        day_of_week = names_vs_numbers[date_str]
        datetime_created = datetime.strptime(str_combined, "%A %H:%M")
        datetime_created = datetime(
            year=datetime.now().year,
            month=datetime.now().month,
            day=now.day
            + day_of_week
            - now.weekday()
            + (
                7 if day_of_week < now.weekday() else 0
            ),  # 15 + 1 Monday - 6 Saturday + 7 = 17
            hour=datetime_created.hour,
            minute=datetime_created.minute,
        )

    year = datetime.now().year

    return datetime(
        year=year,
        month=datetime_created.month,
        day=datetime_created.day,
        hour=datetime_created.hour,
        minute=datetime_created.minute,
    )