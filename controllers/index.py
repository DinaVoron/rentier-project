from app import app
from flask import render_template, request, session
from utils import get_db_connection, get_months
from models.index_model import get_calendar, get_apartments, insert_apartment_day, update_apartment_state, insert_date
from models.index_model import get_quests, search_guest, insert_guest


def insert_date_format(year, month, day):
    if int(day) < 10:
        date_insert = year + "-" + month + "-" + "0" + day
    else:
        date_insert = year + "-" + month + "-" + day
    return date_insert


def get_user_id(conn, name, phone):
    res = search_guest(conn, name, phone)
    if len(res) == 0:
        insert_guest(conn, name, phone)
        res = search_guest(conn, name, phone)
    return res.loc[0]["guest_id"]


@app.route('/', methods=['get'])
def index():
    conn = get_db_connection()
    df_apartments = get_apartments(conn)
    df_months = get_months()
    df_guests = get_quests(conn)
    guest_name = ""
    guest_phone = ""

    if request.values.get("booking_type"):
        booking_state = int(request.values.get("booking_type"))
    if request.values.get("get_calendar"):
        session["month_selected"] = request.values.get("month")
        session["year_selected"] = request.values.get("year")
    elif request.values.get("add_booking"):
        apartment_date = request.values.get("add_booking").split(" ")
        date_insert = insert_date_format(session["year_selected"], session["month_selected"], apartment_date[1])
        if booking_state == 0:
            user_id = int(get_user_id(conn, request.values.get("guest_name"), request.values.get("guest_phone")))
            update_apartment_state(conn, int(apartment_date[0]), user_id, booking_state + 1, date_insert)
        elif request.values.get("guest_name") and request.values.get("guest_phone"):
            user_id = int(get_user_id(conn, request.values.get("guest_name"), request.values.get("guest_phone")))
            update_apartment_state(conn, int(apartment_date[0]), user_id, booking_state + 1, date_insert)
    else:
        session["month_selected"] = "01"
        session["year_selected"] = "2024"
        booking_state = 1

    if request.values.get("guest_name"):
        guest_name = request.values.get("guest_name")

    if request.values.get("guest_phone"):
        guest_phone = request.values.get("guest_phone")

    df_calendar = get_calendar(session["month_selected"], session["year_selected"], conn)

    if len(df_calendar) == 0:
        new_date = session["year_selected"] + "-" + session["month_selected"] + "-01"
        insert_date(conn, new_date)
        df_calendar = get_calendar(session["month_selected"], session["year_selected"], conn)

    html = render_template(
        'index.html',
        df_calendar=df_calendar,
        df_apartments=df_apartments,
        len=len,
        size=int(len(df_calendar)/len(df_apartments))+1,
        year_selected=int(session["year_selected"]),
        month_selected=session["month_selected"],
        df_months=df_months,
        df_guests=df_guests,
        type_selected=booking_state,
        guest_name=guest_name,
        guest_phone=guest_phone
    )

    return html
