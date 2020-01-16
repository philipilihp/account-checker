from ing_parser import parse_all_bookings
from booking_repository import save
from category_parser import parse_categories
import booking_categorizer
from booking_analyzer import sum_up_prices

INPUT_BOOKINGS = "../resources/example_ing_input.csv"
CATEGORY_FILE = "../resources/example_category_keywords.yaml"

categories = parse_categories(CATEGORY_FILE)
bookings = parse_all_bookings("../resources/input/")

booking_categorizer.assign_category(bookings, categories)
print(f"Save bookings")
for booking in bookings:
    save(booking)

bookings_by_category = booking_categorizer.group_by_category(bookings, categories)

print(f"Sum up categories")
for category in bookings_by_category:
    summed_price = sum_up_prices(bookings_by_category[category])
    print(f"  - Category {category} has {len(bookings_by_category[category])} "
          f"items with total amount: {summed_price}.")
