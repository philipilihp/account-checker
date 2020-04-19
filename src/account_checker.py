import datetime
import locale

from booking_parser import parse_all_bookings
from booking_repository import save
from booking_repository import find_all
from category_parser import parse_categories
import booking_categorizer
from booking_analyzer import sum_up_prices
import calendar
import csv

load_from_file = False
booking_path = "../resources/input/example/"

categories = parse_categories(booking_path + "categories.yaml")

if load_from_file:
    bookings = find_all()
else:

    ing_bookings = parse_all_bookings(booking_path + "bookings/ing/", 15, 0, 2, 4, 7, "%d.%m.%Y")
    sparkasse_bookings = parse_all_bookings(booking_path + "bookings/sparkasse/", 1, 1, 11, 4, 14, "%d.%m.%y")

    bookings = ing_bookings + sparkasse_bookings

    booking_categorizer.assign_category(bookings, categories)
    print(f"Save bookings")
    for booking in bookings:
        save(booking)

bookings_by_category = booking_categorizer.group_by_category(bookings, categories)

print(f"Sum up categories")
summed_categories = {}
for category in bookings_by_category:
    summed_price = sum_up_prices(bookings_by_category[category])
    summed_categories[category] = [summed_price, len(bookings_by_category[category])]

sorted_by_price = {k: v for k, v in sorted(summed_categories.items(), key=lambda item: item[1][0])}

max_category_length = max([len(category) for category in sorted_by_price])
max_item_length = max([len(str(sorted_by_price[category][1])) for category in sorted_by_price])
max_price_length = max([len(f"{sorted_by_price[category][0]:.2f}") for category in sorted_by_price])


def get_num_chars(num_char, char):
    chars = ""
    for x in range(0, num_char):
        chars = chars + char
    return chars


for category in sorted_by_price:
    price = sorted_by_price[category][0]
    num_bookings = sorted_by_price[category][1]

    points = "..." + get_num_chars(max_category_length - len(category), ".")
    points2 = "..." + get_num_chars(max_item_length + max_price_length - len(str(num_bookings)) - len(f"{price:.2f}"),
                                    ".")

    print(f"  - {category} {points} {num_bookings} {points2} {price:.2f} €")

by_cat_month = booking_categorizer.group_by_category_and_month(bookings, categories)

print("Prices per month:")

header = f"Category {get_num_chars(max_category_length - len('Category'), ' ')} "

def get_col_names(monthYears):
    col_names = []
    for monthYear in monthYears:
        month = calendar.month_name[monthYear.month][0:3]
        col_names.append(month + " " + str(monthYear.year))
    return col_names


col_names = get_col_names(by_cat_month["Unknown"].keys())
for col_name in col_names:
    header = header + get_num_chars(2, " ") + col_name

print(header + "  |     Mean       Total")

all_month_sorted = sorted(by_cat_month["Unknown"].keys())

total=0
summed_mean = 0
for category in sorted_by_price:
    line = f"{category}{get_num_chars(max_category_length - len(category), ' ')} :"

    total_cat = 0
    for month in all_month_sorted:
        price_per_month = sum_up_prices(by_cat_month[category][month])
        price_as_str = f"{price_per_month:.2f}"
        blanks = get_num_chars(8 - len(price_as_str), " ")
        line = line + f" {blanks} {price_as_str}"
        total_cat += price_per_month
    mean = total_cat / 12
    summed_mean += mean
    total += total_cat
    mean_as_str = f"{mean:.2f}"
    total_cat_as_str = f"{total_cat:.2f}"
    print(line + "  | " + get_num_chars(8 - len(mean_as_str), " ") + mean_as_str
          + get_num_chars(12 - len(total_cat_as_str), " ") + total_cat_as_str)

# sum per month:
prices = f"Sum{get_num_chars(max_category_length - 3, ' ')} :"

for month in all_month_sorted:
    price = 0
    for category in sorted_by_price:
        price += sum_up_prices(by_cat_month[category][month])

    price_as_str = f"{price:.2f}"
    blanks = get_num_chars(8 - len(price_as_str), " ")
    prices = prices + f" {blanks} {price_as_str}"

summed_mean_as_str = f"{summed_mean:.2f}"
total_as_str = f"{total:.2f}"
print(prices + "  | " + get_num_chars(8 - len(summed_mean_as_str), " ") + summed_mean_as_str
      + get_num_chars(12 - len(total_as_str), " ") + total_as_str)


def to_csv(by_cat_month):
    locale.setlocale(locale.LC_ALL, '')
    col_names = get_col_names(by_cat_month["Unknown"].keys())

    # Header
    lines = []
    header = ["Category"]
    for col_name in col_names:
        header.append(col_name)
    lines.append(header)

    for category in sorted_by_price:
        line = [category]
        for month in all_month_sorted:
            price_per_month = sum_up_prices(by_cat_month[category][month])
            price_as_str = f"{price_per_month:n}"
            line.append(price_as_str)
        lines.append(line)

    with open('output.csv', 'w', newline='\n') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_ALL)
        for line in lines:
            csv_writer.writerow(line)

to_csv(by_cat_month)

#category = "Lebensmittel"
category = "Unknown"
month = datetime.date(2020, 1, 1)
print(category)

#for booking in by_cat_month[category][month]:
for booking in bookings_by_category[category]:
    print(f"  - {booking}")
