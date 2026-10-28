import argparse
import datetime
import logging

from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter

from cfg import config
from modules import db_oracle, functions

WEEK_DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


def create_excel(db_name, rows):
    if not rows:
        print("No AWR session data found for the last 7 days.")
        return False

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Sessions"
    values = [int(row[1]) for row in rows]
    minimum, maximum = min(values), max(values)
    current_day = None
    day_index = -1
    excel_row = 2

    for timestamp, count in rows[:168]:
        date_time = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        day = date_time.date()
        if day != current_day:
            current_day = day
            day_index += 1
            excel_row = 2
            hour_column = day_index * 2 + 1
            count_column = hour_column + 1
            sheet.cell(1, hour_column, WEEK_DAYS[day.weekday()] + " " + day.isoformat())
            sheet.cell(1, count_column, "Sessions")
            for column in (hour_column, count_column):
                sheet.cell(1, column).fill = PatternFill(fgColor="999999", fill_type="solid")
            sheet.column_dimensions[get_column_letter(hour_column)].width = 18
            sheet.column_dimensions[get_column_letter(count_column)].width = 12

        sheet.cell(excel_row, hour_column, date_time.strftime("%H:%M"))
        value_cell = sheet.cell(excel_row, count_column, int(count))
        value_cell.fill = PatternFill(
            fgColor=functions.GeneralFunctions.choose_color(int(count), minimum, maximum),
            fill_type="solid",
        )
        excel_row += 1

    filename = db_name + ".xlsx"
    workbook.save(filename)
    print("Excel generated:", filename)
    return True


def run():
    parser = argparse.ArgumentParser(description="Export Oracle AWR session history to Excel")
    parser.add_argument("db_name", help="Database service name from CONNECTING_STRING")
    args = parser.parse_args()

    db = db_oracle.DbOracle()
    settings = config.Config()
    central_connection = None
    target_connection = None
    try:
        central_connection = db.db_connect(
            settings.host_name, settings.db_port, settings.db_service_name,
            settings.db_user, settings.db_password,
        )
        record = db.get_connection_settings(central_connection, args.db_name)
        if record is None:
            raise ValueError("Database not found in CONNECTING_STRING: " + args.db_name)

        _, host, port, service, user, password = record
        target_connection = db.db_connect(host, port, service, user, password)
        rows = db.get_count_connection_per_hour_from_db(target_connection)
        create_excel(args.db_name, rows)
    except Exception:
        logging.exception("Session Counter failed")
        return 1
    finally:
        if target_connection is not None:
            target_connection.close()
        if central_connection is not None:
            central_connection.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
