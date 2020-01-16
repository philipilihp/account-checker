

def sum_up_prices(bookings):
    total_price = 0
    for booking in bookings:
        total_price += booking.amount
    return total_price
