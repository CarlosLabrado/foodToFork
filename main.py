import argparse
from food import Food

# We launch the food app from here, using the parser to get arguments in the command line when launching.
parser = argparse.ArgumentParser()

parser.add_argument('--c', help='API Credentials')
parser.add_argument('--i', help='Space separated, comma separated or dot separated Ingredients')

args = parser.parse_args()

food_app = Food(credentials=args.c, ingredients=args.i)
food_app.main_func()
