import yaml
from category import Category

keyword_category_unknown = "Unknown"
key_category = "category"
key_recipient_keywords = "recipient-keywords"
key_reference_keywords = "reference-keywords"


def parse_categories(category_file):
    with open(category_file, 'r') as stream:
        try:

            parsed_categories = yaml.safe_load(stream)
            print(f"Parsed {len(parsed_categories)} categories from file")

            categories = []
            for category in parsed_categories:
                categories.append(Category(category[key_category],
                                           category[key_recipient_keywords],
                                           category[key_reference_keywords]))

            print(f"Created {len(parsed_categories)} categories")
            return categories

        except yaml.YAMLError as exc:
            print(exc)
