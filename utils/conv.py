from typing import Union
from utils.loc import loc

def time_format(milliseconds: Union[int, float], use_names: bool = False, language: str = "vi") -> str:
    minutes, seconds = divmod(int(milliseconds / 1000), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    if use_names:

        times = []

        for time_, name in (
                (days, loc.get(language, 'time',"days")),
                (hours, loc.get(language, 'time',"hours")),
                (minutes, loc.get(language, 'time',"min")),
                (seconds, loc.get(language, 'time',"sec"))
        ):
            if not time_:
                continue

            times.append(f"{time_} {name}")

        try:
            last_time = times.pop()
        except IndexError:
            last_time = None
            times = ["1s"]

        strings = ", ".join(t for t in times)

        if last_time:
            strings += f" {loc.get(language, 'time','and')} {last_time}" if strings else last_time

    else:

        strings = f"{minutes:02d}:{seconds:02d}"

        if hours:
            strings = f"{hours}:{strings}"

        if days:
            strings = (f"{days} d" if days > 1 else f"{days} d") + (f", {strings}" if strings != "00:00" else "")

    return strings

