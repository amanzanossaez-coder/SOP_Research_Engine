def year_month(date_value: float) -> tuple[int, int]:

    year = int(date_value)
    month = int(round((date_value - year) * 100))

    if month < 1 or month > 12:
        raise ValueError(f"Invalid YYYY.MM month: {date_value}")

    return year, month


def months_between(start_date: float, end_date: float) -> int:

    start_year, start_month = year_month(start_date)
    end_year, end_month = year_month(end_date)

    return (
        (end_year - start_year) * 12
        + (end_month - start_month)
    )
