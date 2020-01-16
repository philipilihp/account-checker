import csv
from booking import Booking


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

        print(f"Parsed {len(bookings)} bookings from file.")
        return bookings
