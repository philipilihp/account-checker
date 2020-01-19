import yaml
from category import Category

keyword_category_unknown = "Unknown"
key_category = "category"
key_recipient_keywords = "recipient-keywords"
key_reference_keywords = "reference-keywords"


def format_keywords(keywords):
    if keywords is None:
        return None

    formatted_keywords = []
    for keyword in keywords:
        formatted_keywords.append(keyword.lower())
    return formatted_keywords


def parse_categories(category_file):
    with open(category_file, 'r') as stream:
        try:

            parsed_categories = yaml.safe_load(stream)
            print(f"Parsed {len(parsed_categories)} categories from file")

            categories = []
            for category in parsed_categories:

                categories.append(Category(category[key_category],
                                           format_keywords(category[key_recipient_keywords]),
                                           format_keywords(category[key_reference_keywords])))

            return categories

        except yaml.YAMLError as exc:
            print(exc)
