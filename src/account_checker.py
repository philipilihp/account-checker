from ing_parser import parse_all_bookings
from booking_repository import save
from category_parser import parse_categories
import booking_categorizer
from booking_analyzer import sum_up_prices

categories = parse_categories("../resources/input/example/categories.yaml")
bookings = parse_all_bookings("../resources/input/example/bookings/")

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

max_category_length = max([len(category.name) for category in sorted_by_price])
max_item_length = max([len(str(sorted_by_price[category][1])) for category in sorted_by_price])
max_price_length = max([len(f"{sorted_by_price[category][0]:.2f}") for category in sorted_by_price])

for category in sorted_by_price:
    price = sorted_by_price[category][0]
    num_bookings = sorted_by_price[category][1]

    points = "..."
    for x in range(0, (max_category_length - len(category.name))):
        points = points + "."

    points2 = "..."
    for x in range(0, (max_item_length + max_price_length - len(str(num_bookings)) - len(f"{price:.2f}"))):
        points2 = points2 + "."

    print(f"  - {category} {points} {num_bookings} {points2} {price:.2f} €")

#print("Unkown")
#for booking in bookings_by_category["Unknown"]:
#    print(f"  - {booking}")

