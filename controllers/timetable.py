from app import app
from flask import render_template, request
from models.timetable_model import get_timetable, update_work
from utils import get_db_connection


@app.route('/timetable', methods=['get'])
def timetable():
    conn = get_db_connection()
    date = ""
    if request.values.get("searched_date"):
        date = request.values.get("searched_date")

    if request.values.get("done"):
        print("Done")
        update_work(conn, int(request.values.get("done")))

    df_timetable = get_timetable(conn, date)

    html = render_template(
        "timetable.html",
        df_timetable=df_timetable,
        len=len,
        date=date
    )

    return html