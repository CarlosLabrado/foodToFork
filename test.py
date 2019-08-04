import unittest

from food import Food


class TestInit(unittest.TestCase):
    _api_valid_string = 'tomato%20onion'

    def test_space_separated(self):
        credentials = None
        ingredients = 'tomato onion'
        food = Food(ingredients=ingredients, credentials=credentials)
        result = food.create_api_string(ingredients)
        self.assertEqual(result, self._api_valid_string, 'Not a valid string')

    def test_comma_separated(self):
        credentials = None
        ingredients = 'tomato,onion'
        food = Food(ingredients=ingredients, credentials=credentials)
        result = food.create_api_string(ingredients)
        self.assertEqual(result, self._api_valid_string, 'Not a valid string')

    def test_dot_separated(self):
        credentials = None
        ingredients = 'tomato.onion'
        food = Food(ingredients=ingredients, credentials=credentials)
        result = food.create_api_string(ingredients)
        self.assertEqual(result, self._api_valid_string, 'Not a valid string')

    def test_empty(self):
        credentials = None
        ingredients = 'tomato onion'
        food = Food(ingredients=ingredients, credentials=credentials)
        # we initialize with something, but pass empty string nothing to the create api string
        result = food.create_api_string('')
        self.assertIs(result, '', 'is not empty')

    def test_credentials_file_exist(self):
        credentials = 'test credential'
        ingredients = 'tomato onion'
        food = Food(ingredients=ingredients, credentials=credentials)
        result = food.get_key()
        self.assertIsNotNone(result, 'Credentials file is empty or has no api_key')


if __name__ == '__main__':
    unittest.main()
