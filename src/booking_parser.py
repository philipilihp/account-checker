import csv
from booking import Booking
from os import listdir
from os.path import isfile, join
from datetime import datetime


def parse_all_bookings(input_dir, offset_header, index_date, index_recipient, index_reference, index_amount, date_format):
    onlyfiles = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]

    all_bookings = []

    for file in onlyfiles:
        bookings = parse_bookings(input_dir + file, offset_header, index_date, index_recipient, index_reference, index_amount, date_format)
        all_bookings = all_bookings + bookings

    return all_bookings


def parse_bookings(csv_file, offset_header, index_date, index_recipient, index_reference, index_amount, date_format):
    with open(csv_file, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')

        rows = []
        for row in csv_reader:
            rows.append(row)

        # Skip Header Lines
        rows = rows[offset_header:]

        bookings = []
        for row in rows:
            bookings.append(Booking(datetime.strptime(row[index_date], date_format),
                                    row[index_recipient],
                                    row[index_reference],
                                    float(row[index_amount].replace(".", "").replace(",", "."))))

        print(f"Parsed {len(bookings)} bookings from {csv_file}")
        return bookings
