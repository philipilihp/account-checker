import os.path
from ing_parser import Booking
from datetime import datetime

BOOKINGS_CSV_FILE = "../resources/bookings.csv"


def csv_header():
    return "Date;Recipient;Reference;Amount;Category\n"


def to_csv(booking):
    category = ""
    if booking.category is not None:
        category = booking.category

    return f"{booking.date.strftime('%d.%m.%Y')};{booking.recipient};{booking.reference};{booking.amount};{category}\n"


def from_csv(line):
    values = line.split(";")
    return Booking(datetime.strptime(values[0], "%d.%m.%Y"),
                   values[1], values[2], float(values[3]), values[4].replace("\n", ""))


def write_initial_file():
    file = open(BOOKINGS_CSV_FILE, "w")
    file.write(csv_header())
    file.close()


def read_all_lines():
    with open(BOOKINGS_CSV_FILE, "r") as file:
        lines = file.readlines()
        file.close()
    return lines


def write_all_line(lines):
    with open(BOOKINGS_CSV_FILE, "w") as file:
        for line in lines:
            file.write(line)
        file.close()


def append_line(line):
    with open(BOOKINGS_CSV_FILE, "a") as file:
        file.write(line)
        file.close()


def update_line(old_line, new_file):
    lines = read_all_lines()
    lines.remove(old_line)
    lines.append(new_file)
    write_all_line(lines)


def insert(booking):
    print(f"  - Insert {booking}")
    append_line(to_csv(booking))


def update(old_booking, new_booking):
    old_line = to_csv(old_booking)
    new_line = to_csv(new_booking)

    if old_line != new_line:
        print(f"  - Update {new_booking}")
        update_line(old_line, new_line)


def find_all():
    lines = read_all_lines()
    lines.pop(0)  # Remove Header Line

    bookings = []
    for line in lines:
        booking = from_csv(line)
        bookings.append(booking)
    return bookings


def find_by_id(booking):
    bookings = find_all()

    for booking_in_file in bookings:
        if booking_in_file.id() == booking.id():
            return booking_in_file

    return None


def save(booking):
    if not os.path.isfile(BOOKINGS_CSV_FILE):
        write_initial_file()

    booking_in_file = find_by_id(booking)

    if booking_in_file is None:
        insert(booking)
    else:
        update(booking_in_file, booking)
