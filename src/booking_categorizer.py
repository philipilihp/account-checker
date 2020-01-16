
keyword_category_unknown = "Unknown"
key_category = "category"
key_recipient_keywords = "recipient-keywords"
key_reference_keywords = "reference-keywords"


def find_category_by_recipient(recipient, categories):
    for category in categories:
        for recipient_keyword in category.recipient_keywords:
            if recipient_keyword in recipient:
                return category
    return keyword_category_unknown


def find_category_by_reference(reference, categories):
    for category in categories:
        for reference_keyword in category.reference_keywords:
            if reference_keyword in reference:
                return category
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
        by_category[category] = []

    for booking in bookings:
        by_category[booking.category].append(booking)

    return by_category
