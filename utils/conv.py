from typing import Union


def time_format(milliseconds: Union[int, float], use_names: bool = False) -> str:
    minutes, seconds = divmod(int(milliseconds / 1000), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    if use_names:

        times = []

        for time_, name in (
                (days, "ngày"),
                (hours, "giờ"),
                (minutes, "phút"),
                (seconds, "giây")
        ):
            if not time_:
                continue

            times.append(f"{time_} {name}")

        try:
            last_time = times.pop()
        except IndexError:
            last_time = None
            times = ["1 giây"]

        strings = ", ".join(t for t in times)

        if last_time:
            strings += f" và {last_time}" if strings else last_time

    else:

        strings = f"{minutes:02d}:{seconds:02d}"

        if hours:
            strings = f"{hours}:{strings}"

        if days:
            strings = (f"{days} ngày" if days > 1 else f"{days} ngày") + (f", {strings}" if strings != "00:00" else "")

    return strings

