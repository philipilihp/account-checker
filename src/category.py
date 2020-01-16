class Category:

    def __init__(self, name, recipient_keywords, reference_keywords):
        self.name = name

        self.recipient_keywords = recipient_keywords
        if self.recipient_keywords is None:
            self.recipient_keywords = []

        self.reference_keywords = reference_keywords
        if self.reference_keywords is None:
            self.reference_keywords = []

    def __str__(self):
        return f"{self.name}"
