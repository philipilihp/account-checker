import unittest
from category_parser import parse_categories

class TestCategoryParser(unittest.TestCase):

    def test_parse_category_file(self):
        file = "../resources/input/test/categories.yaml"

        categories = parse_categories(file)

        self.assertEqual(2, len(categories))
        for category in categories:
            if category.name == "Media":
                self.assertEqual("spotify", category.recipient_keywords[0])
                self.assertEqual("netflix monthly subscription", category.reference_keywords[0])
            else:
                self.assertEqual(2, len(category.recipient_keywords))


if __name__ == '__main__':
    unittest.main()