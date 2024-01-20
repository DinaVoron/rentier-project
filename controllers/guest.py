from app import app
from flask import render_template, request
from models.guest_model import get_apartments, get_day_apartment, get_day, get_apartment, get_all, get_ad
from utils import get_db_connection


@app.route('/guest', methods=['get'])
def guest():
    conn = get_db_connection()
    df_apartments = get_apartments(conn)
    df_guests = []
    search = False
    apartment = 0
    day = ""

    if request.values.get("apartment_info") == "":
        apartment = 0
        if request.values.get("date_info"):
            search = True
            day = request.values.get("date_info")
            df_guests = get_day(conn, day)
    elif request.values.get("search_guest"):
        search = True
        if request.values.get("date_info") and request.values.get("apartment_info"):
            apartment = int(request.values.get("apartment_info"))
            day = request.values.get("date_info")
            df_guests = get_day_apartment(conn, day, apartment)
        elif request.values.get("date_info"):
            day = request.values.get("date_info")
            df_guests = get_day(conn, day)
        else:
            apartment = int(request.values.get("apartment_info"))
            df_guests = get_apartment(conn, apartment)

    if request.values.get("date_info"):
        day = request.values.get("date_info")

    if request.values.get("apartment_info"):
        apartment = int(request.values.get("apartment_info"))

    print(get_ad("01", "2024", conn).to_string())

    html = render_template(
        "guest.html",
        len=len,
        df_apartments=df_apartments,
        df_guests=df_guests,
        search=search,
        day=day,
        apartment=apartment
    )

    return html
