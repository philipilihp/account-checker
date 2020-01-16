import csv
from booking import Booking
from os import listdir
from os.path import isfile, join


def parse_all_bookings(input_dir):
    onlyfiles = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]

    all_bookings = []

    for file in onlyfiles:
        bookings = parse_bookings("../resources/input/" + file)
        all_bookings = all_bookings + bookings

    return all_bookings


def parse_bookings(csv_file):
    with open(csv_file, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')

        rows = []
        for row in csv_reader:
            rows.append(row)

        # Skip Header Lines
        rows = rows[14:]

        bookings = []
        for row in rows:
            bookings.append(Booking(row[2], row[4], float(row[5].replace(".", "").replace(",", "."))))

        print(f"Parsed {len(bookings)} bookings from {csv_file}")
        return bookings
