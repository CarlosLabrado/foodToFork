import requests
import yaml
import argparse
import time


class Food:
    _api_key = ''
    _ingredient_string = ''
    _local_ing_list = []
    _api_ing_list = []

    def __init__(self, credentials, ingredients):
        """
        Initializes the variables either from the arguments or the command line, then calls the main func
        :param credentials: can be empty and if they are we get them from the YAML
        :param ingredients: can be empty and if they are we get them from the terminal
        """
        if credentials is None:
            self._api_key = self.get_key()
        else:
            self._api_key = credentials

        print('Welcome to food2fork python')

        # we don't want the ingredients to be spaces or empty
        if ingredients is None or ingredients == '' or ingredients.isspace():
            lock = True
            while lock:
                print('Please enter your ingredients separated by space, comma or a dot.')
                input_ing = input('Which ingredients do you have?: ')
                if input_ing is None or input_ing == '' or input_ing.isspace():
                    print('\nWe need some ingredients to proceed, please input some ingredients\n')
                    time.sleep(2)
                else:
                    lock = False
                    self._ingredient_string = self.create_api_string(ingredients=input_ing)

        else:
            self._ingredient_string = self.create_api_string(ingredients=ingredients)

        self.main_func()

    def get_key(self):
        """
        tries to  get the API KEY from the un-versioned credentials.yaml

        :return: API key
        """

        try:
            file_name = 'credentials.yaml'
            stream = open(file_name, 'r')
            keys = yaml.safe_load(stream)

            return keys['api_key']
        except yaml.YAMLError as e:
            print('Error getting the api key, could not read from the YAML: {0}'.format(e))
        except Exception as e:
            print('Error getting the api key: {0}'.format(e))

    def create_api_string(self, ingredients):
        """
        Creates a valid string to pass on the API (with the %20 instead of spaces), also populates the _local_ing_list
        with the ingredients that we are going to compare.

        :param ingredients: comma, dot or space separated ingredients
        :return: valid string for the API
        """

        split_char = None
        try:
            if ingredients.find(',') > 0:
                split_char = ','
            elif ingredients.find('.') > 0:
                split_char = '.'

            result = ''
            first = True
            ing_list = ingredients.split(split_char)
            for ingredient in ing_list:
                if not ingredient.isdigit():  # ignore numbers.
                    lc_ingredient = ingredient.lower()  # we only want to deal with lower case
                    self._local_ing_list.append(lc_ingredient)
                    if first:
                        result = lc_ingredient
                        first = False
                    else:
                        result = result + '%20' + lc_ingredient

            return result
        except Exception as e:
            print('Error trying to create the api string: {0}'.format(e))

    def get_missing_ingredients(self, recipe_json):
        """
        Gets the initial json with all the top recipes that meet our criteria and then creates a second request for
        the top recipe only that includes all the ingredients, then we compare to the received ingredients to return
        the missing ones.
        :param recipe_json: initial json with the top recipes
        :return: the missing ingredients list
        """
        try:
            ingredients = []

            if 'recipes' in recipe_json:
                recipes = recipe_json['recipes']
                if len(recipes) > 0:
                    recipe_id = recipes[0]['recipe_id']
                    print('Top recipe: {0}'.format(recipes[0]['title'].capitalize()))

                    print('Your ingredients:')
                    for local_ingredient in self._local_ing_list:
                        print('- {0}'.format(local_ingredient.capitalize()))

                    r2 = requests.get(
                        'https://www.food2fork.com/api/get?key={0}&rId={1}'.format(self._api_key, recipe_id))

                    second_request = r2.json()
                    if 'recipe' in second_request and 'ingredients' in second_request['recipe']:
                        ingredients = second_request['recipe']['ingredients']

                        for local_ing in self._local_ing_list:
                            # we create a slice copy of the list so we can remove while iterating
                            for ingredient in ingredients[:]:
                                # sometimes the requested ingredient is in plural, so we also check without the 's'
                                if local_ing in ingredient.lower() or local_ing[0:-1] in ingredient.lower():
                                    ingredients.remove(ingredient)

                else:
                    raise IndexError('No recipes found')

            return ingredients

        except IndexError as ie:
            print('Error getting the missing ingredients, the recipe list is empty: {0}'.format(ie))
        except KeyError as ke:
            print('Error getting the missing ingredients, the key does not exist: {0}'.format(ke))
        except Exception as e:
            print('Error getting the missing ingredients : {0}'.format(e))

    def main_func(self):

        try:
            r = requests.get(
                'https://www.food2fork.com/api/search?key={0}&q={1}'.format(self._api_key, self._ingredient_string))

            if r.status_code is not 200:  # we might get an error if we try a non valid key.
                raise Exception(r.text)

            recipe_json = r.json()

            if 'error' not in recipe_json:
                missing_ingredients = self.get_missing_ingredients(recipe_json)
                if missing_ingredients is not None:
                    print('Missing ingredients:')
                    for ingredient in missing_ingredients:
                        print('- {0}'.format(ingredient))

                    print('Thank you for using food2fork python.')
            else:
                if recipe_json['error'] == 'limit':
                    raise Exception('We have reach the API quota for the day.')
        except Exception as e:
            print('Main error: {0}'.format(e))


parser = argparse.ArgumentParser()

parser.add_argument('--c', help='API Credentials')
parser.add_argument('--i', help='Ingredients')

args = parser.parse_args()

food_app = Food(credentials=args.c, ingredients=args.i)
