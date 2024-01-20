import sqlite3
import pandas as pd


def get_db_connection():
    return sqlite3.connect('ran_bd.sqlite')


def get_months():
    months = [
        "Январь", "Февраль", "Март",
        "Апрель", "Май", "Июнь",
        "Июль", "Август", "Сентябрь",
        "Октябрь", "Ноябрь", "Декабрь"
    ]
    values = [
        "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12"
    ]
    data = {'month': months, "value": values}
    data = pd.DataFrame(data=data)
    return data

