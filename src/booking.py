class Booking:

    def __init__(self, date, recipient, reference, amount, category=None):
        self.date = date
        self.recipient = recipient
        self.reference = reference
        self.amount = amount
        self.category = category

    def __str__(self):
        return f"{self.recipient} | {self.reference} | {self.amount} | {self.category}"

    def id(self):
        return f"{self.recipient}#{self.reference}#{self.amount}"
