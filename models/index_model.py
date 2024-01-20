import pandas
import sqlite3


def get_calendar(month, year, conn):
    df = pandas.read_sql('''
        SELECT apartment_day_id, guest_id, apartment_day.apartment_id, state_id, date, price
        FROM apartment_day
        INNER JOIN apartment
        ON apartment.apartment_id = apartment_day.apartment_id
        WHERE strftime('%m', date) = :month
        AND strftime('%Y', date) = :year
        ORDER BY price, apartment_day.apartment_id, date
    ''', conn, params={"month": month, "year": year})
    return df


def get_apartments(conn):
    df = pandas.read_sql('''
        SELECT address, apartment_id
        FROM apartment
        ORDER BY price, apartment_id
    ''', conn)
    return df


# Вставка нового заселения
def insert_apartment_day(conn, apartment_id, guest_id, state_id, date):
    cursor = conn.cursor()
    print(apartment_id, guest_id, state_id, date)
    cursor.execute('''
        INSERT INTO apartment_day(guest_id, state_id) 
        VALUES (:guest_id, :state_id)
        WHERE apartment_id = :apartment_id
    ''', {"apartment_id": apartment_id, "guest_id": guest_id, "state_id": state_id, "date": date})
    conn.commit()


def insert_apartment_day(conn, apartment_id, guest_id, state_id, date):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO apartment_day(apartment_id, guest_id, state_id, date) 
        VALUES :apartment_id, :guest_id, :state_id, :date;
    ''', {"apartment_id": apartment_id, "guest_id": guest_id, "state_id": state_id, "date": date})
    conn.commit()


def update_apartment_state(conn, apartment_id, guest_id, state_id, date):
    cursor = conn.cursor()
    if state_id == 2 or state_id == 3:
        cursor.execute('''
            UPDATE apartment_day
            SET guest_id = :guest_id, state_id = :state_id
            WHERE apartment_id = :apartment_id
            AND date = :date''', {"apartment_id": apartment_id, "guest_id": guest_id, "state_id": state_id, "date": date})

    next_guest_df = pandas.read_sql('''
        SELECT apartment_day_id, guest_id
        FROM apartment_day
        WHERE apartment_id = :apartment_id
        AND date = DATE(:date, '+1 days')
    ''', conn, params={"apartment_id": apartment_id, "date": date})

    if len(next_guest_df) != 0:
        next_guest_id = next_guest_df.loc[0]["guest_id"]
        next_day_id = int(next_guest_df.loc[0]["apartment_day_id"])
    else:
        next_guest_id = None
        next_day_id = None

    last_guest_df = pandas.read_sql('''
        SELECT apartment_day_id, guest_id
        FROM apartment_day
        WHERE apartment_id = :apartment_id
        AND date = DATE(:date, '-1 days')
    ''', conn, params={"apartment_id": apartment_id, "date": date})

    last_guest_id = last_guest_df.loc[0]["guest_id"]
    last_day_id = int(last_guest_df.loc[0]["apartment_day_id"])
    print(last_guest_id)
    print(last_day_id)

    apartment_day_id = int(pandas.read_sql('''
        SELECT apartment_day_id
        FROM apartment_day
        WHERE apartment_id = :apartment_id
        AND date = :date
    ''', conn, params={"apartment_id": apartment_id, "date": date}).loc[0]["apartment_day_id"])

    print(apartment_day_id)

    if state_id == 2:

        if guest_id == last_guest_id and guest_id != next_guest_id:
            cursor.execute('''
                INSERT INTO apartment_day_work(work_id, apartment_day_id, is_done)
                VALUES (3, :apartment_day_id, 0);
                ''', {"apartment_day_id": apartment_day_id}
            )
            cursor.execute('''
                INSERT INTO apartment_day_work(work_id, apartment_day_id, is_done)
                VALUES (4, :apartment_day_id, 0);
                ''', {"apartment_day_id": apartment_day_id}
            )
            cursor.execute('''
                DELETE FROM apartment_day_work
                WHERE apartment_day_id = :apartment_day_id
                AND (work_id = 3 OR work_id = 4)
            ''', {"apartment_day_id": last_day_id})

        if guest_id != last_guest_id and guest_id == next_guest_id:
            cursor.execute('''
                INSERT INTO apartment_day_work(work_id, apartment_day_id, is_done)
                VALUES (1, :apartment_day_id, 0);
                ''', {"apartment_day_id": apartment_day_id}
            )
            cursor.execute('''
                INSERT INTO apartment_day_work(work_id, apartment_day_id, is_done)
                VALUES (2, :apartment_day_id, 0);
                ''', {"apartment_day_id": apartment_day_id}
            )
            cursor.execute('''
                DELETE FROM apartment_day_work
                WHERE apartment_day_id = :apartment_day_id
                AND (work_id = 1 OR work_id = 2)
            ''', {"apartment_day_id": next_day_id})

        if guest_id != last_guest_id and guest_id != next_guest_id:
            cursor.execute('''
                INSERT INTO apartment_day_work(work_id, apartment_day_id, is_done)
                VALUES (1, :apartment_day_id, 0);
                ''', {"apartment_day_id": apartment_day_id}
            )
            cursor.execute('''
                INSERT INTO apartment_day_work(work_id, apartment_day_id, is_done)
                VALUES (2, :apartment_day_id, 0);
                ''', {"apartment_day_id": apartment_day_id}
            )
            cursor.execute('''
                INSERT INTO apartment_day_work(work_id, apartment_day_id, is_done)
                VALUES (3, :apartment_day_id, 0);
                ''', {"apartment_day_id": apartment_day_id}
            )
            cursor.execute('''
                INSERT INTO apartment_day_work(work_id, apartment_day_id, is_done)
                VALUES (4, :apartment_day_id, 0);
                ''', {"apartment_day_id": apartment_day_id}
            )

        if guest_id == last_guest_id and guest_id == next_guest_id:
            cursor.execute('''
                DELETE FROM apartment_day_work
                WHERE apartment_day_id = :apartment_day_id
                AND (work_id = 3 OR work_id = 4)
            ''', {"apartment_day_id": last_day_id})
            cursor.execute('''
                DELETE FROM apartment_day_work
                WHERE apartment_day_id = :apartment_day_id
                AND (work_id = 1 OR work_id = 2)
            ''', {"apartment_day_id": next_day_id})

    print("case 0")
    print(guest_id)
    print(last_guest_id)
    print(next_guest_id)

    if state_id == 1:

        if guest_id == last_guest_id and guest_id != next_guest_id:
            print("case 1")
            print(guest_id)
            print(last_guest_id)
            print(next_guest_id)
            cursor.execute('''
                INSERT INTO apartment_day_work(work_id, apartment_day_id, is_done)
                VALUES (3, :apartment_day_id, 0);
                ''', {"apartment_day_id": last_day_id}
            )
            cursor.execute('''
                INSERT INTO apartment_day_work(work_id, apartment_day_id, is_done)
                VALUES (4, :apartment_day_id, 0);
                ''', {"apartment_day_id": last_day_id}
            )

        if guest_id != last_guest_id and guest_id == next_guest_id:
            print("case 2")
            print(guest_id)
            print(last_guest_id)
            print(next_guest_id)
            cursor.execute('''
                INSERT INTO apartment_day_work(work_id, apartment_day_id, is_done)
                VALUES (1, :apartment_day_id, 0);
                ''', {"apartment_day_id": next_day_id}
                           )
            cursor.execute('''
                INSERT INTO apartment_day_work(work_id, apartment_day_id, is_done)
                VALUES (2, :apartment_day_id, 0);
                ''', {"apartment_day_id": next_day_id}
                           )

        if guest_id == last_guest_id and guest_id == next_guest_id:
            print("case 3")
            cursor.execute('''
                INSERT INTO apartment_day_work(work_id, apartment_day_id, is_done)
                VALUES (3, :apartment_day_id, 0);
                ''', {"apartment_day_id": last_day_id})
            cursor.execute('''
                INSERT INTO apartment_day_work(work_id, apartment_day_id, is_done)
                VALUES (4, :apartment_day_id, 0);
                ''', {"apartment_day_id": last_day_id})
            cursor.execute('''
                INSERT INTO apartment_day_work(work_id, apartment_day_id, is_done)
                VALUES (1, :apartment_day_id, 0);
                ''', {"apartment_day_id": next_day_id})
            cursor.execute('''
                INSERT INTO apartment_day_work(work_id, apartment_day_id, is_done)
                VALUES (2, :apartment_day_id, 0);
                ''', {"apartment_day_id": next_day_id})

        cursor.execute('''
            DELETE FROM apartment_day_work
            WHERE apartment_day_id = :apartment_day_id
        ''', {"apartment_day_id": apartment_day_id})
        cursor.execute('''
            UPDATE apartment_day
            SET guest_id = :guest_id, state_id = 1
            WHERE apartment_id = :apartment_id
            AND date = :date''',
        {"apartment_id": apartment_id, "guest_id": None, "date": date})

    conn.commit()


def insert_date(conn, date):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO apartment_day(date, apartment_id, state_id)
            WITH RECURSIVE create_date(cur_date)
            AS (
                SELECT :date
                UNION ALL
                SELECT DATE(cur_date, '+1 day')
                FROM create_date
                WHERE cur_date < DATE(:date, '+1 month', '-1 day')
            )
            SELECT cur_date, apartment_id, '0'
            FROM create_date
            CROSS JOIN apartment;
    ''', {"date": date})
    conn.commit()


def get_quests(conn):
    df = pandas.read_sql('''
        SELECT guest_id, name, phone
        FROM guest
    ''', conn)
    return df


def search_guest(conn, guest_name, guest_phone):
    df = pandas.read_sql('''
        SELECT guest_id
        FROM guest
        WHERE name = :guest_name
        AND phone = :guest_phone
    ''', conn, params={"guest_name": guest_name, "guest_phone": guest_phone})
    return df


def insert_guest(conn, guest_name, guest_phone):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO guest(name, phone)
        VALUES (:guest_name, :guest_phone)
    ''', {"guest_name": guest_name, "guest_phone": guest_phone})
    conn.commit()
