import pandas


def get_apartments(conn):
    df = pandas.read_sql('''
        SELECT apartment_id, address
        FROM apartment
    ''', conn)
    return df


def get_day_apartment(conn, day, apartment):
    df = pandas.read_sql('''
        SELECT apartment_day.apartment_id as 'id', guest.name as 'guest_name', phone, address, date, state.name as 'state_name'
        FROM apartment_day
        INNER JOIN apartment
        ON apartment.apartment_id = apartment_day.apartment_id
        INNER JOIN guest
        ON guest.guest_id = apartment_day.guest_id
        INNER JOIN state
        ON state.state_id = apartment_day.state_id
        WHERE date = :day
        AND apartment_day.apartment_id = :apartment
        AND apartment_day.state_id <> 1
    ''', conn, params={"day": day, "apartment": apartment})
    return df


def get_day(conn, day):
    df = pandas.read_sql('''
        SELECT apartment_day.apartment_id as 'id', guest.name as 'guest_name', phone, address, date, state.name as 'state_name'
        FROM apartment_day
        INNER JOIN apartment
        ON apartment.apartment_id = apartment_day.apartment_id
        INNER JOIN guest
        ON guest.guest_id = apartment_day.guest_id
        INNER JOIN state
        ON state.state_id = apartment_day.state_id
        WHERE date = :day
        AND apartment_day.state_id <> 1
    ''', conn, params={"day": day})
    return df


def get_apartment(conn, apartment):
    df = pandas.read_sql('''
        SELECT apartment_day.apartment_id as 'id', guest.name as 'guest_name', phone, address, date, state.name 
        as 'state_name'
        FROM apartment_day
        INNER JOIN apartment
        ON apartment.apartment_id = apartment_day.apartment_id
        INNER JOIN guest
        ON guest.guest_id = apartment_day.guest_id
        INNER JOIN state
        ON state.state_id = apartment_day.state_id
        WHERE apartment_day.apartment_id = :apartment
        AND apartment_day.state_id <> 1
        ORDER BY date DESC
    ''', conn, params={"apartment": apartment})
    return df


def get_all(conn):
    df = pandas.read_sql('''
        SELECT apartment_day.apartment_id as 'id', guest.name as 'guest_name', phone, address, date, state.name 
        as 'state_name'
        FROM apartment_day
        INNER JOIN apartment
        ON apartment.apartment_id = apartment_day.apartment_id
        INNER JOIN guest
        ON guest.guest_id = apartment_day.guest_id
        INNER JOIN state
        ON state.state_id = apartment_day.state_id
        ORDER BY date DESC
    ''', conn)
    return df


def get_ad(month, year, conn):
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
