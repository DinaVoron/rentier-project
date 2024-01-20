import pandas


def get_timetable(conn, date):
    df = pandas.read_sql('''
        SELECT apartment_day_work_id, name, address, is_done
        FROM apartment_day_work
        INNER JOIN apartment_day
        ON apartment_day.apartment_day_id = apartment_day_work.apartment_day_id
        INNER JOIN work
        ON work.work_id = apartment_day_work.work_id
        INNER JOIN apartment
        ON apartment.apartment_id = apartment_day.apartment_id
        WHERE date = :date
    ''', conn, params={"date": date})
    return df


def update_work(conn, id):
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE apartment_day_work
        SET is_done = True
        WHERE apartment_day_work.apartment_day_work_id = :id
    ''', {"id": id})
    conn.commit()
