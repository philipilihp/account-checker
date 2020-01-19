from category import Category
from dateutil.relativedelta import relativedelta
import datetime

keyword_category_unknown = "Unknown"
key_category = "category"
key_recipient_keywords = "recipient-keywords"
key_reference_keywords = "reference-keywords"


def find_category_by_recipient(recipient, categories):
    for category in categories:
        for recipient_keyword in category.recipient_keywords:
            if recipient_keyword in recipient.lower():
                return category.name
    return keyword_category_unknown


def find_category_by_reference(reference, categories):
    for category in categories:
        for reference_keyword in category.reference_keywords:
            if reference_keyword in reference.lower():
                return category.name
    return keyword_category_unknown


def assign_category(bookings, categories):
    for booking in bookings:
        category = find_category_by_recipient(booking.recipient, categories)
        if category == keyword_category_unknown:
            category = find_category_by_reference(booking.reference, categories)
        booking.category = category


def group_by_category(bookings, categories):

    by_category = {keyword_category_unknown : []}
    for category in categories:
        by_category[category.name] = []

    for booking in bookings:
        by_category[booking.category].append(booking)

    return by_category


def group_by_category_and_month(bookings, categories):

    month_of_booking = datetime.date(bookings[0].date.year, bookings[0].date.month, 1)
    min_month = month_of_booking
    max_month = month_of_booking
    for b in bookings[1:]:
        month_of_booking = datetime.date(b.date.year, b.date.month, 1)
        if month_of_booking < min_month:
            min_month = month_of_booking
        if month_of_booking > max_month:
            max_month = month_of_booking

    all_month = []
    month_of_booking = min_month
    while month_of_booking <= max_month:
        all_month.append(month_of_booking)
        month_of_booking += relativedelta(months=1)

    by_cat_by_month = {keyword_category_unknown: {}}
    for category in categories:
        by_cat_by_month[category.name] = {}

    for category in by_cat_by_month.keys():
        for m in all_month:
            by_cat_by_month[category][m] = []

    by_category = group_by_category(bookings, categories)
    for category in by_category:
        # sort list by month
        bookings = by_category[category]
        for booking in bookings:

            month = datetime.date(booking.date.year, booking.date.month, 1)
            by_cat_by_month[category][month].append(booking)

    return by_cat_by_month
